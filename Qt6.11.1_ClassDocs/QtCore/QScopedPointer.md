# QScopedPointer
> Qt 6.11.1 · Qt Core · 来自 `QScopedPointer<T, Cleanup>`

## 作用定位
`QScopedPointer` 是不可复制的作用域独占指针，离开作用域自动按 cleanup 策略销毁对象。现代 C++ 普通对象的首选通常是 `std::unique_ptr`；本类在 Qt 代码、特定清理策略及 pimpl 私有实现中仍很常见。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 接管裸指针所有权。 |
| `data()` / `get()` | 取得不转移所有权的裸指针。 |
| `operator->` / `operator*` | 像普通指针一样访问对象。 |
| `isNull()` / `operator bool` | 判断是否拥有对象。 |
| `reset(ptr)` | 删除当前对象并接管新对象。 |
| `take()` | 放弃所有权并返回裸指针，调用者必须接管释放。 |
| `swap()` | 交换两个独占所有者。 |
| `QScopedPointerDeleteLater` | 对 QObject 使用 `deleteLater()` 的清理策略。 |

## 使用场景
```cpp
QScopedPointer<Parser> parser(new Parser);
if (!parser->open(path))
    return;
consume(parser.data());
```

## 常见坑与经验
- 不能复制，只能移动式地转移设计责任；不要尝试让两个 `QScopedPointer` 接管同一裸指针。
- `take()` 后原指针不再管理资源，立即交给另一个所有者或在异常安全边界内处理。
- QObject 有父对象时通常无需再放进 scoped pointer，双重所有权会导致重复释放。
- PIMPL 中析构点必须看到完整私有类型定义，或采用合适 cleanup 策略。

## 知识点覆盖
RAII、独占所有权、pimpl、cleanup policy、QObject 延迟销毁、异常安全、与 `std::unique_ptr` 的取舍。
