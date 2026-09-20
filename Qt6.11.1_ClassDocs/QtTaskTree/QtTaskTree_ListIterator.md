# QtTaskTree::ListIterator
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::ListIterator`

## 作用定位

`ListIterator<T>` 让 TaskTree 对 `QList<T>` 中的每个元素执行循环体。循环体中可以通过 `operator*` 或 `operator->` 读取当前元素。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`Iterator`

## API 速查

| API | 说明 |
| --- | --- |
| `ListIterator(const QList<T> &list)` | 用列表创建迭代器。 |
| `operator*()` | 返回当前元素的只读引用。 |
| `operator->()` | 返回当前元素的只读指针。 |

## 使用场景

- 对文件列表逐个执行异步处理。
- 对 URL 列表逐个下载。
- 对配置项列表逐个校验。

## 常见坑与经验
- 列表内容应在任务运行期间保持稳定；不要边迭代边修改源列表。
- 当前元素是只读访问，写入需求应放到存储对象或外部结果集合。
- 每次迭代的异步流程完成后才推进下一项，除非循环体内部再显式并行。

## 知识点覆盖

- 列表批处理
- 当前元素访问
- 迭代源生命周期
