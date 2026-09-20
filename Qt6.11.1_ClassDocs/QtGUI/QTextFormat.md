# QTextFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextFormat`

## 1. 先建立直觉

`QTextFormat` 是 Qt 富文本格式系统的基类和值容器。字符格式、段落格式、列表格式、表格格式、图片格式等都建立在它的“属性表”之上。

它的核心不是某个具体外观，而是用整数 property id 保存 `QVariant` 值，并提供 type/object type 判断。

## 2. 类说明

- 头文件：`#include <QTextFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型
- 派生/相关：`QTextCharFormat`、`QTextBlockFormat`、`QTextFrameFormat`、`QTextImageFormat`、`QTextListFormat`、`QTextTableFormat`

具体格式类只是对常用 property 做了命名 API。自定义文本对象也常通过 `QTextFormat::setProperty()` 保存业务属性。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `type()` | 格式类型，如 char、block、frame、list、table |
| `objectType()` / `setObjectType()` | 自定义对象类型 |
| `property()` / `setProperty()` | 读写任意属性 |
| `hasProperty()` / `clearProperty()` | 查询或清除属性 |
| `properties()` | 取全部属性 |
| `propertyCount()` | 属性数量 |
| `boolProperty()` / `intProperty()` / `doubleProperty()` / `stringProperty()` | 按类型读取属性 |
| `lengthProperty()` / `lengthVectorProperty()` | 读取 `QTextLength` 属性 |
| `colorProperty()` / `brushProperty()` / `penProperty()` | 读取绘制相关属性 |
| `merge()` | 合并另一个格式中设置过的属性 |
| `isCharFormat()` 等判断函数 | 判断可否转换为具体格式 |
| `toCharFormat()` 等转换函数 | 转成具体格式对象 |

## 4. 关键用法

自定义 inline object 属性：

```cpp
QTextCharFormat fmt;
fmt.setObjectType(MyObjectType);
fmt.setProperty(MyObjectText, "E = mc^2");
cursor.insertText(QString(QChar::ObjectReplacementCharacter), fmt);
```

合并格式：

```cpp
QTextCharFormat patch;
patch.setForeground(Qt::red);
cursor.mergeCharFormat(patch);
```

`merge()` 只合并被设置的属性，这对工具栏“只改颜色不动字体”很重要。

## 5. 使用场景

- 统一处理各种 QText 格式。
- 给自定义文本对象存扩展属性。
- 实现格式复制、格式刷、富文本导入导出。
- 判断某个 format 是字符、块、列表还是表格。

## 6. 常见坑与经验

- 未设置的属性和设置为默认值不是一回事，`hasProperty()` 能区分。
- property id 要避开 Qt 内置范围，自定义属性用 `QTextFormat::UserProperty` 以上。
- `toCharFormat()` 只是值转换，不会验证 type 一定合理；先用 `isCharFormat()`。
- 大量自定义属性会进入文档格式系统，注意序列化和兼容性。

## 7. 知识点覆盖

本页覆盖：富文本属性表、格式类型、自定义属性、格式合并、具体格式转换、自定义 inline object 基础。
