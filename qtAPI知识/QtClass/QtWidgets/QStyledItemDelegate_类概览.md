# Qt QStyledItemDelegate 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyledItemDelegate>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QAbstractItemDelegate -> QStyledItemDelegate`  
> 定位：标准项代理

## 1. 先建立整体认识：它解决什么问题

`QStyledItemDelegate` 是 item view 体系里的标准委托。视图本身不直接知道每一项该怎么画、该怎么编辑、编辑器该多大、编辑完成后怎么把值写回模型，这些工作由 delegate 接手。

它解决的是“模型提供数据，视图提供展示框架，委托负责单项呈现和编辑”的分工问题。没有 delegate，`QTableView`、`QTreeView` 这类视图就只能显示很基础的样子；有了 delegate，单元格可以按样式绘制，也可以弹出合适的编辑器。

```text
QAbstractItemView
  └─ QStyledItemDelegate
```

如果你想让表格、树或列表里的某一列支持日期编辑、下拉选择、颜色选择，delegate 往往就是入口。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 直接设置到视图上

```cpp
#include <QApplication>
#include <QTableView>
#include <QStandardItemModel>
#include <QStyledItemDelegate>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QStandardItemModel model(3, 2);
    QTableView view;
    QStyledItemDelegate *delegate = new QStyledItemDelegate(&view);
    view.setItemDelegate(delegate);
    view.setModel(&model);
    view.show();

    return app.exec();
}
```

### 2.3 改写显示文本

```cpp
class DateDelegate : public QStyledItemDelegate
{
public:
    using QStyledItemDelegate::QStyledItemDelegate;

    QString displayText(const QVariant &value, const QLocale &locale) const override
    {
        if (value.canConvert<QDateTime>())
            return locale.toString(value.toDateTime(), QLocale::ShortFormat);
        return QStyledItemDelegate::displayText(value, locale);
    }
};
```

`displayText()` 适合处理“数据显示成什么字”的问题，但它不负责模型里实际存的值。

## 3. 核心使用模型

### 3.1 绘制流程

视图在绘制每个 item 时，会构造一个 `QStyleOptionViewItem`，然后交给 delegate 的 `paint()`。delegate 再根据模型数据、选择状态、焦点状态和样式，把单元格画出来。

### 3.2 编辑流程

单元格进入编辑时，delegate 会按这个顺序工作：

1. `createEditor()` 创建编辑器；
2. `setEditorData()` 把模型值写进编辑器；
3. 用户编辑；
4. `setModelData()` 把编辑结果写回模型；
5. `updateEditorGeometry()` 决定编辑器放哪儿、占多大。

所以 delegate 不是“简单的回调”，它是真正控制编辑器生命周期的角色。

### 3.3 `QItemEditorFactory` 是类型到编辑器的映射

默认 delegate 可以通过 `QItemEditorFactory` 根据元类型挑选编辑器。比如日期类型可以用日期编辑器，整数可以用 spin box。这个工厂让你不用每个类型都手写 `createEditor()`。

`setItemEditorFactory()` 适合全局替换一个委托使用的编辑器策略；`QItemEditorFactory::setDefaultFactory()` 则会影响更广的默认行为。

### 3.4 `initStyleOption()` 是样式入口

`initStyleOption()` 负责把模型数据、装饰、对齐、状态等信息填进 `QStyleOptionViewItem`。它是 `paint()` 里的关键准备步骤。重写它时，要非常小心别把样式默认行为破坏掉。

## 4. 适合用在哪里

- 表格/树/列表里自定义某一列的编辑器；
- 把日期、枚举、颜色、布尔值显示成更适合人的样子；
- 统一某类 item 的绘制风格；
- 给复杂视图做局部交互增强。

如果你只是想改一个单元格的外观，先考虑代理；如果你想改整张表的结构或数据流，那是模型层的事。

## 5. 常见误区

### 5.1 把 delegate 当成模型

它不存业务数据，只负责展示和编辑流程。

### 5.2 只改 `paint()`，不管编辑器

这样常会出现“看起来像自定义了，但编辑时又恢复默认”的割裂感。

### 5.3 在 `setModelData()` 里做额外业务逻辑

这个函数应该主要负责把编辑结果写回模型。复杂业务最好放到模型或上层控制器里。

### 5.4 忘记调用基类 `initStyleOption()`

这会让很多默认样式信息丢失，单元格看起来会很怪。

### 5.5 把 `displayText()` 当成数据转换的唯一出口

它只影响显示文本，不改变模型里的真实值。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyledItemDelegate(QObject *parent = nullptr)` | 创建一个标准项代理。 | 常把视图或控制器作为父对象。 |
| 析构 | `~QStyledItemDelegate()` | 销毁项代理。 | delegate 一般由视图或父对象管理生命周期。 |
| 绘制 | `paint(...)` | 按样式和模型数据绘制单元格。 | 这是最核心的显示入口。 |
| 尺寸 | `sizeHint(...)` | 返回单元格推荐尺寸。 | 影响行高、列宽和布局。 |
| 编辑 | `createEditor(...)` | 为某个索引创建编辑器。 | 返回的控件通常会被视图临时管理。 |
| 编辑 | `setEditorData(...)` | 把模型数据写进编辑器。 | 编辑开始时调用。 |
| 编辑 | `setModelData(...)` | 把编辑器内容写回模型。 | 编辑结束提交时调用。 |
| 编辑 | `updateEditorGeometry(...)` | 计算编辑器在视图里的位置和大小。 | 位置错了会直接影响用户体验。 |
| 工厂 | `itemEditorFactory() const` | 返回当前使用的编辑器工厂。 | 为空时使用默认工厂。 |
| 工厂 | `setItemEditorFactory(QItemEditorFactory *factory)` | 设置当前委托使用的编辑器工厂。 | 要注意工厂对象的生命周期。 |
| 显示 | `displayText(const QVariant &value, const QLocale &locale) const` | 把数据值转成显示文本。 | 适合定制日期、数字、枚举的显示方式。 |
| 保护钩子 | `initStyleOption(QStyleOptionViewItem *option, const QModelIndex &index) const` | 填充绘制所需的样式选项。 | 重写时要保留默认样式信息。 |
| 事件 | `eventFilter(QObject *object, QEvent *event)` | 处理编辑器相关事件过滤。 | 通常用于处理编辑器键盘行为。 |
| 事件 | `editorEvent(QEvent *event, QAbstractItemModel *model, const QStyleOptionViewItem &option, const QModelIndex &index)` | 处理 item 本身的交互事件。 | 常用于复选框、按钮式单元格等交互。 |

## 7. 一句话总结

`QStyledItemDelegate` 是 item view 的标准单项代理，负责绘制、编辑器创建、数据回填和样式选项准备，是表格/树/列表自定义交互的核心入口。
