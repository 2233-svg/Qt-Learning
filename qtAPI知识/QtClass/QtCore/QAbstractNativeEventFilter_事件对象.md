# QAbstractNativeEventFilter 原生事件过滤器深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractNativeEventFilter>`  
> 所属模块：`Qt6::Core`  
> 继承关系：无，纯接口式基类  
> 相关类：`QCoreApplication`、`QAbstractEventDispatcher`

## 1. 它解决什么问题

`QAbstractNativeEventFilter` 让你在 Qt 把平台原生消息转换成 `QEvent` 之前，先看到这些底层消息，必要时还可以拦截它们。

普通 Qt 事件过滤器处理的是：

```text
QEvent::MouseButtonPress
QEvent::KeyPress
QEvent::Resize
QEvent::Close
```

而 native event filter 处理的是平台消息：

```text
Windows MSG
X11 xcb_generic_event_t
macOS NSEvent
```

所以它不是日常事件过滤的首选。只要能用 `QObject::installEventFilter()`、`QWidget::event()`、`QObject::event()` 或具体事件处理函数解决，就不要进入 native 层。native 层代码通常更脆弱，因为消息结构、`eventType` 字符串和行为都跟平台插件有关。

## 2. 它和普通事件过滤器的区别

`QObject::installEventFilter()` 工作在 Qt 事件层。此时平台消息已经被 Qt 翻译成 `QEvent`，跨平台性比较好。

`QAbstractNativeEventFilter` 工作在更早的位置：

```text
操作系统消息
      ↓
QAbstractNativeEventFilter::nativeEventFilter()
      ↓
Qt 平台插件或事件分发器
      ↓
QEvent
      ↓
QObject::eventFilter() / QObject::event()
```

这意味着 native filter 适合这些场景：

- 处理注册热键等系统级消息；
- 观察某些 Qt 没有暴露成 `QEvent` 的平台消息；
- 和原生窗口、平台 SDK、底层输入法或系统集成代码配合；
- 做平台特定诊断。

不适合这些场景：

- 普通鼠标键盘事件；
- 控件内部行为定制；
- 跨平台 UI 逻辑；
- 业务事件分发。

## 3. 如何安装和移除

过滤器对象本身只是一个 C++ 对象。创建它不会自动生效，必须安装到应用或事件分发器上。

常见写法：

```cpp
class NativeFilter : public QAbstractNativeEventFilter
{
public:
    bool nativeEventFilter(const QByteArray &eventType,
                           void *message,
                           qintptr *result) override
    {
        Q_UNUSED(eventType);
        Q_UNUSED(message);
        Q_UNUSED(result);
        return false;
    }
};

NativeFilter filter;
QCoreApplication::instance()->installNativeEventFilter(&filter);
```

不再需要时：

```cpp
QCoreApplication::instance()->removeNativeEventFilter(&filter);
```

也可以通过当前线程的事件分发器安装：

```cpp
QAbstractEventDispatcher::instance()
    ->installNativeEventFilter(&filter);
```

实际项目里更常见的是使用 `QCoreApplication` 入口，因为文档也强调要把过滤器安装到应用对象上。无论哪种方式，重点都是：过滤器对象必须在被调用期间保持有效。

## 4. `nativeEventFilter()` 的返回值

核心函数是：

```cpp
virtual bool nativeEventFilter(const QByteArray &eventType,
                               void *message,
                               qintptr *result) = 0;
```

返回值语义非常重要：

- 返回 `false`：不拦截，继续让 Qt 或后续过滤器处理。
- 返回 `true`：消息已被过滤，停止后续处理。

大多数观察型代码都应该返回 `false`。只有你非常确定这个消息不应再交给 Qt，例如你已经完整处理了某个系统热键或窗口消息，才返回 `true`。

错误地返回 `true` 可能导致窗口无法收到输入、快捷键失效、系统消息被吞掉，甚至让平台插件进入不一致状态。

## 5. `eventType` 和 `message` 如何理解

`eventType` 是平台插件提供的字符串，用来告诉你 `message` 应该怎么解释。

常见情况：

- X11：`eventType` 为 `"xcb_generic_event_t"`，`message` 可转成 `xcb_generic_event_t *`。
- Windows：`eventType` 为 `"windows_generic_MSG"` 时表示顶层窗口消息，`message` 可转成 `MSG *`。
- Windows：`eventType` 为 `"windows_dispatcher_MSG"` 时表示事件分发器收到的系统级消息，例如注册热键。
- macOS：`eventType` 为 `"mac_generic_NSEvent"`，`message` 可转成 `NSEvent *`。

不要脱离 `eventType` 直接强转 `message`。同一个程序换平台、换平台插件、甚至同平台不同消息来源时，`message` 指向的数据结构都可能不同。

Windows 上的 `result` 对应 `LRESULT` 指针。只有在你返回 `true` 并且确实要给 Windows 消息处理返回特定结果时，才应该写它。其它平台通常不会用它。

## 6. Windows 示例：观察热键消息

```cpp
#include <QAbstractNativeEventFilter>
#include <QByteArray>

#ifdef Q_OS_WIN
#  include <windows.h>
#endif

class HotkeyFilter : public QAbstractNativeEventFilter
{
public:
    bool nativeEventFilter(const QByteArray &eventType,
                           void *message,
                           qintptr *result) override
    {
        Q_UNUSED(result);

#ifdef Q_OS_WIN
        if (eventType == "windows_dispatcher_MSG") {
            MSG *msg = static_cast<MSG *>(message);

            if (msg->message == WM_HOTKEY) {
                handleHotkey(msg->wParam);
                return true;
            }
        }
#endif

        return false;
    }

private:
    void handleHotkey(WPARAM id);
};
```

这里返回 `true` 是因为示例假设已经完整处理了 `WM_HOTKEY`。如果只是记录日志，应返回 `false`。

## 7. X11 示例：按类型读取消息

```cpp
class XcbFilter : public QAbstractNativeEventFilter
{
public:
    bool nativeEventFilter(const QByteArray &eventType,
                           void *message,
                           qintptr *) override
    {
        if (eventType == "xcb_generic_event_t") {
            auto *event = static_cast<xcb_generic_event_t *>(message);
            inspectXcbEvent(event);
        }

        return false;
    }

private:
    void inspectXcbEvent(xcb_generic_event_t *event);
};
```

这类代码应放在明确的平台编译条件下。不要让 Windows 或 macOS 构建看到 XCB 类型。

## 8. macOS 示例：Objective-C++ 边界

macOS 示例通常需要 `.mm` 文件，因为 `NSEvent` 属于 AppKit：

```cpp
bool CocoaFilter::nativeEventFilter(const QByteArray &eventType,
                                    void *message,
                                    qintptr *)
{
    if (eventType == "mac_generic_NSEvent") {
        NSEvent *event = static_cast<NSEvent *>(message);
        if ([event type] == NSKeyDown) {
            handleKey(event);
        }
    }

    return false;
}
```

qmake 工程里常见配置是：

```qmake
OBJECTIVE_SOURCES += cocoa_filter.mm
LIBS += -framework AppKit
```

CMake 工程则要按 Objective-C++ 源文件和 AppKit 链接规则配置。这个层面已经越过了普通 Qt 跨平台边界，维护时要非常明确目标平台。

## 9. 多个过滤器的调用顺序

通过事件分发器安装多个 native filter 时，后安装的过滤器先被调用。只要某个过滤器返回 `true`，后续过滤器和 Qt 正常处理就会停止。

因此多个过滤器并存时要遵守两个习惯：

- 观察型过滤器尽量返回 `false`。
- 拦截型过滤器只处理自己明确拥有的消息，不要用宽泛条件吞掉一类消息。

## 10. 生命周期和线程边界

`QAbstractNativeEventFilter` 不是 `QObject`，没有 QObject 父子对象生命周期，也没有信号槽自动断开。你要自己保证对象活得足够久。

析构函数会自动把它从应用移除，但这不等于可以随便让局部对象提前析构。下面这种写法很危险：

```cpp
void installTemporaryFilter()
{
    NativeFilter filter;
    QCoreApplication::instance()->installNativeEventFilter(&filter);
}
```

函数返回后 `filter` 已经销毁，后续如果还有平台消息进入，就可能出问题。应把过滤器作为应用级对象、主窗口成员或更长生命周期对象保存。

`nativeEventFilter()` 可能接收所有线程的原生事件，具体路径跟平台插件和事件分发器有关。回调里不要直接操作不属于当前线程的 QObject。需要跨线程处理时，投递 Qt 事件或 queued signal。

## 11. 常见误区

### 11.1 能用 `QEvent` 却使用 native filter

native filter 牺牲可移植性。普通键盘鼠标、窗口关闭、控件行为，优先使用 Qt 事件系统。

### 11.2 忘记检查 `eventType`

`message` 是 `void *`，只有结合 `eventType` 才知道能转成什么类型。盲目强转是平台相关崩溃的常见来源。

### 11.3 观察消息却返回 `true`

返回 `true` 是拦截，不是“处理成功”。调试打印、统计、旁路观察通常都应该返回 `false`。

### 11.4 生命周期太短

过滤器不是 QObject 子对象，安装后必须保证对象持续存在。需要卸载时主动调用 `removeNativeEventFilter()`。

### 11.5 在回调里做耗时工作

native filter 位于事件入口处。回调太慢会拖慢整个事件分发，甚至影响窗口响应。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造函数 | `QAbstractNativeEventFilter()` | 创建一个原生事件过滤器基类对象 | 创建后不会自动生效，必须安装到应用或 dispatcher |
| 析构函数 | `~QAbstractNativeEventFilter()` | 销毁过滤器并自动从应用移除 | 对象仍必须在安装期间保持有效 |
| 纯虚函数 | `nativeEventFilter(const QByteArray &eventType, void *message, qintptr *result)` | 接收每个原生平台消息并决定是否拦截 | 返回 `true` 会阻止继续处理，返回 `false` 才是旁路观察 |
| 安装相关 | `QCoreApplication::installNativeEventFilter(QAbstractNativeEventFilter *filterObj)` | 把过滤器安装到应用级原生事件入口 | 过滤器不转移所有权 |
| 移除相关 | `QCoreApplication::removeNativeEventFilter(QAbstractNativeEventFilter *filterObj)` | 从应用级原生事件入口移除过滤器 | 可在不需要时主动移除 |
| dispatcher 相关 | `QAbstractEventDispatcher::installNativeEventFilter(QAbstractNativeEventFilter *filterObj)` | 在事件分发器层安装过滤器 | 多个过滤器后装先调用 |
| dispatcher 相关 | `QAbstractEventDispatcher::filterNativeEvent(const QByteArray &eventType, void *message, qintptr *result)` | 事件分发器把原生消息送入过滤器链 | 自定义 dispatcher 必须对收到的系统消息调用 |

## 13. 一句话抓住它

`QAbstractNativeEventFilter` 是进入 Qt 事件系统之前的原生消息观察点。它适合少数平台集成场景，核心规则是先看 `eventType` 再解释 `message`，只是观察就返回 `false`，只有真正要拦截时才返回 `true`。
