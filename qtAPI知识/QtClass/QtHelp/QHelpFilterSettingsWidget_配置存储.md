# QHelpFilterSettingsWidget：编辑 Help filter 的设置面板

> 适用版本：Qt 6.11.1
> 头文件：`#include <QHelpFilterSettingsWidget>`
> 所属模块：`Qt6::Help`
> 继承：`QWidget`

## 它解决什么问题

`QHelpFilterSettingsWidget` 是 Qt Help 的 filter 编辑控件。它把 filter 名称、可用 component 和 version 选项组织成一个设置界面，应用可以先从 `QHelpFilterEngine` 读取已有配置，再让用户修改，最后把结果写回 engine。

它只负责设置界面和读写适配，不负责显示目录、索引或搜索结果，也不拥有传入的 `QHelpFilterEngine`。

## 实际使用场景

- 在帮助窗口中提供“配置过滤器”对话框。
- 从 engine 读取已有 filters，让用户添加、删除或调整组件/版本条件。
- 由应用提供 `availableComponents()`、`availableVersions()` 选项。
- 用户点击“应用”时调用 `applySettings()`，成功后切换 active filter 并刷新内容。

## 推荐调用顺序

创建控件后，先调用 `setAvailableComponents()` 和 `setAvailableVersions()` 填充可选项，再调用 `readSettings(filterEngine)` 读取当前配置。用户编辑结束后调用 `applySettings(filterEngine)` 写回。

`readSettings()` 不会取得 engine 所有权；engine 必须在调用期间保持有效并已经 setup。`applySettings()` 返回 `false` 时，设置可能没有完整写入，应用应保留对话框让用户修正，或读取 engine 的错误信息。

组件和版本选项是界面可选集合，不是自动从 engine 实时同步的数据库。注册/注销文档后，应用应重新提供列表并重新读取设置。

## 生命周期与线程

这是 QWidget，只能在 GUI 线程创建和访问，父对象通常负责销毁。传给 `readSettings()` 或 `applySettings()` 的 engine 不会因为控件关闭而销毁；应用必须保证其生命周期覆盖操作。

## 常见误区

- 在没有提供可用 component/version 列表时直接显示设置控件。
- 先编辑控件，再调用 `readSettings()`，导致用户修改被已有配置覆盖。
- 把 `applySettings()` 的 `true` 理解为 active filter 已经切换；它只负责写入设置。
- engine 尚未 setup、处于只读模式或 collection 不可写时忽略失败返回。
- 在工作线程读写 QWidget 或帮助引擎。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `explicit QHelpFilterSettingsWidget(QWidget *parent = nullptr)` | 创建 filter 设置控件。 | 必须在 GUI 线程；父对象可负责控件销毁。 |
| `~QHelpFilterSettingsWidget()` | 销毁设置控件。 | 不会销毁传入的 `QHelpFilterEngine`。 |
| `void setAvailableComponents(const QStringList &components)` | 设置界面可供选择的 component 列表。 | 注册文档变化后应重新设置；列表不等于当前 filter。 |
| `void setAvailableVersions(const QList<QVersionNumber> &versions)` | 设置界面可供选择的 version 列表。 | 应与 engine 当前已注册文档元数据保持一致。 |
| `void readSettings(const QHelpFilterEngine *filterEngine)` | 从 engine 读取 filter 配置并填充控件。 | 调用前先设置选项；engine 必须有效且 setup 完成。 |
| `bool applySettings(QHelpFilterEngine *filterEngine) const` | 将控件中的 filter 配置写回 engine。 | 返回值必须检查；不自动替换 active filter，也不拥有 engine。 |
| `QWidget::show()` / `exec()` | 显示设置面板或对话框。 | Qt Help 不提供 `exec()`，通常把控件放入自定义 `QDialog`。 |

## 一句话总结

`QHelpFilterSettingsWidget` 是 filter 的编辑器：先提供选项，再读入 engine 配置，最后检查 `applySettings()` 是否成功写回。
