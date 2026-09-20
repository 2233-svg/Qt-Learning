# QWizardPage

> Qt 6.11.1 · Qt Widgets · 来自 `QWizardPage`

## 1. 先建立直觉

`QWizardPage` 是 `QWizard` 的单个步骤页面。它既是一个 `QWidget`，负责摆放本页控件；又是流程节点，负责声明标题、字段、是否完成、下一页是谁、离开前是否验证。

一个好页面应该只处理本步骤的信息，不要把整个向导流程都塞进页面 UI 代码里。

## 2. 类说明

`QWizardPage` 继承自 `QWidget`。它通过 `registerField()` 把控件属性注册成字段，wizard 和其他页面可以用字段名读取。必填字段通常用字段名后加 `*` 表示。

页面生命周期有几个关键钩子：进入页时 `initializePage()`，离开并回退清理时 `cleanupPage()`，点击下一步/完成前 `validatePage()`，控制下一页用 `nextId()`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setTitle()` / `title()` | 设置或读取页面标题。 |
| `setSubTitle()` / `subTitle()` | 设置或读取页面副标题。 |
| `registerField(name, widget, property, changedSignal)` | 把控件属性注册为 wizard 字段。 |
| `field()` / `setField()` | 读取或写入已注册字段。 |
| `initializePage()` | 页面即将显示时调用，适合根据前面字段初始化。 |
| `cleanupPage()` | 用户回退离开时调用，适合恢复本页状态。 |
| `isComplete()` | 返回本页是否完成，影响 Next/Finish 按钮。 |
| `completeChanged()` | 完成状态变化时发出。 |
| `validatePage()` | 点击 Next/Finish 前验证并决定是否允许离开。 |
| `nextId()` | 返回下一页 id，实现分支。 |
| `setCommitPage()` / `isCommitPage()` | 标记提交页，按钮语义会变化。 |
| `setFinalPage()` / `isFinalPage()` | 标记最终页。 |
| `setButtonText()` / `buttonText()` | 为本页覆盖按钮文本。 |
| `setPixmap()` / `pixmap()` | 为本页覆盖向导图片。 |
| `wizard()` | 返回所属 `QWizard`。 |

## 4. 关键用法

```cpp
class AccountPage : public QWizardPage {
public:
    AccountPage()
    {
        setTitle(tr("Account"));
        registerField("account.user*", userEdit);
        registerField("account.token*", tokenEdit);
    }

    bool validatePage() override
    {
        return verifyToken(field("account.token").toString());
    }
};
```

动态分支：

```cpp
int ModePage::nextId() const
{
    return field("advanced").toBool() ? AdvancedPageId : SummaryPageId;
}
```

## 5. 使用场景

适合向导中的信息收集页、确认页、分支选择页、提交页、结果页。

如果页面只是普通设置页的一部分，不需要上一步/下一步流程，就用普通 `QWidget` 加布局。

## 6. 常见坑与经验

`isComplete()` 改变后必须发 `completeChanged()`，否则按钮状态不会及时更新。

`validatePage()` 适合离开前最终检查；实时启用/禁用下一步更适合 `isComplete()`。

必填字段只检查属性是否“非空/有效”，复杂规则仍需要自己实现。
