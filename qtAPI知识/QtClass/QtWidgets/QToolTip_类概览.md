# Qt QToolTip 深入笔记

> 适用版本：Qt 6.11 Widgets  
> 头文件：`#include <QToolTip>`  
> 所属模块：`Qt6::Widgets`

## 1. 先建立整体认识：QToolTip 到底解决什么问题

工具提示（tool tip）是鼠标停留在控件或某个界面区域上时出现的一小段说明文字。它适合解释：

- 一个图标按钮的含义；
- 一个输入框需要填写什么；
- 一个状态指示器的当前含义；
- 鼠标悬停在复杂控件的某个局部区域时，该区域代表什么。

`QToolTip` 是 Qt 提供的**全局静态辅助类**。它没有实例对象，也不能通过 `new QToolTip` 或局部变量构造；所有 API 都是静态函数，直接以 `QToolTip::xxx()` 的形式调用。

它主要解决两类问题：

1. **直接弹出一条提示**：使用 `QToolTip::showText()` 在指定的全局坐标显示文本。
2. **修改工具提示的全局外观或查询全局状态**：使用 `setFont()`、`setPalette()`、`isVisible()`、`text()` 等函数。

不过，日常开发通常不应该一上来就调用 `QToolTip::showText()`。根据提示来源选择 API 更重要：

| 场景 | 优先使用 |
| --- | --- |
| 普通 `QWidget` 始终有一段固定提示 | `QWidget::setToolTip()` |
| `QAction` 同时出现在菜单、工具栏、快捷菜单等位置 | `QAction::setToolTip()` |
| 同一个控件的不同局部区域需要不同提示 | 处理 `QEvent::ToolTip`，再调用 `QToolTip::showText()` |
| 需要在任意坐标临时显示或隐藏提示 | `QToolTip::showText()` / `QToolTip::hideText()` |

可以把关系理解成：

```text
QWidget::setToolTip()       -> Qt 自动处理悬停事件 -> QToolTip 显示
QAction::setToolTip()       -> 菜单/工具栏等 action 宿主显示提示
自定义 QEvent::ToolTip     -> 代码判断区域      -> QToolTip::showText()
```

## 2. 构建与包含

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 头文件

```cpp
#include <QToolTip>
```

如果示例还使用 `QWidget::setToolTip()`、`QAction::setToolTip()` 或重载 `event()`，还需要包含对应的 `QWidget`、`QAction`、`QHelpEvent` 等头文件。

## 3. 最常见的用法：让 Qt 自动管理提示

### 3.1 普通控件使用 `QWidget::setToolTip()`

普通控件固定显示一段说明时，直接给控件设置工具提示即可：

```cpp
#include <QLineEdit>

auto *searchEdit = new QLineEdit(this);
searchEdit->setToolTip(tr("搜索当前文档中的文本"));
```

鼠标停留在 `searchEdit` 上时，Qt 会自动生成 `QEvent::ToolTip` 并显示提示。此时不需要自己启动定时器，也不需要手动跟踪鼠标位置。

这种写法适合提示内容只与控件整体有关的情况，例如：

- “请输入服务器地址”；
- “点击后刷新数据”；
- “文件大小：2.3 MB”。

### 3.2 `QAction` 使用 `QAction::setToolTip()`

如果一个操作同时放进菜单和工具栏，提示应该设置在 `QAction` 上，而不是只给某一个工具栏按钮设置：

```cpp
#include <QAction>
#include <QMainWindow>

auto *openAction = new QAction(tr("&打开..."), this);
openAction->setToolTip(tr("打开一个已有文件"));

fileMenu->addAction(openAction);
fileToolBar->addAction(openAction);
```

这样菜单项、工具栏按钮以及其他由这个 action 创建的界面元素都可以共享这份语义。动作提示属于操作本身，控件只是动作的不同展示宿主。

## 4. `showText()`：手动显示工具提示的核心 API

函数签名：

```cpp
static void showText(const QPoint &pos,
                     const QString &text,
                     QWidget *w = nullptr,
                     const QRect &rect = {},
                     int msecDisplayTime = -1);
```

### 4.1 `pos` 是全局坐标，不是控件局部坐标

`pos` 表示提示所关注的点，坐标系是**屏幕全局坐标**。工具提示会在这个点附近，以当前平台规定的偏移显示。

```cpp
QPoint globalPos = button->mapToGlobal(button->rect().center());
QToolTip::showText(globalPos, tr("这是一个临时提示"), button);
```

不要把 `button->rect().center()` 直接当成 `pos` 传入。`rect().center()` 是控件局部坐标；如果要作为 `showText()` 的位置，必须先用 `mapToGlobal()` 转换。

在处理 `QEvent::ToolTip` 时，`QHelpEvent::globalPos()` 已经是全局坐标，应直接传给 `showText()`：

```cpp
QToolTip::showText(helpEvent->globalPos(), tipText, this);
```

### 4.2 `w` 的两个作用

`w` 不是简单的“提示所属控件”标签，它有两个实际用途：

1. 当 `rect` 非空时，Qt 用 `w` 解释 `rect` 的局部坐标；
2. 在多屏环境下，Qt 可以借助 `w` 判断应该使用哪块屏幕。

因此，即使 `rect` 为空，在多显示器程序中也建议传入相关控件：

```cpp
QToolTip::showText(globalPos, text, targetWidget);
```

如果 `rect` 非空，则 `w` 必须提供，否则 Qt 无法知道这个矩形属于哪个坐标系。

### 4.3 `rect` 是控件局部坐标中的触发区域

`rect` 用来限制提示的有效区域。它的坐标属于 `w` 的局部坐标系；当鼠标离开这个矩形时，工具提示会被隐藏。

```cpp
QToolTip::showText(
    widget->mapToGlobal(QPoint(20, 10)),
    tr("鼠标离开这个区域后提示自动消失"),
    widget,
    QRect(0, 0, 120, 40));
```

这里的 `QRect(0, 0, 120, 40)` 不是屏幕坐标矩形，而是 `widget` 内部的局部矩形。

常见错误是把两个坐标系混在一起：

```cpp
// 错误思路：globalPos 是屏幕坐标，却把它传给局部 rect。
QToolTip::showText(globalPos, text, widget, QRect(globalPos, QSize(100, 30)));
```

正确做法是：

- `pos` 使用全局坐标；
- `rect` 使用 `w` 的局部坐标。

### 4.4 `text` 为空时表示隐藏

传入空字符串不会显示一个“空白提示”，而是隐藏当前工具提示：

```cpp
QToolTip::showText(QPoint(), QString());
```

这正是 `QToolTip::hideText()` 的实现语义。一般代码应直接调用后者，让意图更清晰：

```cpp
QToolTip::hideText();
```

### 4.5 相同文本不会自动移动

如果当前已经显示文本 `"正在加载"`，再次调用 `showText()` 显示同样的文本，即使传入了新的坐标，提示也不会移动。

需要强制把同一段文字移到新位置时，先隐藏再显示：

```cpp
QToolTip::hideText();
QToolTip::showText(newGlobalPos, tr("正在加载"), widget);
```

这条规则在自定义绘图控件或鼠标移动跟踪场景中尤其重要。

### 4.6 `msecDisplayTime` 的显示时长

`msecDisplayTime` 的单位是毫秒：

```cpp
QToolTip::showText(globalPos, tr("短暂提示"), widget, {}, 2000);
```

- 传入正数：提示显示指定的毫秒数；
- 默认值 `-1`：显示时长根据文本长度计算；
- 不要把它当成“鼠标停留多久后才显示”的延迟参数，它控制的是显示后的持续时间。

## 5. 富文本、换行与提示内容

工具提示支持富文本，因此可以使用简单的 HTML 格式：

```cpp
QToolTip::showText(
    globalPos,
    tr("<b>同步状态</b><br>上次同步：刚刚"),
    widget);
```

富文本默认会自动换行。如果确实需要保留空格和换行布局，可以使用 `white-space:pre`：

```cpp
QToolTip::showText(
    globalPos,
    tr("<p style='white-space:pre'>第一列    第二列\nA          B</p>"),
    widget);
```

提示适合提供短而有针对性的辅助信息，不适合承载完整帮助文档。文字过长会让提示难以扫描，也会让默认的自动换行结果难以控制。

## 6. 为同一个控件的不同区域提供不同提示

`QWidget::setToolTip()` 只能表达“整个控件共用一份提示”。如果一个自定义控件内部有多个区域，就需要处理 `QEvent::ToolTip`。

### 6.1 事件处理流程

流程如下：

1. 在控件的 `event()` 中判断事件类型是否为 `QEvent::ToolTip`；
2. 将事件转换为 `QHelpEvent`；
3. 用 `helpEvent->pos()` 判断鼠标位于控件的哪个局部区域；
4. 找到区域后，用 `helpEvent->globalPos()` 调用 `QToolTip::showText()`；
5. 没有匹配区域时调用 `QToolTip::hideText()`，并对事件调用 `ignore()`。

示例：

```cpp
#include <QEvent>
#include <QHelpEvent>
#include <QToolTip>
#include <QWidget>

class StatusWidget final : public QWidget
{
public:
    using QWidget::QWidget;

protected:
    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::ToolTip) {
            auto *helpEvent = static_cast<QHelpEvent *>(event);
            const QPoint localPos = helpEvent->pos();

            if (QRect(0, 0, 80, height()).contains(localPos)) {
                QToolTip::showText(
                    helpEvent->globalPos(),
                    tr("左侧表示连接状态"),
                    this,
                    QRect(0, 0, 80, height()));
            } else if (QRect(80, 0, width() - 80, height()).contains(localPos)) {
                QToolTip::showText(
                    helpEvent->globalPos(),
                    tr("右侧显示当前服务器名称"),
                    this,
                    QRect(80, 0, width() - 80, height()));
            } else {
                QToolTip::hideText();
                event->ignore();
            }

            return true;
        }

        return QWidget::event(event);
    }
};
```

### 6.2 `pos()` 与 `globalPos()` 的区别

在这个事件中，两个坐标分别用于不同目的：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 局部坐标 | `QHelpEvent::pos()` | 返回鼠标在当前控件内部的位置 | 用来判断内部区域或命中哪一段内容；不要直接传给 `showText()` |
| 屏幕坐标 | `QHelpEvent::globalPos()` | 返回鼠标在屏幕上的全局位置 | 传给 `QToolTip::showText()` 作为弹出位置；不要用它做控件内部命中 |

不要为了判断区域而使用 `globalPos()`，也不要把局部 `pos()` 直接当成 `showText()` 的第一个参数。

### 6.3 为什么隐藏后还要 `event->ignore()`

当 `QEvent::ToolTip` 没有对应内容时，调用 `hideText()` 只是隐藏当前提示；调用 `event->ignore()` 还会告诉 Qt：这个事件没有被当前控件作为有效提示处理，不要继续启动对应的工具提示模式。

因此，自定义处理中的“无匹配区域”通常写成：

```cpp
QToolTip::hideText();
event->ignore();
return true;
```

### 6.4 动态区域尺寸的注意点

如果区域依赖当前控件大小，`rect` 也应使用当前尺寸构造。不要在控件大小变化后仍然复用一个旧矩形，否则鼠标离开真实区域时提示可能不能及时隐藏。

## 7. 在 item view 中自定义提示

对于 `QListView`、`QTableView`、`QTreeView` 等 item view，模型/视图体系已经支持为数据项设置工具提示。例如，模型可以通过 `Qt::ToolTipRole` 返回提示文本，或使用具体 item 类的 `setToolTip()`。

如果只是给每个数据项提供固定提示，优先让模型提供 `Qt::ToolTipRole`，不要在视图中重复维护一套坐标判断。

如果提示内容依赖鼠标所在单元格的自定义区域、当前状态或额外业务计算，则应在 `QAbstractItemView::viewportEvent()` 中拦截 `QEvent::ToolTip`：

```cpp
bool CustomTable::viewportEvent(QEvent *event)
{
    if (event->type() == QEvent::ToolTip) {
        auto *helpEvent = static_cast<QHelpEvent *>(event);
        const QModelIndex index = indexAt(helpEvent->pos());

        if (index.isValid()) {
            QToolTip::showText(
                helpEvent->globalPos(),
                tooltipFor(index),
                viewport());
        } else {
            QToolTip::hideText();
            event->ignore();
        }

        return true;
    }

    return QTableView::viewportEvent(event);
}
```

这里的 `helpEvent->pos()` 是 viewport 的局部坐标，因此应传给 `indexAt()`；不是整个表格窗口的坐标。

## 8. 查询当前提示状态

### 8.1 `isVisible()`

`QToolTip::isVisible()` 返回当前是否有工具提示正在显示：

```cpp
if (QToolTip::isVisible()) {
    qDebug() << "当前提示：" << QToolTip::text();
}
```

它表示的是 `QToolTip` 的全局当前状态，不是某一个控件的属性。程序中同时只能把它当作“当前全局提示是否可见”来理解。

### 8.2 `text()`

`QToolTip::text()` 返回当前正在显示的提示文本；没有可见提示时返回空字符串：

```cpp
const QString visibleText = QToolTip::text();
```

不要把它理解成某个控件通过 `setToolTip()` 设置的原始属性。要读取某个控件配置的固定提示，应读取 `widget->toolTip()`；`QToolTip::text()` 只反映当前屏幕上正在显示的全局提示。

## 9. 修改全局字体与调色板

### 9.1 `setFont()` 和 `font()`

`QToolTip::setFont()` 设置工具提示使用的全局字体：

```cpp
QFont font = QToolTip::font();
font.setPointSize(font.pointSize() + 1);
QToolTip::setFont(font);
```

`font()` 用于读取当前工具提示字体。

这不是某个控件级属性，而是工具提示系统的全局配置。通常应在应用初始化或主题切换时统一设置，不要在鼠标移动事件中反复设置。

### 9.2 `setPalette()` 和 `palette()`

`setPalette()` 设置工具提示绘制时使用的全局调色板：

```cpp
QPalette palette = QToolTip::palette();
palette.setColor(QPalette::Inactive, QPalette::ToolTipBase, QColor("#fff8c5"));
palette.setColor(QPalette::Inactive, QPalette::ToolTipText, QColor("#202020"));
QToolTip::setPalette(palette);
```

工具提示不是活动窗口，因此 Qt 使用 `QPalette::Inactive` 颜色组来绘制它。只修改 `QPalette::Active` 的颜色，可能看不到预期效果。

同样，`palette()` 读取的是工具提示系统使用的调色板，不是某个具体控件的 `widget->palette()`。

### 9.3 全局样式的使用边界

修改 `QToolTip` 的字体或调色板会影响应用中的所有工具提示。应注意：

- 主题初始化时统一配置；
- 主题切换时成组更新；
- 不要为了一个局部控件临时修改全局值；
- 与应用的 `QApplication` / `QGuiApplication` 级别字体和调色板保持一致。

如果只是某个控件需要不同颜色，通常应重新考虑提示内容或控件设计，而不是在显示单个提示前修改全局调色板。

## 10. 生命周期、线程与所有权

### 10.1 没有 `QToolTip` 对象可管理

`QToolTip` 构造函数被删除：

```cpp
QToolTip tip;              // 错误
auto *tip = new QToolTip;  // 错误
```

它没有实例生命周期，也没有父子对象所有权。提示窗口由 Qt 的工具提示系统管理，调用方只负责提供文本、坐标和必要的宿主控件。

### 10.2 不需要保存返回对象

`showText()` 返回 `void`，不会返回一个可操作的提示窗口指针。要修改当前提示，应再次调用 `showText()`；要隐藏提示，应调用 `hideText()` 或传入空文本。

### 10.3 在 GUI 线程调用

它属于 Widgets 的界面 API，应在 GUI 线程中调用，并且应用需要正常运行事件循环。后台线程如果计算出了提示内容，应通过信号、槽或其他线程安全方式把结果交给 GUI 线程，再更新控件或显示提示。

## 11. 常见误区与排查顺序

### 11.1 “调用了 `showText()`，但提示没有出现在预期位置”

依次检查：

1. `pos` 是否已经通过 `mapToGlobal()` 转为全局坐标；
2. 是否误把控件局部坐标传给了 `pos`；
3. `w` 是否是正确的宿主控件；
4. 是否有另一次 `showText()` 或 `hideText()` 很快覆盖了当前提示；
5. 是否在调用后立即退出了事件循环或销毁了相关界面。

### 11.2 “`rect` 参数没有按预期工作”

检查 `rect` 是否使用了 `w` 的局部坐标。只要 `rect` 非空，就必须传入 `w`：

```cpp
QToolTip::showText(globalPos, text, widget, widget->rect());
```

如果不需要鼠标离开区域后自动隐藏，直接省略 `rect`，使用默认的空矩形。

### 11.3 “相同文字换了位置却不移动”

这是 `showText()` 的明确行为。先隐藏，再显示：

```cpp
QToolTip::hideText();
QToolTip::showText(newPos, sameText, widget);
```

### 11.4 “修改调色板却没有效果”

工具提示使用 `QPalette::Inactive` 颜色组。确认修改的是：

```cpp
palette.setColor(QPalette::Inactive, QPalette::ToolTipBase, baseColor);
palette.setColor(QPalette::Inactive, QPalette::ToolTipText, textColor);
```

### 11.5 “普通控件不应该手动调用 `showText()`”

如果控件只有一段固定提示，优先使用：

```cpp
widget->setToolTip(tr("固定提示"));
```

手动调用 `showText()` 会让代码承担坐标、事件、隐藏时机和重复显示等额外责任。只有在提示内容或触发区域确实需要动态判断时，才值得接管 `QEvent::ToolTip`。

### 11.6 “自定义提示在 item view 中不响应”

item view 的鼠标提示事件通常发生在 viewport 上。应重载 `viewportEvent()`，而不是只重载外层 view 的普通 `event()` 并假设能拿到正确的局部坐标。

## 12. API 逐项说明

### `[static] void QToolTip::showText(const QPoint &pos, const QString &text, QWidget *w = nullptr, const QRect &rect = {}, int msecDisplayTime = -1)`

**作用：** 在指定的全局位置附近显示一条工具提示。

**参数含义：**

- `pos`：全局屏幕坐标，表示提示关注的点；
- `text`：提示文本，可以是富文本；
- `w`：相关控件。`rect` 非空时它还提供局部坐标系；多屏时可帮助 Qt 选择屏幕；
- `rect`：`w` 局部坐标中的有效区域。鼠标离开该区域后隐藏提示；
- `msecDisplayTime`：显示时长，单位为毫秒；`-1` 表示根据文本长度决定。

**关键规则：**

- `text` 为空时隐藏提示；
- 如果新文本与当前可见文本相同，提示不会自动移动；
- 想让相同文本移动，先调用 `hideText()`；
- `pos` 和 `rect` 使用不同坐标系；
- `rect` 非空时必须提供 `w`。

### `[static] void QToolTip::hideText()`

**作用：** 隐藏当前工具提示。

它等价于：

```cpp
QToolTip::showText(QPoint(), QString());
```

在自定义 `QEvent::ToolTip` 处理里，如果当前区域没有对应提示，应在隐藏后对事件调用 `ignore()`。

### `[static] bool QToolTip::isVisible()`

**作用：** 查询当前是否有工具提示正在显示。

返回值为 `true` 表示全局工具提示当前可见，`false` 表示没有可见提示。它不是某个具体控件的 `toolTip` 属性查询。

### `[static] QString QToolTip::text()`

**作用：** 获取当前可见工具提示的文本。

如果当前没有可见提示，返回空字符串。它读取的是屏幕上当前显示的全局提示，而不是控件通过 `setToolTip()` 保存的配置。

### `[static] QPalette QToolTip::palette()`

**作用：** 获取工具提示绘制时使用的全局调色板。

工具提示使用 `QPalette::Inactive` 颜色组，因为工具提示不是活动窗口。读取后可以修改副本，再通过 `setPalette()` 应用。

### `[static] void QToolTip::setPalette(const QPalette &palette)`

**作用：** 设置工具提示绘制时使用的全局调色板。

这个设置会影响应用中的所有工具提示。修改提示背景和文字颜色时，优先检查 `Inactive` 颜色组中的 `ToolTipBase` 和 `ToolTipText`。

### `[static] QFont QToolTip::font()`

**作用：** 获取工具提示使用的全局字体。

返回的是工具提示系统当前使用的字体，不是某个控件的字体。适合在应用启动或主题设置阶段读取并调整。

### `[static] void QToolTip::setFont(const QFont &font)`

**作用：** 设置工具提示使用的全局字体。

它会影响应用中的所有工具提示。不要为了一个局部提示在高频鼠标事件中重复设置。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 显示 | `[static] void showText(const QPoint &pos, const QString &text, QWidget *w = nullptr, const QRect &rect = {}, int msecShowTime = -1)` | 在指定屏幕全局坐标附近显示一条工具提示，并可指定归属控件、有效区域和显示时长。 | `pos` 是全局坐标；`rect` 是 `w` 的局部坐标；`rect` 非空时必须传 `w`；空文本会隐藏当前提示；相同文本不会自动移动。 |
| 隐藏 | `[static] void hideText()` | 隐藏当前全局工具提示。 | 等价于用空文本调用 `showText()`；在 `QEvent::ToolTip` 处理中通常还应对事件调用 `ignore()`。 |
| 状态 | `[static] bool isVisible()` | 查询当前是否有工具提示可见。 | 查询的是全局工具提示服务状态，不是某个控件的 `toolTip` 属性。 |
| 状态 | `[static] QString text()` | 返回当前可见工具提示的文本。 | 没有可见提示时返回空字符串；它不是读取某个 widget 的固定提示。 |
| 外观 | `[static] QPalette palette()` | 获取工具提示服务当前使用的全局调色板。 | 返回的是全局提示 palette；修改前应考虑应用主题和 `ToolTipBase/ToolTipText` 角色。 |
| 外观 | `[static] void setPalette(const QPalette &palette)` | 设置所有工具提示使用的全局调色板。 | 影响应用内所有提示，不适合在高频鼠标事件中反复设置。 |
| 外观 | `[static] QFont font()` | 获取工具提示服务当前使用的全局字体。 | 它不是某个控件的字体；适合在主题配置阶段读取。 |
| 外观 | `[static] void setFont(const QFont &font)` | 设置所有工具提示使用的全局字体。 | 影响全局提示；局部提示内容不应靠频繁改全局字体解决。 |

## 14. 选择哪种工具提示方案

| 需求 | 推荐方案 | 原因 |
| --- | --- | --- |
| 一个控件只有一段固定说明 | `QWidget::setToolTip()` | Qt 自动处理悬停、显示和隐藏 |
| 一个动作被多个界面元素复用 | `QAction::setToolTip()` | 提示跟随动作，而不是绑定某个展示控件 |
| 一个控件内部多个区域有不同提示 | 处理 `QEvent::ToolTip` + `QToolTip::showText()` | 可以根据 `QHelpEvent::pos()` 选择文本 |
| 表格或树的每个数据项有提示 | 模型的 `Qt::ToolTipRole` | 提示属于数据项，符合 model/view 分工 |
| item view 提示需要动态计算 | `QAbstractItemView::viewportEvent()` | 事件坐标属于 viewport，适合结合索引计算 |
| 修改所有提示的字体或颜色 | `QToolTip::setFont()` / `setPalette()` | 这是全局工具提示配置 |

---

### 一句话总结

`QToolTip` 不是一个需要创建和管理生命周期的控件，而是 Qt 的全局工具提示服务。普通控件优先使用 `QWidget::setToolTip()`，动作优先使用 `QAction::setToolTip()`；只有当提示位置、内容或有效区域需要代码动态判断时，才在 `QEvent::ToolTip` 中使用 `showText()`。使用它时最关键的是记住：`pos` 是全局坐标，`rect` 是 `w` 的局部坐标，空文本表示隐藏，而相同文本不会自动移动。
