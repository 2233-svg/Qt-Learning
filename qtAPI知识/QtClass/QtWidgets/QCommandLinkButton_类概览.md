# QCommandLinkButton 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCommandLinkButton>`  
> 模块：`Qt6::Widgets`  
> 继承：`QPushButton -> QAbstractButton -> QWidget`

`QCommandLinkButton` 是一种“主标题 + 说明文字”的按钮。它仍然是一个真正的 `QPushButton`：可以被点击、设置为默认按钮、连接 `clicked()`，也能参与键盘导航；它新增的价值是把“这个按钮会做什么”作为按钮的一部分展示出来。

它适合用户需要在多个操作之间做判断的界面，例如向导首页、安装方式选择、设置入口和任务选择页。普通按钮通常只有一行短标签，而命令链接按钮允许用第二行说明降低决策成本。

## 1. 它解决什么问题

当界面只有“确定 / 取消 / 保存”这类短动作时，`QPushButton` 已经足够。问题出现在按钮标题本身不够让用户判断后果：

- “快速安装”和“自定义安装”分别会做什么；
- “导入现有项目”和“创建新项目”进入哪条流程；
- “使用推荐设置”和“手动配置”会改变哪些内容；
- 向导下一步到底是继续安装、检查更新，还是打开另一个页面。

这时可以把按钮写成：

```text
使用推荐设置
自动选择适合大多数用户的配置
```

主标题由继承自 `QPushButton` 的 `text()` 提供，第二行由 `description()` 提供。点击、快捷键、`clicked()` 信号等仍然走按钮体系，不需要重新实现一套交互。

它不解决这些问题：

- 不负责展示复杂富文本；
- 不负责把多个按钮变成互斥选项；
- 不负责执行安装、切页或业务逻辑；
- 不保证所有平台的视觉布局完全相同；
- 不适合给普通工具栏按钮普遍加长说明。

## 2. 什么时候用，什么时候不用

| 场景 | 是否适合 | 原因 |
| --- | --- | --- |
| 向导首页选择安装方式 | 适合 | 每个选择通常需要一行解释 |
| 设置页选择功能入口 | 适合 | 用户点击前需要知道会进入什么配置 |
| 任务选择对话框 | 适合 | 标题表达动作，说明表达影响 |
| 普通确认/取消 | 通常不适合 | `QPushButton` 更紧凑，界面扫描更快 |
| 工具栏或窄侧栏 | 通常不适合 | 描述文字会让按钮变高、变宽 |
| 需要图标 + 富文本说明 | 视情况 | 可以使用自定义 widget 或布局，不要强行把描述塞进一行 |
| 多选一的状态选择 | 不一定适合 | 应考虑 `QRadioButton` 或带描述的自定义选项组件 |

命令链接按钮更像“任务入口”，而不是“密集表单里的一个动作控件”。如果页面中放很多个，说明文字会造成垂直空间和视觉层级压力，应让每个按钮的描述都短而有区分度。

## 3. 最小可用代码

```cpp
#include <QApplication>
#include <QCommandLinkButton>
#include <QDialog>
#include <QVBoxLayout>

class StartDialog final : public QDialog
{
public:
    explicit StartDialog(QWidget *parent = nullptr)
        : QDialog(parent)
    {
        auto *recommended = new QCommandLinkButton(
            tr("Use recommended settings"),
            tr("Choose defaults suitable for most projects"),
            this);
        auto *custom = new QCommandLinkButton(
            tr("Customize settings"),
            tr("Review paths, plugins, and advanced options"),
            this);

        auto *layout = new QVBoxLayout(this);
        layout->addWidget(recommended);
        layout->addWidget(custom);

        connect(recommended, &QCommandLinkButton::clicked,
                this, &QDialog::accept);
        connect(custom, &QCommandLinkButton::clicked,
                this, [this] { openAdvancedPage(); });
    }

private:
    void openAdvancedPage()
    {
        // 这里只负责进入业务流程；按钮本身不保存配置逻辑。
    }
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    StartDialog dialog;
    dialog.show();
    return app.exec();
}
```

三个构造函数分别适合：

- 先创建空按钮，再通过继承 API 和 `setDescription()` 配置；
- 只有主标题，说明稍后补上；
- 同时设置主标题与说明，最适合静态创建。

## 4. 标题、说明和点击行为是三条线

`QCommandLinkButton` 自己只增加说明文字；按钮的主标题和动作来自 `QPushButton` / `QAbstractButton`：

```cpp
button->setText(tr("Import project"));       // 继承自 QAbstractButton
button->setDescription(tr("Load an existing project from disk"));
button->setEnabled(canImport);               // 继承自 QWidget

connect(button, &QCommandLinkButton::clicked,
        this, &ProjectDialog::importProject);
```

不要把说明文字当成业务状态。说明只是面向用户的解释；真正决定按钮是否可用、点击后做什么的，是外部业务代码。

如果说明文字在运行时改变，按钮的推荐尺寸和布局可能需要更新。`setDescription()` 会让控件重新计算相关几何，但最终高度仍由 style、字体、布局约束和窗口宽度共同决定，不应假设所有平台都会给出同样的像素尺寸。

## 5. 为什么不能只用两个 `QLabel` 拼一个按钮

当然可以用一个 `QWidget` 加 `QVBoxLayout` 拼出“标题 + 说明”，但那样还要自己处理：

- 鼠标按下、释放和取消；
- 键盘 Space / Enter 激活；
- focus frame 和 Tab 导航；
- enabled 状态和 hover 状态；
- 默认按钮行为；
- accessible role、按键提示和 style option；
- 高 DPI 和平台风格下的尺寸计算。

`QCommandLinkButton` 把这些按钮行为交给 `QAbstractButton`，把命令链接外观交给 style。除非需要完全特殊的交互或布局，否则优先使用它。

相反，也不要为了普通短按钮使用它来“顺便获得更大的按钮”。命令链接的视觉语义是带解释的主动作，滥用会让用户难以区分主要入口和普通操作。

## 6. `flat` 与样式系统

`QCommandLinkButton` 继承了 `QPushButton` 的 `flat` 属性，因此可以调用：

```cpp
button->setFlat(true);
bool flat = button->isFlat();
```

但 `flat` 不是 `QCommandLinkButton` 在 `qcommandlinkbutton.h` 中重新声明的接口，而是继承来的按钮属性。它只改变按钮的平面外观倾向，不会删除说明文字，也不会把命令链接变成普通标签。

命令链接的箭头、边距、字体层级和说明排版主要由当前 `QStyle` 绘制。不要通过固定坐标覆盖它的内部布局；如果产品需要完全不同的视觉结构，应使用自定义控件或自定义 style，而不是依赖某个平台的内部像素。

## 7. 尺寸计算：说明文字会改变布局约束

这个类重写了三个尺寸相关函数：

- `sizeHint()`：给布局一个推荐尺寸；
- `minimumSizeHint()`：给布局一个不应轻易压缩到更小的参考尺寸；
- `heightForWidth(int)`：当宽度受限时，估算说明文字换行后的高度。

因此在 `QVBoxLayout`、`QWizard` 或窄窗口中，按钮高度可能随宽度变化。不要写死：

```cpp
button->setFixedHeight(48); // 可能截断说明或破坏平台风格
```

除非业务明确要求固定卡片规格，否则让布局使用 size hint 更稳妥。如果说明过长，优先缩短文案或给容器更合理的宽度，而不是不断增加固定高度。

## 8. 自定义绘制时应该从哪里接入

`initStyleOption(QStyleOptionButton *)` 是给 style 准备按钮状态和内容信息的入口。它适合自定义 style 或派生类在调用 `QStyle::drawControl()` 前取得正确的样式选项。

`paintEvent(QPaintEvent *)` 是实际绘制事件入口。若重写它，通常应：

1. 创建 `QStyleOptionButton`；
2. 调用 `initStyleOption()`；
3. 交给当前 style 绘制，或明确实现完整的绘制协议；
4. 保留 enabled、hover、pressed、focus、default 等状态。

不要只画标题和说明就丢掉按钮的焦点框、按下状态或平台高亮。除非你确实要实现自定义 style，否则不要重写 `paintEvent()`。

`event(QEvent *)` 是更底层的事件入口。多数应用只需要连接信号或重写更具体的 QWidget 事件；直接重写它往往意味着你正在改变控件生命周期或特殊事件处理。

## 9. 常见误用

| 现象 | 原因 | 处理方式 |
| --- | --- | --- |
| 说明文字被截断 | 宽度不足、固定高度或布局限制过强 | 给布局更多宽度，缩短描述，避免固定高度 |
| 点击没有执行动作 | 只设置了标题和描述，没有连接 inherited signal | 连接 `clicked()`、`pressed()` 或使用 `QDialogButtonBox` 等外部流程 |
| 把 `flat` 当成本类核心配置 | `flat` 来自 `QPushButton`，只改变外观 | 先决定这个控件是否真的应该表达命令链接语义 |
| 自定义 `paintEvent()` 后焦点框消失 | 没有正确初始化和绘制 style option | 调用 `initStyleOption()` 并交给当前 `QStyle` |
| 每个平台高度不同 | style、字体、高 DPI 和文字换行不同 | 使用 `sizeHint()` 和布局，不做跨平台像素假设 |
| 一个页面放几十个命令链接按钮 | 把任务入口当成普通按钮使用 | 减少入口数量，或改用列表/树/自定义选项视图 |

## API 速查表
下表按 Qt 6.11.1 的 `qcommandlinkbutton.h` 直接声明整理。`text()`、`clicked()`、`setFlat()` 等属于基类 API，这里只在“继承能力”一节提到，不伪装成 `QCommandLinkButton` 自己重新声明的成员。

### 10.1 构造与说明文字

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCommandLinkButton(QWidget *parent = nullptr)` | 创建一个没有标题和说明的命令链接按钮 | 可随后使用继承的 `setText()` 和本类的 `setDescription()` 配置 |
| 构造 | `QCommandLinkButton(const QString &text, QWidget *parent = nullptr)` | 创建一个带主标题的命令链接按钮 | 说明文字为空时，仍可能保留命令链接的视觉结构 |
| 构造 | `QCommandLinkButton(const QString &text, const QString &description, QWidget *parent = nullptr)` | 同时设置主标题和说明 | 静态创建“动作 + 后果说明”时最直接 |
| 生命周期 | `~QCommandLinkButton()` | 销毁按钮 | 遵循 QWidget 父子对象树；不要重复释放父对象管理的实例 |
| 内容 | `description() const` | 读取第二行说明文字 | 返回的是原始字符串，不是最终换行后的显示结果 |
| 内容 | `setDescription(const QString &description)` | 设置第二行说明文字 | 会影响尺寸提示和绘制；文案应保持短而有区分度 |

### 10.2 尺寸、样式与事件扩展

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 尺寸 | `sizeHint() const` | 返回包含标题和说明的推荐尺寸 | 交给布局使用；不要假设不同 style 返回相同像素 |
| 尺寸 | `heightForWidth(int width) const` | 根据给定宽度估算控件高度 | 说明文字可能换行；固定宽度容器中尤其有用 |
| 尺寸 | `minimumSizeHint() const` | 返回不希望布局继续压缩的最小建议尺寸 | 不是硬性最小尺寸；布局和 `setMinimumSize()` 仍可能改变结果 |
| 样式 | `initStyleOption(QStyleOptionButton *option) const` | 用本按钮状态填充样式选项 | 自定义 style 或绘制前调用；不要传空指针 |
| 事件 | `event(QEvent *e)` | 处理控件级通用事件 | 一般不直接重写；重写时应把未处理事件交给 `QPushButton` |
| 绘制 | `paintEvent(QPaintEvent *)` | 绘制命令链接按钮 | 自定义时必须保留焦点、按下、禁用和平台 style 状态 |

### 10.3 继承后仍可直接使用的关键 API

这些不是 `QCommandLinkButton` 在头文件中新增的声明，但实际使用时经常和本类配合：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标题 | `setText(const QString &) / text() const` | 设置或读取主标题 | 主标题要短；详细解释放到 `description` |
| 激活 | `clicked()` | 用户完成一次点击激活后发出 | 业务动作通常连接这个信号 |
| 激活 | `pressed()` / `released()` | 按下和释放阶段的信号 | 不要把最终业务提交放在 `pressed()`，除非需要按下即执行 |
| 状态 | `setEnabled(bool) / isEnabled() const` | 控制按钮是否可用 | 禁用状态应由业务条件决定，样式会自动反映 |
| 外观 | `setFlat(bool) / isFlat() const` | 使用或读取继承的扁平按钮外观 | 这是 `QPushButton` 能力，不等于关闭命令链接语义 |
| 焦点 | `setDefault(bool)` | 在对话框中设置默认按钮 | 默认按钮和命令链接视觉主按钮是两种概念，按业务谨慎设置 |
| 快捷键 | `setShortcut(const QKeySequence &)` | 为按钮设置键盘快捷键 | 需要考虑平台习惯和可访问性 |

## 11. 选择建议

可以用一个简单判断：

> 如果用户只需要知道“做什么”，用 `QPushButton`；如果用户还需要知道“会带来什么结果”，再考虑 `QCommandLinkButton`。

它的核心不是更大的按钮，而是把动作说明纳入决策界面。把标题写短、把描述写准、让布局使用尺寸提示，通常比重写绘制代码更能发挥这个类的价值。
