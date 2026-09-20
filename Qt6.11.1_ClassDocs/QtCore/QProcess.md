# QProcess
> Qt 6.11.1 · Qt Core · 来自 `QProcess`

## 作用定位
`QProcess` 异步启动并控制外部进程，提供标准输入、标准输出、标准错误、退出状态、工作目录和环境变量管理。

## API 速查
| API | 是做什么的 |
|---|---|
| `setProgram()` / `setArguments()` | 分别设置可执行程序和参数列表。|
| `start()` | 异步启动进程。|
| `startDetached()` | 启动不受当前对象管理的独立进程。|
| `readyReadStandardOutput()` | 标准输出有数据时通知。|
| `readyReadStandardError()` | 标准错误有数据时通知。|
| `readAllStandardOutput()` | 读取已缓冲标准输出。|
| `finished()` | 进程退出时通知退出码和状态。|
| `terminate()` / `kill()` | 请求优雅结束或强制终止。|
| `setProcessEnvironment()` | 设置子进程环境变量。|
| `setWorkingDirectory()` | 设置子进程工作目录。|

## 使用场景
调用编译器、Git、媒体工具、命令行转换器或受控后台辅助程序，并以信号方式读取输出和退出结果。

## 常见坑与经验
- 将程序路径和每个参数分开传递；不要把用户输入拼进 shell 命令字符串，否则会产生命令注入。
- `finished()` 不代表业务成功，需同时检查 `exitStatus()`、`exitCode()` 和工具输出。
- 大量输出若不持续读取，子进程可能因管道缓冲填满而阻塞。
- `kill()` 会跳过进程自身清理；优先 `terminate()` 并设置超时回退。

## 知识点覆盖
子进程、异步 I/O、标准输出错误、退出码、环境变量、命令注入、背压、取消。
