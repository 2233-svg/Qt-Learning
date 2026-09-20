# Qt QCursor 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCursor>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 定位：鼠标光标的形状、热点与全局位置

## 1. 它解决什么问题

`QCursor` 表示一个可显示的鼠标光标。它既可以是 Qt 或平台提供的标准形状，也可以由 `QPixmap`、`QBitmap` 和掩码构造为自定义图像光标。

它解决两类不同但常被混在一起的问题：

1. **光标长什么样**：箭头、文本插入、拖动、等待、自定义图片等；
2. **鼠标指针在哪里**：读取或设置屏幕上的热点位置。

典型场景：

- 为某个 `QWidget` 设置文本、手形、缩放或拖拽提示光标；
- 应用处理耗时操作时，临时给所有窗口显示等待光标；
- 画布工具在选择、平移、绘制等模式间切换光标；
- 创建像素级热点准确的取色器、十字准星或自定义工具光标；
- 将 widget 局部坐标和鼠标全局坐标互相映射。

`QCursor` 是值类型，不是某个窗口的专属状态。把它赋给 widget、窗口或应用覆盖栈后，才会影响实际显示。

## 2. 构建与使用前提

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

Widgets 项目通常还会链接 `Qt6::Widgets`：

```cpp
#include <QCursor>
#include <QGuiApplication>
#include <QWidget>
```

虽然可以在 `QGuiApplication` 创建前构造一个 `QCursor` 占位对象，但它在那之前没有实际用途。使用一个早于 `QGuiApplication` 创建的 `QCursor` 会导致崩溃。也就是说，光标的实际创建、查询和应用应放在 GUI 应用对象已经存在之后。

## 3. 最小可用代码

### 3.1 为一个 widget 设置光标

```cpp
#include <QCursor>
#include <QWidget>

void configureCanvas(QWidget *canvas)
{
    canvas->setCursor(QCursor(Qt::CrossCursor));
}
```

这里的光标仅在指针位于该 widget 的有效区域时生效；子 widget、应用级覆盖光标或平台限制都可能改变最终显示结果。

### 3.2 临时显示等待光标

```cpp
#include <QGuiApplication>

void runBlockingOperation()
{
    QGuiApplication::setOverrideCursor(Qt::WaitCursor);

    // 执行同步耗时操作。

    QGuiApplication::restoreOverrideCursor();
}
```

每次 `setOverrideCursor()` 都必须有对应的 `restoreOverrideCursor()`。实际代码应使用作用域守卫、RAII 或明确的 `try`/错误路径清理，避免异常返回或提前 return 后把应用永久留在等待光标状态。

## 4. 标准光标、自定义光标与热点

### 4.1 优先使用 `Qt::CursorShape`

标准光标由 `Qt::CursorShape` 枚举描述，常用项包括：

- `Qt::ArrowCursor`：普通箭头，也是默认形状；
- `Qt::IBeamCursor`：文本编辑位置；
- `Qt::PointingHandCursor`：可点击链接或按钮；
- `Qt::OpenHandCursor` / `Qt::ClosedHandCursor`：可拖拽或正在拖动画布；
- `Qt::SizeHorCursor`、`Qt::SizeVerCursor`：尺寸调整；
- `Qt::WaitCursor` / `Qt::BusyCursor`：等待或忙碌；
- `Qt::ForbiddenCursor`：拖放目标不接受当前内容；
- `Qt::BlankCursor`：隐藏光标。

标准形状可适配平台主题、缩放和无障碍习惯。除非产品确实需要特定图案，优先使用标准形状比自定义位图更稳妥。

### 4.2 自定义 `QPixmap` 光标

```cpp
QPixmap pixmap(":/cursors/eyedropper.png");
QCursor eyedropper(pixmap, 2, 18);
targetWidget->setCursor(eyedropper);
```

`hotX`、`hotY` 定义热点，即系统真正认为“鼠标正在指向”的像素。取色器通常让热点位于吸管尖端，而不是图像中心。

若 `hotX` 或 `hotY` 为负数，Qt 默认取对应维度的中心：

```text
hotX = pixmap.width() / 2
hotY = pixmap.height() / 2
```

默认居中对箭头、吸管和画笔等方向性光标常常不正确，应显式设置热点。

光标可支持的尺寸依赖显示硬件和底层窗口系统。Qt 建议使用 `32 x 32`，它在各平台均受支持；某些平台还支持 `16 x 16`、`48 x 48` 或 `64 x 64`。不要假设任意大尺寸都会原样显示。

### 4.3 传统 bitmap + mask 光标

`QCursor(const QBitmap &, const QBitmap &, int, int)` 适用于单色位图和透明掩码。它主要用于遗留资源、极简黑白光标或必须精确控制掩码的场景。

对新代码，透明 `QPixmap` 光标往往更直接。若使用 bitmap/mask，二者必须来自一致的尺寸和像素布局；否则无法得到可预期的形状和透明区域。

## 5. 光标位置与坐标系

### 5.1 `QCursor::pos()` 返回全局屏幕坐标

```cpp
const QPoint global = QCursor::pos();
```

无参数版本返回主屏幕上当前鼠标热点的**全局屏幕坐标**，不是当前 widget 的局部坐标。要取得 widget 内位置，使用：

```cpp
const QPoint local = widget->mapFromGlobal(QCursor::pos());
```

要把 widget 内的点移动到屏幕坐标，则反向映射：

```cpp
QCursor::setPos(widget->mapToGlobal(QPoint(20, 20)));
```

直接把局部 `QPoint(20, 20)` 交给无参数 `setPos()` 会把光标移到主屏幕全局坐标 `(20, 20)`，通常不是目标 widget 的内部位置。

### 5.2 多屏幕重载

```cpp
QPoint position = QCursor::pos(screen);
QCursor::setPos(screen, position);
```

带 `QScreen *` 的重载针对指定屏幕读取或设置热点位置，但坐标仍然是全局屏幕坐标。`QScreen` 指针由 Qt 屏幕管理系统拥有；显示器拔出、虚拟桌面改变或应用退出时，该指针可能失效。

若要长期保存某块屏幕的身份，应监听 `QGuiApplication::screenAdded`、`screenRemoved`，以及 `QWindow::screenChanged` 等变化，而不是缓存一个裸 `QScreen *` 并在未来无条件使用。

### 5.3 没有传统窗口系统的平台

在没有窗口系统或没有可用光标的平台，`pos()` 的返回值基于 `QWindowSystemInterface` 生成的鼠标移动事件。这类环境中不应把读取或设置光标位置作为业务逻辑的唯一依据；触摸设备、嵌入式系统和远程显示环境可能没有可操作的系统光标。

## 6. widget 光标与应用级覆盖光标

### 6.1 widget 级设置

`QWidget::setCursor()` 为一个控件设置默认光标。适用于正常、持久的交互语义，例如文本框的 I-beam、可拖动画布的手形和分隔条的调整光标。

```cpp
splitterHandle->setCursor(Qt::SplitHCursor);
```

这里的设置不需要也不应调用 `restoreOverrideCursor()`；它是控件属性，随控件状态或后续 `unsetCursor()` 改变。

### 6.2 应用级覆盖是栈

`QGuiApplication::setOverrideCursor()` 对整个应用窗口临时覆盖光标。Qt 把覆盖光标保存在内部栈中：

```text
setOverrideCursor(A)  -> [A]
setOverrideCursor(B)  -> [A, B]
restoreOverrideCursor -> [A]
restoreOverrideCursor -> []
```

所以嵌套任务可以安全地各自压入等待光标，前提是每一层都在结束时恢复一次。少恢复一次会让栈无法清空，应用继续显示不正确的覆盖光标。

`QGuiApplication::changeOverrideCursor()` 只替换当前栈顶，不压栈；如果此前没有调用 `setOverrideCursor()`，它没有效果。`QGuiApplication::overrideCursor()` 会返回当前栈顶指针；栈为空时返回 `nullptr`，不要解引用后者。

## 7. 生命周期、复制和移动

`QCursor` 是隐式共享值类型。复制和赋值用于传递光标状态，不表示对某个 OS 光标句柄的独占所有权。`swap()` 很快且不会失败，适合值对象交换。

移动构造或移动赋值后，被移动源对象只允许销毁或再次赋值；调用其它成员函数的行为未定义。通常没有必要为了一个 `QCursor` 手工管理移动后对象，保持普通值语义即可。

`pixmap()`、`bitmap()`、`mask()` 都按值返回图像对象：

- 标准光标的 `bitmap()` 和 `mask()` 返回空对象；
- `pixmap()` 仅在该光标确实是 pixmap 光标时有效；
- 标准光标的 `hotSpot()` 返回 `(0, 0)`，不能用它推断系统箭头尖端的像素位置。

## 8. 比较、序列化与 `QVariant`

`operator==` 比较形状；对于 bitmap 光标还比较热点和 bitmap/mask 或 pixmap。比较 bitmap 光标时，Qt 只比较图像的 cache key，不逐像素比较。因此它适合判断“是不是同一份光标值”，不适合做图像内容的强一致性校验。

`operator<<` 和 `operator>>` 可以将 `QCursor` 写入或读出 `QDataStream`。若数据要跨进程、跨版本或长期保存，应同时控制 `QDataStream` 版本，并认识到标准光标的具体外观最终由平台主题决定。

`operator QVariant()` 允许把光标放进 `QVariant`，用于属性系统、模型数据或动态配置。取回时仍应检查 `QVariant` 类型是否正确。

## 9. 常见误区与排查顺序

### 9.1 设置光标位置后跑到错误位置

检查传给 `setPos()` 的是局部坐标还是全局坐标。`QCursor::setPos()` 接受全局坐标，局部坐标必须先经过 `mapToGlobal()`。

### 9.2 等待光标再也没有消失

检查每个 `setOverrideCursor()` 是否有一一对应的 `restoreOverrideCursor()`，尤其是嵌套调用、错误返回、取消和异常路径。`changeOverrideCursor()` 不能代替恢复栈。

### 9.3 自定义光标点击点不准确

检查热点。负值会导致居中热点；箭头尖端、画笔笔尖和吸管尖端通常必须显式指定。

### 9.4 自定义光标在部分平台模糊或被缩小

检查资源尺寸、设备像素比和平台支持。优先使用常见尺寸，尽量提供适配高 DPI 的 pixmap 资源。

### 9.5 程序刚启动就崩溃

检查是否在 `QGuiApplication` 创建前使用了 `QCursor`。提前构造只能当作无用占位，真正使用必须等待 GUI 应用就绪。

### 9.6 指定屏幕后偶发崩溃

检查保存的 `QScreen *` 是否在屏幕热插拔后失效。屏幕对象不是长期稳定的全局单例。

## 10. 与相关类型的协作

- `Qt::CursorShape`：标准光标形状枚举。
- `QWidget::setCursor()`：设置某个 Widgets 控件的光标。
- `QGuiApplication::setOverrideCursor()`：临时覆盖全应用光标，并使用栈管理。
- `QPixmap`：构造带颜色和透明度的自定义光标。
- `QBitmap`：构造传统黑白 bitmap/mask 光标。
- `QScreen`：在多屏幕下选择光标位置操作所针对的屏幕。
- `QPoint`：保存热点、局部位置和全局位置。
- `QDataStream`、`QVariant`：序列化和动态值传递。

## 11. 逐项 API 说明

### 构造、复制与赋值

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `QCursor()` | 创建默认箭头光标。 | GUI 应用创建前不可实际使用。 |
| `QCursor(Qt::CursorShape shape)` | 创建指定标准形状。 | 优先用于跨平台语义光标。 |
| `explicit QCursor(const QPixmap &pixmap, int hotX = -1, int hotY = -1)` | 创建彩色/透明自定义光标。 | 负热点默认居中；推荐 `32 x 32`。 |
| `QCursor(const QBitmap &bitmap, const QBitmap &mask, int hotX = -1, int hotY = -1)` | 创建单色 bitmap/mask 光标。 | bitmap 与 mask 必须匹配；更适合遗留或单色资源。 |
| `QCursor(const QCursor &other)` | 复制光标值。 | 隐式共享，不是独占 OS 资源。 |
| `QCursor(QCursor &&other) noexcept` | 移动构造。 | 移动源之后只能销毁或重新赋值。 |
| `QCursor &operator=(const QCursor &other)` | 复制赋值。 | 返回当前对象引用。 |
| `QCursor &operator=(QCursor &&other) noexcept` | 移动赋值。 | 不再使用移动源的其它成员。 |
| `void swap(QCursor &other) noexcept` | 高效交换两个光标。 | 只交换值，不改变已应用到其它对象的历史副本。 |

### 形状和图像查询

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `Qt::CursorShape shape() const` | 返回光标形状标识。 | 标准形状的实际像素外观由平台主题决定。 |
| `void setShape(Qt::CursorShape shape)` | 将当前对象改为标准形状。 | 修改值对象后，要重新应用到 widget 或覆盖栈才影响显示。 |
| `QPixmap pixmap() const` | 返回 pixmap 光标的图像。 | 只有 pixmap 光标时有效。 |
| `QBitmap bitmap() const` | 返回 bitmap 光标的位图。 | 标准光标返回空 bitmap。 |
| `QBitmap mask() const` | 返回 bitmap 光标的掩码。 | 标准光标返回空 bitmap。 |
| `QPoint hotSpot() const` | 返回自定义光标热点。 | 标准光标返回 `(0, 0)`。 |

### 全局光标位置

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `static QPoint pos()` | 获取主屏幕中的全局热点坐标。 | 不是 widget 局部坐标。 |
| `static QPoint pos(const QScreen *screen)` | 获取指定屏幕的全局热点坐标。 | `screen` 生命周期由 Qt 管理。 |
| `static void setPos(int x, int y)` | 移动主屏幕上的光标。 | 参数是全局坐标。 |
| `static void setPos(const QPoint &p)` | 以点形式移动光标。 | 等价于无屏幕参数的整数重载。 |
| `static void setPos(QScreen *screen, int x, int y)` | 移动指定屏幕上的光标。 | 坐标仍是全局坐标。 |
| `static void setPos(QScreen *screen, const QPoint &p)` | 以点形式移动指定屏幕上的光标。 | 注意热插拔导致 `screen` 失效。 |

### 相关非成员

| API | 作用 | 关键边界 |
| --- | --- | --- |
| `bool operator==(const QCursor &, const QCursor &) noexcept` | 判断两个光标是否等价。 | bitmap 光标只比较 cache key，不逐像素比较。 |
| `bool operator!=(const QCursor &, const QCursor &) noexcept` | 判断两个光标是否不等价。 | 等价于 `!(a == b)`。 |
| `QDataStream &operator<<(QDataStream &, const QCursor &)` | 序列化光标。 | 长期保存时管理数据流版本和平台外观差异。 |
| `QDataStream &operator>>(QDataStream &, QCursor &)` | 反序列化光标。 | 读取失败时检查 stream 状态。 |
| `operator QVariant() const` | 转为 `QVariant`。 | 取回时验证类型。 |

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标准形状 | `QCursor(Qt::CursorShape)` / `setShape()` | 使用平台适配的箭头、手形、等待等光标。 | 优先于自定义图片；应用前需有 `QGuiApplication`。 |
| 自定义形状 | `QCursor(const QPixmap &, int, int)` | 创建带透明度的图像光标。 | 显式设置热点；尺寸受平台限制。 |
| 自定义形状 | `QCursor(const QBitmap &, const QBitmap &, int, int)` | 创建传统单色 bitmap/mask 光标。 | bitmap 与 mask 必须匹配。 |
| 查询 | `shape()` / `pixmap()` / `bitmap()` / `mask()` / `hotSpot()` | 读取光标表示。 | 标准光标的 bitmap/mask 为空，热点为 `(0, 0)`。 |
| 位置 | `pos()` / `pos(QScreen *)` | 读取鼠标全局位置。 | 需要局部位置时使用 `mapFromGlobal()`。 |
| 位置 | `setPos()` 重载 | 移动系统鼠标光标。 | 传入全局坐标；不要滥用以免破坏用户控制感。 |
| 控件应用 | `QWidget::setCursor()` | 为单个控件指定正常交互光标。 | 这是控件属性，不使用覆盖栈恢复。 |
| 全局覆盖 | `QGuiApplication::setOverrideCursor()` | 在特殊状态临时覆盖全应用光标。 | 每次调用都必须配对 `restoreOverrideCursor()`。 |
| 覆盖栈 | `changeOverrideCursor()` / `overrideCursor()` / `restoreOverrideCursor()` | 更改、查询、弹出当前应用覆盖光标。 | `change...` 不压栈；没有覆盖时 `overrideCursor()` 为 `nullptr`。 |
| 值语义 | 复制、移动、`swap()`、比较 | 传递和管理光标值。 | 移动源不可再调用一般成员；bitmap 比较不逐像素。 |

---

### 一句话总结

`QCursor` 负责光标形状、热点和全局位置；widget 光标用于常态交互，`QGuiApplication` 覆盖光标用于短期全局状态，并且必须严格成对恢复。
