# QCapturableWindow
> Qt 6.11.1 · Qt Multimedia · 来自 `QCapturableWindow`

## 作用定位

`QCapturableWindow` 是可被 `QWindowCapture` 捕获的窗口描述对象。它包含窗口标识、标题/描述等信息，用来展示选择列表并把用户选择交给窗口捕获源。

## 类说明

- 头文件：`#include <QCapturableWindow>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `description()` | 可展示给用户的窗口说明。 |
| `isValid()` | 是否代表一个有效可捕获窗口。 |
| `operator==` / `operator!=` | 比较窗口描述是否相同。 |

## 使用场景
- 用 `QWindowCapture::capturableWindows()` 枚举窗口后展示 UI。
- 保存用户当前选择并传给 `QWindowCapture::setWindow()`。
- 捕获前检查窗口是否仍有效。

## 常见坑与经验
- 窗口列表是快照，用户选择后窗口可能已经关闭，start 前仍要处理失败。
- description 面向展示，不适合作为稳定唯一 ID。
- 不同平台对可捕获窗口的定义不同，系统窗口/受保护窗口可能不可见。

## 知识点覆盖

- 可捕获窗口描述
- 窗口选择 UI
- 窗口捕获有效性
