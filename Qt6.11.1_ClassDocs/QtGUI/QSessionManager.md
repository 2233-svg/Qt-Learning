# QSessionManager
> Qt 6.11.1 · Qt GUI · 来自 `QSessionManager`

## 1. 先建立直觉

`QSessionManager` 用于桌面会话结束、注销、关机或会话恢复时，应用和系统会话管理器之间的协商。它最常见的出现位置不是你主动构造，而是在 `QGuiApplication::commitDataRequest` 或 `saveStateRequest` 的槽函数参数里。

这个类关注两个问题：退出前能不能保存数据，以及下次会话要不要、如何重启应用。

## 2. 类说明

- 头文件：`#include <QSessionManager>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QObject`
- 获取方式：由 `QGuiApplication` 相关信号传入
- 协作类：`QGuiApplication`、`QApplication`、主窗口保存逻辑

应用通常不要长期保存 `QSessionManager *`。它是当前会话管理请求的上下文对象，使用边界在保存/提交阶段内。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `allowsInteraction()` | 请求在关机/注销过程中显示普通交互 UI |
| `allowsErrorInteraction()` | 请求显示错误相关交互 UI，优先级可能更高 |
| `release()` | 交互完成后释放会话管理器的交互令牌 |
| `cancel()` | 用户取消或保存失败时请求取消关机/注销 |
| `requestPhase2()` / `isPhase2()` | 请求第二阶段保存，常用于窗口管理器等特殊应用 |
| `setRestartHint()` / `restartHint()` | 设置会话恢复时是否重启应用 |
| `setRestartCommand()` / `restartCommand()` | 设置恢复应用的命令 |
| `setDiscardCommand()` / `discardCommand()` | 设置放弃保存状态时执行的命令 |
| `setManagerProperty()` | 设置会话管理器理解的额外属性 |
| `sessionId()` / `sessionKey()` | 当前会话标识 |

## 4. RestartHint 速查

| 枚举 | 含义 |
| --- | --- |
| `RestartIfRunning` | 退出会话时应用仍在运行，则下次恢复 |
| `RestartAnyway` | 无论当前是否运行，下次会话都希望启动 |
| `RestartImmediately` | 如果应用不在运行，立即重启 |
| `RestartNever` | 不希望被自动重启 |

默认通常是 `RestartIfRunning`，适合普通 GUI 应用。

## 5. 关键用法

保存未提交文档时：

```cpp
connect(qGuiApp, &QGuiApplication::commitDataRequest,
        this, [this](QSessionManager &manager) {
    if (hasUnsavedChanges()) {
        if (manager.allowsInteraction()) {
            const bool ok = askAndSaveDocuments();
            manager.release();
            if (!ok)
                manager.cancel();
        } else {
            if (!saveWithoutPrompt())
                manager.cancel();
        }
    }
});
```

关键是：能交互不等于可以拖很久。拿到交互许可后应尽快问完用户并 `release()`，真正耗时的保存可以继续做，让其他应用也有机会弹出提示。

## 6. 使用场景

- 文档编辑器在注销前询问保存、放弃或取消。
- IDE、绘图软件保存工作区和打开文件列表。
- 后台工具声明下次会话是否恢复。
- 窗口管理器或会话组件使用第二阶段等待其他应用保存完状态。

## 7. 常见坑与经验

- 不要未经用户同意直接 `cancel()` 关机；这会制造很差的平台体验。
- 会话结束期间并不保证允许弹窗，必须准备无交互保存策略。
- `allowsErrorInteraction()` 也可能返回 `false`，错误处理不能只靠对话框。
- `restartCommand` 要包含足够恢复上下文的信息，但不要把敏感数据写进命令行。
- Windows、macOS、X11、Wayland 对会话管理支持差异很大，功能可用性不能假设一致。

## 8. 知识点覆盖

本页覆盖：会话提交、交互许可、取消关机、应用恢复策略、第二阶段保存、跨平台会话管理限制。
