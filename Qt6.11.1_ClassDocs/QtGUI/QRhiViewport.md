# QRhiViewport
> Qt 6.11.1 · Qt GUI [Private] · 来自 `QRhiViewport`

## 1. 先建立直觉

`QRhiViewport` 描述把裁剪空间结果映射到 render target 上哪一块矩形，以及深度值映射到什么范围。它是 `QRhiCommandBuffer::setViewport()` 的参数，属于命令录制时的动态状态。

它和 `QRhiScissor` 很容易混淆：viewport 决定坐标变换，scissor 决定像素裁剪。一个改变几何映射，一个只是限制写入区域。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)`
- 类型：值类型，可比较、可哈希
- 归属：RHI 私有接口，来自 `QRhiViewport`

RHI 的 viewport `x`、`y` 采用左下角位置，`w`、`h` 是宽高；深度范围默认是 `0.0f` 到 `1.0f`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 空矩形，深度范围为 0 到 1 |
| `QRhiViewport(x, y, w, h, minDepth, maxDepth)` | 一次性描述视口矩形和深度范围 |
| `setViewport(x, y, w, h)` | 修改视口矩形 |
| `viewport()` | 返回 `{x, y, w, h}` |
| `setMinDepth()` / `minDepth()` | 设置或读取最小深度 |
| `setMaxDepth()` / `maxDepth()` | 设置或读取最大深度 |
| `operator==` / `operator!=` / `qHash()` | 比较与缓存状态 |

## 4. 关键用法

渲染到整个输出尺寸：

```cpp
cb->setViewport(QRhiViewport(0, 0, outputSize.width(), outputSize.height()));
```

分屏或小窗渲染：

```cpp
cb->setViewport(QRhiViewport(0, 0, w / 2.0f, h));
drawLeftEye();

cb->setViewport(QRhiViewport(w / 2.0f, 0, w / 2.0f, h));
drawRightEye();
```

如果还要限制写入区域，配合 `QRhiScissor`：

```cpp
cb->setViewport(QRhiViewport(0, 0, w, h));
cb->setScissor(QRhiScissor(10, 10, w - 20, h - 20));
```

两者坐标约定不完全一样时要特别小心，尤其是从 Qt 的左上角 UI 坐标换算到 RHI viewport。

## 5. 使用场景

- 随窗口或 swapchain 尺寸变化更新 viewport。
- 渲染到 texture atlas 的某个区域。
- 多视口编辑器、分屏、VR 双眼渲染。
- 级联阴影图，每个 cascade 使用不同 viewport。
- 调试深度映射或特殊深度范围。

## 6. 常见坑与经验

- `w` 和 `h` 不应为负；无效 viewport 可能被 `setViewport()` 忽略。
- viewport 的 `x`、`y` 是左下角，Qt widget 和 image 常用左上角，换算时最容易上下颠倒。
- viewport 不会阻止 viewport 外已有像素保留；清屏和 scissor 状态要单独考虑。
- HiDPI 下不要直接用逻辑像素尺寸，RHI 输出通常要使用实际像素尺寸。
- 深度范围反转或压缩可能影响深度测试精度；除非有明确理由，保持默认 0 到 1。

## 7. 知识点覆盖

本页覆盖：viewport 变换、深度范围、scissor 区别、左下角坐标、HiDPI 输出尺寸、多视口渲染、动态状态录制。
