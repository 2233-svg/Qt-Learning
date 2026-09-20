# Qt Widgets 基础（上）：布局协商与标准布局

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Widgets  
> 核心类型：`QLayout`、`QLayoutItem`、`QBoxLayout`、`QGridLayout`、`QFormLayout`、`QStackedLayout`、`QSpacerItem`

## 1. 布局不是“自动算坐标”这么简单

布局是约束协商系统。父控件给出可用区域后，布局综合每个子项的：

- `minimumSize`；
- `sizeHint`；
- `maximumSize`；
- `QSizePolicy`；
- stretch；
- alignment；
- `heightForWidth`；
- 行列最小值；
- 内容边距和间距；

最终为每个子项分配 geometry。

```text
父控件可用矩形
  ├─ 扣除 contentsMargins
  ├─ 扣除 spacing
  ├─ 满足子项 minimumSize
  ├─ 尽量靠近 sizeHint
  ├─ 按 sizePolicy + stretch 分剩余空间
  └─ 不超过 maximumSize，并应用 alignment
```

因此布局问题不能只看某一个 stretch 数字。

## 2. 为什么不能依赖固定坐标

```cpp
label->setGeometry(10, 10, 80, 24);
edit->setGeometry(100, 10, 200, 24);
```

这在以下变化后容易失效：

- 用户调整窗口；
- 系统 DPI 改变；
- 字体大小改变；
- 翻译文本变长；
- 样式边距不同；
- 控件动态显示或隐藏；
- 无障碍设置放大界面。

布局把这些变量交给统一算法处理。

## 3. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 4. 最小可用代码：组合布局

```cpp
#include <QApplication>
#include <QFormLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;

    auto *nameEdit = new QLineEdit;
    auto *emailEdit = new QLineEdit;

    auto *form = new QFormLayout;
    form->addRow("姓名：", nameEdit);
    form->addRow("邮箱：", emailEdit);

    auto *buttons = new QHBoxLayout;
    buttons->addStretch();
    buttons->addWidget(new QPushButton("取消"));
    buttons->addWidget(new QPushButton("保存"));

    auto *mainLayout = new QVBoxLayout(&window);
    mainLayout->addLayout(form);
    mainLayout->addStretch();
    mainLayout->addLayout(buttons);

    window.resize(440, 240);
    window.show();
    return app.exec();
}
```

一个 Widget 只能有一个顶层 Layout，但 Layout 可以嵌套任意层次。

## 5. QLayout 与 QLayoutItem

`QLayout` 本身也是 `QLayoutItem`，所以布局能嵌套在另一个布局中。

```text
QLayoutItem
  ├─ QWidgetItem：包装 QWidget
  ├─ QSpacerItem：空白和伸缩项
  └─ QLayout：包装一组子项
       ├─ QBoxLayout
       ├─ QGridLayout
       ├─ QFormLayout
       └─ QStackedLayout
```

布局内部统一操作 Item，而不是只操作 Widget。

```cpp
for (int i = 0; i < layout->count(); ++i) {
    QLayoutItem *item = layout->itemAt(i);
    if (QWidget *widget = item->widget()) {
        // Widget item
    } else if (QLayout *child = item->layout()) {
        // Nested layout
    } else if (QSpacerItem *spacer = item->spacerItem()) {
        // Spacer
    }
}
```

## 6. 设置顶层布局

两种常见方式：

```cpp
auto *layout = new QVBoxLayout(&window);
```

```cpp
auto *layout = new QVBoxLayout;
window.setLayout(layout);
```

不要给同一个 Widget 设置第二个顶层布局。需要切换结构时修改现有布局的内容，或创建新的容器 Widget。

对 `QMainWindow` 不使用普通 `setLayout()`，而是给 central widget 设置布局。

## 7. 谁负责所有权

### 7.1 Widget

把 Widget 加入布局时，布局会确保它成为布局所属父 Widget 的子控件。真正删除 Widget 的仍是 QObject 父子树，不是“布局项”概念本身。

```cpp
layout->addWidget(button);
```

### 7.2 子布局

加入父布局后，父布局接管子布局对象：

```cpp
mainLayout->addLayout(rowLayout);
```

### 7.3 remove 不等于 delete

```cpp
layout->removeWidget(widget);
```

只停止布局管理，一般不会删除 Widget，也不会自动把它隐藏。随后应明确：

```cpp
widget->hide();
widget->deleteLater();
```

或把它加入另一个布局。

## 8. sizeHint、最小值和最大值

布局试图把尺寸保持在：

```text
minimumSize <= 实际尺寸 <= maximumSize
```

并尽量参考 sizeHint。显式 `setMinimumSize()` 会形成硬限制；`minimumSizeHint()` 只是控件建议，可能受 size policy 影响。

```cpp
QSize wanted = widget->sizeHint();
QSize minimum = widget->minimumSizeHint();
```

自定义控件内容变化后：

```cpp
updateGeometry();
```

否则父布局可能继续使用旧的缓存建议。

## 9. QSizePolicy 与 stretch

Size Policy 回答“控件愿不愿在水平/垂直方向缩放”；stretch 回答“多个有资格扩展的项如何分额外空间”。

```cpp
editor->setSizePolicy(QSizePolicy::Expanding,
                      QSizePolicy::Expanding);
layout->addWidget(sidebar, 1);
layout->addWidget(editor, 3);
```

在其他约束允许时，剩余主轴空间近似按 1:3 分配，但这不是绝对宽度比例。最小值、size hint、最大值和不可扩展策略都会先参与。

### 9.1 alignment 会改变填充行为

```cpp
layout->addWidget(button, 0, Qt::AlignRight);
```

无 alignment 时，控件通常填充布局分配的单元格；设置 alignment 后，控件可能只取 sizeHint 大小并在单元格中对齐。

## 10. 内容边距与间距

```cpp
layout->setContentsMargins(12, 12, 12, 12);
layout->setSpacing(8);
```

- contentsMargins：布局内容与父控件边缘的距离；
- spacing：布局内部相邻 Item 的距离；
- QWidget 自身也有 contentsMargins，两层边距可以叠加。

不设置时通常由当前 QStyle 提供平台合适值。应用界面不应为每个布局任意设成 0。

Qt 6.1 起可 `unsetContentsMargins()` 恢复样式默认值。

## 11. QBoxLayout：沿一条轴排列

```text
QBoxLayout
  ├─ QHBoxLayout：水平
  └─ QVBoxLayout：垂直
```

```cpp
row->addWidget(label);
row->addSpacing(8);
row->addWidget(edit, 1);
row->addStretch();
row->addWidget(button);
```

四类 Item：Widget、子 Layout、固定空白、可伸缩 Spacer。

### 11.1 addStretch 与 stretch参数

```cpp
layout->addWidget(left, 1);
layout->addWidget(right, 2);
layout->addStretch(1);
```

Spacer 也参与剩余空间分配。若按钮被意外推远，检查是否存在 stretch 或 Expanding Spacer。

### 11.2 方向

通用 QBoxLayout 支持：

- `LeftToRight`；
- `RightToLeft`；
- `TopToBottom`；
- `BottomToTop`。

主轴决定 stretch 分配的是宽度还是高度。

> 本目录已有《QBoxLayout深入笔记.md》，其中对 add/insert、stretch、spacing、strut 和移除有更完整的单类讲解。本章继续聚焦它与其他布局的统一模型。

## 12. QGridLayout：行列网格

```cpp
auto *grid = new QGridLayout;
grid->addWidget(nameLabel, 0, 0);
grid->addWidget(nameEdit, 0, 1);
grid->addWidget(notesEdit, 1, 0, 1, 2); // 跨两列
```

参数：

```cpp
addWidget(widget, row, column,
          rowSpan, columnSpan, alignment);
```

适合真正具有二维对齐关系的界面，如仪表盘、矩阵和复杂表单。

### 12.1 行列 stretch

```cpp
grid->setColumnStretch(0, 0);
grid->setColumnStretch(1, 1);
grid->setRowStretch(2, 1);
```

额外空间只给有扩展能力的行列。还可设置最低尺寸：

```cpp
grid->setColumnMinimumWidth(0, 100);
grid->setRowMinimumHeight(1, 40);
```

### 12.2 间距

```cpp
grid->setHorizontalSpacing(12);
grid->setVerticalSpacing(6);
```

未单独设置时继承统一 spacing 或样式值。

### 12.3 跨行列不是绝对比例

一个跨两列控件的 size hint 会参与相关列的协商，但不能凭跨列数推断每列一定同宽。相同宽度应明确设置相同 stretch 和最低宽度。

### 12.4 原点角落

```cpp
grid->setOriginCorner(Qt::TopLeftCorner);
```

结合 layoutDirection 会影响视觉方向。支持 RTL 时不要靠反转列号硬编码镜像。

## 13. QFormLayout：语义化表单

```cpp
auto *form = new QFormLayout;
form->addRow(tr("用户名："), new QLineEdit);
form->addRow(tr("密码："), passwordEdit);
form->addRow(errorLabel); // 跨两列
```

它有三种 ItemRole：

- `LabelRole`；
- `FieldRole`；
- `SpanningRole`。

相比手写 Grid，FormLayout 会根据平台风格处理标签对齐、间距和换行策略。

### 13.1 自动 Buddy

字符串重载会创建 QLabel，并把字段设为 buddy：

```cpp
form->addRow(tr("&名称："), nameEdit);
```

用户可用助记键把焦点移到字段。

### 13.2 FieldGrowthPolicy

```cpp
form->setFieldGrowthPolicy(
    QFormLayout::AllNonFixedFieldsGrow);
```

常见策略：

- `FieldsStayAtSizeHint`；
- `ExpandingFieldsGrow`；
- `AllNonFixedFieldsGrow`。

它决定字段列是否利用额外宽度，仍受字段自身 size policy 限制。

### 13.3 RowWrapPolicy

```cpp
form->setRowWrapPolicy(QFormLayout::WrapLongRows);
```

- `DontWrapRows`：标签和字段保持一行；
- `WrapLongRows`：空间不足时换行；
- `WrapAllRows`：字段始终放到标签下一行。

这对窄窗口、较长翻译和大字体非常重要。

### 13.4 removeRow 与 takeRow

删除整行：

```cpp
form->removeRow(row);
```

`removeRow()` 会移除并删除该行的 Widget 和子 Layout。需要保留内容时使用 `takeRow()`，检查返回的 labelItem/fieldItem，并自行安排所有权。

这一行为和多数 `removeWidget()` 不同，调用前必须核对。

## 14. QStackedLayout：多个页面共用一个区域

```cpp
auto *stack = new QStackedLayout;
stack->addWidget(emptyPage);
stack->addWidget(contentPage);
stack->setCurrentWidget(contentPage);
```

默认 `StackOne` 一次显示一页。`StackAll` 会让所有页面可见并叠放，适合覆盖层等特殊场景：

```cpp
stack->setStackingMode(QStackedLayout::StackAll);
```

QStackedLayout 没有自带导航控件。用按钮、列表或状态机控制当前页。需要现成 Tab 导航时使用 QTabWidget。

### 14.1 页面身份

动态插入删除后 index 会变化。长期业务逻辑优先保存页面指针或稳定 ID，再通过 `indexOf()` 查询当前索引。

## 15. Spacer 与 addStretch

显式 Spacer：

```cpp
layout->addItem(new QSpacerItem(
    20, 40,
    QSizePolicy::Minimum,
    QSizePolicy::Expanding));
```

快捷方式：

```cpp
box->addSpacing(12); // 固定主轴空白
box->addStretch(1);  // 可伸缩主轴空白
```

不要用空 QLabel 制造间距；它有字体、size hint 和可访问语义，不是纯布局 Item。

## 16. heightForWidth

自动换行文本的理想高度取决于实际宽度：

```text
宽度大 → 行数少 → 高度小
宽度小 → 行数多 → 高度大
```

布局通过：

```cpp
item->hasHeightForWidth();
item->heightForWidth(width);
```

完成这种双向协商。自定义控件实现时应保证计算快速、确定，并在内容变化后 `updateGeometry()`。

## 17. 隐藏控件与布局

普通 Widget 隐藏后，布局通常会暂时忽略它的占位：

```cpp
advancedPanel->setVisible(showAdvanced);
```

但外层固定尺寸、Spacer、显式 row minimum 或其他 Item 仍可能保留空白。发现空洞时要检查整条布局树，而不是只检查隐藏控件。

`QSizePolicy::retainSizeWhenHidden` 可以要求隐藏后仍保留尺寸：

```cpp
QSizePolicy policy = widget->sizePolicy();
policy.setRetainSizeWhenHidden(true);
widget->setSizePolicy(policy);
```

## 18. LayoutDirection 与国际化

左右方向应尊重应用布局方向：

```cpp
QApplication::layoutDirection();
```

使用语义性布局和 `AlignLeading` / `AlignTrailing`，而不是处处硬编码 Left/Right。RTL 语言下，水平 Box、Form 标签和部分控件会自动镜像。

垂直方向和真正的物理位置需求仍需明确判断。

## 19. 选择标准布局h

| 结构        | 首选                   |
| --------- | -------------------- |
| 单行或单列     | Box                  |
| 工具条式一维组合  | Box                  |
| 二维矩阵、跨单元格 | Grid                 |
| 标签 + 字段   | Form                 |
| 同区域多页面    | Stacked              |
| 任意流式换行    | 自定义 FlowLayout 或合适视图 |

不要为了“统一”把所有界面都塞进 Grid。让布局结构对应界面语义，维护时更容易看懂。

## 20. 常见错误

### 20.1 一个 Widget 设置两个顶层布局

只能有一个。把第二个布局嵌入第一个，或创建子容器。

### 20.2 addWidget 后继续手动 move

布局会再次覆盖 geometry。通过布局参数表达位置。

### 20.3 stretch 没有效果

检查最大尺寸、size policy、alignment、其他 stretch 和父级可用空间。

### 20.4 边距重复

父 Layout、子 Layout、容器 Widget 和 Style Sheet padding 可能叠加。逐层检查。

### 20.5 removeWidget 后对象仍显示

remove 只解除布局管理。还需 hide、转移或删除。

### 20.6 Form removeRow 误删要复用的字段

需要保留时用 takeRow，而不是 removeRow。

### 20.7 固定高度解决文本截断

翻译和字体变化后再次失败。使用合理 size hint、heightForWidth 和换行策略。

## 21. API 速查表

| API                                  | 用途             | 注意点                   |
| ------------------------------------ | -------------- | --------------------- |
| `QWidget::setLayout()`               | 设置顶层布局         | 每个 Widget 只有一个        |
| `addWidget()`                        | 加入 Widget Item | 对象树负责 Widget 删除       |
| `addLayout()`                        | 嵌套布局           | 父布局接管子布局              |
| `removeWidget()`                     | 停止管理 Widget    | 不删除、不隐藏               |
| `setContentsMargins()`               | 设置外边距          | 与 spacing 不同          |
| `setSpacing()`                       | 设置 Item 间距     | 默认来自样式                |
| `addStretch()`                       | 加可伸缩空白         | 参与剩余空间分配              |
| `setStretch()`                       | 改 Box 项伸缩      | 只作用于主轴                |
| `QGridLayout::addWidget()`           | 按行列添加          | 支持 rowSpan/columnSpan |
| `setColumnStretch()`                 | 分配列额外宽度        | 仍受子项约束                |
| `QFormLayout::addRow()`              | 添加语义表单行        | 可自动创建 Buddy 标签        |
| `setRowWrapPolicy()`                 | 控制窄宽度换行        | 适配大字体和翻译              |
| `removeRow()`                        | 移除并删除整行内容      | 保留内容用 takeRow         |
| `QStackedLayout::setCurrentWidget()` | 切换页面           | 长期身份不用 index          |
| `updateGeometry()`                   | 通知父布局尺寸建议变化    | 不等于重绘                 |

## 22. 自测题

### 题 1：stretch 是否等于宽度百分比

<details><summary>答案</summary>

不是。它主要分配满足其他约束后的剩余空间，minimum、sizeHint、maximum、size policy 和 alignment 都会影响最终结果。

</details>

### 题 2：removeWidget 是否删除控件

<details><summary>答案</summary>

通常不删除也不隐藏，只解除布局管理。调用者必须明确后续生命周期和可见性。

</details>

### 题 3：FormLayout 相比 Grid 的优势

<details><summary>答案</summary>

它表达标签/字段语义，并按平台风格处理标签对齐、字段增长和窄窗口换行；字符串标签重载还能建立 Buddy。

</details>

### 题 4：隐藏后为何仍有空白

<details><summary>答案</summary>

可能有 retainSizeWhenHidden、Spacer、行列最小尺寸、固定父尺寸或其他布局 Item 保留空间，需要逐层排查。

</details>

### 题 5：何时调用 updateGeometry

<details><summary>答案</summary>

当控件内容变化导致 sizeHint、minimumSizeHint 或 size policy 相关建议变化时，通知父布局重新协商。

</details>

## 23. 本篇总结

1. 布局通过最小值、建议值、最大值、策略、stretch 和 alignment 协商几何。
2. Layout 操作统一的 QLayoutItem，因此可以容纳 Widget、子布局和 Spacer。
3. Box 解决一维排列，Grid 解决二维矩阵，Form 解决标签字段，Stacked 解决同区多页面。
4. contentsMargins 是边缘留白，spacing 是相邻 Item 距离。
5. remove 通常不等于 delete，但 FormLayout 的 removeRow 会删除整行内容，必须逐类核对。
6. 动态内容改变尺寸建议后要调用 updateGeometry。
7. 国际化界面依赖布局和语义方向，不依赖固定像素坐标。

下篇将继续讲动态增删、递归清空、布局失效与激活、尺寸约束、调试方法，以及如何实现自定义 FlowLayout。
