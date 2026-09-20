# QHostAddress
> Qt 6.11.1 · Qt Network · 来自 `QHostAddress`

## 作用定位
`QHostAddress` 是 IPv4/IPv6 地址的值类型，表示网络端点地址而非主机名、端口或连通性。

## API 速查
| API | 是做什么的 |
|---|---|
| `setAddress()` | 从字符串或协议地址设置值。|
| `toString()` | 转为可显示地址文本。|
| `protocol()` | 判断 IPv4、IPv6 或未知。|
| `isLoopback()` / `isMulticast()` | 判断特殊地址类别。|
| `isInSubnet()` | 判断地址是否落在网络前缀中。|
| `parseSubnet()` | 解析 CIDR 子网文本。|

## 使用场景
校验配置中的监听地址、过滤私有网段、为 socket 指定数值地址。

## 常见坑与经验
- DNS 名称不是 `QHostAddress`；先异步解析。
- IPv6 文本有多种等价写法，比较对象而非字符串。

## 知识点覆盖
IPv4、IPv6、CIDR、环回、多播、地址规范化。
