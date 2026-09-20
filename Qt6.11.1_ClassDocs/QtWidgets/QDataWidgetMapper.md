# QDataWidgetMapper

> Qt 6.11.1 · Qt Widgets · 来自 `QDataWidgetMapper`

## 1. 先建立直觉

`QDataWidgetMapper` 把模型中的一行或一列映射到一组普通 QWidget 上。它像一个轻量表单绑定器：第 0 列绑定姓名输入框，第 1 列绑定年龄 spinbox，第 2 列绑定地址编辑框，然后用 `toNext()` 切换到下一条记录。

它适合主从表单、详情面板、数据库记录编辑、设置页和向导页。它不替代 `QTableView`，而是把同一个 model 的某条记录显示成表单。

## 2. 类说明

- 头文件：`#include <QDataWidgetMapper>`
- 模块：`Qt6::Widgets`
- 继承自：`QObject`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

mapper 不拥有 model，也不拥有被映射的 widgets。它通过 delegate 读写控件属性。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QDataWidgetMapper(parent)` | 创建映射器，默认水平映射、自动提交。 |
| `setModel()` / `model()` | 设置或读取数据模型。 |
| `addMapping(widget, section)` | 把 widget 映射到某列或某行。 |
| `addMapping(widget, section, propertyName)` | 指定 widget 用哪个属性读写数据。 |
| `removeMapping(widget)` | 移除某个 widget 的映射。 |
| `clearMapping()` | 清空所有映射。 |
| `mappedSection(widget)` | 查询 widget 映射到哪个 section。 |
| `mappedWidgetAt(section)` | 查询某 section 对应的 widget。 |
| `mappedPropertyName(widget)` | 查询 widget 使用的属性名。 |
| `setOrientation()` / `orientation()` | 水平表示控件映射到列，当前 index 代表行；垂直则相反。 |
| `setRootIndex()` / `rootIndex()` | 设置模型根索引，常用于层级模型的子区域。 |
| `setCurrentIndex()` / `currentIndex()` | 切换当前记录。 |
| `setCurrentModelIndex()` | 根据某个模型索引切换当前记录。 |
| `toFirst()` / `toLast()` | 跳到第一条或最后一条。 |
| `toNext()` / `toPrevious()` | 切换到下一条或上一条。 |
| `setSubmitPolicy()` / `submitPolicy()` | 自动提交或手动提交。 |
| `submit()` | 手动把 widgets 当前值写回 model。 |
| `revert()` | 丢弃 widgets 未提交修改，恢复 model 当前值。 |
| `setItemDelegate()` / `itemDelegate()` | 设置读写控件属性的 delegate。 |
| `currentIndexChanged(int)` | 当前记录变化信号。 |

## 4. 关键用法

### 水平映射是最常见表单

默认 `Qt::Horizontal` 表示每个 widget 对应一列，`currentIndex` 表示当前行。例如客户表中姓名、电话、邮箱三列分别映射到三个输入控件，`setCurrentIndex(5)` 就显示第 5 行客户。

`Qt::Vertical` 则相反：每个 widget 对应一行，`currentIndex` 表示当前列。它少见，但适合“字段在行、记录在列”的模型。

### 提交策略决定编辑体验

`AutoSubmit` 在控件失去焦点时写回 model，适合简单设置和即时保存。`ManualSubmit` 需要显式调用 `submit()`，适合有“确定/取消/应用”按钮的表单。切换 submit policy 会把控件恢复成 model 数据，别在用户编辑中途随意切换。

### 属性名很重要

默认属性来自 delegate/editor factory 的规则；对普通表单控件，显式传属性名通常更清楚：`QLineEdit` 用 `text`，`QSpinBox` 用 `value`，`QCheckBox` 用 `checked`。属性名错了，表单可能显示正常但提交失败。

### 和选择模型联动

常见主从界面会把 table view 的当前行连接到 mapper 的 `setCurrentModelIndex()`。这样左边选一行，右边表单显示详情。注意代理模型存在时，传给 mapper 的 index 要来自 mapper 使用的同一个 model，必要时做 proxy/source index 转换。

## 5. 常见坑与经验

- mapper 不会替你做数据校验；校验可放在 widget validator、delegate 或 model `setData()`。
- `ManualSubmit` 下忘记调用 `submit()`，界面看着改了，model 没变。
- 映射关系是一对一：一个 widget 不应映射多个 section。
- 更改 orientation 会清空已有映射。
- model reset 后要确认当前 index 和表单内容是否仍有效。
