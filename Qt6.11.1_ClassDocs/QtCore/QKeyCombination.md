# QKeyCombination
> Qt 6.11.1 · Qt Core · 来自 `QKeyCombination`

## 作用定位
`QKeyCombination` 将一个 Qt 键码与零个或多个键盘修饰键组合为强类型快捷键值，避免用裸整数拼接按键状态。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 `(modifiers, key)` | 构造组合键。|
| `keyboardModifiers()` | 读取 Ctrl、Shift、Alt 等修饰键。|
| `key()` | 读取主键。|
| `toCombined()` | 转为兼容旧 API 的整型组合值。|
| `fromCombined()` | 从旧整型组合值恢复。|

## 使用场景
处理 `QKeyEvent`、定义动作快捷键、在 QML/C++ 边界传递用户触发的组合键。

## 常见坑与经验
- 物理按键布局和文本输入语义不同；快捷键匹配不要用字符文本替代 Qt 键码。
- `Ctrl` 与 macOS `Meta` 的用户习惯不同，跨平台命令快捷键优先使用 Qt 标准键机制。

## 知识点覆盖
键盘事件、修饰键、快捷键、跨平台键位、类型安全。
