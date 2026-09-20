# Qt QWizard 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QWizard>`
> 所属模块：`Qt6::Widgets`
> 继承：`QDialog -> QWizard`
> 常见搭档：`QWizardPage`、`QLineEdit`、`QCheckBox`、`QComboBox`

## 1. QWizard 解决什么问题

`QWizard` 是一套“分步骤完成任务”的对话框框架。它最适合注册、配置、导入、创建项目这类流程：用户一页一页往前走，页面之间还能互相传值、校验输入、决定下一页去哪。

它解决的不是普通表单问题，而是这三件事：

- 把一个复杂流程拆成可理解的步骤；
- 管住“下一步 / 上一步 / 完成 / 帮助”这些按钮；
- 让页面间共享字段，而不是页面彼此硬耦合。

典型场景：

- 新建项目向导；
- 注册/登录/初始化流程；
- 导入导出步骤；
- 条件分支比较多的设置向导。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QLabel>
#include <QVBoxLayout>
#include <QWizard>
#include <QWizardPage>

static QWizardPage *makePage(const QString &title, const QString &text)
{
    auto *page = new QWizardPage;
    page->setTitle(title);

    auto *layout = new QVBoxLayout(page);
    layout->addWidget(new QLabel(text));
    return page;
}

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWizard wizard;
    wizard.addPage(makePage("欢迎", "这是第一步"));
    wizard.addPage(makePage("完成", "这是最后一步"));
    wizard.show();

    return app.exec();
}
```

`QWizard` 的核心不是“显示一个对话框”，而是“让页面按规则流转”。页与页之间的逻辑应该通过 `QWizardPage` 的 `nextId()`、`isComplete()`、`registerField()` 来表达。

## 3. 页面怎么组织

### 3.1 `addPage`

```cpp
int id = wizard.addPage(new QWizardPage);
```

适合线性向导。`addPage()` 会返回系统分配的页面 ID，ID 会比当前已有 ID 更大。

### 3.2 `setPage`

```cpp
enum PageId { Page_Intro, Page_Details, Page_Done };
wizard.setPage(Page_Intro, new QWizardPage);
wizard.setPage(Page_Details, new QWizardPage);
wizard.setPage(Page_Done, new QWizardPage);
```

适合非线性向导。你自己定义 ID，就能在 `nextId()` 里跳转到不同页面。

### 3.3 页面生命周期

```cpp
wizard.setStartId(Page_Intro);
```

`startId` 决定第一次显示的页面。若没显式设置，Qt 会从已插入页面里找一个合适的起点。

页面进入和退出时，向导会调用：

- `initializePage()`：显示前准备页面；
- `cleanupPage()`：返回上一步时清理页面；
- `validateCurrentPage()`：点 Next / Finish 前做最后校验。

## 4. 字段机制是核心

`QWizard` 最好用的地方不是页面跳转，而是“字段共享”。

```cpp
class AccountPage : public QWizardPage
{
public:
    AccountPage()
    {
        auto *edit = new QLineEdit;
        registerField("account.name*", edit);
    }
};
```

字段名末尾的 `*` 表示必填字段。只要该字段没填好，Next / Finish 就会被禁用。

页面里可以直接读别的页的字段：

```cpp
QString name = field("account.name").toString();
wizard()->setField("account.name", "Alice");
```

这比页面之间互相传指针干净得多。

## 5. 页面流转怎么定

### 5.1 `nextId`

`QWizardPage::nextId()` 决定下一页是谁。  
如果你不重写它，默认就是按 ID 递增。

### 5.2 `isComplete`

`isComplete()` 决定当前页能不能继续往下走。  
如果你自己控制复杂校验，就重写它，并在状态变化时发 `completeChanged()`。

### 5.3 `validatePage`

`validatePage()` 适合做最后一步校验，比如检查文件路径是否可写、密码是否一致。  
如果只是表单没填完，优先用必填字段或 `isComplete()`，别把所有逻辑都塞进 `validatePage()`。

## 6. 按钮、外观和风格

```cpp
wizard.setWizardStyle(QWizard::ModernStyle);
wizard.setOption(QWizard::HaveHelpButton, true);
wizard.setOption(QWizard::IndependentPages, true);
wizard.setButtonText(QWizard::CancelButton, tr("退出"));
```

`WizardButton` 决定按钮槽位，`WizardOption` 决定按钮是否出现、顺序如何、页面是否独立。

几个最常见的选项：

- `IndependentPages`：回退时不重置页面字段；
- `NoBackButtonOnStartPage`：起始页不显示返回；
- `HaveNextButtonOnLastPage`：最后页也保留 Next；
- `HaveFinishButtonOnEarlyPages`：提前完成；
- `NoCancelButton`：去掉取消；
- `HaveHelpButton`：增加帮助按钮；
- `HaveCustomButton1/2/3`：加自定义按钮。

## 7. 页标题、图片和侧边栏

```cpp
wizard.setTitleFormat(Qt::RichText);
wizard.setSubTitleFormat(Qt::RichText);
wizard.setPixmap(QWizard::LogoPixmap, QPixmap(":/logo.png"));
wizard.setSideWidget(new QLabel(tr("提示区")));
```

`QWizardPage` 自己也有 `title`、`subTitle` 和页级 pixmap。  
`QWizard` 的 `setPixmap()` 是全局设置，页级 `setPixmap()` 可以覆盖具体页面。

`setSideWidget()` 适合放说明、图示或辅助内容。这个 widget 会被向导接管生命周期，别再手动 delete。

## 8. 适合怎么验证

```cpp
connect(&wizard, &QWizard::currentIdChanged,
        [](int id) { qDebug() << "page:" << id; });
```

`currentIdChanged`、`pageAdded`、`pageRemoved`、`helpRequested`、`customButtonClicked` 是向导调试时最有用的信号。

## API 速查表
### 9.1 构造、页面和流转

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QWizard(QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 创建一个向导对话框外壳。 | 它继承 `QDialog`，适合短流程任务，不适合当普通主窗口用。 |
| 析构 | `~QWizard()` | 销毁向导以及由它托管的页面。 | 页面加入向导后通常不用手动 delete。 |
| 页面管理 | `addPage(QWizardPage *page)` | 追加页面，并返回自动分配的页面 ID。 | 适合一页接一页的线性流程；后续跳转逻辑依赖返回的 ID。 |
| 页面管理 | `setPage(int id, QWizardPage *page)` | 用指定 ID 注册页面。 | 适合非线性流程；自己定义枚举 ID 可读性更好。 |
| 页面管理 | `removePage(int id)` | 从向导中移除指定页面。 | 会改变可访问页面集合，复杂向导中要重新检查 `nextId()`。 |
| 页面查询 | `page(int id) const` | 根据 ID 取回页面指针。 | ID 不存在时返回空指针，使用前先判断。 |
| 页面查询 | `pageIds() const` | 返回当前所有页面 ID。 | 常用于调试、生成步骤导航或检查页面注册是否完整。 |
| 访问历史 | `visitedIds() const` | 返回用户已经走过的页面 ID。 | 分支流程中可据此判断某一步是否曾经出现过。 |
| 访问历史 | `hasVisitedPage(int id) const` | 判断某个页面是否被访问过。 | 只反映本轮向导历史，`restart()` 后逻辑要重新看。 |
| 起点 | `setStartId(int id)` / `startId() const` | 设置或读取向导起始页面。 | 起始页最好显式设置，避免页面插入顺序变化带来隐性影响。 |
| 当前页 | `currentPage() const` / `currentId() const` | 读取当前页面对象或当前页面 ID。 | 做状态栏提示、日志、调试跳转时很有用。 |
| 当前页 | `setCurrentId(int id)` | 程序主动跳到指定页面。 | ID 必须有效；别用它绕过页面校验做正常流程跳转。 |
| 导航槽 | `back()` | 返回上一页。 | 会触发对应页面清理逻辑，是否回滚字段受选项影响。 |
| 导航槽 | `next()` | 前进到下一页。 | 会经过当前页完整性与校验流程。 |
| 导航槽 | `restart()` | 重新开始向导流程。 | 会回到起始页，并重建访问路径。 |
| 流程钩子 | `nextId() const` | 计算当前页之后应该去哪一页。 | 通常由 `QWizardPage::nextId()` 承担，向导级重写适合集中控制流程。 |
| 流程钩子 | `validateCurrentPage()` | 离开当前页前做最终校验。 | 返回 `false` 会停在当前页；耗时校验要给用户反馈。 |

### 9.2 字段、按钮和外观

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 字段 | `field(const QString &name) const` | 读取向导中注册字段的当前值。 | 页面之间传数据优先用字段，不要互相保存控件指针。 |
| 字段 | `setField(const QString &name, const QVariant &value)` | 设置某个注册字段的值。 | 字段名要和 `registerField()` 一致；类型转换由 `QVariant` 承担。 |
| 字段 | `setDefaultProperty(const char *className, const char *property, const char *changedSignal)` | 为某类输入控件指定默认字段属性和变化信号。 | 自定义控件参与 `registerField()` 时很关键，信号签名要能触发完成状态刷新。 |
| 外观 | `setWizardStyle(WizardStyle style)` / `wizardStyle() const` | 设置或读取向导整体风格。 | 不同平台表现不同，别把像素级布局写死。 |
| 选项 | `setOption(WizardOption option, bool on = true)` | 打开或关闭单个向导选项。 | 用来控制按钮、页面回滚、帮助按钮、自定义按钮等行为。 |
| 选项 | `testOption(WizardOption option) const` | 检查某个选项当前是否启用。 | 写条件逻辑时比直接比较 flags 清楚。 |
| 选项 | `setOptions(WizardOptions options)` / `options() const` | 批量设置或读取向导选项集合。 | 初始化时一次设置更集中；后续修改要确认不会打乱当前页面状态。 |
| 按钮 | `setButtonText(WizardButton which, const QString &text)` / `buttonText(WizardButton which) const` | 设置或读取某个向导按钮文字。 | 页面级按钮文字可由 `QWizardPage` 覆盖。 |
| 按钮 | `setButtonLayout(const QList<WizardButton> &layout)` | 自定义底部按钮排列顺序。 | 别漏掉必要按钮；`Stretch` 用来控制按钮之间的空白。 |
| 按钮 | `setButton(WizardButton which, QAbstractButton *button)` / `button(WizardButton which) const` | 替换或访问某个按钮对象。 | 自定义按钮后要保持向导期望的点击语义。 |
| 图片 | `setPixmap(WizardPixmap which, const QPixmap &pixmap)` / `pixmap(WizardPixmap which) const` | 设置或读取全局向导图片。 | 页级图片可覆盖全局图片；资源大小要适配不同向导风格。 |
| 标题格式 | `setTitleFormat(Qt::TextFormat format)` / `titleFormat() const` | 控制页面标题按纯文本还是富文本解释。 | 富文本标题要避免拼接不可信字符串。 |
| 标题格式 | `setSubTitleFormat(Qt::TextFormat format)` / `subTitleFormat() const` | 控制副标题文本格式。 | 长副标题会影响页面高度，尽量保持简短。 |
| 侧边栏 | `setSideWidget(QWidget *widget)` / `sideWidget() const` | 设置或读取向导侧边辅助控件。 | 向导会接管传入 widget 的所有权；适合说明区，不适合塞主表单。 |

### 9.3 信号和受保护函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `currentIdChanged(int id)` | 当前页面 ID 改变时发出。 | 适合更新步骤提示、日志或外部导航状态。 |
| 信号 | `helpRequested()` | 用户点击 Help 按钮时发出。 | 只有相关选项启用后按钮才会出现。 |
| 信号 | `customButtonClicked(int which)` | 用户点击自定义按钮时发出。 | `which` 对应 `CustomButton1/2/3`，业务逻辑要自己分派。 |
| 信号 | `pageAdded(int id)` | 页面加入向导时发出。 | 动态构建页面或排查注册顺序时有用。 |
| 信号 | `pageRemoved(int id)` | 页面移除时发出。 | 移除页面后要确认当前页和下一页仍合法。 |
| 保护钩子 | `initializePage(int id)` | 某页即将显示时执行初始化。 | 默认会转调页面自己的 `initializePage()`；重写时别破坏字段初始化。 |
| 保护钩子 | `cleanupPage(int id)` | 用户回退离开某页时执行清理。 | `IndependentPages` 会影响默认字段回滚行为。 |
| QWidget 重写 | `setVisible(bool visible)` | 显示或隐藏向导。 | 显示向导会启动当前页初始化流程。 |
| QWidget 重写 | `sizeHint() const` | 返回向导建议尺寸。 | 多页尺寸差异大时，可通过页面布局和尺寸策略影响最终效果。 |

### 一句话总结

`QWizard` 的本质是“把多步流程变成可校验、可分支、可回退的页面链”；页面之间别硬传对象，优先用 field，页面流转别写死，优先让 `nextId()` 和 `isComplete()` 说话。
