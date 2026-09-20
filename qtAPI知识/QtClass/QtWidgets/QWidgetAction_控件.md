# Qt QWidgetAction 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QWidgetAction>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAction -> QWidgetAction`  
> 定位：让一个 action 在菜单或工具栏中显示为真实 `QWidget`

## 1. QWidgetAction 解决什么问题

普通 `QAction` 表示的是一个命令：

- 放进菜单后显示为菜单项；
- 放进工具栏后显示为按钮；
- 可以携带文本、图标、快捷键、启用状态、选中状态和 `triggered()` 信号。

但有些操作不是一个按钮能表达的：

- 工具栏里的缩放比例下拉框；
- 菜单里的搜索框；
- 工具栏里的字体选择器、颜色选择器或模式切换控件；
- 同一个业务操作需要同时出现在工具栏和菜单中，并且每个容器都要有自己的控件实例。

`QWidgetAction` 的作用是把“action 的命令语义”和“真实 QWidget 的可视表现”连接起来：

```text
QAction
  ├─ 命令语义：文本、图标、enabled、visible、data、triggered()
  └─ QWidgetAction：在支持的 action 容器中提供 QWidget
       ├─ QToolBar
       └─ QMenu
```

它仍然是 `QAction`，不是 `QWidget`。因此不能直接对它调用 `show()` 或把它当布局子控件使用，必须把它加入 `QMenu`、`QToolBar` 等 action 容器。

## 2. 什么时候使用，什么时候不要使用

适合使用 `QWidgetAction` 的场景：

- 控件需要出现在 `QMenu` 或 `QToolBar` 的 action 序列中；
- 希望控件和普通 action 一样受 `addAction()`、`removeAction()`、`setEnabled()`、`setVisible()` 管理；
- 同一个业务动作需要在多个 action 容器中各生成一份控件；
- 控件变化需要触发统一的 action 或业务逻辑。

不适合使用的场景：

- 控件只在一个普通页面中出现，此时直接把它加入布局更简单；
- 需要复杂表单、长期输入或多步交互，此时应使用普通页面、`QDialog` 或 `QDockWidget`；
- 只是想往一个工具栏临时放控件，不需要 action 语义，此时 `QToolBar::addWidget()` 更直接。

尤其要注意：`QWidgetAction` 不是“把任意复杂控件塞进菜单”的通用容器。菜单有自动关闭、键盘焦点、平台原生菜单等规则，复杂交互通常不适合放在菜单中。

## 3. 最小可用示例：一个默认控件

当一个 action 只会在一个容器中使用时，可以设置一个默认 widget：

```cpp
#include <QComboBox>
#include <QToolBar>
#include <QWidgetAction>

auto *zoomBox = new QComboBox;
zoomBox->addItems({"50%", "75%", "100%", "125%", "150%"});

auto *zoomAction = new QWidgetAction(this);
zoomAction->setText(tr("Zoom"));
zoomAction->setDefaultWidget(zoomBox);

toolBar->addAction(zoomAction);
```

`setDefaultWidget()` 将这个 widget 交给 `QWidgetAction` 管理。action 被容器请求显示时，默认 widget 会被重新设置到容器提供的父控件下。

默认 widget 是**一个具体的控件实例**，不是一个工厂。它在同一时刻只能出现在一个容器中。如果同一个 action 需要同时显示在两个工具栏或菜单中，就不能只依赖 `setDefaultWidget()`。

## 4. 多容器场景：重写 createWidget()

如果同一个 action 可能出现在多个容器中，应继承 `QWidgetAction`，在 `createWidget()` 中为每个容器创建一个独立 widget：

```cpp
#include <QComboBox>
#include <QWidgetAction>

class ZoomAction final : public QWidgetAction
{
public:
    explicit ZoomAction(QObject *parent)
        : QWidgetAction(parent)
    {
        setText(QObject::tr("Zoom"));
    }

protected:
    QWidget *createWidget(QWidget *parent) override
    {
        auto *box = new QComboBox(parent);
        box->addItems({"50%", "75%", "100%", "125%", "150%"});

        connect(box, &QComboBox::currentTextChanged,
                this, [this](const QString &text) {
                    setData(text);
                    trigger();
                });

        return box;
    }
};
```

`createWidget()` 的几个约束：

- 每次调用通常都应该返回一个新的 widget；
- 新 widget 的 parent 应使用传入的 `parent`；
- 不需要提供控件时可以返回 `nullptr`；
- widget 被用户操作后，要由代码决定何时更新 action 或业务对象；
- 多个 widget 同时存在时，必须主动同步它们的状态。

容器加入 action 后，通常会自动请求 widget；业务代码一般不需要手动调用 `requestWidget()`。

## 5. 容器、action 和 widget 的生命周期协议

支持 `QWidgetAction` 的容器大致按照下面的协议工作：

```text
容器加入 action
    -> requestWidget(parent)
       -> 如果默认 widget 可用，返回默认 widget
       -> 否则调用 createWidget(parent)

容器移除 action
    -> releaseWidget(widget)
       -> 默认 widget：释放占用状态，保留 widget
       -> createWidget 创建的 widget：调用 deleteWidget(widget)
```

这里有三个不同的所有权概念：

1. `QWidgetAction` 本身由 QObject parent 或其他 QObject 生命周期管理；
2. 默认 widget 由 `QWidgetAction` 持有，并且只能被一个容器同时使用；
3. `createWidget()` 返回的 widget 通常由容器作为父控件管理，释放时由 `deleteWidget()` 处理。

默认的 `deleteWidget()` 会隐藏 widget，并调用 `deleteLater()` 延迟删除。子类只有在确实需要自定义回收策略时才重写它。

`releaseWidget()` 不是“让业务代码取回 widget”的接口，而是容器释放 action 表现时使用的协议入口。直接在业务代码中随意调用它，容易破坏容器和 action 之间的状态。

## 6. 默认 widget 和 createWidget() 如何选择

| 做法 | 适合场景 | 关键限制 |
| --- | --- | --- |
| `setDefaultWidget(widget)` | 控件只在一个菜单或工具栏中显示。 | 只有一个实体；不能同时显示在多个容器中。 |
| 重写 `createWidget(parent)` | 同一个 action 要出现在多个容器中。 | 每个容器可能有独立 widget，状态同步由子类负责。 |
| `QToolBar::addWidget(widget)` | 只把控件放进一个工具栏。 | 不产生可复用的 action 语义，不能直接加入菜单。 |
| 普通布局 | 控件属于页面本身，而不是 action 序列。 | 不应为了放置普通页面控件而创建 QWidgetAction。 |

经验法则：单工具栏的小控件可以直接 `addWidget()`；需要被菜单、工具栏统一添加和移除，或需要在多个容器复用时，才使用 `QWidgetAction`。

## 7. 控件如何触发 action

`QWidgetAction` 不会自动知道控件什么时候代表“用户触发了动作”。例如 `QComboBox` 的当前文本变化，并不天然等价于 `QAction::triggered()`。

可以在控件信号中主动触发：

```cpp
connect(combo, &QComboBox::currentTextChanged,
        action, [action](const QString &value) {
            action->setData(value);
            action->trigger();
        });
```

常见职责分工是：

- widget 负责采集用户输入；
- action 的 `data()` 暂存本次选择值，或传递轻量参数；
- 业务对象负责保存长期状态；
- `triggered()` 或自定义信号通知业务执行操作。

如果控件表示的是持续状态，例如当前缩放比例、当前字体或当前颜色，不要只把值塞进 `QAction::data()` 后就结束。应该让业务对象持有真实状态，然后把状态同步回所有由 action 创建的 widget。

## 8. 多个 widget 的状态同步

一个继承自 `QWidgetAction` 的 action 可能创建多个 widget：

```text
ZoomAction
  ├─ 工具栏中的 QComboBox
  └─ 菜单中的 QComboBox
```

如果用户在工具栏中选择了 `125%`，菜单里的下拉框也应该更新到 `125%`。不要只修改触发信号的那个 widget。

可以在 action 中统一保存状态，并遍历 `createdWidgets()`：

```cpp
class ZoomAction final : public QWidgetAction
{
public:
    explicit ZoomAction(QObject *parent)
        : QWidgetAction(parent)
    {
    }

    void setZoom(int value)
    {
        m_zoom = value;

        for (QWidget *widget : createdWidgets()) {
            auto *box = qobject_cast<QComboBox *>(widget);
            if (!box)
                continue;

            QSignalBlocker blocker(box);
            box->setCurrentText(QString::number(m_zoom) + "%");
        }
    }

protected:
    QWidget *createWidget(QWidget *parent) override
    {
        auto *box = new QComboBox(parent);
        box->addItems({"50%", "75%", "100%", "125%", "150%"});
        box->setCurrentText(QString::number(m_zoom) + "%");

        connect(box, &QComboBox::currentTextChanged,
                this, [this](const QString &text) {
                    setZoom(text.chopped(1).toInt());
                    trigger();
                });
        return box;
    }

private:
    int m_zoom = 100;
};
```

`createdWidgets()` 返回的是由 `createWidget()` 创建、当前仍在管理中的 widget 列表；它不等同于默认 widget。这个函数是给 `QWidgetAction` 子类同步状态用的保护成员函数，业务代码通常不应把返回列表当作自己的容器保存。

同步状态时常用 `QSignalBlocker`，避免程序主动更新控件又触发一遍“用户修改”逻辑。

## 9. 在 QMenu 中使用的限制

`QWidgetAction` 可以加入 `QMenu`：

```cpp
auto *searchAction = new QWidgetAction(menu);
auto *searchEdit = new QLineEdit;
searchEdit->setPlaceholderText(QObject::tr("Search"));
searchAction->setDefaultWidget(searchEdit);
menu->addAction(searchAction);
```

但菜单不是普通面板：

- 菜单可能在点击后自动关闭；
- 控件获得键盘焦点的行为受平台和菜单实现影响；
- 菜单中的复杂输入可能打断用户的菜单导航；
- macOS 原生菜单栏对嵌入 widget 有更多限制；
- 同一个默认 widget 被不同菜单请求时，显示位置和父对象会发生变化。

菜单中适合放轻量的搜索框、简单选择器或短暂输入。复杂表单、长文本编辑和需要持续交互的控件，更适合放在 `QDialog`、`QDockWidget` 或普通页面中。

## 10. QWidgetAction 与 QAction 的关系

`QWidgetAction` 自己主要解决“如何提供 widget 表现”；命令文本、图标、启用状态、可见状态和触发信号仍然来自 `QAction`。

```cpp
auto *action = new QWidgetAction(this);
action->setText(tr("Zoom"));
action->setIcon(QIcon(":/icons/zoom.svg"));
action->setEnabled(false);
action->setData(100);

connect(action, &QAction::triggered, this, [this] {
    // 执行业务操作
});
```

`setEnabled(false)`、`setVisible(false)` 等 action 状态会影响容器中的 action 表现，但具体 widget 是否如何响应，还取决于容器和 widget 的实现。自定义 widget 时，必要时可以在 action 状态变化后同步 `setEnabled()` 或其他属性。

## API 速查表
### 11.1 构造、默认控件和生命周期

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `QWidgetAction(QObject *parent)` | 创建一个能提供 widget 表现的 action。 | `parent` 管理 action 生命周期；action 本身不是 widget。 |
| 生命周期 | `~QWidgetAction()` | 销毁 action 并清理其默认 widget、创建记录和相关连接。 | 不要在 action 销毁后访问它提供过的 widget。 |
| 默认控件 | `setDefaultWidget(QWidget *widget)` | 设置一个默认的 widget 表现。 | widget 的管理权交给 action；同一时刻只能被一个容器使用。 |
| 默认控件 | `defaultWidget()` | 返回当前设置的默认 widget。 | 没有设置时返回 `nullptr`；返回指针不代表可以绕过 action 协议随意 reparent。 |

### 11.2 容器请求、创建和释放

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 容器协议 | `requestWidget(QWidget *parent)` | 请求一个用于显示 action 的 widget。 | 主要由 `QToolBar`、`QMenu` 等容器调用；业务代码通常不直接调用。 |
| 容器协议 | `releaseWidget(QWidget *widget)` | 通知 action 某个容器不再使用该 widget。 | 主要由容器调用；默认 widget 通常被释放占用但保留，动态 widget 进入删除流程。 |
| 工厂扩展 | `createWidget(QWidget *parent)` | 为一个容器创建新的 widget 表现。 | 子类重写；应使用传入 parent；不提供控件时返回 `nullptr`。 |
| 删除扩展 | `deleteWidget(QWidget *widget)` | 回收 `createWidget()` 创建的 widget。 | 默认实现隐藏并 `deleteLater()`；只有需要自定义回收时才重写。 |
| 状态同步 | `createdWidgets()` | 返回当前由 `createWidget()` 创建且仍被管理的 widget 列表。 | 保护成员函数；不包含默认 widget，适合子类遍历同步状态。 |

### 11.3 事件扩展

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件处理 | `event(QEvent *event)` | 处理 action 自身收到的事件。 | 通常不需要重写；重写时应保留基类处理结果。 |
| 事件过滤 | `eventFilter(QObject *watched, QEvent *event)` | 过滤 action 相关对象的事件。 | 用于特殊的 widget 生命周期或交互联动；不要把普通业务逻辑都塞进事件过滤器。 |

### 11.4 常用 QAction 继承 API

这些函数不是 `QWidgetAction` 新增的，但决定了它在菜单、工具栏中的 action 语义：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 文本 | `setText(const QString &text)` / `text()` | 设置或读取 action 的名称。 | 菜单等容器可能仍使用它显示辅助文本或无 widget 时的默认表现。 |
| 图标 | `setIcon(const QIcon &icon)` / `icon()` | 设置或读取 action 图标。 | 自定义 widget 是否显示图标由 widget 自己决定。 |
| 状态 | `setEnabled(bool)` / `isEnabled()` | 启用或禁用 action。 | 容器和自定义 widget 对禁用状态的呈现可能不同，必要时主动同步 widget。 |
| 状态 | `setVisible(bool)` / `isVisible()` | 显示或隐藏 action。 | 影响 action 容器中的表现，不等于直接调用 widget 的 `hide()`。 |
| 参数 | `setData(const QVariant &value)` / `data()` | 保存或读取 action 携带的数据。 | 适合轻量参数；长期业务状态应放到业务对象。 |
| 触发 | `trigger()` | 主动触发 action。 | 控件变化不会自动触发，通常在 widget 信号槽中调用。 |
| 触发信号 | `triggered(bool checked = false)` | action 被触发时通知业务。 | `checked` 只对可选中 action 有意义；控件自身的值仍需单独读取或传递。 |
| 状态信号 | `changed()` | action 属性发生变化时通知。 | 适合重新同步自定义 widget 的通用属性。 |

## 12. 常见误区

### 12.1 把 QWidgetAction 当 QWidget 使用

`QWidgetAction` 继承自 `QAction`，不是 `QWidget`。它没有独立的 `show()` 用法，必须加入菜单、工具栏等 action 容器。

### 12.2 一个 defaultWidget 放进多个地方

默认 widget 是一个真实控件实例，不能同时拥有两个父控件。需要多处显示时，重写 `createWidget()`，为每个容器创建一份。

### 12.3 以为控件变化会自动触发 action

不会。`QComboBox`、`QLineEdit` 等控件的信号不会自动转成 `QAction::triggered()`。需要在槽函数中主动调用 `trigger()`，或者发出自定义业务信号。

### 12.4 只更新触发事件的那个 widget

如果一个 action 创建了多个 widget，只更新当前控件会让菜单、工具栏之间的显示状态不一致。应把状态放在 action 或业务对象中，再同步到 `createdWidgets()`。

### 12.5 把 createdWidgets() 当成永久控件列表

这个列表只代表当前仍由 action 管理的动态 widget。容器移除 action 后，widget 可能很快被释放，不能长期缓存其中的裸指针。

### 12.6 菜单里塞复杂表单

菜单可能自动关闭并受平台限制。复杂输入应放到 `QDialog`、`QDockWidget` 或普通页面，不要用 `QWidgetAction` 代替完整界面容器。

---

### 一句话总结

`QWidgetAction` 是“带 QWidget 表现的 QAction”：单处显示时用 `setDefaultWidget()`，多容器复用时重写 `createWidget()`，容器通过 `requestWidget()`/`releaseWidget()` 管理表现，`createdWidgets()` 用来同步动态控件，而控件何时触发 action 必须由代码明确调用 `trigger()`。
