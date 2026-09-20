# Qt QBoxLayout 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QBoxLayout>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QLayout`  
> 定位：沿一条主轴依次排列布局项的通用盒式布局

## 1. QBoxLayout 解决什么问题

大多数 Widgets 界面都能拆成“横向一排”与“纵向一列”的组合：

```text
设置页面
├─ 标题
├─ 表单区域
└─ 按钮行
   ├─ 可伸缩空白
   ├─ 取消
   └─ 应用
```

`QBoxLayout` 把可用矩形沿一条主轴切成连续的盒子，每个盒子放一个：

- `QWidget`；
- 子 `QLayout`；
- `QSpacerItem`；
- 任意 `QLayoutItem`。

它负责解决：

1. 窗口变大或变小时，各项怎样按尺寸约束重新分配空间；
2. 多余空间如何根据 stretch 和 `QSizePolicy` 分给不同项目；
3. 固定空白、可伸缩空白和嵌套布局如何统一参与排列；
4. 不同 DPI、字体、语言文本长度下，控件怎样避免依赖固定坐标。

```text
QLayout
  └─ QBoxLayout
       ├─ QHBoxLayout  固定为 LeftToRight
       └─ QVBoxLayout  固定为 TopToBottom
```

`QBoxLayout` 是通用方向版本。日常开发通常优先使用 `QHBoxLayout`、`QVBoxLayout`；只有需要运行时改变排列方向，或需要从四个方向中明确选择时，才直接创建 `QBoxLayout`。

## 2. 最小可用示例

```cpp
#include <QApplication>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *layout = new QVBoxLayout(&window);
    layout->addWidget(new QLabel("用户名："));
    layout->addWidget(new QLineEdit);
    layout->addWidget(new QPushButton("登录"));

    window.resize(360, 180);
    window.show();
    return app.exec();
}
```

`new QVBoxLayout(&window)` 会直接成为 `window` 的顶层布局。一个 QWidget 只能有一个顶层布局；复杂页面应在这个布局中继续嵌套其它布局。

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. 方向决定主轴

`QBoxLayout::Direction` 决定项目的排列顺序，也决定 stretch 作用在哪个维度。

| 方向 | 主轴 | 项目顺序 | stretch 影响 |
| --- | --- | --- | --- |
| `LeftToRight` | 水平 | 左到右 | 宽度 |
| `RightToLeft` | 水平 | 右到左 | 宽度 |
| `TopToBottom` | 垂直 | 上到下 | 高度 |
| `BottomToTop` | 垂直 | 下到上 | 高度 |

直接构造通用布局：

```cpp
auto *layout = new QBoxLayout(
    QBoxLayout::LeftToRight, parentWidget);
```

运行时切换方向：

```cpp
layout->setDirection(QBoxLayout::TopToBottom);
```

这适合响应式工具面板：宽窗口横向放置操作区，窄窗口改为纵向堆叠。切换方向后布局会根据新主轴重新协商尺寸。

不要把 `RightToLeft` 当作国际化文本方向的自动替代品。它明确改变的是当前布局项目的排列方向；界面整体的布局方向、文本方向与 locale 仍应按 QWidget/应用程序的布局方向机制处理。

## 4. 盒式布局如何分配空间

一次 QBoxLayout 计算可以理解为：

1. 获取父控件或父布局分给它的矩形；
2. 扣除 `contentsMargins()`；
3. 扣除项目之间的 spacing；
4. 确保每一项至少满足最小尺寸，且不突破最大尺寸；
5. 在主轴上把剩余空间按 stretch 和 size policy 分配；
6. 对每个 `QLayoutItem` 调用 `setGeometry()`。

假设横向布局剩余可分配宽度为 300，三个项目的 stretch 是 `1 : 2 : 0`：

```text
额外宽度 300
├─ 项目 A: 约 100
├─ 项目 B: 约 200
└─ 项目 C: 不因正 stretch 获得份额
```

项目 C 并不一定完全不变宽。若所有项目的 stretch 都为 0，Qt 会回退到它们的 `QSizePolicy` 进行协商；最大尺寸和最小尺寸也会限制最终结果。

## 5. 添加控件、子布局和空白

### 5.1 添加控件：`addWidget()`

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QLabel("名称："));
row->addWidget(new QLineEdit, 1);
row->addWidget(new QPushButton("浏览"));
```

第二个参数 `stretch` 只沿主轴生效。上例中输入框在水平方向优先吸收剩余空间。

第三个参数 `alignment` 控制控件在自己的布局单元格内的位置：

```cpp
row->addWidget(
    new QPushButton("操作"),
    0,
    Qt::AlignRight | Qt::AlignVCenter);
```

默认 alignment 为 0，含义是控件填满其布局单元格。对齐不会突破控件最小/最大尺寸，也不会替代 stretch。

### 5.2 添加子布局：`addLayout()`

```cpp
auto *main = new QVBoxLayout(&window);
auto *buttons = new QHBoxLayout;

buttons->addWidget(new QPushButton("取消"));
buttons->addWidget(new QPushButton("保存"));

main->addWidget(new QLabel("编辑内容"));
main->addLayout(buttons);
```

子布局加入后成为当前布局的子布局，不能再属于另一个父布局。使用嵌套布局表达区域结构，比手动为每个控件设置坐标可靠得多。

### 5.3 三种空白的语义

| 做法 | 空白类型 | 什么时候用 |
| --- | --- | --- |
| `addSpacing(16)` | 固定空白 | 两项之间必须固定多出 16 像素 |
| `addStretch(1)` | 可伸缩空白 | 推动按钮靠右、靠下或在两侧居中 |
| `addSpacerItem(...)` | 自定义空白项 | 同时精确控制水平/垂直 size policy |

典型按钮右对齐：

```cpp
auto *buttons = new QHBoxLayout;
buttons->addStretch();
buttons->addWidget(new QPushButton("取消"));
buttons->addWidget(new QPushButton("确定"));
```

`addStretch()` 插入的 spacer 最小尺寸为 0，会优先吞掉多余的主轴空间。`addSpacing()` 插入的是不可伸缩的固定空白。

### 5.4 `addStrut()` 约束交叉轴

```cpp
auto *row = new QHBoxLayout;
row->addStrut(40);
```

`addStrut(40)` 不添加可见项目。它把**垂直于主轴**的最小尺寸设为至少 40：

- 水平布局：最小高度至少 40；
- 垂直布局：最小宽度至少 40。

它适合整行控件需要统一最低高度或整列需要统一最低宽度的情况。其它子项的尺寸约束仍然可能让最终尺寸更大。

## 6. Stretch、QSizePolicy 和 alignment 的分工

这三个概念经常被混用。

| 概念 | 它回答的问题 | 作用范围 |
| --- | --- | --- |
| stretch | 多余主轴空间按什么比例分 | 当前 QBoxLayout 的直接项 |
| `QSizePolicy` | 项目是否愿意扩展或收缩 | 控件/布局项自身的尺寸协商 |
| alignment | 项目在已经分到的单元格内放在哪里 | 项目所在单元格 |

例如：

```cpp
auto *row = new QHBoxLayout;
auto *edit = new QLineEdit;

row->addWidget(new QLabel("路径："));
row->addWidget(edit, 1);
row->addWidget(new QPushButton("选择"), 0, Qt::AlignRight);
```

- `edit` 的 stretch 为 1，优先获取额外宽度；
- 按钮 stretch 为 0，不主动参与正 stretch 分配；
- 按钮的 `AlignRight` 影响其在单元格中的位置；
- 若按钮设置了固定宽度，stretch 也不能让它继续变宽。

## 7. Margin、spacing 与指定位置的额外空白

```cpp
layout->setContentsMargins(12, 8, 12, 8);
layout->setSpacing(6);
layout->addSpacing(16);
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 外边距 | `setContentsMargins()` | 设置布局边缘到内容区之间的四边留白 | 影响整个布局外圈；参数顺序是左、上、右、下 |
| 项间距 | `setSpacing()` | 设置相邻布局项之间的统一间距 | 与外边距不同；未显式设置时常由当前 style 或父布局决定 |
| 局部空白 | `addSpacing()` / `insertSpacing()` | 在某个位置插入固定大小的空白项 | 只影响该位置；不会随窗口变大而自动吃掉剩余空间 |

默认 margin 和 spacing 由当前 Qt style 以及布局层级决定。顶层布局通常从 style 获取默认边距；嵌套布局的 spacing 可能继承父布局或由 style 算出。除非设计规范要求像素级固定，否则不要假定所有平台都有相同默认数值。

`QBoxLayout::spacing()` 的特别之处是：若没有显式设置有效 spacing，它会根据父控件的 style 或父布局计算合适的水平/垂直 spacing。

## 8. 插入、查询、移除与所有权

### 8.1 在指定位置插入

```cpp
layout->insertWidget(0, new QLabel("提示："));
layout->insertLayout(1, childLayout, 1);
layout->insertSpacing(2, 12);
layout->insertStretch(3, 1);
```

所有 `insert*` API 的 `index` 是当前布局的直接项索引：

- `0..count()` 是有效插入位置；
- `index == count()` 表示追加；
- 负索引也表示追加到末尾。

`insertItem()` 是最底层版本，可插入任意 `QLayoutItem *`。传入 item 后，所有权转给当前布局。

### 8.2 查询与遍历

```cpp
for (int i = 0; i < layout->count(); ++i) {
    QLayoutItem *item = layout->itemAt(i);
    if (QWidget *widget = item->widget()) {
        widget->setEnabled(false);
    }
}
```

`itemAt()` 只借出查看指针，不转移所有权。项目可能是：

- `item->widget()`：控件；
- `item->layout()`：子布局；
- `item->spacerItem()`：空白项。

`stretch(i)` 返回第 `i` 个直接项的主轴 stretch 因子；`setStretch(i, value)` 按索引修改它。

### 8.3 动态移除

`QLayout::removeWidget(widget)` 只让控件离开布局，不删除控件：

```cpp
layout->removeWidget(editor);
editor->deleteLater();
```

动态清空布局时，用 `takeAt()` 转移布局项所有权：

```cpp
while (QLayoutItem *item = layout->takeAt(0)) {
    if (QWidget *widget = item->widget()) {
        widget->deleteLater();
    } else if (QLayout *child = item->layout()) {
        delete child;
    }
    delete item;
}
```

实际项目中，若子布局内有动态创建的控件，应在删除子布局前递归清空。若只是迁移控件，不要删除控件；取走旧 item 后把控件加入目标布局即可。

隐藏控件也会暂时不参与可见布局分配，适合展开/收起区域；永久移除才使用 `removeWidget()` 和明确销毁。

## 9. 方向切换与响应式布局

通用 `QBoxLayout` 的一个独特价值是运行时切换方向：

```cpp
void ActionPanel::setCompactMode(bool compact)
{
    layout_->setDirection(
        compact
            ? QBoxLayout::TopToBottom
            : QBoxLayout::LeftToRight);
}
```

适合：

- 工具栏在窄宽度下变成纵向操作区；
- 设置页按钮从一行切换为一列；
- 桌面布局与小尺寸嵌入面板复用同一套控件。

切换方向只改变排列主轴，不会替你重新设计每个控件的最小尺寸、最大尺寸、文本换行规则或可访问性。窄模式下仍要验证控件是否真的有足够空间。

## 10. 尺寸与缓存相关 API：通常由 Qt 调用

以下 API 是布局引擎的协商接口，普通业务代码以理解为主：

- `sizeHint()`、`minimumSize()`、`maximumSize()`：汇总直接项后的整体尺寸边界；
- `expandingDirections()`：布局在什么方向能吸收更多空间；
- `hasHeightForWidth()`、`heightForWidth()`、`minimumHeightForWidth()`：宽度影响高度时的协商；
- `setGeometry()`：父布局给本布局分配矩形；
- `invalidate()`：清除缓存，要求之后重新计算。

例如内部有自动换行 `QLabel` 时，QBoxLayout 可能需要根据可用宽度重新计算推荐高度。动态改变子项、文本、字体、边距、spacing 或方向后，Qt 通常会安排更新；自定义动态场景需要立即刷新时再考虑 `invalidate()` 或基类的 `activate()`。

## 11. 综合示例：可自适应的设置面板

```cpp
#include <QCheckBox>
#include <QComboBox>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

class SettingsWidget final : public QWidget
{
public:
    SettingsWidget()
    {
        auto *main = new QVBoxLayout(this);
        main->setContentsMargins(16, 12, 16, 12);
        main->setSpacing(10);

        auto *title = new QLabel("应用设置");
        main->addWidget(title);

        auto *form = new QFormLayout;
        form->addRow("服务器：", new QLineEdit);
        form->addRow("主题：", new QComboBox);
        form->addRow("自动保存：", new QCheckBox);
        main->addLayout(form, 1);

        auto *buttons = new QHBoxLayout;
        buttons->addStretch();
        buttons->addWidget(new QPushButton("取消"));
        buttons->addWidget(new QPushButton("应用"));
        main->addLayout(buttons);
    }
};
```

这个例子表达了三层职责：

- 外层 `QVBoxLayout` 决定标题、表单、按钮行的纵向结构；
- `QFormLayout` 处理标签-字段对齐；
- 按钮 `QHBoxLayout` 用可伸缩空白把操作按钮推到右侧。

这里 `main->addLayout(form, 1)` 的 stretch 只作用于外层纵向主轴，因此表单区优先吸收额外高度。

## 12. 常见误区与排查

### 12.1 一个 QWidget 设置两个顶层布局

一个 QWidget 只能有一个顶层布局。多个区域要在主布局中嵌套 `QHBoxLayout`、`QVBoxLayout`、`QGridLayout` 或 `QFormLayout`。

### 12.2 把 `setSpacing()` 当作窗口边距

边缘留白是 `setContentsMargins()`；相邻项目间距才是 `setSpacing()`。

### 12.3 设置 stretch 但控件不变大

stretch 只分配剩余的主轴空间，还会受 `minimumSize`、`maximumSize`、`QSizePolicy` 和父窗口尺寸限制。

### 12.4 用固定 `addSpacing(300)` 把按钮推到右侧

这是把窗口尺寸假设写死。应使用 `addStretch()` 或一个水平 `Expanding` spacer。

### 12.5 以为 `removeWidget()` 会删除控件

它只解除布局关系。控件仍存在，是否隐藏、迁移或删除必须由业务代码决定。

### 12.6 `setStretchFactor()` 返回 false

它只在当前布局的直接项中查找，不递归进入子布局。确认传入的是当前层级实际加入的 widget 或 layout。

### 12.7 用 `resizeEvent()` 手动摆放受布局管理的控件

下一次布局计算会覆盖手动 geometry。应通过嵌套结构、size policy、stretch、margin、spacing 和 alignment 表达需求。

## API 速查表
表中列出 QBoxLayout 自己声明与重写的 API；`QLayout` 继承来的通用 API，如 `removeWidget()`、`setContentsMargins()`、`activate()`，请结合 `QLayout` 笔记阅读。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum QBoxLayout::Direction` | 定义盒式布局的项目顺序和主轴方向。 | 决定 stretch 是作用于宽度还是高度。 |
| 枚举值 | `LeftToRight` | 从左到右水平排列。 | `QHBoxLayout` 的默认方向。 |
| 枚举值 | `RightToLeft` | 从右到左水平排列。 | 需要明确反向排列同一组项目时使用。 |
| 枚举值 | `TopToBottom` | 从上到下垂直排列。 | `QVBoxLayout` 的默认方向。 |
| 枚举值 | `BottomToTop` | 从下到上垂直排列。 | 需要把新增内容朝上堆叠时使用。 |
| 枚举值 | `Down` | `TopToBottom` 的别名。 | 旧代码或更口语化方向命名中可能见到；语义等同从上到下。 |
| 枚举值 | `Up` | `BottomToTop` 的别名。 | 旧代码或更口语化方向命名中可能见到；语义等同从下到上。 |
| 构造函数 | `QBoxLayout(QBoxLayout::Direction dir, QWidget *parent = nullptr)` | 创建指定方向的盒式布局。 | 传入 QWidget 后成为其顶层布局；一个 QWidget 只能有一个顶层布局。 |
| 析构函数 | `virtual ~QBoxLayout()` | 销毁布局和其管理的布局项。 | 布局自身不会直接销毁已管理的 QWidget；控件通常由父 QWidget 对象树销毁。 |
| 添加 | `void addLayout(QLayout *layout, int stretch = 0)` | 在末尾加入子布局并设置其主轴 stretch。 | 子布局成为当前布局的子布局，不能再加入另一个父布局。 |
| 添加 | `void addSpacerItem(QSpacerItem *spacerItem)` | 在末尾加入自定义 spacer。 | 所有权转给布局；适合需要控制双方向 size policy 的空白。 |
| 添加 | `void addSpacing(int size)` | 在末尾加入固定大小的非伸缩空白。 | 用于某一位置额外留白；不是边距，也不会随窗口增长。 |
| 添加 | `void addStretch(int stretch = 0)` | 在末尾加入最小尺寸为 0 的可伸缩空白。 | 常用于把后续控件推向右侧或底部。 |
| 添加 | `void addStrut(int size)` | 提高交叉轴方向的最小尺寸。 | 水平布局影响最小高度，垂直布局影响最小宽度；不添加可见项目。 |
| 添加 | `void addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())` | 在末尾加入控件，并设置主轴 stretch 与单元格内对齐。 | `stretch` 只在主轴有效；默认 alignment 为 0，控件填满单元格。 |
| 查询 | `QBoxLayout::Direction direction() const` | 返回当前排列方向。 | 同时说明添加顺序和 stretch 的作用轴。 |
| 插入 | `void insertItem(int index, QLayoutItem *item)` | 在索引位置插入任意布局项。 | `0..count()` 或负索引有效；负索引/末尾表示追加；所有权转给布局。 |
| 插入 | `void insertLayout(int index, QLayout *layout, int stretch = 0)` | 在索引位置插入子布局。 | 负索引追加；子布局成为当前布局子对象。 |
| 插入 | `void insertSpacerItem(int index, QSpacerItem *spacerItem)` | 在索引位置插入自定义 spacer。 | 所有权转给布局；适合复杂空白策略。 |
| 插入 | `void insertSpacing(int index, int size)` | 在索引位置插入固定额外空白。 | 负索引追加；它不等同于全局 `spacing`。 |
| 插入 | `void insertStretch(int index, int stretch = 0)` | 在索引位置插入可伸缩空白。 | 最小尺寸为 0；多个 stretch 按因子分配剩余主轴空间。 |
| 插入 | `void insertWidget(int index, QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())` | 在索引位置插入控件。 | 负索引追加；stretch 和 alignment 规则与 `addWidget()` 相同。 |
| 设置 | `void setDirection(QBoxLayout::Direction direction)` | 运行时改变排列方向。 | 适合响应式结构；切换后仍要检查控件最小尺寸与文本换行。 |
| 设置 | `void setStretch(int index, int stretch)` | 按直接项索引设置主轴 stretch。 | 索引范围来自 `count()`；不递归影响子布局内部项目。 |
| 设置 | `bool setStretchFactor(QWidget *widget, int stretch)` | 按控件设置 stretch。 | 仅搜索当前布局直接 widget；找不到返回 `false`。 |
| 设置 | `bool setStretchFactor(QLayout *layout, int stretch)` | 按直接子布局设置 stretch。 | 仅搜索当前层；与 QWidget 重载区分参数类型。 |
| 查询 | `int stretch(int index) const` | 返回指定直接项的 stretch 因子。 | 用于检查动态修改后的布局权重；越界索引没有有效业务含义。 |
| 重写 | `void addItem(QLayoutItem *item)` | 把任意布局项追加到末尾。 | 自定义或底层代码使用；布局接管 item 所有权。 |
| 重写 | `int count() const` | 返回当前直接布局项数。 | 用于遍历、插入索引和动态管理。 |
| 重写 | `Qt::Orientations expandingDirections() const` | 返回布局可以在哪些方向吸收额外空间。 | 由直接项的尺寸策略综合决定；一般由 Qt 布局系统查询。 |
| 重写 | `bool hasHeightForWidth() const` | 返回布局的推荐高度是否依赖宽度。 | 内部含自动换行内容时可能为 true；通常由 Qt 查询。 |
| 重写 | `int heightForWidth(int w) const` | 计算宽度为 `w` 时的推荐高度。 | 支持换行内容的尺寸协商；业务代码通常不直接调用。 |
| 重写 | `void invalidate()` | 清除已缓存的布局计算信息。 | 动态改子项、方向、间距或尺寸策略后需要重新计算时使用。 |
| 重写 | `QLayoutItem *itemAt(int index) const` | 查看指定直接布局项，不转移所有权。 | 返回项可能是 widget、layout 或 spacer；越界返回 `nullptr`。 |
| 重写 | `QSize maximumSize() const` | 返回由所有直接项约束汇总出的最大尺寸。 | 受子项最大尺寸、margin 和方向影响。 |
| 重写 | `int minimumHeightForWidth(int w) const` | 返回给定宽度下布局的最小高度。 | 宽度影响换行时参与上层布局协商。 |
| 重写 | `QSize minimumSize() const` | 返回布局可接受的最小尺寸。 | 子项最小尺寸、margin、spacing 和 strut 都会影响它。 |
| 重写 | `void setGeometry(const QRect &r)` | 接收父级矩形并分配给每个直接项。 | 布局计算核心；受布局管理的控件 geometry 会因此更新。 |
| 重写 | `void setSpacing(int spacing)` | 设置直接相邻项目间的统一间距。 | 不影响外边缘 margin，也不替代局部 `addSpacing()`。 |
| 重写 | `QSize sizeHint() const` | 返回布局推荐尺寸。 | 用于父布局/窗口初始尺寸协商，不是固定尺寸。 |
| 重写 | `int spacing() const` | 返回当前有效项目间距。 | 未显式设置时会从 style 或父布局计算合适值。 |
| 重写 | `QLayoutItem *takeAt(int index)` | 移除指定项并把其所有权交给调用方。 | 动态清空或迁移时使用；必须处理返回 item 及其关联对象。 |

## 14. 与相关布局如何选择

| 需求 | 推荐类型 | 原因 |
| --- | --- | --- |
| 固定横向一行 | `QHBoxLayout` | 语义最明确，少写方向参数 |
| 固定纵向一列 | `QVBoxLayout` | 语义最明确，少写方向参数 |
| 需要运行时横竖切换 | `QBoxLayout` | 支持 `setDirection()` |
| 行列、跨度、表格 | `QGridLayout` | 不要用大量嵌套 box 模拟二维网格 |
| 标签-字段表单 | `QFormLayout` | 自动处理标签列与字段列 |
| 多页切换 | `QStackedLayout` | 管理一个当前页面，不必手工 hide/show |

### 一句话总结

`QBoxLayout` 是一条主轴上的自适应排列算法：它将控件、子布局和空白项排成连续盒子，用 stretch 分配剩余主轴空间，用 `QSizePolicy` 与尺寸边界限制实际大小，用 margin/spacing 控制留白，并允许通过 `setDirection()` 在横向与纵向结构之间切换。
