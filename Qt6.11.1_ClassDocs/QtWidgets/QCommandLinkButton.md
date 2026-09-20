# QCommandLinkButton

> Qt 6.11.1 · Qt Widgets · 来自 `QCommandLinkButton`

## 1. 先建立直觉

`QCommandLinkButton` 是一种“带说明的命令入口”。它看起来像按钮，但语义更接近“选择下一步做什么”：标题告诉用户动作，描述补充后果或适用条件。

它最适合出现在向导、首次启动页、设置入口、错误恢复界面中，让用户从几条明确路径里选一条。和普通 `QPushButton` 相比，它能承载更多解释；和 `QRadioButton` 相比，它不是先选择再确认，而是点击即执行或进入下一步。

## 2. 类说明

`QCommandLinkButton` 继承自 `QPushButton`，因此保留按钮的点击、默认按钮、图标、启用状态、快捷键等行为，同时新增 `description` 属性，用来显示副标题式说明。

它的强项是降低用户做选择时的认知成本。按钮文本应该写动作本身，例如“创建新项目”；描述写补充条件，例如“从模板开始，并在下一步选择构建系统”。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QCommandLinkButton(QWidget *)` | 创建空命令链接按钮。 |
| `QCommandLinkButton(const QString &, QWidget *)` | 创建只有主标题的命令链接按钮。 |
| `QCommandLinkButton(const QString &, const QString &, QWidget *)` | 创建带主标题和描述的按钮，是最常见构造方式。 |
| `setDescription(const QString &)` / `description()` | 设置或读取描述文字。描述应解释动作结果，而不是重复标题。 |
| `setText(const QString &)` / `text()` | 继承自 `QAbstractButton`，设置按钮主标题。 |
| `clicked(bool)` | 用户点击时发出，用于进入对应流程或执行命令。 |
| `setIcon(const QIcon &)` | 给命令添加视觉识别。图标应服务于动作，不要只作装饰。 |
| `setDefault(bool)` | 在对话框中指定默认触发按钮。谨慎使用，避免用户误触高风险操作。 |
| `setFlat(bool)` / `isFlat()` | 继承按钮扁平样式属性；是否有效取决于平台样式。 |
| `sizeHint()` / `minimumSizeHint()` | 返回适合主标题和描述的尺寸，布局中应给它足够宽度。 |
| `heightForWidth(int)` | 文本换行后高度会随宽度变化，适合响应式布局。 |

## 4. 关键用法

```cpp
auto *createProject = new QCommandLinkButton(
    tr("Create a new project"),
    tr("Start from a template and configure build settings."),
    this);

connect(createProject, &QCommandLinkButton::clicked,
        this, &WelcomePage::openNewProjectWizard);
```

多个命令链接按钮放在一起时，标题之间应互斥且可比较：

```cpp
layout->addWidget(new QCommandLinkButton(tr("Open existing workspace"),
                                         tr("Choose a folder that already contains project files.")));
layout->addWidget(new QCommandLinkButton(tr("Clone from version control"),
                                         tr("Download a remote repository and open it locally.")));
```

这里每个按钮都是一条路径，不需要再放一个“确定”按钮。用户点击时就应该进入对应流程。

## 5. 使用场景

适合欢迎页、安装向导、首次运行配置、错误恢复页、空状态页、导入向导入口、账户连接选项、项目创建方式选择。

不适合工具栏、小表单提交、表格行操作、频繁点击的小按钮。那些地方 `QPushButton`、`QToolButton` 或菜单动作更轻、更符合用户预期。

## 6. 常见坑与经验

描述文字不是帮助文档。它应该一句话说明“点它会发生什么”，而不是塞入完整规则。

不要把风险不同的操作并排做成同等视觉重量。例如“打开示例项目”和“删除所有本地配置”不应该只是两个一样的 command link。

如果命令只是切换一个选项而不是立即进入流程，优先考虑 `QRadioButton`。`QCommandLinkButton` 的心理模型是“点了就走”。
