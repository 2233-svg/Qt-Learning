# Qt QStyleOptionHeaderV2 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleOptionHeaderV2>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionHeader -> QStyleOptionHeaderV2`  
> 常见协作者：`QHeaderView`、`QStyle`

## 1. 它解决什么问题

`QStyleOptionHeaderV2` 是 `QStyleOptionHeader` 的扩展数据包。基础类已经描述了表头文字、图标、排序箭头、section 的视觉位置和选择邻接关系；V2 再补充两件在现代表格交互中很重要的信息：

1. **文字太长时在哪里显示省略号**。
2. **用户拖动列时，当前 section 是否是插入落点**。

```text
QStyleOptionHeader
  ├─ 文本、图标、对齐
  ├─ section / orientation / position
  ├─ 选择邻接关系、排序箭头
  └─ 通用 style 状态

QStyleOptionHeaderV2
  ├─ textElideMode：文字如何截断
  └─ isSectionDragTarget：拖动 section 的插入目标
```

它依旧不是一个表头控件，也不负责移动列或截断文字；它仅把这次绘制所需信息交给 `QStyle`。真正处理列移动的是 `QHeaderView`，真正决定像素排版的是当前 style。

## 2. 为什么还会有一个 V2

Qt 头文件将它标注为“计划在 Qt 7 合并回 `QStyleOptionHeader`”的兼容性扩展类。对笔记使用者来说，这意味着：

- 写普通表格、树视图业务时，几乎不需要显式创建 V2。
- 重写 `QHeaderView::paintSection()` 或实现 style 时，遇到 V2 才读取它新增的两个字段。
- 不要因为名称里有 V2，就自己维护一套“旧版/新版表头绘制分支”；应先按 `QStyleOptionHeader` 写通用逻辑，再在确认参数确为 V2 时使用扩展数据。

这不是“功能更强的 `QHeaderView`”，而是 style option 的 ABI/兼容性演进形式。

## 3. 构建与典型使用

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 在自定义 style 中读取 V2 扩展字段

style 的入口参数通常是 `const QStyleOption *`。先把它当作 `QStyleOptionHeader` 处理基础信息；只有需要 V2 的截断或拖拽状态时，再安全转换：

```cpp
#include <QProxyStyle>
#include <QStyleOptionHeaderV2>

class HeaderFeedbackStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_HeaderSection) {
            if (const auto *header =
                    qstyleoption_cast<const QStyleOptionHeader *>(option)) {
                // 这里可读取 header->section、header->position 等基础数据。
                (void)header;
            }

            if (const auto *headerV2 =
                    qstyleoption_cast<const QStyleOptionHeaderV2 *>(option)) {
                if (headerV2->isSectionDragTarget) {
                    // 在调用基类绘制前后加入插入落点的视觉提示。
                }
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

`qstyleoption_cast()` 会检查 type 和 version。不能把任意 `QStyleOption *` 直接 `static_cast` 成 V2：绘制一个 header 的调用方可以只传入基础 `QStyleOptionHeader`，此时读取扩展字段是未定义行为。

## 4. `textElideMode`：文字截断的语义

当表头 section 的可用宽度不足以完整显示 `text` 时，`textElideMode` 指定 style 应把省略号放在哪一侧。

| 值 | 效果 | 适合的内容 |
| --- | --- | --- |
| `Qt::ElideLeft` | 左侧省略，例如 `...report.csv`。 | 文件名后缀、路径末段等“末尾更重要”的文字。 |
| `Qt::ElideRight` | 右侧省略，例如 `Customer repr...`。 | 普通自然语言标题，保留开头更易识别。 |
| `Qt::ElideMiddle` | 中间省略，例如 `project...config`。 | 两端都具有辨识度的标识符。 |
| `Qt::ElideNone` | 不要求插入省略号。 | 宽度已足够，或由自定义 style 自行处理溢出。 |

默认值是 `Qt::ElideNone`。它不等于“文字保证完整显示”，而是 option 没有要求 style 使用省略号；最后如何处理由实际 style 和可用矩形决定。

`textElideMode` 只描述**绘制策略**，不会改变 `text` 字符串，也不会影响模型中的 header data。不要把已经带 `...` 的字符串写回模型；这样在表头变宽后，原始文字也无法恢复。

```cpp
QStyleOptionHeaderV2 option;
option.text = "Very long transaction reference";
option.textElideMode = Qt::ElideRight;
```

若你在 `QHeaderView` 子类中想统一控制省略策略，优先配置/复用视图已有的初始化流程，而不是在每个 `paintSection()` 中按像素手工截断文本。

## 5. `isSectionDragTarget`：列拖动的落点，不是“正在拖动”

用户启用 `QHeaderView::setSectionsMovable(true)` 后，可以拖动 section 调整视觉顺序。拖动过程中，某一位置需要提示“如果此时松开鼠标，正在拖动的 section 会插入这里”。

`isSectionDragTarget == true` 表示当前正在绘制的 section 就是这个**插入目标位置**。

```text
拖动“金额”列：

[日期] [客户] [金额] [状态]
               ↓
[日期] [客户] |插入这里| [状态]
```

它不表示：

- 当前 section 是被拖起来移动的那一列。
- 用户只是把鼠标悬停在当前 section。
- 当前 section 被选中或被按下。

这些状态分别属于拖拽实现、`QStyleOption::state` 或 `QHeaderView` 的交互逻辑。自定义 style 只应把它用于落点提示，例如更明显的边线或间隙，不应据此修改模型顺序。

## 6. 它和 `QHeaderView` 的协作边界

`QHeaderView` 负责 section 的模型映射、拖放判定、点击和几何；V2 只是让 style 看见这次绘制的附加上下文。

| 需求 | 应找的类型 | 不应只改 V2 字段的原因 |
| --- | --- | --- |
| 允许/禁止用户拖动列 | `QHeaderView::setSectionsMovable()` | `isSectionDragTarget` 不会开启拖动。 |
| 实际移动 section | `QHeaderView::moveSection()` | option 不保存或改变视觉顺序。 |
| 表头标题 | 模型的 `headerData()` | `text` 是绘制快照，改它不会持久更新模型。 |
| 长文本展示偏好 | `QHeaderView`/style 的现有配置或 V2 的绘制数据 | V2 不会修改文本本身。 |
| 绘制插入落点提示 | `QStyle` / `QProxyStyle` | V2 的 `isSectionDragTarget` 正是这里的输入。 |

`QStyleOptionHeaderV2` 仍然继承基础类的全部字段，例如 `rect`、`state`、`text`、`section`、`position` 和 `sortIndicator`。阅读 V2 时不要遗漏基础页中的逻辑索引与视觉位置之分。

## 7. 类型、版本与生命周期

头文件为 V2 单独定义了以下类型常量：

| 常量 | 值 | 用途 |
| --- | --- | --- |
| `QStyleOptionHeaderV2::Type` | `QStyleOption::SO_Header` | 表明它仍是一种表头 option。 |
| `QStyleOptionHeaderV2::Version` | `2` | 表明它包含基础类 version 1 没有的扩展字段。 |

因此，V2 与基础类的 type 相同，但 version 更高。style 代码若仅需要基础字段，可以接受 `QStyleOptionHeader`；需要 `textElideMode` 或 `isSectionDragTarget` 时则必须以 V2 版本安全转换。

它是短生命周期值对象：

```cpp
QStyleOptionHeaderV2 option;
// 填写字段并立即传给 style。
```

没有父子对象、没有事件循环依赖、不拥有 `QHeaderView` 或 `QPainter`。不要保存 option 指针到绘制结束之后。

## 8. 常见误区与排查

### 8.1 “设置 `textElideMode` 后，模型里的标题也出现省略号”

不会。该字段只影响这次 style 绘制；模型数据保持原样。若看到模型文本被改写，问题在业务代码，而不在 V2。

### 8.2 “列没有设置可移动，为什么 `isSectionDragTarget` 从未为真”

这是正常的。没有可进行的 section 拖动，就没有插入目标。先检查 `setSectionsMovable(true)` 和是否由 `QHeaderView` 的正常交互流程生成该 option。

### 8.3 “我根据 `isSectionDragTarget` 调了 `moveSection()`”

不要这样做。该字段只描述当前已经发生的拖动反馈；在绘制函数中改变 section 顺序会干扰事件处理，可能导致重绘或位置抖动。

### 8.4 “自定义 style 总能转换成 V2”

不能假设。style API 面向基类指针，调用方可能提供基础 version 1 option。需要扩展字段时使用 `qstyleoption_cast<const QStyleOptionHeaderV2 *>` 并处理空指针。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionHeaderV2()` | 创建并以默认值初始化一份带扩展字段的表头绘制参数。 | 是短生命周期值对象；通常在当前绘制调用中创建、填写并立即使用。 |
| 构造 | `QStyleOptionHeaderV2(const QStyleOptionHeaderV2 &other)` | 创建另一个 V2 表头 option 的值副本。 | 复制字段，不转移 `QHeaderView`、模型、painter 或 style 的所有权。 |
| 类型常量 | `QStyleOptionHeaderV2::StyleOptionType::Type` | 提供值为 `SO_Header` 的运行时类型标识。 | 与基础表头 option 共用 type；仅检查 type 不能确认对象包含 V2 字段。 |
| 类型常量 | `QStyleOptionHeaderV2::StyleOptionVersion::Version` | 表示 V2 数据布局版本，Qt 6.11.1 中为 `2`。 | 需要读取扩展字段时用 `qstyleoption_cast()` 同时检查 type 和 version。 |
| 公共字段 | `Qt::TextElideMode textElideMode` | 指定表头文字不足以完整显示时省略号的位置策略。 | 默认 `Qt::ElideNone`；只影响本次绘制，不修改原始 `text` 或模型数据。 |
| 公共字段 | `bool isSectionDragTarget` | 标识当前 section 是否是拖动 section 的插入落点。 | 只用于视觉反馈，不代表拖动源、悬停或选中，也不会自动移动列。 |
| 继承字段 | `QStyleOptionHeader::text` | 提供待绘制的表头标题文字。 | style 通常结合 `textElideMode` 决定最终显示文本。 |
| 继承字段 | `QStyleOptionHeader::position` | 提供当前 section 在视觉序列中的首、中、尾位置。 | 列拖动后它与 logical index 可能不同，不能用 `section` 数字替代。 |
| 继承字段 | `QStyleOption::state` | 提供启用、按下、悬停、选中等通用绘制状态。 | 它与 `isSectionDragTarget` 属于不同维度，不能相互替代。 |
| 初始化 | `QHeaderView::initStyleOptionForIndex(...)` | 从真实 header 和指定逻辑 section 填充基础表头绘制数据。 | V2 字段是否被填充取决于调用方的版本和绘制流程，不能默认总是存在。 |
| 行为配置 | `QHeaderView::setSectionsMovable(bool)` | 开启或关闭用户拖动 section 的能力。 | 不开启拖动通常不会产生有效的拖动目标状态；它不会由 option 字段反向开启。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_HeaderSection, ...)` | 让当前 style 绘制一个表头 section。 | V2 字段供 style 读取；绘制期间不要调用 `moveSection()` 改变模型映射。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionHeaderV2 *>(option)` | 从基类 option 安全识别是否真的包含 V2 扩展字段。 | 失败返回空指针；不要用无条件 `static_cast` 读取 `mouseDown` 类似的扩展数据。 |

---

### 一句话总结

`QStyleOptionHeaderV2` 在基础表头绘制数据上补充了“长标题怎么截断”和“列拖动将插在哪里”：`textElideMode` 只影响显示策略，`isSectionDragTarget` 只提供拖放落点反馈；二者都由 `QHeaderView` 的交互和 `QStyle` 的绘制协作完成，而不是用来直接改模型或移动列。
