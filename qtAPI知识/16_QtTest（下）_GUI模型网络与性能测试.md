# Qt Test（下）：GUI、模型、网络与性能测试

> 本篇承接《16_QtTest（上）_单元测试与数据驱动测试》，聚焦真实应用中最容易“偶尔失败”的测试：窗口交互、异步事件、Model/View 契约、网络替身、日志断言和性能基准。示例是可复制的代码片段，不包含完整工程文件。

## 1. 为什么 GUI 测试比普通单元测试难

普通函数通常满足“输入确定，输出确定”。GUI 测试还受到以下状态影响：

- 控件是否创建、显示并获得焦点；
- 事件是否已经进入事件循环；
- 平台窗口系统是否真的暴露窗口；
- 字体、屏幕缩放、主题和语言环境；
- 动画、定时器、网络回调是否在断言前完成。

因此 GUI 测试的核心不是“多等几秒”，而是等待可观察条件，并控制外部状态。

## 2. GUI 测试的运行环境

### 2.1 CMake 配置片段

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Test)

target_link_libraries(tst_login PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
    Qt6::Test
)
```

测试程序必须使用 `QTEST_GUILESS_MAIN`、`QTEST_MAIN` 或手动创建 `QApplication`。只测试纯 QObject 时不需要 GUI；只要实例化 QWidget，就应使用 GUI 应用对象。

### 2.2 三种入口宏

```cpp
#include <QtTest>

class CoreTest : public QObject
{
    Q_OBJECT
private slots:
    void value_data();
    void value();
};

QTEST_GUILESS_MAIN(CoreTest) // 不创建 QApplication，适合 Core 测试
```

```cpp
#include <QtTest>
#include <QWidget>

class WidgetTest : public QObject
{
    Q_OBJECT
private slots:
    void buttonClick();
};

QTEST_MAIN(WidgetTest) // 创建 QApplication，适合 QWidget/GUI
```

`QTEST_APPLESS_MAIN` 适合没有事件循环需求的极简测试。遇到 `QWidget: Cannot create a QWidget without QApplication`，优先检查入口宏是否正确，而不是在测试函数中临时补建应用对象。

### 2.3 无显示器环境

在 CI 或容器中可以设置平台插件：

```text
QT_QPA_PLATFORM=offscreen
```

这只能解决“没有物理显示器”的启动问题，不能保证像素、字体和窗口管理行为与桌面系统完全一致。截图测试应固定平台、字体和缩放策略。

## 3. 控件测试：从状态到用户动作

### 3.1 先测可观察行为

不要测试按钮的私有布局坐标，也不要依赖内部子控件名称。测试用户能看到或业务能观察到的结果，例如：点击“登录”后发出信号、错误标签出现、按钮变为禁用。

```cpp
#include <QtTest>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QSignalSpy>
#include <QVBoxLayout>
#include <QWidget>

class LoginWidget : public QWidget
{
    Q_OBJECT
public:
    explicit LoginWidget(QWidget *parent = nullptr) : QWidget(parent)
    {
        user = new QLineEdit(this);
        submit = new QPushButton(tr("登录"), this);
        message = new QLabel(this);
        auto *layout = new QVBoxLayout(this);
        layout->addWidget(user);
        layout->addWidget(submit);
        layout->addWidget(message);
        connect(submit, &QPushButton::clicked, this, [this] {
            message->setText(user->text().isEmpty() ? tr("请输入用户名") : tr("已提交"));
        });
    }
    QLineEdit *user;
    QPushButton *submit;
    QLabel *message;
};

class LoginWidgetTest : public QObject
{
    Q_OBJECT
private slots:
    void emptyUserShowsMessage()
    {
        LoginWidget widget;
        widget.show();
        QVERIFY(QTest::qWaitForWindowExposed(&widget));

        QSignalSpy clicked(&widget, &QPushButton::clicked);
        QTest::mouseClick(widget.submit, Qt::LeftButton);

        QCOMPARE(clicked.count(), 1);
        QCOMPARE(widget.message->text(), QStringLiteral("请输入用户名"));
    }
};

QTEST_MAIN(LoginWidgetTest)
```

`QTest::mouseClick()` 可以接收 `QWidget*` 或 `QWindow*`，还可以传入按钮、修饰键、位置和延迟。`QTest::keyClick()`、`QTest::keyClicks()` 用于键盘动作。动作完成后，若结果由 queued signal 或定时器驱动，使用 `QTRY_VERIFY`/`QTRY_COMPARE` 等待条件。

### 3.2 焦点和窗口暴露

```cpp
widget.show();
QVERIFY(QTest::qWaitForWindowExposed(&widget));
widget.user->setFocus();
QVERIFY(widget.user->hasFocus());
QTest::keyClicks(widget.user, QStringLiteral("alice"));
QCOMPARE(widget.user->text(), QStringLiteral("alice"));
```

`show()` 只是请求显示，窗口可能尚未由窗口系统暴露。Qt 6.10 提供了 `QTest::qWaitForWindowExposed()`，可等待 QWidget 或 QWindow 暴露；旧版本可使用 `QTest::qWaitForWindowShown()`（具体可用性依 Qt 版本而定）。

不要把固定 `qWait(500)` 当作同步机制。固定延时既可能让测试变慢，也可能在负载较高时仍然不够。

### 3.3 异步条件等待

```cpp
QTRY_VERIFY_WITH_TIMEOUT(controller->isReady(), 2000);
QTRY_COMPARE_WITH_TIMEOUT(controller->state(), State::Ready, 2000);
```

`QTRY_*` 会反复处理事件并检查条件，适合信号、定时器和网络回调。超时应短而明确，并在失败信息中保留当前状态：

```cpp
QTRY_VERIFY2_WITH_TIMEOUT(controller->isReady(),
                          qPrintable(controller->errorString()), 2000);
```

注意：条件本身必须是可重复、无副作用的查询。不要在 `QTRY_VERIFY` 条件里执行会修改状态的操作。

## 4. Model/View 测试

### 4.1 模型契约

自定义 `QAbstractItemModel` 的问题通常不是某一个值错，而是索引、父子关系、行列计数和信号顺序不一致。重点检查：

1. `index()` 返回的索引必须与 `parent()` 互相匹配；
2. `rowCount(parent)`、`columnCount(parent)` 在所有父索引下都有效；
3. 插入、删除、移动操作必须使用正确的 `begin...`/`end...` 配对；
4. `dataChanged` 的范围、角色和索引必须准确；
5. 非法编辑必须返回 `false`，不能悄悄改动数据。

### 4.2 QAbstractItemModelTester

Qt Test 提供 `QAbstractItemModelTester`，会读取模型元数据、执行非破坏性检查，并在模型变化后重复检查。它还会尝试部分非法修改；健壮模型应拒绝这些修改且不改变数据。

```cpp
#include <QAbstractItemModelTester>
#include <QtTest>

class ModelTest : public QObject
{
    Q_OBJECT
private slots:
    void modelContract()
    {
        auto *model = new MyModel(this);
        auto *tester = new QAbstractItemModelTester(
            model,
            QAbstractItemModelTester::FailureReportingMode::QtTest,
            this);
        QVERIFY(tester->model() == model);
        tester->setUseFetchMore(true); // 模型实现了 fetchMore 时启用
    }
};

QTEST_GUILESS_MAIN(ModelTest)
```

`FailureReportingMode` 有三种模式：

- `QtTest`：作为 Qt Test 失败报告；
- `Warning`：写入 `qt.modeltest` 日志类别；
- `Fatal`：通过 `qFatal()` 立即终止。

它不能替代业务测试，也不会进行有意义的破坏性测试。仍需单独验证排序、编辑、撤销、持久化和并发变更。

### 4.3 视图中的用户流程

```cpp
QTableView view;
MyModel model;
view.setModel(&model);
view.show();
QVERIFY(QTest::qWaitForWindowExposed(&view));

QModelIndex first = model.index(0, 0);
QVERIFY(first.isValid());
view.setCurrentIndex(first);
QCOMPARE(view.currentIndex(), first);
```

代理编辑通常需要三层断言：编辑器是否创建、提交后模型是否改变、取消后模型是否保持原值。不要只断言编辑器存在，因为代理可能创建了编辑器却没有正确提交。

## 5. 网络测试：让异步变得可控

### 5.1 不直接依赖公网

真实公网测试会受到 DNS、代理、证书、服务限流和时区影响。将网络访问封装为接口，在单元测试中注入 fake；把少量真实服务检查放在单独的集成测试作业。

```cpp
class HttpClient : public QObject
{
    Q_OBJECT
public:
    explicit HttpClient(QNetworkAccessManager *manager, QObject *parent = nullptr)
        : QObject(parent), manager(manager) {}

    void get(const QUrl &url)
    {
        QNetworkReply *reply = manager->get(QNetworkRequest(url));
        connect(reply, &QNetworkReply::finished, this, [this, reply] {
            const QByteArray body = reply->readAll();
            emit completed(reply->error(), body);
            reply->deleteLater();
        });
    }

signals:
    void completed(QNetworkReply::NetworkError error, QByteArray body);

private:
    QNetworkAccessManager *manager;
};
```

### 5.2 QNetworkAccessManager 的替身边界

Qt 没有内置一个可以直接“返回预设 HTTP 响应”的通用 fake `QNetworkAccessManager`。常见做法是：

- 在业务层抽象 `IHttpClient`，测试注入内存实现；
- 使用本地 HTTP 测试服务器，验证请求路径、方法、头和响应；
- 对 `QNetworkReply` 做专门的 fake，但要完整模拟信号、错误和生命周期。

第一种方式最适合快速单元测试，第二种适合协议集成测试。不要为了测试而把生产代码改成读取全局变量。

### 5.3 等待网络结果

```cpp
QSignalSpy spy(client, &HttpClient::completed);
client->get(QUrl(QStringLiteral("http://127.0.0.1:18080/data")));

QTRY_COMPARE_WITH_TIMEOUT(spy.count(), 1, 3000);
const auto args = spy.takeFirst();
QCOMPARE(args.at(0).value<QNetworkReply::NetworkError>(),
         QNetworkReply::NoError);
QCOMPARE(args.at(1).toByteArray(), QByteArray("{\"ok\":true}"));
```

测试错误路径同样重要：连接拒绝、超时、取消、非 2xx 状态、无效 JSON、重复完成信号。每个测试都应能独立结束 reply，避免上一个测试的异步回调污染下一个测试。

## 6. 日志、警告和失败诊断

### 6.1 将意外警告当作失败

```cpp
void warningFreePath()
{
    QTest::failOnWarning(); // Qt 6.8：本测试中出现 warning 即失败
    codeUnderTest();
}
```

也可以只匹配特定消息：

```cpp
QTest::failOnWarning(QRegularExpression(QStringLiteral("invalid token")));
```

该机制适合捕捉未连接信号、非法布局、资源加载失败等问题，但要避免把第三方库无法避免的警告纳入过宽匹配。

### 6.2 诊断信息

```cpp
QVERIFY2(reply != nullptr, qPrintable(QStringLiteral("URL=%1").arg(url.toString())));
QCOMPARE_EQ(actual, expected); // 选择能显示差异的断言
```

为异步失败记录 URL、请求编号、当前状态和错误字符串。这样比单独输出“超时”更容易定位。

## 7. 性能基准测试

### 7.1 QBENCHMARK 的语义

```cpp
void parseLargePayload()
{
    const QByteArray payload = makePayload(10000);
    QJsonDocument result;

    QBENCHMARK {
        result = QJsonDocument::fromJson(payload);
    }

    QVERIFY(!result.isNull()); // 防止测到错误快速返回路径
}
```

`QBENCHMARK` 中的代码可能被重复执行，具体次数由测量后端决定。一个测试函数或一个数据标签只应有一个基准区块。准备数据、分配固定输入和结果验证尽量放在区块外或之后，避免把测试准备成本混进指标。

### 7.2 QBENCHMARK_ONCE

`QBENCHMARK_ONCE` 只运行一次测量区块，适合初始化成本、一次性 I/O 或不适合重复执行的操作。一次测量的噪声更大，不能直接与稳定循环基准混为一谈。

```cpp
QBENCHMARK_ONCE {
    cache->warmUp();
}
```

### 7.3 让基准可比较

- 固定输入规模并使用数据驱动标签区分规模；
- 不在基准区块内打印日志、访问随机设备或等待网络；
- 在同一构建类型和相近机器上比较；
- 保留基准后端、单位和提交版本；
- 发生异常路径时用断言标记结果无效。

```cpp
void sort_data();
void sort()
{
    QFETCH(QVector<int>, values);
    QBENCHMARK {
        auto copy = values;
        std::sort(copy.begin(), copy.end());
    }
    QVERIFY(true);
}
```

## 8. CTest 与 CI 集成

### 8.1 CMake 注册测试

```cmake
include(CTest)
enable_testing()

add_test(NAME tst_login COMMAND tst_login -platform offscreen)
set_tests_properties(tst_login PROPERTIES
    TIMEOUT 30
    ENVIRONMENT "QT_QPA_PLATFORM=offscreen")
```

可按标签拆分快速测试、集成测试和基准测试。基准通常不应阻塞普通提交门禁，而应在专门流水线记录趋势。

### 8.2 命令行选项

```text
tst_login -functions
tst_login emptyUserShowsMessage
tst_login -v2
tst_login -o result.xml,junitxml
tst_login -xml
```

将 XML/JUnit 输出交给 CI 测试报告；失败时保留标准输出、平台插件日志和崩溃转储。

## 9. 常见失败模式

| 症状 | 常见原因 | 修复思路 |
| --- | --- | --- |
| 偶发超时 | 用固定延时等待异步回调 | 改为 `QTRY_*` 并设置明确超时 |
| 点击无效 | 窗口未暴露或控件不可见 | `show()` 后等待 `qWaitForWindowExposed()` |
| 文本输入错乱 | 没有焦点、输入法或平台差异 | 显式 `setFocus()`，优先测试业务结果 |
| 模型测试崩溃 | begin/end 信号不配对 | 检查行列范围和父索引 |
| 网络测试互相影响 | reply 未删除、全局 manager 复用 | 每个测试独立 fixture，`deleteLater()` 并清理事件 |
| 基准突然变快 | 测到了错误/缓存路径 | 基准后增加结果验证 |
| CI 找不到平台插件 | 未设置 QPA 平台 | 设置 `QT_QPA_PLATFORM=offscreen` 并检查插件部署 |

## 10. 一套可复用的测试结构

```cpp
class FeatureTest : public QObject
{
    Q_OBJECT
private slots:
    void initTestCase();
    void cleanupTestCase();
    void init();
    void cleanup();
    void happyPath();
    void errorPath_data();
    void errorPath();
    void performance_data();
    void performance();
};
```

推荐顺序是：

1. fixture 创建依赖；
2. 测试单一行为；
3. 用信号、模型数据或可见文本断言结果；
4. 异步路径使用条件等待；
5. 失败时输出上下文；
6. 测试结束清理所有对象和临时资源。

## 11. 自测题

1. 为什么 `show()` 后还可能不能立即 `mouseClick()`？
2. `QTRY_COMPARE` 与固定 `qWait()` 的核心差异是什么？
3. `QAbstractItemModelTester` 能否替代所有模型业务测试？
4. 为什么网络单元测试不应直接依赖公网？
5. `QBENCHMARK` 后为什么仍要做一次结果验证？

### 参考答案

1. 显示请求还未经过窗口系统处理，控件可能没有暴露或事件目标未准备好。
2. `QTRY_COMPARE` 在处理事件的同时重复检查条件，满足即结束；固定等待无法根据实际完成时间自适应。
3. 不能。它主要检查模型结构和信号契约，排序、业务编辑、持久化和破坏性场景仍需单独覆盖。
4. 公网受 DNS、服务状态、代理、证书和限流影响，会产生非确定性失败。
5. 基准代码可能走错误或提前返回路径，结果验证可以把这类无效测量识别出来。

## 12. 小结

Qt Test 的高级用法可以归纳为四条：

- GUI 测试等待窗口和事件，而不是等待时间；
- 异步测试等待可观察条件，并隔离 reply、定时器和全局状态；
- Model/View 测试同时验证数据结果和模型契约；
- 性能测试控制输入、测量边界和结果有效性。

做到这些，测试才会从“能跑一次”变成可在本地和 CI 中长期提供反馈的工程资产。
