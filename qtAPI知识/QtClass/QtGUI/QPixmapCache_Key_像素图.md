# QPixmapCache::Key：高效访问全局像素图缓存的句柄

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPixmapCache>`  
> 所属类型：`QPixmapCache`  
> 相关类型：`QPixmap`、`QHash`

`QPixmapCache::Key` 是由 `QPixmapCache` 生成的轻量身份句柄。它把某个对象与缓存中的一张 `QPixmap` 做一对一关联，比用字符串查缓存更高效。它不是业务 ID，不包含图片数据，也不保证长期有效。

典型模式是：对象首次需要昂贵像素图时生成并插入缓存，保存返回的 `Key`；之后优先用 key 查找，缓存淘汰或清空后发现 key 已失效，再重新生成图片和 key。

## 它解决的问题

某些图像生成代价高，例如语法高亮缩略图、复杂图标、缩放后的预览、图表标记或样式化控件缓存。若每次绘制都重建，CPU 和内存带宽都会浪费。

`QPixmapCache` 提供全局临时 pixmap 缓存。字符串 key 适合能稳定命名的复杂组合条件；`QPixmapCache::Key` 更适合“一个业务对象对应一张临时 pixmap”的场景：

```cpp
class ThumbnailItem
{
public:
    QPixmapCache::Key cacheKey;
};

QPixmap cachedThumbnail(ThumbnailItem &item)
{
    QPixmap pixmap;
    if (item.cacheKey.isValid()
        && QPixmapCache::find(item.cacheKey, &pixmap)) {
        return pixmap;
    }

    pixmap = renderThumbnail();
    item.cacheKey = QPixmapCache::insert(pixmap);
    return pixmap;
}
```

`isValid()` 和 `find()` 都要检查：key 可能已经因缓存淘汰、`clear()` 或相关删除而失效。

## 实际使用场景

### 1. 每个模型项缓存一张生成的图标

```cpp
QPixmap iconFor(Row &row)
{
    QPixmap icon;
    if (row.iconKey.isValid() && QPixmapCache::find(row.iconKey, &icon))
        return icon;

    icon = renderIcon(row);
    row.iconKey = QPixmapCache::insert(icon);
    return icon;
}
```

这是 `Key` 最适合的场景：key 可作为模型项成员，避免维护冗长且易碰撞的字符串键。

### 2. 缓存失效后重新生成

```cpp
void Row::invalidateIcon()
{
    if (iconKey.isValid())
        QPixmapCache::remove(iconKey);

    iconKey = QPixmapCache::Key();
}
```

业务数据变化时，主动从缓存移除旧 pixmap 并清空对象持有的 key。即使没有主动移除，缓存容量不足时也可能自动淘汰，因此查找失败必须有重建路径。

### 3. 将 key 作为哈希容器键

```cpp
QHash<QPixmapCache::Key, Metadata> metadata;
```

Qt 6.6 起提供 `qHash(const QPixmapCache::Key &, size_t)`，因此 key 可作为 `QHash` 键。注意这只解决容器哈希，不延长缓存项寿命；容器中仍可能保留一个已失效 key。

## 核心语义与边界

### key 由缓存生成，默认构造无效

```cpp
QPixmapCache::Key key;
Q_ASSERT(!key.isValid());

key = QPixmapCache::insert(pixmap);
```

默认构造的 key 是空句柄。应用不能自行构造一个可用 key，也不应试图把内存地址、字符串或序号转换为它。

### 有效性不是永久承诺

`isValid()` 为 `true` 表示当前仍有关联的缓存 pixmap。缓存项被冲刷、淘汰或删除后，key 不再有效。

全局缓存受 `QPixmapCache::cacheLimit()` 限制，缓存满时会淘汰项目；因此：

- 不要把 key 当作持久存储引用；
- 不要把 `isValid()` 视为“图片内容仍与当前业务数据一致”的证明；
- 查找失败不是异常，而是正常缓存未命中；
- 业务版本变化时仍应主动让旧 key 失效或替换。

### key 比字符串快，但不能跨进程持久化

key 用于当前进程中的当前 `QPixmapCache` 实例。它没有稳定文本表示，也不会在下次程序启动后恢复关联。跨会话、跨进程或磁盘缓存应保存生成参数、资源路径或自己的稳定字符串键，而不是保存 `Key`。

### 仅限应用主线程

`QPixmapCache` 只能在应用主线程使用；从其他线程访问会被忽略并返回失败。`Key` 虽是值类型，但围绕它的 `insert()`、`find()`、`remove()` 与 `isValid()` 所表达的缓存状态应在主线程处理。

后台任务需要准备像素内容时，使用 `QImage` 或纯数据在后台生成，再通过主线程转成 `QPixmap` 并插入缓存。

### 比较与复制

`Key` 可复制和移动。`operator==` 比较它们是否指向同一缓存身份，`operator!=` 是其否定。复制 key 不会复制 `QPixmap`，也不会阻止缓存淘汰。

两个无效 key 是否相等不应用作业务逻辑判断；真正需要的是“能否 `find()` 到当前缓存项”。

## 关键 API 语义

### 插入、查询、失效恢复

```cpp
QPixmap pixmap;

if (!key.isValid() || !QPixmapCache::find(key, &pixmap)) {
    pixmap = renderExpensivePixmap();
    key = QPixmapCache::insert(pixmap);
}
```

即使 `isValid()` 先返回 `true`，也应把 `find()` 的返回值作为实际读取结果。缓存是全局可变资源，容器管理和业务数据修改都可能导致重新生成需求。

### 替换现有 key

`QPixmapCache::replace(const Key &, const QPixmap &)` 在 Qt 6.6 起已弃用。新代码使用“先删除，后插入”：

```cpp
if (key.isValid())
    QPixmapCache::remove(key);

key = QPixmapCache::insert(updatedPixmap);
```

这种写法也更明确地反映 key 可能变为新的身份。

## 常见错误

### 假设 key 永不失效

缓存本来就允许丢弃内容以控制内存。每次需要 pixmap 时都必须准备未命中的再生成路径。

### 在工作线程访问 QPixmapCache

主线程以外的访问会失败。不要把缓存调用藏在并行图片生成函数里；只把生成结果交回 GUI 线程缓存。

### 把 key 序列化到配置或数据库

它只在当前进程缓存中有意义，重启后不能恢复。保存图片生成参数或业务实体 ID。

### 手工复制 pixmap，却忘记更新 key

当业务对象的视觉输入变化时，旧 key 仍可能命中旧图片。将 key 与影响绘制的版本号一起管理，或数据变化时主动 `remove()` 并重置 key。

## API 速查表

### `QPixmapCache::Key`

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `Key()` | 构造空的无效 key。 | 作为未缓存状态或主动重置的值。 |
| `Key(const Key &other)` | 复制缓存身份句柄。 | 不复制 pixmap，不延长缓存存活期。 |
| `Key(Key &&other)` | 移动 key。 | 移动后源对象不再保有原身份。 |
| `operator=(const Key &other)` | 复制赋值。 | 用于让业务对象保存新 key。 |
| `operator=(Key &&other)` | 移动赋值。 | `noexcept`；普通缓存代码通常直接赋 `insert()` 返回值。 |
| `~Key()` | 销毁 key 句柄。 | 不会自动删除缓存 pixmap。 |
| `isValid() const` | 是否仍有缓存 pixmap 与此 key 关联。 | 淘汰、清空或删除后会变为无效；仍应检查 `find()`。 |
| `operator==(const Key &other) const` | 判断两个 key 是否代表相同缓存身份。 | 不等价于 pixmap 内容相同。 |
| `operator!=(const Key &other) const` | `operator==` 的否定。 | 用于身份变更检测。 |
| `swap(Key &other)` | 快速交换两个 key。 | `noexcept`；交换句柄，不移动缓存数据。 |
| `qHash(const Key &key, size_t seed = 0)` | 计算 key 的哈希值。Qt 6.6 起提供。 | 支持作为 `QHash` 键；哈希容器不维护缓存生命周期。 |

### 配套 `QPixmapCache` API

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `insert(const QPixmap &pixmap)` | 插入 pixmap 并返回缓存生成的 `Key`。 | 返回 key 后保存它；仅在主线程调用。 |
| `find(const Key &key, QPixmap *pixmap)` | 用 key 读取缓存 pixmap。 | 返回 `false` 时重新生成，而不是把它当作错误。 |
| `remove(const Key &key)` | 删除此 key 对应的缓存项。 | 视觉输入变化时主动失效；之后重置业务侧 key。 |
| `clear()` | 清空全局 pixmap 缓存。 | 所有现有 key 可能随之失效。 |
| `cacheLimit()` / `setCacheLimit(int kb)` | 查询 / 设置全局缓存内存上限（KB）。 | 不要把大缓存上限当作永久保留保证。 |

一句话记忆：`QPixmapCache::Key` 是“当前全局 pixmap 缓存里这张图的临时句柄”，查不到就重新生成，绝不把它当作永久 ID。
