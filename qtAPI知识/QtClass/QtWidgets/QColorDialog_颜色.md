# QColorDialog 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QColorDialog>`  
> 模块：`Qt6::Widgets`  
> 继承：`QDialog -> QColorDialog`  
> 常见搭档：`QColor`、`QPalette`、`QBrush`、`QPen`

`QColorDialog` 负责让用户选择一个 `QColor`。它不保存主题，不替你把颜色应用到控件，也不负责绘图；它只是把“用户怎么挑颜色”这件事包装成一个标准对话框，并把过程色和最终色用属性、静态函数与信号交给你。

## 1. 它解决什么问题

颜色选择看似只是一个 RGB 值，实际 UI 里会遇到很多细节：

- 用户需要从标准色、最近/自定义色或色域面板里挑；
- 有时要允许透明度，有时不能让 alpha 出现；
- 有些平台有原生颜色面板，产品又可能要求 Qt 自绘一致外观；
- 绘图工具需要实时预览，但“取消”时还要恢复原色；
- 简单表单只需要一次性拿到确认后的颜色。

`QColorDialog` 把这些需求拆成两种使用方式：

| 用法 | 适合什么 | 关键 API |
| --- | --- | --- |
| 静态函数 | 点击按钮后阻塞式选择一次颜色 | `QColorDialog::getColor()` |
| 对象对话框 | 需要实时预览、异步打开、复用对话框或细调选项 | `setCurrentColor()`、`open()`、`currentColorChanged()`、`colorSelected()` |

如果界面只允许用户在 5 个品牌色里选一个，用一排色块按钮通常更清楚；如果需要完整调色、alpha、原生取色器或标准颜色面板，才是 `QColorDialog` 发挥价值的时候。

## 2. 最短路径：静态 `getColor()`

```cpp
#include <QApplication>
#include <QColorDialog>
#include <QPushButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QPushButton button(QObject::tr("Choose color"));
    QObject::connect(&button, &QPushButton::clicked, [&] {
        const QColor color = QColorDialog::getColor(
            Qt::white,
            &button,
            QObject::tr("Choose button color"),
            QColorDialog::ShowAlphaChannel);

        if (!color.isValid())
            return;

        button.setStyleSheet(QStringLiteral("background-color: %1")
                                 .arg(color.name(QColor::HexArgb)));
    });

    button.show();
    return app.exec();
}
```

`getColor()` 的返回值必须检查 `isValid()`。用户点取消、关闭窗口或原生面板没有产生有效选择时，都不应该把返回值当作新颜色直接写入配置。

静态函数适合“一点按钮，选完，返回”的流程。它不适合做 live preview，因为调用方直到对话框结束才拿到结果；需要实时预览时，创建对象并连接信号。

## 3. 对象版：区分过程色和最终色

```cpp
auto *dialog = new QColorDialog(currentBrushColor, this);
dialog->setOption(QColorDialog::ShowAlphaChannel);

connect(dialog, &QColorDialog::currentColorChanged,
        this, [this](const QColor &color) {
            previewBrushColor(color);
        });

connect(dialog, &QColorDialog::colorSelected,
        this, [this](const QColor &color) {
            applyBrushColor(color);
        });

dialog->open();
```

这里有两个颜色概念：

| 概念 | API | 语义 |
| --- | --- | --- |
| 当前色 | `currentColor()` / `setCurrentColor()` | 用户正在面板中预览或拖动到的颜色 |
| 选中色 | `selectedColor()` / `colorSelected()` | 用户确认后产生的颜色 |

实时预览时要准备“取消恢复”策略：`currentColorChanged()` 可能发出很多次，但用户最后可能取消。常见做法是打开前保存旧颜色，预览阶段只改临时显示，`colorSelected()` 才写入模型；若对话框 rejected，则恢复旧颜色。

## 4. 四个选项位

```cpp
dialog->setOptions(QColorDialog::ShowAlphaChannel
                   | QColorDialog::DontUseNativeDialog);
```

| 选项 | 作用 | 使用场景与边界 |
| --- | --- | --- |
| `ShowAlphaChannel` | 显示透明度通道 | 绘图、图层、主题颜色常用；普通表单色可能不该暴露 alpha |
| `NoButtons` | 不显示 OK / Cancel 按钮 | 适合即时生效面板；取消/确认语义需要自己设计 |
| `DontUseNativeDialog` | 强制使用 Qt 自绘对话框 | 需要统一样式或嵌入式行为时使用；会放弃平台原生体验 |
| `NoEyeDropperButton` | 隐藏滴管取色按钮 | 安全、权限或产品不希望跨窗口取色时使用 |

选项最好在显示前设置。尤其是原生/非原生对话框相关选项，显示后再改可能受平台实现限制，结果不一定符合预期。

`setOption(option, false)` 只关闭某一个位；`setOptions(options)` 是整体替换。若你先配置了一组 flags，再调用 `setOptions(QColorDialog::NoButtons)`，之前的 `ShowAlphaChannel` 会被清掉。

## 5. 自定义颜色槽和标准颜色槽

`QColorDialog` 提供两组静态颜色槽：

```cpp
const int count = QColorDialog::customCount();
QColorDialog::setCustomColor(0, QColor("#2b7cff"));
QColorDialog::setStandardColor(0, QColor("#1f2328"));

QColor custom = QColorDialog::customColor(0);
QColor standard = QColorDialog::standardColor(0);
```

这些槽更像对话框使用的共享调色板，不是某个 `QColorDialog` 实例的私有属性。适合放最近常用色、品牌色或启动时预置的常见色。由于它们是静态接口，模块之间若都随意写槽位，最终会互相覆盖；产品级应用应集中初始化，或约定哪些槽位归谁使用。

`customCount()` 返回可用自定义槽数量。使用索引前应确保在范围内，别把它当作无限数组。

## 6. 原生对话框与 Qt 对话框

默认情况下，Qt 可能使用平台原生颜色对话框。原生对话框的优点是用户熟悉，外观和系统一致；缺点是某些选项或嵌入行为不完全受 Qt 控制。

强制 Qt 自绘：

```cpp
dialog->setOption(QColorDialog::DontUseNativeDialog);
```

适合以下场景：

- 需要稳定测试 UI；
- 需要统一跨平台外观；
- 需要 `NoButtons`、alpha、预览等行为更可控；
- 产品设计明确不希望弹出平台原生面板。

不适合为了“看起来一样”盲目关闭原生对话框。桌面应用很多时候应该尊重系统颜色面板，尤其是用户习惯依赖系统级色板或取色工具时。

## 7. 打开方式：`exec()`、`open()` 与接收者回调

作为 `QDialog`，它继承了 `exec()`、`open()`、`accept()`、`reject()` 等能力。本类又提供：

```cpp
dialog->open(receiver, SLOT(useColor(QColor)));
```

这个重载把“对话框确认后调用哪个成员”包装起来。现代代码里更常见的是直接连接 `colorSelected()`，语义更清楚，也避免老式字符串签名写错。

阻塞式 `exec()` 让流程写起来直，但会进入局部事件循环。普通按钮触发一次颜色选择可以接受；复杂状态机、跨线程信号、嵌套对话框多的界面中，更推荐 `open()` + 信号。

## 8. 常见误用

| 现象 | 原因 | 处理方式 |
| --- | --- | --- |
| 用户取消后颜色被改成黑色或白色 | 没检查 `getColor()` 返回值是否有效 | 先判断 `color.isValid()` |
| 拖动色盘时配置文件被不断写入 | 把 `currentColorChanged()` 当最终确认 | 预览用它，持久化放到 `colorSelected()` |
| `setOptions()` 后 alpha 不见了 | `setOptions()` 整体替换了 flags | 用按位 OR 传完整选项，或用 `setOption()` 改单项 |
| 跨模块预设色互相覆盖 | 静态颜色槽是共享状态 | 集中初始化或约定槽位 |
| 非原生选项没效果 | 对话框已显示，平台原生面板已创建 | 显示前设置 `DontUseNativeDialog` |
| 只允许少数主题色却弹完整对话框 | 工具过重，用户选择范围过大 | 使用色块按钮、菜单或自定义小面板 |

## API 速查表
下表按 Qt 6.11.1 的 `qcolordialog.h` 直接声明整理。继承自 `QDialog` 的 `exec()`、`accept()`、`reject()` 等在实际使用中很重要，但不属于本类新增声明。

### 9.1 构造、颜色状态与选项

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QColorDialog(QWidget *parent = nullptr)` | 创建颜色对话框 | 默认当前色由实现初始化；通常打开前显式 `setCurrentColor()` |
| 构造 | `QColorDialog(const QColor &initial, QWidget *parent = nullptr)` | 创建并设置初始当前色 | 适合编辑已有颜色 |
| 生命周期 | `~QColorDialog()` | 销毁对话框 | 遵循 QObject 父子对象树 |
| 当前色 | `setCurrentColor(const QColor &color)` | 设置正在预览的颜色 | 打开前设初值，打开后可用于同步外部选择 |
| 当前色 | `currentColor() const` | 读取正在预览的颜色 | 可能不是最终确认结果 |
| 结果色 | `selectedColor() const` | 读取最终选中的颜色 | 通常在 accepted 或 `colorSelected()` 后读取 |
| 单项选项 | `setOption(ColorDialogOption option, bool on = true)` | 开关某一个选项位 | 只影响指定 bit，适合增量配置 |
| 单项选项 | `testOption(ColorDialogOption option) const` | 判断某选项是否开启 | 用于根据配置调整外部 UI |
| 批量选项 | `setOptions(ColorDialogOptions options)` | 整体替换所有选项 | 会清除未包含的旧选项 |
| 批量选项 | `options() const` | 读取当前选项 flags | 可用于保存或调试配置 |

### 9.2 打开、静态调色板与信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 异步打开 | `open(QObject *receiver, const char *member)` | 异步打开并在确认后调用接收者成员 | 老式字符串签名；现代代码常直接连接 `colorSelected()` |
| 可见性 | `setVisible(bool visible)` | 显示或隐藏对话框 | 重写用于同步内部面板；选项最好显示前配置 |
| 静态入口 | `getColor(const QColor &initial = Qt::white, QWidget *parent = nullptr, const QString &title = QString(), ColorDialogOptions options = {})` | 一次性打开颜色对话框并返回选择结果 | 取消时返回无效颜色，必须检查 `isValid()` |
| 自定义色槽 | `customCount()` | 返回可用自定义颜色槽数量 | 索引必须在范围内 |
| 自定义色槽 | `customColor(int index)` | 读取指定自定义颜色槽 | 静态共享槽，不属于某个实例 |
| 自定义色槽 | `setCustomColor(int index, QColor color)` | 写入指定自定义颜色槽 | 适合保存最近常用色；避免模块互相覆盖 |
| 标准色槽 | `standardColor(int index)` | 读取指定标准颜色槽 | 静态共享状态 |
| 标准色槽 | `setStandardColor(int index, QColor color)` | 写入指定标准颜色槽 | 适合应用启动时预置品牌色 |
| 信号 | `currentColorChanged(const QColor &color)` | 当前预览色变化时发出 | 会高频触发；适合 live preview |
| 信号 | `colorSelected(const QColor &color)` | 用户确认颜色时发出 | 适合写入模型、配置或真正应用颜色 |

### 9.3 受保护扩展点与枚举

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件 | `changeEvent(QEvent *event)` | 响应语言、样式、调色板等变化 | 派生类扩展时应保留基类处理 |
| 结束 | `done(int result)` | 对话框结束前后的收尾入口 | 重写时要保持 accepted/rejected 语义 |
| 选项枚举 | `ShowAlphaChannel` | 显示 alpha 通道 | 透明度有业务意义时才开启 |
| 选项枚举 | `NoButtons` | 隐藏 OK / Cancel | 需要即时应用或嵌入式选择时使用 |
| 选项枚举 | `DontUseNativeDialog` | 强制 Qt 自绘颜色对话框 | 显示前设置；会放弃原生面板 |
| 选项枚举 | `NoEyeDropperButton` | 隐藏滴管按钮 | 平台不支持或产品不允许屏幕取色时使用 |
| flags | `ColorDialogOptions` | `ColorDialogOption` 的按位组合 | 用 `|` 组合多个选项 |

## 10. 使用建议

把颜色选择拆成三个问题：用户能选哪些颜色，选择过程中要不要预览，确认后写到哪里。只要一次性拿结果，用 `getColor()`；需要过程控制，用对象版对话框和 `currentColorChanged()` / `colorSelected()`。这样既不丢取消语义，也不会让颜色对话框偷偷承担业务模型的责任。
