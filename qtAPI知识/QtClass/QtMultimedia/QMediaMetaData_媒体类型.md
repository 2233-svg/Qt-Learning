# QMediaMetaData：用键值表表示媒体和轨道元数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMediaMetaData>`  
> 所属模块：`Qt6::Multimedia`  
> 继承：无  
> 类型性质：值类型

## 它解决什么问题

`QMediaMetaData` 用 `Key -> QVariant` 的方式保存媒体描述信息。它承载的不是音视频数据，而是标题、作者、时长、编码器、分辨率、封面和轨道语言等标签。

常见来源有两类：

- `QMediaPlayer::metaData()`：当前媒体的元数据；
- `QMediaPlayer::audioTracks()`、`videoTracks()`、`subtitleTracks()`：各轨道的元数据；
- `QImageCapture::imageMetadataAvailable()`：一次拍照得到的元数据；
- `QImageCapture::setMetaData()`：为后续拍照设置待写入元数据。

```text
媒体文件/采集后端
          |
          v
    QMediaMetaData
      Key -> QVariant
```

## 真实使用场景

- 播放器显示标题、作者、专辑和封面；
- 轨道选择菜单显示音频语言和字幕信息；
- 拍照时写入说明、版权或应用自定义的拍摄记录；
- 调试后端实际识别出的容器、编解码器、码率和分辨率；
- 把元数据值复制到业务模型或日志中。

## 基本用法

```cpp
QMediaMetaData data;
data.insert(QMediaMetaData::Title, QStringLiteral("Demo"));
data.insert(QMediaMetaData::Author,
            QStringList{QStringLiteral("Alice")});
data.insert(QMediaMetaData::Date, QDateTime::currentDateTime());
data.insert(QMediaMetaData::Resolution, QSize(1920, 1080));

const QString title = data.stringValue(QMediaMetaData::Title);
```

`QVariant` 让不同键可以保存不同类型，但也意味着读取时不能只凭键名猜测所有平台都返回完全一致的类型。Qt 文档给出了每个标准键的推荐类型；应用读取时应使用 `value().canConvert<T>()`、`value<T>()` 或 `to...()` 做边界处理。

## `Key` 与推荐值类型

Qt 6.11.1 定义了以下键。后端不一定支持所有键，未提供的键不会出现在 `keys()` 中。

| 键 | 含义 | 推荐值类型 |
| --- | --- | --- |
| `Title` | 媒体标题。 | `QString` |
| `Author` | 作者列表。 | `QStringList` |
| `Comment` | 用户评论。 | `QString` |
| `Description` | 媒体描述。 | `QString` |
| `Genre` | 媒体所属流派。 | `QStringList` |
| `Date` | 录制时间或媒体流编码时间。 | `QDateTime` |
| `Language` | 媒体语言。 | `QLocale::Language` |
| `Publisher` | 发布者。 | `QString` |
| `Copyright` | 版权声明。 | `QString` |
| `Url` | 媒体来源 URL。 | `QUrl` |
| `Duration` | 媒体时长，单位毫秒。 | `qint64` |
| `MediaType` | 媒体类型，例如音频或视频。 | `QString` |
| `FileFormat` | 文件格式。 | `QMediaFormat::FileFormat` |
| `AudioBitRate` | 音频码率，单位 bit/s。 | `int` |
| `AudioCodec` | 音频编解码器。 | `QMediaFormat::AudioCodec` |
| `VideoBitRate` | 视频码率，单位 bit/s。 | `int` |
| `VideoCodec` | 视频编解码器。 | `QMediaFormat::VideoCodec` |
| `VideoFrameRate` | 视频帧率。 | `qreal` |
| `AlbumTitle` | 专辑标题。 | `QString` |
| `AlbumArtist` | 专辑主要艺术家。 | `QString` |
| `ContributingArtist` | 参与创作者列表。 | `QStringList` |
| `TrackNumber` | 曲目编号。 | `int` |
| `Composer` | 作曲者列表。 | `QStringList` |
| `LeadPerformer` | 主要表演者列表。 | `QStringList` |
| `ThumbnailImage` | 内嵌缩略图。 | `QImage` |
| `CoverArtImage` | 内嵌封面图。 | `QImage` |
| `Orientation` | 图像或视频旋转角度。 | `int` |
| `Resolution` | 图像或视频尺寸。 | `QSize` |
| `HasHdrContent` | 是否含有面向 HDR 显示的内容。 | `bool` |

`HasHdrContent` 自 Qt 6.8 引入，而且文档明确限定为 FFmpeg 和 Darwin 后端支持的只读信息。`NumMetaData` 是键数量边界，不是一个应该插入到对象中的元数据键。

## 缺失值、类型和读取策略

默认构造对象为空，`isEmpty()` 返回 `true`。调用 `value(key)` 查询不存在的键会得到无效 `QVariant`；不能把无效值和一个实际存在但内容为空的字符串混为一谈。

```cpp
const QVariant value = data.value(QMediaMetaData::Duration);
if (value.isValid() && value.canConvert<qint64>()) {
    const qint64 durationMs = value.toLongLong();
}
```

`stringValue(key)` 是方便的字符串读取函数。它适合标题、作者和界面展示，但对于 `QDateTime`、`QImage`、枚举、尺寸和布尔值，不应把字符串当作无损存储格式。要保留原始语义，应读取 `QVariant` 并按键使用对应类型。

后端和平台可能只提供一部分键，也可能对同一类媒体缺少封面、语言或编码时间。Qt 文档明确说明不是所有标识符都在所有平台受支持，应用界面应允许缺省，而不是把缺失元数据当作解析失败。

## 插入、替换和删除

`insert(key, value)` 在键已存在时替换旧值。`remove(key)` 删除键；删除不存在的键没有有用的错误返回。`clear()` 清空全部元数据。

`operator[](key)` 返回一个可写的 `QVariant &`。如果键原来不存在，使用下标访问会创建一个对应键的条目，因此：

```cpp
data[QMediaMetaData::Comment] = QStringLiteral("edited");
```

会插入或替换评论。读取场景不要随意使用非常量 `operator[]`，否则可能因为一次查询改变 `isEmpty()` 和 `keys()` 的结果。用于只读查询时优先 `value()`。

`QMediaMetaData` 没有通用的“值类型校验”公开插入 API。应用负责选择与键匹配的 `QVariant` 类型；错误类型可能导致后端忽略、转换失败或写文件时丢弃。

## 遍历、比较和复制

`keys()` 返回当前存在的键列表。`asKeyValueRange()` 自 Qt 6.9 提供范围视图，可以遍历键值对：

```cpp
for (const auto [key, value] : data.asKeyValueRange()) {
    qDebug() << QMediaMetaData::metaDataKeyToString(key) << value;
}
```

范围的有效期受 `QMediaMetaData` 对象及其数据修改影响。不要在对象被销毁或结构发生修改后继续保存迭代器/引用。

它是值类型，复制得到独立的逻辑值；底层 `QVariant` 和其中的隐式共享类型可能按 Qt 的值语义共享存储。复制元数据不会修改播放器、录制器或图像文件。`operator==` 比较键值表内容，不代表两个对象来自同一个媒体文件。

## 与播放器和拍照的边界

`QMediaPlayer::metaData()` 返回当前媒体的只读结果，元数据何时可用取决于媒体加载；应连接 `metaDataChanged()`。轨道列表的 `QMediaMetaData` 描述具体轨道，不等同于播放器整体元数据。

`QImageCapture::setMetaData()` 和 `addMetaData()` 使用的是应用为后续拍照准备的配置；`imageMetadataAvailable` 是后端对已拍图像实际提供的元数据。设置成功不等于平台一定写入文件，格式和编码器可能丢弃不支持的字段。

## 线程和所有权

值对象本身没有线程归属，可以作为信号参数、容器元素或跨线程消息传递。它不拥有媒体文件、图像设备或播放器。若 `QVariant` 中保存了 `QImage` 等隐式共享值，跨线程处理仍应遵守这些值类型的访问规则；若保存自定义 QObject 指针，则不要把它误当成元数据资源管理。

从 `QMediaPlayer` 或 `QImageCapture` 取得元数据后，应复制到业务模型再交给工作线程。不要在工作线程直接调用媒体 `QObject` 的 getter 来等待后端更新。

## 常见误区

- 认为所有键在所有平台都存在。
- 用 `stringValue()` 读取图片、尺寸或枚举后再试图无损恢复。
- 用非常量 `operator[]` 做查询，意外插入了空键。
- 把 `Duration` 与播放器 `duration()` 的单位弄混；这里同样是毫秒，但来源可能未提供。
- 把轨道元数据当成整个文件的元数据。
- 认为设置元数据一定会写入所有格式的文件。
- 把 `QMediaMetaData` 的复制当成复制媒体文件或播放器状态。
- 把 `NumMetaData` 当作可插入的键。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 查询 | `QVariant value(Key key) const` | 按键读取值。 | 不存在时返回无效 `QVariant`；读取不会插入。 |
| 修改 | `void insert(Key key, const QVariant &value)` | 插入或替换键值。 | 应使用与键匹配的值类型。 |
| 修改 | `void remove(Key key)` | 删除指定键。 | 不存在时没有错误结果。 |
| 查询 | `QList<Key> keys() const` | 返回当前已存在的键。 | 只包含后端/应用实际提供的键。 |
| 修改 | `QVariant &operator[](Key key)` | 返回可写键值引用，不存在时创建条目。 | 只读查询不要使用，以免改变容器。 |
| 修改 | `void clear()` | 删除所有键值。 | 不影响来源媒体或播放器。 |
| 查询 | `bool isEmpty() const` | 判断是否没有元数据条目。 | 一个空字符串值仍可能使对象非空。 |
| 查询 | `QString stringValue(Key key) const` | 以字符串形式读取键值。 | 不适合无损读取图像、尺寸、日期和枚举。 |
| 展示 | `static QString metaDataKeyToString(Key key)` | 把键转换为可显示名称。 | 用于界面/日志，不是持久化协议。 |
| 遍历 | `auto asKeyValueRange() const` | 自 Qt 6.9 返回键值范围视图。 | 视图依赖对象生命周期和未修改状态。 |
| 比较 | `operator==(const QMediaMetaData &, const QMediaMetaData &)` | 比较两个键值表是否相等。 | 比较内容，不比较来源对象身份。 |
| 比较 | `operator!=(const QMediaMetaData &, const QMediaMetaData &)` | 判断两个键值表不同。 | 仍只反映键值内容。 |
| 枚举 | `enum Key` | 定义标准元数据键。 | 不保证所有后端都支持；`HasHdrContent` 自 Qt 6.8 起。 |
| 常量 | `static constexpr int NumMetaData` | 表示元数据键数量边界。 | 不是有效业务键。 |
| 保护 | `static QMetaType keyType(Key key)` | 返回键对应的元类型。 | 受保护接口，主要供 Qt 扩展使用。 |

## 一句话总结

`QMediaMetaData` 是媒体标签的值容器：用标准 `Key` 访问 `QVariant`，对缺失键和平台差异保持宽容，读取时按键校验类型，写入时不要把“应用设置”误认为“后端一定落盘”。
