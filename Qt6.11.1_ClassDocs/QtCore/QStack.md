# QStack
> Qt 6.11.1 · Qt Core · 来自 `QStack<T>`

## 作用定位
`QStack<T>` 是后进先出容器，基于 Qt 顺序容器提供 `push/pop/top` 语义。它适合解析栈、撤销片段、深度优先遍历等场景。

## API 速查
| API | 是做什么的 |
|---|---|
| `push()` | 把元素压入栈顶。 |
| `pop()` | 移除并返回栈顶元素；栈不能为空。 |
| `top()` | 查看栈顶元素但不移除。 |
| `swap()` | 快速交换两份栈内容。 |
| 继承的 `isEmpty()` / `size()` | 检查状态。 |

## 使用场景
```cpp
QStack<Node *> stack;
stack.push(root);
while (!stack.isEmpty())
    visit(stack.pop());
```

## 常见坑与经验
- `pop/top` 都要求非空；解析输入前保持明确的空栈错误处理。
- 不要在需要队列语义时使用栈，任务调度通常应是 `QQueue` 或优先队列。
- 大对象频繁入栈可考虑移动语义或存指针/值句柄。

## 知识点覆盖
LIFO、解析、DFS、容器继承、空栈检查、移动成本。
