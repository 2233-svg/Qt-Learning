# QDialogButtonBox

> Qt 6.11.1 · Qt Widgets · 来自 `QDialogButtonBox`

## 1. 先建立直觉

`QDialogButtonBox` 是自定义对话框里放“确定、取消、应用、帮助”等按钮的标准容器。它会根据平台样式自动决定按钮顺序和间距，避免你在 Windows、macOS、Linux 上手写出不符合习惯的按钮排列。

它不替你保存数据，也不自动关闭对话框；它通过按钮角色发出 `accepted()`、`rejected()`、`helpRequested()` 等信号，让你连接到 `QDialog::accept()`、`reject()` 或自己的槽。

## 2. 类说明

- 头文件：`#include <QDialogButtonBox>`
- 模块：`Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它通常放在对话框主布局底部或侧边，和 `QDialog` 搭配使用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QDialogButtonBox(parent)` | 创建空水平按钮盒。 |
| `QDialogButtonBox(buttons, parent)` | 用标准按钮集合创建。 |
| `QDialogButtonBox(orientation, parent)` | 创建指定方向按钮盒。 |
| `setStandardButtons()` / `standardButtons()` | 设置标准按钮集合。 |
| `addButton(StandardButton)` | 添加标准按钮并返回 `QPushButton`。 |
| `addButton(text, role)` | 添加自定义文本按钮并指定角色。 |
| `addButton(button, role)` | 添加已有按钮并指定角色。 |
| `removeButton()` | 移除按钮。 |
| `clear()` | 清空所有按钮。 |
| `button(StandardButton)` | 获取某个标准按钮对象。 |
| `standardButton(button)` | 查询按钮对应的标准按钮枚举。 |
| `buttonRole(button)` | 查询按钮角色。 |
| `buttons()` | 获取所有按钮。 |
| `setOrientation()` / `orientation()` | 水平或垂直排列。 |
| `setCenterButtons()` / `centerButtons()` | 是否居中按钮。 |
| `accepted()` | AcceptRole/YesRole 等接受类按钮触发。 |
| `rejected()` | RejectRole/NoRole 等拒绝类按钮触发。 |
| `helpRequested()` | HelpRole 按钮触发。 |
| `clicked(button)` | 任意按钮点击。 |

## 4. 关键用法

### 标准按钮优先

能用 `Ok | Cancel | Apply | Help` 这类标准按钮时，优先使用标准按钮。Qt 会处理本地化文本、图标、顺序和角色。自定义按钮适合业务动作，如“测试连接”“恢复默认配置”，并应选择正确的 `ButtonRole`。

### 角色决定信号

`AcceptRole`、`YesRole` 通常触发 `accepted()`；`RejectRole`、`NoRole` 通常触发 `rejected()`；`HelpRole` 触发 `helpRequested()`；`ActionRole` 更像“执行某个动作但不关闭”。按钮文字不决定行为，角色才决定语义。

### 自定义对话框的典型连接

```cpp
connect(buttonBox, &QDialogButtonBox::accepted, dialog, &QDialog::accept);
connect(buttonBox, &QDialogButtonBox::rejected, dialog, &QDialog::reject);
```

如果接受前要校验输入，不要直接连 `accept()`；先连接到自定义槽，校验通过再调用 `accept()`。

### 平台顺序不要手写

macOS、Windows、GNOME 等平台对“确定/取消”的顺序习惯不同。`QDialogButtonBox` 的意义就是让你不必在布局里手动排列按钮。

## 5. 常见坑与经验

- `clicked()` 总会发出，但不代表对话框应该关闭。
- `ActionRole` 按钮不会自动 accept/reject，适合“应用”“测试”等行为。
- 校验失败时不要关闭对话框，给出错误提示并保持焦点。
- `centerButtons` 常用于消息框风格，自定义设置对话框通常保持默认。
- 自定义按钮也要设置合适默认按钮和快捷键，保证键盘体验。
