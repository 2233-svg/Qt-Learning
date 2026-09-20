# QPixmapCache

> Qt 6.11.1 · Qt GUI · 来自 `QPixmapCache`

## 1. 先建立直觉

`QPixmapCache` 是 Qt 提供的进程级、内存受限、最近最少使用倾向的 `QPixmap` 缓存。它适合留住昂贵生成的缩略图、缩放图、组合背景和图标变体，避免在每次绘制时重复做 decode、缩放或 transform。

它不是可靠存储：条目随时可能因为内存上限被淘汰，`clear()` 也会清空全局内容。因此所有读取都必须把 miss 视为正常路径，并能从原始数据重建 pixmap。

## 2. 类说明

- 头文件：`#include <QPixmapCache>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：静态全局缓存，不需要实例化。
- 线程：`QPixmapCache` 仅可从主线程访问。后台任务应缓存 `QImage` 或普通数据，回到 GUI 线程后再使用 pixmap cache。
- 淘汰：插入会在必要时清除较久未访问的条目；缓存不提供固定生命周期保证。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `insert(QString, QPixmap)` | 用调用方稳定字符串键插入；成功返回 `true` |
| `find(QString, QPixmap *)` | 通过字符串键查询；miss 时输出 pixmap 不变 |
| `remove(QString)` | 主动移除一个字符串键条目 |
| `insert(QPixmap)` | 让缓存生成高效的 `QPixmapCache::Key` |
| `find(Key, QPixmap *)` | 通过内部 key 查询；miss 后 key 通常失效 |
| `remove(Key)` | 删除内部 key 所指条目 |
| `cacheLimit()` | 获取全局缓存上限，单位 KB |
| `setCacheLimit(kb)` | 设置全局缓存上限，单位 KB |
| `clear()` | 清空进程中所有 cache 条目 |
| `QPixmapCache::Key` | 高效的一对一对象到 pixmap 的内部句柄 |

## 4. 关键用法

### 用完整渲染参数构造字符串键

```cpp
const QString key = QStringLiteral(
    "thumb:v3:file=%1:size=%2x%3:dpr=%4:theme=%5")
    .arg(fileId)
    .arg(logicalSize.width())
    .arg(logicalSize.height())
    .arg(screenDpr, 0, 'f', 2)
    .arg(themeRevision);

QPixmap thumb;
if (!QPixmapCache::find(key, &thumb)) {
    const QImage image = makeThumbnail(fileId, logicalSize, screenDpr);
    thumb = QPixmap::fromImage(image);
    if (!thumb.isNull())
        QPixmapCache::insert(key, thumb);
}
painter.drawPixmap(target, thumb);
```

键必须包含所有会改变像素结果的输入：源版本、目标尺寸、DPR、裁剪、颜色方案、主题、滤镜参数等。若只用文件路径作键，窗口移动到高 DPI 屏、主题切换或缩略图尺寸变化时都会复用错误资源。

### 用内部 Key 绑定到稳定业务对象

```cpp
class PreviewItem {
public:
    QPixmapCache::Key cacheKey;
};

QPixmap pm;
if (!QPixmapCache::find(item.cacheKey, &pm)) {
    pm = renderPreview(item);
    item.cacheKey = QPixmapCache::insert(pm);
}
```

`Key` 避免构造和哈希长字符串，适合一个对象只持有一张派生 pixmap 的场景。缓存淘汰后 `find()` 会失败，此 key 随后不再有效；下一次生成时用新的 `insert()` 返回值覆盖它。

### 明确调整全局内存预算

```cpp
const int oldLimitKb = QPixmapCache::cacheLimit();
QPixmapCache::setCacheLimit(48 * 1024); // 48 MiB
```

这是进程级预算，影响 Qt 和所有依赖库的 pixmap cache 使用。不要由某个局部控件随意改大；先通过内存剖析确认需求，必要时在应用初始化配置一次。

## 5. 使用场景

- 项目视图、文件浏览器、图片库的大量缩略图。
- 自绘控件中尺寸和主题稳定的复杂背景、阴影、路径栅格化结果。
- 图标变体、状态叠加层、昂贵 transform 的 GUI 线程缓存。
- 与业务对象一一对应且可随时重建的预览 pixmap。

## 6. 常见坑与经验

- **缓存 miss 不是错误。** `find()` 失败应走生成路径，不能把它当作资源丢失或逻辑异常。
- **不要用 `$qt` 前缀。** 该前缀保留给 Qt 内部键，用户键绝不应以它开头。
- **不要缓存不可重建的唯一数据。** 条目会被淘汰；原始图像/模型数据应在别处保存。
- **`clear()` 是全局重锤。** 它会影响应用其他组件甚至某些 Qt 内部缓存使用，主题切换也应优先做精确 key 失效。
- **大图很快吃掉预算。** 一张 `2048x2048` ARGB pixmap 约 16 MiB；缓存缩略图时限制目标大小。
- **不要从 worker 线程调用。** 先生成 `QImage`，通过信号把它交给 GUI 线程插入/显示。
- **键版本化。** 算法、色彩管理或渲染规则升级后，给 key 加版本字段，避免复用旧语义结果。

## 7. 知识点覆盖

LRU 风格缓存、进程级内存预算、QPixmap GUI 线程约束、缓存键设计、DPR/主题维度、淘汰与失效、缩略图优化、Key 句柄。
