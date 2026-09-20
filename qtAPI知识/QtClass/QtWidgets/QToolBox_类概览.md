# Qt QToolBox 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QToolBox>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QFrame -> QToolBox`  
> 关键词：页面容器、垂直标题、当前页、`QStyleOptionToolBox`

## 1. 先说结论：QToolBox 是一次只展示一页的垂直页面容器

`QToolBox` 将多个 `QWidget` 页面放在一起，并在顶部到下方垂直排列页面标题。用户点击一条标题后，对应页面显示为当前页。

```text
QToolBox
┌────────────────────────────┐
│ [图标] 常规                │ <- 标题 0
│  常规页面内容              │ <- 当前页面
├────────────────────────────┤
│ [图标] 网络                │ <- 标题 1
├────────────────────────────┤
│ [图标] 高级                │ <- 标题 2
└────────────────────────────┘
```

它适合少量、主题明确的设置页，例如“常规 / 网络 / 高级”。它不适合几十个页面的复杂导航，也不适合同一时间要看到全部分组内容的表单。

不要把它与 `QToolBar` 混淆：

| 类 | 它容纳什么 | 典型用途 |
| --- | --- | --- |
| `QToolBar` | `QAction` 和少量快捷控件。 | 高优先级命令。 |
| `QToolBox` | 多个完整 `QWidget` 页面。 | 侧栏设置、属性分组。 |
| `QTabWidget` | 多个页面和横向/纵向 tab。 | 文档或功能页切换。 |

## 2. 最小可用示例

```cpp
#include <QFormLayout>
#include <QLabel>
#include <QLineEdit>
#include <QToolBox>
#include <QVBoxLayout>

auto *toolBox = new QToolBox;

auto *generalPage = new QWidget;
auto *generalForm = new QFormLayout(generalPage);
generalForm->addRow("名称：", new QLineEdit);

auto *networkPage = new QWidget;
auto *networkLayout = new QVBoxLayout(networkPage);
networkLayout->addWidget(new QLabel("代理与连接设置"));
networkLayout->addStretch();

const int generalIndex = toolBox->addItem(generalPage, "常规");
const int networkIndex = toolBox->addItem(networkPage, "网络");
toolBox->setCurrentIndex(generalIndex);
```

加入一个页面后，`QToolBox` 管理它的显示、隐藏和父子关系。页面内部仍要由自己的布局负责排版。

## 3. 页面、标题与 index 的关系

每个 item 都由两部分组成：

```text
index
  ├─ 标题文字 text
  ├─ 可选图标 icon
  ├─ 可选工具提示 toolTip
  ├─ enabled 状态
  └─ QWidget 页面
```

`count()` 是页面数量，空工具箱为 `0`。`currentIndex()` 是当前页索引，空工具箱为 `-1`；此时 `currentWidget()` 返回 `nullptr`。

```cpp
connect(toolBox, &QToolBox::currentChanged, this,
        [toolBox](int index) {
            if (index < 0) {
                return;
            }
            qDebug() << "当前标题：" << toolBox->itemText(index);
        });
```

不能把 index 长期当作页面身份。插入或删除 item 后，后续页面的 index 会变化；业务代码更稳妥的做法是保存页面指针，必要时用 `indexOf(page)` 获取当前 index。

## 4. 添加与插入页面

### 4.1 `addItem()`

`addItem()` 总是在底部追加页面，并返回新页面的 index：

```cpp
int index = toolBox->addItem(page, QIcon(":/network.svg"), "网络");
```

无图标版本：

```cpp
int index = toolBox->addItem(page, "网络");
```

### 4.2 `insertItem()`

```cpp
int index = toolBox->insertItem(1, page, "连接");
```

若 `index` 超出范围，Qt 将页面追加到工具箱底部。不要依赖负数或超大 index 作为某种特殊业务排序协议；若想明确追加，直接使用 `addItem()` 更清晰。

插入页面会改变已有页面 index。若插入位置在当前页面之前，当前页面的 index 可能后移，但当前 page widget 本身不会因此变成另一个页面。

## 5. 设置和读取标题属性

每个页面标题可独立配置：

```cpp
toolBox->setItemText(index, "网络(&N)");
toolBox->setItemIcon(index, QIcon(":/network.svg"));
toolBox->setItemToolTip(index, "配置代理、连接和证书");
toolBox->setItemEnabled(index, false);
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 标题读取 | `itemText(int index)` | 返回指定页面的标题文字 | 索引越界返回空字符串；标题中的 `&` 会作为助记键标记 |
| 标题读取 | `itemIcon(int index)` | 返回指定页面标题旁的图标 | 索引越界返回空 `QIcon`；空图标不代表页面不存在 |
| 标题读取 | `itemToolTip(int index)` | 返回指定页面标题的提示文本 | 索引越界返回空字符串；只影响标题区域提示 |
| 状态读取 | `isItemEnabled(int index)` | 查询某个页面标题是否可选 | 禁用页面通常不能被用户切换到，但页面对象仍存在 |
| 标题修改 | `setItemText(int, const QString &)` | 修改指定页面的标题文字 | 不改变页面 widget 本身；注意助记键 `&` 的显示规则 |
| 标题修改 | `setItemIcon(int, const QIcon &)` | 修改指定页面标题图标 | 只影响工具箱标题区，不影响页面内容 |
| 标题修改 | `setItemToolTip(int, const QString &)` | 修改指定页面标题的 tooltip | 用于补充标题含义；不要把必要信息只放在 tooltip 中 |
| 状态修改 | `setItemEnabled(int, bool)` | 启用或禁用指定页面标题 | 禁用不是删除；已有数据和页面生命周期仍由容器关系管理 |

标题文字里的 `&` 会定义助记键：

```cpp
toolBox->setItemText(index, "网络(&N)");
```

`N` 将成为助记键；要显示字面量 `&`，使用 `&&`。

## 6. 切换当前页面

按 index 切换：

```cpp
toolBox->setCurrentIndex(networkIndex);
```

按页面指针切换：

```cpp
toolBox->setCurrentWidget(networkPage);
```

传给 `setCurrentWidget()` 的 widget 必须已经属于当前 `QToolBox`。当前页变化时，`currentChanged(int)` 发出；当不存在当前页时，信号参数是 `-1`。

`currentIndex` 只表示当前页面，不表示页面是否启用。禁用某页后是否需要切换到另一个可用页，应由你的交互流程明确处理。

## 7. 移除、移动与所有权

```cpp
QWidget *page = toolBox->widget(index);
toolBox->removeItem(index);
```

`removeItem(index)` 只将页面从工具箱移除，**不会删除页面 widget**。这使得页面可以被移到别处：

```cpp
toolBox->removeItem(toolBox->indexOf(networkPage));
otherContainer->layout()->addWidget(networkPage);
```

若你只是希望销毁页面，应在移除后按自身所有权策略处理：

```cpp
toolBox->removeItem(index);
page->deleteLater();
```

移动一个页面通常是“取到指针、移除、重新插入”：

```cpp
const int oldIndex = toolBox->indexOf(networkPage);
toolBox->removeItem(oldIndex);
toolBox->insertItem(0, networkPage, "网络");
```

不要先 `delete page` 再调用 `removeItem()`。页面被销毁时 Qt 会处理相关内部关系，但这类顺序容易让业务侧保留悬空指针；先明确移除再销毁更容易推理。

## 8. 与 QStyleOptionToolBox 的关系

`QToolBox` 管理页面，`QStyleOptionToolBox` 描述每一条页面标题的绘制参数。

```text
QToolBox
  └─ 内部标题条
       └─ QStyleOptionToolBox
            └─ QStyle::CE_ToolBoxTab
```

要改变页面内容，用 `QToolBox` API；要改变标题条的背景、图标、相邻选中边界等视觉效果，使用 `QProxyStyle` 并处理 `CE_ToolBoxTab`。不要在业务代码中手工构造 option 来试图切换页面。

## 9. 生命周期、线程与扩展点

- `QToolBox` 是 `QWidget`，只应在 GUI 线程创建和修改；
- 加入的页面由工具箱管理显示和 parent 关系；
- `removeItem()` 不删除页面；
- `widget(index)`、`currentWidget()` 返回非拥有指针；
- 插入和移除完成后，分别调用受保护虚函数 `itemInserted(index)` 和 `itemRemoved(index)`；
- 子类重写这两个钩子时，应把它们看作“页面结构变化后的通知”，不要在其中假设 index 永远对应旧页面。

`event()`、`showEvent()`、`changeEvent()` 是 QWidget/QFrame 的框架事件扩展点。除非确实要定制行为，普通项目不应靠重写它们来替代 `currentChanged()` 或页面自身的逻辑。

## 10. 常见误区

### 10.1 把 QToolBox 当成工具栏

QToolBox 容纳完整页面，不容纳 action 命令。工具栏用 `QToolBar`。

### 10.2 删除 item 后以为页面已被释放

`removeItem()` 不删除 widget。需要复用就重新插入；需要销毁就自己处理。

### 10.3 保存 index 作为永久身份

页面插入、删除、重排后 index 会变。保存页面指针或稳定的业务 id。

### 10.4 对不属于工具箱的 widget 调用 `setCurrentWidget()`

不会产生有效的当前页切换。先加入页面，再切换。

### 10.5 直接重画标题条

标题绘制由 style 系统负责。视觉定制应读 `QStyleOptionToolBox`，而不是从 `QToolBox::paintEvent()` 绕过内部标题结构。

## API 速查表
### 11.1 页面管理和属性

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| 构造 | `QToolBox(QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 创建垂直页面标题容器。 | `parent` 管理对象树；`f` 是窗口标志，不是页面配置。 |
| 析构 | `~QToolBox()` | 销毁工具箱及其管理的页面关系。 | 页面通常随 QObject 父子关系清理；被 `removeItem()` 取出的页面不再由工具箱管理。 |
| 查询 | `count()` | 返回当前页面数量。 | 空工具箱返回 `0`。 |
| 查询 | `currentIndex()` | 返回当前显示页面的 index。 | 空工具箱或无当前页时返回 `-1`。 |
| 切换 | `setCurrentIndex(int index)` | 按 index 切换当前页面。 | index 必须指向已有页面；切换会发出 `currentChanged()`。 |
| 查询 | `currentWidget()` | 返回当前显示的页面 widget。 | 没有当前页时返回 `nullptr`；返回指针不转移所有权。 |
| 切换 | `setCurrentWidget(QWidget *widget)` | 按页面指针切换当前页。 | widget 必须已经属于这个工具箱，不能传任意外部控件。 |
| 查询 | `widget(int index)` | 返回指定 index 对应的页面 widget。 | 越界返回 `nullptr`；页面插入/移除后旧 index 可能失效。 |
| 查询 | `indexOf(const QWidget *widget)` | 查询页面当前 index。 | 页面不属于该工具箱时返回 `-1`；适合用页面指针抵抗 index 变化。 |
| 添加 | `addItem(QWidget *, const QString &text)` | 在末尾添加无图标页面并返回新 index。 | 工具箱接管页面显示和父子关系，但不是永久业务身份。 |
| 添加 | `addItem(QWidget *, const QIcon &, const QString &text)` | 在末尾添加带图标页面。 | 图标用于标题条；建议使用多分辨率 `QIcon`。 |
| 插入 | `insertItem(int, QWidget *, const QString &text)` | 在指定位置插入无图标页面。 | 越界时通常追加；插入会改变后续页面 index。 |
| 插入 | `insertItem(int, QWidget *, const QIcon &, const QString &text)` | 在指定位置插入带图标页面。 | 插入前保存的后续 index 需要重新查询。 |
| 移除 | `removeItem(int index)` | 从工具箱中移除页面。 | 不会删除页面 widget；要复用就重新挂到其他容器，要销毁就由调用方处理。 |
| 状态 | `setItemEnabled(int, bool)` | 设置某个页面标题是否可用。 | 只控制标题交互和可用状态，不等于删除页面或强制切换当前页。 |
| 状态 | `isItemEnabled(int) const` | 查询某个页面标题是否可用。 | 先确认 index 有效；不要把越界结果当成业务状态。 |
| 标题 | `setItemText(int, const QString &)` | 修改页面标题文字。 | `&` 可定义助记键，显示字面量 `&` 要写成 `&&`。 |
| 标题 | `itemText(int) const` | 读取页面标题文字。 | 越界返回空字符串，空字符串不等于页面不存在。 |
| 图标 | `setItemIcon(int, const QIcon &)` | 修改页面标题图标。 | 图标变化会触发标题重绘；实际尺寸由 style 和 DPI 决定。 |
| 图标 | `itemIcon(int) const` | 读取页面标题图标。 | 越界返回空 `QIcon`。 |
| 提示 | `setItemToolTip(int, const QString &)` | 设置页面标题的工具提示。 | Qt 配置启用 tooltip 时可用；适合补充简短说明。 |
| 提示 | `itemToolTip(int) const` | 读取页面标题的工具提示。 | 越界返回空字符串；不等于页面内容 widget 的 tooltip。 |

### 11.2 信号和受保护 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| 信号 | `currentChanged(int index)` | 当前页面发生改变时通知外部。 | 没有当前页时 index 为 `-1`；适合同步业务状态和导航高亮。 |
| 受保护虚函数 | `itemInserted(int index)` | 新页面添加或插入完成后给子类的结构变化钩子。 | 它不是公共信号；重写时不要假设旧 index 仍代表同一个页面。 |
| 受保护虚函数 | `itemRemoved(int index)` | 页面移除完成后给子类的结构变化钩子。 | index 表示移除位置；需要页面对象时应在移除前保存指针。 |
| 事件 | `event(QEvent *)` | 处理工具箱及标题交互的通用事件入口。 | 仅在需要高级事件定制时重写，普通页面切换应连接信号。 |
| 事件 | `showEvent(QShowEvent *)` | 工具箱显示或再次显示时的事件。 | 不用于替代 `currentChanged()`；首次显示时页面状态可能仍需布局。 |
| 事件 | `changeEvent(QEvent *)` | 响应样式、字体、语言等外部环境变化。 | 自定义缓存或标题布局时要在这里正确失效和更新。 |

---

### 一句话总结

`QToolBox` 是垂直标题、一次展示一页的 `QWidget` 容器。用页面指针管理真实对象，用 index 做即时定位；插入会改变 index，移除不会删除页面，标题外观则交给 `QStyleOptionToolBox` 与 style 系统。
