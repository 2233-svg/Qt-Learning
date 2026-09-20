# QML 基础：语法、对象与属性绑定

> QML 是 Qt 用于声明用户界面和对象关系的语言。它把对象树、属性、信号处理器和 JavaScript 表达式组合在一起；真正的优势不在于“少写几行界面代码”，而在于状态变化时依赖关系能够自动传播。本篇从能读懂一个 QML 文件开始，逐步讲到组件边界、绑定失效和 C++ 交互。

## 1. QML 文件的基本形状

一个 QML 文档通常只有一个顶层对象。顶层对象可以包含子对象、属性声明、信号、方法和处理器。

```qml
import QtQuick

Item {
    width: 320
    height: 180

    Rectangle {
        anchors.fill: parent
        color: "steelblue"
    }
}
```

`import QtQuick` 导入类型命名空间；`Item` 是不可直接绘制的基础对象；`Rectangle` 是可绘制的子对象。对象块使用大括号，属性使用 `name: value`，语句通常不要求分号。

### 1.1 类型、对象和实例

```qml
Rectangle {                 // 类型
    id: panel                // 实例的局部标识
    width: 200               // 属性赋值
    color: "#20242b"

    Text {                   // 子对象
        text: "状态"
    }
}
```

`Rectangle` 是类型，运行时创建的是一个实例。`id` 不是字符串属性，也不是对象的运行时名称，而是当前组件作用域中的编译期标识，只能在允许的作用域内引用。

## 2. 属性与值类型

### 2.1 常见值类型

QML 常用类型包括 `bool`、`int`、`real`、`double`、`string`、`url`、`color`、`date`、`var`、`list` 和枚举。Qt Quick 还大量使用 `point`、`size`、`rect`、`font`、`vector2d` 等值类型。

```qml
Item {
    property bool enabledForUser: true
    property int retryCount: 0
    property real ratio: 0.5
    property string title: qsTr("首页")
    property color accent: "#35a7ff"
    property url iconSource: "qrc:/icons/home.svg"
    property var metadata: ({ version: 1, debug: false })
}
```

对象类型属性保存对象引用；值类型属性保存值。修改值类型的一部分时，要注意 QML 的值语义：

```qml
Item {
    property rect area: Qt.rect(0, 0, 100, 60)
    Component.onCompleted: {
        area.width = 120 // 对值类型成员的修改会触发 area 的变更通知
    }
}
```

### 2.2 自定义属性

属性声明可以作为组件公开接口。对于要由实例使用者提供的输入，Qt 6 推荐使用 `required property`，这样缺失输入会在加载时暴露，而不是默默得到空值。

```qml
// StatusBadge.qml
import QtQuick

Rectangle {
    required property string label
    property color badgeColor: "#3b82f6"
    implicitWidth: textItem.implicitWidth + 24
    implicitHeight: textItem.implicitHeight + 10
    radius: 4
    color: badgeColor

    Text {
        id: textItem
        anchors.centerIn: parent
        text: label
        color: "white"
    }
}
```

```qml
StatusBadge {
    label: qsTr("在线")
    badgeColor: "#16a34a"
}
```

`implicitWidth`/`implicitHeight` 表示内容建议尺寸，布局可以在此基础上再施加约束。组件接口应优先公开语义属性，例如 `label`、`busy`、`errorText`，不要让外部依赖内部 `id`。

## 3. id、作用域和对象树

### 3.1 id 的生命周期

`id` 在组件实例创建后可用于引用对象，但它不是可绑定的属性，不能写成 `id: someExpression`。同一组件作用域内的 `id` 必须唯一，并且不能在运行时修改。

```qml
Item {
    id: root
    property int spacing: 8

    Rectangle {
        id: box
        width: root.width - root.spacing * 2
    }
}
```

### 3.2 组件作用域

组件内部的 `id` 不应被另一个 QML 文件直接访问。跨组件通信应通过属性、信号、方法或注入的模型完成：

```qml
// SearchBox.qml
Item {
    signal submitted(string query)
    property alias text: input.text

    TextInput {
        id: input
        onAccepted: submitted(text)
    }
}
```

```qml
SearchBox {
    onSubmitted: function (query) {
        console.log("搜索", query)
    }
}
```

这样，父对象不需要知道 `SearchBox` 内部使用的是 `TextInput` 还是其他实现。

### 3.3 parent 与可视父项

QML 对象通常有对象树父对象；Qt Quick `Item` 还有用于绘制和坐标转换的可视父项。声明式嵌套通常会同时建立两者，但动态创建或把对象交给 `Loader` 时，必须确认 `parent`、`visual parent` 和所有权是否符合预期。

## 4. 属性绑定：QML 的核心机制

### 4.1 从赋值到绑定

下面两种写法语义不同：

```qml
Item {
    width: parent.width / 2 // 绑定：parent.width 变化时自动重算
}
```

```qml
Item {
    Component.onCompleted: {
        width = parent.width / 2 // 一次性赋值，之后 parent.width 变化不会同步
    }
}
```

绑定是一个表达式及其依赖集合。QML 引擎追踪表达式读取过的属性，当依赖发出变更通知时重新求值。

### 4.2 绑定表达式的组成

绑定可以引用当前对象属性、同作用域对象、父对象、函数返回值和条件表达式：

```qml
Rectangle {
    property bool compact: width < 500
    height: compact ? 44 : 64
    color: enabled ? "#2563eb" : "#9ca3af"
    opacity: visible ? 1.0 : 0.0
}
```

表达式应保持纯粹、快速且可重复。不要在绑定中修改其他属性、执行 I/O 或调用有副作用的函数，否则依赖图难以理解，并可能造成循环更新。

### 4.3 绑定被覆盖

给一个已有绑定的属性做普通赋值，会移除该属性原来的绑定：

```qml
Rectangle {
    width: parent.width / 2

    function resetWidth() {
        width = 100 // 绑定被永久替换为常量赋值
    }
}
```

如果确实需要在 JavaScript 中重新建立绑定，使用 `Qt.binding()`，但应把这种命令式操作限制在明确的状态切换处：

```qml
width = Qt.binding(function () { return parent.width / 2 })
```

更好的设计通常是绑定到状态属性，由状态属性决定表达式结果，而不是反复拆装绑定。

### 4.4 循环绑定

```qml
Item {
    width: height
    height: width // 循环依赖，结果不可预测
}
```

循环绑定会导致警告、反复求值或不稳定结果。将共享状态提升到第三个属性，或只保留单向依赖：

```qml
Item {
    property real side: 80
    width: side
    height: side
}
```

## 5. property alias 与接口转发

`property alias` 将外部属性直接转发到已有对象的属性或信号，适合做轻量封装：

```qml
Item {
    property alias text: editor.text
    property alias placeholderText: editor.placeholderText

    TextInput {
        id: editor
        anchors.fill: parent
    }
}
```

alias 不是复制值，读写都会作用于目标属性，也会保留目标属性的通知语义。目标对象必须在 alias 可解析的作用域内；不要让 alias 穿透太多内部层级，否则重构成本会很高。

## 6. 信号与处理器

### 6.1 声明信号

```qml
Item {
    signal saved(string fileName, int bytes)

    function saveDone(name, size) {
        saved(name, size)
    }
}
```

信号只描述“发生了什么”，不应承担复杂业务流程。信号参数应使用明确类型，便于 QML 编译器和工具检查。

### 6.2 on<Signal> 处理器

```qml
Button {
    text: qsTr("保存")
    onClicked: controller.save()
}
```

处理器在信号到达时执行。对于 QML 类型自身的信号，这是最简洁的写法。不要在处理器中堆积大量业务代码，可以调用控制器方法或发出领域信号。

### 6.3 Connections

当发送者不在当前对象范围、需要多个监听者或需要动态切换目标时，使用 `Connections`：

```qml
Connections {
    target: controller
    enabled: root.visible

    function onErrorOccurred(message) {
        errorLabel.text = message
    }
}
```

Qt 6 推荐使用 `function onSignal(...) {}` 形式。`Connections` 的 `target` 可以为 `null`，此时连接暂时不生效；`enabled` 可控制是否接收信号。`ignoreUnknownSignals` 只应在确实需要兼容多个目标类型时使用，否则会掩盖拼写错误。

## 7. JavaScript 方法与状态

### 7.1 方法

```qml
Item {
    function clamp(value, minimum, maximum) {
        return Math.max(minimum, Math.min(maximum, value))
    }

    function updateProgress(done, total) {
        progress = total > 0 ? clamp(done / total, 0, 1) : 0
    }

    property real progress: 0
}
```

方法可以访问组件作用域，但应避免隐式依赖太多外部对象。可复用的业务算法更适合放在 C++ 或独立 JavaScript 模块中。

### 7.2 状态与 State

简单界面可以用布尔属性控制；互斥的复杂外观更适合 `states` 和 `State`：

```qml
Rectangle {
    id: card
    width: 240
    height: 80
    color: "white"

    states: [
        State {
            name: "selected"
            when: card.activeFocus
            PropertyChanges { target: card; color: "#dbeafe" }
        }
    ]
}
```

状态描述“处于什么状态”，动画描述“如何过渡”。把所有变化都写成嵌套 `if` 会让依赖关系和回退逻辑变得难以维护。

## 8. Component、Loader 与动态对象

### 8.1 内联 Component

`Component` 封装一个待实例化的对象。它本身不是 `Item`，不能直接显示或进行锚定：

```qml
Item {
    Component {
        id: redSquare
        Rectangle { width: 40; height: 40; color: "red" }
    }

    Loader {
        sourceComponent: redSquare
        anchors.centerIn: parent
    }
}
```

组件状态包括 `Null`、`Loading`、`Ready` 和 `Error`。动态创建前检查 `status` 和 `errorString()`，不要在错误组件上直接调用 `createObject()`。

### 8.2 Loader 的生命周期

`Loader` 可以按需加载文件或 `sourceComponent`，通过 `active` 控制是否创建对象。停用 Loader 会销毁其加载对象；不要把加载对象的引用长期保存而不处理销毁信号。

```qml
Loader {
    id: pageLoader
    active: root.pageVisible
    source: "SettingsPage.qml"

    onStatusChanged: {
        if (status === Loader.Error)
            console.error("加载失败", source)
    }
}
```

## 9. Component.onCompleted 与初始化顺序

```qml
Component.onCompleted: {
    console.log("对象已完成", objectName)
}
```

`Component.onCompleted` 在组件实例初始化完成后触发。嵌套对象处理器的执行顺序不应作为业务契约；如果顺序重要，应显式调用初始化方法或由一个控制器协调。

对应的 `Component.onDestruction` 可撤销初始化期间注册的外部资源，但不要把它当作精确的生命周期事务边界。

## 10. C++ 与 QML 的边界

### 10.1 C++ 暴露对象的基本形态

```cpp
class AppController : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool busy READ busy NOTIFY busyChanged)
public:
    bool busy() const { return m_busy; }

public slots:
    void refresh();

signals:
    void busyChanged();
    void errorOccurred(const QString &message);

private:
    bool m_busy = false;
};
```

属性必须有正确的 `NOTIFY` 信号，QML 才能可靠地重新计算依赖它的绑定。C++ 在设置值时应只在值真的变化时发通知，避免无意义的绑定重算。

### 10.2 注入上下文对象

```cpp
QQmlApplicationEngine engine;
AppController controller;
engine.rootContext()->setContextProperty("controller", &controller);
engine.loadFromModule("MyApp", "Main");
```

上下文属性简单直接，但依赖是隐式的，组件脱离该上下文后难以复用。大型应用优先注册类型或通过根组件的 `required property` 显式传入依赖：

```qml
ApplicationWindow {
    required property AppController controller
}
```

### 10.3 QML 调用 C++ 与 C++ 调用 QML

QML 可调用公开槽、`Q_INVOKABLE` 方法和属性；C++ 可通过 `QObject::findChild()` 或 `QQmlComponent::create()` 获取对象，但不应依赖脆弱的对象名层级。跨边界传输的数据应使用可被元对象系统识别的类型，并明确所有权。

## 11. 绑定性能与可维护性

绑定不是免费操作。以下做法能减少不必要的工作：

- 让绑定表达式短小，复杂计算放入 C++ 或缓存属性；
- 避免在高频动画属性上创建大量对象和字符串；
- 为 C++ 属性提供准确的通知信号；
- 使用 `required property` 和类型注解帮助 qmllint 发现错误；
- 不在绑定中读写全局可变状态；
- 把页面拆成有清晰输入输出的组件。

可以用 `qmlcachegen`/Qt Quick Compiler 和 `qmllint` 提前发现类型、绑定和未使用属性问题。工具检查不能替代运行时行为测试，但能显著缩短反馈时间。

## 12. 常见错误诊断

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 绑定只更新一次 | 在初始化函数中使用了普通赋值 | 改为声明式绑定或显式重新建立绑定 |
| 属性变了界面不变 | C++ 属性缺少 `NOTIFY` 或未发信号 | 添加准确的通知信号 |
| `id` 找不到 | 超出组件作用域或拼写错误 | 通过属性、信号或方法建立接口 |
| `Connections` 报未知信号 | target 类型不匹配、信号名错误 | 检查类型注册和 `onSignal` 拼写 |
| required property 错误 | 创建组件时未提供必需输入 | 在实例处提供属性，或给出合理默认值 |
| 动态对象泄漏/提前销毁 | 未理解 Loader 和 JS 所有权 | 明确 parent、Loader 生命周期和销毁回调 |
| 绑定循环警告 | 两个属性互相依赖 | 引入单一源状态，改为单向绑定 |

## 13. 自测题

1. `width: parent.width / 2` 与在 `Component.onCompleted` 中执行同样赋值有何区别？
2. 为什么公共组件不应让外部直接访问内部 `id`？
3. `property alias` 是复制值还是转发属性？
4. 什么时候使用 `Connections`，而不是 `on<Signal>`？
5. C++ 属性为什么通常需要 `NOTIFY` 信号？

### 参考答案

1. 前者是持续绑定，依赖变化时自动重算；后者是一次性赋值。
2. `id` 属于组件内部作用域，直接依赖会破坏封装并阻碍重构。
3. 是转发，读写作用于目标属性，不是复制一份独立值。
4. 发送者在外部、需要多个连接或目标动态切换时使用。
5. QML 通过通知信号知道依赖变化，从而重新求值绑定。

## 14. 小结

QML 的学习顺序可以概括为：先读懂对象树和属性，再掌握绑定和信号，最后用组件接口和 C++ 边界管理复杂度。最重要的工程判断是区分“声明状态”与“执行动作”：状态适合属性绑定，动作适合方法和信号；一旦把两者混在一起，界面就会出现难以解释的更新顺序和生命周期问题。
