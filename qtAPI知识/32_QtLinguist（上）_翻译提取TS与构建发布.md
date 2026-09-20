# Qt Linguist（上）：翻译提取、TS 文件与构建发布

Qt Linguist 解决的是国际化（internationalization，简称 i18n）和本地化（localization，简称 l10n）问题。开发者在源代码中标记可翻译文本，工具从源码提取消息，翻译人员在 Qt Linguist 中维护 `.ts` 文件，构建阶段再把 `.ts` 编译成运行时使用的 `.qm` 文件。

本文先建立一条可靠的工具链，再解释上下文、源文本、注释、占位符、复数和 ID-based 翻译等基础概念。运行时加载翻译器和语言热切换放在下一篇。

## 1. 国际化的完整链路

```text
源代码中的 tr()/qsTr()/QT_TR_NOOP
             │
             ▼
          lupdate
             │
             ▼
        app_zh_CN.ts  ── Qt Linguist 翻译 ──► 已完成翻译
             │
             ▼
          lrelease
             │
             ▼
          app_zh_CN.qm
             │
             ▼
       QTranslator.load() + installTranslator()
```

`.ts` 是 XML 格式的可编辑翻译源文件，适合版本控制和人工审阅；`.qm` 是紧凑的二进制运行时文件，应用启动时加载它。不要把 `.ts` 当作运行时资源，也不要只提交 `.qm` 而不保存 `.ts`。

## 2. CMake 配置

### 2.1 查找 LinguistTools

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core LinguistTools)

qt_add_executable(mytarget
    main.cpp
    mainwindow.cpp
    mainwindow.h
)

set(TS_FILES
    translations/myapp_zh_CN.ts
    translations/myapp_ja_JP.ts
)

qt_add_translations(mytarget
    TS_FILES ${TS_FILES}
)
```

`qt_add_translations()` 会为目标配置 `lupdate` 和 `lrelease` 相关构建步骤。生成的 `.qm` 通常会放入目标的翻译目录或资源系统，具体布局受 Qt 版本和 CMake 参数影响。构建时应查看 CMake 输出，确认翻译文件实际安装位置。

### 2.2 使用 `qt_add_lupdate` 和 `qt_add_lrelease`

需要更细粒度控制时可以拆开配置：

```cmake
qt_add_lupdate(mytarget
    TS_FILES ${TS_FILES}
)

qt_add_lrelease(mytarget
    TS_FILES ${TS_FILES}
    QM_FILES_OUTPUT_VARIABLE qm_files
)

target_sources(mytarget PRIVATE ${qm_files})
```

项目中应统一由 CMake 生成工具命令，避免开发者在不同终端手动使用不一致的参数。Qt 5 项目常见的 `qt5_create_translation` 仍可见于旧代码，但新项目应优先采用 Qt 6 的 LinguistTools 命令。

## 3. 在 C++ 中标记可翻译文本

### 3.1 QObject 上下文中的 `tr()`

继承自 `QObject` 的类可以调用静态生成的 `tr()`：

```cpp
class LoginDialog : public QDialog
{
    Q_OBJECT
public:
    LoginDialog(QWidget *parent = nullptr) : QDialog(parent)
    {
        setWindowTitle(tr("Sign in"));
        userEdit->setPlaceholderText(tr("User name"));
        loginButton->setText(tr("Log in"));
    }
};
```

这里的上下文通常是类名 `LoginDialog`。同样的英文源文本在不同上下文中可以拥有不同译文，例如菜单中的“Open”和文件对话框中的“Open”可能需要不同表达。

### 3.2 非 QObject 代码中的 `QCoreApplication::translate`

工具类或命名空间函数没有 `tr()` 时，可以显式提供上下文：

```cpp
const QString text = QCoreApplication::translate(
    "ImportController", "Import failed");
```

第一个参数是稳定的上下文名，不要求一定对应 C++ 类，但应保持唯一、可读且长期不变。不要使用临时文件名或函数地址作为上下文。

### 3.3 `QT_TR_NOOP`：先标记，后翻译

当字符串保存在静态表中，不能在初始化阶段直接调用翻译函数时，使用 `QT_TR_NOOP`：

```cpp
static const char *const modes[] = {
    QT_TR_NOOP("Automatic"),
    QT_TR_NOOP("Manual")
};

QString modeText(int index)
{
    return QCoreApplication::translate("Settings", modes[index]);
}
```

`QT_TR_NOOP` 只做提取标记，不返回当前语言的译文。真正显示前仍要调用 `translate()`，否则语言切换不会生效。

## 4. 提取翻译源：`lupdate`

### 4.1 手动命令

```text
lupdate src include -ts translations/myapp_zh_CN.ts translations/myapp_ja_JP.ts
```

`lupdate` 扫描 C++、UI、QML 等源文件中的翻译标记，并把源文本、上下文和注释写入 `.ts`。它不会翻译文本，也不会删除已经存在但当前源码暂时未出现的条目，除非显式要求清理。

### 4.2 增量更新的原则

建议把 `lupdate` 放在持续集成或明确的开发命令中，而不是每次编译都隐式运行。原因是：

1. `.ts` 会发生格式和顺序变化，导致无意义的提交噪声。
2. 翻译人员正在编辑的条目可能被重新标记为待审阅。
3. CI 可以在提取后检查是否出现未翻译的新消息。

源码修改后，先运行 `lupdate`，在 Qt Linguist 中处理新增和“需要审阅”条目，再运行 `lrelease` 生成发布文件。

### 4.3 给翻译人员提供注释

使用 `//:` 或 `QT_TRANSLATE_NOOP` 的注释可以帮助翻译人员理解上下文：

```cpp
//: Shown when the network request cannot be retried.
label->setText(tr("Request failed"));
```

更复杂的情况可以使用 `QCoreApplication::translate` 的第三个参数传递额外注释：

```cpp
const QString text = QCoreApplication::translate(
    "Checkout", "Pay", "Button label for submitting the order");
```

注释应描述用途、语气、单位或长度限制，而不是重复源文本本身。

## 5. `.ts` 文件的结构与状态

一个简化的 `.ts` 片段如下：

```xml
<context>
    <name>LoginDialog</name>
    <message>
        <source>Sign in</source>
        <translation>登录</translation>
    </message>
</context>
```

重要元素包括：

- `<context>`：翻译上下文。
- `<source>`：源语言文本或 ID。
- `<translation>`：目标语言译文。
- `<extracomment>`：给翻译人员看的额外说明。
- `<location>`：源码位置，仅用于定位，重构后可能变化。
- `type="unfinished"`：尚未完成或需要审阅。
- `type="obsolete"`：源码中已不存在，暂时保留供清理。

不要直接用脚本替换 XML 文本来“批量翻译”。这会破坏转义、复数节点或译文状态。批量修改应使用 Qt Linguist、`lconvert` 或经过 XML 解析器验证的工具。

## 6. 翻译占位符与格式化

### 6.1 `%1` 等参数必须保留

```cpp
label->setText(tr("Welcome, %1").arg(userName));
```

译文必须保留 `%1`，并根据目标语言语序调整位置，例如：

```text
Welcome, %1  ->  欢迎，%1
```

如果需要多个参数，使用 `%1`、`%2`，不要依赖参数出现的顺序来表达业务含义。可以在测试中检查译文是否仍包含全部占位符。

### 6.2 数字和单位

```cpp
const QString text = tr("%1 files copied").arg(fileCount);
```

数字格式、千位分隔符和单位应由 `QLocale` 或专门的格式化函数处理，不要在源字符串中拼接语言相关的空格和标点：

```cpp
const QString number = QLocale().toString(fileCount);
label->setText(tr("Files copied: %1").arg(number));
```

## 7. 复数：`n` 参数与 `numerusform`

### 7.1 C++ 写法

```cpp
label->setText(tr("%n file(s) copied", "", fileCount));
```

第三个参数 `n` 告诉 Qt 使用复数规则。翻译文件中会出现一个或多个 `<numerusform>`，具体数量由目标语言规则决定：

```xml
<translation numerus="yes">
    <numerusform>%n 个文件已复制</numerusform>
</translation>
```

不要手动写 `file`/`files` 的二元判断来代替 `n`，因为许多语言有两种以上复数形式。

### 7.2 QML 写法

在 QML 中可使用 `qsTr()` 的 `n` 参数：

```qml
Text {
    text: qsTr("%n file(s) copied", "", fileCount)
}
```

QML 文件也必须纳入 `lupdate` 的扫描范围，否则这些消息不会出现在 `.ts` 中。

## 8. 编译发布文件：`lrelease`

### 8.1 基本命令

```text
lrelease translations/myapp_zh_CN.ts -qm translations/myapp_zh_CN.qm
```

`lrelease` 会忽略未完成翻译（除非配置允许），把可用条目压缩为 `.qm`。发布包中只需要 `.qm` 和应用程序，不必把 `.ts` 暴露给最终用户；`.ts` 应保留在源码仓库和翻译交付物中。

### 8.2 检查未翻译条目

```text
lrelease -fail-on-unfinished translations/myapp_zh_CN.ts
```

在发布构建中启用失败策略，可以防止关键语言包含有未完成条目。开发构建则可以允许未完成条目，以便先验证程序流程。

## 9. `lconvert` 与团队协作

`lconvert` 用于合并、拆分或转换 `.ts` 文件。例如把多个团队维护的文件合并：

```text
lconvert part-a.ts part-b.ts -o merged.ts
```

协作建议：

1. 按目标语言拆分文件，而不是按模块随意复制同一上下文。
2. 用版本控制审阅 `<source>`、`<translation>` 和状态变化。
3. 在 CI 中运行 `lupdate` 并检查新增消息是否被翻译。
4. 把 `lrelease` 作为可重复的构建步骤，避免手工复制旧 `.qm`。

## 10. ID-based 翻译的适用场景

Qt Linguist 也支持以稳定 ID 作为消息键，而不是把完整源文本作为键：

```cpp
const QString title = QCoreApplication::translate(
    "id", "welcome.title");
```

ID-based 方式适合源文本频繁改写、需要严格控制文案版本或多人协作的大型产品。优点是修改英文显示文案不会让所有译文失效；代价是源码可读性下降，需要维护 ID 命名规范和缺失 ID 检查。小型工具通常先采用普通 `tr()`，在文案治理成熟后再迁移。

## 11. 工具链排查清单

### `lupdate` 没有提取消息

- 文件扩展名和扫描路径是否正确。
- C++ 类是否包含 `Q_OBJECT`，或是否使用了显式 `QCoreApplication::translate`。
- QML 是否被传递给 `lupdate`，且字符串是否使用 `qsTr()`。
- 宏是否被条件编译排除。

### `lrelease` 后运行时仍显示源文案

- `.qm` 是否与目标语言和上下文匹配。
- 程序是否加载了新文件而不是安装目录中的旧副本。
- 翻译条目是否标记为 `unfinished`。
- 占位符数量是否一致导致条目被判为不可用。

下一篇将继续介绍 `QTranslator` 的加载顺序、资源系统部署、`LanguageChange` 事件、QML 热切换和多语言测试。
