# QtTaskTree::Forever
> Qt 6.11.1 · Qt TaskTree · 来自 `QtTaskTree::Forever`

## 作用定位

`Forever` 是无限重复执行的可执行组。它适合常驻监听、轮询、服务循环等需要持续运行直到外部取消的流程。

## 类说明

- 头文件：`#include <qtasktree.h>`
- 基类：`ExecutableItem`

## API 速查

| API | 说明 |
| --- | --- |
| `Forever(const GroupItems &children)` | 持续重复执行子项列表。 |
| `Forever(std::initializer_list<GroupItem>)` | 初始化列表版本。 |

## 使用场景

- 等待外部事件并循环处理。
- 持续重试/轮询直到任务树被取消。
- 长生命周期后台工作流。

## 常见坑与经验
- 无限流程一定要配取消、超时、外部 stop 或退出条件，否则测试和关闭都麻烦。
- 循环体失败后是停止还是继续，要结合 workflow policy 设计。
- 不要用 `Forever` 替代定时器；如果只是定时触发，定时任务/等待节点更清晰。

## 知识点覆盖

- 无限任务流程
- 外部取消
- 常驻异步工作流
- 失败策略
