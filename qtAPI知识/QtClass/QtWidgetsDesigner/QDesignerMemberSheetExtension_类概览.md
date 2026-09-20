# QDesignerMemberSheetExtension 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerMemberSheetExtension>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerMemberSheetExtension` 用来向 Qt Widgets Designer 的信号与槽编辑器描述一个 widget 的成员函数。它回答的不是“这个控件有哪些属性”，而是：

- 有多少可供 Designer 处理的成员；
- 某个成员的名称、完整签名、参数类型和参数名；
- 它是信号、槽还是其他成员；
- 它声明在哪个类、是否从 `QWidget` 继承；
- 在 Designer 的信号槽编辑器中是否可见，显示在哪个分组。

它适用于希望改变 Designer 连接编辑体验的自定义控件，例如隐藏不建议用户连接的 inherited 成员，或者将某些领域信号归入“Data”“Validation”等分组。

它不改变 C++ 真实元对象中的信号槽，也不阻止代码在运行时连接信号。它控制的是 Designer 编辑器呈现和选择成员的方式。

## 典型用途

最常见用法是取得某个 widget 的 member sheet，找到指定成员，再改变其在 Designer 中的可见性：

```cpp
auto *sheet = qt_extension<QDesignerMemberSheetExtension *>(
    formEditor->extensionManager(), widget);

if (!sheet)
    return;

const int index = sheet->indexOf("setEchoMode(QLineEdit::EchoMode)");
if (index >= 0)
    sheet->setVisible(index, false);
```

实际自定义扩展则需要维护一份能稳定映射索引的成员描述表。`count()`、`memberName()`、`signature()`、参数信息与各种判断函数都必须针对同一索引空间工作。

## 设计索引模型

接口绝大部分成员以 `index` 为参数。实现时应把每一个索引绑定到唯一成员记录，避免 `indexOf()` 找到的索引和 `signature(index)`、`isSignal(index)` 描述的不是同一成员。

一个常见内部模型是：

```cpp
struct MemberInfo {
    QString name;
    QString signature;
    QList<QByteArray> parameterTypes;
    QList<QByteArray> parameterNames;
    QString group;
    bool signal = false;
    bool slot = false;
    bool visible = true;
};
```

`parameterTypes()` 与 `parameterNames()` 返回的列表应保持相同长度并按参数位置一一对应。

## 它和属性表扩展的区别

- `QDesignerMemberSheetExtension` 管理信号槽编辑器里的成员函数。
- `QDesignerPropertySheetExtension` 管理属性编辑器里的属性。

两者都叫 sheet，但服务的是 Designer 完全不同的面板。不要为了隐藏属性而实现 member sheet，也不要为了隐藏信号槽而实现 property sheet。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QDesignerMemberSheetExtension()` | 销毁成员表扩展接口。 | 实现类通常配合 `QObject` 和 extension factory 使用。 |
| 数量 | `count() const` | 返回可描述的成员函数数量。 | 所有以 `index` 为参数的 API 都必须以此范围为准。 |
| 声明来源 | `declaredInClass(int index) const` | 返回该成员声明所在的类名。 | 索引无效时应按实现约定返回空字符串，不要访问越界数据。 |
| 按名查找 | `indexOf(const QString &name) const` | 返回指定成员名对应的索引。 | 名称匹配规则要与 `memberName()` 保持一致；找不到时返回无效索引。 |
| QWidget 继承判断 | `inheritedFromWidget(int index) const` | 判断成员是否从 `QWidget` 继承。 | 不要把“从任意基类继承”误报为从 `QWidget` 继承。 |
| 信号判断 | `isSignal(int index) const` | 判断该成员是否是 signal。 | 结果应与 `signature()` 和元对象真实语义一致。 |
| 槽判断 | `isSlot(int index) const` | 判断该成员是否是 slot。 | 一个成员的分类应稳定，避免 UI 显示前后不一致。 |
| 可见性 | `isVisible(int index) const` | 判断成员是否在 Designer 信号槽编辑器中显示。 | 只影响 Designer 呈现，不会禁用运行时 C++ 信号槽。 |
| 分组读取 | `memberGroup(int index) const` | 返回成员在 Designer 中的显示分组名。 | 分组名用于组织 UI，保持简洁且稳定。 |
| 名称读取 | `memberName(int index) const` | 返回成员函数名称。 | 通常是不带参数的函数名；完整参数签名由 `signature()` 提供。 |
| 参数名 | `parameterNames(int index) const` | 返回成员参数名列表。 | 列表顺序与 `parameterTypes()` 必须一一对应。 |
| 参数类型 | `parameterTypes(int index) const` | 返回成员参数类型列表。 | 使用 `QByteArray` 保存元对象风格类型名，顺序必须对应签名。 |
| 分组设置 | `setMemberGroup(int index, const QString &group)` | 修改成员在 Designer 中的显示分组。 | 仅改设计器分类；实现应保存修改后的分组状态。 |
| 可见性设置 | `setVisible(int index, bool visible)` | 显示或隐藏某成员在 Designer 信号槽编辑器中的条目。 | 不改变 C++ 成员本身的可调用性或元对象内容。 |
| 完整签名 | `signature(int index) const` | 返回成员函数完整签名。 | 应与参数类型、成员名和 signal/slot 类型协调；用于 Designer 的连接匹配。 |

## 易错点

1. 它控制的是 Designer 里的成员呈现，不会真的删除或禁用运行时信号槽。
2. `indexOf()` 返回的索引必须能被所有其他 `index` API 正确识别。
3. `memberName()` 和 `signature()` 不同：前者是名称，后者应包含参数信息。
4. 参数名与参数类型列表长度不一致会让 Designer 的成员描述失真。
5. 不要用它管理属性编辑器字段，属性应交给 `QDesignerPropertySheetExtension`。

### 一句话总结

`QDesignerMemberSheetExtension` 是自定义 widget 的信号槽成员目录：它让 Designer 知道成员的签名、类别、分组和可见性，而不改变这些成员在 C++ 运行时的真实行为。
