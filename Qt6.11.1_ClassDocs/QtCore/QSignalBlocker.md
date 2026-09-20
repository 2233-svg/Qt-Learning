# QSignalBlocker
> Qt 6.11.1 · Qt Core · 来自 `QSignalBlocker`
## 作用定位
`QSignalBlocker` 临时调用 QObject 的 `blockSignals(true)`，析构时恢复原先的阻塞状态，常用于批量更新控件避免递归信号。
## API 速查
| API | 是做什么的 |
|---|---|
| `(QObject *)` | 构造时阻塞该对象信号。 |
| `unblock()` / `reblock()` | 临时恢复或再次阻塞。 |
| `dismiss()` | 放弃恢复责任，对象已销毁时使用。 |
## 使用场景
```cpp
QSignalBlocker blocker(combo);
combo->setCurrentIndex(index);
```
## 常见坑与经验
- 被阻塞的信号不会排队补发；必要业务更新应显式执行。
- 只影响该对象，不影响其子对象和其他连接端。
- 如果对象先销毁，先 `dismiss()`。
## 知识点覆盖
信号抑制、RAII、递归更新、批量 UI 同步、生命周期。
