# QSizeGrip

> Qt 6.11.1 · Qt Widgets · 来自 `QSizeGrip`

## 1. 先建立直觉

`QSizeGrip` 是窗口角落里的“拖拽改尺寸抓手”。用户按住它拖动时，会调整所属顶层窗口的大小。它常见于状态栏右下角，也可以放进自定义对话框、浮动面板或没有原生边框的工具窗口。

它不是普通的布局占位符，也不是 splitter。`QSplitter` 调整的是窗口内部多个区域的比例；`QSizeGrip` 调整的是整个顶层窗口大小。这个区别决定了它应该放在窗口边缘或角落，而不是放在内容中间充当分隔器。

## 2. 类说明

`QSizeGrip` 继承自 `QWidget`。它会向上查找合适的顶层窗口，并在鼠标拖动时请求该窗口 resize。Qt 会按照当前平台样式绘制抓手外观，所以它通常能和系统主题保持一致。

`QStatusBar` 可以自动管理 size grip；普通窗口中则可以手动创建一个 `QSizeGrip`，并通过布局把它放到右下角或左下角。需要注意 RTL 布局和平台窗口装饰差异：某些系统已经提供原生 resize corner，重复放置可能显得多余。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSizeGrip(QWidget *)` | 创建尺寸抓手。父对象通常是状态栏、对话框底部区域或自定义窗口容器。 |
| `setVisible(bool)` | 显示或隐藏抓手。固定大小窗口、最大化窗口常会隐藏它。 |
| `sizeHint()` | 返回平台风格建议的抓手尺寸。布局中一般尊重它。 |
| `hideEvent()` | 抓手隐藏时触发；子类可同步状态。 |
| `showEvent()` | 抓手显示时触发；子类可刷新布局或样式。 |
| `mousePressEvent()` | 开始拖拽调整窗口大小。通常不需要手动调用。 |
| `mouseMoveEvent()` | 拖动过程中计算并请求新的窗口尺寸。 |
| `mouseReleaseEvent()` | 结束拖动。适合子类做状态清理。 |
| `moveEvent()` | 抓手自身位置变化时触发，常由布局或窗口缩放引起。 |
| `paintEvent()` | 按当前 `QStyle` 绘制抓手。自定义外观时可重写。 |

## 4. 典型用法

状态栏场景中优先让 `QStatusBar` 处理：

```cpp
statusBar()->setSizeGripEnabled(true);
```

如果是一个自定义无边框对话框，可以手动把抓手放在底部布局末端：

```cpp
auto *bottom = new QHBoxLayout;
bottom->addStretch();
bottom->addWidget(new QSizeGrip(this));
mainLayout->addLayout(bottom);
```

这样写的关键点是 `addStretch()`：它把抓手推到角落，让用户形成“从窗口角拖动”的预期。

## 5. 使用场景

`QSizeGrip` 适合可调整大小的工具窗口、属性面板、浮动日志窗口、无边框对话框、嵌入式风格应用中的自定义窗口壳，以及需要明确给用户一个 resize affordance 的界面。

如果窗口已经有清晰的系统边框和可拖角，额外添加 `QSizeGrip` 不一定增加可用性。它最有价值的地方，是在自绘窗口、状态栏或视觉边界不明显的窗口里告诉用户“这里可以拖”。

## 6. 常见坑与经验

固定大小窗口不应该显示 `QSizeGrip`。如果 `minimumSize` 和 `maximumSize` 相同，抓手虽然可能可见，但拖动不会产生有效变化，用户会觉得控件坏了。

最大化窗口、全屏窗口中通常应隐藏它。用户此时预期是先还原窗口，再调整大小。

在无边框窗口里，`QSizeGrip` 可以解决角落缩放，但不能自动提供移动窗口、边缘缩放、系统菜单等完整窗口管理体验。它只是 resize corner，不是完整标题栏框架。
