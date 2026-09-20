# QIconEngine

> Qt 6.11.1 · Qt GUI · 来自 `QIconEngine`

## 1. 先建立直觉

`QIconEngine` 是 `QIcon` 背后的策略对象：当控件请求“24 逻辑像素、DPR 2、Disabled + On 的图标”时，engine 决定如何选择资源、生成 pixmap 或直接绘制。

它面向图标格式实现者，而非普通界面开发。用 `QIcon`、SVG、主题图标已能解决绝大多数需求；只有自定义矢量格式、远程/程序生成图标、专有多分辨率容器时，才继承该类。

## 2. 类说明

- 头文件：`#include <QIconEngine>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：多态基类，由 `QIcon` 持有和复制。
- 必须实现：`clone() const` 与 `paint(...)`。
- 每个 `QIcon` 副本需要独立 engine 状态，因此 `clone()` 必须返回逻辑等价、可独立修改的新实例。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `clone()` | 必须深/正确复制当前 engine，供 `QIcon` 值语义使用 |
| `paint(painter, rect, mode, state)` | 必须在目标矩形绘制所需状态的图标 |
| `pixmap(size, mode, state)` | 生成 pixmap；默认可借助 `paint()` 实现 |
| `scaledPixmap(size, mode, state, scale)` | 为 DPR/缩放请求生成 pixmap，尺寸为逻辑像素 |
| `actualSize(size, mode, state)` | 返回该请求下真实可用的逻辑尺寸 |
| `availableSizes(mode, state)` | 返回该状态可提供的资源尺寸 |
| `addFile()` / `addPixmap()` | 接收 `QIcon` 添加的文件或 pixmap 资源 |
| `key()` | 返回 engine 类型标识，通常用于序列化/恢复 |
| `iconName()` | 返回图标来源名称，常用于主题/诊断 |
| `isNull()` | 判断 engine 是否表示空 icon |
| `read()` / `write()` | 支持从 `QDataStream` 恢复/保存 engine 状态 |
| `virtual_hook()` | 以 ABI 兼容方式支持扩展钩子 |
| `IsNullHook` | 兼容旧引擎的空状态查询 |
| `ScaledPixmapHook` | 兼容高 DPI pixmap 请求，参数为 `ScaledPixmapArgument` |

## 4. 关键用法

### 以 paint 为唯一真实渲染路径

```cpp
class BadgeEngine final : public QIconEngine
{
public:
    QIconEngine *clone() const override { return new BadgeEngine(*this); }

    void paint(QPainter *p, const QRect &rect,
               QIcon::Mode mode, QIcon::State state) override
    {
        p->save();
        const QColor color = mode == QIcon::Disabled
                           ? QColor("#9aa0a6") : baseColor;
        p->setBrush(color);
        p->setPen(Qt::NoPen);
        p->drawEllipse(rect);
        if (state == QIcon::On)
            drawCheckMark(*p, rect);
        p->restore();
    }
};
```

把状态与缩放逻辑集中在 `paint()`，可以让默认 `pixmap()` 实现自然工作。`paint()` 必须保护 painter 状态：任何画笔、画刷、变换、裁剪或合成模式改动都应以 `save()`/`restore()` 包围。

### 正确处理逻辑尺寸和 DPR

```cpp
QPixmap BadgeEngine::scaledPixmap(const QSize &logicalSize,
                                  QIcon::Mode mode,
                                  QIcon::State state,
                                  qreal scale)
{
    QPixmap pm(logicalSize * scale);
    pm.setDevicePixelRatio(scale);
    pm.fill(Qt::transparent);

    QPainter p(&pm);
    paint(&p, QRect(QPoint(), logicalSize), mode, state);
    return pm;
}
```

`size` 是设备无关的逻辑尺寸，物理分配才乘 `scale`。设置 DPR 后，painter 的有效逻辑坐标仍是 `logicalSize`，这能避免在高 DPI 下把图标画得过大或过小。

### 克隆状态而不是共享可变指针

```cpp
QIconEngine *BadgeEngine::clone() const
{
    auto *copy = new BadgeEngine;
    copy->baseColor = baseColor;
    copy->glyph = glyph;
    return copy;
}
```

若 engine 内部缓存有共享对象，应保证它们的并发/修改语义明确。`QIcon` 期待值类型行为：复制一个图标再修改其中一份，不应意外改变另一份的显示。

## 5. 使用场景

- 用代码程序化生成状态图标、徽标、计数圆点。
- 用专有矢量图、图标字体、远程资产或主题索引驱动 `QIcon`。
- 为品牌系统统一生成 disabled、active、checked 的视觉变体。
- 为新的图标容器格式接入 Qt action/control 生态。

## 6. 常见坑与经验

- **不要把 `QIconEngine` 当缓存容器。** 可缓存昂贵的解析/栅格化结果，但缓存键必须含 size、DPR、Mode、State 和主题/颜色环境。
- **`clone()` 不能返回 `this`。** 除非有极其严谨的不可变引用计数设计，否则会打破生命周期和值语义。
- **`actualSize()` 必须返回逻辑尺寸。** 高 DPI 的物理像素数在 `scaledPixmap()` 层处理。
- **`addFile()`/`addPixmap()` 是可选扩展点。** 对纯程序化 engine 可忽略，但要确保调用者理解资源不会被存储。
- **流序列化要配合 `key()`。** 只有能稳定恢复自身格式的 engine 才应重载 `read()`/`write()` 并提供稳定类型 key。
- **不要自行依赖私有 hook 细节。** `virtual_hook()` 主要为 Qt 的二进制兼容而存在；新实现优先重载公开虚函数。

## 7. 知识点覆盖

策略模式、QIcon 值语义、克隆、状态渲染、高 DPI 逻辑坐标、painter 状态隔离、图标缓存、流序列化、ABI 兼容钩子、自定义图标格式。
