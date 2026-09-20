# Qt Widgets 基础（上）：QWidget 与窗口基础

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Widgets  
> 核心类型：`QApplication`、`QWidget`、`QSizePolicy`、`QPalette`  
> 本篇目标：理解控件树、顶层窗口、几何坐标、显示状态、焦点、尺寸协商以及 QWidget 的生命周期。

## 1. QWidget 是什么

`QWidget` 是 Qt Widgets 界面的基本单元。按钮、输入框、标签、窗口等最终都继承自它。

每个 Widget：

- 占据一个矩形区域；
- 可以接收鼠标、键盘、触摸和窗口系统事件；
- 可以绘制自身；
- 可以作为其他 Widget 的父对象；
- 在兄弟控件之间拥有 Z 顺序；
- 会被父控件边界和上层兄弟控件裁剪。

```text
QObject
  └─ QWidget
      ├─ QLabel
      ├─ QPushButton
      ├─ QLineEdit
      ├─ QDialog
      └─ QMainWindow
```

## 2. QApplication：Widgets 应用入口

任何 QWidget 创建之前，都必须先创建一个 `QApplication`：

```cpp
int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    window.show();

    return app.exec();
}
```

`QApplication` 在 `QGuiApplication` 基础上增加了 Widgets 所需的样式、字体、调色板、双击间隔等管理。

一个进程通常只能有一个应用对象，并且它必须活到所有 Widget 销毁之后。

## 3. 最小可用代码

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 3.2 一个带子控件的窗口

```cpp
#include <QApplication>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    window.setWindowTitle("QWidget 基础");

    auto *layout = new QVBoxLayout(&window);
    layout->addWidget(new QLabel("这是一个子控件"));

    auto *button = new QPushButton("关闭");
    layout->addWidget(button);

    QObject::connect(button, &QPushButton::clicked,
                     &window, &QWidget::close);

    window.resize(360, 180);
    window.show();
    return app.exec();
}
```

布局和控件均由 `window` 的对象树接管，不需要逐个 `delete`。

## 4. 顶层窗口与子控件

构造函数的 parent 决定 Widget 的基本身份：

```cpp
QWidget *window = new QWidget;          // parent == nullptr，顶层窗口
QPushButton *button = new QPushButton(window); // 子控件
```

- 没有父 Widget：通常成为独立顶层窗口；
- 有父 Widget：嵌入父控件的客户区；
- 有父对象但显式带 `Qt::Window`：仍可成为窗口。

查询：

```cpp
widget->isWindow();
widget->window();       // 所属顶层窗口
widget->parentWidget();
```

### 4.1 父子关系同时解决什么

Widget 父子关系至少影响：

1. 所有权：父控件析构时删除子控件；
2. 坐标：子控件位置相对父控件；
3. 裁剪：子控件不能绘制到父控件可见区域之外；
4. 显隐：父控件隐藏时子控件随之不可见；
5. 启用状态：父控件禁用时子控件不可交互；
6. 样式和字体等属性继承；
7. 事件传播和焦点范围。

### 4.2 构造过程中设置 parent

优先在构造函数中传 parent：

```cpp
auto *label = new QLabel("状态", panel);
```

稍后 `setParent()` 会改变对象树；对 Widget 还可能改变窗口身份、坐标和可见性。重设父对象后通常需要重新 `show()`，不要把它仅理解为所有权修改。

## 5. 对象树与内存管理

以下代码无需手动删除按钮：

```cpp
auto *button = new QPushButton("确定", &window);
```

父对象销毁时会删除子对象。即使 child 比 parent 更早手动删除，它也会先从父对象的 children 列表移除，不会被父对象再次删除。

### 5.1 栈对象的构造顺序陷阱

安全：

```cpp
QWidget window;
QPushButton button("确定", &window);
```

C++ 逆序析构，button 先析构并脱离父对象，然后 window 析构。

危险写法：

```cpp
QPushButton button;
QWidget window;
button.setParent(&window);
```

window 先析构时会尝试删除作为栈对象的 button，之后作用域又会再次析构 button。栈 Widget 的父子关系必须匹配构造和析构顺序。实际界面通常让窗口在栈上、子控件在堆上，由对象树管理。

### 5.2 QPointer 观察对象寿命

```cpp
QPointer<QWidget> guard = dialog;
dialog->deleteLater();

// 延迟回调中
if (guard)
    guard->show();
```

QObject 删除后 `QPointer` 自动变空，适合观察异步回调中的 UI 对象，但它不延长对象寿命。

## 6. 三套常用矩形

理解 QWidget 几何必须区分：

| 属性                | 坐标系      | 是否含窗口边框    |
| ----------------- | -------- | ---------- |
| `rect()`          | 控件自身局部坐标 | 不含         |
| `geometry()`      | 相对父控件    | 顶层窗口不含系统边框 |
| `frameGeometry()` | 顶层窗口相对屏幕 | 包含系统边框     |

```cpp
QRect local = widget->rect();
QRect inParent = widget->geometry();
QRect withFrame = widget->frameGeometry();
```

`rect()` 通常从 `(0, 0)` 开始，适合绘制和局部命中测试。

### 6.1 pos、size、move、resize

```cpp
widget->move(20, 30);
widget->resize(320, 180);

QPoint position = widget->pos();
QSize size = widget->size();
```

组合设置：

```cpp
widget->setGeometry(20, 30, 320, 180);
```

使用布局的子控件不应频繁手动 `move()` 或 `resize()`，下一次布局激活时会覆盖它们。

## 7. 坐标转换

```cpp
QPoint global = child->mapToGlobal(QPoint(0, 0));
QPoint local = child->mapFromGlobal(global);

QPoint inOther = child->mapTo(otherWidget, point);
QPoint fromParent = child->mapFromParent(point);
```

Qt 6 还为多种映射提供 `QPointF` 重载，连续缩放和高 DPI 场景应尽量保留浮点精度。

不要通过手动累加多层 `pos()` 模拟转换，窗口边框、嵌套和变换会让这种计算脆弱。

## 8. 窗口首次显示时的几何

顶层窗口边框由窗口管理器创建。窗口显示前，边框宽度和最终位置可能尚不准确。

因此：

- 内容尺寸使用 `size()` / `geometry()`；
- 屏幕边框范围使用 `frameGeometry()`；
- 不依赖构造函数中尚未完成的原生窗口几何；
- 保存恢复窗口位置使用 `saveGeometry()` / `restoreGeometry()`，不要只保存四个整数。

## 9. 最小、最大和固定尺寸

```cpp
widget->setMinimumSize(240, 120);
widget->setMaximumSize(1200, 800);
```

固定尺寸：

```cpp
widget->setFixedSize(320, 200);
```

固定尺寸会削弱响应式布局和本地化适应能力。只有画布、固定规格预览等确有格式要求时使用。

## 10. sizeHint 与 minimumSizeHint

自定义控件可告诉布局“理想尺寸”和“合理最小尺寸”：

```cpp
QSize ColorPreview::sizeHint() const
{
    return QSize(240, 160);
}

QSize ColorPreview::minimumSizeHint() const
{
    return QSize(80, 60);
}
```

它们是建议，不是强制限制。布局会结合尺寸策略、最小最大尺寸和可用空间做决定。

当影响尺寸建议的数据变化时：

```cpp
text_ = text;
updateGeometry(); // 通知布局重新协商尺寸
update();         // 通知内容重绘
```

二者职责不同：`updateGeometry()` 面向布局，`update()` 面向绘制。

## 11. QSizePolicy：控件愿意怎样伸缩

```cpp
widget->setSizePolicy(QSizePolicy::Expanding,
                      QSizePolicy::Preferred);
```

常见 Policy：

| Policy             | 含义                  |
| ------------------ | ------------------- |
| `Fixed`            | 使用 sizeHint，不愿伸缩    |
| `Minimum`          | sizeHint 是最小值，可以变大  |
| `Maximum`          | sizeHint 是最大值，可以变小  |
| `Preferred`        | sizeHint 最佳，可变大或变小  |
| `Expanding`        | 可变大，并希望获得额外空间       |
| `MinimumExpanding` | 不能小于 sizeHint，也希望扩展 |
| `Ignored`          | 布局可忽略 sizeHint      |

Policy 是意愿，stretch 是同类控件之间分配额外空间的权重。两者不要混为一谈。

### 11.1 高度依赖宽度

自动换行标签等控件可能 `hasHeightForWidth()` 为真。自定义控件可重写 `heightForWidth()`，但计算应快速且结果稳定，否则布局反复试算会很昂贵。

## 12. 显示、隐藏与实际可见

```cpp
widget->show();
widget->hide();
widget->setVisible(condition);
```

需要区分：

- `isHidden()`：该对象是否被显式隐藏；
- `isVisible()`：相对其祖先是否可见；
- `isVisibleTo(ancestor)`：相对指定祖先是否可见。

子控件即使没有显式 hide，只要父窗口隐藏，它就不在屏幕上可见。

### 12.1 show 的窗口状态变体

```cpp
window->showNormal();
window->showMinimized();
window->showMaximized();
window->showFullScreen();
```

全屏、最大化和激活行为受操作系统窗口管理器约束，不能假定各平台完全一致。

## 13. enabled 与 visible 不同

```cpp
button->setEnabled(false);
```

禁用控件仍然可见，但不接受普通用户交互，样式通常显示为 Disabled 状态。父控件禁用时子控件也被有效禁用。

用禁用表达“当前不可操作”，用隐藏表达“当前不应出现”。不要用隐藏代替权限或数据校验，因为隐藏控件并不是安全边界。

## 14. 焦点策略

```cpp
widget->setFocusPolicy(Qt::StrongFocus);
widget->setFocus(Qt::OtherFocusReason);
```

常见策略：

| 策略            | 含义                  |
| ------------- | ------------------- |
| `NoFocus`     | 不接受键盘焦点             |
| `TabFocus`    | 通过 Tab 获得焦点         |
| `ClickFocus`  | 鼠标点击获得焦点            |
| `StrongFocus` | Tab 和点击均可           |
| `WheelFocus`  | StrongFocus 加滚轮获得焦点 |

处理键盘事件前先确认控件能获得焦点。

### 14.1 Tab 顺序

默认顺序通常跟控件创建/布局顺序相关。可显式设置：

```cpp
QWidget::setTabOrder(nameEdit, passwordEdit);
QWidget::setTabOrder(passwordEdit, loginButton);
```

顺序应符合视觉和业务阅读流程，并在界面动态变化后重新检查。

### 14.2 焦点代理

复合控件可把焦点转给内部编辑器：

```cpp
setFocusProxy(lineEdit_);
```

点击外壳或通过 Tab 到达复合控件时，真正输入焦点落到代理控件。

## 15. 窗口标志 WindowFlags

窗口标志由一个主要类型和若干提示组合：

```cpp
setWindowFlags(Qt::Tool |
               Qt::FramelessWindowHint |
               Qt::WindowStaysOnTopHint);
```

常见类型：

- `Qt::Window`：普通窗口；
- `Qt::Dialog`：对话框；
- `Qt::Tool`：工具窗口；
- `Qt::Popup`：弹出窗口，通常点击外部关闭；
- `Qt::ToolTip`：提示窗口。

常见提示：

- `WindowTitleHint`；
- `WindowSystemMenuHint`；
- `WindowMinimizeButtonHint`；
- `WindowMaximizeButtonHint`；
- `WindowCloseButtonHint`；
- `FramelessWindowHint`；
- `WindowStaysOnTopHint`。

窗口管理器可以忽略某些提示。运行中更改 flags 可能使窗口被重新创建并隐藏，之后需要再次 `show()`。

## 16. WidgetAttribute：精细行为开关

```cpp
widget->setAttribute(Qt::WA_DeleteOnClose);
widget->setAttribute(Qt::WA_TranslucentBackground);
widget->setAttribute(Qt::WA_AcceptTouchEvents);
```

常见属性：

| 属性                         | 用途             |
| -------------------------- | -------------- |
| `WA_DeleteOnClose`         | close 成功后删除对象  |
| `WA_TranslucentBackground` | 顶层窗口透明背景       |
| `WA_OpaquePaintEvent`      | 控件每次会绘满自身，帮助优化 |
| `WA_NoSystemBackground`    | 不由系统自动擦除背景     |
| `WA_AcceptTouchEvents`     | 接收触摸事件         |
| `WA_QuitOnClose`           | 关闭该顶层窗口可参与退出判断 |

属性往往包含平台约束。透明无边框窗口还需要自己处理拖动、缩放、阴影和可访问性，不能只设置两个标志就认为功能完整。

## 17. show、hide、close、delete 的区别

| 操作              | 对象还存在吗 | 含义           |
| --------------- | ------ | ------------ |
| `show()`        | 是      | 请求显示         |
| `hide()`        | 是      | 隐藏但不关闭       |
| `close()`       | 通常是    | 发送关闭事件，接受后隐藏 |
| `deleteLater()` | 稍后否    | 回到事件循环后删除    |
| `delete`        | 立即否    | 同步销毁，须保证调用安全 |

默认情况下 `close()` 并不删除 Widget。设置 `WA_DeleteOnClose` 后才会在关闭成功后删除。

## 18. closeEvent：允许用户取消关闭

```cpp
void EditorWindow::closeEvent(QCloseEvent *event)
{
    if (!documentModified_) {
        event->accept();
        return;
    }

    const auto answer = QMessageBox::question(
        this, tr("未保存"), tr("放弃未保存的修改吗？"));

    if (answer == QMessageBox::Yes)
        event->accept();
    else
        event->ignore();
}
```

默认 `QWidget::closeEvent()` 接受关闭。忽略事件后窗口继续存在并保持显示。

不要在析构函数才询问是否保存，因为那时对象销毁已经不可撤销。关闭确认属于 `closeEvent()`。

## 19. 重要生命周期事件

| 事件函数              | 发生时机        | 常见用途         |
| ----------------- | ----------- | ------------ |
| `showEvent()`     | 控件变为显示      | 启动只在可见时需要的刷新 |
| `hideEvent()`     | 控件隐藏        | 暂停预览或动画      |
| `closeEvent()`    | 收到关闭请求      | 保存确认、允许拒绝    |
| `resizeEvent()`   | 尺寸变化        | 更新与尺寸强相关的缓存  |
| `moveEvent()`     | 位置变化        | 少量位置相关状态     |
| `changeEvent()`   | 字体、样式、语言等变化 | 刷新派生资源       |
| `focusInEvent()`  | 获得焦点        | 切换编辑视觉状态     |
| `focusOutEvent()` | 失去焦点        | 提交或校验编辑状态    |

重写后如果没有完全替代父类语义，应调用基类实现。

### 19.1 构造函数不是“窗口已就绪”事件

构造期间：

- 布局可能尚未完成；
- 原生窗口可能尚未创建；
- 最终屏幕和 DPI 可能尚未确定；
- 子控件可能还没全部加入。

需要最终尺寸的计算放到首次 `showEvent()`、`resizeEvent()` 或事件循环后的单次回调，并避免每次 show 重复做昂贵初始化。

## 20. 绘制与背景

自定义控件在 `paintEvent()` 中绘制：

```cpp
void Preview::paintEvent(QPaintEvent *)
{
    QPainter p(this);
    p.fillRect(rect(), palette().brush(QPalette::Base));
    p.setPen(palette().color(QPalette::Text));
    p.drawText(rect(), Qt::AlignCenter, text_);
}
```

使用 palette 角色比硬编码黑白更能适配深色主题、禁用状态和平台风格。

普通 QWidget 若希望样式表背景被标准方式绘制，可使用 `QStyleOption` 配合 `style()->drawPrimitive()`；不要在不了解样式系统时同时用 palette、样式表和手动画背景互相覆盖。

## 21. Palette、Style 与 Style Sheet 的层次

- `QStyle`：平台控件的几何指标和绘制行为；
- `QPalette`：文本、窗口、按钮、高亮等语义颜色角色；
- Qt Style Sheets：类似 CSS 的局部外观覆盖；
- 自绘：完全由 `paintEvent()` 负责。

优先顺序不是简单的“谁最后设置谁赢”，不同控件和属性的样式支持不同。选择一种主导方式，并在目标平台测试。

### 21.1 不要把 palette 当固定主题表

```cpp
const QColor text = palette().color(
    isEnabled() ? QPalette::Active : QPalette::Disabled,
    QPalette::Text);
```

Palette 有 Active、Inactive、Disabled 三个颜色组。只读取 Active 颜色会让失活或禁用状态看起来不自然。

## 22. 原生 Widget 与非原生 Widget

许多子 Widget 默认没有各自独立的原生窗口句柄，而由祖先窗口统一绘制，这能减少系统资源和闪烁。

调用 `winId()`、设置 `WA_NativeWindow`、嵌入某些原生窗口时可能强制创建原生句柄，并连带影响祖先或子控件。

只有与平台 API、视频表面或第三方原生组件集成时才主动要求原生窗口。普通控件不要为“可能更快”而调用 `winId()`。

## 23. 保存与恢复窗口几何

```cpp
// 关闭时
settings.setValue("mainWindow/geometry", saveGeometry());

// 创建后、显示前
restoreGeometry(
    settings.value("mainWindow/geometry").toByteArray());
```

`saveGeometry()` 保存的信息比 `pos()` 和 `size()` 更完整，能处理最大化状态和窗口边框差异。

屏幕布局可能已经改变。恢复失败或窗口落在所有可用屏幕之外时，应回退到当前主屏幕可用区域。

## 24. 应用何时退出

默认 `QApplication::quitOnLastWindowClosed()` 为 true。最后一个带 `WA_QuitOnClose` 的可见主窗口关闭时，应用通常退出。

```cpp
QApplication::setQuitOnLastWindowClosed(false);
```

托盘应用可能关闭所有窗口后继续运行，此时应提供明确的“退出”动作并管理后台资源，而不是让进程无界面地意外存活。

## 25. 常见错误

### 25.1 有布局又手动 setGeometry

布局下次激活会覆盖手动几何。应通过 size policy、stretch、spacing、margin 和 size hint 表达需求。

### 25.2 close 后继续使用 DeleteOnClose 对象

`close()` 触发延迟删除后，保存的裸指针会悬空。使用父对象所有权、`QPointer` 或在 destroyed 信号中清空引用。

### 25.3 把 isHidden 当实际不可见

父控件隐藏时，子控件自身可能不是 hidden，但仍不可见。根据需求使用 `isVisible()` 或 `isVisibleTo()`。

### 25.4 在构造函数依赖最终尺寸

布局和窗口系统还没完成协商。把尺寸相关逻辑放到 resize/show 生命周期，并保证可重复执行。

### 25.5 自定义控件不提供 sizeHint

布局只能依据默认无效建议和硬限制猜尺寸。根据内容实现 size hint，内容变化时调用 `updateGeometry()`。

### 25.6 无条件固定窗口尺寸

字体、DPI、翻译文本变化后内容可能被截断。默认让布局和尺寸建议工作。

### 25.7 禁用控件却仍从其他路径执行动作

`setEnabled(false)` 只阻止普通 UI 输入，不是业务权限控制。菜单、快捷键和程序调用仍需统一检查命令可用性。

## 26. API 速查表

| API                              | 用途          | 注意点          |
| -------------------------------- | ----------- | ------------ |
| `setParent()`                    | 改变父对象和嵌入关系  | 可能改变窗口身份并隐藏  |
| `rect()`                         | 自身局部矩形      | 常从 0,0 开始    |
| `geometry()`                     | 相对父控件的客户区几何 | 顶层窗口不含边框     |
| `frameGeometry()`                | 含窗口框架的几何    | 显示前可能不准确     |
| `mapToGlobal()`                  | 局部转屏幕坐标     | 不要手工累加位置     |
| `sizeHint()`                     | 理想尺寸建议      | 布局不保证完全采用    |
| `updateGeometry()`               | 通知布局建议变化    | 不负责重绘        |
| `update()`                       | 安排重绘        | 请求可被合并       |
| `setSizePolicy()`                | 表达伸缩意愿      | 与 stretch 配合 |
| `show()` / `hide()`              | 显示或隐藏       | 不销毁对象        |
| `close()`                        | 发送关闭事件      | 默认只隐藏        |
| `setAttribute(WA_DeleteOnClose)` | 关闭后删除       | 后续不要使用裸指针    |
| `setFocusPolicy()`               | 设置焦点来源      | 键盘事件的前提      |
| `saveGeometry()`                 | 序列化窗口几何     | 配合 QSettings |
| `restoreGeometry()`              | 恢复窗口几何      | 处理屏幕变化回退     |

## 27. 自测题

### 题 1：没有 parent 的 QWidget 是什么

<details>
<summary>答案</summary>

通常是独立顶层窗口；如果有 parent 但指定 `Qt::Window` 标志，也可成为窗口。

</details>

### 题 2：close 是否等于 delete

<details>
<summary>答案</summary>

默认不等于。close event 被接受后 Widget 通常只是隐藏。设置 `WA_DeleteOnClose` 时才在成功关闭后删除。

</details>

### 题 3：update 与 updateGeometry 有何区别

<details>
<summary>答案</summary>

`update()` 请求重新绘制；`updateGeometry()` 通知布局尺寸建议或策略发生变化。自定义控件内容和理想尺寸同时变化时可能都要调用。

</details>

### 题 4：为什么布局控件不应手动 resize

<details>
<summary>答案</summary>

布局拥有几何管理权，下一次布局激活会重新分配尺寸。应通过尺寸策略、最小最大尺寸、size hint 和 stretch 表达意图。

</details>

### 题 5：geometry 与 frameGeometry 的区别

<details>
<summary>答案</summary>

顶层窗口的 geometry 表示不含系统边框的客户区几何；frameGeometry 包含标题栏和边框，适合判断窗口在屏幕上的完整占用范围。

</details>

## 28. 本篇总结

1. QWidget 既是绘制和事件单元，也是对象树和几何树的节点。
2. parent 决定所有权、坐标、裁剪、可见性继承和窗口身份。
3. rect、geometry、frameGeometry 属于不同坐标语义，不能混用。
4. 布局通过 size hint、size policy 和限制协商尺寸，避免硬编码几何。
5. show、hide、close 和 delete 是不同生命周期操作。
6. 键盘输入依赖焦点策略，复合控件可使用焦点代理。
7. 窗口标志和原生句柄受平台窗口系统约束。
8. 关闭确认放在 closeEvent，尺寸相关逻辑放在正确生命周期事件。

下篇将进入应用级窗口结构：`QMainWindow` 的中心区、菜单、工具栏、Dock 和状态栏，以及 `QDialog` 的模态、异步打开和返回值管理。
