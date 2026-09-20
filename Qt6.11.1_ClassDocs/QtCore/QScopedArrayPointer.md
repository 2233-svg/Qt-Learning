# QScopedArrayPointer
> Qt 6.11.1 · Qt Core · 来自 `QScopedArrayPointer<T, Cleanup>`

## 作用定位
`QScopedArrayPointer` 是面向 `new T[]` 分配数组的作用域独占指针，析构时使用数组删除语义。现代 C++ 优先使用 `std::vector<T>` 管理动态数组；只有确实需要原生数组所有权接口时才选它。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 接管由 `new T[]` 获得的数组。 |
| `operator[]` | 访问数组元素，不做边界检查。 |
| `data()` / `get()` | 取得不转移所有权的数组首地址。 |
| `reset(ptr)` | 释放旧数组后接管新数组。 |
| `take()` | 交出数组所有权，调用者需用 `delete[]` 或匹配所有者释放。 |
| `isNull()` / `operator bool` | 判断是否持有数组。 |
| `swap()` | 交换两份数组所有权。 |

## 使用场景
```cpp
QScopedArrayPointer<char> buffer(new char[capacity]);
const qint64 read = device.read(buffer.data(), capacity);
```

## 常见坑与经验
- 只能接管 `new[]` 的结果，不能接管 `malloc`、`QByteArray::data()`、栈数组或单对象 `new T`。
- 它不保存长度；边界、元素数和容量必须由调用者另行维护。
- 需要调整大小、迭代、自动记录长度时 `QByteArray`、`QVector` 或 `std::vector` 更合适。
- `take()` 后释放方式必须仍是 `delete[]`，不能写成 `delete`。

## 知识点覆盖
数组所有权、`delete[]`、缓冲区边界、RAII、容器替代方案、C API 互操作。
