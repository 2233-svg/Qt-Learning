# Qt QWizardPage 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）
> 头文件：`#include <QWizardPage>`
> 所属模块：`Qt6::Widgets`
> 继承：`QWidget -> QWizardPage`
> 常见搭档：`QWizard`

## 1. QWizardPage 解决什么问题

`QWizardPage` 是向导中的“一页”。它并不是普通的表单页，而是专门为 `QWizard` 设计的：它知道自己什么时候该被初始化、什么时候该被清理、什么时候该判定为完成、下一页是谁。

它负责的不是单纯显示控件，而是这几个问题：

- 这一页的标题和副标题是什么；
- 页面里哪些输入是必填的；
- 当前页是否已经完整；
- 页面跳转到哪里；
- 页面里的字段怎样暴露给别的页。

## 2. 最小可用代码

```cpp
#include <QApplication>
#include <QLabel>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QWizard>
#include <QWizardPage>

class NamePage : public QWizardPage
{
public:
    NamePage()
    {
        setTitle(tr("用户名"));
        auto *edit = new QLineEdit;
        registerField("account.name*", edit);

        auto *layout = new QVBoxLayout(this);
        layout->addWidget(new QLabel(tr("请输入用户名：")));
        layout->addWidget(edit);
    }
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWizard wizard;
    wizard.addPage(new NamePage);
    wizard.show();

    return app.exec();
}
```

`QWizardPage` 自己可以看作一个普通 widget，但只有放进 `QWizard` 后，它的向导语义才完整。

## 3. 标题、副标题和图

```cpp
page->setTitle("创建账户");
page->setSubTitle("先填最关键的信息");
page->setPixmap(QWizard::LogoPixmap, QPixmap(":/logo.png"));
```

页面标题和副标题会被 `QWizard` 用来组织页面头部。  
图片也可以按页面单独设置，不必全局共用一套。

如果页面是最终页，可以直接标记：

```cpp
page->setFinalPage(true);
page->setCommitPage(true);
```

- `finalPage` 会让 Finish 逻辑出现；
- `commitPage` 适合“提交并继续”的页面。

## 4. 字段机制

`QWizardPage` 最值钱的能力就是注册字段。

```cpp
registerField("profile.email*", emailEdit);
registerField("profile.age", ageSpinBox);
```

字段名末尾 `*` 表示必填。  
如果你不手动指定属性名和 changedSignal，Qt 会对常见控件自动选默认属性，比如 `QLineEdit::text`、`QCheckBox::checked`、`QComboBox::currentIndex`。

页面内部可直接读写字段：

```cpp
QString email = field("profile.email").toString();
setField("profile.email", "alice@example.com");
```

这比页面之间互相找控件稳得多。

## 5. 页面生命周期

```cpp
void initializePage() override;
void cleanupPage() override;
bool validatePage() override;
bool isComplete() const override;
int nextId() const override;
```

这些函数各管一段：

- `initializePage()`：页面刚要显示时填默认值；
- `cleanupPage()`：用户点 Back 时清理或回滚；
- `validatePage()`：用户点 Next / Finish 前的最后检查；
- `isComplete()`：决定 Next / Finish 是否可点；
- `nextId()`：决定下一页是谁。

如果你重写 `isComplete()`，记得在状态变化时发 `completeChanged()`，否则向导按钮不会及时刷新。

## 6. 常见用法

### 6.1 初始化时引用前页字段

```cpp
void initializePage() override
{
    QString name = field("account.name").toString();
    setSubTitle(tr("欢迎，%1").arg(name));
}
```

### 6.2 必填字段

```cpp
registerField("license.key*", keyEdit);
```

必填字段的逻辑不是简单看控件有没有内容，它还会考虑原始值和部分控件的可接受输入状态。

### 6.3 自定义完整性判断

```cpp
bool isComplete() const override
{
    return !emailEdit->text().isEmpty() && emailEdit->hasAcceptableInput();
}
```

这比只靠 `registerField()` 更灵活。

## 7. 什么时候重写哪一个

| 需求 | 更适合的钩子 |
| --- | --- |
| 进入页面时预填数据 | `initializePage()` |
| 返回上一页时恢复状态 | `cleanupPage()` |
| 控制 Next / Finish 是否可用 | `isComplete()` + `completeChanged()` |
| 最后一步校验并阻止前进 | `validatePage()` |
| 根据用户选择决定下一页 | `nextId()` |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QWizardPage(QWidget *parent = nullptr)` | 创建一个向导页面。 | 单独创建只是普通 widget，放进 `QWizard` 后才有完整流程语义。 |
| 析构 | `~QWizardPage()` | 销毁页面及其子控件。 | 页面加入向导后通常由向导管理生命周期。 |
| 标题 | `title() const` / `setTitle(const QString &title)` | 读取或设置页面主标题。 | 标题显示在向导头部，用来告诉用户当前步骤是什么。 |
| 标题 | `subTitle() const` / `setSubTitle(const QString &subTitle)` | 读取或设置页面副标题。 | 副标题适合解释本页要做的事，不适合堆大段说明。 |
| 图片 | `pixmap(QWizard::WizardPixmap which) const` / `setPixmap(QWizard::WizardPixmap which, const QPixmap &pixmap)` | 读取或设置页面级图片。 | 页面设置会覆盖向导全局图片，常用于某一步需要不同图示。 |
| 流程状态 | `isFinalPage() const` / `setFinalPage(bool finalPage)` | 判断或标记该页是否可作为最终页。 | 非线性流程里某些分支可提前 Finish 时很有用。 |
| 流程状态 | `isCommitPage() const` / `setCommitPage(bool commitPage)` | 判断或标记该页是否是提交页。 | 适合“点 Commit 后执行不可轻易回退的动作”的步骤。 |
| 按钮 | `buttonText(QWizard::WizardButton which) const` / `setButtonText(QWizard::WizardButton which, const QString &text)` | 读取或设置本页面专属按钮文字。 | 它会覆盖向导全局按钮文字，只影响当前页。 |
| 生命周期 | `initializePage()` | 页面即将显示时初始化内容。 | 常用于读取前面页面的字段并填充当前页。 |
| 生命周期 | `cleanupPage()` | 用户点击 Back 离开页面时清理。 | 默认会恢复注册字段的初始值，是否保留取决于向导选项。 |
| 校验 | `validatePage()` | 点击 Next 或 Finish 前做最终校验。 | 返回 `false` 会阻止离开当前页；适合路径可写、账号可用这类最终检查。 |
| 完成状态 | `isComplete() const` | 判断当前页是否已经填写完整。 | 重写后状态变化时必须发 `completeChanged()`。 |
| 流程跳转 | `nextId() const` | 返回下一页 ID。 | 分支向导的核心入口；返回 `-1` 表示没有下一页。 |
| 信号 | `completeChanged()` | 页面完成状态可能变化时通知向导刷新按钮。 | 输入控件变化、校验状态变化时要发出。 |
| 字段 | `field(const QString &name) const` | 读取向导字段值。 | 可读其他页面注册过的字段，减少页面之间的直接依赖。 |
| 字段 | `setField(const QString &name, const QVariant &value)` | 修改向导字段值。 | 字段名必须已注册；类型要能转换成目标控件属性类型。 |
| 字段 | `registerField(const QString &name, QWidget *widget, const char *property = nullptr, const char *changedSignal = nullptr)` | 把页面中的控件注册成向导字段。 | 字段名末尾 `*` 表示必填；自定义控件最好显式给 property 和 changedSignal。 |
| 所属关系 | `wizard() const` | 返回当前页面所在的 `QWizard`。 | 页面还没加入向导时可能为空，使用前先判断。 |

### 一句话总结

`QWizardPage` 就是一页，但它不是“摆控件的页”，而是“会初始化、会验证、会决定流程的一页”；字段共享和 `isComplete()` 才是它真正的骨架。
