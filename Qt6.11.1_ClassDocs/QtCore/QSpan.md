# QSpan
> Qt 6.11.1 · Qt Core · 来自 `QSpan<T, Extent>`

## 作用定位
`QSpan` 是连续内存的非拥有视图，类似 `std::span`。它用指针和长度描述一段数组、容器或缓冲区，不负责分配和释放。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 从数组、指针加长度或连续容器创建视图。 |
| `data()` | 取得首地址。 |
| `size()` / `size_bytes()` | 查询元素数和字节数。 |
| `empty()` | 判断是否为空。 |
| `operator[]` | 无边界检查访问元素。 |
| `first()` / `last()` / `subspan()` | 创建子视图。 |
| `begin()` / `end()` | 迭代元素。 |

## 使用场景
函数只需要临时读取或写入调用者提供的连续数据时，用 `QSpan` 避免复制和模板泛滥。

```cpp
void normalize(QSpan<float> samples);
```

## 常见坑与经验
- `QSpan` 不延长底层内存生命期，不能返回指向局部数组的 span。
- `operator[]` 不检查范围，外部长度协议必须可信。
- 容器扩容或 detach 后，旧 span 可能悬空。
- 只读接口用 `QSpan<const T>`，让写权限在类型上可见。

## 知识点覆盖
非拥有视图、连续内存、生命周期、边界检查、零拷贝 API、const 正确性。
