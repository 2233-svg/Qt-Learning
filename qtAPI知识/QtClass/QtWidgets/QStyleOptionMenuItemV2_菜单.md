# Qt QStyleOptionMenuItemV2 深入笔记

> 适用版本：Qt 6.11.1（本类自 Qt 6.11 起提供）  
> 头文件：`#include <QStyleOptionMenuItemV2>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QStyleOption -> QStyleOptionMenuItem -> QStyleOptionMenuItemV2`

## 1. 它解决什么问题

`QStyleOptionMenuItemV2` 在 `QStyleOptionMenuItem` 的完整菜单项绘制数据上，新增了一个 `mouseDown` 字段。它解决的是一个很具体却很重要的状态歧义：

> `QStyle::State_Sunken` 被设置时，菜单项不一定正被鼠标按住。

菜单已经打开其弹出子菜单时，style 也可能看到 `State_Sunken`。如果自定义 style 把所有 `State_Sunken` 都画成“鼠标压下去”的效果，用户松开鼠标后仍会看到过重的按压态，菜单栏和子菜单的视觉反馈就不自然。

```text
State_Sunken == true
  ├─ 鼠标当前仍按下：应表现为真正的 press
  └─ 菜单/子菜单处于打开状态：可能只需表现为 active/open

QStyleOptionMenuItemV2::mouseDown
  └─ 精确回答“鼠标是否正按下”
```

它不是鼠标事件，也不会改变菜单打开状态；它只是此次 `QStyle::CE_MenuItem` / `CE_MenuBarItem` 绘制所需的补充上下文。

## 2. 与基础类的关系

基础 `QStyleOptionMenuItem` 负责菜单项的主体信息：

- 文本和快捷键列。
- 图标列与勾选列。
- 普通项、子菜单、分隔线等 `menuItemType`。
- `checked`、`checkType`、`State_Selected`、`State_Enabled` 等状态。

V2 仅增加：

| V2 字段 | 解决的缺口 |
| --- | --- |
| `mouseDown` | 从含义较宽的 `State_Sunken` 中识别“鼠标物理按下”这一严格状态。 |

Qt 头文件也注明该 V2 类计划在 Qt 7 合并回基础类。因此编写 style 时应先以 `QStyleOptionMenuItem` 处理通用菜单逻辑，再把 V2 当作可选扩展读取，而不是假设每次菜单绘制都一定给出 V2。

## 3. 构建与使用场景

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

qmake 工程使用 `QT += widgets`。

### 3.2 自定义 style 中区分“按住”与“菜单已打开”

`drawControl()` 的参数类型是基类 `QStyleOption *`。先检查基础 menu item，再按需尝试 V2：

```cpp
#include <QProxyStyle>
#include <QStyleOptionMenuItemV2>

class MenuPressStyle final : public QProxyStyle
{
public:
    using QProxyStyle::QProxyStyle;

    void drawControl(ControlElement element,
                     const QStyleOption *option,
                     QPainter *painter,
                     const QWidget *widget = nullptr) const override
    {
        if (element == CE_MenuItem || element == CE_MenuBarItem) {
            const auto *item =
                qstyleoption_cast<const QStyleOptionMenuItem *>(option);
            const auto *itemV2 =
                qstyleoption_cast<const QStyleOptionMenuItemV2 *>(option);

            const bool isSunken =
                item && (item->state & State_Sunken);
            const bool isPhysicalPress = itemV2 && itemV2->mouseDown;

            if (isSunken && isPhysicalPress) {
                // 仅在鼠标仍按下时添加更明显的按压反馈。
            }
        }

        QProxyStyle::drawControl(element, option, painter, widget);
    }
};
```

`itemV2` 可能为空，这是正常分支。若 style 只拿到基础 version 1 option，仍应正常调用基类 style 完成绘制。

## 4. `mouseDown` 的精确含义

`mouseDown == true` 表示鼠标当前按下。它是一个 bit field，但使用方式和普通 `bool` 一样：

```cpp
if (itemV2->mouseDown) {
    // 当前有实际的鼠标按压。
}
```

它和几个相近状态的差异如下：

| 状态 | 表示什么 | 适合做什么 |
| --- | --- | --- |
| `mouseDown` | 鼠标物理按键仍然处于按下状态。 | 绘制即时 press feedback。 |
| `QStyle::State_Sunken` | 菜单项处于 sunken/open 相关状态，可能包含真正按下，也可能表示菜单已显示。 | 保留菜单“打开/激活”视觉语义。 |
| `QStyle::State_Selected` | 当前项被鼠标或键盘导航选中。 | 绘制悬停/当前高亮行。 |
| `QStyleOptionMenuItem::checked` | 可勾选 action 的持久开关状态。 | 绘制勾选框、单选点或勾号。 |

一个菜单项可能同时 `State_Selected == true`、`State_Sunken == true`、`mouseDown == false`：这并不矛盾，例如菜单或子菜单已经打开，但用户当前没有按住鼠标。

## 5. 哪些代码不应直接设置它

普通应用不应自己构造 V2 并设置 `mouseDown` 来“模拟点击”。正确的职责划分是：

| 目标 | 正确入口 |
| --- | --- |
| 响应鼠标按下/释放 | `QMenu`/`QMenuBar` 的事件处理或 action 触发逻辑。 |
| 打开或关闭子菜单 | `QMenu` 与 `QAction` 的菜单关系。 |
| 定制按下、打开、悬停外观 | `QStyle` 或 `QProxyStyle`。 |
| 向 style 报告真实按键状态 | Qt 菜单控件内部创建的 V2 option。 |

在 `drawControl()` 内修改菜单状态、触发 action 或重新弹出菜单，会把纯绘制函数变成状态机入口，容易造成重入、闪烁和事件顺序问题。

## 6. 类型、版本与生命周期

V2 保持基础类的菜单项 type，并将 version 提升到 2：

| 常量 | 值 | 意义 |
| --- | --- | --- |
| 继承的 `QStyleOptionMenuItem::Type` | `SO_MenuItem` | 说明它仍是一种菜单项 option。 |
| `QStyleOptionMenuItemV2::Version` | `2` | 说明该对象包含 `mouseDown` 扩展字段。 |

type 相同不代表对象一定有 V2 字段，因此需要 `qstyleoption_cast<const QStyleOptionMenuItemV2 *>`。该函数同时检查 type 与 version，比直接转换可靠。

它是短生命周期值对象：

```cpp
QStyleOptionMenuItemV2 option;
// 填写后只在当前绘制调用期间传给 style。
```

没有 `QObject` 父子关系，不拥有 `QMenu`、`QAction`、`QPainter` 或 `QStyle`。复制构造函数复制当前数据快照。

## 7. 常见误区与排查

### 7.1 “有 `State_Sunken` 就应该画成鼠标按下”

不一定。子菜单处于打开状态时也可能设置 `State_Sunken`。只有 `mouseDown` 为真，才能确认此时仍是物理按压。

### 7.2 “`mouseDown` 为假，所以菜单项不应高亮”

不对。高亮由 `State_Selected` 表达，`mouseDown` 只描述鼠标按键是否按着。键盘导航菜单时，`mouseDown` 通常为假但当前项仍应有选择高亮。

### 7.3 “V2 只需 `static_cast`，因为 `CE_MenuItem` 一定来自 `QMenu`”

style 是扩展点，调用方可以传基础 `QStyleOptionMenuItem`。使用 `qstyleoption_cast()` 并在失败时退回基础逻辑。

### 7.4 “为了显示按压效果，我在 style 的绘制函数里触发 action”

不要这样做。绘制应是无副作用的；action 的触发属于菜单事件处理。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QStyleOptionMenuItemV2()` | 创建并以默认值初始化一份带 `mouseDown` 扩展的菜单项绘制参数。 | Qt 6.11 起可用；通常由菜单控件内部生成，普通业务代码很少手工构造。 |
| 构造 | `QStyleOptionMenuItemV2(const QStyleOptionMenuItemV2 &other)` | 创建另一个 V2 菜单项 option 的值副本。 | 复制绘制快照，不转移 `QMenu`、`QAction`、painter 或 style 的所有权。 |
| 类型常量 | `QStyleOptionMenuItemV2::StyleOptionType::Type` | 继承菜单项的 `SO_MenuItem` 类型标识。 | type 与基础 `QStyleOptionMenuItem` 相同，不能仅靠 type 判断是否是 V2。 |
| 类型常量 | `QStyleOptionMenuItemV2::StyleOptionVersion::Version` | 表示 V2 菜单项数据布局版本，Qt 6.11 中为 `2`。 | 需要读取 `mouseDown` 时用 `qstyleoption_cast()` 同时检查 type/version。 |
| 公共字段 | `bool mouseDown` | 精确表示鼠标物理按键当前是否仍处于按下状态。 | 它只描述绘制快照，不会触发 action、打开菜单或改变菜单状态。 |
| 继承字段 | `QStyleOptionMenuItem::state` | 提供 `State_Sunken`、`State_Selected`、`State_Enabled` 等菜单交互状态。 | `State_Sunken` 可能表示菜单已打开，不能单独证明鼠标仍按着。 |
| 继承字段 | `QStyleOptionMenuItem::checked` | 表示可勾选菜单 action 的持久选中状态。 | 与 `mouseDown`、高亮和菜单打开状态是不同维度。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_MenuItem, ...)` | 让当前 style 绘制菜单项，并可结合 V2 区分按住与打开状态。 | 自定义 style 仍应支持基础 version 1 option，不能假设每次调用都有 V2。 |
| 绘制 | `QStyle::drawControl(QStyle::CE_MenuBarItem, ...)` | 让当前 style 绘制菜单栏项目的同类状态。 | 如果 style 同时处理菜单和菜单栏，要按 `ControlElement` 分支，不能只看 option 类型。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionMenuItem *>(option)` | 先把基类 option 安全识别为基础菜单项 option。 | 即使 V2 转换失败，也可用基础字段完成降级绘制。 |
| 类型转换 | `qstyleoption_cast<const QStyleOptionMenuItemV2 *>(option)` | 安全判断当前 option 是否真正包含 V2 的 `mouseDown` 字段。 | 失败返回空指针；不要用无条件 `static_cast` 读取扩展字段。 |

---

### 一句话总结

`QStyleOptionMenuItemV2` 为 Qt 6.11 的菜单绘制补上了 `mouseDown`：它让 style 不再把“鼠标真的还按着”和“菜单/子菜单已经打开”这两种都会出现 `State_Sunken` 的情形混为一谈；普通菜单代码无需手工设置它，自定义 style 才应安全读取它。
