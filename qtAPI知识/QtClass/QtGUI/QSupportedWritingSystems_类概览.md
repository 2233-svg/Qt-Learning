# Qt QSupportedWritingSystems：字体数据库的文字系统支持集合

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QtGui/qpa/qplatformfontdatabase.h>`  
> 所属模块：`Qt6::Gui` 的 QPA 私有接口  
> 继承：无  
> 类型定位：字体平台插件内部使用的值类型

## 1. 它解决什么问题

`QSupportedWritingSystems` 记录一个字体支持哪些文字系统，例如拉丁、西里尔、希腊、汉字、阿拉伯文或其他 `QFontDatabase::WritingSystem` 枚举项。

字体数据库扫描字体文件时，需要把 TrueType 的 Unicode range/code page 位图转换为 Qt 的 writing system 集合，然后把结果注册给 Qt。这个类就是这个中间值容器。

它不是应用层的“用户语言设置”，也不是 `QString` 是否能显示某个字符的完整保证。一个字体被标记支持某个 writing system，并不等于它覆盖该系统的全部字符、变体、emoji 或复杂排版特性。

## 2. 这是 QPA 私有 API

类定义位于：

```cpp
#include <QtGui/qpa/qplatformfontdatabase.h>
```

该头文件明确标记为 QPA API，不面向普通应用。使用它可能造成源代码和二进制不兼容，Qt 小版本升级也不保证接口稳定。

普通应用应优先使用公开的 `QFontDatabase`、`QFontInfo`、`QFontMetrics` 和字体回退机制，而不是直接依赖该类。

## 3. 结构和存储模型

`QSupportedWritingSystems` 是值类型，内部保存一组支持状态：

```text
WritingSystem -> bool
```

创建、复制和赋值不会关联字体对象，也不会加载字体文件。它只是一个集合快照。

## 4. 成员函数

### `QSupportedWritingSystems()`

创建空集合。没有显式调用 `setSupported()` 的 writing system 均不应被当作支持。

### `QSupportedWritingSystems(const QSupportedWritingSystems &other)`

复制集合值。它复制支持状态，不复制字体数据库、文件句柄或平台资源。

### `QSupportedWritingSystems &operator=(const QSupportedWritingSystems &other)`

复制赋值，使目标集合具有源集合的支持状态。

### `~QSupportedWritingSystems()`

销毁值对象和内部集合数据，不影响字体数据库中已经注册的字体。

### `void setSupported(QFontDatabase::WritingSystem writingSystem, bool supported = true)`

设置指定 writing system 是否支持：

```cpp
systems.setSupported(QFontDatabase::Latin);
systems.setSupported(QFontDatabase::Cyrillic, false);
```

第二个参数默认为 `true`。它只修改当前集合，不会自动扫描字体，也不会通知 `QFontDatabase` 注册新字体。

### `bool supported(QFontDatabase::WritingSystem writingSystem) const`

查询指定 writing system 是否被标记为支持。它回答的是集合状态，不是对任意字符进行实际 glyph 覆盖测试。

## 5. 实际使用场景

### 5.1 QPA 字体数据库注册

平台字体插件可以在扫描字体后构造集合，再把它传给 Qt 内部注册函数：

```cpp
QSupportedWritingSystems systems;
systems.setSupported(QFontDatabase::Latin);
systems.setSupported(QFontDatabase::Han);
```

此流程属于 Qt 平台集成代码，普通应用不应模仿 QPA 私有调用链。

### 5.2 从字体文件位图推导集合

`QPlatformFontDatabase` 还提供从 TrueType 表格位图推导 `QSupportedWritingSystems` 的静态辅助函数，但这些函数和本类一样属于 QPA 私有接口。真正的字体覆盖仍可能需要逐字符或 shaping 级别验证。

## 6. 复制、比较和调试

QPA 头文件还声明：

- `operator==`；
- `operator!=`；
- `operator<<`，在未禁用 debug stream 时可用。

相等比较适合测试字体扫描结果是否变化。debug 输出适合平台插件日志，不是稳定序列化格式。

## 7. 与公开字体 API 的区别

| 类型 | 面向对象 | 适合用途 |
| --- | --- | --- |
| `QSupportedWritingSystems` | Qt QPA 字体插件 | 保存扫描出的文字系统位图结果 |
| `QFontDatabase` | 应用层公开 API | 查询字体家族、样式、writing system |
| `QFontInfo` | 应用层公开 API | 查询实际选择的字体信息 |
| `QFontMetrics` | 应用层公开 API | 测量绘制结果 |

`supported()` 返回 true 时，仍可能因为字形缺失、字体回退、语言 shaping 或 variation selector 导致实际显示效果不同。

## 8. 生命周期、线程和所有权

它是普通值类型，不是 QObject。平台字体数据库一般在 Qt 字体系统初始化期间使用，调用方不拥有外部字体资源。

如果平台插件在多个线程扫描字体，应让集合在单一线程构造完成后再按值传递，并由字体数据库注册路径负责同步。普通应用不要因为它是值类型就直接跨线程操作 QPA 字体数据库。

## 9. 常见误区

- 在普通应用中包含 QPA 私有头文件，把它当成稳定公开 API。
- 把 writing system 支持当成所有字符都有 glyph。
- 认为 `setSupported()` 会修改 QFontDatabase 全局状态。
- 把集合复制当成字体文件或字体引擎复制。
- 用 debug 输出作为跨版本持久化格式。
- 忽略字体回退、复杂脚本 shaping 和 emoji 覆盖差异。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QSupportedWritingSystems()` | 创建空支持集合 | 不扫描字体 |
| 构造 | `QSupportedWritingSystems(const QSupportedWritingSystems &)` | 复制集合 | 只复制状态 |
| 赋值 | `operator=(const QSupportedWritingSystems &)` | 复制集合 | 不注册字体 |
| 析构 | `~QSupportedWritingSystems()` | 销毁值对象 | 不影响字体数据库 |
| 设置 | `setSupported(WritingSystem, bool)` | 设置某文字系统支持状态 | 只改当前集合；默认 true |
| 查询 | `supported(WritingSystem) const` | 查询集合标记 | 不保证每个字符有 glyph |
| 比较 | `operator==` | 比较集合状态 | 不是实际渲染效果比较 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |
| 调试 | `operator<<` | 输出调试信息 | 非稳定序列化格式 |
| 兼容性 | `qplatformfontdatabase.h` | 提供类声明 | QPA 私有 API，不建议普通应用依赖 |

---

### 一句话总结

`QSupportedWritingSystems` 是 QPA 字体平台插件用来保存“某字体被扫描为支持哪些文字系统”的值类型；它不是稳定公开 API，也不等价于逐字符 glyph 覆盖，普通应用应优先使用 `QFontDatabase` 等公开字体接口。
