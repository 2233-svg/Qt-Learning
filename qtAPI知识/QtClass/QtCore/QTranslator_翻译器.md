# Qt QTranslator：把 `.qm` 翻译表接入 Qt 应用

`QTranslator` 保存一组“源文本到目标语言文本”的映射。它本身不是翻译器生成工具，也不会把任意中文自动翻成英文；它加载由 Qt Linguist 工具链生成的二进制 `.qm` 文件，然后响应 Qt 的翻译查询。

最常见的工作流是：

1. 用 `lupdate` 从源码收集可翻译文本。
2. 用 Qt Linguist 编辑 `.ts` 文件。
3. 用 `lrelease` 生成 `.qm` 文件。
4. 程序启动时用 `QTranslator::load()` 加载 `.qm`。
5. 用 `QCoreApplication::installTranslator()` 安装。
6. 代码通过 `tr()` 或 `QCoreApplication::translate()` 查询文本。

```cpp
#include <QApplication>
#include <QTranslator>

int main(int argc, char **argv)
{
    QApplication app(argc, argv);

    QTranslator translator;
    if (translator.load(QLocale(), "myapp", "_", ":/i18n"))
        QCoreApplication::installTranslator(&translator);

    MainWindow window;
    window.show();
    return app.exec();
}
```

## 它解决什么问题

Qt 的翻译键不是简单的“英文字符串全局替换”。一个源词可能在不同上下文、不同语义说明或不同数量形式下有不同译法。`QTranslator` 使用以下信息定位翻译：

- `context`：通常是调用 `tr()` 的类名。
- `sourceText`：源文本。
- `disambiguation`：区分相同文本不同语义的说明。
- `n`：复数数量，供 `.qm` 中的复数形式选择。

例如同样是 `"Enabled"`，打印机双面设置和装订设置可能需要不同的西班牙语阴阳性。为它们提供不同 disambiguation，比在代码里改写源文本更可靠。

## 加载与安装的生命周期

`QTranslator` 继承 `QObject`。翻译器必须在被安装期间保持存活，通常让它成为 `QApplication` 或主窗口的成员/子对象：

```cpp
class Application : public QApplication
{
public:
    Application(int &argc, char **argv)
        : QApplication(argc, argv), translator(this)
    {
        if (translator.load(QLocale(), "myapp", "_", ":/i18n"))
            installTranslator(&translator);
    }

private:
    QTranslator translator;
};
```

文档特别强调：翻译器应在创建应用控件之前安装，这样控件构造过程中产生的文本就能得到正确翻译。翻译器被析构后，不应继续由 `QCoreApplication` 持有或查询。

安装和卸载是 `QCoreApplication` 的职责：

```cpp
QCoreApplication::installTranslator(&translator);
QCoreApplication::removeTranslator(&translator);
```

卸载/安装翻译器会触发语言变化通知。已有窗口通常要在 `changeEvent(QEvent::LanguageChange)` 中重新执行 `retranslateUi()` 或更新自己的文本；`QTranslator` 不会自动重建你的业务界面。

## 选择 `load()` 重载

### 按当前 UI 语言加载

优先使用带 `QLocale` 的重载：

```cpp
translator.load(QLocale(), "myapp", "_", ":/i18n", ".qm");
```

它使用 `QLocale::uiLanguages()`，例如依次尝试 `myapp.es.qm`、`myapp.fr_CA.qm`、`myapp.fr.qm` 等回退文件。UI 语言和数字/日期格式 locale 不一定相同，所以不要简单用 `QLocale::name()` 自己拼文件名替代它。

`prefix` 位于基本文件名和 UI 语言名之间，例如文件名模式 `myapp_de.qm` 可以使用前缀 `"_"`。

### 按文件名加载

```cpp
translator.load("myapp_de", ":/i18n");
```

未指定 suffix 时默认尝试 `.qm`。`search_delimiters` 默认按 `"_.“` 的分隔符逐步剥离 locale 后缀，适合根据 `myapp.fr_CA` 回退到 `myapp.fr` 和 `myapp`。

这类重载在你已经明确选好文件时很直接，但它只根据文件名字符串搜索；国际化应用通常更适合带 `QLocale` 的版本。

### 从内存加载

```cpp
QByteArray qmData = loadFromResourceOrPackage();
translator.load(reinterpret_cast<const uchar *>(qmData.constData()),
                qmData.size(), ":/i18n");
```

这个重载不会复制数据。`qmData` 的内存必须在翻译器使用期间一直存在，不能在 `load()` 返回后释放、修改或让临时缓冲区失效。`directory` 只用于 `.qm` 依赖文件的基目录；`filePath()` 对内存加载返回空。

## 查询语义

直接调用 `translate()` 找不到匹配项时返回 null `QString`；它不会自动把 `sourceText` 返回给你。`QCoreApplication::translate()` 和 `tr()` 会在没有翻译时按 Qt 规则回退到源文本。

```cpp
const QString translated =
    translator.translate("SettingsDialog", "Enabled", "two-sided printing");

if (translated.isNull())
    useSourceText("Enabled");
else
    useText(translated);
```

`translate()` 首先按完整键查询；没有找到时还会尝试空 disambiguation。翻译表不完整时，某些不同 disambiguation 的条目可能产生意外匹配，因此应保持 `.ts` 文件和上下文完整。

`n != -1` 时用于选择复数形式。源文本通常使用 `%n`，最终文本通过 `QString::arg()` 或 Qt 的翻译调用方式填充数量。不要把复数句子拆成 `"1 file"` / `"2 files"` 两个硬编码字符串。

`translate()` 标记为线程安全，适合多个线程查询已加载的只读翻译表。但加载、替换、安装和卸载是状态变更，应由应用统一管理，不要让线程同时修改同一个 `QTranslator`。

## 多个翻译器的优先级

应用可以安装多个翻译器。Qt 按安装顺序的逆序搜索：最后安装的翻译器优先，找到匹配项后停止。

这适合“应用默认翻译 + 插件或用户覆盖”的结构。需要改变优先级时，先 `removeTranslator()`，再 `installTranslator()`，让它回到搜索队列最前面。

```cpp
QCoreApplication::installTranslator(baseTranslator);
QCoreApplication::installTranslator(pluginTranslator); // 优先搜索
```

不要把同一份翻译分别安装多次来“提高优先级”；保持明确的安装/卸载配对更容易维护。

## 动态切换语言

动态切换时通常按以下顺序：

1. 从应用卸载旧翻译器。
2. 让同一个或新的 `QTranslator` 加载目标语言。
3. 加载成功后重新安装。
4. 在窗口/控件收到 `LanguageChange` 后重新设置界面文本。

如果使用 Qt Designer 生成的 UI，通常在窗口类中调用 `ui->retranslateUi(this)`；手写控件则需要自己更新标题、菜单、模型列名和状态栏文本。数据模型里的用户可见字符串也要纳入重新翻译路径。

## 文件和安全边界

`.qm` 是二进制翻译文件，不应当把它当普通文本文件直接编辑。只加载可信来源的 `.qm`：格式损坏可能导致加载失败甚至崩溃，合法文件也可能包含误导性的文本。

资源系统路径如 `:/i18n/myapp_de.qm` 很适合随应用发布。外部下载的翻译包需要校验来源、版本和完整性，并考虑文本内容本身的安全和合规性。

## 自定义翻译器

如果翻译不是来自 `.qm` 文件，也可以继承 `QTranslator` 并重写 `translate()`，例如从数据库或远程缓存读取。不过要自己定义线程安全、缓存、失败回退和动态更新策略。

```cpp
class MapTranslator final : public QTranslator
{
public:
    QString translate(const char *context,
                      const char *sourceText,
                      const char *disambiguation,
                      int n) const override
    {
        Q_UNUSED(disambiguation);
        Q_UNUSED(n);
        if (qstrcmp(context, "MainWindow") == 0 &&
            qstrcmp(sourceText, "Ready") == 0)
            return QStringLiteral("就绪");
        return {};
    }
};
```

重写时找不到翻译应返回 null `QString`，让后续翻译器或 Qt 的源文本回退机制继续工作；不要随意返回一个空但非 null 的字符串来表示“没有翻译”。

## 常见错误

- `load()` 返回 `false` 仍然安装翻译器。应只安装成功加载且 `!isEmpty()` 的翻译器。
- 翻译器是局部变量，函数返回后仍安装在应用中。安装期间必须保持对象存活。
- 只切换翻译文件，不重新翻译已经创建的窗口。
- 用 `QLocale::name()` 代替 `QLocale::uiLanguages()` 拼 UI 语言文件名。
- 内存加载后释放或修改原始 `.qm` 数据。`load(data, len)` 不复制数据。
- 直接使用 `translate()` 时把 null 结果误当成已翻译的空文本。
- 省略 context 或 disambiguation，导致同源文本串译或查不到。
- 通过缩写或源文本内容猜测语言。应读取 `language()` 或由应用配置管理语言选择。
- 把 `QTranslator` 当成翻译编辑器。`.ts` 编辑和 `.qm` 生成属于 Qt Linguist 工具链。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTranslator(QObject *parent = nullptr)` | 创建空翻译器 | 初始不连接任何翻译文件；通常由应用对象管理生命周期 |
| `~QTranslator()` | 销毁翻译器 | 析构前应从 `QCoreApplication` 移除 |
| `load(const QString &filename, const QString &directory, const QString &search_delimiters, const QString &suffix)` | 按文件名加载 `.qm` | 成功返回 true；会丢弃之前内容；可按分隔符逐级回退 |
| `load(const QLocale &locale, const QString &filename, const QString &prefix, const QString &directory, const QString &suffix)` | 按 UI 语言加载 | 使用 `uiLanguages()`，通常是推荐重载；会丢弃之前内容 |
| `load(const uchar *data, int len, const QString &directory)` | 从内存加载 `.qm` | 不复制 `data`；调用期间必须保持内存不变 |
| `isEmpty()` | 判断是否没有翻译内容 | 加载失败或空文件通常为 true |
| `language()` | 读取 `.qm` 内记录的目标语言 | 不等于当前系统 locale；未加载时通常为空 |
| `filePath()` | 读取加载文件路径 | 内存加载、未加载或失败时为空 |
| `translate(context, sourceText, disambiguation, n)` | 直接查询翻译 | 找不到返回 null `QString`；`n` 用于复数；函数可线程安全查询 |
| `QCoreApplication::installTranslator()` | 安装翻译器 | 最后安装者优先；会影响后续翻译查询并触发语言变化事件 |
| `QCoreApplication::removeTranslator()` | 卸载翻译器 | 动态切换或改变优先级时使用；卸载后对象仍由调用方管理 |
| `QObject::tr()` | 以 QObject 上下文查询 | 通常由 Qt 元对象/类上下文生成 context |
| `QCoreApplication::translate()` | 在非 QObject 代码中查询 | 应显式提供稳定 context、源文本和可选 disambiguation |
| `QTranslator::translate()` 重写 | 提供自定义翻译后端 | 找不到时返回 null，避免阻断其它翻译器和源文本回退 |
