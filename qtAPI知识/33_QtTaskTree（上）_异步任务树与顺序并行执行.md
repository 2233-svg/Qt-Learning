# Qt TaskTree（上）：异步任务树与顺序、并行执行

Qt TaskTree 模块用于把异步工作组织成声明式任务树。与“创建一堆 `QFuture` 再手动串联回调”相比，任务树把顺序、并行、条件、循环和完成处理集中描述，并由运行器负责生命周期、取消和进度聚合。

> 该模块的 API 命名空间是 `QtTaskTree`，核心类包括 `QTaskTree`、`Group`、`Then`、`QSequentialTaskTreeRunner` 和 `QParallelTaskTreeRunner`。使用前应确认当前 Qt 版本对该模块的发布状态和 ABI 兼容承诺。

## 1. 安装和 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core TaskTree)

target_link_libraries(mytarget PRIVATE
    Qt6::Core
    Qt6::TaskTree
)
```

部分 Qt 发行包可能把 TaskTree 作为技术预览或单独开发组件提供。若 `find_package` 找不到模块，先检查 Qt 安装是否包含 `qttasktree` 文档、头文件和 CMake 配置，而不要把 API 复制到项目中自行维护。

## 2. 任务树的基本模型

任务树是一个由节点组成的配方（recipe）：

```text
Group
├─ 初始化（同步任务）
├─ Then ─► 下载配置（异步任务）
└─ 并行组
   ├─ 加载图片
   └─ 读取缓存
```

`Group` 把多个任务组合起来；`Then` 表示前一个任务完成后再进入下一个任务；并行组允许互不依赖的分支同时运行。树本身描述“做什么”，`QTaskTree` 或运行器描述“何时运行、如何取消和如何接收完成通知”。

## 3. 最小顺序任务示例

```cpp
#include <QTaskTree>
#include <QDebug>

using namespace QtTaskTree;

Group recipe = Group {
    Sync([] {
        qDebug() << "准备资源";
    }),
    Then([] {
        return QThreadFunction([] {
            QThread::msleep(100);
            qDebug() << "后台工作完成";
        });
    })
};

QTaskTree tree(recipe);
QObject::connect(&tree, &QTaskTree::done,
                 [](DoneWith result) {
    qDebug() << "任务树结束:" << result;
});
```

不同任务工厂（如 `Sync`、`Then`）的可用重载取决于 Qt 6.11.1 的头文件定义。核心思想是：同步函数快速返回，耗时工作包装为异步任务，完成结果通过树的 `done` 信号统一通知。

## 4. `QTaskTree` 生命周期与状态

### 4.1 启动与完成

```cpp
QTaskTree tree(recipe);
tree.start();

QObject::connect(&tree, &QTaskTree::done,
                 &tree, [](DoneWith result) {
    // result 表示成功、取消或失败等终态
});
```

构造树和启动树是两个阶段。这样可以先连接信号、设置对象父子关系，再开始执行。若树对象析构，未完成的任务会按模块规则停止或取消，因此树的生命周期至少要覆盖整个异步流程。

### 4.2 查询运行状态与进度

```cpp
if (tree.isRunning())
    qDebug() << "当前仍在运行";

qDebug() << tree.progressValue() << "/" << tree.progressMaximum();

QObject::connect(&tree, &QTaskTree::progressValueChanged,
                 [](qsizetype value) {
    qDebug() << "进度:" << value;
});
```

进度是树中任务进度的聚合值，只有任务正确报告进度时才有意义。不要把“已进入回调”直接当成完成百分比；对于无法估算的网络任务，应显示忙碌状态或阶段文本。

### 4.3 取消任务树

```cpp
cancelButton->setEnabled(true);
QObject::connect(cancelButton, &QPushButton::clicked,
                 &tree, &QTaskTree::cancel);
```

`cancel()` 是协作式取消：运行器发出取消信号，任务实现需要定期检查并尽快结束。阻塞在不可中断系统调用中的任务无法立即响应，因此接口设计时应把大工作拆成可检查取消状态的小步骤。

## 5. 顺序运行器：`QSequentialTaskTreeRunner`

### 5.1 将多个配方排队

```cpp
#include <QSequentialTaskTreeRunner>

QSequentialTaskTreeRunner runner;
runner.enqueue(firstRecipe,
               [] { qDebug() << "第一个任务开始"; },
               [](DoneWith result) {
                   qDebug() << "第一个任务结束:" << result;
               });
runner.enqueue(secondRecipe);
```

顺序运行器保证队列中的配方按提交顺序运行。前一个任务完成、取消或失败后，后一个任务是否继续取决于完成策略和 `DoneWith` 结果。需要严格事务语义时，应在完成处理器中明确决定是否继续入队。

### 5.2 管理当前任务

```cpp
if (runner.isRunning())
    runner.cancelCurrent();

runner.resetCurrent();
runner.reset();
```

`cancelCurrent()` 只取消当前配方，队列中的后续配方仍可保留；`cancel()` 通常取消整个队列。`resetCurrent()` 和 `reset()` 用于清理当前状态或整个运行器，调用前应确认没有业务代码仍在引用任务结果。

## 6. 并行运行器：`QParallelTaskTreeRunner`

```cpp
#include <QParallelTaskTreeRunner>

QParallelTaskTreeRunner runner;
runner.start({recipeA, recipeB, recipeC});

QObject::connect(&runner, &QParallelTaskTreeRunner::done,
                 [](DoneWith result) {
    qDebug() << "并行批次结束:" << result;
});
```

并行执行适合互不依赖的工作，例如读取多个配置文件或同时请求不同服务。共享资源仍需要自己的线程安全策略；任务树只负责调度，不会自动保护数据库连接、临界区或非线程安全的第三方对象。

### 6.1 并行与顺序的组合

```cpp
Group recipe = Group {
    prepareTask,
    Parallel {
        downloadTask,
        cacheTask
    },
    finalTask
};
```

这类结构表达“先准备，再并行，再汇总”。汇总任务只有在并行分支按组策略完成后才开始。设计时应避免在并行分支中直接写同一个 UI 控件；让分支返回数据，最后在 GUI 线程统一更新界面。

## 7. `QFuture` 与任务树的桥接

已有 Qt Concurrent 或自定义异步 API 时，可以把 `QFuture<void>` 纳入任务树：

```cpp
QFuture<void> future = QtConcurrent::run([] {
    // 耗时计算
});

Group recipe = Group {
    Then(future),
    Sync([] { qDebug() << "future 已完成"; })
};
```

如果异步 API 不是 `QFuture`，可以使用 `QCustomTask` 或适配器在下一篇中介绍的接口，把回调完成转换为 TaskTree 能识别的完成事件。

## 8. 完成结果与错误传播

`DoneWith` 用于描述树的结束原因，常见类别包括正常完成、被取消和失败。不要只连接一个无参数“完成”槽而忽略结果，否则用户点击取消后可能仍被当成成功。

```cpp
QObject::connect(&tree, &QTaskTree::done,
                 [&](DoneWith result) {
    switch (result) {
    case DoneWith::Success:
        showSuccess();
        break;
    case DoneWith::Canceled:
        showCanceled();
        break;
    default:
        showFailure();
        break;
    }
});
```

枚举成员名称应以本机 Qt 头文件为准；文档版本变化可能增加新的失败或跳过状态。业务代码可以把底层结果映射为自己的错误类型，避免 UI 直接依赖 TaskTree 的内部枚举。

## 9. 线程边界和 QObject 规则

任务树可以在线程池中执行函数，但 QObject 仍有线程亲和性：

- GUI 控件只能在 GUI 线程访问。
- `QNetworkAccessManager`、数据库连接等对象通常应在所属线程创建和使用。
- 信号槽跨线程连接默认是队列连接，槽函数会在接收对象线程执行。
- 捕获局部引用的异步 lambda 可能在函数返回后悬空，应捕获值或使用受控生命周期对象。

推荐让任务返回值通过安全的数据类型传递，再在 `done` 或 GUI 线程槽中更新界面：

```cpp
auto *guard = new QPointer<MainWindow>(window);
// 异步任务只生成纯数据；完成槽检查 guard 后更新 UI。
```

## 10. 调试和可观测性

为每棵树设置业务标识，在任务开始、结束、取消和失败时记录结构化日志。至少记录：任务名、批次 ID、耗时、线程、完成结果和错误码。不要在高频进度信号中打印大量日志，否则日志 I/O 反过来拖慢任务。

## 11. 选择合适的执行方式

| 场景 | 推荐方式 |
| --- | --- |
| 单个简单异步操作 | `QFuture` 或自定义信号 |
| 多步骤且有依赖 | `QTaskTree` + `Group`/`Then` |
| 一批任务必须串行 | `QSequentialTaskTreeRunner` |
| 独立任务并发 | `QParallelTaskTreeRunner` |
| 需要跨任务共享结果 | `Storage`（见下篇） |
| 需要自定义生命周期/取消 | `QCustomTask`、`QTaskInterface` |

下一篇将深入自定义任务适配器、`Storage`、屏障（Barrier）、循环和并发限制，并给出网络/进程任务的可靠性模式。
