# QTextObjectInterface 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractTextDocumentLayout>`  
> 所属模块：`Qt6::Gui`  
> 类型：自定义内联文本对象接口

## 1. 它解决什么问题

`QTextObjectInterface` 让应用把自定义内联对象接入 `QTextDocument` 的布局与绘制过程。通过它可以在普通文字中显示公式、标签、附件图标、进度标记或业务占位对象，而不把这些内容伪装成一串普通字符。

接口只定义两件事：

- `intrinsicSize()`：对象在行内需要多大空间；
- `drawObject()`：布局分配好矩形后怎样画出来。

它不负责对象注册、文档编辑、资源下载或交互事件分发。对象身份通常由 `QTextFormat::objectType()` 及从 `UserProperty` 开始的自定义格式属性表达。

## 2. 正确接入步骤

实现类通常同时继承 `QObject`，并声明 Qt 接口：

```cpp
class BadgeRenderer final : public QObject, public QTextObjectInterface
{
    Q_OBJECT
    Q_INTERFACES(QTextObjectInterface)

public:
    QSizeF intrinsicSize(QTextDocument *, int,
                         const QTextFormat &) override;
    void drawObject(QPainter *, const QRectF &, QTextDocument *, int,
                    const QTextFormat &) override;
};
```

然后把 QObject 实例注册给文档布局的对象类型：

```cpp
layout->registerHandler(MyBadgeObjectType, renderer);
```

插入文本时，给 `QTextCharFormat` 设置相同的 `objectType`，再通过 `QTextCursor` 插入相应对象替代字符或使用适合的自定义对象路径。对象类型和 property ID 应在应用内集中定义，避免与 Qt 预定义值冲突。

## 3. 尺寸和绘制契约

`intrinsicSize()` 必须快速、稳定，并只根据格式、位置和可安全读取的外部数据返回逻辑尺寸。尺寸变化会触发行高和换行变化；不要在此函数里修改同一份文档、启动阻塞 I/O 或依赖未准备好的异步结果。

`drawObject()` 收到的 `rect` 是布局为该对象分配的矩形。应在此矩形内绘制，尊重 painter 的现有变换和裁剪；不要自行重设全局 painter 状态后不恢复，也不要假定 rect 是屏幕坐标。

如果对象显示内容异步变化，更新缓存后应以文档/布局支持的方式触发布局或重绘，而不是长期保存一次回调中的 `QTextInlineObject`。

## 4. 生命周期和线程

`registerHandler()` 注册的是 `QObject *`。注册不应被当成所有权转移：调用方应保证 handler 在布局使用期间有效，或在销毁前 `unregisterHandler()`。让 renderer 以 layout 或同线程控制器为 parent 是常见做法。

布局回调、文档和 painter 都在文档所属线程使用。接口实现不得从后台线程直接读写正在显示的文档；后台任务完成后以队列方式回到文档线程更新数据并请求重绘。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `~QTextObjectInterface()` | 虚析构函数。 | 通过接口指针销毁实现时必须有正确的实际对象生命周期。 |
| `intrinsicSize(QTextDocument *, int, const QTextFormat &)` | 返回对象要求的逻辑尺寸。 | 纯虚函数；应快速、无阻塞、无重入编辑，位置是文档文本位置。 |
| `drawObject(QPainter *, const QRectF &, QTextDocument *, int, const QTextFormat &)` | 在布局给定矩形中绘制对象。 | 纯虚函数；painter 有效性、裁剪和线程由布局调用上下文决定。 |
| `QAbstractTextDocumentLayout::registerHandler()` | 为 object type 注册 QObject 接口实现。 | 类型必须与插入格式匹配；注册不等于所有权转移。 |
| `QAbstractTextDocumentLayout::unregisterHandler()` | 移除某个类型的 handler。 | handler 销毁或替换前应解除注册。 |
| `QAbstractTextDocumentLayout::handlerForObject()` | 查询已注册的接口实现。 | 返回接口观察指针，不拥有实现对象。 |

## 5. 记忆重点

`QTextObjectInterface` 是“测量 + 绘制”的小接口。尺寸先于绘制，格式提供对象类型和业务数据，布局提供矩形；实现必须保持无阻塞、无重入，并和 handler 的注册生命周期保持一致。
