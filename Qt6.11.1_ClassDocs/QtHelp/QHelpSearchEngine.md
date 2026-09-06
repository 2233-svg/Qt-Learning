# QHelpSearchEngine

> Qt 6.11.1 · Qt Help

## 1. 先建立直觉

**一句话定位：** `QHelpSearchEngine` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** 这是 Qt Help 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QHelpSearchEngine` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QHelpSearchEngine>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Help)
target_link_libraries(mytarget PRIVATE Qt6::Help)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QHelpSearchEngine(QHelpEngineCore *helpEngine, QObject *parent = nullptr)`
- `virtual ~QHelpSearchEngine()`
- `QHelpSearchQueryWidget * queryWidget()`
- `QHelpSearchResultWidget * resultWidget()`
- `QString searchInput() const`
- `int searchResultCount() const`
- `QList<QHelpSearchResult> searchResults(int start, int end) const`

### 公有槽函数

- `void cancelIndexing()`
- `void cancelSearching()`
- `void reindexDocumentation()`
- `void search(const QString &searchInput)`

### 信号

- `void indexingFinished()`
- `void indexingStarted()`
- `void searchingFinished(int searchResultCount)`
- `void searchingStarted()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QHelpSearchEngine::QHelpSearchEngine(QHelpEngineCore *helpEngine, QObject *parent = nullptr)`

**作用与语义：**

基于给定`parent`构建一个新的搜索引擎。搜索引擎利用给定的`helpEngine`访问需要索引的文档。`QHelpEngine`的 setupFinished() 信号会自动连接到 QHelpSearchEngine 的索引功能，因此信号发出后新的文档也会被索引。

### `[virtual noexcept] QHelpSearchEngine::~QHelpSearchEngine()`

**作用与语义：**

这会摧毁搜索引擎。

### `[slot] void QHelpSearchEngine::cancelIndexing()`

**作用与语义：**

这样可以停止索引过程。

### `[slot] void QHelpSearchEngine::cancelSearching()`

**作用与语义：**

这会停止搜索过程。

### `[signal] void QHelpSearchEngine::indexingFinished()`

**作用与语义：**

该信号在索引过程完成时发出。

### `[signal] void QHelpSearchEngine::indexingStarted()`

**作用与语义：**

该信号在索引过程启动时发出。

### `QHelpSearchQueryWidget *QHelpSearchEngine::queryWidget()`

**作用与语义：**

返回一个小部件作为输入小部件。根据你的搜索引擎配置，你会得到一个包含更多或更少子小部件的不同小部件。

### `[slot] void QHelpSearchEngine::reindexDocumentation()`

**作用与语义：**

强制搜索引擎重新索引所有文档文件。

### `QHelpSearchResultWidget *QHelpSearchEngine::resultWidget()`

**作用与语义：**

返回一个小部件，可以保存并显示搜索结果。

### `[slot] void QHelpSearchEngine::search(const QString &searchInput)`

**作用与语义：**

使用给定的搜索词组`searchInput`开始搜索过程。
该短语可能由多个词组成。默认情况下，搜索引擎返回包含所有指定词汇的文档列表。短语可以包含逻辑运算符 AND、OR 和 NOT 的任意组合。运算符必须全部大写，否则将被视为搜索短语的一部分。
如果使用双引号来分组这些词，搜索引擎会搜索与该短语的完全匹配。
有关文本查询语法的更多信息，请参见SQLite FTS5扩展。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
helpSearchEngine， qOverload（&QHelpSearchEngine：：search））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
helpSearchEngine， [receiver = helpSearchEngine]（const QString &searchInput） { receiver->search（searchInput）; }）;


更多示例和方法，请参见连接超载槽位。

### `QString QHelpSearchEngine::searchInput() const`

**作用与语义：**

返回最后搜索的短语。

### `int QHelpSearchEngine::searchResultCount() const`

**作用与语义：**

返回搜索引擎找到的结果数量。

### `QList<QHelpSearchResult> QHelpSearchEngine::searchResults(int start, int end) const`

**作用与语义：**

返回从`start`指定的索引到`end`指定的索引范围内的搜索结果列表。

### `[signal] void QHelpSearchEngine::searchingFinished(int searchResultCount)`

**作用与语义：**

当搜索过程完成时，该信号会发出。搜索结果计数存储在`searchResultCount`中。

### `[signal] void QHelpSearchEngine::searchingStarted()`

**作用与语义：**

当搜索过程开始时，该信号会发出。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QHelpSearchEngine` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
