# Qt Test（上）：单元测试与数据驱动测试

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Test  
> 核心内容：测试类、断言、fixture、数据驱动、信号验证、异步等待、CMake/CTest 集成

Qt Test 是 Qt 自带的 C++ 测试框架。它不仅能测试 QObject，也能测试普通 C++ 业务代码、信号、事件循环和 Widget 交互。

## 1. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Test)
target_link_libraries(mytarget PRIVATE Qt6::Test)
```

使用 Widgets 的测试：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets Test)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::Test)
```

接入 CTest 的关键片段：

```cmake
include(CTest)
add_test(NAME mytest COMMAND mytest)
```

本篇只给出可摘用片段，不创建完整测试工程。

## 2. 最小测试类

```cpp
#include <QtTest>

class TestCalculator : public QObject
{
    Q_OBJECT

private slots:
    void addition()
    {
        QCOMPARE(2 + 3, 5);
    }
};

QTEST_APPLESS_MAIN(TestCalculator)
#include "testcalculator.moc"
```

Qt Test 通过元对象系统发现 private slots 中的测试函数。测试类需要 `Q_OBJECT`，构建系统需要运行 moc。

### 2.1 main 宏怎么选

| 宏 | 创建的应用对象 | 适用场景 |
|---|---|---|
| `QTEST_APPLESS_MAIN` | 不创建应用对象 | 纯算法、容器等无需事件循环的测试 |
| `QTEST_GUILESS_MAIN` | `QCoreApplication` | QObject、定时器、线程、网络等非 GUI 测试 |
| `QTEST_MAIN` | `QApplication` 或 `QGuiApplication` | Widget、窗口、键鼠 GUI 测试 |

“没有窗口显示”不等于 app-less。只要代码依赖事件循环、标准路径或 QObject 异步投递，通常使用 GUILESS 或 MAIN。

## 3. 测试函数的生命周期

Qt Test 识别这些特殊槽：

```cpp
private slots:
    void initTestCase();       // 整个测试类开始前一次
    void initTestCase_data();  // 全局数据表
    void init();               // 每个测试函数/数据行之前
    void cleanup();            // 每个测试函数/数据行之后
    void cleanupTestCase();    // 整个测试类结束后一次
```

顺序：

```text
initTestCase
  ├─ init → testA → cleanup
  ├─ init → testB[data row 1] → cleanup
  └─ init → testB[data row 2] → cleanup
cleanupTestCase
```

测试提前失败后，`cleanup()` 仍会执行。局部资源优先使用 RAII，让析构自动清理。

### 3.1 测试隔离

每个测试函数都应能单独、重复、任意顺序运行：

- 不依赖前一个测试留下的数据；
- 不共用可变全局状态；
- 临时文件使用 `QTemporaryDir`；
- 数据库使用唯一连接名和独立临时库；
- 修改全局 locale、环境变量后恢复；
- 线程、Reply、定时器在结束前清理。

## 4. 断言宏

### 4.1 QVERIFY

```cpp
QVERIFY(result.isValid());
QVERIFY2(file.open(QIODevice::ReadOnly),
         qPrintable(file.errorString()));
```

适合布尔条件。若是在比较两个值，使用 `QCOMPARE`，失败输出更清楚。

### 4.2 QCOMPARE

```cpp
QCOMPARE(actual, expected);
QCOMPARE(user.name, QStringLiteral("Alice"));
QCOMPARE(values.size(), qsizetype(3));
```

失败会同时显示实际值和期望值。两侧类型应明确兼容，避免隐式转换掩盖错误。

Qt 6.4+ 还有 `QCOMPARE_EQ`、`QCOMPARE_NE`、`QCOMPARE_LT` 等关系宏；Qt 6.9+ 有 `QCOMPARE_3WAY`。

### 4.3 QFAIL、QSKIP、QEXPECT_FAIL

```cpp
if (!featureAvailable)
    QSKIP("当前平台没有此能力");

if (unexpectedBranch)
    QFAIL("进入了不应到达的分支");
```

`QEXPECT_FAIL` 用于已知、被跟踪的问题，而不是长期隐藏失败。应注明原因和对应数据行，并在缺陷修复后移除。

### 4.4 异常

```cpp
QVERIFY_THROWS_EXCEPTION(ParseError, parse("invalid"));
QVERIFY_THROWS_NO_EXCEPTION(parse("valid"));
```

Qt 本身许多 API 不使用异常，但普通 C++ 业务层可以使用这些宏验证异常契约。

## 5. 一个测试只验证一个行为

不意味着每个函数只能有一个断言，而是失败原因应聚焦：

```cpp
void TestCounter::setValueClampsAboveMaximum()
{
    Counter counter;
    counter.setRange(0, 100);

    counter.setValue(120);

    QCOMPARE(counter.value(), 100);
}
```

命名使用“场景 + 结果”，比 `test1()`、`basic()` 更易定位失败。

## 6. 数据驱动测试

同一行为有多组输入时，不要复制测试函数。Qt Test 用 `_data()` 建表，测试函数取值。

```cpp
class TestClamp : public QObject
{
    Q_OBJECT

private slots:
    void clamp_data()
    {
        QTest::addColumn<int>("input");
        QTest::addColumn<int>("minimum");
        QTest::addColumn<int>("maximum");
        QTest::addColumn<int>("expected");

        QTest::newRow("inside") << 5 << 0 << 10 << 5;
        QTest::newRow("below")  << -2 << 0 << 10 << 0;
        QTest::newRow("above")  << 20 << 0 << 10 << 10;
        QTest::newRow("single") << 8 << 8 << 8 << 8;
    }

    void clamp()
    {
        QFETCH(int, input);
        QFETCH(int, minimum);
        QFETCH(int, maximum);
        QFETCH(int, expected);

        QCOMPARE(qBound(minimum, input, maximum), expected);
    }
};
```

数据列名和 `QFETCH` 变量名、类型必须一致。每个 row tag 应描述场景，失败日志才能直接指出是哪组数据。

### 6.1 addRow 与 newRow

```cpp
QTest::addRow("value-%d", value) << value << expected;
QTest::newRow("empty") << QString{} << false;
```

`addRow()` 可格式化标签；`newRow()` 使用固定字符串。

### 6.2 自定义类型

```cpp
struct PointPair { QPoint a; QPoint b; };
Q_DECLARE_METATYPE(PointPair)

QTest::addColumn<PointPair>("pair");
```

类型需要满足元类型要求。若希望 `QCOMPARE` 失败时打印清楚，可提供 `operator<<` 到 `QDebug`，或专用 `toString()`。

### 6.3 全局测试数据

`initTestCase_data()` 定义全局数据，每个测试会对每个全局行执行。若测试本身也有本地数据，执行次数是两者笛卡尔积。

只在 locale、后端实现、数据格式等确实需要覆盖整个测试类时使用，避免测试数量意外膨胀。

## 7. 比较浮点数

```cpp
QVERIFY(qAbs(actual - expected) < 1e-9);
```

容差要来自领域精度，而不是随手写一个很大的 epsilon。相对误差和绝对误差应结合数值量级。`qFuzzyCompare()` 有自己的相对比较语义，先理解再使用。

货币等需要精确十进制的领域不应因为测试方便而使用 double；应使用整数最小单位或明确十进制类型。

## 8. QSignalSpy

```cpp
Counter counter;
QSignalSpy spy(&counter, &Counter::valueChanged);
QVERIFY(spy.isValid());

counter.setValue(42);

QCOMPARE(spy.count(), 1);
const QList<QVariant> arguments = spy.takeFirst();
QCOMPARE(arguments.at(0).toInt(), 42);
```

它记录信号每次发射的参数。自定义参数需注册元类型：

```cpp
qRegisterMetaType<Result>();
```

### 8.1 不仅验证“发了”

还应验证：

- 发射次数正确；
- 参数正确；
- 相同值不重复通知；
- 失败/取消时发正确的信号；
- 状态已在信号发出前更新。

### 8.2 等待异步信号

```cpp
QSignalSpy spy(worker, &Worker::finished);
worker->start();

QVERIFY(spy.wait(1000));
QCOMPARE(spy.count(), 1);
```

`wait()` 等待下一次信号或超时。如果信号可能在调用 wait 前同步发出，应先检查 `spy.isEmpty()`，或直接对最终状态使用 QTRY 宏。

## 9. 异步条件：QTRY 宏

```cpp
controller.start();
QTRY_COMPARE_WITH_TIMEOUT(controller.state(), State::Ready, 2s);
QTRY_VERIFY_WITH_TIMEOUT(model.rowCount() > 0, 2s);
```

QTRY 宏在等待期间处理事件并重复检查条件，比固定 `qWait(500)` 更稳：状态早到可立即结束，机器较慢时也有明确上限。

### 9.1 避免固定等待

```cpp
QTest::qWait(1000); // 慢且仍可能偶发失败
```

只有测试“在一段时间内不应发生某事”或模拟时间经过时才考虑固定等待。更好的设计是注入 clock/timer，使时间逻辑可确定测试。

### 9.2 超时应有意义

过短造成慢机器偶发失败；过长使真实错误拖慢 CI。默认等待与单项特殊等待分开配置，并在失败日志输出当前状态。

## 10. 消息和警告

```cpp
QTest::ignoreMessage(QtWarningMsg, "expected warning");
callThatWarns();
```

仅对当前测试明确预期的完整消息使用，过宽正则会吞掉新问题。

可以把意外警告变成失败：

```cpp
QTest::failOnWarning();
```

对模型、QObject 生命周期和线程测试尤其有用。先清理已有已知警告，否则测试套件会充满无关失败。

## 11. 临时文件与目录

```cpp
QTemporaryDir dir;
QVERIFY(dir.isValid());

QFile file(dir.filePath("settings.json"));
QVERIFY(file.open(QIODevice::WriteOnly));
QCOMPARE(file.write("{}"), qint64(2));
```

不要把测试输出写到源码目录或固定系统路径。`QTemporaryDir` 析构时清理；失败后需要保留现场时可临时禁用自动删除并打印路径。

资源 fixture 可通过 `QFINDTESTDATA` 查找，使从构建目录、源码目录和安装环境运行时都更稳定。

## 12. 环境与全局状态

测试修改环境变量时要恢复：

```cpp
const QByteArray oldValue = qgetenv("MYAPP_MODE");
const bool existed = qEnvironmentVariableIsSet("MYAPP_MODE");
const auto restore = qScopeGuard([=] {
    if (existed)
        qputenv("MYAPP_MODE", oldValue);
    else
        qunsetenv("MYAPP_MODE");
});

qputenv("MYAPP_MODE", "test");
```

locale、时区、默认 QSettings 组织名、当前目录和全局 Qt 属性也属于共享状态。并行测试时更要避免修改进程全局状态。

## 13. CTest 集成

```cmake
include(CTest)

qt_add_executable(test_counter test_counter.cpp)
target_link_libraries(test_counter PRIVATE Qt6::Test mylib)

add_test(NAME counter COMMAND test_counter)
set_tests_properties(counter PROPERTIES TIMEOUT 30)
```

运行：

```text
ctest --test-dir build --output-on-failure
```

不要只在 IDE 中手动点测试。CTest 让本地、Visual Studio 和 CI 使用一致入口。

### 13.1 测试函数选择

Qt Test 可通过命令行只运行某个函数或数据行，便于复现：

```text
test_counter clamp:above
```

## 14. 测试代码也需要可维护性

- 使用 Builder/fixture 减少无关初始化；
- 数据行表达边界条件，而不是堆随机数字；
- 期望值应独立得出，避免复制生产算法；
- 失败信息要能说明业务场景；
- 不因实现细节重构就大面积失败；
- 同时验证成功、拒绝、错误和取消路径。

## 15. 常见错误

### 15.1 使用错误 main 宏

依赖事件循环却使用 APPLESS，异步信号和定时器无法按预期运行；Widget 测试需要 `QApplication`。

### 15.2 QVERIFY(actual == expected)

失败只看到条件 false。使用 QCOMPARE 显示两侧值。

### 15.3 数据行标签没有意义

`row1`、`case2` 无法定位边界。使用 `empty-input`、`above-maximum`。

### 15.4 用 qWait 掩盖竞态

固定等待不能建立 happens-before，只让测试更慢。等待可观察状态或信号。

### 15.5 一个测试依赖另一个

单独运行或顺序变化就失败。每项独立准备和清理。

### 15.6 QSignalSpy 只检查 count

信号参数可能错，重复通知也可能未覆盖。检查次数、顺序和参数。

### 15.7 测试计算期望值时复制生产实现

同一错误会在两边同时存在。使用手工已知结果、性质或独立参考实现。

## 16. API 速查

| API/宏 | 用途 |
|---|---|
| `QTEST_APPLESS_MAIN` | 无应用对象测试入口 |
| `QTEST_GUILESS_MAIN` | QCoreApplication 测试入口 |
| `QTEST_MAIN` | GUI 测试入口 |
| `QVERIFY` / `QVERIFY2` | 验证布尔条件 |
| `QCOMPARE` | 比较并输出两侧值 |
| `QFAIL` | 立即失败 |
| `QSKIP` | 因环境/能力跳过 |
| `QTest::addColumn` | 声明数据列 |
| `QTest::newRow` / `addRow` | 添加数据行 |
| `QFETCH` | 取出当前行数据 |
| `QSignalSpy` | 捕获信号及参数 |
| `QTRY_COMPARE` / `QTRY_VERIFY` | 处理事件并轮询异步状态 |
| `QTest::failOnWarning` | 将意外警告转为失败 |
| `QTemporaryDir` | 独立临时目录 |
| `QFINDTESTDATA` | 查找测试数据 |

## 17. 自测题

1. 测试 QObject 定时器时应选 APPLESS 还是 GUILESS？
2. init 和 initTestCase 的调用频率有何区别？
3. 为什么比较值时优先 QCOMPARE？
4. 数据驱动测试函数如何关联其数据函数？
5. 本地数据和全局数据同时存在会执行多少次？
6. QSignalSpy 使用前为什么检查 isValid？
7. QTRY_COMPARE 为什么通常优于 qWait？
8. 测试临时文件为什么不写源码目录？
9. QEXPECT_FAIL 是否适合永久隐藏缺陷？
10. 为什么测试期望值不应复制生产算法？

## 18. 参考答案

1. GUILESS，因为它需要 QCoreApplication 和事件循环。
2. init 每个测试函数/数据行前调用；initTestCase 整类一次。
3. 失败时能显示实际值与期望值，诊断更直接。
4. 名为 `function_data()` 的槽为 `function()` 提供数据。
5. 全局行数乘本地行数。
6. 无效连接会导致 spy 永远收不到信号，错误原因应立即暴露。
7. 它等待可观察条件，早完成早返回，并有明确超时。
8. 避免污染仓库、权限依赖和并行冲突，并能自动清理。
9. 不适合；它只用于有明确跟踪和移除计划的已知失败。
10. 两边可能复制同一错误，形成虚假通过。

## 19. 本篇结论

```text
选择正确应用入口
  → 每个测试独立 arrange / act / assert
  → 重复场景使用数据表
  → 信号检查次数和参数
  → 异步状态使用 QTRY 或 spy.wait
  → 临时资源和全局状态可靠清理
  → 通过 CTest 统一运行
```

下篇继续讲 Widget 输入测试、Model/View 测试、网络与数据库替身、Benchmark、随机/性质测试，以及 CI 中稳定运行 Qt 测试。
