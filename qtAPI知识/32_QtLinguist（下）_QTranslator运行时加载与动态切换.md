# Qt Linguist（下）：QTranslator 运行时加载与动态切换

上篇完成了 `lupdate -> .ts -> lrelease -> .qm` 工具链。本篇进入应用运行阶段：如何选择语言、从资源或磁盘加载 `.qm`、正确安装和移除 `QTranslator`、让 Widgets 和 QML 在运行中刷新，以及如何测试多语言行为。

## 1. `QTranslator` 的角色

`QTranslator` 是运行时翻译表对象。它本身不决定当前语言，也不自动扫描磁盘；应用需要：

1. 根据用户设置或系统区域选择语言。
2. 加载对应的 `.qm` 文件。
3. 把翻译器安装到 `QCoreApplication`。
4. 在切换时移除旧翻译器并重新翻译界面。

翻译查找会沿着已安装翻译器进行。后安装的翻译器优先级更高，因此安装顺序会影响同一上下文和源文本的最终结果。

## 2. 最小运行时代码

### 2.1 从文件系统加载

```cpp
#include <QApplication>
#include <QTranslator>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QTranslator translator;
    if (translator.load(QLocale("zh_CN"),
                        "myapp", "_", ":/i18n")) {
        app.installTranslator(&translator);
    }

    MainWindow window;
    window.show();
    return app.exec();
}
```

`load(QLocale, filename, prefix, directory, suffix)` 会按区域规则尝试文件名，例如 `myapp_zh_CN.qm`、`myapp_zh.qm`。目录可以是资源路径，也可以是本地文件夹。加载失败时不要安装空翻译器，应记录路径和 `translator.isEmpty()` 状态。

### 2.2 直接指定文件名

```cpp
QTranslator translator;
if (translator.load("translations/myapp_ja_JP.qm"))
    app.installTranslator(&translator);
```

部署目录结构由应用决定，但应把语言代码纳入文件名，避免多个版本的同名文件互相覆盖。跨平台路径使用 `QDir` 或资源系统，不要手工拼接反斜杠。

## 3. 使用 Qt Resource System 部署 `.qm`

### 3.1 `.qrc` 片段

```xml
<RCC>
    <qresource prefix="/i18n">
        <file>translations/myapp_zh_CN.qm</file>
        <file>translations/myapp_ja_JP.qm</file>
    </qresource>
</RCC>
```

资源路径是 `:/i18n/translations/myapp_zh_CN.qm`。如果使用 `qt_add_translations()`，可以让 CMake 自动把生成的 `.qm` 纳入资源，但要确认安装阶段仍然把它们放入目标资源或预期目录。

### 3.2 资源路径的常见错误

- `.qrc` 中的 `prefix` 不等于磁盘目录名。
- `load()` 的路径必须以 `:/` 开头才能访问资源系统。
- 修改 `.qrc` 后需重新运行 CMake，旧构建目录不会自动发现所有变更。
- Windows 下资源路径依然使用 `/`，不要写成 `C:\...`。

## 4. 设计语言管理器

把翻译器管理从窗口类中分离，可以统一处理设置保存、信号、回滚和测试：

```cpp
#include <QObject>
#include <QTranslator>

class LanguageManager : public QObject
{
    Q_OBJECT
public:
    explicit LanguageManager(QCoreApplication &app, QObject *parent = nullptr)
        : QObject(parent), m_app(app) {}

    bool setLocale(const QLocale &locale)
    {
        const QString resource =
            ":/i18n/myapp_" + locale.name() + ".qm";

        auto *next = new QTranslator(this);
        if (!next->load(resource)) {
            delete next;
            return false;
        }

        if (m_current)
            m_app.removeTranslator(m_current);
        delete m_current;
        m_current = next;
        m_app.installTranslator(m_current);
        emit localeChanged(locale);
        return true;
    }

signals:
    void localeChanged(const QLocale &locale);

private:
    QCoreApplication &m_app;
    QTranslator *m_current = nullptr;
};
```

关键点是“先加载新翻译器，成功后再移除旧翻译器”。这样新文件损坏或缺失时仍保留旧语言。`removeTranslator()` 必须在对象销毁前调用，避免应用继续访问已释放的翻译器。

## 5. Widgets 的动态切换

### 5.1 `LanguageChange` 事件

安装或移除翻译器后，Qt 会向顶层窗口发送 `QEvent::LanguageChange`。使用 Qt Designer 生成的界面，通常在 `retranslateUi()` 中更新文本：

```cpp
void MainWindow::changeEvent(QEvent *event)
{
    if (event->type() == QEvent::LanguageChange) {
        ui->retranslateUi(this);
        updateActionTexts();
    }
    QMainWindow::changeEvent(event);
}
```

手写界面则应集中保存需要翻译的控件，并在一个函数中重新设置文本：

```cpp
void MainWindow::retranslate()
{
    setWindowTitle(tr("Inventory"));
    openAction->setText(tr("Open"));
    statusLabel->setText(tr("Ready"));
}
```

不要只在构造函数里调用一次 `tr()`。构造函数中的字符串不会在语言切换后自动重新求值。

### 5.2 动态创建控件

动态创建的控件也要遵循相同原则：保存业务状态而不是保存已翻译的最终文本，在 `LanguageChange` 时依据状态重新计算文本：

```cpp
void FileRow::setFileCount(int count)
{
    m_count = count;
    retranslate();
}

void FileRow::retranslate()
{
    countLabel->setText(tr("%n file(s)", "", m_count));
}
```

这样语言切换后复数规则和数字内容都能保持正确。

## 6. QML 的运行时翻译

### 6.1 `qsTr()` 与上下文

```qml
import QtQuick

Item {
    property int count: 3

    Text {
        text: qsTr("%n file(s) copied", "", count)
    }
}
```

QML 文件中的 `qsTr()` 会由 `lupdate` 提取。组件的 QML 类型名通常参与上下文生成，因此重命名组件可能造成已有翻译条目需要重新审阅。

### 6.2 重新翻译 QML 引擎

```cpp
#include <QQmlApplicationEngine>

QQmlApplicationEngine engine;
engine.loadFromModule("MyApp", "Main");

// 安装新 QTranslator 后：
engine.retranslate();
```

`retranslate()` 会让使用 `qsTr()` 的绑定重新求值。若 Qt 版本或项目封装没有提供该调用，则可通过重新加载根对象实现，但这会丢失页面状态，应优先使用引擎的重新翻译能力。

### 6.3 QML 与 C++ 的语言状态同步

可以把当前语言暴露为只读属性，并让 QML 监听变化：

```cpp
class LanguageBridge : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString locale READ locale NOTIFY localeChanged)
public:
    QString locale() const { return m_locale.name(); }
signals:
    void localeChanged();
private:
    QLocale m_locale;
};
```

语言管理器完成切换后发出信号，QML 只负责更新选择控件和调用需要重新计算的业务绑定，翻译器的安装仍由 C++ 完成。

## 7. 语言选择与回退策略

### 7.1 系统语言和应用语言分离

`QLocale::system()` 表示操作系统区域设置，应用还应支持用户单独选择语言。建议保存 BCP 47 或 Qt 区域名（如 `zh_CN`、`en_GB`），不要保存显示名称，因为显示名称会随语言变化。

### 7.2 分层回退

一个稳健的加载顺序是：

1. 用户明确选择的完整区域（例如 `zh_Hans_CN`）。
2. 语言级别的通用区域（例如 `zh`）。
3. 应用内置默认语言（通常是源语言）。

可以尝试多个文件名，成功加载第一个即可：

```cpp
const QStringList candidates = {
    ":/i18n/myapp_zh_Hans_CN.qm",
    ":/i18n/myapp_zh_CN.qm",
    ":/i18n/myapp_zh.qm"
};

for (const QString &path : candidates) {
    if (translator.load(path)) {
        app.installTranslator(&translator);
        break;
    }
}
```

不要在找不到目标语言时卸载所有翻译器再显示半翻译界面；应先确认候选文件可用。

## 8. 翻译器的安装顺序与模块化

大型程序往往有多个翻译文件：核心模块、插件、第三方组件。建议从通用到具体安装，具体模块最后安装，以便覆盖通用文本：

```cpp
app.installTranslator(&qtTranslator);      // Qt 自带控件
app.installTranslator(&coreTranslator);    // 应用核心
app.installTranslator(&pluginTranslator);  // 当前插件，优先级最高
```

卸载时按相反顺序移除。插件卸载前必须先移除它的翻译器，不能让翻译器指向已卸载的插件资源。

## 9. 运行时翻译质量测试

### 9.1 自动化切换测试

```cpp
QTranslator translator;
QVERIFY(translator.load(":/i18n/myapp_zh_CN.qm"));
qApp->installTranslator(&translator);

QCOMPARE(window.windowTitle(), QStringLiteral("库存"));

qApp->removeTranslator(&translator);
QCOMPARE(window.windowTitle(), QStringLiteral("Inventory"));
```

测试应覆盖安装、移除、回退和窗口重新翻译，而不仅是检查 `.qm` 文件存在。

### 9.2 占位符和加速键检查

翻译文本常见的回归包括 `%1` 丢失、`%n` 被改写、菜单加速键 `&File` 冲突以及按钮文本过长。可以在 CI 中：

- 用 XML 解析器比较源文和译文中的占位符集合。
- 检查同一菜单层级中加速键是否重复。
- 对关键窗口在多个语言下运行截图或布局测试。
- 对 `unfinished` 条目设置发布门禁。

### 9.3 伪本地化

伪本地化通过人为拉长字符串、加入重音字符或镜像方向，提前暴露布局硬编码问题。它不替代真实翻译，但适合在 UI 自动化阶段验证按钮、表格列和弹窗是否能够适应不同文本长度。

## 10. 部署检查表

1. `.qm` 文件已随安装包或资源系统发布。
2. 运行时使用的文件名与 `lrelease` 输出一致。
3. 安装目录、用户数据目录和搜索路径在 Windows、Linux、macOS 上都可写或可读。
4. 更新翻译文件后不会继续命中旧缓存。
5. Qt 自带控件翻译（如 `qt_zh_CN.qm`）按需要加载，并与应用翻译器分开管理。
6. 语言切换后所有顶层窗口、菜单、模型列标题和状态消息都已刷新。

## 11. 进一步延伸

### 11.1 翻译版本与产品版本解耦

应用可以把翻译包作为独立资源更新，但必须保证消息上下文和源文本兼容。若翻译包来自网络，下载后先校验签名或哈希，再复制到应用数据目录并原子替换，避免读取到半写入文件。

### 11.2 日志与可观测性

在发布版本记录语言代码、加载路径、`.qm` 文件版本和失败原因。不要记录包含用户隐私的完整翻译文本；只记录上下文和消息 ID，便于定位缺失翻译。

### 11.3 Qt Quick Controls 的特殊注意点

Qt Quick Controls 的默认样式、系统对话框和应用自己的 `qsTr()` 可能来自不同翻译器。切换语言时要同时调用 `QQmlApplicationEngine::retranslate()`，并确认样式插件没有缓存需要翻译的文本。

掌握 `QTranslator` 的生命周期、事件刷新和部署策略后，Qt Linguist 工具链就从“能翻译”提升到了“可持续交付多语言产品”。
