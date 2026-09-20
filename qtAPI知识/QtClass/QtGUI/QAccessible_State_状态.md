# Qt QAccessible::State 深入笔记

> 适用版本：Qt 6.11.1  
> 定义位置：`#include <QAccessible>`  
> 所属模块：`Qt6::Gui`  
> 定位：可访问对象状态的位字段值类型

## 1. 它解决什么问题

`QAccessible::State` 把一个可访问对象在当前时刻的交互与可见状态打包为一组布尔位。辅助技术通过 `QAccessibleInterface::state()` 读取这些位，进而知道对象是否可聚焦、是否禁用、是否已选中、是否展开、是否在屏幕外或是否已经失效。

它描述的是**语义状态**，不是 QWidget 或 QML 项的完整运行时快照：

- `focused` 不等同于“鼠标悬停”；
- `selected` 不等同于文本选区；
- `invisible` 不等同于对象已销毁；
- `invalid`/`defunct` 表示对象不能再正常使用；
- `offscreen` 表示被可视区域裁掉，屏幕外对象也应视为不可见；
- 状态本身不发送事件，状态变化时还应发送合适的 `QAccessibleStateChangeEvent`。

## 2. 实际使用场景

自定义控件的 accessible interface 需要把控件真实状态翻译为 `State`：

```cpp
QAccessible::State MyButtonAccessible::state() const
{
    QAccessible::State result;
    result.focusable = button()->focusPolicy() != Qt::NoFocus;
    result.focused = button()->hasFocus();
    result.disabled = !button()->isEnabled();
    result.invisible = !button()->isVisible();
    result.checkable = button()->isCheckable();
    result.checked = button()->isChecked();
    return result;
}
```

控件状态改变时，事件必须只标出改变的位：

```cpp
QAccessible::State changed;
changed.checked = true;
QAccessibleStateChangeEvent event(button, changed);
QAccessible::updateAccessibility(&event);
```

上例中的 `changed` 不是完整 state，而是“本次变化涉及 `checked` 位”的掩码语义。不要把完整状态直接当作 changed state 发送，否则辅助技术可能误判一大批状态都发生改变。

## 3. 构造与值语义

### `State()`

默认构造函数把所有状态位设为 `false`。它适合从零开始描述当前状态，也适合作为状态变化掩码。

`State` 是轻量值类型，可复制、作为返回值传递和在栈上创建。它不拥有 QObject、可访问接口或平台资源。默认值不代表对象一定有效，只代表所有已知状态位都未置位。

## 4. 状态位速览

### 激活、焦点与可用性

| 字段 | 含义 | 容易混淆的边界 |
| --- | --- | --- |
| `active` | 活动窗口，或容器中获得容器焦点时将激活的子元素。 | 不等同于 `focused`。 |
| `focusable` | 对象可接收焦点。 | 只有活动窗口中的对象才能真正获得焦点。 |
| `focused` | 对象当前拥有键盘焦点。 | 应同时满足真实焦点状态，而非仅可聚焦。 |
| `disabled` | 用户不可用，例如禁用控件。 | 不等同于 `readOnly`。 |
| `busy` | 当前暂时不能接受输入。 | 完成后应清除并报告变化。 |
| `modal` | 阻止其他对象输入。 | 用于模态对象语义，不是普通弹出层。 |

### 选择、勾选与值

| 字段 | 含义 | 容易混淆的边界 |
| --- | --- | --- |
| `selectable` | 该对象可被选中。 | 指对象/子项选择，不是文本选择。 |
| `selected` | 对象当前被选中。 | 独立于 `selectableText`。 |
| `multiSelectable` | 容器支持同时选多个项。 | 不表示当前已经有多个被选中。 |
| `extSelectable` | 支持扩展选择。 | 表示选择模型能力。 |
| `selectableText` | 文本可被选择。 | 不等同于 item `selectable`。 |
| `checkable` | 可以勾选。 | 不表示当前被勾选。 |
| `checked` | 当前已勾选。 | 三态控件的半选应使用 `checkStateMixed`。 |
| `checkStateMixed` | 三态勾选框半选。 | 通常不能简单和 `checked` 互换。 |

### 展开、可见与生命周期

| 字段 | 含义 | 容易混淆的边界 |
| --- | --- | --- |
| `expandable` | 可以展开，常用于树视图单元格。 | 不表示已经展开。 |
| `expanded` | 子项当前可见的展开状态。 | 应和 `expandable` 的能力保持一致。 |
| `collapsed` | 当前折叠，例如关闭的树项或最小化窗口。 | 与 `expanded` 通常互斥。 |
| `invisible` | 用户不可见。 | 屏幕外对象也应为不可见。 |
| `offscreen` | 被可见区域裁掉。 | 也应同时表达不可见语义。 |
| `invalid` | 对象因删除等原因不再有效。 | 之后不能继续提供普通接口数据。 |
| `defunct` | 可访问对象已经不再存在。 | 属于生命周期终止语义。 |

### 文本与编辑

| 字段 | 含义 | 容易混淆的边界 |
| --- | --- | --- |
| `editable` | 有文本插入光标，通常实现文本接口。 | 不等于可修改，`readOnly` 可同时为真。 |
| `readOnly` | 通常可编辑的对象被显式设为只读。 | 不等同于 `disabled`。 |
| `multiLine` | 多行文本或自动换行。 | 不等同于存在多个 paragraph。 |
| `passwordEdit` | 密码输入字段。 | 不应通过文本接口泄露实际密码。 |
| `searchEdit` | 用于搜索查询的单行编辑框。 | 表示语义角色补充。 |
| `supportsAutoCompletion` | 支持自动完成。 | 不表示自动完成弹窗当前已展开。 |

### 交互与表现

| 字段 | 含义 | 容易混淆的边界 |
| --- | --- | --- |
| `pressed` | 当前被按下。 | 短暂交互状态，不能长期遗留。 |
| `hotTracked` | 外观会随鼠标位置敏感变化。 | 不等同于 `focused`。 |
| `hasPopup` | 会打开弹出内容。 | 不代表 popup 当前已显示。 |
| `defaultButton` | 对话框默认按钮。 | 不等于当前拥有焦点。 |
| `movable` | 可以移动。 | 常见于窗口或可拖动对象。 |
| `sizeable` | 可以调整大小。 | 常见于顶层窗口。 |
| `linked` | 与其他对象关联，例如超链接。 | `traversed` 才表示已访问。 |
| `traversed` | 链接已经访问。 | 应只用于链接语义。 |
| `animated` | 外观频繁变化。 | 可提示辅助技术注意更新频率。 |
| `marqueed` | 显示滚动内容，例如日志视图。 | 不等于普通可滚动容器。 |
| `selfVoicing` | 自己通过语音或声音描述自身。 | 辅助技术可据此避免重复播报。 |

## 5. 实现边界

### 状态必须来自真实 UI

不要为了让读屏“好听”而报告与实际控件不符的 `enabled`、`focused` 或 `checked` 状态。辅助技术依赖状态决定是否提供操作；错误状态会造成无法操作或误操作。

### 报告变化而非轮询

`state()` 只提供当前查询。状态改变时，使用 `QAccessibleStateChangeEvent` 和 `QAccessible::updateAccessibility()` 主动通知，尤其是焦点、禁用、展开、选择和勾选变化。

### 保持状态组合自洽

常见规则包括：

- `disabled` 的对象不应在 action interface 中暴露可执行操作；
- `expanded` 通常要求 `expandable`；
- `selected` 通常要求 `selectable`；
- `checkStateMixed` 通常要求 `checkable`；
- `offscreen` 应结合 `invisible`；
- `invalid` 或 `defunct` 后不要继续访问底层已释放对象。

## API 速查表

| 类别 | API/字段 | 作用 | 使用边界 |
| --- | --- | --- | --- |
| 构造 | `State()` | 创建全部位为 `false` 的状态。 | 可表示完整 state 或变化掩码。 |
| 焦点 | `active`、`focusable`、`focused` | 描述活动性与键盘焦点。 | 三者不是同义词。 |
| 可用性 | `disabled`、`busy`、`modal` | 描述可操作性和输入限制。 | `disabled` 不等于 `readOnly`。 |
| 选择 | `selectable`、`selected`、`multiSelectable`、`extSelectable`、`selectableText` | 描述对象和文本选择语义。 | item 选择与文本选择分开。 |
| 勾选 | `checkable`、`checked`、`checkStateMixed` | 描述二态/三态勾选。 | 半选不等价于已勾选。 |
| 结构 | `expandable`、`expanded`、`collapsed` | 描述树和折叠内容。 | 状态组合要保持一致。 |
| 生命周期 | `invisible`、`offscreen`、`invalid`、`defunct` | 描述可见性和有效性。 | 失效对象不能继续提供普通数据。 |
| 文本 | `editable`、`readOnly`、`multiLine`、`passwordEdit`、`searchEdit`、`supportsAutoCompletion` | 描述文本编辑语义。 | 可编辑能力与可修改状态分开。 |
| 表现 | `animated`、`marqueed`、`selfVoicing` | 描述动态和播报特征。 | 仅报告真实的辅助技术相关特征。 |
| 交互 | `pressed`、`hotTracked`、`hasPopup`、`defaultButton`、`movable`、`sizeable` | 描述交互状态或能力。 | 不要把短暂状态长期置位。 |
| 链接 | `linked`、`traversed` | 描述链接和访问历史。 | 仅用于链接语义。 |

### 一句话总结

`QAccessible::State` 是可访问对象的语义状态位集合：完整状态必须忠实反映真实 UI，状态变化必须配合无障碍事件通知，而 `State` 作为变化事件参数时应只标出真正改变的位。
