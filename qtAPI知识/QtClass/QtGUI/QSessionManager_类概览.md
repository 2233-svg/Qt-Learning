# Qt QSessionManager：会话关闭与状态保存协商

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSessionManager>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QObject -> QSessionManager`  
> 类型定位：桌面会话管理器交互对象

## 1. 它解决什么问题

`QSessionManager` 是应用与操作系统或桌面会话管理器之间的协商接口。它主要处理三类任务：

- 用户注销、关机或会话检查点到来时，应用提交未保存数据；
- 应用保存足够的信息，以便下一次会话恢复窗口和文档状态；
- 应用在得到许可后向用户询问是否保存，或在保存失败且用户确认后取消关闭流程。

它不是普通的“窗口关闭事件”，也不是应用退出 API。会话管理器可能在真正退出前向应用发出 `QGuiApplication::commitDataRequest()` 或 `QGuiApplication::saveStateRequest()`，应用必须在这些信号对应的槽中使用传入的 `QSessionManager &`。

`QSessionManager` 的构造函数和析构函数都不是应用 API。对象由 `QGuiApplication` 创建并管理，应用只在会话请求的回调期间借用它。Qt 还可能在编译时定义 `QT_NO_SESSIONMANAGER`，此时该类不可用。

## 2. 构建与包含

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

源码：

```cpp
#include <QGuiApplication>
#include <QSessionManager>
#include <QSettings>
```

如果在保存前显示 `QMessageBox` 或其他控件，需要额外链接 `Qt6::Widgets`。

qmake 工程使用：

```qmake
QT += gui
```

会话管理支持是平台相关能力。Qt 文档指出，完整的“保存并在下一会话恢复”机制目前主要由 X11 会话管理器支持；Windows 等平台通常至少提供优雅注销时的提交数据机会，而不同桌面环境的支持程度可能不同。

## 3. 最小使用方式

### 3.1 处理提交数据请求

```cpp
#include <QGuiApplication>
#include <QSessionManager>

class ApplicationController : public QObject
{
    Q_OBJECT

public:
    using QObject::QObject;

public slots:
    void commitData(QSessionManager &manager)
    {
        if (!hasUnsavedChanges())
            return;

        if (!manager.allowsInteraction()) {
            // 无权弹出询问框时，执行应用预先定义的无交互策略。
            return;
        }

        const bool saveSucceeded = saveAllDocuments();
        manager.release();

        if (!saveSucceeded)
            manager.cancel();
    }

private:
    bool hasUnsavedChanges() const;
    bool saveAllDocuments();
};

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    ApplicationController controller;

    QObject::connect(&app, &QGuiApplication::commitDataRequest,
                     &controller, &ApplicationController::commitData);
    return app.exec();
}
```

真实应用通常在 `allowsInteraction()` 返回 `true` 后显示保存、丢弃和取消对话框：

```cpp
if (manager.allowsInteraction()) {
    const UserChoice choice = askSaveDiscardCancel();
    manager.release();

    if (choice == UserChoice::Cancel)
        manager.cancel();
    else if (choice == UserChoice::Save && !saveAllDocuments())
        manager.cancel();
}
```

交互完成后尽快调用 `release()`，让其他应用有机会获得会话管理器的交互许可。不要在没有许可时直接显示模态对话框。

### 3.2 保存可恢复状态

```cpp
void ApplicationController::saveState(QSessionManager &manager)
{
    QSettings settings;
    settings.beginGroup(QStringLiteral("session/") + manager.sessionId());
    settings.setValue("openDocuments", openDocumentPaths());
    settings.setValue("activeDocument", activeDocumentPath());
    settings.setValue("windowGeometry", windowGeometry());
    settings.endGroup();
}
```

连接到：

```cpp
QObject::connect(&app, &QGuiApplication::saveStateRequest,
                 &controller, &ApplicationController::saveState);
```

恢复通常发生在 `main()` 中：检查 `QGuiApplication::isSessionRestored()`，再用 `QGuiApplication::sessionId()` 访问保存的数据。会话 ID 应作为状态数据的命名空间，避免不同会话之间发生冲突。

## 4. 核心使用模型

### 4.1 只在两个会话信号的槽中访问

Qt 文档明确规定，`QSessionManager` 只能在 `QGuiApplication::commitDataRequest()` 和 `QGuiApplication::saveStateRequest()` 调用的槽中访问。不要在普通按钮槽、定时器、构造函数或退出后的异步回调中保存并使用这个引用。

两个信号职责不同：

- `commitDataRequest`：会话管理器要求应用提交未保存数据，例如把文档写入永久存储；
- `saveStateRequest`：会话管理器要求应用保存下次会话可恢复的应用状态。

同一次会话关闭流程可能触发其中一个或两个信号，具体取决于平台和会话管理器。

### 4.2 交互许可是一次会话资源

在提交或保存回调中，应用原则上不能自行弹出用户界面。应先调用：

- `allowsInteraction()`：请求普通用户交互；
- `allowsErrorInteraction()`：保存或提交发生错误、确实需要向用户说明时请求更高优先级的交互。

返回 `false` 时必须采用无交互策略，例如自动保存、放弃本次保存并记录错误，或等待会话管理器后续处理。Qt 不强制阻止对话框，但会话管理器可能拒绝应用的交互请求。

返回 `true` 后完成对话框或错误提示，应调用 `release()` 释放会话管理器的交互信号量。进程退出时信号量会隐式释放，但显式释放能让其他应用及时获得机会。

### 4.3 `cancel()` 只用于用户确认取消或无法安全提交

`cancel()` 请求会话管理器取消关闭流程。它不是普通的“保存失败自动退出”按钮，也不应在没有询问用户的情况下随意调用。

典型逻辑是：

1. 取得交互许可；
2. 询问用户；
3. 如果用户选择取消，调用 `cancel()`；
4. 如果用户选择保存但保存失败，向用户说明并在确认后调用 `cancel()`；
5. 交互完成后释放信号量。

## 5. 实际使用场景

### 5.1 优雅注销

连接 `commitDataRequest`，保存文档和数据库事务，必要时询问用户。Windows 等主要提供优雅注销能力的平台，通常首先需要实现这个路径。

### 5.2 X11 会话恢复

连接 `saveStateRequest`，把打开文档、活动标签、窗口布局和应用内部模式写入 `QSettings`、数据库或文件。下一次启动时用 `QGuiApplication::isSessionRestored()` 和 `sessionId()` 找回对应数据。

### 5.3 保存失败处理

正常交互许可不足以表达“必须向用户报告错误”时，可以尝试 `allowsErrorInteraction()`。它可能比普通交互请求更容易获准，但仍不保证成功。返回 `false` 时不能强行弹出错误对话框。

### 5.4 应用重启策略

桌面环境可能希望应用在下一会话重启，或者某个常驻工具在不运行时自动启动。通过 `setRestartHint()` 指定偏好，并通过 `setRestartCommand()` 提供完整重启命令。

### 5.5 两阶段会话管理

窗口管理器等需要观察其他应用在第一阶段保存后的结果时，可以调用 `requestPhase2()` 请求第二阶段。之后 `commitDataRequest` 或 `saveStateRequest` 会再次调用，槽中可用 `isPhase2()` 区分当前阶段。

第二阶段不是“让当前函数暂停直到所有其他应用完成”。它是会话管理器安排的后续回调，而且另一个应用的第二阶段可能在你的第二阶段之前、同时或之后发生。

## 6. 会话关闭的正确处理流程

### 6.1 `commitDataRequest` 的建议流程

```text
收到 commitDataRequest(manager)
    -> 判断是否有未保存数据
    -> 需要询问时调用 allowsInteraction()
    -> 获准后显示对话框
    -> 保存或丢弃
    -> 对话框结束后调用 release()
    -> 用户取消或保存失败且确认取消时调用 cancel()
```

如果无权交互，不应把对话框放到另一个线程、定时器或延迟回调中绕过限制。应执行明确的无交互策略，并确保数据一致性。

### 6.2 `saveStateRequest` 的建议流程

保存恢复状态通常不应依赖用户操作。状态写入要尽量快速、可重复和幂等，并使用 `sessionId()` 作为键的一部分。不要把大量状态塞进重启命令行，命令行长度有限；应使用 `QSettings`、临时文件或数据库。

### 6.3 恢复状态的时机

恢复应在应用启动阶段完成，而不是等到下一次 `saveStateRequest`。典型检查顺序是：

```cpp
QGuiApplication app(argc, argv);

if (app.isSessionRestored()) {
    QSettings settings;
    settings.beginGroup(QStringLiteral("session/") + app.sessionId());
    restoreDocuments(settings);
    settings.endGroup();
}
```

`QGuiApplication::sessionId()` 与 `QSessionManager::sessionId()` 都描述当前会话上下文；在会话信号的槽中使用 manager 版本，在启动恢复逻辑中使用 application 版本。

## 7. 重启命令与 `RestartHint`

### 7.1 `RestartIfRunning`

如果会话关闭时应用仍在运行，希望下一次会话启动它。这是默认提示，适合普通桌面应用。

### 7.2 `RestartAnyway`

无论关闭时应用是否仍在运行，都希望下一次会话启动它。适合会话启动后执行一次任务的工具类应用。

### 7.3 `RestartImmediately`

希望在应用不运行时立即启动它。它适合需要持续存在的工具，但是否有效取决于会话管理器。

### 7.4 `RestartNever`

明确表示不希望被会话管理器自动重启。

### 7.5 `setRestartCommand()` 的参数约定

命令使用 `QStringList` 的参数形式，而不是一整条需要 shell 解析的字符串。第一个元素通常是可执行文件，后续元素是独立参数。Qt 文档特别要求重启命令包含 `-session` 选项，否则 `QGuiApplication` 无法判断应用是否从会话恢复以及当前会话 ID：

```cpp
manager.setRestartCommand({
    applicationFilePath,
    QStringLiteral("-session"),
    manager.sessionId()
});
```

实际命令还要考虑平台启动器、工作目录、权限和应用自己的命令行解析。不要把包含空格的整条 shell 命令作为一个 `QString` 元素，也不要把大量恢复数据直接塞进命令行。

## 8. 会话 ID、会话 key 与对象属性

### 8.1 `sessionId()`

返回当前会话的应用标识。保存恢复数据时，可把它作为 `QSettings` 分组名、数据库命名空间或临时文件名的一部分。应避免把它当作用户账号 ID 或设备永久 ID。

### 8.2 `sessionKey()`

返回会话管理器提供的会话 key。它是会话协议的一部分，应用通常只在需要与对应会话管理器协作时读取，不应擅自推断其格式或把它当作加密密钥。

### 8.3 `setManagerProperty()`

向会话管理器设置一个字符串或字符串列表属性。它主要面向 Unix/X11 上更复杂的会话管理器和协议扩展。属性名和值的解释不是 Qt 跨平台通用业务协议，使用时必须查目标会话管理器文档。

它有两个重载：

```cpp
manager.setManagerProperty(QStringLiteral("property"),
                           QStringLiteral("value"));

manager.setManagerProperty(QStringLiteral("listProperty"),
                           QStringList{QStringLiteral("one"),
                                       QStringLiteral("two")});
```

## 9. 两阶段会话管理

`requestPhase2()` 请求会话管理器在大多数或全部其他应用完成第一阶段后，再次调用本应用的提交或保存槽。`isPhase2()` 用来判断当前回调是否属于第二阶段。

常见适用场景是窗口管理器需要在其他应用完成会话保存后，再记录这些应用窗口的最终布局。普通文档应用通常不需要第二阶段。

第二阶段仍然遵守交互许可规则。不要假设第二阶段一定在所有其他应用之后执行，也不要把它当成一个可以阻塞等待全局完成的同步屏障。

## 10. 生命周期、所有权和线程

### 10.1 不要保存 `QSessionManager &`

信号槽中的 manager 引用只在当前回调期间有效。不要保存引用、裸指针或把它捕获到延迟 lambda 中：

```cpp
// 错误思路：回调返回后 manager 可能已失效。
QSessionManager *savedManager = &manager;
QTimer::singleShot(0, this, [savedManager] {
    savedManager->release();
});
```

如果需要稍后执行保存，应在会话槽中完成必要的同步操作，或复制 `sessionId()`、命令和业务数据到自己的对象中。不能把“稍后再调用 manager”作为异步控制流。

### 10.2 不要创建或删除对象

构造函数和析构函数位于类的私有区域，应用不能直接构造或删除 `QSessionManager`。它由 `QGuiApplication` 在会话管理回调中提供。

### 10.3 在 GUI 线程完成会话处理

提交数据和显示交互对话框属于 GUI 线程工作。耗时的文件写入可以交给工作对象，但会话槽必须设计好同步边界，确保在槽返回前会话管理器得到明确结果，不能启动一个尚未完成的异步保存就直接返回。

### 10.4 线程安全不是会话协议

即使保存数据的容器本身可以跨线程使用，`allowsInteraction()`、`release()`、`cancel()` 和阶段查询仍属于会话协议操作，应在会话信号对应的线程和回调中完成。

## 11. 常见误区与排查顺序

### 11.1 在普通退出路径使用 `QSessionManager`

普通用户点击窗口关闭按钮时，通常应使用窗口关闭事件和自己的文档保存流程。`QSessionManager` 只在会话管理器发出的提交或保存信号中可用。

### 11.2 未取得许可就弹框

`commitDataRequest` 和 `saveStateRequest` 中默认没有用户交互许可。先检查 `allowsInteraction()` 或错误场景下的 `allowsErrorInteraction()`；返回 `false` 时不要强行显示模态对话框。

### 11.3 取得许可后忘记 `release()`

会话管理器的交互信号量会在应用退出时隐式释放，但长时间持有会阻塞其他应用的会话交互。对话框或错误提示结束后尽快调用 `release()`。

### 11.4 任意调用 `cancel()`

`cancel()` 会尝试取消整个会话关闭流程。只有在用户明确选择取消，或用户确认保存失败后中止时才调用；不要把普通异常、日志写入失败或开发者不喜欢的退出路径都变成 `cancel()`。

### 11.5 只实现 `commitDataRequest`，却期待状态恢复

提交未保存数据和保存下次会话状态是两种不同任务。需要恢复打开文档或窗口布局时，还要实现 `saveStateRequest`，并在启动时检查 `isSessionRestored()`。

### 11.6 把会话状态都写入重启命令

命令行长度有限，也容易受到转义和隐私问题影响。使用 `QSettings`、临时文件或数据库保存实际状态，命令行只携带 `-session` 和必要的会话标识。

### 11.7 把 `sessionKey()` 当作安全密钥

它是会话协议字段，不应未经协议文档说明用于加密、认证或用户身份识别。

### 11.8 假设所有平台都支持完整恢复

会话管理器能力由平台和桌面环境决定。应用应让优雅提交在没有完整恢复能力时也能工作，并把恢复功能视为平台可用时的增强。

### 11.9 忽略 `QT_NO_SESSIONMANAGER`

如果 Qt 构建配置定义了 `QT_NO_SESSIONMANAGER`，相关头文件和 API 不可用。跨配置构建时，应让会话管理代码具有条件编译或由应用构建系统明确要求该能力。

## 12. 逐项 API 说明

### 成员类型

#### `enum QSessionManager::RestartHint`

指定会话关闭后应用的自动重启偏好。默认值是 `RestartIfRunning`。

| 枚举值 | 数值 | 语义 |
| --- | ---: | --- |
| `RestartIfRunning` | `0` | 如果关闭时应用仍在运行，希望下一次会话启动 |
| `RestartAnyway` | `1` | 无论关闭时是否运行，都希望下一次会话启动 |
| `RestartImmediately` | `2` | 应用不运行时希望立即启动 |
| `RestartNever` | `3` | 不希望被自动重启 |

这是提示，不是所有平台都强制执行的命令。

### 会话标识

#### `QString QSessionManager::sessionId() const`

返回当前会话标识。适合将保存状态与某个会话关联。它的格式由会话管理器决定，不应解析其内部结构。

#### `QString QSessionManager::sessionKey() const`

返回当前会话 key。它是会话管理协议的值，不应未经协议约定当成密码、加密密钥或持久 ID。

### 交互权限与关闭控制

#### `bool QSessionManager::allowsInteraction()`

请求普通用户交互许可。只有在 `commitDataRequest` 或 `saveStateRequest` 的槽中调用才符合文档使用边界。返回 `true` 后可以显示保存或丢弃对话框；完成交互后应调用 `release()`。

返回 `false` 时不能强行交互，应采用无交互保存、放弃或错误记录策略。

#### `bool QSessionManager::allowsErrorInteraction()`

请求用于报告保存错误的交互许可。会话管理器可能给这类请求更高优先级，但仍可能返回 `false`。它不是无条件显示错误对话框的通行证。

#### `void QSessionManager::release()`

释放在交互阶段占用的会话管理器交互信号量。完成对话框或错误提示后调用，让其他应用有机会交互。应用退出时会隐式释放，但不应依赖这一点。

#### `void QSessionManager::cancel()`

请求会话管理器取消关闭流程。应在用户明确选择取消，或用户确认无法安全保存并要求中止时使用。不要把它当作普通异常处理或应用退出接口。

### 重启配置

#### `void QSessionManager::setRestartHint(QSessionManager::RestartHint hint)`

设置自动重启提示。它只表达应用偏好，最终行为取决于会话管理器。通常在会话请求槽中设置，或在应用生命周期中根据当前模式设置。

#### `QSessionManager::RestartHint QSessionManager::restartHint() const`

返回当前自动重启提示。默认是 `RestartIfRunning`。

#### `void QSessionManager::setRestartCommand(const QStringList &command)`

设置会话管理器用于重启应用的参数列表。列表第一个元素通常是可执行文件，后续元素是独立参数。命令必须包含 `-session` 选项，否则 Qt 无法识别会话恢复和当前会话标识。

这是参数数组，不是 shell 字符串；不要把整条命令拼成一个元素，也不要将完整恢复状态塞入命令行。

#### `QStringList QSessionManager::restartCommand() const`

返回当前重启命令参数列表。返回值可用于诊断或在会话回调中调整命令；不要假设列表一定非空或包含平台所需的全部启动环境。

#### `void QSessionManager::setDiscardCommand(const QStringList &command)`

设置会话管理器在需要放弃或丢弃会话状态时使用的命令列表。它主要面向更复杂的 Unix/X11 会话管理器。参数按 `QStringList` 传递，具体执行时机和解释由平台协议决定。

#### `QStringList QSessionManager::discardCommand() const`

返回当前丢弃命令参数列表。该能力和命令执行语义是平台相关的，不应把它当作应用内部的“删除文件”命令。

### 会话管理器扩展

#### `void QSessionManager::setManagerProperty(const QString &name, const QString &value)`

以单个字符串值设置会话管理器属性。属性名和值的标准由目标会话管理器或协议决定；Qt 不为任意名称提供跨平台语义。

#### `void QSessionManager::setManagerProperty(const QString &name, const QStringList &value)`

以字符串列表值设置会话管理器属性。它与单字符串重载表达不同的协议数据形状；调用重载不明确时，应显式构造 `QStringList`。

### 两阶段管理

#### `bool QSessionManager::isPhase2() const`

返回当前会话请求是否处于第二阶段。只有在会话管理器再次调用提交或保存槽时才有实际意义。

#### `void QSessionManager::requestPhase2()`

请求会话管理器在第一阶段完成后再次调用本应用的会话槽。适合需要观察其他应用保存结果的特殊应用，例如窗口管理器；普通应用通常不需要。

第二阶段不是全局同步屏障，其他应用的第二阶段可能和本应用重叠。

### 继承自 `QObject` 的常用边界

`QSessionManager` 是 `QObject`，但它的主要 API 不是通过普通对象生命周期使用的。`parent()`、`thread()`、`deleteLater()`、信号槽连接等基类能力不改变“只能在会话请求槽中使用 manager”的协议限制。

不要把 `QObject` 的常规可延迟销毁习惯套到 `QSessionManager` 上，也不要尝试通过 `setParent()` 改变其所有权。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 生命周期 | `QSessionManager` 构造函数 | 由 `QGuiApplication` 创建会话管理对象 | 构造函数私有，应用不能自行创建 |
| 生命周期 | `~QSessionManager()` | 销毁会话管理对象 | 析构函数私有，不要删除信号槽传入的对象 |
| 枚举 | `enum RestartHint` | 定义自动重启偏好 | 只是平台提示，不保证所有会话管理器强制执行 |
| 枚举值 | `RestartIfRunning` | 运行中才希望下一会话重启 | 默认值 |
| 枚举值 | `RestartAnyway` | 无论是否运行都希望下一会话启动 | 适合启动后执行任务的工具 |
| 枚举值 | `RestartImmediately` | 应用不运行时希望立即启动 | 平台支持情况不同 |
| 枚举值 | `RestartNever` | 不希望自动重启 | 只是应用偏好 |
| 标识 | `sessionId() const` | 获取当前会话标识 | 用于保存状态命名空间；不要解析格式 |
| 标识 | `sessionKey() const` | 获取会话协议 key | 不是密码、加密密钥或永久 ID |
| 交互 | `allowsInteraction()` | 请求普通用户交互许可 | 只能在两个会话请求槽中用；返回 false 不得强行弹框 |
| 交互 | `allowsErrorInteraction()` | 请求报告错误的交互许可 | 优先级可能更高，但仍可能返回 false |
| 交互 | `release()` | 释放交互信号量 | 交互结束后尽快调用 |
| 关闭 | `cancel()` | 请求取消会话关闭 | 仅在用户明确取消或确认无法安全保存时调用 |
| 重启 | `setRestartHint(RestartHint hint)` | 设置自动重启偏好 | 最终行为由会话管理器决定 |
| 重启 | `restartHint() const` | 读取自动重启偏好 | 默认是 `RestartIfRunning` |
| 重启 | `setRestartCommand(const QStringList &command)` | 设置重启参数列表 | 必须包含 `-session`；按参数列表传递，不是 shell 字符串 |
| 重启 | `restartCommand() const` | 读取重启参数列表 | 平台可能提供空列表或额外约束 |
| 丢弃 | `setDiscardCommand(const QStringList &command)` | 设置丢弃会话状态的命令 | 主要面向 Unix/X11 扩展；执行语义由平台决定 |
| 丢弃 | `discardCommand() const` | 读取丢弃命令列表 | 不是应用内部删除文件命令 |
| 扩展 | `setManagerProperty(const QString &name, const QString &value)` | 设置单字符串会话管理器属性 | 名称和值由目标协议定义 |
| 扩展 | `setManagerProperty(const QString &name, const QStringList &value)` | 设置字符串列表会话管理器属性 | 重载选择要明确；不提供跨平台通用语义 |
| 阶段 | `isPhase2() const` | 判断是否为第二阶段回调 | 只在会话管理器再次回调时有意义 |
| 阶段 | `requestPhase2()` | 请求第二阶段会话回调 | 不是等待所有其他应用完成的同步屏障 |
| 应用信号 | `QGuiApplication::commitDataRequest(QSessionManager &)` | 请求应用提交未保存数据 | 槽中默认不可交互，需先申请许可 |
| 应用信号 | `QGuiApplication::saveStateRequest(QSessionManager &)` | 请求应用保存下次会话状态 | 恢复通常在下一次启动时完成 |
| 应用状态 | `QGuiApplication::isSessionRestored()` | 判断本次启动是否来自会话恢复 | 与应用级 `sessionId()` 一起使用 |
| 应用状态 | `QGuiApplication::sessionId()` | 启动和恢复逻辑中获取会话标识 | 会话槽中也可使用 manager 的同名 API |
| QObject 边界 | `QObject::setProperty()` | 设置 QObject 动态属性 | 文档中的 manager property 与 QObject 动态属性不是同一个协议 |
| QObject 边界 | `QObject::deleteLater()` | 请求延迟销毁 QObject | 不适合释放 QSessionManager；所有权由 Qt 会话流程管理 |

---

### 一句话总结

`QSessionManager` 是会话关闭期间的协议对象：在 `commitDataRequest` 或 `saveStateRequest` 槽中提交数据、保存恢复状态和协商交互；先申请交互许可，结束后释放，只有在用户确认取消或无法安全保存时才调用 `cancel()`，并始终把平台差异和 manager 引用的短生命周期放在心上。
