# QScopedPropertyUpdateGroup
> Qt 6.11.1 · Qt Core · 来自 `QScopedPropertyUpdateGroup`

## 作用定位
`QScopedPropertyUpdateGroup` 在作用域内合并 Qt 属性绑定系统的变化通知，避免连续写多个互相关联属性时触发中间态重算。
## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 开始一个属性更新组。 |
| 析构函数 | 结束组并统一处理挂起的属性更新。 |
| `endUpdate()` | 提前结束当前组。 |
## 使用场景
```cpp
QScopedPropertyUpdateGroup batch;
width = 640;
height = 480;
```
## 常见坑与经验
- 只合并属性系统更新，不是线程同步原语。
- 组范围不要覆盖耗时 I/O 或事件循环嵌套。
- 用它消除可观察的中间状态，不应借它掩盖循环绑定。
## 知识点覆盖
批量更新、响应式依赖、通知合并、RAII、中间态。
