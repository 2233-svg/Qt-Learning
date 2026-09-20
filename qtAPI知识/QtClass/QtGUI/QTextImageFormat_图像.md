# QTextImageFormat 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextImageFormat>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextCharFormat`

## 1. 它解决什么问题

`QTextImageFormat` 是插入富文本文档的图像对象的格式描述。它保存资源名称、显示宽高、最大宽度和质量提示；真正的图像数据由 `QTextDocument` 的资源系统根据名称解析。

它解决“文档中的这个对象应引用哪个图像、以什么尺寸排版”，而不是读取图片文件、解码图片或管理磁盘缓存。图像加载通常来自文档资源缓存、`loadResource()`、resource provider 或相对 `baseUrl()`。

常见场景：

- 在富文本编辑器中插入应用资源、内存 `QImage` 或 URL 图像；
- 生成带 logo、截图或公式位图的报告；
- 使用百分比最大宽度让图片适配不断变化的文本区域；
- 导出或导入 HTML 时检查图像格式而不直接操作图像字节。

## 2. 名称是资源键，不等于文件一定存在

`setName()` 设置的是文档资源引用名，常见形式是资源路径或 URL。插入前可主动给文档缓存添加资源：

```cpp
document->addResource(
    QTextDocument::ImageResource,
    QUrl("memory://diagram"),
    QVariant::fromValue(image));

QTextImageFormat format;
format.setName("memory://diagram");
format.setWidth(240);
cursor.insertImage(format);
```

`name()` 匹配成功不保证资源可加载；URL 错误、provider 返回空值或图片解码失败时，布局只能按文档的失败处理方式呈现。反过来，资源已存在也不会自动显示，仍需把相应格式插入文档。

## 3. 尺寸和质量边界

`setWidth()`、`setHeight()` 指定显示尺寸，改变的是排版几何，不会重采样或修改资源中的原始 `QImage`。只设置一边时，是否、如何保持图像比例由当前文本布局与资源本身决定；需要确定比例时应显式计算两边。

`maximumWidth()` 是 `QTextLength`，可表示固定值、百分比或可变长度：

```cpp
format.setMaximumWidth(
    QTextLength(QTextLength::PercentageLength, 100));
```

它是最大宽度约束，而非“总会占满 100% 宽度”的命令；最终大小仍由图片本身、显式宽度、可用行宽和布局决定。

`setQuality(int)` 保存编码质量提示，主要在图像格式写出或序列化路径中有意义。Qt 6.3 起无参 `setQuality()` 已弃用；明确调用 `setQuality(100)`。质量不等于显示清晰度，也不能修复已低分辨率的资源。

## 4. 有效性、线程和生命周期

`isValid()` 只判断底层格式类型是否是 image format，不能证明 `name()` 非空、资源已加载或显示尺寸可用。

本类是可复制值类型，不拥有图像数据和文档。可以在后台准备格式值与图像数据，但 `addResource()`、`insertImage()` 和任何会访问既有 `QTextDocument` 的操作必须在该文档所属线程执行。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextImageFormat()` | 创建图像格式值。 | 尚未关联资源，也没有插入文档。 |
| `isValid()` | 判断是否为图像格式类别。 | 不验证资源 URL、图片内容或加载结果。 |
| `setName(const QString &)` / `name()` | 设置或读取文档资源键。 | 是资源名称/URL，不是已打开文件句柄。 |
| `setWidth(qreal)` / `width()` | 设置或读取显示宽度。 | 只影响布局显示尺寸，不缩放原始资源数据。 |
| `setHeight(qreal)` / `height()` | 设置或读取显示高度。 | 需要确定比例时建议显式设置成对尺寸。 |
| `setMaximumWidth(QTextLength)` / `maximumWidth()` | 设置或读取最大宽度约束。 | 可为固定、百分比或可变长度；不是强制最终宽度。 |
| `setQuality(int)` / `quality()` | 设置或读取图像编码质量提示。 | 使用显式值；无参 `setQuality()` 在 Qt 6.3 起已弃用。 |
| 继承的 `setToolTip()` / `toolTip()` | 为图像对象设置悬停提示。 | 实际交互呈现取决于使用该文档的控件。 |
| 继承的 `setAnchorHref()` / `anchorHref()` | 为图像设置链接语义。 | 点击处理需要由编辑器或浏览器控件实现。 |

## 6. 记忆重点

`QTextImageFormat` 是“资源引用 + 布局尺寸”的格式值。`name()` 是资源键，宽高是显示约束，`maximumWidth()` 可随可用空间变化；它本身从不加载图片，文档资源系统才负责那件事。
