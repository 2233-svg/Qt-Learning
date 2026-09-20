# Qt QBoxLayout 深入笔记

> 适用版本：Qt 6 Widgets（Qt 5 的核心用法基本一致）  
> 头文件：`#include <QBoxLayout>`  
> 所属模块：`Qt6::Widgets`

## 1. 先建立整体认识：布局到底解决什么问题

在 Qt 中，窗口中的控件不应该依赖固定坐标（`move()`、`setGeometry()`）来摆放。窗口大小变化、字体变化、系统缩放比例变化、翻译后文字变长，都会让固定坐标失效。

布局（`QLayout`）是一套“根据约束自动分配矩形区域”的算法：

1. 父窗口把可用矩形交给顶层布局。
2. 布局扣除内容边距（contents margins）和控件之间的间距（spacing）。
3. 每个子项至少满足最小尺寸，尽量不超过最大尺寸。
4. 剩余空间按伸缩因子（stretch factor）和控件的 `QSizePolicy` 分配。
5. 布局将最终矩形写入控件的 geometry。

`QBoxLayout` 就是“沿一条轴线排成盒子”的布局：可以横向排成一行，也可以纵向排成一列。它继承自 `QLayout`，而 `QHBoxLayout`、`QVBoxLayout` 分别是它的水平和垂直便捷子类。

```text
QLayout
  └─ QBoxLayout
       ├─ QHBoxLayout（LeftToRight）
       └─ QVBoxLayout（TopToBottom）
```

## 2. 最小可用代码

### 2.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 一个垂直布局窗口

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
    auto *layout = new QVBoxLayout(&window); // 直接成为 window 的顶层布局
    layout->addWidget(new QLabel("用户名："));
    layout->addWidget(new QLineEdit);
    layout->addWidget(new QPushButton("登录"));

    window.resize(360, 180);
    window.show();
    return app.exec();
}
```

构造 `QVBoxLayout(&window)` 等价于创建布局后调用 `window.setLayout(layout)`。一个 `QWidget` 只能有一个顶层布局；需要更多结构时，应在这个顶层布局中嵌套其他布局。

## 3. Direction：四种排列方向

```cpp
enum QBoxLayout::Direction {
    LeftToRight,  // 水平：左 -> 右
    RightToLeft,  // 水平：右 -> 左
    TopToBottom,  // 垂直：上 -> 下
    BottomToTop   // 垂直：下 -> 上
};
```

最常用的是 `QHBoxLayout`（内部方向为 `LeftToRight`）和 `QVBoxLayout`（内部方向为 `TopToBottom`）。需要动态切换时使用通用类：

```cpp
auto *box = new QBoxLayout(QBoxLayout::LeftToRight, &window);
box->setDirection(QBoxLayout::TopToBottom);
QBoxLayout::Direction current = box->direction();
```

注意：方向决定“主轴”，伸缩因子也只在主轴上生效。横向布局伸缩的是宽度，纵向布局伸缩的是高度。

## 4. 添加控件、布局与空白项

### 4.1 `addWidget`

```cpp
void addWidget(QWidget *widget,
               int stretch = 0,
               Qt::Alignment alignment = Qt::Alignment());
```

- `widget`：加入布局的控件。布局会将其设为父布局所管理窗口的子控件。
- `stretch`：主轴伸缩因子，数值越大，获得的剩余空间越多。
- `alignment`：控件在自己单元格中的对齐方式。默认值为 0，表示填满单元格。

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QLabel("固定在左侧"));
row->addWidget(new QLineEdit, 1); // 输入框优先占据剩余宽度
row->addWidget(new QPushButton("确定"), 0, Qt::AlignRight);
```

当所有项的 stretch 都是 0 时，Qt 会参考各控件的 `QSizePolicy` 分配空间；因此“stretch=0”并不等于“永远不变宽”。若必须固定大小，可使用 `setFixedWidth()` 或合适的 `QSizePolicy`，但通常应优先让布局自适应。

### 4.2 `addLayout`

把另一个布局作为一个“盒子”加入当前布局：

```cpp
auto *mainLayout = new QVBoxLayout(&window);
auto *buttonRow = new QHBoxLayout;
buttonRow->addWidget(new QPushButton("取消"));
buttonRow->addWidget(new QPushButton("保存"));
mainLayout->addWidget(new QLabel("编辑内容"));
mainLayout->addLayout(buttonRow);
```

子布局不能同时属于两个父布局。加入后，父布局负责其生命周期和几何更新。

### 4.3 `addSpacing` 与 `addStretch`

```cpp
layout->addSpacing(16); // 固定 16 像素的空白
layout->addStretch(1);  // 可伸缩空白，stretch 为 1
```

典型的“按钮靠右”写法：

```cpp
auto *buttons = new QHBoxLayout;
buttons->addStretch();
buttons->addWidget(new QPushButton("取消"));
buttons->addWidget(new QPushButton("确定"));
```

`addSpacing()` 的最小尺寸是指定值且不会随剩余空间增长；`addStretch()` 的最小尺寸为 0，会吞掉多余空间。`addSpacerItem()` 可传入自定义的 `QSpacerItem`，适合同时控制水平/垂直尺寸策略：

```cpp
#include <QSpacerItem>
layout->addSpacerItem(new QSpacerItem(
    20, 0, QSizePolicy::Expanding, QSizePolicy::Minimum));
```

### 4.4 `addStrut`

`addStrut(size)` 设置布局在**垂直于主轴**方向的最小尺寸。水平布局中它限制最小高度，垂直布局中限制最小宽度：

```cpp
auto *row = new QHBoxLayout;
row->addStrut(40); // 这一行至少高 40 像素
```

它不会直接添加一个可见控件，而是改变该行的尺寸约束。

## 5. Stretch：剩余空间如何分配

假设水平布局内容区域宽度为 600，扣除固定间距后，三个控件的最小宽度之和为 300，剩余 300；它们的 stretch 分别为 `1、2、0`：

- stretch 总和为 3。
- 第一个控件约获得 `300 × 1/3 = 100` 的额外宽度。
- 第二个控件约获得 `300 × 2/3 = 200` 的额外宽度。
- 第三个控件没有正 stretch，通常按其 size policy 和最大尺寸处理。

```cpp
auto *row = new QHBoxLayout;
row->addWidget(new QLabel("左"), 1);
row->addWidget(new QLineEdit, 2);
row->addWidget(new QPushButton("操作"), 0);
```

### 5.1 修改 stretch

```cpp
row->setStretch(0, 1);             // 按索引设置
row->setStretchFactor(edit, 3);    // 按控件设置
row->setStretchFactor(buttonRow, 1); // 按子布局设置
int value = row->stretch(0);
```

`setStretchFactor()` 只搜索当前布局的直接子项，不会递归搜索更深层的子布局；找不到时返回 `false`。索引可通过 `count()`、`itemAt(i)` 获取。

## 6. 边距与间距：两个容易混淆的概念

```cpp
layout->setContentsMargins(12, 8, 12, 8); // 左、上、右、下
layout->setSpacing(6);                    // 相邻项之间
int s = layout->spacing();
```

- **contents margins**：布局内容与父窗口边界之间的外边距。
- **spacing**：相邻盒子之间的间隔。
- `addSpacing(n)`：只在某一个位置额外插入固定空白。

默认值由当前 Qt Style 决定。顶层布局通常使用窗口风格提供的边距，嵌套布局的 spacing 往往继承父布局或由 style 计算。为了跨平台一致，只有确实需要像素级统一时才硬编码数值。

## 7. 插入、遍历、移除

### 7.1 插入 API

```cpp
layout->insertWidget(0, widget, 1, Qt::AlignCenter);
layout->insertLayout(1, childLayout, 0);
layout->insertSpacing(2, 12);
layout->insertStretch(3, 1);
```

`index < 0` 或 `index == count()` 时表示追加到末尾。更底层的 `insertItem(index, QLayoutItem *)` 可插入任意布局项，所有权会转交给当前布局。

### 7.2 遍历布局项

```cpp
for (int i = 0; i < layout->count(); ++i) {
    QLayoutItem *item = layout->itemAt(i); // 只查看，不转移所有权
    if (QWidget *w = item->widget()) {
        w->setEnabled(false);
    }
}
```

`itemAt()` 返回空指针表示索引无效；项可能是控件、子布局或 spacer，分别通过 `widget()`、`layout()`、`spacerItem()` 判断。

### 7.3 移除控件与 `takeAt`

```cpp
layout->removeWidget(edit); // 从布局摘下，控件本身不会被删除
edit->deleteLater();
```

批量清空布局时使用 `takeAt()` 转移并销毁布局项：

```cpp
while (QLayoutItem *item = layout->takeAt(0)) {
    if (QWidget *w = item->widget())
        w->deleteLater();
    else if (QLayout *child = item->layout())
        delete child; // 递归清空时应先处理 child 的 item
    delete item;
}
```

只调用 `removeWidget()` 不会删除控件；只调用 `takeAt()` 也不会自动删除控件。对象所有权和销毁时机必须由代码明确处理。

隐藏控件（`widget->hide()`）会使其暂时不参与布局可见区域分配，重新 `show()` 后会恢复；这适合临时隐藏，不适合永久删除。

## 8. 尺寸相关 API：理解而不是频繁手动调用

以下函数是布局引擎为 `QLayout`/`QLayoutItem` 提供的尺寸协商接口，通常由 Qt 在布局过程自动调用：

- `sizeHint()`：推荐尺寸。
- `minimumSize()` / `maximumSize()`：可接受的尺寸边界。
- `setGeometry(const QRect &r)`：父布局分配矩形时写入几何区域。
- `expandingDirections()`：布局愿意在哪些方向扩展。
- `hasHeightForWidth()`、`heightForWidth(w)`：内容高度依赖宽度时使用，例如自动换行标签。
- `minimumHeightForWidth(w)`：给定宽度下的最小高度。
- `invalidate()`：清除缓存并要求重新计算。

例如，`QLabel` 设置 `wordWrap` 后可能报告 `hasHeightForWidth() == true`，窗口变窄时布局会据此增加标签高度。自定义布局或自定义控件时，重载这些函数比在外部手动计算坐标更可靠。

## 9. 综合示例：可伸缩的设置面板

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
        title->setStyleSheet("font-size: 18px; font-weight: 600;");
        main->addWidget(title);

        auto *form = new QFormLayout;
        form->addRow("服务器：", new QLineEdit);
        form->addRow("主题：", new QComboBox);
        form->addRow("自动保存", new QCheckBox);
        main->addLayout(form, 1); // 表单区域承担纵向剩余空间

        auto *buttons = new QHBoxLayout;
        buttons->addStretch(1); // 将按钮推到右侧
        buttons->addWidget(new QPushButton("取消"));
        buttons->addWidget(new QPushButton("应用"));
        main->addLayout(buttons);
    }
};
```

这里体现了三层关系：外层 `QVBoxLayout` 管理标题、表单和按钮行；`QFormLayout` 负责标签-字段对齐；按钮行用 `addStretch()` 将操作按钮靠右。窗口变大时，stretch 为 1 的表单区域优先吸收垂直空间。

## 10. 常见误区与排查顺序

### 10.1 “控件不显示”

确认控件已经 `addWidget()`，且顶层窗口已经 `show()`。如果布局是嵌套布局，确认子布局已经 `parentLayout->addLayout(childLayout)`。

### 10.2 “设置了 stretch 但大小不变”

stretch 只分配**剩余空间**，并且受控件的 `minimumSize`、`maximumSize`、`QSizePolicy` 限制。检查是否有最大尺寸、固定尺寸或其它项已经占满空间。

### 10.3 “顶层布局边缘太宽/太窄”

检查 `setContentsMargins()`；不要把 `setSpacing()` 当成外边距。默认值来自 style，跨平台时不要假设永远是 9 或 11。

### 10.4 “删除后布局仍有空白”

从布局移除后要触发布局更新，并正确销毁 `QLayoutItem`/控件。动态重建时优先使用 `takeAt()` 循环；必要时调用 `layout->invalidate()` 或 `parentWidget->adjustSize()`。

### 10.5 “一个窗口设置了两个布局”

一个 `QWidget` 只能有一个顶层布局。把多个区域放入一个主布局，区域内部再使用 `QHBoxLayout`、`QVBoxLayout`、`QGridLayout` 等。

## 11. 进一步延伸：如何选择布局

| 需求            | 推荐布局                                |
| ------------- | ----------------------------------- |
| 单行或单列排列       | `QHBoxLayout` / `QVBoxLayout`       |
| 行列网格、表格式对齐    | `QGridLayout`                       |
| 标签与字段成对排列     | `QFormLayout`                       |
| 多页面但同时只显示一个页面 | `QStackedLayout` / `QStackedWidget` |
| 复杂界面          | 外层 box + 内层 grid/form 的组合           |

经验法则：先用语义最明确的便捷类；只有需要运行时切换方向时才直接使用 `QBoxLayout`。把布局看作“约束系统”而不是坐标容器，优先调整 size policy、最小/最大尺寸、stretch、margin 和 spacing，尽量不要在 `resizeEvent()` 中手动摆放子控件。

## API 速查表

| API                  | 作用           | 关键注意点          |
| -------------------- | ------------ | -------------- |
| `addWidget`          | 追加控件         | stretch 只作用于主轴 |
| `addLayout`          | 追加子布局        | 子布局只能有一个父布局    |
| `addSpacing`         | 固定空白         | 不会随窗口增长        |
| `addStretch`         | 可伸缩空白        | 常用于居中、靠右/靠下    |
| `addStrut`           | 限制垂直于主轴的最小尺寸 | 不添加可见控件        |
| `insert*`            | 指定索引插入       | 负索引表示追加        |
| `setStretch`         | 按索引设置伸缩      | 索引来自 `count()` |
| `setStretchFactor`   | 按控件/布局设置伸缩   | 仅查找直接子项        |
| `setContentsMargins` | 设置外边距        | 参数顺序左、上、右、下    |
| `setSpacing`         | 设置相邻项间距      | 与外边距不同         |
| `itemAt`             | 查看项          | 不转移所有权         |
| `takeAt`             | 移除并转移项       | 需自行处理删除        |
| `removeWidget`       | 从布局移除控件      | 不会删除控件         |
| `setDirection`       | 运行时切换方向      | 切换后布局会重新计算     |

---

### 一句话总结

`QBoxLayout` 沿一条主轴把控件、子布局和 spacer 排成盒子；用 `stretch` 决定剩余空间的相对分配，用 `contentsMargins/spacing` 控制整体留白，用嵌套布局表达复杂界面，用 size policy 和尺寸边界处理自适应，最终让界面在不同窗口尺寸、平台和语言环境下都保持稳定。
