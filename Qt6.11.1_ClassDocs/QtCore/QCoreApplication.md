# QCoreApplication
> Qt 6.11.1 · Qt Core · 来自 `QCoreApplication`

## 作用定位
`QCoreApplication` 是非 GUI Qt 程序的应用对象，保存全局应用元数据、命令行参数、翻译器，并驱动主线程事件循环。Widgets/Quick 应用分别使用其派生应用类。

## API 速查
| API | 是做什么的 |
|---|---|
| `exec()` | 进入主事件循环，返回退出码。|
| `quit()` / `exit()` | 请求或设置事件循环退出。|
| `arguments()` | 读取启动参数。|
| `applicationName()` 等 | 设置应用标识信息。|
| `translate()` | 执行翻译查找。|
| `installTranslator()` | 安装翻译器。|
| `postEvent()` | 异步向 QObject 投递事件。|
| `sendEvent()` | 同步发送事件。|
| `aboutToQuit()` | 应用即将退出时通知。|

## 使用场景
命令行服务、后台任务或测试程序创建一个 `QCoreApplication`，完成初始化后调用 `exec()`；需要 GUI 时改用 `QGuiApplication` 或 `QApplication`。

## 常见坑与经验
- `quit()` 在事件循环尚未启动前调用不一定能达到预期；从启动逻辑退出优先返回错误码。
- `aboutToQuit()` 中适合停止异步工作，不适合启动需要长期事件循环的新任务。
- `sendEvent()` 可重入；跨线程通信应使用 signal/slot 或 `postEvent()`。

## 知识点覆盖
应用生命周期、事件循环、退出码、命令行、翻译、事件投递、线程通信。
