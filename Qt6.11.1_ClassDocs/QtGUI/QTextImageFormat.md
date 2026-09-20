# QTextImageFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextImageFormat`

## 1. 先建立直觉

`QTextImageFormat` 描述文档里的图片对象：图片资源名、宽高、质量、最大宽度等。插入图片时，文档通过 name 去找资源或加载 URL。

它是 `QTextCharFormat` 的专用形式，因为图片在文本流里表现为一个内联对象。

## 2. 类说明

- 头文件：`#include <QTextImageFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextCharFormat`
- 协作类：`QTextCursor::insertImage()`、`QTextDocument::addResource()`

图片数据不一定存进 format；format 更多保存引用和显示尺寸。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setName()` / `name()` | 图片资源名或 URL |
| `setWidth()` / `width()` | 显示宽度 |
| `setHeight()` / `height()` | 显示高度 |
| `setQuality()` / `quality()` | 导出或编码质量提示 |
| `setMaximumWidth()` / `maximumWidth()` | 最大宽度，支持 `QTextLength` |
| `isValid()` | 是否是有效图片格式 |

## 4. 关键用法

```cpp
doc->addResource(QTextDocument::ImageResource, QUrl("logo"), image);

QTextImageFormat img;
img.setName("logo");
img.setWidth(128);
cursor.insertImage(img);
```

如果 name 是 URL，文档可能尝试通过资源加载机制解析；自定义资源更稳定。

## 5. 使用场景

- 富文本中插入本地或资源图片。
- 报表 logo、截图、图标。
- HTML `<img>` 导入导出。
- 控制图片显示尺寸和最大宽度。

## 6. 常见坑与经验

- `name()` 必须能被文档资源系统解析，否则图片显示为空。
- 只设置 width 或 height 可能保持比例，也可能受布局和资源信息影响，复杂场景建议明确测试。
- 大图片插入前最好缩放或缓存，避免文档布局和绘制成本过高。
- 导出格式对质量字段支持不完全一致。

## 7. 知识点覆盖

本页覆盖：文档图片资源、内联图片、显示尺寸、最大宽度、HTML 图片导入导出、资源 URL。
