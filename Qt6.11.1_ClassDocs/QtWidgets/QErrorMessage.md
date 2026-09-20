# QErrorMessage

> Qt 6.11.1 · Qt Widgets · 来自 `QErrorMessage`

## 1. 先建立直觉

`QErrorMessage` 是专门显示错误消息的对话框，特点是支持“不要再显示此类消息”，并且会把待显示消息排队。它适合处理可能重复出现的非致命错误，而不是每次都用 `QMessageBox::critical()` 打断用户。

典型场景包括插件加载失败、某类后台同步错误、重复的数据格式警告、Qt 默认日志消息展示。对于一次性、需要明确选择的严重错误，`QMessageBox` 仍然更合适。

## 2. 类说明

- 头文件：`#include <QErrorMessage>`
- 模块：`Qt6::Widgets`
- 继承自：`QDialog`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它是对话框，但 `showMessage()` 会立即返回；如果当前已有消息在显示，后续消息会排队。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QErrorMessage(parent)` | 创建错误消息对话框。 |
| `showMessage(message)` | 显示一条错误消息；用户可选择不再显示相同消息。 |
| `showMessage(message, type)` | 按错误类型去重，适合同类错误不同文本。 |
| `qtHandler()` | 获取用于显示 Qt 默认日志消息的共享错误对话框。 |

## 4. 关键用法

### 适合重复错误

如果一个操作可能连续产生很多相同错误，用 `QErrorMessage` 比循环弹 `QMessageBox` 更友好。用户勾选不再显示后，同类消息不会继续打断工作。

`showMessage(message, type)` 的 `type` 很有用。比如“网络断开”每次详细文本不同，但你希望用户可以屏蔽这一类，就给它们同一个 type。

### 不适合决策型提示

`QErrorMessage` 只表达错误，不适合“重试/忽略/取消”这种需要用户选择的流程。需要选择时，用 `QMessageBox` 或自定义对话框。

### Qt 日志处理

`qtHandler()` 返回一个共享对象，用于显示 Qt 默认消息。它会继续把消息转发给原始消息处理器。这个入口适合调试工具或内部应用，不建议在面向普通用户的产品中无筛选地弹出所有日志。

## 5. 常见坑与经验

- `showMessage()` 不阻塞等待用户处理，后续逻辑不要依赖它的返回值。
- “不再显示”按消息或 type 起作用，设计 type 时要有稳定分类。
- 大量技术日志不应该直接弹给用户，先分级和去噪。
- GUI 线程中使用；后台错误通过信号投递过来。
- 真正致命错误应结合日志、状态恢复和明确退出策略。
