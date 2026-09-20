# QScopedValueRollback
> Qt 6.11.1 · Qt Core · 来自 `QScopedValueRollback<T>`

## 作用定位
`QScopedValueRollback` 在进入作用域时记住一个变量值，析构时自动恢复，适合临时状态标记和重入防护。
## API 速查
| API | 是做什么的 |
|---|---|
| `(T &var)` | 保存当前值，析构时恢复。 |
| `(T &var, value)` | 保存旧值并立即写入临时值。 |
| `commit()` | 将当前值设为新的恢复基线。 |
## 使用场景
```cpp
QScopedValueRollback<bool> guard(m_updating, true);
refresh();
```
## 常见坑与经验
- 管理的是变量值，不管理锁、对象所有权或异常本身。
- `commit()` 后恢复的是提交时的值，命名要清楚避免误解。
- 被引用变量必须比 rollback 对象活得久。
## 知识点覆盖
RAII、状态恢复、重入防护、异常安全、事务式局部修改。
