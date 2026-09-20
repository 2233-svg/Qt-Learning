# Qt Widgets 进阶（上）：Widget 事件处理与输入分发

> 适用版本：Qt 6.11.1  
> 核心类型：`QEvent`、`QWidget`、`QMouseEvent`、`QKeyEvent`、`QWheelEvent`、`QFocusEvent`、`QShortcut`、`QContextMenuEvent`

Qt Core 事件篇解释了事件循环和通用事件机制。本篇专门回答 Widgets 开发中的实际问题：事件到达哪个控件、在哪一层拦截、什么时候接受或忽略，以及如何让鼠标、键盘、焦点、快捷键和输入法协同工作。

## 1. Widget 收到事件时发生了什么

简化流程如下：

```text
操作系统/Qt 内部产生输入或状态变化
                ↓
          QApplication::notify()
                ↓
       目标对象上的事件过滤器
                ↓
          QWidget::event()
                ↓
      mousePressEvent() 等专用处理器
                ↓
      事件被接受、忽略或继续传播
```

对大多数自定义控件，直接重写最具体的处理器即可：

```cpp
void MyWidget::mousePressEvent(QMouseEvent *event)
{
    // 处理鼠标按下
}
```

只有需要统一处理多种类型、截获 Tab、处理自定义类型时，才重写 `event()`；只有需要观察别的对象时，才安装事件过滤器。

## 2. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. 最小可用代码：可点击的自定义区域

```cpp
#include <QApplication>
#include <QMouseEvent>
#include <QPainter>
#include <QWidget>

class ClickArea : public QWidget
{
public:
    using QWidget::QWidget;

protected:
    void mousePressEvent(QMouseEvent *event) override
    {
        if (event->button() == Qt::LeftButton) {
            m_pressed = true;
            update();
            event->accept();
            return;
        }
        QWidget::mousePressEvent(event);
    }

    void mouseReleaseEvent(QMouseEvent *event) override
    {
        if (event->button() == Qt::LeftButton) {
            m_pressed = false;
            update();
            event->accept();
            return;
        }
        QWidget::mouseReleaseEvent(event);
    }

    void paintEvent(QPaintEvent *) override
    {
        QPainter painter(this);
        painter.fillRect(rect(), m_pressed ? QColor("#b8d9ff")
                                           : QColor("#e8eef5"));
        painter.drawText(rect(), Qt::AlignCenter,
                         m_pressed ? QStringLiteral("按下")
                                   : QStringLiteral("点击这里"));
    }

private:
    bool m_pressed = false;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    ClickArea area;
    area.resize(320, 160);
    area.show();
    return app.exec();
}
```

示例只处理左键。其他按键转交 `QWidget` 默认实现，使未处理行为仍有传播机会。

## 4. 选哪一层处理事件

| 需求 | 最合适的入口 |
|---|---|
| 当前控件处理鼠标按下 | `mousePressEvent()` |
| 当前控件处理按键 | `keyPressEvent()` |
| 当前控件处理绘制 | `paintEvent()` |
| 当前控件统一判断多个事件类型 | `event()` |
| 观察或拦截另一个 QObject | `eventFilter()` |
| 全应用级输入策略 | QApplication 级过滤器，谨慎使用 |
| 操作系统原生消息 | `nativeEvent()`，最后手段 |

越靠上层，影响范围越大，也越容易破坏 Qt 默认行为。能在具体控件的专用处理器解决，就不要上升到全局过滤器。

## 5. `event()` 与专用处理器

`QWidget::event()` 会识别事件类型，再分发给 `mousePressEvent()`、`keyPressEvent()` 等专用虚函数。

例如让自定义编辑器自己接收 Tab：

```cpp
bool CodeEditor::event(QEvent *event)
{
    if (event->type() == QEvent::KeyPress) {
        auto *keyEvent = static_cast<QKeyEvent *>(event);
        if (keyEvent->key() == Qt::Key_Tab) {
            insertPlainText(QStringLiteral("    "));
            return true;
        }
    }
    return QPlainTextEdit::event(event);
}
```

返回 `true` 表示事件已经处理；未处理的类型必须交给基类。若简单地在末尾返回 `true`，焦点、快捷键、样式和输入法事件都可能被吞掉。

### 5.1 `return true` 与 `event->accept()` 不是完全同一件事

- `event()` / `eventFilter()` 的布尔返回值控制这一层是否停止继续处理。
- `QEvent::accept()` / `ignore()` 修改事件接受状态，某些事件用它决定是否传播给父 Widget或是否执行默认操作。

二者经常配合，但语义层次不同。阅读具体事件类文档，不能假设所有事件都以同一种方式传播。

## 6. 事件过滤器

事件过滤器适合不修改目标类就观察其事件，例如对一个 `QLineEdit` 拦截 Enter：

```cpp
class EnterFilter : public QObject
{
public:
    using QObject::QObject;

protected:
    bool eventFilter(QObject *watched, QEvent *event) override
    {
        if (event->type() == QEvent::KeyPress) {
            auto *key = static_cast<QKeyEvent *>(event);
            if (key->key() == Qt::Key_Return
                || key->key() == Qt::Key_Enter) {
                qDebug() << "提交" << watched;
                return true; // 拦截，不再交给 watched
            }
        }
        return QObject::eventFilter(watched, event);
    }
};

auto *filter = new EnterFilter(&window);
lineEdit->installEventFilter(filter);
```

### 6.1 生命周期

`installEventFilter()` 不表示 watched 拥有 filter。示例把 filter 的 parent 设为 window，确保它不会先成为悬空指针。

Qt 会在过滤器销毁时自动解除相关过滤关系，但清晰的父子所有权仍更易维护。

### 6.2 线程限制

被观察对象与过滤器必须在同一线程，否则过滤器不会正常工作。两者后来移动到不同线程时，过滤调用也会暂停，直到再次处于同一线程。

### 6.3 删除被观察对象

如果过滤器在处理事件时删除了 `watched`，必须返回 `true`，避免 Qt 随后把同一个事件发送给已删除对象。更常见、更安全的是调用 `deleteLater()`，并明确终止当前事件路径。

### 6.4 过滤器顺序

后安装的过滤器先执行。多个过滤器相互依赖会让行为难以推理，尽量把同一输入策略集中到一个明确组件。

## 7. 鼠标事件

### 7.1 `button()` 与 `buttons()`

```cpp
void Canvas::mouseMoveEvent(QMouseEvent *event)
{
    if (event->buttons() & Qt::LeftButton)
        drawTo(event->position());
}
```

- `button()`：触发当前 press/release 的那个按键；MouseMove 中通常是 `NoButton`。
- `buttons()`：事件发生时所有仍按住的按键集合。

因此拖动判断用 `buttons()`，点击触发判断用 `button()`。

### 7.2 坐标系

Qt 6 鼠标事件常用浮点坐标：

| API | 坐标系 |
|---|---|
| `position()` | 接收 Widget 的局部坐标 |
| `scenePosition()` | 图形场景相关坐标，视事件类型而定 |
| `globalPosition()` | 屏幕全局坐标 |

菜单通常需要全局坐标，控件内部命中测试用局部坐标：

```cpp
if (buttonRect.contains(event->position().toPoint()))
    activate();
```

不要把 `globalPosition()` 直接与 `rect()` 比较。需要转换时使用 `mapToGlobal()` / `mapFromGlobal()`。

### 7.3 鼠标移动与 tracking

默认情况下，只有按着鼠标按钮移动才收到 `mouseMoveEvent()`。要在悬停时持续跟踪：

```cpp
setMouseTracking(true);
```

若只需要进入/离开状态，优先实现 `enterEvent()` / `leaveEvent()`，避免处理高频 MouseMove。

### 7.4 按下后的隐式抓取

Widget 收到鼠标按下后，通常会继续收到对应的移动和释放，即使光标已经移出控件。这让拖动实现更自然。

```cpp
void SliderLike::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        m_dragging = true;
        setValueFromPosition(event->position().x());
        event->accept();
    }
}

void SliderLike::mouseReleaseEvent(QMouseEvent *event)
{
    if (m_dragging && event->button() == Qt::LeftButton) {
        m_dragging = false;
        event->accept();
    }
}
```

除特殊交互外，不要长期显式 `grabMouse()`；若忘记 `releaseMouse()`，整个应用的鼠标输入都可能异常。

### 7.5 双击不是独立于单击的第一事件

双击序列包含按下、释放、第二次按下、双击、第二次释放。第一下发生时无法提前知道用户会不会再点一次。因此双击最好是单击动作的自然扩展，而不是与单击完全冲突的操作。

## 8. 键盘、焦点与快捷键

### 8.1 先让控件获得焦点

```cpp
setFocusPolicy(Qt::StrongFocus);
```

常见策略：

| FocusPolicy | 含义 |
|---|---|
| `NoFocus` | 不通过键盘焦点交互 |
| `TabFocus` | 可通过 Tab 获得焦点 |
| `ClickFocus` | 可通过点击获得焦点 |
| `StrongFocus` | Tab 和点击均可 |
| `WheelFocus` | StrongFocus 外加滚轮焦点语义 |

一个可键盘操作的自定义控件应在 `paintEvent()` 中清楚显示焦点状态，并实现合理的方向键、Enter/Space 行为。

### 8.2 按键与文本不是一回事

```cpp
void Editor::keyPressEvent(QKeyEvent *event)
{
    if (event->matches(QKeySequence::Copy)) {
        copySelection();
        event->accept();
        return;
    }

    if (!event->text().isEmpty())
        insertText(event->text());
    else
        QWidget::keyPressEvent(event);
}
```

- `key()` 表示物理/逻辑键，如 `Qt::Key_Left`。
- `text()` 表示考虑键盘布局和修饰键后的文本。
- `modifiers()` 表示 Ctrl、Shift、Alt 等状态。
- `matches()` 能按平台标准快捷键匹配 Copy、Paste 等操作。

不要用 `key()` 手工拼出所有字符，国际键盘布局和输入法会使这种实现失效。

### 8.3 自动重复

按住按键会连续产生事件：

```cpp
if (event->isAutoRepeat()) {
    // 需要时忽略重复触发
}
```

移动光标可以接受自动重复，触发“删除项目”或“打开窗口”等动作则通常要评估是否应该忽略。

### 8.4 用 QAction/QShortcut 表达命令

对于应用命令，优先使用 `QAction` 或 `QShortcut`，而不是在每个 Widget 的 `keyPressEvent()` 里重复判断：

```cpp
auto *saveAction = new QAction(QStringLiteral("保存"), &window);
saveAction->setShortcut(QKeySequence::Save);
window.addAction(saveAction);

QObject::connect(saveAction, &QAction::triggered,
                 &controller, &Controller::save);
```

这样命令可同时出现在菜单、工具栏和快捷键中，并统一 enabled/checked 状态。

### 8.5 `ShortcutOverride`

当某控件需要优先接管一个可能触发快捷键的按键时，可在 `event()` 中接受 `QEvent::ShortcutOverride`：

```cpp
if (event->type() == QEvent::ShortcutOverride) {
    auto *key = static_cast<QKeyEvent *>(event);
    if (key->matches(QKeySequence::Copy)) {
        event->accept();
        return true;
    }
}
```

接受后，快捷键不会抢走它，按键会作为普通 KeyPress 送到焦点控件。不要全局接受所有 ShortcutOverride，这会让应用快捷键失效。

## 9. 焦点事件

```cpp
void CustomControl::focusInEvent(QFocusEvent *event)
{
    QWidget::focusInEvent(event);
    update();
}

void CustomControl::focusOutEvent(QFocusEvent *event)
{
    QWidget::focusOutEvent(event);
    update();
}
```

`QFocusEvent::reason()` 可以区分 Tab、鼠标、窗口激活等来源，但业务逻辑不要过度依赖它，因为平台交互可能不同。

### 9.1 current、focus 和 selection 不相同

在 Item View 中：

- 键盘焦点属于 View Widget；
- current index 由 SelectionModel 表示当前项；
- selected indexes 是选区。

不要用 `hasFocus()` 判断某个 Item 是否被选择。

### 9.2 焦点代理

复合控件本身不编辑，内部 `QLineEdit` 才编辑时：

```cpp
setFocusProxy(lineEdit);
setFocusPolicy(lineEdit->focusPolicy());
```

外部对复合控件设置焦点时会转给内部编辑器，Tab 导航也更自然。

## 10. 滚轮和高分辨率触控板

```cpp
void ZoomView::wheelEvent(QWheelEvent *event)
{
    if (event->modifiers() & Qt::ControlModifier) {
        const QPoint delta = event->angleDelta();
        if (!delta.isNull())
            zoomBy(delta.y() / 120.0);
        event->accept();
        return;
    }
    QWidget::wheelEvent(event);
}
```

- `angleDelta()` 以八分之一度为单位，传统滚轮常见一步 120，但不要假设永远如此。
- `pixelDelta()` 在支持的高分辨率触控设备上给出像素滚动量，可能为空。
- 未处理的滚轮应交给基类或忽略，让父级滚动区域有机会响应。

平滑滚动应累积小 delta，而不是每次事件都强制跳固定一行。

## 11. Context Menu

推荐重写 `contextMenuEvent()`，它同时适配鼠标右键和键盘菜单键：

```cpp
void Editor::contextMenuEvent(QContextMenuEvent *event)
{
    QMenu menu(this);
    menu.addAction(m_copyAction);
    menu.addAction(m_pasteAction);
    menu.exec(event->globalPos());
}
```

如果只是外部拼装菜单，可使用：

```cpp
widget->setContextMenuPolicy(Qt::CustomContextMenu);
QObject::connect(widget, &QWidget::customContextMenuRequested,
                 &window, [widget](const QPoint &pos) {
    QMenu menu(widget);
    menu.addAction(QStringLiteral("刷新"));
    menu.exec(widget->mapToGlobal(pos));
});
```

`customContextMenuRequested` 的位置通常是 Widget 局部坐标，`QMenu::exec()` 需要全局坐标。

## 12. 关闭、显示、隐藏和尺寸变化

### 12.1 关闭确认

```cpp
void EditorWindow::closeEvent(QCloseEvent *event)
{
    if (!m_modified) {
        event->accept();
        return;
    }

    const auto answer = QMessageBox::question(
        this, QStringLiteral("未保存"),
        QStringLiteral("放弃未保存的修改吗？"));

    if (answer == QMessageBox::Yes)
        event->accept();
    else
        event->ignore();
}
```

`close()` 请求关闭，不一定销毁。是否删除取决于对象所有权和 `Qt::WA_DeleteOnClose` 等设置。不要把 close、hide 和 delete 混为一谈。

### 12.2 resizeEvent 不应替代布局

```cpp
void Preview::resizeEvent(QResizeEvent *event)
{
    QWidget::resizeEvent(event);
    rebuildCachedBackground(event->size());
}
```

resizeEvent 适合更新尺寸相关缓存，不适合手工排列常规子控件。子控件几何应优先交给 Layout。

### 12.3 showEvent 不等于首次构造

Widget 可反复 show/hide，因此 `showEvent()` 可能多次调用。只执行一次的昂贵初始化应有显式状态，或者在更明确的生命周期节点完成。

## 13. 状态变化事件 `changeEvent()`

字体、调色板、语言、Style、enabled 状态变化会到达控件：

```cpp
void CustomControl::changeEvent(QEvent *event)
{
    QWidget::changeEvent(event);

    switch (event->type()) {
    case QEvent::FontChange:
    case QEvent::StyleChange:
    case QEvent::PaletteChange:
        updateGeometry();
        update();
        break;
    case QEvent::LanguageChange:
        updateTranslatedText();
        break;
    default:
        break;
    }
}
```

自定义控件若缓存了字体度量、颜色或文本尺寸，应在相应变化后失效缓存。只在构造函数读取一次 Style 会导致运行时换主题后显示错误。

## 14. 输入法不是普通键盘事件

中文、日文等输入法有“预编辑文本”和“提交文本”。真正的文本编辑控件需支持：

- `inputMethodEvent()`：接收预编辑和提交；
- `inputMethodQuery()`：告诉输入法光标矩形、当前文本和选择；
- `Qt::WA_InputMethodEnabled`：启用输入法；
- 正确绘制组合中的预编辑文本。

轮廓：

```cpp
void TextControl::inputMethodEvent(QInputMethodEvent *event)
{
    replaceSelection(event->commitString());
    m_preedit = event->preeditString();
    update();
    event->accept();
}

QVariant TextControl::inputMethodQuery(Qt::InputMethodQuery query) const
{
    if (query == Qt::ImCursorRectangle)
        return cursorRect();
    if (query == Qt::ImSurroundingText)
        return m_text;
    if (query == Qt::ImCursorPosition)
        return m_cursorPosition;
    return QWidget::inputMethodQuery(query);
}
```

手写完整文本编辑器远比处理 `keyPressEvent()` 复杂。没有特殊需求时优先复用 `QLineEdit`、`QTextEdit` 或 `QPlainTextEdit`。

## 15. 自定义事件与 queued 调用

### 15.1 注册和发送自定义事件

```cpp
class ResultEvent : public QEvent
{
public:
    static QEvent::Type typeId()
    {
        static const int type = QEvent::registerEventType();
        return static_cast<QEvent::Type>(type);
    }

    explicit ResultEvent(QString text)
        : QEvent(typeId()), result(std::move(text)) {}

    QString result;
};

QCoreApplication::postEvent(receiver,
    new ResultEvent(QStringLiteral("完成")));
```

接收：

```cpp
void Receiver::customEvent(QEvent *event)
{
    if (event->type() == ResultEvent::typeId()) {
        auto *result = static_cast<ResultEvent *>(event);
        applyResult(result->result);
        return;
    }
    QObject::customEvent(event);
}
```

`postEvent()` 接管堆上事件的所有权并异步投递；`sendEvent()` 同步调用且不接管所有权。

多数跨组件业务通信更适合信号与槽。自定义事件适合接入事件优先级、统一 event 分派或已有事件驱动框架。

## 16. `update()`、`repaint()` 和事件合并

状态变化后通常调用：

```cpp
update();
```

它安排未来的 Paint 事件，Qt 可以合并多个更新区域。`repaint()` 倾向于立即同步重绘，频繁调用会阻塞事件处理并可能造成递归绘制，除非有明确理由，一般不用。

高频输入中应只更新受影响区域：

```cpp
update(oldHandleRect.united(newHandleRect));
```

## 17. 原生事件是最后手段

`nativeEvent()` 暴露平台消息，代码会直接依赖 Windows、X11、Wayland 或 macOS 细节。使用前先确认：

1. Qt 是否已有跨平台事件或属性；
2. `QWindow` / `QNativeInterface` 是否提供更窄的接口；
3. 平台分支是否隔离在小模块中；
4. Qt 和操作系统升级后如何测试。

普通鼠标、键盘、窗口状态和拖放不应通过原生消息实现。

## 18. 常见错误

### 18.1 所有事件都 return true

结果：默认焦点、快捷键、输入法、拖放或绘制行为失效。只吞掉真正处理完的类型。

### 18.2 忘记调用基类处理器

重写函数只处理一个分支时，其余分支要转给基类。对于 `paintEvent()` 之类完全自绘的函数是否调用基类取决于控件设计，但必须是有意识的决定。

### 18.3 在 MouseMove 中用 `button()` 判断拖动

MouseMove 的 `button()` 通常是 `NoButton`；应检查 `buttons()` 位集合。

### 18.4 混用局部和全局坐标

典型表现是菜单出现在错误屏幕位置、命中区域随窗口移动而漂移。先写清每个点属于哪个坐标系。

### 18.5 在事件处理器中执行耗时任务

事件循环被阻塞后，界面无法重绘和响应输入。把耗时工作放到线程/异步任务中，完成后排队回 GUI 线程更新状态。

### 18.6 用过滤器实现本类自身的所有行为

会隐藏控件的职责并增加生命周期复杂度。自己类的标准输入优先重写专用 handler。

### 18.7 把 `ignore()` 理解成“什么都不做”

某些事件被 ignore 后会传播到父 Widget 或触发其他默认处理。接受状态具有事件类型相关语义，要查对应类文档。

## 19. 调试方法

临时过滤器可以打印类型和目标：

```cpp
bool EventLogger::eventFilter(QObject *watched, QEvent *event)
{
    qDebug() << watched << event->type() << event->isAccepted();
    return QObject::eventFilter(watched, event);
}
```

调试建议：

- 打印 `objectName()`、事件类型、接受状态和坐标；
- 检查目标对象是否 enabled、visible、是否被透明层遮挡；
- 检查 focus policy 和当前 `QApplication::focusWidget()`；
- 检查父子控件谁先接到事件；
- 检查是否存在后安装的过滤器提前返回 true；
- 高频事件只短期记录，否则日志本身会严重影响时序。

## 20. API 速查

| API | 用途 |
|---|---|
| `QWidget::event()` | Widget 事件统一入口 |
| `eventFilter()` | 观察/拦截其他 QObject 的事件 |
| `accept()` / `ignore()` | 修改事件接受状态 |
| `QMouseEvent::button()` | 当前发生变化的按键 |
| `QMouseEvent::buttons()` | 当前所有按住的按键 |
| `position()` | Widget 局部浮点坐标 |
| `globalPosition()` | 屏幕全局浮点坐标 |
| `setMouseTracking()` | 无按键时也接收 MouseMove |
| `setFocusPolicy()` | 声明获得键盘焦点的方式 |
| `QKeyEvent::matches()` | 匹配平台标准快捷键 |
| `QShortcut` / `QAction` | 表达可复用命令快捷键 |
| `contextMenuEvent()` | 鼠标和键盘一致的上下文菜单入口 |
| `changeEvent()` | 响应字体、Style、语言等变化 |
| `inputMethodEvent()` | 处理输入法预编辑和提交 |
| `postEvent()` | 异步投递并转移事件所有权 |
| `update()` | 安排可合并的未来重绘 |

## 21. 自测题

1. 当前 Widget 只需要处理鼠标按下时，应该优先重写哪个函数？
2. `eventFilter()` 返回 `true` 表示什么？
3. 为什么 `event()` 对未处理类型要调用基类实现？
4. 拖动时应该检查 `button()` 还是 `buttons()`？
5. `position()` 和 `globalPosition()` 的坐标系有何区别？
6. 为什么自定义可操作控件需要 focus policy？
7. `key()` 和 `text()` 分别表示什么？
8. 为什么上下文菜单最好使用 `contextMenuEvent()`？
9. `postEvent()` 对事件对象的所有权如何处理？
10. 状态变化后为什么通常用 `update()` 而不是 `repaint()`？

## 22. 参考答案

1. `mousePressEvent()`，它比 `event()` 和全局过滤器更具体。
2. 过滤器已经处理事件，停止把它继续发送给被观察对象。
3. 基类负责焦点、Tab、快捷键、输入法以及分派到各专用处理器；吞掉未知类型会破坏默认行为。
4. `buttons()`，因为 MouseMove 中 `button()` 通常是 `NoButton`。
5. `position()` 相对接收 Widget；`globalPosition()` 相对屏幕。
6. 没有合适的策略，控件无法通过 Tab/点击获得键盘焦点，也就不能可靠接收键盘事件。
7. `key()` 是键枚举，`text()` 是考虑布局和修饰键后的文本输入。
8. 它同时覆盖鼠标和键盘发起的上下文菜单请求，并提供正确的位置语义。
9. `postEvent()` 接管用 `new` 创建的事件，投递后负责销毁。
10. `update()` 可让 Qt 合并重绘并保持事件循环流畅；同步 `repaint()` 容易造成阻塞和重复绘制。

## 23. 本篇结论

Widget 事件处理最可靠的策略是“在最具体、最局部的层级处理”：

```text
自己的标准输入 → 专用 event handler
自己的特殊事件 → event()
观察别的对象   → eventFilter()
应用级策略     → 全局过滤器（谨慎）
平台消息       → nativeEvent()（最后手段）
```

只消费已经完整处理的事件，其他路径交回基类；始终区分处理函数返回值、事件接受状态和父子传播，并明确坐标系、焦点与输入法语义。下一篇将在这些事件基础上构建真正可复用的自定义 Widget。
