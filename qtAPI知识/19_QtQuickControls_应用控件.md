# Qt Quick Controls：应用控件与界面工程化

> Qt Quick Controls 2 提供跨平台的按钮、输入框、列表、弹窗、菜单和导航容器。它们已经处理了大量键盘、触摸、焦点和可访问性细节；使用时应先理解控件的状态模型，再决定何时自定义视觉样式。

## 1. ApplicationWindow：应用级根窗口

```qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 900
    height: 600
    title: qsTr("任务中心")

    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            ToolButton { text: qsTr("刷新"); onClicked: controller.refresh() }
            Label { text: qsTr("任务中心"); Layout.fillWidth: true }
        }
    }

    footer: StatusBar {
        Label { text: qsTr("就绪") }
    }

    Page {
        anchors.fill: parent
        padding: 16
    }
}
```

`ApplicationWindow` 在 `Window` 基础上提供 `menuBar`、`header`、`footer` 和内容区域。页面内容通常放在默认内容数据中，或使用 `Page`、`StackView` 组织。

## 2. Control 的通用状态

绝大多数 Controls 派生自 `Control` 或 `AbstractButton`，具有以下常见概念：

- `enabled`：是否允许交互；
- `visible`：是否参与显示；
- `focusPolicy`：鼠标、键盘或无焦点；
- `hovered`、`pressed`、`checked`：交互状态；
- `padding`、`leftPadding` 等：内容与背景之间的空间；
- `contentItem`、`background`、`indicator`：可替换的视觉部件。

状态和视觉分离后，业务逻辑应读取 `checked`/`pressed` 等语义属性，而不是查找内部矩形颜色。

## 3. Button、ToolButton 与 Action

### 3.1 基本按钮

```qml
Button {
    text: qsTr("保存")
    enabled: form.valid && !controller.busy
    onClicked: controller.save(form.values)
}
```

按钮的 `clicked` 信号只描述用户触发动作。耗时操作应立即将 `busy` 状态反馈给用户，避免重复提交。

### 3.2 Action 复用命令

```qml
Action {
    id: refreshAction
    text: qsTr("刷新")
    shortcut: StandardKey.Refresh
    onTriggered: controller.refresh()
}

ToolButton { action: refreshAction }
MenuItem { action: refreshAction }
```

同一个 `Action` 绑定到工具栏按钮和菜单项时，`enabled`、`checkable`、`checked`、`text` 和图标状态可以同步。命令复用比在每个控件中复制处理器更不易漂移。

### 3.3 CheckBox、RadioButton 和 ButtonGroup

```qml
ButtonGroup {
    id: displayGroup
    buttons: [compactButton, comfortableButton]
}

RadioButton { id: compactButton; text: qsTr("紧凑") }
RadioButton { id: comfortableButton; text: qsTr("舒适") }
```

`RadioButton` 和 `TabButton` 默认具有互斥倾向；显式使用 `ButtonGroup` 可以跨层级管理互斥关系。需要持久化的选项应绑定到模型或设置对象，而不是只依赖控件实例。

## 4. 文本输入与验证

### 4.1 TextField

```qml
TextField {
    id: emailField
    placeholderText: qsTr("邮箱")
    inputMethodHints: Qt.ImhEmailCharactersOnly
    validator: RegularExpressionValidator {
        regularExpression: /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/
    }
}
```

`TextField` 适合单行输入，`TextArea` 适合多行。`validator` 负责输入约束，但业务层仍要在提交时再次验证，因为文本可能由粘贴、脚本或模型赋值产生。

### 4.2 密码和提交

```qml
TextField {
    echoMode: TextInput.Password
    onAccepted: loginButton.clicked()
}
```

密码输入不应写入日志或错误提示；提交动作应支持 Enter，也应提供鼠标、触摸和辅助技术可用的按钮。

## 5. 数值和范围控件

```qml
RowLayout {
    SpinBox {
        from: 0
        to: 100
        value: 25
        editable: true
    }

    Slider {
        from: 0
        to: 1
        value: 0.4
        Layout.fillWidth: true
    }
}
```

`SpinBox` 的 `from`、`to`、`stepSize` 定义离散范围；`Slider` 使用连续或离散值。显示文本需要格式化时，使用 `textFromValue`/`valueFromText` 或单独的格式化函数，避免把本地化字符串直接当作数值。

## 6. ComboBox 与模型

```qml
ComboBox {
    id: priorityBox
    model: [qsTr("低"), qsTr("中"), qsTr("高")]
    currentIndex: 1
    onActivated: controller.setPriority(currentIndex)
}
```

复杂数据应使用带角色的模型：

```qml
ComboBox {
    textRole: "label"
    valueRole: "id"
    model: ListModel {
        ListElement { label: "普通"; id: 1 }
        ListElement { label: "紧急"; id: 2 }
    }
    onActivated: controller.setPriority(currentValue)
}
```

区分展示角色和业务值角色，避免在业务代码中解析显示文本。

## 7. Popup、Dialog、Drawer

### 7.1 Popup

```qml
Popup {
    id: toast
    anchors.centerIn: Overlay.overlay
    padding: 12
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    Label { text: qsTr("已保存") }
}

function showToast() {
    toast.open()
}
```

Popup 有 `opened`、`aboutToShow`、`aboutToHide` 等生命周期信号。需要模态阻塞时设置 `modal: true`，并确认关闭策略不会让用户丢失未提交输入。

### 7.2 Dialog

```qml
Dialog {
    id: confirmDialog
    title: qsTr("确认删除")
    modal: true
    standardButtons: Dialog.Ok | Dialog.Cancel

    Label { text: qsTr("删除后无法恢复，是否继续？") }

    onAccepted: controller.removeCurrent()
}
```

对话框结果应通过 `accepted`/`rejected` 或按钮点击传给业务层。不要在 Dialog 内直接修改多个页面的状态；让控制器处理最终命令更容易测试。

### 7.3 Drawer

```qml
Drawer {
    id: drawer
    width: Math.min(window.width * 0.8, 320)
    edge: Qt.LeftEdge

    ListView {
        anchors.fill: parent
        model: navigationModel
        delegate: ItemDelegate {
            width: parent.width
            text: model.title
            onClicked: {
                stack.replace(model.component)
                drawer.close()
            }
        }
    }
}
```

Drawer 是导航容器而不是普通浮层。关闭时要恢复焦点到触发它的控件，保证键盘和屏幕阅读器用户仍能继续操作。

## 8. Menu、MenuBar 和 ContextMenu

```qml
MenuBar {
    Menu {
        title: qsTr("文件")
        Action { text: qsTr("新建"); shortcut: StandardKey.New; onTriggered: controller.create() }
        MenuSeparator {}
        Action { text: qsTr("退出"); onTriggered: Qt.quit() }
    }
}
```

菜单项优先复用 `Action`，以同步快捷键和启用状态。上下文菜单应提供与当前选择相关的命令，并在对象被删除或失去上下文时关闭。

## 9. StackView 与 TabBar 导航

### 9.1 StackView

```qml
RowLayout {
    anchors.fill: parent

    StackView {
        id: stack
        Layout.fillWidth: true
        Layout.fillHeight: true
        initialItem: dashboardPage
    }

    Component {
        id: dashboardPage
        Page { Label { anchors.centerIn: parent; text: qsTr("概览") } }
    }
}
```

`push()`、`pop()`、`replace()` 管理页面栈。页面之间传参可通过初始属性或显式属性接口完成，避免用全局上下文变量隐式传递。

### 9.2 TabBar + SwipeView

```qml
ColumnLayout {
    TabBar {
        id: tabs
        Layout.fillWidth: true
        TabButton { text: qsTr("概览") }
        TabButton { text: qsTr("设置") }
    }

    SwipeView {
        currentIndex: tabs.currentIndex
        Layout.fillWidth: true
        Layout.fillHeight: true
        Page { }
        Page { }
    }
}
```

`TabBar.currentIndex` 与 `SwipeView.currentIndex` 应保持单一绑定方向，避免双向绑定循环。页面较重时可结合 Loader 延迟创建。

## 10. 自定义 Control 的方法

### 10.1 替换 background 和 contentItem

```qml
Button {
    id: button
    contentItem: Text {
        text: button.text
        color: button.enabled ? "white" : "#94a3b8"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 36
        radius: 4
        color: button.pressed ? "#1d4ed8" : "#2563eb"
    }
}
```

自定义视觉时保留控件的语义属性、焦点、可访问性和默认输入行为。背景和内容项都应提供合理 implicit size，否则布局可能坍缩。

### 10.2 何时做独立组件

只改颜色、间距或字体时，优先使用主题或样式属性；需要新增业务状态、多个交互区域或跨页面复用时，再封装独立 QML 类型。不要把所有控件复制成“带颜色的 Button”，这会使键盘和平台风格逐渐分叉。

## 11. 样式与主题

Qt Quick Controls 支持 Basic、Fusion、Imagine、Material、Universal 等样式（具体可用样式依部署而定）。可以通过环境变量或 `QQuickStyle` 选择样式，也可以在 QML 中统一设置调色板和字体。

```cpp
#include <QQuickStyle>

QQuickStyle::setStyle(QStringLiteral("Fusion"));
```

样式选择应在创建控件前完成。不要混用多个样式目录的私有实现；自定义样式需要提供完整控件模板并处理高 DPI、键盘焦点、禁用状态和 RTL 布局。

## 12. 键盘、焦点和可访问性

```qml
Button {
    text: qsTr("应用")
    focusPolicy: Qt.StrongFocus
    Accessible.name: qsTr("应用设置")
    Accessible.description: qsTr("保存当前设置")
}
```

Controls 通常已经提供合理的焦点链。自定义 `contentItem` 时不要覆盖焦点属性；对话框打开后应把焦点放到第一个可操作控件，关闭后恢复原焦点。

## 13. 性能和生命周期

- Popup/Drawer 中的重内容可用 Loader 延迟创建；
- 大列表使用模型视图，不要手动创建数千个控件；
- 页面切换时明确是否保留状态，避免 StackView 无限增长；
- 绑定到 `currentIndex` 等高频属性时，确保表达式轻量；
- 弹窗关闭后及时停止定时器、网络请求和动画。

## 14. 常见问题

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| Button 没有可见内容 | 自定义 contentItem 未设置尺寸 | 提供 implicit size 和对齐属性 |
| ComboBox 业务值错误 | 使用显示文本当作 ID | 设置 `textRole`/`valueRole` |
| Dialog 关闭后重复提交 | 处理器和按钮逻辑各执行一次 | 统一由 `accepted` 或 action 触发 |
| Tab 页面互相跳动 | currentIndex 双向绑定 | 选择一个单一数据源 |
| 自定义控件键盘不可用 | 覆盖模板时丢失 focusPolicy | 保留 Control/AbstractButton 行为 |
| Popup 被内容裁剪 | 放在普通 Item 中且超出边界 | 使用 Overlay 或合理的 parent |

## 15. 自测题

1. 为什么推荐用 Action 复用菜单和工具栏命令？
2. ComboBox 的 `textRole` 与 `valueRole` 分别解决什么问题？
3. 自定义 Button 的 contentItem 需要注意哪些尺寸和状态？
4. Dialog 的业务结果应该在哪里处理？
5. 为什么 TabBar 与 SwipeView 不应互相建立复杂双向绑定？

### 参考答案

1. 它统一命令处理、快捷键、启用和勾选状态，避免多个控件逻辑漂移。
2. `textRole` 控制显示文本，`valueRole` 提供稳定的业务值。
3. 提供 implicit size、处理 enabled/pressed/focus 状态，并保留可访问性和输入语义。
4. 由 Dialog 的 accepted/rejected 或统一 Action 触发控制器命令。
5. 双向依赖容易形成循环更新；应让一个状态源驱动另一个控件。

## 16. 小结

Qt Quick Controls 的价值是把交互语义、平台适配和视觉模板分层。实际开发中先用标准控件和 Action 组装流程，再在明确的组件边界上定制 `background`、`contentItem` 或主题。这样能同时得到一致的用户体验、可测试的业务逻辑和可维护的样式体系。
