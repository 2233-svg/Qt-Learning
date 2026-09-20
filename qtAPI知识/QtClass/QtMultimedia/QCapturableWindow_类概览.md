# QCapturableWindow：描述一个可被窗口采集的窗口

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCapturableWindow>`  
> 所属模块：`Qt6::Multimedia`  
> 类型性质：隐式共享值类型  
> 引入版本：Qt 6.10  
> 相关类型：`QWindow`、`QWindowCapture`、`QMediaDevices`

## 1. 它解决什么问题

`QCapturableWindow` 是系统窗口采集列表中的一项描述信息。它让应用可以把“用户想录制的某个窗口”作为一个值传递给 `QWindowCapture`，而不必自己维护平台窗口句柄。

它描述的是可采集目标，不是视频帧接收器，也不直接开始录制：

```text
QMediaDevices::capturableWindows()
             |
             v
QCapturableWindow  --选择窗口-->  QWindowCapture
                                      |
                                      v
                              QMediaCaptureSession
```

### 1.1 真实场景

- 录屏工具让用户从当前窗口列表选择一个窗口；
- 教学或演示软件只录制某个应用窗口，不录制整个桌面；
- 自动化测试把指定 `QWindow` 作为采集源；
- 窗口销毁后，界面需要知道原来的采集目标已经失效。

## 2. 如何取得和使用

窗口列表由 `QMediaDevices::capturableWindows()` 提供。选择一项后传给 `QWindowCapture::setWindow()`：

```cpp
const QList<QCapturableWindow> windows =
        QMediaDevices::capturableWindows();

if (!windows.isEmpty()) {
    QWindowCapture capture;
    capture.setWindow(windows.first());
    // 再把 capture 接入 QMediaCaptureSession，并处理权限和错误。
}
```

Qt 6.10 起，也可以从本进程已有的 `QWindow` 构造：

```cpp
QCapturableWindow target(window);
if (target.isValid())
    capture.setWindow(target);
```

## 3. 有效性、快照和所有权

### 3.1 默认构造是空信息

`QCapturableWindow()` 构造一个不指向任何窗口的空对象。`isValid()` 返回 `false`，`description()` 通常为空或没有可用标题。

传入 `nullptr` 的 `QWindow*` 也会得到不指向窗口的对象。调用 `setWindow()` 前必须排除这种对象。

### 3.2 不拥有 `QWindow`

这个类型是值对象，不是 `QObject`，不会接管传入 `QWindow` 的所有权。销毁 `QCapturableWindow` 不会销毁窗口。

从 `QWindow*` 构造时，窗口必须在其所属 GUI 线程中使用；传入的指针也必须仍然指向有效的 `QWindow`。如果窗口先被销毁，描述对象不会替应用维持窗口。

### 3.3 `isValid()` 会读取当前状态

类文档特别说明：除了 `isValid()` 以外，类中保存的是窗口信息；`isValid()` 在调用时会拉取窗口当前状态。因此，之前有效的对象可能因为目标窗口被关闭、销毁或平台状态变化而变成无效。

不要只在选择窗口时检查一次有效性。开始采集前、窗口列表刷新后和收到采集错误时，都适合再次检查。

### 3.4 `description()` 是展示文本

描述通常对应窗口标题。标题会随着应用改名、文档切换或本地化而变化，不能用它作为稳定标识。若需要长期追踪窗口，应优先依赖 Qt 返回的对象和当前列表刷新机制，而不是持久化标题字符串。

## 4. 构造函数和复制移动

### 4.1 `QCapturableWindow()`

创建空窗口信息，不引用任何窗口。

### 4.2 `QCapturableWindow(QWindow *window)`

Qt 6.10 起提供，显式接收一个 `QWindow*`，建立指向该窗口的描述。构造函数可能在窗口尚未显示时生成无效对象，因此窗口已经 `show()` 或呈现后再构造更可靠。

如果应用还没有进入 Qt 事件循环，窗口的底层平台资源可能尚未建立。此时应稍后重新构造或重新调用 `isValid()`，不要把第一次失败永久缓存。

### 4.3 拷贝、移动、赋值和 `swap()`

复制、移动和赋值操作只转移或共享描述数据，不复制窗口本身，也不开始采集。`swap()` 适合在容器或状态更新中无额外拷贝地交换两个值。

相关非成员 `operator==` 和 `operator!=` 用于比较窗口描述。比较的目标是描述对象所代表的窗口，不应把 `description()` 字符串比较当成等价替代。

## 5. 与 `QWindowCapture` 的协作边界

`QCapturableWindow` 只解决“选哪个窗口”。`QWindowCapture` 才负责把目标窗口产生的视频送入 `QMediaCaptureSession`。

在典型链路中还需要：

1. 从 `QMediaDevices` 获取窗口列表；
2. 过滤 `isValid()` 为真的项；
3. 让用户选择；
4. 设置到 `QWindowCapture`；
5. 将 `QWindowCapture` 放进 `QMediaCaptureSession`；
6. 监听采集对象的状态和错误；
7. 窗口消失后重新枚举并让用户选择新的目标。

窗口可枚举并不保证一定能成功采集。操作系统隐私权限、窗口所在桌面、最小化状态、平台安全策略和后端支持都可能影响最终结果。

## 6. 线程与异步边界

对象本身是值类型，没有事件循环和信号。窗口发现和列表变化由 `QMediaDevices` 异步通知；采集状态和错误由 `QWindowCapture` / `QMediaCaptureSession` 通知。

`QWindow` 属于 GUI 线程对象。跨线程保存一个 `QCapturableWindow` 值不等于可以在工作线程直接访问窗口或启动窗口采集。涉及 `QWindow` 构造、窗口显示状态和媒体 QObject 的操作，应遵守各自线程归属。

## 7. 常见误区

- 把 `QCapturableWindow` 当成视频流：它只是目标描述。
- 认为描述对象拥有窗口：它不会销毁或保持窗口存活。
- 只看 `description()`：标题不是稳定 ID。
- 构造后永远认为有效：窗口关闭后 `isValid()` 会改变。
- 在窗口尚未呈现时构造并永久缓存：可能得到暂时无效对象。
- 以为设置窗口就已经开始录制：还需要 `QWindowCapture`、session、输出和权限。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCapturableWindow()` | 构造不指向任何窗口的空描述。 | `isValid()` 为 `false`。 |
| 构造 | `explicit QCapturableWindow(QWindow *window)` | Qt 6.10 起从已有 `QWindow` 创建窗口描述。 | 不转移所有权；窗口尚未呈现时可能无效。 |
| 构造 | `QCapturableWindow(const QCapturableWindow &other)` | 复制窗口描述。 | 不复制或拥有 `QWindow`。 |
| 构造 | `QCapturableWindow(QCapturableWindow &&other)` | 移动窗口描述。 | 被移动对象只应继续析构或重新赋值。 |
| 析构 | `~QCapturableWindow()` | 销毁描述值。 | 不销毁目标窗口。 |
| 赋值 | `QCapturableWindow &operator=(const QCapturableWindow &other)` | 复制赋值。 | 只替换描述关系。 |
| 赋值 | `QCapturableWindow &operator=(QCapturableWindow &&other)` | 移动赋值。 | 适合容器和临时返回值。 |
| 工具 | `void swap(QCapturableWindow &other) noexcept` | 交换两个描述对象。 | 不启动采集。 |
| 比较 | `bool operator==(const QCapturableWindow &, const QCapturableWindow &) noexcept` | 比较两个窗口描述。 | 不要用标题字符串代替。 |
| 比较 | `bool operator!=(const QCapturableWindow &, const QCapturableWindow &) noexcept` | 判断两个窗口描述是否不同。 | 适合检测选择变化。 |
| 查询 | `bool isValid() const` | 查询目标窗口当前是否仍有效。 | 每次调用可能读取当前平台状态。 |
| 查询 | `QString description() const` | 返回窗口说明，通常是标题。 | 适合显示，不是稳定标识。 |

## 9. 一句话总结

`QCapturableWindow` 是窗口采集的“目标描述值”：它不拥有窗口、不承载帧，只把用户选择的窗口交给 `QWindowCapture`，并要求应用持续处理窗口失效和平台采集边界。
