# Qt QFocusFrame 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFocusFrame>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QFocusFrame`  
> 定位：跟随目标控件的焦点装饰框

## 1. QFocusFrame 解决什么问题

`QFocusFrame` 用来在另一个控件周围绘制焦点框。它适合在不修改目标控件自身样式的情况下，额外提供一层焦点视觉提示。

它解决的是：

- 自定义焦点指示；
- 给没有明显焦点样式的控件加高亮框；
- 让焦点框跨越控件边界绘制；
- 在复杂容器中把“焦点装饰”从实际控件绘制里分离出来。

```text
目标 QWidget
      ▲
      │ setWidget()
      │
QFocusFrame
```

它不是普通的装饰性矩形。它会关注目标控件的几何、显示状态和事件变化，并根据当前样式绘制合适的焦点框。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 给输入框加焦点框

```cpp
#include <QApplication>
#include <QFocusFrame>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *edit = new QLineEdit(&window);
    edit->setGeometry(40, 40, 220, 32);

    auto *focusFrame = new QFocusFrame(&window);
    focusFrame->setWidget(edit);

    window.resize(320, 120);
    window.show();
    edit->setFocus();

    return app.exec();
}
```

实际项目中更常把 `QFocusFrame` 的父对象设为目标控件所在的顶层窗口，而不是把它塞进目标控件的布局里。这样它才有足够的空间绘制在目标控件外侧。

## 3. 核心使用模型

### 3.1 `setWidget()` 建立跟踪关系

```cpp
focusFrame->setWidget(target);
```

设置后，焦点框会以目标控件为参照处理位置、尺寸和状态。`widget()` 可以取回当前跟踪的目标。

### 3.2 焦点框和目标控件不是父子替代关系

`QFocusFrame` 不会替代目标控件，也不会把目标控件变成自己的子控件。它只是一个额外的 QWidget，用来绘制装饰。

### 3.3 目标控件所在的顶层窗口很重要

焦点框需要在目标控件所在的窗口层级里工作。若父对象、窗口层级或坐标关系不对，常见表现是焦点框不显示、位置偏移或被目标控件裁掉。

### 3.4 样式由 QStyle 决定

`QFocusFrame` 通过 `initStyleOption()` 准备样式选项，再让当前样式绘制。它不会自己硬编码一个跨平台一致的边框。

## 4. 适合用在哪里

- 无障碍或键盘导航增强；
- 自定义表单的焦点视觉；
- 给复杂控件增加外部高亮；
- 不希望修改控件内部样式表时的焦点装饰。

如果只是普通按钮或输入框的焦点样式，优先使用控件自身样式或样式表；`QFocusFrame` 更适合需要独立绘制层的场景。

## 5. 常见误区

### 5.1 把它放进目标控件的布局

焦点框通常应该是目标控件所在顶层窗口的子控件，而不是占用布局空间的普通子控件。

### 5.2 忘记调用 `setWidget()`

没有目标控件时，焦点框没有跟踪对象，自然不知道应该画在哪里。

### 5.3 手动频繁同步 geometry

这个类存在的意义就是跟踪目标控件。一般不要在每次 resize/focus 事件里自己重复移动它。

### 5.4 用样式表直接给 QFocusFrame 画死

它的绘制依赖 `QStyleOption` 和当前样式。过度硬编码可能让它在不同平台或 DPI 下表现不一致。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QFocusFrame(QWidget *parent = nullptr)` | 创建一个焦点装饰框控件。 | 父对象通常应是目标控件所在的顶层窗口。 |
| 析构 | `~QFocusFrame()` | 销毁焦点装饰框。 | 不会销毁被跟踪的目标控件。 |
| 关联 | `setWidget(QWidget *widget)` | 设置需要跟踪和装饰的目标控件。 | 目标控件应和焦点框处于合适的窗口层级。 |
| 查询 | `widget() const` | 返回当前跟踪的目标控件。 | 没有目标时返回 `nullptr`。 |
| 事件 | `event(QEvent *event)` | 处理焦点框自身的通用事件。 | 负责协调跟踪状态和控件事件。 |
| 事件过滤 | `eventFilter(QObject *watched, QEvent *event)` | 监听目标控件或相关对象的事件变化。 | 用于同步几何、显示和焦点状态。 |
| 绘制 | `paintEvent(QPaintEvent *)` | 绘制当前样式下的焦点框。 | 通常由 Qt 自动调用。 |
| 样式 | `initStyleOption(QStyleOption *option) const` | 填充给当前样式使用的焦点框选项。 | 子类化重写时要保持样式状态完整。 |

## 7. 一句话总结

`QFocusFrame` 是一个会跟踪目标控件的焦点装饰层，适合把焦点视觉从控件本身分离出来，并按当前 Qt 样式绘制。
