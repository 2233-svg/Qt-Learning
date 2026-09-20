# QColormap

> Qt 6.11.1 · Qt Widgets · 来自 `QColormap`

## 1. 先建立直觉

`QColormap` 描述屏幕设备如何把 `QColor` 映射成底层像素值。它关心的是显示设备的颜色模式：真彩、索引色、灰度。现代桌面环境大多是 Direct 真彩模式，所以普通 Widgets 应用很少直接碰它。

它更像一把“底层显示兼容性尺子”。当你要和老式 indexed color 设备、特殊远程显示、低色深环境或原生像素接口打交道时，`QColormap` 才变得有意义。

## 2. 类说明

`QColormap` 是值类型，不是控件，也不继承 `QObject`。通过 `instance(screen)` 取得某个屏幕的颜色映射，然后可以查询深度、模式、可用颜色列表，以及颜色到像素值、像素值到颜色的转换。

在常规绘制中，你应该继续使用 `QPainter`、`QColor`、`QPalette`、`QImage` 等高级接口。只有当你明确需要设备相关 pixel 值时，再把 `QColormap` 拉出来。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `instance(int screen = -1)` | 获取指定屏幕的 colormap。`-1` 通常表示默认屏幕。 |
| `mode()` | 返回映射模式：`Direct`、`Indexed` 或 `Gray`。 |
| `depth()` | 返回显示深度，帮助判断颜色能力。 |
| `size()` | 返回颜色表大小。Direct 模式下意义有限。 |
| `colormap()` | 返回索引色/灰度模式下的颜色列表；Direct 模式通常为空。 |
| `pixel(const QColor &)` | 把 `QColor` 转成设备相关像素值。 |
| `colorAt(uint pixel)` | 把设备像素值反查成 `QColor`。 |
| `Mode::Direct` | 真彩模式，像素值直接编码颜色。现代桌面常见。 |
| `Mode::Indexed` | 像素值是颜色表索引。 |
| `Mode::Gray` | 像素值映射到灰度表。 |

## 4. 关键用法

```cpp
const QColormap map = QColormap::instance();

if (map.mode() == QColormap::Direct) {
    // 普通现代屏幕通常走这里，高级绘图接口已足够。
} else {
    const uint pixel = map.pixel(Qt::red);
    const QColor actual = map.colorAt(pixel);
}
```

这类代码一般只应该出现在平台适配、图像导出、老系统兼容或低层绘制桥接中。业务界面里到处转换 pixel 值，通常说明抽象层用低了。

## 5. 使用场景

适合处理低色深显示、远程 X11/嵌入式显示、需要分析屏幕颜色能力的诊断工具、把 Qt 绘制结果桥接到原生像素 API 的兼容层。

不适合普通主题配色、按钮颜色、文本颜色或图像处理。那些场景用 `QPalette`、样式表、`QColor`、`QImage::pixelColor()` 更自然。

## 6. 常见坑与经验

Direct 模式下 `colormap()` 可能为空，这不是错误，而是说明设备不靠颜色表工作。

`pixel()` 返回的是设备相关值，不是通用 RGB，也不适合作为跨平台持久化格式。要保存颜色配置，请保存 `QColor` 或字符串形式。

多屏环境中不同屏幕理论上可能有不同映射。需要精确时传入对应 screen，而不是假设默认屏幕代表全部显示设备。
