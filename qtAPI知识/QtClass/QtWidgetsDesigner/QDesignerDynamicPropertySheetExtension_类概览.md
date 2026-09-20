# QDesignerDynamicPropertySheetExtension 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerDynamicPropertySheetExtension>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerDynamicPropertySheetExtension` 是 `QDesignerPropertySheetExtension` 的补充接口，用来让 Qt Widgets Designer 添加、识别和删除动态属性。

动态属性是 `QObject::setProperty()` 可以在运行时附加、但没有写在类 `Q_PROPERTY` 声明中的属性。例如：

```cpp
widget->setProperty("validationRule", "email");
```

`validationRule` 不需要出现在 widget 的 C++ 元对象中，也可以存在于对象上。这个接口决定 Designer 是否允许用户创建这类属性，以及创建后如何把它纳入 property sheet 的索引模型。

它适合插件要允许设计者附加可配置的扩展键值，或需要对动态属性的名称、类型与删除权限施加约束的情况。若 widget 不应支持动态属性，应通过 `dynamicPropertiesAllowed()` 返回 `false`。

## 与普通属性表的关系

动态属性并不是一套独立属性编辑器。它们最终仍会作为 property sheet 中的条目出现，因此实现这个接口时通常需要和 `QDesignerPropertySheetExtension` 使用相同的属性索引空间。

换句话说：

- `addDynamicProperty()` 成功返回的索引，应能被 property sheet 的 `propertyName(index)`、`property(index)` 等 API识别；
- `isDynamicProperty(index)` 用来告诉 Designer 这一项不是编译期 `Q_PROPERTY`；
- `removeDynamicProperty(index)` 移除后，property sheet 的数量和索引映射也要同步更新。

## 添加前为什么先检查名称

`canAddDynamicProperty(name)` 不只是“这个名字好不好看”。它应检查名称是否有效且唯一，至少避免：

- 空名称；
- 与已有普通属性或动态属性冲突；
- 不符合插件约束的保留前缀；
- 会被格式、代码生成或 UI 保存流程误解的名称。

`addDynamicProperty()` 失败时返回 `-1`，调用方不能把 `-1` 当作有效 property sheet 索引继续调用其它属性 API。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QDesignerDynamicPropertySheetExtension()` | 销毁动态属性表扩展接口。 | 通常与普通 property sheet 一起由 Designer 扩展系统提供。 |
| 新增动态属性 | `addDynamicProperty(const QString &propertyName, const QVariant &value)` | 新增指定名称和值的动态属性，并返回其属性索引。 | 成功返回有效索引，失败返回 `-1`；成功后必须同步普通 property sheet 的属性索引模型。 |
| 新增前校验 | `canAddDynamicProperty(const QString &propertyName) const` | 判断名称是否可作为新的动态属性名。 | 应检查名称合法性和唯一性，也应避免覆盖已有 `Q_PROPERTY`。 |
| 总开关 | `dynamicPropertiesAllowed() const` | 判断当前 widget 是否允许 Designer 创建动态属性。 | 返回 `false` 时 Designer 不应提供添加动态属性功能。 |
| 动态属性判断 | `isDynamicProperty(int index) const` | 判断 property sheet 中指定索引项是否为动态属性。 | 索引应来自同一 property sheet；删除后不要继续使用旧索引。 |
| 删除动态属性 | `removeDynamicProperty(int index)` | 移除指定索引的动态属性，成功返回 `true`。 | 只能删除动态属性；成功后更新属性数、名称映射与 UI 保存状态。 |

## 易错点

1. 动态属性不是 `Q_PROPERTY`，它们通常没有编译期 getter、setter 或 notify 信号。
2. `addDynamicProperty()` 返回 `-1` 表示失败，不能继续传给 `property(index)` 等 API。
3. 动态属性和普通属性共享 property sheet 语义，新增或删除时一定要维护索引一致性。
4. 删除属性会改变属性集合，外部缓存的索引可能失效。
5. 不想让设计者随意写键值时，应明确让 `dynamicPropertiesAllowed()` 返回 `false`，而不是只在 add 时静默失败。

### 一句话总结

`QDesignerDynamicPropertySheetExtension` 让 Designer 安全地管理没有 `Q_PROPERTY` 声明的对象属性：先判断能否添加，再以稳定索引加入 property sheet，并在删除时同步整个属性模型。
