# QAccessibleEditableTextInterface

> Qt 6.11.1 · Qt GUI · 来自 `QAccessibleEditableTextInterface`

## 1. 先建立直觉

`QAccessibleEditableTextInterface` 赋予辅助技术修改文本的能力。屏幕阅读器、语音输入和替代输入工具可以借此在自定义编辑器中插入、删除或替换文本，而不必模拟不可靠的键盘事件。

它是 `QAccessibleTextInterface` 的补充：后者负责读取文本、光标和选择；本接口负责写入。一个只读文本展示不应实现它，一个真正可编辑的自定义文本组件通常应同时实现二者。

## 2. 类说明

- 头文件：`#include <QAccessibleEditableTextInterface>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：抽象可访问子接口；通过 `QAccessibleInterface::interface_cast()` 提供。
- 对象要求：编辑操作必须与组件的真实文本模型、撤销栈、验证规则和变化通知保持一致。

偏移量是文本接口使用的字符位置，不是 UTF-8 字节偏移，也不应直接当作渲染 glyph 或像素坐标。

## 3. API 速查

| API | 用途 |
|---|---|
| `insertText(offset, text)` | 在偏移量处插入文本。 |
| `deleteText(startOffset, endOffset)` | 删除 `[startOffset, endOffset)` 范围文本。 |
| `replaceText(startOffset, endOffset, text)` | 以给定文本替换该半开区间。 |
| 析构函数 | 供多态销毁；接口由可访问对象体系管理。 |

所有区间都应按半开区间理解：起点包含、终点不包含。因此 `deleteText(4, 4)` 是空操作，`replaceText(0, length, text)` 可替换整段内容。

## 4. 关键用法

```cpp
void AccessibleEditor::replaceText(int start, int end, const QString &text)
{
    auto *editor = this->editor();
    if (!editor->canEditRange(start, end))
        return;

    editor->document()->replace(start, end - start, text);
    // document() 的正常修改路径负责撤销栈、重绘和文本变化事件。
}
```

实现应调用与普通用户编辑相同的文档/命令路径，而不是直接篡改底层字符串。这样输入法、撤销/重做、最大长度、只读区域、语法高亮和 `QAccessibleTextInsertEvent` / `QAccessibleTextRemoveEvent` 等通知才能保持一致。

## 5. 使用场景

| 场景 | 是否应实现 |
|---|---|
| `QLineEdit`、`QTextEdit` 等标准控件 | 通常无需自行实现，Qt 已提供接口。 |
| 自定义代码编辑器、终端输入区 | 应实现，并与自身文档模型和选择逻辑对接。 |
| 公式、富文本或结构化编辑器 | 可以实现，但要明确偏移量在逻辑文本中的含义。 |
| 只读预览、日志、标签 | 不实现；仅提供文本读取接口即可。 |
| 密码输入 | 是否允许辅助技术修改取决于组件策略，但不能泄露读取文本。 |

## 6. 常见坑与经验

- 对无效范围要安全处理：`start`、`end` 不能越界，且 `start <= end`。不要因为平台传来异常索引而让编辑器崩溃。
- `QString` 的索引以 UTF-16 code unit 为基础；表情、组合字符和某些文字可能由多个 code unit 组成。编辑器应尽量按文本光标边界校正，而不是把区间截在代理项中间。
- 不要把 `insertText()` 实现为模拟键盘事件。它会受当前焦点、输入法、快捷键和事件过滤器影响，且难以保证确定性。
- 修改后必须让 `QAccessibleTextInterface` 返回的新文本、光标和选择与真实界面一致。
- 只读、锁定或验证失败时应拒绝修改并维持状态一致；不要假装成功后再悄悄回滚。
- GUI 文本模型通常只能在 GUI 线程修改。后台语音识别结果应排队回 GUI 线程后再执行编辑。

## 7. 知识点覆盖

- 可读文本接口与可编辑文本接口的分工
- 半开文本区间和插入/删除/替换语义
- Unicode、UTF-16 偏移与文本边界
- 与文档模型、撤销栈、验证和输入法的集成
- 文本变化无障碍事件与线程边界
