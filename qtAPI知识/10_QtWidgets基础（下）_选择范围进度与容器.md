# Qt Widgets 基础（下）：选择、范围、进度与容器

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Widgets  
> 核心类型：`QComboBox`、`QSpinBox`、`QDoubleSpinBox`、`QDateTimeEdit`、`QSlider`、`QProgressBar`、`QGroupBox`、`QTabWidget`、`QStackedWidget`、`QScrollArea`、`QSplitter`

## 1. 选择控件的原则

| 任务 | 控件 |
|---|---|
| 少量固定选项，下拉显示 | `QComboBox` |
| 有边界的整数输入 | `QSpinBox` |
| 有边界的小数输入 | `QDoubleSpinBox` |
| 日期、时间或日期时间 | `QDateEdit` / `QTimeEdit` / `QDateTimeEdit` |
| 快速调整连续范围 | `QSlider` / `QDial` |
| 展示任务进度 | `QProgressBar` |
| 带标题的视觉分组 | `QGroupBox` |
| 用户主动切换并列页面 | `QTabWidget` |
| 程序控制工作流页面 | `QStackedWidget` |
| 内容大于视口 | `QScrollArea` |
| 用户拖动分配两块空间 | `QSplitter` |

## 2. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. 最小可用代码：参数面板

```cpp
#include <QApplication>
#include <QComboBox>
#include <QFormLayout>
#include <QProgressBar>
#include <QSlider>
#include <QSpinBox>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    auto *layout = new QFormLayout(&window);

    auto *mode = new QComboBox;
    mode->addItem("快速", "fast");
    mode->addItem("均衡", "balanced");
    mode->addItem("精细", "quality");

    auto *threads = new QSpinBox;
    threads->setRange(1, 32);
    threads->setValue(4);

    auto *slider = new QSlider(Qt::Horizontal);
    slider->setRange(0, 100);
    slider->setValue(40);

    auto *progress = new QProgressBar;
    progress->setRange(0, 100);
    QObject::connect(slider, &QSlider::valueChanged,
                     progress, &QProgressBar::setValue);

    layout->addRow("模式：", mode);
    layout->addRow("线程数：", threads);
    layout->addRow("进度：", slider);
    layout->addRow("", progress);

    window.resize(380, 220);
    window.show();
    return app.exec();
}
```

ComboBox 的显示文本用于界面，itemData 中的稳定键用于业务，避免把翻译后的文字当数据库值。

## 4. QComboBox：下拉选择

```cpp
combo->addItem(tr("管理员"), "admin");
combo->addItem(tr("普通用户"), "user");

QString roleKey = combo->currentData().toString();
```

每项可保存多个 role 数据：

```cpp
combo->setItemData(index, description, Qt::ToolTipRole);
combo->setItemData(index, id, Qt::UserRole);
```

### 4.1 不要用显示文字做业务键

```cpp
if (combo->currentText() == "管理员") // 翻译后失效
```

应使用稳定 ID：

```cpp
if (combo->currentData().toString() == "admin")
```

### 4.2 三类信号

| 信号 | 用户操作 | 程序 setCurrentIndex | 特点 |
|---|---:|---:|---|
| `currentIndexChanged` | 是 | 是 | 当前索引真实变化 |
| `currentTextChanged` | 是 | 是 | 当前文本真实变化 |
| `activated` / `textActivated` | 是 | 否 | 用户选中，即使选回同项也可能发出 |
| `highlighted` | 是 | 否 | 弹出列表中只是高亮浏览 |

数据绑定使用 currentChanged；只响应用户确认选择使用 activated。

### 4.3 无选择占位

```cpp
combo->setPlaceholderText(tr("请选择"));
combo->setCurrentIndex(-1);
```

如果在添加项目之前设置 placeholder，它会直接显示；添加后再设置时需显式把索引设为 -1。Editable ComboBox 应对内部 LineEdit 设置 placeholder。

### 4.4 Editable ComboBox

```cpp
combo->setEditable(true);
combo->setInsertPolicy(QComboBox::NoInsert);
combo->setDuplicatesEnabled(false);
```

输入策略包括插到顶部、底部、当前项前后等。是否把自由输入写回候选列表是业务决定，不要依赖默认 `InsertAtBottom`。

可对内部输入设置 Validator 和 Completer。改回不可编辑会移除 Completer/Validator 关联，动态切换后需重新确认配置。

### 4.5 Model/View 基础

ComboBox 内部本来就使用模型：

```cpp
combo->setModel(model);
combo->setModelColumn(1);
```

大数据或多个视图共享选项时，应使用模型而非逐项复制。完整 Model/View 在后续专章讲解。

## 5. QSpinBox：整数输入

```cpp
spin->setRange(1, 65535);
spin->setValue(8080);
spin->setSingleStep(1);
spin->setPrefix(tr("端口 "));
```

数值始终被约束在 minimum 和 maximum 之间。不要用普通 QLineEdit 再手动解析有明确数值范围的字段。

### 5.1 特殊最小值文本

```cpp
spin->setRange(0, 120);
spin->setSpecialValueText(tr("无限制"));
spin->setSuffix(tr(" 秒"));
```

当值等于 minimum 时显示特殊文本，prefix/suffix 不显示。业务层仍取得数值 0，需要明确定义 0 的语义。

### 5.2 wrapping 与 keyboardTracking

```cpp
spin->setWrapping(true);
spin->setKeyboardTracking(false);
```

- wrapping：最大值继续加会回到最小值；
- keyboardTracking 默认 true，用户输入每个字符都可能产生 valueChanged；
- 关闭后通常在 Enter、失焦或完成编辑时才提交最终值。

昂贵计算绑定 SpinBox 时可关闭 keyboardTracking，或做防抖。

### 5.3 自定义文本映射

继承 QSpinBox 可重写：

```cpp
QString PrioritySpinBox::textFromValue(int value) const
{
    return priorityName(value);
}

int PrioritySpinBox::valueFromText(const QString &text) const
{
    return priorityValue(text);
}
```

同时应实现合适的 `validate()`，确保解析、显示和可编辑中间状态一致。

## 6. QDoubleSpinBox：小数输入

```cpp
spin->setRange(0.0, 100.0);
spin->setDecimals(2);
spin->setSingleStep(0.25);
spin->setSuffix(" %");
```

浮点显示会舍入到 decimals 指定位数。程序设置的值可能在显示和读取时受舍入影响，不要用二进制浮点精确表示货币。

自适应步长：

```cpp
spin->setStepType(QAbstractSpinBox::AdaptiveDecimalStepType);
```

步长会随当前数量级变化，适合跨多个数量级调整。

## 7. 日期与时间编辑

```cpp
auto *date = new QDateEdit;
date->setCalendarPopup(true);
date->setDisplayFormat("yyyy-MM-dd");
date->setDateRange(QDate::currentDate(),
                   QDate::currentDate().addYears(2));
```

日期格式用于显示，不应替代结构化存储。保存时使用 QDate/QDateTime 或明确 ISO 格式。

### 7.1 QDateTime 与时区

```cpp
QDateTime value = edit->dateTime();
```

跨地区业务必须明确时区或 time zone。仅保存屏幕字符串会丢失时区、历法和歧义信息。对绝对时间通常保存 UTC 瞬间和需要的时区标识。

### 7.2 Section

DateTimeEdit 将年、月、日、时、分等视为 section，可查询 `currentSection()` 或选择指定 section。键盘上下键只调整当前 section。

## 8. QSlider 与 QDial

二者基于 `QAbstractSlider`，共享：

```cpp
slider->setRange(0, 100);
slider->setSingleStep(1);
slider->setPageStep(10);
slider->setValue(50);
slider->setTracking(true);
```

### 8.1 valueChanged 与 sliderMoved

- `valueChanged(int)`：值变化，包括程序设置；
- `sliderMoved(int)`：用户拖动手柄时；
- `sliderPressed()` / `sliderReleased()`：拖动会话边界。

关闭 tracking 后，拖动中 position 改变，但 value 通常到释放时才提交：

```cpp
slider->setTracking(false);
```

昂贵预览可在 sliderMoved 展示轻量反馈，在 sliderReleased 执行最终计算。

### 8.2 范围映射

Slider 只保存 int。映射到浮点业务值：

```cpp
double normalized = (slider->value() - slider->minimum()) /
                    double(slider->maximum() - slider->minimum());
double actual = minValue + normalized * (maxValue - minValue);
```

必须处理最大值等于最小值，且反向映射时正确取整和夹紧。

### 8.3 invertedAppearance 与 invertedControls

- invertedAppearance：颠倒视觉高低方向；
- invertedControls：颠倒按键和滚轮操作方向。

它们不是一回事。还要考虑右到左布局和平台习惯。

## 9. QProgressBar：展示进度

确定进度：

```cpp
progress->setRange(0, total);
progress->setValue(done);
progress->setFormat("%v / %m (%p%)");
```

未知总量：

```cpp
progress->setRange(0, 0); // busy indicator
```

未知进度不是 0%。不要显示停在 0 的确定进度条让用户误以为没有工作。

### 9.1 线程更新

工作线程不能直接操作 ProgressBar。发出 `progressChanged(int)`，让主线程的排队槽调用 setValue。

进度更新不宜每处理一个字节都发信号。按时间或百分比节流，避免事件队列被高频通知淹没。

### 9.2 进度的可信度

进度条应单调、可解释：

- 工作总量变化时重新定义范围；
- 多阶段任务按权重合成；
- 无法估算时使用 busy；
- 取消后显示“正在取消”直到生产者真正停止；
- 完成、失败、取消采用不同最终状态。

## 10. QGroupBox：视觉和启用分组

```cpp
auto *group = new QGroupBox(tr("网络"));
auto *layout = new QFormLayout(group);
layout->addRow(tr("主机："), hostEdit);
layout->addRow(tr("端口："), portSpin);
```

可设为 checkable：

```cpp
group->setCheckable(true);
group->setChecked(false);
```

未选中时其子控件通常被禁用。它表达“整组功能是否启用”，不要用作任意折叠容器；视觉折叠需要专门交互和尺寸管理。

QGroupBox 是可见容器，QButtonGroup 是不可见的按钮逻辑分组，二者职责不同。

## 11. QTabWidget：用户切换页面

```cpp
int index = tabs->addTab(generalPage, tr("常规"));
tabs->addTab(advancedPage, tr("高级"));
tabs->setTabToolTip(index, tr("常用设置"));
tabs->setMovable(true);
tabs->setTabsClosable(true);
```

### 11.1 关闭标签页

```cpp
connect(tabs, &QTabWidget::tabCloseRequested,
        this, [tabs](int index) {
    QWidget *page = tabs->widget(index);
    tabs->removeTab(index);
    page->deleteLater();
});
```

`removeTab()` 只移除页面，不删除它。若不再使用，调用者负责删除；若要移动到其他容器，则重新设置或由新容器接管。

页面索引会随插入、关闭和移动变化，长期业务身份不要只保存 index。可通过页面对象或稳定 ID 查找。

### 11.2 不要滥用标签页

标签过多会难以扫描，标题被截断。大量动态文档可使用文档列表、侧栏或更专业的多文档导航。

## 12. QStackedWidget：程序控制页面

```cpp
stack->addWidget(welcomePage);
stack->addWidget(editorPage);
stack->setCurrentWidget(editorPage);
```

它没有内置标签导航，适合：

- 向导式步骤；
- 登录前后页面；
- 侧栏导航对应内容；
- 状态机驱动视图。

`addWidget()` 接管页面所有权。`removeWidget()` 通常只移除，不删除；根据页面是否复用决定其后处理。

Qt 6.9 起有 `widgetAdded(int)` 信号，可在动态页面体系中观察添加。

## 13. QToolBox

QToolBox 以竖直按钮切换页面，适合少量设置类别：

```cpp
toolBox->addItem(networkPage, tr("网络"));
toolBox->addItem(displayPage, tr("显示"));
```

它一次显示一页。不要把它与可同时展开多个区域的 Accordion 混淆。

## 14. QScrollArea：一个大内容控件

```cpp
auto *content = new QWidget;
auto *layout = new QVBoxLayout(content);
// 向 layout 添加内容

auto *scroll = new QScrollArea;
scroll->setWidget(content);
scroll->setWidgetResizable(true);
```

ScrollArea 主要管理一个 content widget，不是直接向 viewport 布局添加许多控件。

### 14.1 widgetResizable

- false：内容保持自己的尺寸，超出视口时滚动；
- true：ScrollArea 尝试调整内容以利用空间，同时尊重 size hint 和最小尺寸。

表单一般设 true；查看原始像素尺寸图片时常设 false。

### 14.2 所有权和顺序

`setWidget()` 接管 content。若 content 的布局要正确参与尺寸计算，应在 `setWidget()` 前设置好布局和尺寸约束。

```cpp
QWidget *content = scroll->takeWidget();
```

`takeWidget()` 移除并把所有权交还调用方。

### 14.3 ensureVisible

```cpp
scroll->ensureWidgetVisible(invalidField, 20, 20);
invalidField->setFocus();
```

长表单验证失败时可自动滚动到错误字段，但避免每次输入都强行改变用户视口。

## 15. QSplitter：用户控制空间分配

```cpp
auto *splitter = new QSplitter(Qt::Horizontal);
splitter->addWidget(navigation);
splitter->addWidget(editor);
splitter->setStretchFactor(0, 0);
splitter->setStretchFactor(1, 1);
```

Splitter 不是普通 Layout，它有可拖动 handle，并接管加入 Widget 的所有权。

### 15.1 初始尺寸和 stretch

```cpp
splitter->setSizes({240, 760});
```

`setStretchFactor()` 的结果还与初始 sizeHint/size 相乘，并非简单百分比。需要明确初始比例时 `setSizes()` 更直观。

### 15.2 防止折叠到 0

默认子控件可被拖到尺寸 0，即使有非零 minimumSizeHint：

```cpp
splitter->setChildrenCollapsible(false);
// 或 splitter->setCollapsible(index, false);
```

### 15.3 保存恢复

```cpp
settings.setValue("editor/splitter", splitter->saveState());
splitter->restoreState(
    settings.value("editor/splitter").toByteArray());
```

恢复失败时使用合理默认尺寸。保存数据应在界面结构兼容时使用。

## 16. 容器页面的懒加载

昂贵页面可在首次显示时创建：

```cpp
connect(tabs, &QTabWidget::currentChanged,
        this, [this](int index) {
    if (index == previewIndex_ && !previewLoaded_)
        loadPreviewPage();
});
```

需要区分：

- 创建 UI 骨架；
- 启动异步数据请求；
- 页面离开后是否取消；
- 请求回来时页面是否仍存在；
- 加载失败如何重试。

不要在 currentChanged 槽里同步执行耗时 I/O。

## 17. 动态页面与索引稳定性

以下操作都会改变索引：

- insert；
- remove；
- 用户移动标签；
- 条件页面加入或消失。

错误：长期保存 `settingsPageIndex = 3` 作为业务身份。

更稳妥：

```cpp
QWidget *page = pagesById.value("settings");
stack->setCurrentWidget(page);
```

索引只作为当前容器的短期定位值。

## 18. 信号回路与批量刷新

程序加载配置时会触发 valueChanged/currentIndexChanged：

```cpp
QSignalBlocker a(combo);
QSignalBlocker b(spin);
QSignalBlocker c(slider);

combo->setCurrentIndex(index);
spin->setValue(value);
slider->setValue(level);
```

也可让槽先比较模型新旧值。`QSignalBlocker` 会阻止所有信号，因此不要在需要其他观察者同步的路径滥用。

## 19. 输入控件与模型边界

推荐流程：

```text
模型值 → 程序设置控件
用户编辑 → 控件信号 → 表单缓冲/命令
点击应用 → 统一验证 → 写入模型
模型发 changed → 刷新其他视图
```

大型表单每个键击直接写持久数据库，会导致性能、撤销和错误恢复困难。根据业务选择即时应用、失焦提交或显式 Apply。

## 20. 常见错误

### 20.1 用 currentText 保存枚举

翻译和显示文字修改会破坏数据。把稳定 ID 存在 UserRole。

### 20.2 把 activated 当所有变化

程序 setCurrentIndex 不触发 activated。模型同步使用 currentIndexChanged。

### 20.3 SpinBox 范围使用默认值

默认范围未必符合业务，设置 value 前先设置 range，避免值被意外夹紧。

### 20.4 未知任务显示 0%

使用 `setRange(0, 0)` 表示繁忙状态，能估算后再切换确定范围。

### 20.5 removeTab 后以为页面已删除

remove 只解除页面与标签关系。明确删除、复用或交给新容器。

### 20.6 ScrollArea 内容没有布局或尺寸建议

内容尺寸无法正确增长，滚动条行为异常。为 content 设置布局和合理最小尺寸策略。

### 20.7 Splitter 页面被拖没

默认允许折叠到 0。关键页面设置不可折叠。

### 20.8 直接从工作线程 setValue

所有 Widget 只在 GUI 线程操作。使用信号槽或主线程上下文 continuation。

## 21. API 速查表

| API / 信号 | 用途 | 注意点 |
|---|---|---|
| `QComboBox::addItem(text,data)` | 显示文本关联业务值 | data 用稳定 ID |
| `currentIndexChanged` | 任意来源的真实变化 | 程序设置也触发 |
| `activated` | 用户选择 | 同项再次选择也可触发 |
| `QSpinBox::setRange()` | 限制数值 | 先设范围再设值 |
| `setKeyboardTracking(false)` | 延迟提交键入值 | 适合昂贵响应 |
| `specialValueText` | 最小值特殊语义 | 明确定义业务值 |
| `QSlider::setTracking()` | 拖动时是否实时提交 | position 与 value 可不同 |
| `QProgressBar::setRange(0,0)` | 未知进度 | busy 状态 |
| `QTabWidget::removeTab()` | 移除标签页 | 不删除页面 |
| `QStackedWidget::setCurrentWidget()` | 按对象切换页面 | 比长期索引稳健 |
| `QScrollArea::setWidget()` | 设置内容控件 | 接管所有权 |
| `setWidgetResizable(true)` | 内容适应视口 | 仍尊重尺寸约束 |
| `QSplitter::setSizes()` | 设置初始分配 | 单位是像素权重式尺寸 |
| `setChildrenCollapsible(false)` | 禁止折叠到 0 | 关键面板使用 |
| `QSplitter::saveState()` | 保存用户分割位置 | QSettings 持久化 |

## 22. 自测题

### 题 1：如何保存 ComboBox 业务值

<details><summary>答案</summary>

把稳定 ID 放进 itemData/UserRole，用 currentData() 读取；不要依赖可翻译的 currentText。
</details>

### 题 2：activated 与 currentIndexChanged 的区别

<details><summary>答案</summary>

activated 只代表用户选中，程序设置不触发；currentIndexChanged 在当前索引因用户或程序发生变化时都会触发。
</details>

### 题 3：ProgressBar 如何表示未知总量

<details><summary>答案</summary>

调用 `setRange(0, 0)` 进入繁忙指示状态，而不是伪造 0% 或不断循环百分比。
</details>

### 题 4：removeTab 后页面归谁

<details><summary>答案</summary>

页面没有被删除。调用方应决定重新加入、转移 parent 或 deleteLater，避免泄漏和悬空引用。
</details>

### 题 5：ScrollArea 的 widgetResizable 有何意义

<details><summary>答案</summary>

true 时内容会在尺寸约束允许范围内适应视口；false 时保持自身尺寸，超出视口后用滚动条查看。
</details>

### 题 6：为什么 Splitter 子项可能缩到 0

<details><summary>答案</summary>

默认 childrenCollapsible 为 true，即使最小尺寸建议非零也可折叠。关键子项需要显式禁止折叠。
</details>

## 23. 本篇总结

1. ComboBox 显示文本和业务 ID 分离，并按“任意变化”或“用户激活”选择信号。
2. SpinBox 和 DateTimeEdit 把范围、解析、步进和格式封装成结构化输入。
3. Slider 适合快速范围调整，昂贵操作应考虑关闭 tracking 或做防抖。
4. 确定进度设置真实范围，未知进度使用 busy 状态。
5. TabWidget 面向用户并列页面，StackedWidget 面向程序控制工作流。
6. ScrollArea 管理一个内容 Widget，Splitter 让用户调整多个 Widget 的空间。
7. remove 类 API 通常不等于 delete，必须核对所有权。

下一章将专门讲布局系统，从 size hint 和 size policy 的协商过程深入到 Box、Grid、Form、Stacked、自定义布局以及动态界面更新。
