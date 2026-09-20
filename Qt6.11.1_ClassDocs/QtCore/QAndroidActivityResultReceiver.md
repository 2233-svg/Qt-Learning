# QAndroidActivityResultReceiver
> Qt 6.11.1 · Qt Core · 来自 `QAndroidActivityResultReceiver`

## 作用定位
`QAndroidActivityResultReceiver` 接收 Android Activity 启动后返回的结果，例如文件选择器、系统设置或第三方 Activity。

## API 速查
| API | 是做什么的 |
|---|---|
| `handleActivityResult()` | 重实现以处理 request code、result code 与 Intent 数据。|
| `QtAndroidPrivate::startActivity()` | 配合发起 Activity 请求。|

## 使用场景
从 Qt 调起 Android 文件选择界面后接收用户选择结果。

## 常见坑与经验
- Android Activity 可能在后台被系统重建；不要只依赖临时 C++ 内存状态。
- request code 要集中管理，避免不同功能冲突。

## 知识点覆盖
Android Activity、结果回调、生命周期、request code、平台桥接。
