# QPageSetupDialog
> Qt 6.11.1 · Qt Print Support · 来自 `QPageSetupDialog`

## 1. 先建立直觉

`QPageSetupDialog` 是页面设置对话框，用来让用户调整纸张、方向和页边距等页面布局参数。它修改的是 `QPrinter` 的页面配置，不负责选择打印机，也不负责执行打印。

## 2. 类说明

保留类说明：这些 API 来自 `QPageSetupDialog`，属于 Qt Print Support 模块，用于显示页面设置界面并更新 `QPrinter`。

它适合放在“页面设置...”菜单项里，和“打印...”分开：前者配置页面，后者选择设备并开始打印。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QPageSetupDialog(parent)` | 使用内部打印机配置创建页面设置对话框。 |
| `QPageSetupDialog(QPrinter *printer, parent)` | 修改调用者提供的 `QPrinter` 页面设置。 |
| `exec()` | 模态显示页面设置。 |
| `open(receiver, member)` | 非模态显示，结束后通知 receiver。 |
| `printer()` | 返回被修改的 `QPrinter`。 |
| `done(result)` / `setVisible(visible)` | 对话框生命周期重实现，通常由框架调用。 |

## 4. 典型流程

```cpp
QPageSetupDialog dialog(&printer, this);
if (dialog.exec() == QDialog::Accepted) {
    updatePagePreview(printer.pageLayout());
}
```

页面设置通常应该影响预览和后续打印，因此对话框接受后要刷新文档分页或预览缓存。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 文档编辑器页面设置 | 用户先设置纸张/方向/边距，再编辑或打印。 |
| 报表打印参数 | 让用户在打印前调整横向/纵向和边距。 |
| 预览前配置页面 | 接受后调用预览控件的 `updatePreview()`。 |

## 6. 常见坑与经验

页面设置改变后，文档分页可能全部变化。不要只刷新当前页画面；页数、页码、页眉页脚和表格断页都可能要重算。

某些平台或打印驱动会限制可用纸张和边距。用户在对话框里能选的结果，要以最终 `QPrinter` 状态为准。

如果程序自己维护 `QPageLayout`，要决定是以 `QPrinter` 为真，还是以文档模型为真。两边各存一份但不同步，会造成预览和打印不一致。

## 7. 知识点覆盖

- 页面设置和打印执行的职责分离。
- `QPrinter` 页布局、方向、纸张和边距。
- 页面设置变更后的重新分页。
- 模态/非模态对话框生命周期。
