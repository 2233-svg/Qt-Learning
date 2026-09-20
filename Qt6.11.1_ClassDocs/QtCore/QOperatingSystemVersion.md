# QOperatingSystemVersion
> Qt 6.11.1 · Qt Core · 来自 `QOperatingSystemVersion`

## 作用定位
`QOperatingSystemVersion` 表示运行时操作系统类型与版本号，用于有针对性地启用平台能力或规避已知系统限制。

## API 速查
| API | 是做什么的 |
|---|---|
| `current()` | 获取当前运行系统版本。|
| `type()` | 查询 Android、Windows、macOS、iOS 等类型。|
| `majorVersion()` / `minorVersion()` | 读取版本组成。|
| `microVersion()` | 读取补丁级版本。|
| `isAnyOfType()` | 判断是否属于一组系统类型。|
| 比较运算符 | 与已知系统版本常量比较。|

## 使用场景
根据平台版本选择 API 调用、兼容旧系统限制、记录诊断环境。

## 常见坑与经验
- 版本判断应是最后的兼容手段；优先进行能力检测或尝试后处理失败。
- 厂商版本号不总能直接映射到功能可用性，尤其是 Android 定制系统和补丁回移。
- 不要因版本字符串拼接来判断系统，使用类型和数值比较。

## 知识点覆盖
平台检测、版本比较、能力检测、兼容性、诊断、移动/桌面差异。
