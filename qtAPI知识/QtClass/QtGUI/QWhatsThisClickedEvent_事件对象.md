# QWhatsThisClickedEvent：Whats This 超链接事件

> 适用版本：Qt 6.11.1
> 头文件：`#include <QWhatsThisClickedEvent>`
> 所属模块：`Qt6::Gui`
> 继承：`QEvent`

## 它解决什么问题

`QWhatsThisClickedEvent` 表示用户点击了 `QWhatsThis` 帮助文本中的超链接。它把链接地址作为事件数据交给接收对象，使应用可以把帮助文本中的某个链接转换为打开文档、切换设置页或跳转到在线说明等动作。

这个类只负责携带 `href`，不负责解析 HTML，也不负责打开链接。链接如何解释、是否允许外部地址以及由哪个对象处理，都由应用决定。

## 实际使用场景

- 在自定义窗口或控件中拦截 `QEvent::WhatsThisClicked`。
- 将 `href` 映射为应用内部帮助页、设置页或命令。
- 对外部链接调用 `QDesktopServices::openUrl()`，对内部链接走自己的路由。
- 在统一帮助控制器中记录用户从 What's This 文本进入了哪个主题。

## 处理方式与生命周期

事件通常由 Qt 在 What's This 交互过程中创建并派发。可在控件重写 `event()`，或在事件过滤器中检查事件类型后转换为 `QWhatsThisClickedEvent`。事件对象只适合在当前事件处理期间读取；如果需要异步处理，应立即复制 `href()` 返回的 `QString`，不要保存事件指针。

处理完后是否调用 `accept()` 或 `ignore()`，取决于应用是否希望继续让默认处理流程接管。对于自定义路由，通常处理成功后接受事件，并返回 `true`。

## 关键边界

- `href()` 返回的是链接属性值，不保证一定是完整 URL，也可能是应用自定义的相对标识。
- 空字符串并不等于“没有事件”；它可能来自没有有效 `href` 的链接文本，应用应自行决定是否忽略。
- 该类只有在启用 `whatsthis` 配置时可用。
- `href()` 按值返回 `QString`，适合复制保存；事件本身仍不能跨事件循环长期持有。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `explicit QWhatsThisClickedEvent(const QString &href)` | 创建一个携带链接地址的 What's This 点击事件。 | `href` 只是数据，不会自动进行 URL 解析或打开。 |
| `QString href() const` | 返回被点击链接的 `href` 值。 | 返回副本；可立即复制后交给异步任务。 |
| `QEvent::type()` | 取得事件类型，通常为 `QEvent::WhatsThisClicked`。 | 先检查类型再转换事件对象。 |
| `accept()` / `ignore()` | 标记事件是否已处理。 | 自定义帮助路由通常在成功处理后接受事件。 |

## 一句话总结

`QWhatsThisClickedEvent` 是 What's This 超链接点击时的轻量数据事件：读取 `href`，按应用自己的帮助路由处理即可。
