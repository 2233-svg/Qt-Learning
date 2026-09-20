# QWinEventNotifier
> Qt 6.11.1 · Qt Core · 来自 `QWinEventNotifier`
## 作用定位
`QWinEventNotifier` 将 Windows HANDLE 事件对象接入 Qt 事件循环，在句柄变为 signaled 时发出通知。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 指定 Windows 事件 HANDLE。 |
| `setHandle()` / `handle()` | 设置或查询句柄。 |
| `setEnabled()` | 开关通知。 |
| `activated` | 句柄触发时发出。 |
## 使用场景
把 Win32 重叠 I/O、进程事件或自定义事件对象转成 Qt 回调。
## 常见坑与经验
- 仅 Windows 平台可用，跨平台代码要隔离。
- 句柄关闭前禁用或销毁 notifier。
- 回调中按 Win32 语义重置事件，避免重复触发。
## 知识点覆盖
Windows HANDLE、事件循环、平台条件编译、句柄生命周期、异步 I/O。
