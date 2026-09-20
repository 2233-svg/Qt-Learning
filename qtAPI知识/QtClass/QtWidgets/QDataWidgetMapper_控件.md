# Qt QDataWidgetMapper 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QDataWidgetMapper>`
> 所属模块：`Qt6::Widgets`
> 继承：`QObject -> QDataWidgetMapper`
> 常见搭档：`QAbstractItemModel`、`QAbstractItemDelegate`、`QWidget`

## 1. QDataWidgetMapper 解决什么问题

`QDataWidgetMapper` 用来把模型的一行或一列数据，映射到一组普通控件上。它解决的是“表单控件和模型数据之间怎么对上”的问题。

适合的场景：

- 主从详情页；
- 表格选中一行，右侧表单显示详情；
- 表单控件直接编辑模型字段；
- 不想自己手写一堆 `setText()` / `text()` 同步代码。

它不是模型，也不是视图。它更像一个“翻译器”：一边读模型，一边把值塞进 widget；反过来又把 widget 的值写回模型。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QDataWidgetMapper>
#include <QLineEdit>
#include <QStandardItemModel>
#include <QSpinBox>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    auto *model = new QStandardItemModel(3, 2);
    model->setData(model->index(0, 0), "Alice");
    model->setData(model->index(0, 1), 18);

    auto *nameEdit = new QLineEdit;
    auto *ageSpin = new QSpinBox;

    auto *mapper = new QDataWidgetMapper;
    mapper->setModel(model);
    mapper->addMapping(nameEdit, 0);
    mapper->addMapping(ageSpin, 1);
    mapper->toFirst();

    QWidget window;
    auto *layout = new QVBoxLayout(&window);
    layout->addWidget(nameEdit);
    layout->addWidget(ageSpin);
    window.show();

    return app.exec();
}
```

这段代码里真正重要的不是控件本身，而是 `addMapping()` 把“哪个控件对应模型哪一列”说清楚了。

## 3. 映射规则

### 3.1 orientation

```cpp
mapper->setOrientation(Qt::Horizontal);
```

默认是水平映射：一个 section 对应模型的“列”，`currentIndex` 对应行。  
如果改成 `Qt::Vertical`，section 就对应行，`currentIndex` 对应列。

切换 orientation 会清空已有映射，所以这不是轻量切换，别在已经配好映射后随便改。

### 3.2 addMapping

```cpp
mapper->addMapping(nameEdit, 0);
mapper->addMapping(ageSpin, 1);
mapper->addMapping(customWidget, 2, "value");
```

不传 `propertyName` 时，会使用控件的 user property。  
传了 `propertyName` 就按指定属性读写，适合自定义控件。

### 3.3 rootIndex

```cpp
mapper->setRootIndex(treeView->currentIndex());
```

这让 mapper 可以只处理树模型某个分支下面的子项。  
适合“树里选一个节点，右侧表单编辑这个节点的子数据”。

## 4. 提交策略

```cpp
mapper->setSubmitPolicy(QDataWidgetMapper::AutoSubmit);
mapper->setSubmitPolicy(QDataWidgetMapper::ManualSubmit);
```

- `AutoSubmit`：控件失去焦点就写回模型；
- `ManualSubmit`：必须手动调用 `submit()`。

`ManualSubmit` 特别适合对话框：用户可以改很多项，最后点确定才统一提交；如果点取消，就调用 `revert()` 回滚。

```cpp
mapper->submit();
mapper->revert();
```

`submit()` 会把所有映射控件的当前值写回模型，并调用模型的 `submit()`；  
`revert()` 则把控件重新填回模型当前值。

## 5. 和视图联动

```cpp
connect(tableView->selectionModel(), &QItemSelectionModel::currentRowChanged,
        mapper, &QDataWidgetMapper::setCurrentModelIndex);
```

`setCurrentModelIndex()` 是最实用的联动入口。  
表格当前行一变，mapper 就把那一行的数据同步到表单。

导航槽也很常用：

```cpp
mapper->toFirst();
mapper->toNext();
mapper->toPrevious();
mapper->toLast();
```

它们都只是帮你换当前索引，不会改变模型结构。

## 6. delegate 和所有权

```cpp
mapper->setItemDelegate(new QStyledItemDelegate);
```

`QDataWidgetMapper` 用 delegate 在 model 和 widget 之间转值。

但要注意：`setItemDelegate()` 不接管所有权，旧 delegate 只会被移除，不会自动 delete。  
这和 `setProxyModel()`、`setWidget()` 这种“直接接管”的接口不一样。

## 7. 适合什么时候用

适合：

- 一个模型行对应一组表单控件；
- 需要少量控件映射；
- 想复用 model/view 数据流，但界面是表单不是表格。

不适合：

- 你要显示一整个表格，那应该用 `QTableView`；
- 你要自己维护复杂双向同步，手写会更透明；
- 映射关系特别动态，控件经常增删，mapper 反而会绕。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDataWidgetMapper(QObject *parent = nullptr)` | 创建模型到控件的映射器。 | 默认水平映射、自动提交；它本身不显示界面。 |
| 析构 | `~QDataWidgetMapper()` | 销毁映射器。 | 不负责删除外部模型、控件和 delegate。 |
| 模型 | `setModel(QAbstractItemModel *model)` / `model() const` | 设置或读取映射器的数据模型。 | 模型必须在映射前准备好对应行列和角色数据。 |
| 委托 | `setItemDelegate(QAbstractItemDelegate *delegate)` / `itemDelegate() const` | 设置模型值与控件属性之间的转换器。 | mapper 不接管 delegate 所有权，生命周期要单独管理。 |
| 根索引 | `setRootIndex(const QModelIndex &index)` / `rootIndex() const` | 限制映射器只浏览某个模型分支。 | 树模型详情页很有用；根索引改变后要重新检查当前索引。 |
| 方向 | `setOrientation(Qt::Orientation aOrientation)` / `orientation() const` | 设置 section 对应模型行还是列。 | 水平通常是 section=列、currentIndex=行；切换会清空已有映射。 |
| 提交策略 | `setSubmitPolicy(SubmitPolicy policy)` / `submitPolicy() const` | 设置控件修改何时写回模型。 | `ManualSubmit` 更适合“确定提交、取消回滚”的对话框。 |
| 类型 | `SubmitPolicy` | 定义自动提交或手动提交策略。 | 策略改变会影响焦点丢失时的模型更新时机。 |
| 枚举值 | `AutoSubmit` | 控件编辑后按 mapper 规则自动写回模型。 | 适合直接编辑详情页；仍要考虑 delegate 的提交时机。 |
| 枚举值 | `ManualSubmit` | 只有调用 `submit()` 时才统一写回模型。 | 配合取消按钮调用 `revert()`。 |
| 映射 | `addMapping(QWidget *widget, int section)` | 把控件映射到指定 section，并使用控件 user property。 | 普通 Qt 控件最方便；自定义控件可能没有合适的 user property。 |
| 映射 | `addMapping(QWidget *widget, int section, const QByteArray &propertyName)` | 显式指定控件用于读写的属性。 | 自定义控件和非 user property 场景必须明确属性名。 |
| 映射 | `removeMapping(QWidget *widget)` | 移除一个控件的映射关系。 | 不删除控件，也不修改模型。 |
| 映射 | `clearMapping()` | 清空所有控件映射。 | 切换表单结构时使用；清空后要重新 addMapping。 |
| 映射查询 | `mappedSection(QWidget *widget) const` | 查询控件映射到哪个 section。 | 未映射返回 -1。 |
| 映射查询 | `mappedPropertyName(QWidget *widget) const` | 查询控件使用的属性名。 | 排查“控件有值但模型不更新”时很有用。 |
| 映射查询 | `mappedWidgetAt(int section) const` | 按 section 反查对应控件。 | 没有映射时返回空指针。 |
| 当前项 | `currentIndex() const` / `setCurrentIndex(int index)` | 读取或设置当前映射行/列。 | 改变后 mapper 会刷新所有映射控件。 |
| 当前项 | `setCurrentModelIndex(const QModelIndex &index)` | 用具体模型索引切换当前项。 | 常与 `QItemSelectionModel::currentChanged` 连接。 |
| 信号 | `currentIndexChanged(int index)` | 当前映射索引变化时通知。 | 用于更新上一条/下一条按钮和详情标题。 |
| 提交 | `submit()` | 把所有映射控件的值写回模型。 | 返回 `false` 表示提交失败；确认按钮常调用它。 |
| 回滚 | `revert()` | 用模型当前值重新填充映射控件，丢弃未提交修改。 | 取消编辑前调用；不会恢复到更早的历史版本。 |
| 导航 | `toFirst()` / `toLast()` / `toNext()` / `toPrevious()` | 在模型记录之间切换当前项。 | 到边界时不会创建新记录，也不会改变模型结构。 |

### 一句话总结

`QDataWidgetMapper` 负责把“模型的一行或一列”翻译成“表单里的几件控件”，它最适合的不是复杂表格，而是详情页、编辑页和主从联动。
