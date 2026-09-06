# QMediaMetaData

> Qt 6.11.1 · Qt Multimedia

## 1. 先建立直觉

**一句话定位：** `QMediaMetaData` 是 Qt Multimedia 的“媒体Meta数据”类型，参与媒体源、设备、格式、播放/采集状态或音视频数据处理。

**模块背景：** Qt Multimedia 提供音频、视频、摄像头、媒体会话和设备访问能力。

### 这是什么

`QMediaMetaData` 是 多媒体设备与会话机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

**适用场景：** 先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

## 2. 依赖与对象关系

- 头文件：`#include <QMediaMetaData>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Multimedia)
target_link_libraries(mytarget PRIVATE Qt6::Multimedia)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

多媒体类型通常把设备、媒体会话、格式、播放状态和异步错误分开。硬件能力、平台后端、权限和资源状态会影响结果；请求成功发起不等于设备已准备好。

### 状态、生命周期和线程

**生命周期：** 设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

**状态与结果：** 区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

**线程与事件循环：** 媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

## 3. 直接使用

先检查平台能力和权限，再创建会话/设备，设置格式和源，连接状态与错误信号，执行开始/暂停/停止并在结束后清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Key { Title, Author, Comment, Description, Genre, …, HasHdrContent }`

### 公有函数

- `(since 6.9) auto asKeyValueRange() const`
- `void clear()`
- `void insert(QMediaMetaData::Key k, const QVariant &value)`
- `bool isEmpty() const`
- `QList<QMediaMetaData::Key> keys() const`
- `void remove(QMediaMetaData::Key k)`
- `QString stringValue(QMediaMetaData::Key key) const`
- `QVariant value(QMediaMetaData::Key key) const`
- `QVariant & operator[](QMediaMetaData::Key k)`

### 静态公有成员

- `QString metaDataKeyToString(QMediaMetaData::Key key)`

### 相关非成员函数

- `bool operator!=(const QMediaMetaData &a, const QMediaMetaData &b)`
- `bool operator==(const QMediaMetaData &a, const QMediaMetaData &b)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMediaMetaData::Key`

**作用与语义：**

可以使用以下元数据密钥：
- `QMediaMetaData::Title`：`0`;媒体标题
- `QMediaMetaData::Author`：`1`;媒体作者
- `QMediaMetaData::Comment`：`2`;评论
- `QMediaMetaData::Description`：`3`;简短的废弃
- `QMediaMetaData::Genre`：`4`;媒体所属的类型
- `QMediaMetaData::Date`：`5`;创建日期
- `QMediaMetaData::Language`：`6`;媒体语言
- `QMediaMetaData::Publisher`：`7`;媒体出版商信息。
- `QMediaMetaData::Copyright`：`8`;媒体版权信息。
- `QMediaMetaData::Url`：`9`;出版商网站网址
- `QMediaMetaData::Duration`：`10`;媒体播放时长
- `QMediaMetaData::MediaType`：`11`;媒体类型
- `QMediaMetaData::FileFormat`：`12`;文件格式
- `QMediaMetaData::AudioBitRate`：`13`
- `QMediaMetaData::AudioCodec`：`14`
- `QMediaMetaData::VideoBitRate`：`15`
- `QMediaMetaData::VideoCodec`：`16`
- `QMediaMetaData::VideoFrameRate`：`17`
- `QMediaMetaData::AlbumTitle`：`18`;专辑标题
- `QMediaMetaData::AlbumArtist`：`19`;艺术家信息。
- `QMediaMetaData::ContributingArtist`：`20`
- `QMediaMetaData::TrackNumber`：`21`
- `QMediaMetaData::Composer`：`22`;媒体作曲家信息。
- `QMediaMetaData::LeadPerformer`：`23`
- `QMediaMetaData::ThumbnailImage`：`24`;媒体缩略图（嵌入元数据时）
- `QMediaMetaData::CoverArtImage`：`25`;媒体封面艺术
- `QMediaMetaData::Orientation`：`26`
- `QMediaMetaData::Resolution`：`27`
- `QMediaMetaData::HasHdrContent (since Qt 6.8)`：`28`;视频可能包含HDR内容（仅读，仅限FFmpeg和Darwin媒体后端）

### `[since 6.9] auto QMediaMetaData::asKeyValueRange() const`

**作用与语义：**

返回一个范围对象，允许对该哈希进行键值对迭代。

### `[invokable] void QMediaMetaData::clear()`

**作用与语义：**

从元数据对象中移除所有数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] void QMediaMetaData::insert(QMediaMetaData::Key k, const QVariant &value)`

**作用与语义：**

在钥匙中插入一个`value`：`k`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QMediaMetaData::isEmpty() const`

**作用与语义：**

如果元数据中没有任何项，返回`true`;否则返回`false`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[static protected] QMetaType QMediaMetaData::keyType(QMediaMetaData::Key key)`

**作用与语义：**

返回用于存储密钥`key`数据的元类型。

### `[invokable] QList<QMediaMetaData::Key> QMediaMetaData::keys() const`

**作用与语义：**

返回QMediaMetaData：：Keys的`QList`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[static invokable] QString QMediaMetaData::metaDataKeyToString(QMediaMetaData::Key key)`

**作用与语义：**

返回一个字符串表示`key`，可用于向用户展示元数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] void QMediaMetaData::remove(QMediaMetaData::Key k)`

**作用与语义：**

从Key： `k`中移除元数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] QString QMediaMetaData::stringValue(QMediaMetaData::Key key) const`

**作用与语义：**

返回密钥`key`的元数据作为`QString`。
这主要是为了简化向用户展示元数据的过程。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[invokable] QVariant QMediaMetaData::value(QMediaMetaData::Key key) const`

**作用与语义：**

返回密钥`key`的元数据值，若无元数据则返回空`QVariant`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QVariant &QMediaMetaData::operator[](QMediaMetaData::Key k)`

**作用与语义：**

返回存储在密钥`k`的数据。

**官方示例：**

```cpp
 QMediaMetaData rockBallad1;
 rockBalad[QMediaMetaData::Genre]="Rock"
```

### `QHash<QMediaMetaData::Key, QVariant> QMediaMetaData::data`

**作用与语义：**

该变量存储元数据。
注意：这是同类`protected`成员。

### `bool operator!=(const QMediaMetaData &a, const QMediaMetaData &b)`

**作用与语义：**

比较两个元数据对象 `a` 和 `b`，如果相同则返回`false`，若不同则返回`true`。

### `bool operator==(const QMediaMetaData &a, const QMediaMetaData &b)`

**作用与语义：**

比较两个元数据对象`a`和`b`，若相同则返回`true`，若不同则返回`false`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

设备或媒体对象要在使用期间保持有效，开始前配置输入/输出和格式，停止后释放会话或解除设备占用。状态、媒体状态和错误信号共同决定下一步操作。

### 状态和错误边界

区分无媒体、加载中、已加载、播放中、暂停、停止、结束和错误。进度、时长、缓冲和设备可用性不是同一个状态，不能只用一个 bool 表示。

### 线程边界

媒体对象通常依赖事件循环和平台线程边界；GUI 展示对象在 GUI 线程，后台处理要使用类明确支持的线程模型。

### 最容易出现的错误

不要假设所有平台支持相同编解码器和格式；不要忽略权限和后端错误；不要在状态未准备好时连续调用控制 API；媒体对象销毁前先停止使用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMediaMetaData` 所属机制类型：多媒体设备与会话机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
