# QMediaMetaData
> Qt 6.11.1 · Qt Multimedia · 来自 `QMediaMetaData`

## 作用定位

`QMediaMetaData` 是媒体元数据的键值容器，用来表示标题、作者、专辑、封面、日期、分辨率、时长等信息。播放器读取它，录制器也可写入它。

## 类说明

- 头文件：`#include <QMediaMetaData>`
- CMake：链接 `Qt6::Multimedia`
- 继承：无公开 QObject 继承，值类型

## API 速查

| API | 说明 |
| --- | --- |
| `insert(key, value)` | 设置某项元数据。 |
| `value(key)` / `operator[]` | 读取某项值。 |
| `remove(key)` / `clear()` | 删除或清空元数据。 |
| `contains(key)` / `keys()` | 查询已有字段。 |
| `isEmpty()` | 是否无元数据。 |
| `asKeyValueRange()` | 遍历键值。 |
| `metaDataKeyToString()` | 把元数据键转成显示字符串。 |
| `stringValue()` | 读取适合显示的字符串值。 |

## 使用场景

- 播放器显示歌曲标题、艺术家、专辑封面。
- 录制文件时写入作者、标题、日期。
- 媒体库扫描和索引。

## 常见坑与经验
- 元数据不一定存在，也不一定在媒体加载初期就可用，要监听播放器变化。
- 不同容器支持的字段不同，写入不保证最终文件都保留。
- 图片、日期、数值等字段类型不同，读取前看 QVariant 类型。
- `stringValue()` 适合 UI 展示，结构化处理仍应按 key 的预期类型读取。

## 知识点覆盖

- 媒体标签和元信息
- 播放读取与录制写入
- QVariant 类型化字段
- UI 展示与结构化处理
