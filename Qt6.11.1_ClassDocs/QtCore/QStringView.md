# QStringView
> Qt 6.11.1 · Qt Core · 来自 `QStringView`

## 作用定位
`QStringView` 是 UTF-16 字符串的非拥有只读视图，可引用 `QString`、`QChar` 数组或兼容字面量，用于避免只读参数复制。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 从字符串、字面量或指针范围创建视图。 |
| `size()` / `empty()` | 查询长度和空状态。 |
| `data()` | 取得 UTF-16 首地址。 |
| `mid/left/right` | 创建子视图。 |
| `toString()` | 拷贝为拥有型 `QString`。 |
| `begin/end` | 遍历 `QChar`。 |

## 使用场景
```cpp
bool isKeyword(QStringView s);
```
函数只读、不保存参数时使用 view，让调用者传 `QString` 或字面量都高效。

## 常见坑与经验
- 不拥有数据，不能保存引用临时字符串的 view。
- `data()` 不保证以 NUL 结尾，传给 C API 前要拷贝或附加终止符。
- 长度是 UTF-16 单元数，不等于用户可见字符数。

## 知识点覆盖
非拥有视图、UTF-16、参数优化、临时对象生命周期、NUL 终止边界。
