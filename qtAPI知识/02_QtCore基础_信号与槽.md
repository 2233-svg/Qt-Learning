# Qt Core 基础：信号与槽

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core  
> 前置知识：`QObject`、对象树、C++ 成员函数、lambda、线程基础

## 1. 信号与槽解决什么问题

对象之间经常需要通信。例如：

- 按钮被点击后关闭窗口。
- 下载完成后刷新界面。
- 数据发生变化后通知多个观察者。
- 工作线程计算完成后把结果送回 GUI 线程。

传统回调通常要求调用方保存函数指针或函数对象。Qt 的信号与槽在此基础上提供了：

- 编译期类型检查
- 一对一、一对多和多对一连接
- 接收者销毁后的自动断开
- 跨线程排队调用
- 与元对象系统、属性系统和 QML 的集成

基本关系是：

```text
发送者状态变化
      ↓ emit
     信号
      ↓ connect
槽函数 / 普通成员函数 / lambda / 另一个信号
```

发送者只负责表达“发生了什么”，不需要知道有多少接收者，也不需要知道接收者如何处理。这种低耦合是信号与槽最重要的设计价值。

## 2. 最小示例

```cpp
QPushButton *button = new QPushButton(QStringLiteral("关闭"), &window);

QObject::connect(button, &QPushButton::clicked,
                 &window, &QWidget::close);
```

四个参数分别表示：

1. `button`：发送者
2. `&QPushButton::clicked`：信号
3. `&window`：接收者
4. `&QWidget::close`：收到信号后调用的函数

当按钮发出 `clicked` 时，Qt 调用 `window.close()`。按钮并不知道窗口的存在，窗口也不需要主动轮询按钮状态。

## 3. 自定义信号与槽

### 3.1 类声明

```cpp
#pragma once

#include <QObject>

class Counter final : public QObject
{
    Q_OBJECT
    //在Qt中，Q_OBJECT宏是启用元对象功能的关键，如动态属性、信号和槽。这个宏通常用于声明自己的信号和槽或使用Qt元对象系统提供的其他服务的类中。
    只有继承了QObject类的类，才具有信号槽的能力。因此，为了使用信号槽，必须继承QObject。凡是QObject类（不管是直接子类还是间接子类），都应该在第一行代码写上Q_OBJECT。这个宏的展开将为我们的类提供信号槽机制、国际化机制以及Qt提供的不基于C++ RTTI的反射能力。

public:
    explicit Counter(QObject *parent = nullptr);

    int value() const;

public slots:
    void setValue(int value);

signals:
    void valueChanged(int value);

private:
    int value_ = 0;
};
```

### 3.2 类实现

```cpp
#include "counter.h"

Counter::Counter(QObject *parent)
    : QObject(parent)
{
}

int Counter::value() const
{
    return value_;
}

void Counter::setValue(int value)
{
    if (value_ == value)
        return;

    value_ = value;
    emit valueChanged(value_);
}
```

### 3.3 建立连接

```cpp
Counter first;
Counter second;

QObject::connect(&first, &Counter::valueChanged,
                 &second, &Counter::setValue);

first.setValue(12);

Q_ASSERT(first.value() == 12);
Q_ASSERT(second.value() == 12);
```

`first` 改变后发出信号，`second` 的槽接收新值。

## 4. Q_OBJECT、moc 与构建系统

声明自定义信号、槽或 Qt 属性的 `QObject` 子类需要 `Q_OBJECT`：

```cpp
class Service : public QObject
{
    Q_OBJECT
};
```

Qt 的元对象编译器 `moc` 会读取这个类声明，并生成信号分发、运行时类型信息等代码。信号只声明，不由开发者在 `.cpp` 中手动实现。

### 4.1 CMake 配置

使用 Qt 提供的目标创建命令：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)

qt_add_executable(SignalDemo
    main.cpp
    counter.cpp
    counter.h
)

target_link_libraries(SignalDemo PRIVATE Qt6::Core)
```

也可以显式启用：

```cmake
set(CMAKE_AUTOMOC ON)
```

如果出现类似下面的链接错误：

```text
undefined reference to vtable for Counter
unresolved external symbol Counter::staticMetaObject
```

优先检查：

1. 类是否写了 `Q_OBJECT`。
2. 含 `Q_OBJECT` 的头文件是否加入目标源文件列表。
3. `AUTOMOC` 是否启用。
4. 修改宏后是否重新运行 CMake 配置。

### 4.2 Q_OBJECT 会切换访问级别

`Q_OBJECT` 宏展开后会进入 private 区域，所以它后面的公共成员仍应明确写 `public:`。

## 5. signal 和 slot 各自是什么

### 5.1 信号表达已经发生的事实

推荐命名：

```cpp
signals:
    void connected();
    void valueChanged(int value);
    void requestFailed(QString message);
```

信号通常使用过去式或 `Changed`，表达状态已经发生变化。不要把需要返回结果的命令设计成信号。

信号在类声明中出现，但不写普通 C++ 实现：

```cpp
emit valueChanged(value_);
```

`emit` 是为了增强可读性的 Qt 宏，不改变访问控制。技术上其他代码能够调用信号函数，但良好设计应只让定义该信号的类及其派生类发出它。

### 5.2 槽本质上仍是函数

槽可以像普通函数一样直接调用：

```cpp
counter.setValue(42);
```

现代函数指针连接语法通常不要求接收函数写在 `slots:` 区域。普通成员函数也可以作为接收端：

```cpp
public:
    void setValue(int value);
```

`public slots:` 的意义主要在于把函数注册为元对象可识别的槽，以支持字符串调用、设计器、旧语法和某些动态调用场景。

### 5.3 访问级别

槽可以是 public、protected 或 private。即使槽是 private，已经建立的信号连接仍可调用它。访问控制检查发生在建立连接或直接调用的 C++ 表达式处，而不是信号发出时再次检查。

## 6. 为什么 setter 要先判断值是否改变

推荐写法：

```cpp
void Counter::setValue(int value)
{
    if (value_ == value)
        return;

    value_ = value;
    emit valueChanged(value_);
}
```

原因有三点：

1. 避免没有实际变化时产生无意义通知。
2. 降低界面刷新、网络同步或数据库写入成本。
3. 防止双向连接形成无限递归。

```cpp
connect(&first, &Counter::valueChanged,
        &second, &Counter::setValue);
connect(&second, &Counter::valueChanged,
        &first, &Counter::setValue);
```

如果 `setValue()` 每次都无条件发信号，两个对象会不断互相调用。

## 7. 参数兼容规则

信号参数必须能够传给接收函数。槽可以忽略信号末尾的多余参数。

例如：

```cpp
signals:
    void progressChanged(int value, QString message);

private slots:
    void updateProgress(int value);
```

该连接合法，因为槽使用了信号的第一个参数并忽略第二个参数。

反过来不合法：槽不能要求信号没有提供的参数。

现代语法会在编译期检查大部分不兼容问题：

```cpp
connect(sender, &Sender::progressChanged,
        receiver, &Receiver::updateProgress);
```

旧式 `SIGNAL()` / `SLOT()` 字符串语法通常只能在运行时发现拼写和签名错误，所以新代码应优先使用函数指针语法。

## 8. 连接到 lambda

### 8.1 最简单的 lambda

```cpp
connect(button, &QPushButton::clicked, [] {
    qDebug() << "clicked";
});
```

这种无上下文连接只有在 lambda 不捕获外部对象，或其生命周期绝对明确时才适合。

### 8.2 推荐提供上下文对象

```cpp
connect(button, &QPushButton::clicked,
        this, [this] {
            updateState();
        });
```

`this` 是上下文对象。当发送者或上下文对象销毁时，连接会自动断开。它还决定排队连接在哪个线程执行。

### 8.3 危险捕获

```cpp
QWidget *panel = createPanel();

connect(timer, &QTimer::timeout, [panel] {
    panel->update(); // panel 可能已经销毁
});
```

更安全的写法是将 `panel` 作为上下文：

```cpp
connect(timer, &QTimer::timeout,
        panel, [panel] {
            panel->update();
        });
```

如果 lambda 观察的是另一个独立对象，可以捕获 `QPointer<T>`：

```cpp
QPointer<QWidget> guardedPanel = panel;

connect(timer, &QTimer::timeout,
        this, [guardedPanel] {
            if (guardedPanel)
                guardedPanel->update();
        });
```

关键问题不是“lambda 能不能捕获指针”，而是“回调执行时捕获对象是否一定还活着”。

## 9. 一个信号可以连接多少接收者

Qt 支持：

- 一个信号连接多个槽
- 多个信号连接一个槽
- 一个信号连接另一个信号
- 同一连接重复建立多次

```cpp
connect(source, &Source::ready, logger, &Logger::recordReady);
connect(source, &Source::ready, view, &View::refresh);
```

对于直接调用，同一个信号上的槽通常按连接建立顺序依次执行。但业务设计不应依赖多个接收者互相修改共享状态的精确顺序；如果顺序是业务约束，应在一个明确的协调函数中组织步骤。

### 9.1 重复连接

以下代码会建立两条连接：

```cpp
connect(source, &Source::ready, view, &View::refresh);
connect(source, &Source::ready, view, &View::refresh);
```

发出一次信号，`refresh()` 会调用两次。

可以使用 `Qt::UniqueConnection` 防止相同的成员函数连接重复建立：

```cpp
const QMetaObject::Connection connection =
    connect(source, &Source::ready,
            view, &View::refresh,
            Qt::UniqueConnection);
```

重复时连接失败。`Qt::UniqueConnection` 不适合依赖 lambda/仿函数身份去重，因为它们不能像成员函数连接那样比较。

## 10. 重载信号与重载槽

如果信号名有多个重载，编译器不知道你选择哪个：

```cpp
connect(comboBox, &QComboBox::currentIndexChanged,
        receiver, &Receiver::handleChange); // 可能产生歧义
```

使用 `qOverload` 指定参数：

```cpp
connect(comboBox,
        qOverload<int>(&QComboBox::currentIndexChanged),
        receiver,
        &Receiver::handleIndexChanged);
```

对于 const 重载可使用 `qConstOverload`，非 const 重载可使用 `qNonConstOverload`。

也可以显式转换函数指针，但可读性通常较差：

```cpp
using Signal = void (QComboBox::*)(int);

connect(comboBox,
        static_cast<Signal>(&QComboBox::currentIndexChanged),
        receiver,
        &Receiver::handleIndexChanged);
```

## 11. Qt::ConnectionType：调用发生在何时、何处

这是信号与槽最关键的进阶部分。

### 11.1 `Qt::AutoConnection`

默认类型。

- 发出信号时，接收者与当前发出信号的线程相同：行为类似直接连接。
- 接收者属于另一个线程：行为类似排队连接。

判断依据是信号发出时的执行线程与接收对象线程归属，而不能只看发送对象最初在哪个线程创建。

```cpp
connect(sender, &Sender::resultReady,
        receiver, &Receiver::handleResult);
```

大多数普通连接从默认类型开始最合理。

### 11.2 `Qt::DirectConnection`

信号发出时立即调用槽，槽在**发出信号的当前线程**执行：

```cpp
connect(sender, &Sender::ready,
        receiver, &Receiver::handleReady,
        Qt::DirectConnection);
```

它类似普通函数调用。跨线程强制直接连接可能让槽在错误线程访问接收对象，尤其不能由工作线程直接操作 GUI 控件。

### 11.3 `Qt::QueuedConnection`

Qt 把调用封装成事件，投递给接收对象所属线程；槽稍后由该线程的事件循环执行：

```cpp
connect(worker, &Worker::resultReady,
        view, &View::showResult,
        Qt::QueuedConnection);
```

特点：

- `emit` 后发送线程立即继续。
- 槽不会在当前调用栈立即执行。
- 接收线程必须能够处理事件。
- 参数需要复制并保存到队列中。

### 11.4 `Qt::BlockingQueuedConnection`

与排队连接类似，但发送线程会阻塞，直到接收线程执行完槽。

```cpp
Qt::BlockingQueuedConnection
```

同一线程中使用会死锁。跨线程使用也容易形成锁顺序问题，应只用于经过严格设计的同步边界，不要把它当成“等待异步操作完成”的通用工具。

### 11.5 `Qt::UniqueConnection`

这是可与基本连接类型组合的标志，用于避免完全相同的成员函数连接重复建立。

```cpp
Qt::AutoConnection | Qt::UniqueConnection
```

### 11.6 `Qt::SingleShotConnection`

Qt 6 提供的一次性连接标志。信号触发一次后自动断开：

```cpp
connect(source, &Source::ready,
        receiver, &Receiver::initialize,
        Qt::SingleShotConnection);
```

也可以与基本连接类型组合。它比在槽内部保存连接句柄并手动断开更直接。

## 12. 跨线程连接中的参数

排队连接需要复制参数并将其保存到事件中，因此参数类型必须被 Qt 元类型系统识别。

Qt 内置类型通常已经注册。自定义类型可以这样声明：

```cpp
struct Result
{
    int code;
    QString message;
};

Q_DECLARE_METATYPE(Result)
```

需要按名称进行运行时排队连接等场景时，还可能需要在建立连接前注册：

```cpp
qRegisterMetaType<Result>("Result");
```

设计跨线程信号参数时，优先使用：

- 可复制或可移动的值类型
- 不依赖发送线程局部状态的数据
- 清晰表达所有权的数据结构

不要把指向发送线程临时对象的裸指针作为异步结果传递给另一个线程。

## 13. 连接生命周期与自动断开

Qt 会在以下情况自动移除连接：

- 发送者销毁
- 接收者销毁
- lambda 连接的上下文对象销毁

因此普通成员函数连接通常不需要在析构函数里逐条断开。

但要注意：

- 无上下文 lambda 捕获的对象不会被 Qt 自动保护。
- 手动 `disconnect()` 后，已经进入事件队列的调用仍可能被执行。
- 断开连接不等于取消相关业务任务。

## 14. 保存并断开特定连接

`connect()` 返回 `QMetaObject::Connection`：

```cpp
QMetaObject::Connection connection =
    connect(timer, &QTimer::timeout,
            this, &Controller::poll);
```

稍后精确断开：

```cpp
QObject::disconnect(connection);
```

这对 lambda 特别重要，因为无法通过比较两个 lambda 表达式来定位原连接。

检查连接是否有效：

```cpp
if (connection) {
    // connect 创建过一个有效连接
}
```

连接句柄本身不拥有发送者或接收者。保存一个句柄不会延长对象生命周期。

## 15. 临时阻止信号

### 15.1 `blockSignals()`

```cpp
const bool wasBlocked = object->blockSignals(true);
updateSeveralProperties();
object->blockSignals(wasBlocked);
```

手动恢复容易在异常或提前返回时遗漏。

### 15.2 `QSignalBlocker`

推荐 RAII 写法：

```cpp
#include <QSignalBlocker>

{
    const QSignalBlocker blocker(spinBox);
    spinBox->setValue(42);
}
// 离开作用域后自动恢复原来的阻塞状态
```

信号阻塞期间发出的信号不会被缓存并在稍后补发。`QObject::destroyed()` 即使在信号被阻塞时仍会发出。

使用场景包括初始化表单、同步多个控件、避免程序性赋值触发业务提交。不要长期阻塞对象信号来掩盖状态设计问题。

## 16. 属性通知信号

Qt 属性通常配套一个 notify 信号：

```cpp
class Temperature : public QObject
{
    Q_OBJECT
    Q_PROPERTY(double value READ value WRITE setValue NOTIFY valueChanged)
    //Qt属性系统提供了一种强大的机制来定义类的属性，这些属性可以通过Qt的元对象系统进行访问和操作。使用Q_PROPERTY宏，开发者可以声明类的属性，并将其与类中的成员变量或成员函数关联起来，从而实现属性的自动化处理，如绑定、序列化、动态属性设置等。        
    Q_PROPERTY宏用于在Qt中声明一个类的属性。要声明属性，类需要继承自QObject，并在类定义中使用Q_PROPERTY宏。以下是Q_PROPERTY宏的基本语法：
    Q_PROPERTY(Type name READ readFunction [WRITE writeFunction] [NOTIFY notifySignal])
Type 是属性的数据类型。
name 是属性的名称。
READ 是用于读取属性值的成员函数。
WRITE 是可选的，用于写入属性值的成员函数。
NOTIFY 是可选的，当属性值改变时发出的信号。

public:
    double value() const { return value_; }

    void setValue(double value)
    {
        if (qFuzzyCompare(value_, value))
            return;

        value_ = value;
        emit valueChanged();
    }

signals:
    void valueChanged();

private:
    double value_ = 0.0;
};
```

通知信号应只在属性值真正变化时发出。它可以不带参数，让接收者重新读取属性；也可以携带新值，减少一次读取。团队应保持一致风格。

## 17. 完整 Core 示例：定时产生读数

### 17.1 `sensor.h`

```cpp
#pragma once

#include <QObject>
#include <QTimer>

class Sensor final : public QObject
{
    Q_OBJECT

public:
    explicit Sensor(QObject *parent = nullptr)
        : QObject(parent)
    {
        connect(&timer_, &QTimer::timeout,
                this, &Sensor::measure);
    }

    void start()
    {
        timer_.start(500);
    }

signals:
    void valueChanged(int value);

private:
    void measure()
    {
        value_ += 5;
        emit valueChanged(value_);

        if (value_ >= 20)
            timer_.stop();
    }

    QTimer timer_;
    int value_ = 0;
};
```

`timer_` 是值成员，与 `Sensor` 生命周期完全一致，因此无需额外 parent。

### 17.2 `main.cpp`

```cpp
#include "sensor.h"

#include <QCoreApplication>
#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    Sensor sensor;

    QObject::connect(&sensor, &Sensor::valueChanged,
                     &app, [](int value) {
        qDebug() << "value:" << value;

        if (value >= 20)
            QCoreApplication::quit();
    });

    sensor.start();
    return app.exec();
}
```

数据流：

```text
QTimer::timeout
      ↓
Sensor::measure
      ↓ emit valueChanged
main 中的 lambda
      ↓
输出读数并在达到 20 时退出
```

## 18. 设计信号时的原则

### 18.1 描述事实，不发命令

更推荐：

```cpp
emit documentSaved(path);
```

不太推荐：

```cpp
emit pleaseRefreshEveryViewNow();
```

信号应该表达发送者领域内发生的事实，让接收者自行决定反应。

### 18.2 参数保持通用、稳定

过度特殊的参数类型会限制可连接性。公开库 API 中尤其需要避免暴露不必要的内部实现类型。

### 18.3 不依赖接收者数量

发送者不应通过“有没有人连接”来决定核心状态是否更新。`receivers()` 和 `isSignalConnected()` 会破坏模块独立性，仅适合极少数昂贵数据生成优化，并且要理解并发状态可能立即变化。

### 18.4 不用信号请求同步返回值

一个信号可能有零个、一个或多个接收者，也可能排队执行，因此它不适合作为普通的请求-返回函数。需要同步查询时使用明确接口，需要异步结果时使用请求函数加结果信号。

## 19. 常见错误与排查

### 19.1 信号没有触发槽

依次检查：

1. `connect()` 是否真的执行。
2. 连接返回值是否有效。
3. 发送者是否真的执行到 `emit`。
4. 发送者、接收者或上下文是否已经销毁。
5. 重载信号是否选择正确。
6. 排队连接的接收线程是否运行事件循环。
7. 自定义参数类型是否已注册。

### 19.2 槽被调用多次

常见原因是初始化函数重复执行并重复 `connect()`。应修复连接建立时机，而不是在槽里添加布尔变量掩盖问题。必要时使用 `Qt::UniqueConnection`。

### 19.3 lambda 偶发崩溃

重点检查捕获的裸指针和引用。发送者活着并不意味着捕获对象也活着；提供上下文对象或使用 `QPointer`。

### 19.4 跨线程后 GUI 崩溃

检查是否强制使用 `DirectConnection`，导致工作线程执行 GUI 槽。默认 `AutoConnection` 或明确 `QueuedConnection` 通常更合适。

### 19.5 BlockingQueuedConnection 卡死

同线程使用一定会死锁。跨线程时还要检查接收线程是否反向等待发送线程持有的锁。

### 19.6 修改值后形成递归

setter 应先比较新旧值；复杂双向绑定还应明确数据的唯一真实来源。

## 20. API 速查

| API/关键字                        | 作用          | 注意点             |
| ------------------------------ | ----------- | --------------- |
| `signals:`                     | 声明信号        | 信号不写普通实现        |
| `slots:`                       | 声明元对象槽      | 普通函数也可作为现代连接接收端 |
| `emit`                         | 发出信号        | 主要增强可读性         |
| `QObject::connect()`           | 建立连接        | 推荐函数指针语法        |
| `QObject::disconnect()`        | 断开连接        | 已排队调用仍可能到达      |
| `QMetaObject::Connection`      | 表示一条连接      | 不拥有两端对象         |
| `Qt::AutoConnection`           | 自动选择直接或排队   | 默认选择            |
| `Qt::DirectConnection`         | 当前线程立即调用    | 跨线程访问接收者很危险     |
| `Qt::QueuedConnection`         | 投递到接收线程事件循环 | 参数需要可复制和元类型信息   |
| `Qt::BlockingQueuedConnection` | 阻塞等待远端槽完成   | 同线程必然死锁         |
| `Qt::UniqueConnection`         | 防止重复成员函数连接  | 不适合 lambda 去重   |
| `Qt::SingleShotConnection`     | 调用一次后自动断开   | Qt 6 可用         |
| `QSignalBlocker`               | 作用域内阻塞信号    | 自动恢复原状态         |
| `qOverload`                    | 消除重载函数歧义    | 模板参数写信号参数类型     |
| `Q_DECLARE_METATYPE`           | 声明自定义元类型    | 跨线程排队参数常用       |
| `qRegisterMetaType`            | 运行时注册元类型    | 需在连接或调用前完成      |

## 21. 自测题

1. 信号与普通回调相比，核心优势是什么？
2. 为什么 setter 应该先比较新旧值？
3. 普通成员函数能否作为槽的接收端？
4. 为什么连接 lambda 时推荐提供上下文对象？
5. `AutoConnection` 如何决定直接调用还是排队调用？
6. `DirectConnection` 跨线程使用有什么风险？
7. 为什么 `BlockingQueuedConnection` 不能在同线程使用？
8. 为什么排队连接的自定义参数需要元类型信息？
9. 保存 `QMetaObject::Connection` 有什么用途？
10. `QSignalBlocker` 离开作用域后会发生什么？

### 参考答案

1. 类型安全、低耦合、自动管理连接生命周期，并支持跨线程排队调用。
2. 避免无意义通知、额外开销和双向连接递归。
3. 可以；现代函数指针语法不要求它必须声明在 `slots:` 下。
4. 上下文销毁后连接自动断开，并为排队调用提供接收线程归属。
5. 比较发出信号的当前线程与接收对象所属线程。
6. 槽会在发出信号的线程执行，可能在错误线程访问接收对象或 GUI。
7. 发送线程等待槽完成，而槽又必须由同一个已阻塞线程执行，因此死锁。
8. Qt 需要复制参数并保存到事件队列中。
9. 可以精确断开特定连接，尤其适用于 lambda。
10. 自动恢复对象原先的信号阻塞状态。

---

## 总结

信号与槽不是简单的“按钮点击回调”，而是 Qt 对象之间的类型安全通信机制。基础阶段要掌握声明、发出、函数指针连接和 lambda；进阶阶段必须理解上下文对象、连接生命周期、重复连接和重载消歧；跨线程时则必须真正理解 `AutoConnection`、直接调用、排队调用、事件循环和参数复制。写出稳定连接的关键，是同时回答三个问题：调用何时发生、在哪个线程发生、调用发生时相关对象是否仍然存活。
