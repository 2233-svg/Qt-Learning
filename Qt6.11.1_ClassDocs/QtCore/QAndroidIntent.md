# QAndroidIntent
> Qt 6.11.1 · Qt Core · 来自 `QAndroidIntent`

## 作用定位
`QAndroidIntent` 是 Android Intent 的 Qt 封装，用于启动 Activity、Service 或传递平台数据。

## API 速查
| API | 是做什么的 |
|---|---|
| `setAction()` | 设置 Intent action。|
| `setData()` | 设置 URI 数据。|
| `putExtra()` | 传递额外参数。|
| `setComponent()` | 指定目标组件。|
| `handle()` | 获取原生 Java 对象句柄。|

## 使用场景
发起文件选择、打开系统设置、启动 Android service。

## 常见坑与经验
- action、extra key 和 URI 权限完全受 Android 平台约束；需要配套 manifest 与授权 flag。
- 不要把敏感数据明文塞进隐式 Intent。

## 知识点覆盖
Android Intent、URI、extras、组件、权限、跨应用调用。
