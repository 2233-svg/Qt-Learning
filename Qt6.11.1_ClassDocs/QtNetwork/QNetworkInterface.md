# QNetworkInterface
> Qt 6.11.1 · Qt Network · 来自 `QNetworkInterface`

## 作用定位
`QNetworkInterface` 描述本机网络接口及其地址、MAC、标志和索引。

## API 速查
| API | 是做什么的 |
|---|---|
| `allInterfaces()` | 枚举本机接口。|
| `interfaceFromName()` / `interfaceFromIndex()` | 查找特定接口。|
| `addressEntries()` | 读取接口地址列表。|
| `flags()` | 查询 up、running、loopback、multicast 等状态。|
| `hardwareAddress()` | 读取 MAC 地址文本。|
| `index()` | 获取系统接口索引。|

## 使用场景
选择多播加入接口、显示网络诊断、避免把 loopback 误当作 LAN 地址。

## 常见坑与经验
- 网卡 up 不代表能访问互联网；还需路由、DNS 和连通性检查。
- MAC 地址不是稳定设备身份，虚拟网卡与隐私策略都会改变它。

## 知识点覆盖
多网卡、MAC、接口标志、多播、网络诊断、身份边界。
