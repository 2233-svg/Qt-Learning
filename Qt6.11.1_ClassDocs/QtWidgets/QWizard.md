# QWizard

> Qt 6.11.1 · Qt Widgets · 来自 `QWizard`

## 1. 先建立直觉

`QWizard` 是多步骤流程对话框。它把“下一步/上一步/完成/取消”、页面切换、字段共享、校验、分支流程和平台化向导外观组合在一起。

它适合安装、导入、项目创建、账户配置、复杂设置初始化这类需要分步收集信息的任务。不适合只有一两个简单选项的普通对话框。

## 2. 类说明

`QWizard` 继承自 `QDialog`。每一步是一个 `QWizardPage`，页面可以注册字段，wizard 通过 `field()` / `setField()` 共享数据。流程可以是线性的，也可以通过 `nextId()` 动态分支。

Wizard 的关键不是“分页显示控件”，而是控制用户完成任务的路径：什么时候能下一步，什么时候必须验证，什么时候进入提交页，什么时候完成。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `addPage(QWizardPage *)` | 添加页面并自动分配 id。 |
| `setPage(int, QWizardPage *)` | 用指定 id 注册页面，适合分支流程。 |
| `page(int)` / `pageIds()` | 查询页面。 |
| `setStartId(int)` / `startId()` | 设置或读取起始页。 |
| `currentId()` / `currentPage()` | 当前页面 id 和对象。 |
| `nextId()` | 返回下一页 id；可重写实现全局流程。 |
| `field()` / `setField()` | 读取或写入页面注册字段。 |
| `validateCurrentPage()` | 切换下一步前验证当前页。 |
| `hasVisitedPage()` / `visitedIds()` | 查询访问历史。 |
| `setButton()` / `button()` | 替换或读取 Back/Next/Finish 等按钮。 |
| `setButtonText()` / `buttonText()` | 自定义按钮文本。 |
| `setButtonLayout()` | 自定义按钮排列。 |
| `setOption()` / `testOption()` | 设置向导行为选项，如起始页无返回按钮。 |
| `setPixmap()` / `pixmap()` | 设置 watermark、logo、banner、background 图。 |
| `setWizardStyle()` | 设置 Classic、Modern、Mac、Aero 等风格。 |
| `currentIdChanged()` | 当前页变化时发出。 |
| `pageAdded()` / `pageRemoved()` | 页面增删时发出。 |

## 4. 关键用法

```cpp
auto *wizard = new QWizard(this);
wizard->addPage(new IntroPage);
wizard->addPage(new AccountPage);
wizard->addPage(new SummaryPage);
wizard->setWindowTitle(tr("New Project"));
wizard->exec();
```

读取页面字段：

```cpp
const QString name = wizard->field("project.name").toString();
```

自定义按钮：

```cpp
wizard->setButtonText(QWizard::FinishButton, tr("Create"));
wizard->setOption(QWizard::NoBackButtonOnStartPage);
```

## 5. 使用场景

适合创建项目向导、安装器、导入流程、首次运行配置、连接远程服务、生成证书、复杂导出设置。

不适合小表单或频繁任务。向导会增加步骤感，只有当分步能降低认知负担时才值得使用。

## 6. 常见坑与经验

页面之间不要直接互相找控件。用 `registerField()` 和 `field()` 共享数据，流程会更清楚。

耗时验证不要阻塞 GUI。需要联网或扫描文件时，禁用按钮、显示进度，把结果通过信号带回。

分支流程要把 page id 当作流程图维护。随意依赖添加顺序，后期插页会很痛。
