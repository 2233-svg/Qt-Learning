# Qt QFontDialog 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QFontDialog>`
> 所属模块：`Qt6::Widgets`
> 继承：`QDialog -> QFontDialog`
> 常见搭档：`QFont`、`QLabel`、`QTextEdit`

## 1. QFontDialog 解决什么问题

`QFontDialog` 让用户挑字体。它不负责显示文本，也不负责应用字体，它只负责把“家族、字重、字号、是否等宽”等字体选择工作交给用户。

常见场景：

- 富文本编辑器选字体；
- 主题设置里选标题字体；
- 打印/预览前选排版字体；
- 给某个控件即时换字体。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QFontDialog>
#include <QPushButton>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QPushButton button("选择字体");
    QObject::connect(&button, &QPushButton::clicked, [&] {
        bool ok = false;
        QFont font = QFontDialog::getFont(&ok, button.font(), &button, "选择字体");
        if (ok)
            button.setFont(font);
    });

    button.show();
    return app.exec();
}
```

`getFont()` 返回的是完整 `QFont`，不是字符串。  
你拿到的是可以直接 `setFont()` 的对象。

## 3. currentFont 和 selectedFont

```cpp
dialog.setCurrentFont(QFont("Times New Roman", 12));
QFont live = dialog.currentFont();
QFont chosen = dialog.selectedFont();
```

这两个值不要混：

- `currentFont`：对话框里当前正在预览的字体；
- `selectedFont`：用户最终确认时选中的字体。

对应信号也是两套：

- `currentFontChanged()`：实时变化；
- `fontSelected()`：最终确认。

## 4. 过滤字体类型

```cpp
dialog.setOption(QFontDialog::ScalableFonts, true);
dialog.setOption(QFontDialog::MonospacedFonts, true);
dialog.setOption(QFontDialog::ProportionalFonts, false);
```

可用选项：

- `NoButtons`：没有 OK / Cancel，适合 live 预览；
- `DontUseNativeDialog`：不用原生字体面板；
- `ScalableFonts`：显示可缩放字体；
- `NonScalableFonts`：显示非可缩放字体；
- `MonospacedFonts`：显示等宽字体；
- `ProportionalFonts`：显示比例字体。

如果你在做代码编辑器、终端模拟器这类产品，`MonospacedFonts` 很实用。

## 5. 静态入口和异步入口

```cpp
QFont font = QFontDialog::getFont(&ok, initialFont, parent, "选择字体", options);
```

`getFont()` 是最常用的一次性入口。  
如果你想让对话框非阻塞地跑，也可以用 `open(QObject *, const char *)`。

实时变化时，`currentFontChanged` 可以驱动预览；  
真正确认后，`fontSelected` 负责落地。

## 6. 适合什么时候用

适合：

- 让用户选择一个字体配置；
- 想要标准的字体选择 UI；
- 需要兼容 Qt 原生/非原生风格。

不适合：

- 只想切换“粗体/斜体/字号”的小面板，那自己做更轻；
- 想定制特别复杂的字体策略，字体对话框太重了。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFontDialog(QWidget *parent = nullptr)` | 创建字体选择对话框。 | 默认使用系统初始字体；适合对象式配置。 |
| 构造 | `QFontDialog(const QFont &initial, QWidget *parent = nullptr)` | 创建并指定初始预览字体。 | 适合编辑已有文本或控件字体。 |
| 析构 | `~QFontDialog()` | 销毁字体对话框。 | 一般由 Qt 父对象或局部对象管理。 |
| 当前状态 | `setCurrentFont(const QFont &font)` / `currentFont() const` | 设置或读取用户当前正在预览的字体。 | 这是过程状态，适合实时预览，不代表用户已确认。 |
| 最终状态 | `selectedFont() const` | 读取用户最终确认的字体。 | 确认后使用；取消时不要把它当成新配置。 |
| 选项 | `setOption(FontDialogOption option, bool on = true)` / `testOption(...) const` | 开关或查询某个字体过滤/外观选项。 | 等宽、比例、可缩放字体过滤可以组合使用。 |
| 选项 | `setOptions(FontDialogOptions options)` / `options() const` | 批量设置或读取选项集合。 | 初始化时统一设置更清楚。 |
| 静态选择 | `getFont(bool *ok, QWidget *parent = nullptr)` | 用系统默认初始字体弹出一次性字体选择器。 | `ok` 用于区分确认和取消。 |
| 静态选择 | `getFont(bool *ok, const QFont &initial, QWidget *parent, const QString &title, FontDialogOptions options)` | 用指定初始字体、标题和选项完成一次性选择。 | 最常见的静态入口；确认后才应用结果。 |
| 异步打开 | `open(QObject *receiver, const char *member)` | 非阻塞打开，并把结果连接到旧式槽。 | 需要按 `fontSelected` 等信号处理最终结果。 |
| 显示 | `setVisible(bool visible)` | 控制对话框显示和隐藏。 | 对象式使用可配合 `show/open`；不要和静态入口混用。 |
| 信号 | `currentFontChanged(const QFont &font)` | 预览字体变化时通知。 | 适合实时更新示例文本或编辑器预览。 |
| 信号 | `fontSelected(const QFont &font)` | 用户确认字体后通知。 | 适合写入设置或正式应用到目标控件。 |
| 事件 | `changeEvent(QEvent *event)` | 响应字体、语言和样式变化。 | 派生重写时保留基类行为。 |
| 事件过滤 | `eventFilter(QObject *object, QEvent *event)` | 过滤内部控件事件。 | 只有深度定制对话框行为时才使用。 |
| 结果 | `done(int result)` | 处理对话框关闭结果。 | 重写时要正确区分 Accepted/Rejected。 |

### 一句话总结

`QFontDialog` 的重点是“预览和确认”两套字体状态：`currentFont` 管过程，`selectedFont` 管结果。
