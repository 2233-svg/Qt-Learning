# QDesignerWidgetBoxInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerWidgetBoxInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：`QWidget`

## 它解决什么问题

`QDesignerWidgetBoxInterface` 是 Qt Widgets Designer “控件盒”面板的接口。控件盒是 Designer 左侧或侧边栏中按分类列出可拖拽控件的区域，例如 Buttons、Containers、Display Widgets。

这个接口专门管理控件盒的 **XML 持久化文件**：

- `fileName()` 查询当前用于填充控件盒的 XML 文件；
- `load()` 从当前 XML 文件载入或重新载入控件盒内容；
- `save()` 把当前控件盒内容写回当前 XML 文件；
- `setFileName()` 只更换目标文件名，实际内容要再调用 `load()` 才会刷新。

它不应直接实例化。自定义 widget 插件可从初始化得到的 form editor 调用 `core->widgetBox()` 取得现有面板。

## 为什么 `setFileName()` 后必须 `load()`

`setFileName()` 只改变“接下来要读写哪个 XML 文件”的状态，并不会立即解析新文件。因此以下流程缺一不可：

```cpp
auto *widgetBox = core->widgetBox();
widgetBox->setFileName("D:/designer/widgetbox-custom.xml");

if (!widgetBox->load()) {
    // 文件不可读、XML 格式错误或内容无效时处理失败。
}
```

同样，`save()` 将内容写入 **当前** `fileName()` 指向的文件。若要保留原控件盒配置，应先保存旧路径，换到新路径再保存：

```cpp
const QString originalFile = widgetBox->fileName();
widgetBox->setFileName("D:/designer/widgetbox-custom.xml");
widgetBox->save();

widgetBox->setFileName(originalFile);
widgetBox->load();
```

## 使用场景与边界

它适合为团队提供一套固定的控件分类和自定义控件入口，或者由 IDE 维护不同项目的控件盒配置。

它不是自定义 widget 的注册接口。让 Designer 识别编译好的自定义控件应实现 `QDesignerCustomWidgetInterface` 并提供插件；控件盒 XML 管的是面板展示和分类。文件读写失败要检查 `bool` 返回值，不能假设 XML 一定可用。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDesignerWidgetBoxInterface(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())` | 构造控件盒接口 widget。 | 实际使用中由 Designer 创建，通过 `core->widgetBox()` 获取。 |
| 析构 | `~QDesignerWidgetBoxInterface()` | 销毁控件盒接口。 | 从 Designer 取得的指针不转移所有权。 |
| 当前文件 | `fileName() const` | 返回当前用于填充控件盒的 XML 文件名。 | 该路径同时决定 `load()` 的读取目标和 `save()` 的写入目标。 |
| 载入 | `load()` | 从当前 XML 文件填充或重新填充控件盒，成功返回 `true`。 | `setFileName()` 后必须调用；失败时不要假定旧内容已被正确替换。 |
| 保存 | `save()` | 将当前控件盒内容写入当前 XML 文件，成功返回 `true`。 | 先确认 `fileName()`，否则可能覆盖原配置；检查写权限和返回值。 |
| 更换文件 | `setFileName(const QString &fileName)` | 设置控件盒将使用的 XML 文件。 | 只修改路径，不刷新显示；需要随后调用 `load()`。 |

## 易错点

1. `setFileName()` 后不调用 `load()`，控件盒不会切换到新文件的内容。
2. `save()` 保存到当前文件名，换文件前不备份路径容易覆盖默认配置。
3. 控件盒 XML 不代替自定义 widget 插件的注册和实现。
4. `load()`、`save()` 都可能失败，必须处理返回值。

### 一句话总结

`QDesignerWidgetBoxInterface` 是 Designer 控件盒的 XML 配置接口，用来查询、切换、载入和保存控件盒内容。
