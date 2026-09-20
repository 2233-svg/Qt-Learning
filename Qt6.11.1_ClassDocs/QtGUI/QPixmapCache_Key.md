# QPixmapCache::Key

> Qt 6.11.1 · Qt GUI · 来自 `QPixmapCache::Key`

## 1. 先建立直觉

`QPixmapCache::Key` 是 `QPixmapCache` 插入时生成的内部句柄。它适合“某个对象对应一张可重建的 pixmap”这一对一关系，比每次拼接字符串键更轻量。

它不是永久 ID，也不是对象 ID。缓存为了腾出内存淘汰 pixmap 后，这个 key 会失效；下一次查找失败就是正常信号，业务对象应重新生成 pixmap 并保存新的 key。

## 2. 类说明

- 头文件：`#include <QPixmapCache>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：值类型，只能由 `QPixmapCache::insert(const QPixmap&)` 获得有效实例。
- 关联：`QPixmapCache` 仅能从主线程使用，因此 key 的查找、插入、移除也应留在 GUI 线程。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `Key()` | 创建无效空 key |
| `isValid()` | 判断 key 当前是否仍关联缓存条目 |
| `swap(other)` | 常数时间交换两个 key |
| `qHash(key, seed)` | Qt 6.6 起可作为哈希容器键 |
| `QPixmapCache::insert(pixmap)` | 插入 pixmap 并返回一个有效 key（若插入成功） |
| `QPixmapCache::find(key, &pixmap)` | 查找对应 pixmap；失败表示被移除/淘汰 |
| `QPixmapCache::remove(key)` | 显式删除条目并使 key 不再可用 |

## 4. 关键用法

```cpp
class AvatarItem {
public:
    QPixmapCache::Key renderedAvatar;
};

QPixmap avatar;
if (!QPixmapCache::find(item.renderedAvatar, &avatar)) {
    avatar = QPixmap::fromImage(renderAvatar(item.data));
    item.renderedAvatar = QPixmapCache::insert(avatar);
}
painter.drawPixmap(target, avatar);
```

写法的关键不是 `isValid()`，而是 `find()`：即使 key 以前有效，缓存也可能在两次使用间因淘汰变空。`find()` 成功才代表输出 pixmap 可用；失败时直接重建并用新 key 覆盖旧 key。

如果业务数据改变，主动让缓存关系失效：

```cpp
QPixmapCache::remove(item.renderedAvatar);
item.renderedAvatar = {};
```

这能释放不再正确的渲染结果；不过仅将 key 置空不一定立刻从缓存中删除条目。

## 5. 使用场景

- 列表、场景节点、数据模型项各自缓存一张缩略图或预览图。
- 自绘对象保存生成的阴影、文字栅格化、图表小图等 pixmap。
- 需要避免字符串键分配和维护，同时结果可随时重建的 GUI 热点。

## 6. 常见坑与经验

- **无效 key 不是错误。** 默认构造、显式 remove、全局 clear 和 LRU 淘汰都会导致无效。
- **不要把 key 持久化。** 它只在当前进程当前缓存生命周期内有效，重启后没有意义。
- **不要跨线程使用。** key 本身虽是值类型，但与 `QPixmapCache` 的交互仍受主线程限制。
- **不要假定 `isValid()` 后一定能 find。** 以 `find()` 的返回值为准，确保有 miss 重建路径。
- **哈希能力不等于稳定身份。** Qt 6.6 的 `qHash` 仅方便你在本地容器索引 key，不能跨运行或跨缓存实例比较。

## 7. 知识点覆盖

缓存句柄、临时有效期、LRU 淘汰、GUI 线程约束、按需重建、显式失效、值类型、哈希容器。
