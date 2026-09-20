# Qt Quick 基础：Item、布局、输入与动画

> Qt Quick 建立在 QML 对象和场景图之上。`Item` 负责几何、层级、可见性和输入边界；可视类型负责绘制；视图类型负责批量创建和回收 delegate；动画负责把状态变化变成连续过渡。本篇从一个矩形开始，逐步构建可交互的页面。

## 1. Item 的几何模型

### 1.1 坐标、尺寸和层级

每个 `Item` 都有相对于父项的 `x`、`y`、`width`、`height`，以及 `visible`、`opacity`、`enabled`、`z` 等通用属性。

```qml
import QtQuick

Item {
    width: 360
    height: 200

    Rectangle {
        x: 20
        y: 30
        width: 120
        height: 60
        color: "tomato"
        z: 1
    }
}
```

`x`、`y` 描述位置，`width`、`height` 描述尺寸；`z` 只影响同一可视父项下的绘制顺序，不会改变对象树。`opacity` 会影响子项整体透明度，`visible: false` 的项不会绘制，也不会接收鼠标输入。

### 1.2 anchors 锚点

锚点用边线和中心线建立相对几何关系：

```qml
Rectangle {
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.margins: 16
    height: 48
}
```

常用简写：

```qml
Rectangle {
    anchors.fill: parent
    anchors.margins: 12
}

Text {
    anchors.centerIn: parent
}
```

同一方向上不要同时混用 anchors 和 `x`/`width` 的互相冲突的绑定。锚点只能连接有共同祖先的 Item；不能把一个对象锚定到没有可视几何的 `QtObject`。

### 1.3 anchors 与布局的选择

- 少量固定关系：使用 anchors；
- 需要行列、换行、间距和伸缩：使用 Qt Quick Layouts；
- 大量滚动项：使用 `ListView`、`GridView` 或 `TableView`；
- 不要让多个机制同时争夺同一项的宽高。

## 2. Qt Quick Layouts

### 2.1 RowLayout 与 ColumnLayout

```qml
import QtQuick
import QtQuick.Layouts

ColumnLayout {
    width: 360
    spacing: 8

    Text { text: qsTr("用户名") }
    TextField {
        Layout.fillWidth: true
    }
    Button {
        text: qsTr("提交")
        Layout.alignment: Qt.AlignRight
    }
}
```

`Layout.fillWidth`、`Layout.fillHeight` 表示愿意占用额外空间；`Layout.preferredWidth`/`preferredHeight` 是首选尺寸；`Layout.minimumWidth` 和 `maximumWidth` 限制范围。布局会综合这些约束计算子项几何。

### 2.2 布局中的 implicit size

控件应提供合理的 `implicitWidth`/`implicitHeight`，否则布局无法根据内容分配空间：

```qml
Item {
    implicitWidth: label.implicitWidth + 24
    implicitHeight: label.implicitHeight + 12

    Text {
        id: label
        anchors.centerIn: parent
    }
}
```

不要同时绑定一个布局子项的 `width` 和 `Layout.fillWidth`，否则会产生竞争。需要临时固定尺寸时，切换 `Layout.preferredWidth` 通常比改写 `width` 更清晰。

## 3. 绘制基础类型

### 3.1 Rectangle、Text 和 Image

```qml
Rectangle {
    color: "#f8fafc"
    border.color: "#cbd5e1"
    radius: 6

    Text {
        anchors.centerIn: parent
        text: qsTr("欢迎")
        color: "#0f172a"
        font.pixelSize: 18
    }
}
```

`Text` 的尺寸由 `implicitWidth`/`implicitHeight` 和换行策略决定。长文本应设置 `wrapMode`、`elide` 和可用宽度，避免遮挡其他内容。

```qml
Text {
    width: parent.width
    wrapMode: Text.WordWrap
    elide: Text.ElideRight
    maximumLineCount: 2
}
```

`Image` 使用 `source` 加载资源；大图可使用 `asynchronous: true`，并根据场景选择 `fillMode`。应监听 `status` 和 `sourceSize`，在加载失败或尺寸未知时提供占位状态。

## 4. 输入系统：从 MouseArea 到 Pointer Handlers

### 4.1 MouseArea 的适用场景

```qml
Rectangle {
    signal activated

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton
        onClicked: parent.activated()
    }
}
```

`MouseArea` 简洁、适合覆盖整块区域的点击和拖动。多个重叠 `MouseArea` 会产生事件抢占，复杂交互容易变得难以组合。

### 4.2 TapHandler、DragHandler 和 PinchHandler

Pointer Handlers 能把点击、拖动、缩放等手势拆成可组合对象：

```qml
Rectangle {
    id: card
    width: 160
    height: 100
    color: tap.pressed ? "#bfdbfe" : "#dbeafe"

    TapHandler {
        id: tap
        onTapped: console.log("点击", point.position)
    }

    DragHandler {
        target: card
        acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchScreen
    }
}
```

`target` 指定由 handler 修改几何的 Item；不设置时可以只观察手势。使用 `acceptedButtons`、`acceptedDevices`、`grabPermissions` 等属性收敛输入范围，减少多个处理器互相抢抓。

### 4.3 WheelHandler 与滚轮

```qml
WheelHandler {
    property: "contentY"
    onWheel: function (event) {
        event.accepted = true
    }
}
```

滚轮应优先交给当前可滚动区域；处理器若消费事件，要明确设置 `accepted`，否则事件可能继续传播到父级。

## 5. 键盘焦点与 Keys

### 5.1 焦点基础

```qml
Item {
    id: root
    focus: true
    Keys.onEscapePressed: root.visible = false
}
```

只有获得 active focus 的 Item 才能可靠接收键盘事件。可交互自定义项应设置 `focus: true` 或在获得焦点时调用 `forceActiveFocus()`，并提供清晰的视觉焦点反馈。

### 5.2 Keys 处理顺序

```qml
Keys.onPressed: function (event) {
    if (event.key === Qt.Key_Return) {
        submit()
        event.accepted = true
    }
}
```

不消费的按键应保持 `event.accepted = false`，让父项或其他处理器继续处理。Tab 导航、快捷键和文本输入需要协调，不能在根项无条件吞掉所有按键。

## 6. Flickable 和滚动内容

```qml
Flickable {
    anchors.fill: parent
    contentWidth: width
    contentHeight: column.implicitHeight
    clip: true

    Column {
        id: column
        width: parent.width
        spacing: 12
        Repeater {
            model: 20
            Rectangle { width: column.width; height: 40 }
        }
    }
}
```

`Flickable` 不会自动计算内容尺寸，必须正确设置 `contentWidth`/`contentHeight`。`clip: true` 防止内容绘制到视口之外。滚动条、键盘滚动和可访问性通常应使用更高层的 `ScrollView`。

## 7. ListView、GridView 与 delegate

### 7.1 ListModel + ListView

```qml
ListModel {
    id: people
    ListElement { name: "Alice"; online: true }
    ListElement { name: "Bob"; online: false }
}

ListView {
    anchors.fill: parent
    model: people
    spacing: 4

    delegate: Rectangle {
        required property string name
        required property bool online
        width: ListView.view.width
        height: 44

        Text { anchors.centerIn: parent; text: name }
        color: online ? "#dcfce7" : "#f1f5f9"
    }
}
```

delegate 是一个组件模板，视图会按需创建、复用和销毁实例。不要在 delegate 中保存只属于某一行的长期状态；滚出视口后 delegate 可能被回收。需要持久化的状态放回模型或由唯一 key 管理。

### 7.2 视图性能

- 设置稳定的 `height` 或 `implicitHeight`，避免频繁重新布局；
- 避免 delegate 内嵌复杂层级和大量绑定；
- 使用 `cacheBuffer` 平衡滚动流畅度与内存；
- 大数据集使用 C++ 模型的增量更新，而不是每次重建整个 `ListModel`；
- 通过 `reuseItems` 和 `ListView.onReused`/`onPooled` 处理复用状态。

## 8. Behavior 与动画

### 8.1 Behavior：属性变化的默认动画

```qml
Rectangle {
    id: panel
    width: expanded ? 320 : 160
    property bool expanded: false

    Behavior on width {
        NumberAnimation { duration: 180; easing.type: Easing.OutCubic }
    }
}
```

`Behavior on property` 会捕获该属性的变化并自动动画。它适合“每次变化都要平滑”的属性。用户主动拖动、键盘操作或减少动画设置时，应考虑关闭或缩短动画。

### 8.2 NumberAnimation、OpacityAnimator 和 RotationAnimation

```qml
NumberAnimation on opacity {
    from: 0
    to: 1
    duration: 200
}
```

Animator 类型通常在场景图线程上更新渲染属性，适合高频视觉变化；普通 Animation 更适合同时驱动多个 QML 属性。选择时关注被动画属性和线程限制，不要为了“更快”盲目替换。

### 8.3 SequentialAnimation 与 ParallelAnimation

```qml
SequentialAnimation on x {
    NumberAnimation { to: 80; duration: 150 }
    PauseAnimation { duration: 60 }
    NumberAnimation { to: 0; duration: 250 }
}
```

```qml
ParallelAnimation {
    running: moving
    NumberAnimation { target: icon; property: "x"; to: 120; duration: 300 }
    NumberAnimation { target: icon; property: "opacity"; to: 0.4; duration: 300 }
}
```

动画对象要明确 `running`、`loops` 和结束行为。重复启动同一属性上的多个动画会互相覆盖，复杂流程应使用状态和 `Transition` 统一管理。

## 9. States 与 Transitions

```qml
Rectangle {
    id: tile
    property bool selected: false

    states: State {
        name: "selected"
        when: tile.selected
        PropertyChanges { target: tile; scale: 1.05; color: "#dbeafe" }
    }

    transitions: Transition {
        NumberAnimation { properties: "scale"; duration: 160 }
        ColorAnimation { duration: 160 }
    }
}
```

状态描述目标值，过渡描述切换动画。锚点变化要使用 `AnchorChanges`，并在 Transition 中使用 `AnchorAnimation`；不要同时用普通 `NumberAnimation` 和 anchors 改写同一几何属性。

## 10. 可访问性与输入反馈

可交互项应提供 `Accessible.name`、角色、键盘焦点和明确的按下/禁用状态。屏幕阅读器依靠这些元数据建立虚拟焦点，即便设备主要使用触摸输入也不能忽略。

```qml
Rectangle {
    Accessible.name: qsTr("播放")
    Accessible.role: Accessible.Button
    Accessible.focusable: true
    Accessible.onPressAction: play()
}
```

焦点视觉反馈不应只依赖颜色，最好同时使用边框、形状或文字状态；颜色对比度和动态字体大小也应纳入设计。

## 11. 场景图与性能边界

Qt Quick 使用场景图批量提交绘制。影响性能的常见因素包括过多节点、频繁改变大面积属性、透明层叠、复杂文本和不必要的重绘。

- 合并静态背景，减少节点数量；
- 对不可见页面使用 Loader 延迟创建；
- 避免在每帧 JavaScript 中分配大量对象；
- 使用 QML Profiler、`QSG_VISUALIZE` 等工具定位瓶颈；
- 让动画只作用于必要属性，避免整个页面反复布局。

## 12. 常见问题

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| 子项跑出父项 | 未设置 anchors 或父项尺寸不稳定 | 明确几何约束，必要时启用 `clip` |
| 布局尺寸异常 | 同时使用 width 和 Layout 属性 | 让布局独占子项几何控制 |
| 点击被父项抢走 | MouseArea/Handler 抢抓策略冲突 | 收敛 accepted 范围并检查 grab 权限 |
| 键盘无响应 | 没有 active focus | `forceActiveFocus()` 并显示焦点状态 |
| ListView 滚动闪烁 | delegate 状态未在复用时重置 | 在复用回调中恢复临时状态 |
| 动画不执行 | 属性被另一绑定或动画覆盖 | 检查绑定、状态和同时运行的动画 |
| 滚动内容截断 | contentHeight 计算错误 | 绑定到内容项的 `implicitHeight` |

## 13. 自测题

1. `anchors.fill: parent` 解决了什么问题？
2. 为什么 ListView delegate 中的临时状态不能默认当作永久状态？
3. Behavior 和 Transition 的主要区别是什么？
4. `event.accepted = true` 在按键或滚轮处理中有什么作用？
5. 什么情况下应优先使用 Qt Quick Layouts 而不是 anchors？

### 参考答案

1. 它把子项四条边绑定到父项对应边，随父项尺寸变化自动调整。
2. 视图会回收和复用 delegate，离开视口后实例可能销毁或承载另一条数据。
3. Behavior 针对某个属性的每次变化提供默认动画；Transition 描述状态切换时的一组动画。
4. 表示当前处理器消费事件，阻止继续传播给其他处理器或父项。
5. 需要行列排列、间距、伸缩和最小/最大尺寸约束时。

## 14. 小结

Qt Quick 的实用路径是：用 Item 建立稳定几何，用 anchors 或 Layouts 管理空间，用 Pointer Handlers 和 Keys 处理输入，用 ListView 管理大量 delegate，用 State/Transition/Behavior 表达视觉变化。工程质量的关键在于让每个机制各司其职，避免几何、输入和动画同时修改同一属性。
