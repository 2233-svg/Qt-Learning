# QDBusUnixFileDescriptor
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusUnixFileDescriptor`

## 作用定位

`QDBusUnixFileDescriptor` 用于通过 D-Bus 传递 Unix 文件描述符。它不是把 fd 数字当整数发给对方，而是使用 D-Bus/Unix 域套接字的 fd passing 能力，让接收方拿到一个可用的文件描述符副本。

这个类只在支持 Unix fd 传递的平台和连接上有意义，跨平台代码必须先检查支持情况。

## 类说明

- 头文件：`#include <QDBusUnixFileDescriptor>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承
- 平台：主要用于 Unix-like 系统；还要看连接能力 `QDBusConnection::UnixFileDescriptorPassing`

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusUnixFileDescriptor()` | 创建无效 fd 包装。 |
| `QDBusUnixFileDescriptor(int fd)` | 包装一个现有 fd，Qt 会复制/持有可传递描述符。 |
| `QDBusUnixFileDescriptor(const QDBusUnixFileDescriptor &)` | 复制 fd 包装，语义是可独立持有的描述符引用。 |
| `~QDBusUnixFileDescriptor()` | 释放内部持有的描述符。 |
| `fileDescriptor()` | 取出原生 fd；无效时返回负值。 |
| `setFileDescriptor()` | 替换内部 fd。 |
| `isValid()` | 当前是否持有有效 fd。 |
| `isSupported()` | 当前平台/Qt 构建是否支持 fd passing。 |
| `swap()` | 快速交换两个 fd 包装。 |
| `operator=` | 复制或移动赋值。 |

## 使用场景

- 把已经打开的文件、socket、memfd、pipe 交给另一个进程处理。
- 大数据传输时通过 fd 共享通道，D-Bus 只负责控制消息。
- 与 systemd、portal、沙盒服务等需要 fd passing 的接口交互。

## 常见坑与经验

- 发送前同时检查 `QDBusUnixFileDescriptor::isSupported()` 和连接的 `connectionCapabilities()`。
- 不要把 `fileDescriptor()` 返回的整数长期保存后假设包装对象销毁也没影响；先明确所有权和复制语义。
- fd passing 只在支持的传输上工作，TCP 或某些私有 bus 配置可能不支持。
- fd 是进程本地资源，接收方拿到的是另一个描述符号，不是同一个整数值。
- Windows 等平台不要把这个类当作通用文件句柄传输方案。

## 知识点覆盖

- Unix fd passing
- D-Bus 连接能力协商
- 文件描述符生命周期与所有权
- 控制消息与数据通道分离
