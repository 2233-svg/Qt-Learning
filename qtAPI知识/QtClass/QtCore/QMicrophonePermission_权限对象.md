# Qt QMicrophonePermission：麦克风访问的权限描述对象

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.5  
> 头文件：`#include <QPermissions>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制、可移动的轻量权限值对象，不是 `QObject`

## 1. 它解决什么问题

录音、实时音量监测、语音聊天和语音识别都需要从麦克风获取输入音频。许多系统不会因为程序创建了音频输入对象就自动允许访问，应用必须先取得用户授权。

`QMicrophonePermission` 是 Qt 权限框架中的强类型描述对象，用来表达：

```text
应用希望访问麦克风
```

它本身不会：

- 打开麦克风设备；
- 读取音频样本；
- 开始录音；
- 弹出系统授权窗口；
- 保存或上传录音。

它只作为参数交给 `QCoreApplication::checkPermission()` 或 `QCoreApplication::requestPermission()`。真正的录音和音频采集仍由 Qt Multimedia 或其他音频后端完成。

```text
用户点击“开始录音”
          |
          v
checkPermission(QMicrophonePermission{})
          |
   Granted / Denied / Undetermined
          |
          v
requestPermission() and wait for callback
          |
          v
only after Granted: start audio capture
```

## 2. 实际使用场景

`QMicrophonePermission` 适合放在下列操作之前：

- 录制语音备忘录；
- 语音通话或语音聊天室；
- 语音识别、语音指令、听写；
- 实时音量表、音频波形、环境声音监测；
- 把麦克风输入交给 `QAudioSource`、媒体录制或第三方音频引擎。

只播放音乐、播放视频声音、输出 TTS 语音通常不需要麦克风权限，因为它们只使用扬声器输出，而不读取音频输入。

拥有 `Granted` 也不保证录音一定能开始。授权后仍可能遇到：

- 没有可用麦克风；
- 设备被其他应用独占；
- 用户在系统隐私设置中后来关闭访问；
- 音频后端、采样格式或设备初始化失败。

权限错误与设备或媒体错误应分别提示和处理。

## 3. 最小使用流程

权限请求应发生在用户点击明确功能之后，而不是应用启动时。

```cpp
#include <QCoreApplication>
#include <QPermission>
#include <QPermissions>

class RecorderController : public QObject
{
public:
    void startRecording()
    {
        const QMicrophonePermission permission;
        QCoreApplication *app = QCoreApplication::instance();

        switch (app->checkPermission(permission)) {
        case Qt::PermissionStatus::Granted:
            beginAudioCapture();
            return;

        case Qt::PermissionStatus::Denied:
            showMicrophonePermissionHelp();
            return;

        case Qt::PermissionStatus::Undetermined:
            app->requestPermission(permission, this,
                [this](const QPermission &result) {
                    if (result.status() ==
                        Qt::PermissionStatus::Granted) {
                        beginAudioCapture();
                    } else {
                        showMicrophonePermissionHelp();
                    }
                });
            return;
        }
    }

private:
    void beginAudioCapture();
    void showMicrophonePermissionHelp();
};
```

这个示例的要点：

- `checkPermission()` 只查询，不显示系统对话框；
- 只有 `Undetermined` 才发起请求；
- `requestPermission()` 异步完成，不能假定下一行已经获授权；
- 只有回调或检查结果为 `Granted` 才初始化音频输入；
- `Denied` 是正常业务分支，不是可以忽略的异常。

## 4. 三种状态的处理

| 状态 | 含义 | 正确动作 |
| --- | --- | --- |
| `Granted` | 用户已授权，或该平台不要求用户显式授权 | 尝试打开音频输入设备 |
| `Denied` | 用户拒绝，或该权限在当前平台不可访问或不适用 | 不读取麦克风，提供明确说明或设置入口 |
| `Undetermined` | 尚未取得最终授权结果 | 在主线程按需调用 `requestPermission()` |

请求完成后的回调不会再得到 `Undetermined`，只会得到 `Granted` 或 `Denied`。

不要用循环、定时器或应用启动时的批量请求反复打断用户。更合适的方式是：用户再次点击“录音”时解释功能需要麦克风，并在必要时引导其到系统设置。

## 5. 平台声明是运行时请求的前置条件

运行时 API 不能替代打包时的系统声明。缺少声明时，系统可能无法展示正确提示、拒绝授权，或使应用不符合平台要求。

### 5.1 Apple 平台

在应用 `Info.plist` 中提供用途说明：

```xml
<key>NSMicrophoneUsageDescription</key>
<string>用于录制语音备忘录。</string>
```

这段文字会展示给用户，应准确说明实际用途，例如“用于语音通话”或“用于将语音转换为文字”，而不是笼统写“需要麦克风”。

### 5.2 Android

在 `AndroidManifest.xml` 中声明：

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

自定义 Android manifest 时还应保留 Qt 项目需要的权限插入配置，确保最终打包产物包含所需声明。

不同平台的音频会话、前台服务、后台录音和隐私指示器还有额外规则；`QMicrophonePermission` 只处理“是否有权访问麦克风”这一层。

## 6. 它与 `QPermission`、`QCoreApplication` 的关系

`QMicrophonePermission` 是强类型权限描述。`QPermission` 是 Qt 在通用检查和异步结果中使用的类型擦除包装器。

平时不需要手工包装：

```cpp
QMicrophonePermission microphone;
const auto status =
    QCoreApplication::instance()->checkPermission(microphone);
```

请求完成后，回调参数是 `const QPermission &`：

```cpp
app->requestPermission(QMicrophonePermission{}, this,
    [](const QPermission &result) {
        if (result.status() != Qt::PermissionStatus::Granted)
            return;

        startCapture();
    });
```

如果一个通用回调需要确认原始权限类型，可以使用：

```cpp
const auto original = result.value<QMicrophonePermission>();
if (!original)
    return;
```

对只处理一次麦克风请求的普通代码，`result.status()` 已足够。`QMicrophonePermission` 本身没有额外配置项，因此取回 value 通常没有业务价值。

## 7. 生命周期、线程和回调上下文

`QMicrophonePermission` 是值对象：

- 可栈上临时构造；
- 可复制、移动、赋值和交换；
- 没有 `QObject` parent；
- 不拥有麦克风；
- 不缓存“当前是否授权”的全局状态；
- 析构不会撤销系统已授予权限，也不会取消已发起的系统请求。

真正有线程要求的是 `requestPermission()`：

- 只能从主线程调用；
- 无 context 的回调生命周期由调用方自行保证；
- 带 `QObject *context` 的重载会让回调在 context 所在线程执行；
- 若 context 在请求完成前销毁，回调不会被调用。

因此涉及页面、控制器或对象成员的代码优先使用 context 重载：

```cpp
app->requestPermission(QMicrophonePermission{}, this,
    [this](const QPermission &result) {
        if (result.status() == Qt::PermissionStatus::Granted)
            beginAudioCapture();
    });
```

音频编码、波形分析等耗时工作可以在工作线程进行，但“请求系统权限”这一动作应留在主线程。

## 8. 请求时机与库代码边界

麦克风权限属于高敏感权限。请求应紧贴用户动作：

```text
点击录音 -> 简要说明 -> 系统请求 -> 获准后录音
```

不建议：

- 第一次启动时就请求；
- 因为将来可能用到就预先请求；
- 同时请求相机、位置、通讯录和麦克风；
- 由底层库在不清楚产品文案的情况下直接弹系统对话框。

合理分工：

- UI 或业务入口：解释目的并发起请求；
- 库：用 `checkPermission()` 验证前置条件；
- 未授权时：库通过返回值、错误对象或状态通知上层；
- 获授权后：音频模块再创建 `QAudioSource` 或其他采集对象。

## 9. 常见错误

### 9.1 构造 `QMicrophonePermission` 后期待弹窗

构造只产生一个描述值。必须调用 `QCoreApplication::requestPermission()` 才会请求系统授权。

### 9.2 `Undetermined` 时直接开始录音

它表示当前没有最终授权结果，不能当作临时允许。请求完成后再根据回调决定。

### 9.3 只播放音频却请求麦克风

扬声器输出不需要读取麦克风。无关请求会降低用户信任，也可能影响审核。

### 9.4 把 `Granted` 当成设备可用保证

权限只解决授权。设备不存在、被占用或音频后端失败仍需由媒体层处理。

### 9.5 缺少 `Info.plist` 或 Android manifest 声明

运行时请求和构建期声明缺一不可。修复项目配置，而不是反复调用 `requestPermission()`。

### 9.6 在工作线程请求

Qt 规定权限请求只能从主线程发起。后台任务应通知界面或应用主线程处理授权。

### 9.7 忽略 `Denied`

拒绝是可预期状态，也可能意味着平台不支持或不允许该能力。应停止采集并提供清晰降级体验。

## 10. 逐项 API 说明

`QMicrophonePermission` 是 Qt 的 minimal permission 类型，没有“录音参数”或“访问范围”成员；下列 API 都是值语义操作，不触发系统调用。

| API | 语义 | 关键边界 |
| --- | --- | --- |
| `QMicrophonePermission()` | 构造麦克风权限描述 | 不检查、不请求、不授予权限 |
| `QMicrophonePermission(const QMicrophonePermission &other) noexcept` | 复制权限描述 | 复制不产生新请求，也不改变系统授权 |
| `QMicrophonePermission(QMicrophonePermission &&other) noexcept` | 移动权限描述 | moved-from 对象只应析构、赋值或重新使用 |
| `~QMicrophonePermission()` | 销毁描述对象 | 不撤销授权，不关闭麦克风 |
| `operator=(const QMicrophonePermission &other) noexcept` | 复制赋值 | 仅改变本地值 |
| `operator=(QMicrophonePermission &&other) noexcept` | 移动赋值 | 不要依赖移动后源对象的旧状态 |
| `void swap(QMicrophonePermission &other) noexcept` | 交换两个权限对象 | 主要用于容器和泛型算法；不触发系统请求 |

## 11. 相关但不属于本类的关键 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 查询 | `QCoreApplication::checkPermission(permission)` | 查询当前麦克风授权状态 | 只查询，不显示对话框 |
| 请求 | `QCoreApplication::requestPermission(permission, functor)` | 异步请求授权 | 只能在主线程调用；自行保证回调捕获对象仍有效 |
| 请求 | `QCoreApplication::requestPermission(permission, context, functor)` | 带 QObject 上下文的异步请求 | context 销毁后不调用回调；回调在 context 线程执行 |
| 结果 | `Qt::PermissionStatus::Undetermined` | 尚未获得最终选择 | 请求后回调不会返回该状态 |
| 结果 | `Qt::PermissionStatus::Granted` | 已获准，或平台无需授权 | 仍需处理麦克风设备或后端失败 |
| 结果 | `Qt::PermissionStatus::Denied` | 被拒绝、不可访问或不适用 | 不得继续访问音频输入 |
| 包装 | `QPermission::status()` | 读取异步请求结果 | 回调中首先判断是否 `Granted` |
| 包装 | `QPermission::value<QMicrophonePermission>()` | 尝试取回原始强类型描述 | 类型不匹配返回 `std::nullopt`；多数单一请求不需要 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 描述 | `QMicrophonePermission{}` | 表达“需要访问麦克风” | 本身不会弹窗或开始录音 |
| 查询 | `checkPermission()` | 读取当前授权状态 | `Undetermined` 后再考虑请求 |
| 请求 | `requestPermission()` | 异步取得最终授权结果 | 仅主线程调用；优先提供 context |
| 成功 | `Granted` | 可以尝试启动音频输入 | 不是设备可用保证 |
| 拒绝 | `Denied` | 停止输入访问并降级处理 | 不能继续初始化录音 |
| 配置 | `NSMicrophoneUsageDescription` | Apple 用途声明 | 打包前必须配置 |
| 配置 | `android.permission.RECORD_AUDIO` | Android 权限声明 | 写入最终 manifest |
| 值语义 | 复制、移动、赋值、`swap()` | 管理权限描述值 | 不改变系统授权或请求状态 |

## 13. 一句话总结

`QMicrophonePermission` 只描述应用需要麦克风：在用户触发录音、监听或语音功能时从主线程先检查、未决定再异步请求，获准后才启动音频输入，并同时保证 Apple 与 Android 的构建期声明完整。
