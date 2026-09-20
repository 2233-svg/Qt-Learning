# QUtiMimeConverter 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QUtiMimeConverter>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QUtiMimeConverter` 解决的是 Qt MIME 数据和 Apple Uniform Type Identifier 之间的互认问题。Qt 的剪贴板与拖放 API 使用 MIME 类型描述数据，例如 `text/plain`、`text/html`、`text/uri-list`；macOS、iOS 等 Apple 平台的系统剪贴板和拖放协议更常遇到 UTI，例如 `public.utf8-plain-text`、`public.html`、`public.file-url`。这个类就是桥接层：当 Qt 遇到某个 UTI，需要把它变成 `QMimeData` 中的 MIME 内容；或者 Qt 要把 MIME 内容交给系统，需要生成对应的 UTI 数据。

它不是通用 MIME 解析器，也不是 `QMimeData` 的替代品。它的价值在于把一种类型名映射到另一种类型名，并在必要时转换底层字节。Qt 已经内置了常见文本、HTML、URL、文件 URL、部分图片和 vCard 等 UTI 映射；只有当应用需要和 Finder、系统应用、第三方原生应用交换自定义格式或私有 UTI 时，才需要自己派生 `QUtiMimeConverter`。

## 实际使用场景

- 在 macOS 应用中把内部文档片段拖到另一款原生应用，对方只识别某个私有 UTI。
- 从系统剪贴板读取一组 UTI 数据，把它包装成 Qt 侧的 `QMimeData` MIME 格式。
- 让 Qt 拖放系统额外导出 `com.example.my-document-fragment`，同时继续保留普通 `text/plain` 或 `text/html` 兜底格式。
- 调试剪贴板数据时确认“Qt 能看到 MIME，但系统应用看不到 UTI”的转换缺口。

## 使用模型

`QUtiMimeConverter` 是抽象接口，直接构造基类没有意义；通常做法是实现一个派生类，并在创建 `QGuiApplication` 之后创建该派生对象。构造函数会把转换器加入 Qt 维护的全局转换器列表，析构函数会把它移出列表。

转换器实例可以放在栈上，也可以堆分配。堆分配时 Qt 会取得所有权，并在 `QGuiApplication` 关闭阶段删除它；栈对象则以普通 C++ 生命周期为准。析构会取消注册，所以不要让转换器早于你需要支持剪贴板或拖放的时段销毁。

当 Qt 查找可用转换器时，会遍历所有 `QUtiMimeConverter` 实例，并优先选择最后创建的实例。这意味着后注册的转换器可以覆盖或优先处理同一 MIME/UTI 对；自定义实现要尽量只声明自己确实支持的格式，避免拦截本该由内置转换器处理的数据。

## 关键语义与边界

`mimeForUti()` 和 `utiForMime()` 是声明能力的入口。返回空字符串表示“不支持这个方向”，不要为了兜底返回一个模糊类型，否则 `canConvert()` 和后续实际转换都会被误导。

`convertFromMime()` 的方向是从 Qt MIME 数据生成 UTI 字节；`convertToMime()` 的方向是从 UTI 字节还原成 Qt MIME 值。两者都必须由派生类实现。UTI 数据要求自终止，文档特别提醒输入或输出的 `QByteArray` 末尾可能带有额外数据，转换代码不要用“整个数组长度等于有效载荷长度”做脆弱假设。

`convertToMime()` 返回 `QVariant`，它最终会进入 `QMimeData` 语义中，因此类型要和目标 MIME 匹配：文本通常是 `QString`，URL 列表通常是 `QList<QUrl>` 或 Qt 期望的相关类型，二进制私有格式则常见 `QByteArray`。无法转换时应返回无效或空结果，而不是伪造部分数据。

`count()` 用于告诉 Qt 给定 `QMimeData` 能导出多少项。默认行为适合大多数单项 MIME 数据；如果你的格式天然是多项数据，例如拖放多个对象，可以重写它，让系统侧看到正确数量。

## 常见误区

- 在 `QGuiApplication` 创建前注册转换器。此类依赖 GUI 应用的剪贴板/拖放基础设施，应在应用对象之后创建。
- 忘记保存转换器实例。栈对象离开作用域会立即取消注册，后续拖放或剪贴板转换自然失效。
- 把 MIME 名和 UTI 名写反。`convertFromMime()` 是 MIME 到 UTI，`convertToMime()` 是 UTI 到 MIME。
- 对不支持的格式返回“差不多”的类型名。转换器查找按能力声明路由，错误声明会让真正可用的转换器失去机会。
- 假设只有一个转换器参与。Qt 会遍历全局列表，而且后创建的实例优先。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `QUtiMimeConverter::QUtiMimeConverter()` | 创建转换器并注册到 Qt 的全局 UTI/MIME 转换器列表。 | 必须在 `QGuiApplication` 创建之后调用；后创建的转换器查找优先级更高。 |
| `[virtual noexcept] QUtiMimeConverter::~QUtiMimeConverter()` | 销毁转换器并从全局列表注销。 | 析构后对应格式不再参与剪贴板/拖放转换；堆分配对象可由 Qt 在应用关闭时删除。 |
| `bool canConvert(const QString &mime, const QString &uti) const` | 判断当前转换器是否能在给定 MIME 与 UTI 之间双向转换。 | 结果取决于 `mimeForUti()` 与 `utiForMime()` 的实现；只声明真实支持的组合。 |
| `[pure virtual] QList<QByteArray> convertFromMime(const QString &mime, const QVariant &data, const QString &uti) const` | 把 Qt MIME 数据转换为指定 UTI 的原始字节列表。 | 返回数据可能需要自终止；UTI 字节末尾允许存在额外尾随数据。 |
| `[pure virtual] QVariant convertToMime(const QString &mime, const QList<QByteArray> &data, const QString &uti) const` | 把指定 UTI 的原始字节列表还原为 Qt MIME 数据。 | 输入字节可能有尾随数据；返回 `QVariant` 类型要符合目标 MIME 的 Qt 约定。 |
| `[virtual] int count(const QMimeData *mimeData) const` | 返回给定 MIME 数据可导出的项目数量。 | 多项拖放格式可重写；不要返回超过实际可转换项数量的值。 |
| `[pure virtual] QString mimeForUti(const QString &uti) const` | 查询某个 UTI 对应的 MIME 类型。 | 不支持时返回空字符串；不要用宽泛 MIME 误报能力。 |
| `[pure virtual] QString utiForMime(const QString &mime) const` | 查询某个 MIME 类型对应的 UTI。 | 不支持时返回空字符串；映射应和 `convertFromMime()` 可实际生成的数据一致。 |

## 一句话总结

`QUtiMimeConverter` 是 Apple 平台剪贴板和拖放里的格式翻译插槽：只在需要补充自定义 UTI/MIME 转换时派生它，并让能力声明、字节转换和对象生命周期保持一致。
