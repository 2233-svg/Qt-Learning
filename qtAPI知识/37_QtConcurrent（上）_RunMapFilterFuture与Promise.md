# Qt Concurrent（上）：Run、Map、Filter、QFuture 与 QPromise

Qt Concurrent 在 `QThreadPool` 之上提供高层并行 API。它适合把纯计算、批量转换和可拆分任务交给线程池，而不必手工创建 `QThread`、移动 QObject 或编写工作队列。

它不能让任意代码自动线程安全。传入的函数必须明确输入、输出和共享状态，GUI 对象仍只能在 GUI 线程访问。

## 1. CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Concurrent)

target_link_libraries(mytarget PRIVATE
    Qt6::Core
    Qt6::Concurrent
)
```

常用头文件：

```cpp
#include <QtConcurrent>
#include <QFuture>
#include <QFutureWatcher>
#include <QPromise>
```

## 2. `QtConcurrent::run`：执行一个函数

### 2.1 最小示例

```cpp
QFuture<int> future = QtConcurrent::run([] {
    int sum = 0;
    for (int i = 1; i <= 1000; ++i)
        sum += i;
    return sum;
});
```

`run()` 把可调用对象提交到线程池，立即返回 `QFuture<T>`。任务何时实际开始取决于线程池负载。

### 2.2 传递参数

```cpp
QString path = "data/input.txt";
QFuture<QByteArray> future = QtConcurrent::run(
    [](QString filePath) {
        QFile file(filePath);
        if (!file.open(QIODevice::ReadOnly))
            return QByteArray{};
        return file.readAll();
    },
    path);
```

默认按值复制参数更安全。若使用 `std::ref` 或捕获引用，必须保证任务完成前对象一直存在，并且并发访问受到保护。

### 2.3 成员函数

```cpp
QFuture<QImage> future = QtConcurrent::run(
    &ImageProcessor::resize,
    processor,
    input,
    QSize(800, 600));
```

传对象指针时要保证对象存活，并确认成员函数可以在任意线程调用。QObject 的线程亲和性不会因为 `run()` 自动迁移。

## 3. 不要在 GUI 线程等待

```cpp
// GUI 线程中不推荐：
const int result = future.result();
```

如果结果尚未就绪，`result()`、`waitForFinished()` 和部分结果访问可能阻塞。GUI 线程应使用 `QFutureWatcher` 或 continuation：

```cpp
auto *watcher = new QFutureWatcher<int>(window);

QObject::connect(watcher, &QFutureWatcher<int>::finished,
                 window, [watcher, window] {
    window->showResult(watcher->result());
    watcher->deleteLater();
});

watcher->setFuture(future);
```

先连接信号，再调用 `setFuture()`，避免一个极快任务在连接前已经完成。

## 4. `QFuture` 的状态与结果

`QFuture<T>` 是共享的异步结果句柄，可复制但不拥有 GUI 生命周期。常见状态：

```cpp
future.isStarted();
future.isRunning();
future.isFinished();
future.isCanceled();
future.resultCount();
```

对于多结果 future，可读取单个结果或全部结果：

```cpp
for (const auto &value : future.results())
    qDebug() << value;
```

`results()` 可能等待所有结果，且会把结果复制到容器。大数据流应使用 `QFutureWatcher::resultReadyAt` 增量消费。

## 5. `map`：原地修改序列

```cpp
QList<QImage> images = loadImages();

QFuture<void> future = QtConcurrent::map(images, [](QImage &image) {
    image = image.scaled(320, 240,
                         Qt::KeepAspectRatio,
                         Qt::SmoothTransformation);
});
```

`map` 对容器元素原地调用函数。任务完成前不要在其他线程读取或修改同一容器，也不要改变容器长度。适合容器归当前任务独占的情况。

阻塞版本：

```cpp
QtConcurrent::blockingMap(images, normalizeImage);
```

阻塞 API 适合命令行工具或本就在工作线程的代码，不适合 GUI 事件处理器。

## 6. `mapped`：生成新结果序列

```cpp
QStringList files = {"a.png", "b.png", "c.png"};

QFuture<QImage> future = QtConcurrent::mapped(
    files,
    [](const QString &path) {
        return QImage(path).scaledToWidth(256);
    });
```

`mapped` 不修改输入，而是产生一个多结果 `QFuture<Output>`。输入容器在框架读取期间也必须保持有效；最稳妥的做法是传入独立副本或保证拥有者生命周期。

同步收集：

```cpp
QList<QImage> thumbnails =
    QtConcurrent::blockingMapped<QList<QImage>>(files, makeThumbnail);
```

## 7. `filter` 与 `filtered`

### 7.1 原地过滤

```cpp
QList<int> values = {1, 2, 3, 4, 5, 6};
QFuture<void> future = QtConcurrent::filter(values, [](int value) {
    return value % 2 == 0;
});
```

`filter` 保留谓词返回 `true` 的元素，并修改输入序列。

### 7.2 返回过滤结果

```cpp
QFuture<QString> future = QtConcurrent::filtered(
    files,
    [](const QString &path) {
        return path.endsWith(".json", Qt::CaseInsensitive);
    });
```

过滤函数应是纯函数或至少是线程安全函数。不要在每个谓词调用中更新同一个进度标签。

## 8. Map-Reduce 聚合

`mappedReduced` 先并行映射，再用 reduce 函数汇总结果：

```cpp
using CountMap = QHash<QString, int>;

QFuture<CountMap> future = QtConcurrent::mappedReduced<CountMap>(
    files,
    [](const QString &path) {
        return countWordsInFile(path);
    },
    [](CountMap &total, const CountMap &partial) {
        for (auto it = partial.cbegin(); it != partial.cend(); ++it)
            total[it.key()] += it.value();
    });
```

映射函数可并行，reduce 的执行策略由选项控制。若 reduce 依赖结果顺序，启用有序归约会牺牲部分吞吐；若操作满足结合律和交换律，使用无序归约更灵活。

## 9. Continuation：`then()`

```cpp
QFuture<int> resultFuture = QtConcurrent::run(loadValue)
    .then([](int value) {
        return value * 2;
    })
    .then([](int value) {
        qDebug() << "结果:" << value;
        return value;
    });
```

`then()` 把依赖关系写成链。continuation 在哪个线程执行取决于重载、上下文对象和调度策略。需要更新 UI 时，提供 GUI 上下文或显式队列回主线程：

```cpp
future.then(window, [window](int value) {
    window->showResult(value);
});
```

上下文对象销毁后，关联 continuation 不应再访问它。仍建议捕获 `QPointer` 处理复杂生命周期。

## 10. `QPromise`：主动报告结果与进度

### 10.1 Promise 模式 `run`

```cpp
QFuture<int> future = QtConcurrent::run(
    [](QPromise<int> &promise) {
        promise.setProgressRange(0, 100);

        for (int i = 0; i < 100; ++i) {
            if (promise.isCanceled())
                return;

            const int value = calculatePart(i);
            promise.addResult(value);
            promise.setProgressValue(i + 1);
        }
    });
```

Promise 模式允许多个结果、进度、暂停和取消协作。函数返回时 Promise 完成，不需要手工调用 `finish()`；若自行创建和管理 `QPromise`，则要遵守 `start()`/`finish()` 生命周期。

### 10.2 增量接收结果

```cpp
auto *watcher = new QFutureWatcher<int>(window);

QObject::connect(watcher, &QFutureWatcher<int>::resultReadyAt,
                 window, [watcher, window](int index) {
    window->appendValue(watcher->resultAt(index));
});

watcher->setFuture(future);
```

结果产生速度可能高于 UI 消费速度。可以使用 watcher 的 pending results 限制或在业务层批量合并更新，避免事件队列积压。

## 11. 进度显示

```cpp
QObject::connect(watcher, &QFutureWatcherBase::progressRangeChanged,
                 progressBar, &QProgressBar::setRange);
QObject::connect(watcher, &QFutureWatcherBase::progressValueChanged,
                 progressBar, &QProgressBar::setValue);
```

进度更新会被节流，不保证每一个数值都发出。业务逻辑不能依赖收到连续的 0、1、2……；信号只用于展示和观测。

## 12. 数据竞争示例

错误写法：

```cpp
int total = 0;
QtConcurrent::map(values, [&](int value) {
    total += value; // 多线程写同一个 int，存在数据竞争
});
```

正确方向是使用 `mappedReduced`、原子变量或互斥保护。对于求和，reduce 更符合语义，也更容易测试。

## 13. 选择 API

| 需求 | API |
| --- | --- |
| 执行一个函数并返回一个结果 | `QtConcurrent::run` |
| 原地修改每个元素 | `map` |
| 每个输入生成一个输出 | `mapped` |
| 原地保留符合条件的元素 | `filter` |
| 返回符合条件的元素 | `filtered` |
| 并行转换并聚合 | `mappedReduced` |
| 多结果、进度和协作取消 | `QPromise` |
| GUI 中监听 future | `QFutureWatcher` |

下一篇将集中讨论线程池选择、任务优先级、取消和暂停的真实语义、异常传播、嵌套并行、资源上限以及测试方法。
