# QPixmapCache：面向 GUI 的全局像素图缓存

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPixmapCache>`  
> 所属模块：`Qt6::Gui`  
> 类型性质：只提供静态函数的应用级缓存；嵌套类型 `QPixmapCache::Key`

`QPixmapCache` 用来缓存生成成本较高、但可以随时重新生成的 `QPixmap`。例如按钮状态图、绘制后的缩略图、主题图标和复杂背景。它内部是 Qt 维护的全局缓存，不是一个需要实例化的容器对象。

它解决的是“重复绘制或解码同一 pixmap 太慢”的问题：

- 首次使用时生成 pixmap 并插入缓存。
- 后续使用时按键查找，命中则直接复用。
- 缓存接近容量上限时自动淘汰较旧、较少访问的条目。
- 条目被淘汰后，代码重新生成即可，不应把缓存当作持久存储。

## 适用场景

### 按稳定字符串缓存

字符串键适合由多个业务参数组成的复杂键，例如主题、尺寸、状态和语言：

```cpp
QPixmap pixmap;
const QString key = QStringLiteral("toolbar/%1/%2/%3")
                        .arg(themeName)
                        .arg(iconName)
                        .arg(pixelSize);

if (!QPixmapCache::find(key, &pixmap)) {
    pixmap = buildToolbarPixmap(themeName, iconName, pixelSize);
    if (!pixmap.isNull())
        QPixmapCache::insert(key, pixmap);
}
```

### 一对一对象映射

一个对象只对应一个 pixmap 时，用缓存生成的 `Key` 更高效。把 key 保存为对象成员即可：

```cpp
class IconItem
{
public:
    QPixmap pixmap() const
    {
        QPixmap result;
        if (!m_key.isValid() || !QPixmapCache::find(m_key, &result)) {
            result = buildPixmap();
            m_key = QPixmapCache::insert(result);
        }
        return result;
    }

private:
    mutable QPixmapCache::Key m_key;
};
```

`Key` 失效通常意味着条目被缓存淘汰；下一次访问应重新生成并用新的 key 替换旧 key。

## 重要边界

### 只能在应用主线程使用

Qt 6.11.1 文档明确规定，`QPixmapCache` 只能从应用程序主线程使用；其他线程的访问会被忽略并返回失败。不要用它在工作线程之间传递图片，也不要把它当作线程安全缓存。

后台线程若要共享生成结果，应使用线程安全的业务缓存和 `QImage`；回到 GUI 主线程后再转换为 `QPixmap` 并放入 `QPixmapCache`。

### 这是全局缓存，不是实例

`QPixmapCache` 没有可供构造的业务状态，所有 API 都是静态函数。不能通过创建多个 `QPixmapCache` 对象来获得多个独立缓存，也不能给某个缓存实例设置独立容量。

### 缓存会自动淘汰

默认容量为 `10240 KB`，即 10 MB。容量按近似的 pixmap 内存大小计算，约为：

```text
width * height * depth / 8
```

当插入新 pixmap 会超过限制时，Qt 会优先删除最旧、最近最少访问的条目。缓存命中后不要永久保存“必然存在”的假设，每次使用仍需处理 miss。

### 键必须由应用负责区分

字符串键相同会覆盖旧条目。Qt 自己插入的字符串键以 `$qt` 开头，应用自定义键不要使用这个前缀，以免和 Qt 内部条目冲突。

键必须包含所有会影响 pixmap 内容的参数。例如尺寸、设备像素比、主题、状态、语言或颜色方案遗漏在键中，会导致错误复用旧图片。

## 字符串键和 `Key` 的选择

| 方式 | 优点 | 代价与边界 |
| --- | --- | --- |
| `QString` | 可读、易调试、适合复杂组合键 | 查找较慢；需要自行保证命名空间和参数完整 |
| `QPixmapCache::Key` | 查找更快；适合对象到 pixmap 的一对一映射 | 由缓存生成；条目淘汰后自动失效；不能自己构造有效条目 |

不要把 `Key` 序列化到磁盘或当作跨进程 ID。它只对当前进程中的当前缓存有效。

## 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QPixmapCache>
```

## API 逐项说明

### 缓存容量与清空

#### `int QPixmapCache::cacheLimit()`

返回缓存容量上限，单位是 KB。Qt 6.11.1 的默认值是 `10240`。它是全局设置，不属于某个 `QPixmapCache` 实例。

#### `void QPixmapCache::setCacheLimit(int n)`

把全局缓存容量上限设置为 `n` KB。容量较小时，pixmap 可能刚插入就因空间不足而被淘汰；容量应结合应用的图片尺寸、内存预算和访问模式设置。

设置容量不会让缓存成为持久存储，也不能保证任何指定 key 一定保留。

#### `void QPixmapCache::clear()`

删除缓存中的所有 pixmap。清空后所有由缓存生成的 `Key` 都不再有效；保存这些 key 的对象必须在下次访问时检查 `isValid()` 或直接处理 `find()` 失败。

### 查找

#### `bool QPixmapCache::find(const QString &key, QPixmap *pixmap)`

按字符串键查找 pixmap。命中时把结果写入 `pixmap` 并返回 `true`；未命中时保持 `pixmap` 原值不变并返回 `false`。

传入的输出指针必须指向有效的 `QPixmap` 对象。未命中时不要把输出对象被清空当作契约，也不要忽略返回值：

```cpp
QPixmap cached;
if (QPixmapCache::find(key, &cached)) {
    painter.drawPixmap(target, cached);
} else {
    cached = createPixmap();
    QPixmapCache::insert(key, cached);
}
```

#### `bool QPixmapCache::find(const QPixmapCache::Key &key, QPixmap *pixmap)`

按缓存生成的 `Key` 查找。命中时写入 pixmap 并返回 `true`；未命中时不改变输出 pixmap 并返回 `false`。如果条目已经被淘汰，key 会被释放并变为无效，下一次应重新插入并保存返回的新 key。

这类 key 适合保存为某个对象的成员，不适合动态拼接多个业务字段。

### 插入

#### `bool QPixmapCache::insert(const QString &key, const QPixmap &pixmap)`

用字符串键插入 pixmap 的副本。成功插入返回 `true`，失败返回 `false`。如果同一字符串键已经存在，新的 pixmap 替换旧条目。

插入会受缓存容量和主线程限制影响。应用键不要以 `$qt` 开头；空 pixmap 通常没有缓存价值，插入前应检查 `isNull()`。

#### `QPixmapCache::Key QPixmapCache::insert(const QPixmap &pixmap)`

插入 pixmap 的副本并返回由缓存生成的 `Key`。返回的 key 可用于更快的后续 `find()`。如果条目无法保留，返回的 key 可能是无效 key，必须通过 `isValid()` 判断。

```cpp
QPixmapCache::Key key = QPixmapCache::insert(pixmap);
if (!key.isValid()) {
    // 缓存没有接受该条目，业务上仍可直接使用 pixmap
}
```

缓存保存的是 pixmap 的副本引用语义；调用方仍可修改自己的 pixmap，不应依赖修改自动同步到缓存条目。

### 删除

#### `void QPixmapCache::remove(const QString &key)`

删除字符串键对应的条目。如果键不存在，不应把调用当作错误；它只是确保该字符串条目不再留在缓存中。

#### `void QPixmapCache::remove(const QPixmapCache::Key &key)`

删除 key 对应的条目，并释放这个 key 供之后的缓存插入使用。删除后该 key 不再表示有效缓存内容，不能继续用于命中查找。

#### `bool QPixmapCache::replace(const QPixmapCache::Key &key, const QPixmap &pixmap)`（已弃用）

旧版接口尝试用新 pixmap 替换 key 对应的缓存项。Qt 6.6 起标记为弃用，头文件建议改为“先 `remove(key)`，再 `key = insert(pixmap)`”。新代码不要依赖它：

```cpp
QPixmapCache::remove(key);
key = QPixmapCache::insert(pixmap);
```

替换后的 key 可能不同，不能继续假设原 key 仍然有效。

## `QPixmapCache::Key` 逐项说明

`Key` 是由缓存生成的轻量句柄。默认构造得到空 key，不代表任何缓存条目；只有 `QPixmapCache::insert(const QPixmap &)` 返回的 key 才可能有效。

### `QPixmapCache::Key::Key()`

构造空 key。新对象的 `isValid()` 返回 `false`。

### `QPixmapCache::Key::~Key()`

销毁 key 对象。销毁 key 不应被理解为主动从缓存删除 pixmap；需要明确删除条目时调用 `QPixmapCache::remove(key)`。

### `bool QPixmapCache::Key::isValid() const noexcept`

判断当前 key 是否仍关联一个缓存 pixmap。如果条目被淘汰、缓存被清空或 key 被删除，返回 `false`。

### `void QPixmapCache::Key::swap(QPixmapCache::Key &other) noexcept`

交换两个 key 的内部句柄。操作很快且不会失败。交换不会复制或重新生成 pixmap。

### `bool operator==(const QPixmapCache::Key &, const QPixmapCache::Key &)`

比较两个 key 是否表示相同的缓存句柄。即使两个 key 当前相等，也不要把它当作 pixmap 内容比较；key 的有效性受缓存淘汰影响。

### `bool operator!=(const QPixmapCache::Key &, const QPixmapCache::Key &)`

返回两个 key 是否不同，语义与 `operator==` 相反。

### `size_t qHash(const QPixmapCache::Key &key, size_t seed = 0)`（Qt 6.6 起）

返回 key 的哈希值，可把 `Key` 用作 `QHash` 或其他哈希容器的键。哈希值只服务于当前 key 值，不是持久化标识，也不替代 `isValid()`。

## 一个完整的缓存辅助函数

```cpp
QPixmap loadOrCreatePixmap(const QString &key)
{
    QPixmap result;
    if (QPixmapCache::find(key, &result))
        return result;

    result = createExpensivePixmap();
    if (!result.isNull())
        QPixmapCache::insert(key, result);
    return result;
}
```

这个模式的关键是：命中和未命中都返回一个明确的 `QPixmap`，缓存只是性能优化。即使插入失败，业务仍应能够使用本次生成的结果；下一次调用再重新生成即可。

## 常见错误排查

1. **工作线程查找总是失败**：`QPixmapCache` 只允许应用主线程访问；把工作线程逻辑改为 `QImage` 或业务缓存。
2. **不同配置显示了同一张图**：检查字符串键是否包含尺寸、DPI、主题、状态、颜色和语言等全部影响因素。
3. **插入后马上 miss**：检查 pixmap 是否过大、缓存容量是否过小、是否发生了自动淘汰，以及是否在主线程操作。
4. **`Key` 失效后仍不断查找**：缓存淘汰或 `clear()` 后 key 会失效；重新生成 pixmap 并用新返回值覆盖旧 key。
5. **使用 `$qt` 前缀**：该前缀保留给 Qt 自己插入的条目，应用字符串键应避开。
6. **把缓存当作资源所有权**：cache miss 是正常路径；不要让程序正确性依赖缓存永久保存条目。
7. **用 `replace()` 写新代码**：Qt 6.6 起弃用，使用 `remove()` 加 `insert()`，并保存新的 key。
8. **把容量单位当成字节**：`cacheLimit()` 和 `setCacheLimit()` 使用 KB，不是字节。
9. **用 `Key` 做磁盘缓存 ID**：`Key` 只在当前进程的当前缓存中有效，不能跨进程或跨运行保存。

## API 速查表

| 类别 | API | 作用 | 关键边界与注意事项 |
| --- | --- | --- | --- |
| 容量 | `cacheLimit()` | 查询全局缓存上限 | 单位 KB；默认 `10240` |
| 容量 | `setCacheLimit(int n)` | 设置全局缓存上限 | 容量不足会自动淘汰旧条目 |
| 管理 | `clear()` | 清空全部 pixmap | 已保存的 `Key` 全部可能失效 |
| 查找 | `find(QString, QPixmap *)` | 按字符串键查找 | 命中写输出；miss 时保持输出原值 |
| 查找 | `find(Key, QPixmap *)` | 按生成 key 查找 | miss 可能使 key 失效；必须处理返回值 |
| 插入 | `insert(QString, QPixmap)` | 以字符串键插入副本 | 相同键覆盖旧条目；避开 `$qt` 前缀 |
| 插入 | `insert(QPixmap)` | 插入并生成 `Key` | 返回 key 可能无效；用 `isValid()` 检查 |
| 删除 | `remove(QString)` | 删除字符串条目 | 不存在时通常无需特殊处理 |
| 删除 | `remove(Key)` | 删除 key 对应条目 | key 释放后不能继续当有效句柄 |
| 替换 | `replace(Key, QPixmap)` | 旧式替换缓存条目 | Qt 6.6 起弃用；改用 remove 加 insert |
| 嵌套类型 | `Key()` | 构造空 key | 不关联缓存，`isValid()` 为 false |
| 嵌套类型 | `Key::~Key()` | 销毁 key 句柄 | 不等于显式删除缓存条目 |
| 嵌套类型 | `Key::isValid()` | 判断 key 是否仍关联条目 | 淘汰、清空、删除后为 false |
| 嵌套类型 | `Key::swap(Key &) noexcept` | 交换两个 key | 很快且不会失败 |
| 比较 | `operator==` / `operator!=` | 比较 key 句柄 | 不代表 pixmap 内容相等 |
| 哈希 | `qHash(Key, seed)` | 将 key 用于哈希容器 | Qt 6.6 起；不是持久化 ID |

### 一句话总结

`QPixmapCache` 是 GUI 主线程专用的全局性能缓存：键要覆盖所有图像配置，容量按 KB 计算，淘汰和 miss 都是正常情况；把缓存当作可丢弃的加速层，程序才不会被偶发的缓存失效绑住。
