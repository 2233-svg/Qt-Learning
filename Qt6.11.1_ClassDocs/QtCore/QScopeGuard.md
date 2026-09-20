# QScopeGuard
> Qt 6.11.1 · Qt Core · 来自 `QScopeGuard<Functor>`

## 作用定位
`QScopeGuard` 在离开作用域时执行一个无参清理函数，是没有专门 RAII 类型时的轻量退出钩子。
## API 速查
| API | 是做什么的 |
|---|---|
| `qScopeGuard(functor)` | 创建守卫，析构时调用函子。 |
| `dismiss()` | 取消后续清理。 |
| 移动构造 | 转移清理责任。 |
## 使用场景
```cpp
beginUpdate();
const auto finish = qScopeGuard([this] { endUpdate(); });
```
## 常见坑与经验
- 清理函数应 `noexcept` 且快速；析构中抛异常会终止程序。
- 捕获 `this` 时对象必须仍然存活。
- 成功路径可 `dismiss()`，但不要把它变成难以追踪的隐式控制流。
## 知识点覆盖
Scope exit、RAII、异常安全、清理路径、移动所有权。
