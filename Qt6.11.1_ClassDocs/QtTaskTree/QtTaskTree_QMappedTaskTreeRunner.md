# QtTaskTree::QMappedTaskTreeRunner
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::QMappedTaskTreeRunner`

## 作用定位

`QMappedTaskTreeRunner` 把一组输入项映射成一组任务树运行。它适合“对每个数据项构造一个 recipe，然后统一运行和收集结果”的批处理模式。

## 类说明

- 头文件：`#include <qtasktreerunner.h>`
- 继承：`QObject`

## API 速查

| API | 说明 |
| --- | --- |
| 映射启动接口 | 根据输入项创建并启动对应任务树。 |
| `cancel()` | 取消当前映射批处理。 |
| `isRunning()` | 是否仍有映射任务在执行。 |
| 完成信号 | 批处理或单项完成时通知。 |

## 使用场景

| 场景 | 说明 |
| --- | --- |
| 文件列表处理 | 每个文件映射成一个检查/转换 recipe。 |
| URL 列表下载 | 每个 URL 对应一棵任务树。 |
| 项目批量操作 | 每个项目使用同一 recipe 模板但不同输入。 |

## 常见坑与经验

- mapper 捕获输入时要避免引用悬空，尤其是异步运行。
- 大批量映射要考虑并发限制，不要一次性打满资源。
- 单项失败的聚合策略要提前设计：全部失败、部分成功还是继续收集。

## 知识点覆盖

- map-style 批处理
- 输入到 recipe 的转换
- 结果聚合和并发控制
