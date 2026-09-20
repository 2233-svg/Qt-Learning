# Qt Core 基础：QObject 与对象树

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core  
> 头文件：`#include <QObject>`  
> 前置知识：C++ 对象生命周期、构造与析构、栈和堆、指针基础

## 1. QObject 为什么是 Qt 的根基

`QObject` 是 Qt 对象模型的基类。大量 Qt 类型直接或间接继承自它，例如：

- `QCoreApplication`、`QApplication`
- `QTimer`
- `QThread`
- `QNetworkAccessManager`
- `QAbstractItemModel`
- `QWidget`
- `QQuickItem`

继承 `QObject` 后，对象可以获得：

1. 父子对象树和自动销毁
2. 信号与槽
3. 事件和事件过滤器
4. 对象名称与运行时查找
5. 动态属性
6. 元对象信息
7. 国际化辅助能力
8. 线程归属

这几项能力并不是互相独立的。例如，线程归属决定排队信号在哪个线程执行；父子关系又限制对象是否可以移动到另一个线程。因此，生命周期是学习其他 Qt API 之前必须先掌握的基础。

## 2. 引入 Qt Core

### 2.1 CMake

```cmake
cmake_minimum_required(VERSION 3.21)
project(QObjectDemo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core)

qt_add_executable(QObjectDemo
    main.cpp
)

target_link_libraries(QObjectDemo PRIVATE Qt6::Core)
```

### 2.2 qmake

旧项目可能使用：

```qmake
QT += core
```

Qt 6 新项目优先使用 CMake。

## 3. QObject 与普通 C++ 值对象的区别

### 3.1 值对象表达“值”

`QString`、`QPoint`、`QSize` 等类型可以复制：

```cpp
QString first = QStringLiteral("Qt");
    QStringLiteral 是 Qt 框架中的一个宏，用于创建高效、安全的字符串字面量。它在编译                           时处理，避免运行时拷贝，提升性能，并且利于编译期检查，增强安全性。
QString second = first;
second.append('6');
```

此时 `first` 和 `second` 是两个独立的逻辑值。

### 3.2 QObject 表达“有身份的实体”

一个按钮、定时器或网络请求管理器具有唯一身份、连接关系、线程归属和生命周期，不适合通过复制产生“另一个相同对象”。因此 `QObject` 禁用了复制构造和复制赋值。

下面的代码不能编译：

```cpp
QObject first;
QObject second = first; // 错误：QObject 不可复制
```

Qt 容器中通常保存 `QObject` 指针，而不是保存对象本身：

```cpp
QList<QObject *> objects;
objects.append(new QObject);
```

但裸指针容器不会自动表达所有权。必须另外明确：对象由父对象销毁、由其他所有者销毁，还是由当前代码手动销毁。

## 4. 父子对象树的基本规则

构造 `QObject` 时可以传入父对象：

```cpp
QObject *parent = new QObject;
QObject *child = new QObject(parent);
```

此时建立双向可查询的关系：

```cpp
Q_ASSERT(child->parent() == parent);
Q_ASSERT(parent->children().contains(child));
    Q_ASSERT 是 Qt 提供的一个调试宏，用于在调试模式下验证条件是否为真。如果条件为假，程序会中断并输出错误信息，帮助开发者快速定位问题。
```

核心规则是：

> 父对象析构时，会析构它仍然拥有的所有子对象。

因此：

```cpp
delete parent; // child 也被删除
```

之后绝不能再次 `delete child`，因为 `child` 已经失效。

### 4.1 对象树可以有很多层

```cpp
QObject *applicationService = new QObject;
QObject *repository = new QObject(applicationService);
QObject *cache = new QObject(repository);

delete applicationService;
// repository 和 cache 都会被递归销毁
```

这是一棵所有权树：每个对象最多只有一个 `QObject` 父对象，但一个父对象可以有多个直接子对象。

### 4.2 子对象先单独销毁也安全

```cpp
QObject *parent = new QObject;
QObject *child = new QObject(parent);

delete child;
delete parent;
```

`child` 析构时会自动把自己从父对象的子对象列表中移除，所以父对象之后不会再次删除它。

### 4.3 `setParent()` 会改变所有权

```cpp
QObject *firstParent = new QObject;
QObject *secondParent = new QObject;
QObject *child = new QObject(firstParent);

child->setParent(secondParent);
```

调用后：

- `firstParent` 不再拥有 `child`。
- `secondParent` 开始拥有 `child`。
- 删除 `secondParent` 时会删除 `child`。

将父对象设为空指针会把对象从树上摘下：

```cpp
child->setParent(nullptr);
```

此时自动销毁责任也随之消失，必须为 `child` 安排新的所有者或主动删除它。

## 5. 堆对象：最常见也最容易理解的情况

下面是标准用法：

```cpp
auto *parent = new QObject;
auto *childA = new QObject(parent);
auto *childB = new QObject(parent);

delete parent;
```

不需要分别删除 `childA` 和 `childB`。这种模式特别适合生命周期明显从属于父对象的组件。

### 5.1 不要重复表达所有权

危险写法：

```cpp
auto parent = std::make_unique<QObject>();
auto child = std::make_unique<QObject>(parent.get());
```

这里父对象和 `unique_ptr` 都认为自己拥有 `child`：

- 若父对象先销毁，`child` 已被删除；随后 `unique_ptr` 再删除一次。
- 若 `child` 的 `unique_ptr` 先销毁，通常能够从父树移除，但代码的所有权表达仍然混乱。

更清晰的方案是只选一种所有权模型。

由对象树拥有：

```cpp
auto parent = std::make_unique<QObject>();
auto *child = new QObject(parent.get());
```

或者完全由智能指针拥有，不设置父对象：

```cpp
auto parent = std::make_unique<QObject>();
auto child = std::make_unique<QObject>();
```

并不是说智能指针不能与 Qt 一起使用，而是一个对象在同一时刻应有清晰且唯一的所有权策略。

## 6. 栈对象：构造顺序决定析构顺序

C++ 局部对象按照构造顺序的逆序析构。

### 6.1 安全写法：先构造父对象

```cpp
int main()
{
    QObject parent;
    QObject child(&parent);
}
```

构造顺序：

```text
parent → child
```

析构顺序：

```text
child → parent
```

`child` 先正常析构，并从 `parent` 的子对象列表移除；随后 `parent` 析构时已经找不到它，因此安全。

### 6.2 危险写法：后构造父对象，再修改 parent

```cpp
int main()
{
    QObject child;
    QObject parent;

    child.setParent(&parent); // 危险
}
```

构造顺序：

```text
child → parent
```

析构顺序：

```text
parent → child
```

`parent` 先析构，它会尝试 `delete` 自己的子对象。但 `child` 是栈对象，不能被当作堆对象删除；随后作用域结束还会再次析构 `child`。这会造成未定义行为。

结论：

> 栈上的父对象必须先于栈上的子对象构造；不要给一个更早构造的栈对象设置一个更晚构造的栈父对象。

### 6.3 推荐实践

- 生命周期复杂的 `QObject` 子类通常在堆上创建并交给父对象。
- 简单局部对象可以放在栈上，但要严格遵守构造和析构顺序。
- 不要为了少写一行 `delete` 而随意调用 `setParent()`。

## 7. QWidget 中的父对象关系

`QWidget` 间接继承 `QObject`，所以同样具有对象树。对控件而言，父控件通常同时表示：

- 对象所有权
- 窗口坐标关系
- 可见区域和裁剪关系
- 顶层窗口/子控件关系

```cpp
QWidget window;
auto *button = new QPushButton(QStringLiteral("确定"), &window);

window.show();
```

`window` 销毁时会销毁 `button`。

### 7.1 布局与控件所有权不是同一件事

```cpp
auto *layout = new QVBoxLayout(&window);
auto *button = new QPushButton(QStringLiteral("确定"));
layout->addWidget(button);
```

加入布局后，控件会成为布局所管理窗口的子控件。布局负责几何管理，父控件负责控件生命周期。不要把“布局管理位置”和“QObject 父对象管理生命周期”混为一谈。

### 7.2 QWidget 的显示层级变化

对 `QWidget` 调用 `raise()` 或 `lower()` 可能影响 `children()` 中相关控件的顺序。因此，业务逻辑不应依赖 `children()` 永远保持最初的插入顺序。

        在Qt中，*raise()*和*lower()*是两个用于控制窗口层级的重要函数。*raise()*函数将窗口提升到其父窗口堆栈的顶部，使窗口在所有重叠的同级窗口之上可见。相反，*lower()*函数将窗口降低到其父窗口堆栈的底部，使窗口在所有重叠的同级窗口之下不可见。

        In Qt, children() returns a list of a QObject's child objects, while findChild() and findChildren() allow type- and name-specific searches, supporting safe and recursive access to child widgets.

## 8. 对象命名与查找

### 8.1 `objectName`

每个 `QObject` 都有 `objectName` 属性：

```cpp
auto *button = new QPushButton(&window);
button->setObjectName(QStringLiteral("saveButton"));
```

它常用于：

- 调试对象树
- 自动连接槽
- 样式表选择器
- `findChild()` 查找
- 自动化测试

对象名称不是 C++ 变量名，也不保证全局唯一。通常只要求在明确的父对象范围内具有可辨识性。

### 8.2 查找一个子对象

```cpp
QPushButton *button =
    window.findChild<QPushButton *>(QStringLiteral("saveButton"));

if (button)
    button->setEnabled(false);
```

默认会递归查找后代。只查找直接子对象：

```cpp
auto *button = window.findChild<QPushButton *>(
    QStringLiteral("saveButton"),
    Qt::FindDirectChildrenOnly);
```

找不到时返回空指针，所以必须检查结果。

### 8.3 查找多个子对象

```cpp
const QList<QPushButton *> buttons =
    window.findChildren<QPushButton *>();

for (QPushButton *button : buttons)
    button->setEnabled(false);
```

也可以按名称或正则表达式筛选。

### 8.4 不要滥用运行时查找

如果一个对象是当前类长期依赖的核心组件，通常应保存一个明确成员指针，而不是每次用字符串查找：

```cpp
class Editor : public QWidget
{
public:
    Editor()
        : saveButton(new QPushButton(QStringLiteral("保存"), this))
    {
    }

private:
    QPushButton *saveButton;
};
```

`findChild()` 更适合动态表单、测试、插件、设计器生成界面或非核心的临时查找。

## 9. `delete` 和 `deleteLater()` 的区别

### 9.1 直接 `delete`

```cpp
delete object;
```

对象会立即析构。只有在以下条件明确时才适合：

- 当前调用位置允许对象立即消失。
- 不在对象处理自身事件或信号的危险调用栈中。
- 调用线程和对象线程归属符合要求。
- 后续代码不会继续访问它。

Qt 官方文档特别提醒：当对象正在处理事件，或对象属于另一个线程时，直接删除可能导致崩溃。

### 9.2 延迟删除

```cpp
object->deleteLater();
```

它不会在这一行立即析构对象，而是投递一个延迟删除事件。控制权返回对应事件循环后，Qt 才销毁对象。

典型场景：

```cpp
connect(reply, &QNetworkReply::finished,
        reply, &QObject::deleteLater);
```

网络响应发出 `finished` 时可能仍在内部调用过程中，延迟删除比在槽中立即 `delete reply` 更稳妥。

### 9.3 `deleteLater()` 依赖事件循环

必须理解以下边界：

- 在事件循环启动前调用：对象会在事件循环启动后删除。
- 主事件循环已经停止后调用：对象不会再由该事件循环删除。
- 对象所属线程没有运行事件循环：通常在线程结束时删除。
- 它不是“过几毫秒删除”，而是“回到合适的事件循环时删除”。

因此，下面的代码不能把 `deleteLater()` 当成立即清理：

```cpp
object->deleteLater();
Q_ASSERT(object == nullptr); // 错误：原始指针不会自动变为空
```

对象此刻通常仍存在，原始指针也不会在对象析构时自动清空。

## 10. `destroyed()` 信号与自动断开连接

对象即将销毁时会发出：

```cpp
void QObject::destroyed(QObject *object = nullptr);
```

示例：

```cpp
QObject *service = new QObject;

QObject::connect(service, &QObject::destroyed,
                 [](QObject *object) {
                     qDebug() << "destroyed:" << object;
                 });

delete service;
```

需要注意：

- 即使调用过 `blockSignals(true)`，`destroyed()` 仍会发出。
  - 在Qt框架中，*blockSignals*函数是一个用于控制对象信号是否发出的功能。当你需要暂时阻止信号触发相关的槽函数时，可以使用这个函数。*blockSignals*的原型是*bool QObject::blockSignals(bool block)*，其中*block*参数为*true*时，信号发射会被阻塞；为*false*时，则不会阻塞信号。
- 信号发出后，子对象将继续被销毁。
- 与该对象相关的普通信号槽连接会在对象销毁时自动解除。
- 自动断开连接只能防止连接继续调用，不能修复 lambda 捕获的其他悬空指针。

危险示例：

```cpp
QTimer *timer = new QTimer;
QObject *other = new QObject;

connect(timer, &QTimer::timeout, [other] {
    // other 若已销毁，这里会访问悬空指针
    other->setObjectName(QStringLiteral("updated"));
});
```

带上下文对象的连接更安全：

```cpp
connect(timer, &QTimer::timeout, other, [other] {
    other->setObjectName(QStringLiteral("updated"));
});
```

这里把 `other` 同时指定为连接的上下文对象。当 `other` 销毁时，连接会自动断开，lambda 不会再被调用。

信号与槽的完整规则会在下一份专题中展开。

## 11. 使用 QPointer 防止 QObject 悬空引用

`QPointer<T>` 是针对 `QObject` 子类的守卫指针。当目标对象被销毁时，它会自动变为空。

```cpp
#include <QPointer>

QPointer<QObject> guard = new QObject;
delete guard.data();

Q_ASSERT(guard.isNull());
```

实际用法：

```cpp
QPointer<QWidget> dialog = createDialog();
dialog->show();

// 某个异步操作完成后
if (dialog)
    dialog->setWindowTitle(QStringLiteral("完成"));
```

### 11.1 QPointer 不负责删除对象

`QPointer` 只观察对象，不拥有对象：

```cpp
QPointer<QObject> pointer = new QObject;
// pointer 离开作用域时，不会删除该 QObject
```

如果没有父对象或其他所有者，上述代码会泄漏。

### 11.2 什么时候需要 QPointer

适合：

- 对象由别处拥有，当前代码只观察它。
- 异步回调执行时，目标对象可能已经销毁。
- 缓存某个 UI 对象，但 UI 可以由用户关闭并删除。

不需要把所有成员指针都替换为 `QPointer`。如果父对象明确拥有子对象，且成员不会比所属父对象活得更久，普通指针往往已经足够清晰。

## 12. 对象树与线程归属

每个 `QObject` 都有线程归属：

```cpp
QThread *ownerThread = object->thread();
```

父子对象必须位于同一线程。由此产生几条重要规则：

1. 给对象设置另一个线程中的父对象会失败。
2. 父对象移动线程时，其子对象会一起移动。
3. 有父对象的对象不能单独 `moveToThread()`。
4. 成员变量不会自动成为子对象，除非构造时传入父对象或显式 `setParent()`。

```cpp
auto *worker = new Worker;
worker->moveToThread(thread); // worker 必须没有 parent
```

典型的工作对象清理方式：

```cpp
auto *thread = new QThread(this);
auto *worker = new Worker;

worker->moveToThread(thread);

connect(thread, &QThread::finished,
        worker, &QObject::deleteLater);

thread->start();
```

这里不能把 `worker` 的 parent 设为当前窗口，否则它无法移动到工作线程。

另一个常见误区是：`QThread` 对象本身通常属于创建它的线程，而不是它所管理的新线程。线程与异步专题会进一步解释这一点。

## 13. 调试对象树

### 13.1 设置有意义的对象名称

```cpp
window.setObjectName(QStringLiteral("mainWindow"));
button->setObjectName(QStringLiteral("saveButton"));
```

### 13.2 输出对象树

```cpp
window.dumpObjectTree();
```

它会把对象及其后代输出到调试日志，适合排查：

- 控件是否真的挂到预期父对象上
- 某个动态对象是否重复创建
- 对象层级是否异常
- 对象为何没有随预期父对象销毁

### 13.3 输出对象信息

```cpp
button->dumpObjectInfo();
```

它可以帮助查看对象名称和信号连接等调试信息。两者主要用于诊断，不应作为正式业务逻辑依赖。

## 14. 综合示例：观察对象树的创建与销毁

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QObject>
#include <QString>
#include <utility>

class TrackedObject final : public QObject
{
public:
    explicit TrackedObject(QString name, QObject *parent = nullptr)
        : QObject(parent)
        , name_(std::move(name))
    {
        setObjectName(name_);
        qDebug() << "construct" << name_;
    }

    ~TrackedObject() override
    {
        qDebug() << "destroy" << name_;
    }

private:
    QString name_;
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    auto *root = new TrackedObject(QStringLiteral("root"));
    auto *service = new TrackedObject(QStringLiteral("service"), root);
    new TrackedObject(QStringLiteral("cache"), service);
    new TrackedObject(QStringLiteral("logger"), root);

    root->dumpObjectTree();

    QObject::connect(root, &QObject::destroyed, &app, [&app] {
        qDebug() << "root destroyed";
        app.quit();
    });

    root->deleteLater();
    return app.exec();
}
```

可以观察到：

1. 四个对象按代码顺序构造。
2. `root` 形成一棵多层对象树。
3. `deleteLater()` 等事件循环开始处理后再删除 `root`。
4. 删除 `root` 会递归销毁 `service`、`cache` 和 `logger`。
5. 不需要逐个删除子对象。

## 15. 常见错误与修正

### 15.1 父对象删除后继续使用子对象

错误：

```cpp
QObject *parent = new QObject;
QObject *child = new QObject(parent);

delete parent;
child->setObjectName(QStringLiteral("invalid")); // 悬空指针
```

修正：删除父对象后不再使用子指针；若只是观察外部对象，可使用 `QPointer`。

### 15.2 手动删除已经由父对象删除的子对象

错误：

```cpp
delete parent;
delete child; // 重复删除
```

修正：明确父对象拥有子对象后，只删除父对象。

### 15.3 从对象树摘下后忘记处理

```cpp
child->setParent(nullptr);
```

此后父对象不再负责它。修正方式是设置新父对象、交给明确的智能指针，或在适当时机删除。

### 15.4 认为 deleteLater 会立即把指针清空

原始指针不会自动清空，延迟删除也不是立即析构。需要观察目标是否仍存在时使用 `QPointer`。

### 15.5 把布局关系误认为所有权关系

布局负责计算位置，`QObject` parent 负责生命周期。排查时分别检查 `layout()`、`parentWidget()` 和 `parent()`。

### 15.6 为了查找对象，到处依赖 objectName 字符串

核心依赖优先保存类型明确的成员指针。名称查找适合动态和弱耦合场景，不应代替清晰的类结构。

### 15.7 给工作线程对象设置 GUI 父对象

有 parent 的对象无法单独移动到工作线程。工作对象先保持无父对象，在线程结束时通过 `deleteLater()` 清理。

## 16. QObject 生命周期 API 速查

| API                 | 作用          | 关键注意点         |
| ------------------- | ----------- | ------------- |
| `QObject(parent)`   | 创建时加入对象树    | parent 将拥有该对象 |
| `parent()`          | 返回直接父对象     | 可能为空          |
| `children()`        | 返回直接子对象列表   | 不包含更深后代       |
| `setParent()`       | 改变所有权树      | 受线程归属限制       |
| `deleteLater()`     | 通过事件循环延迟删除  | 依赖所属线程的事件循环   |
| `destroyed()`       | 对象销毁前发出的信号  | 即使阻塞信号也会发出    |
| `objectName()`      | 读取对象名称      | 名称不保证全局唯一     |
| `setObjectName()`   | 设置对象名称      | 调试、查找和样式常用    |
| `findChild<T>()`    | 查找一个匹配后代    | 找不到返回空指针      |
| `findChildren<T>()` | 查找所有匹配后代    | 默认递归查找        |
| `dumpObjectTree()`  | 输出对象树       | 主要用于调试        |
| `dumpObjectInfo()`  | 输出对象信息      | 主要用于调试        |
| `thread()`          | 查询线程归属      | 不代表当前正在执行的线程  |
| `moveToThread()`    | 改变对象及子树线程归属 | 有父对象时不能移动     |

## 17. 设计时的判断顺序

创建一个 `QObject` 子类对象前，依次回答：

1. 谁拥有它？
2. 谁负责触发销毁？
3. 它是否需要比当前作用域活得更久？
4. 它是否属于某个明确的父对象？
5. 它在哪个线程接收事件和排队信号？
6. 是否存在对象销毁后仍可能执行的异步回调？
7. 观察它的代码是否需要 `QPointer`？

如果第一问回答不清楚，后面的代码通常很容易出现泄漏、重复删除或悬空访问。

## 18. 延伸知识

### 18.1 QQuickItem 有两种父子关系

Qt Quick 中需要区分：

- `QObject` parent：对象生命周期树
- `QQuickItem::parentItem`：视觉场景树

二者经常相关，但概念并不相同。分析 QML/Quick 对象时不能只看 `QObject::parent()`。

### 18.2 模型索引等类型不是 QObject

不要因为某个类型以 `Q` 开头，就认为它一定继承 `QObject`。`QString`、`QVariant`、`QModelIndex` 等都是值类型，生命周期规则完全不同。

### 18.3 RAII 仍然重要

Qt 对象树没有替代 C++ RAII。文件句柄、锁、容器、值对象和非 `QObject` 资源仍应使用栈对象和智能指针。对象树只是特别适合表达 `QObject` 的层级所有权。

## 19. 自测题

1. 为什么 `QObject` 不提供复制构造？
2. 删除父对象后，保存的子对象裸指针处于什么状态？
3. 为什么先构造栈子对象、后构造栈父对象，再调用 `setParent()` 是危险的？
4. `deleteLater()` 什么时候真正删除对象？
5. `QPointer` 是否拥有并删除目标对象？
6. 为什么有父对象的 worker 不能直接移动到另一个线程？
7. 布局拥有控件，还是父窗口拥有控件？
8. `findChild()` 默认只查直接子对象还是递归查找？

### 参考答案

1. `QObject` 表达具有身份、连接、线程归属和生命周期的实体，复制语义不明确。
2. 它成为悬空指针，除非使用 `QPointer` 等机制观察生命周期。
3. 父对象先析构时会试图删除仍在栈上的子对象，之后栈展开还会再次析构该子对象。
4. 控制权返回对象所属线程的合适事件循环并处理延迟删除事件时:
   1. *deleteLater()* 是一种 **异步操作**，不会立即销毁对象，而是将销毁任务放入事件队列中，等到当前事件和相关事件处理完成后再销毁对象。
   2. 适用场景：
      - 对象正在处理事件或信号槽时，使用 *deleteLater()* 可以避免在事件未处理完毕时销毁对象，从而防止程序崩溃。
      
      - 依赖事件循环的场景。如果没有事件循环，*deleteLater()* 可能不会执行。
      
      - 如果对象正在处理事件或信号槽，推荐使用 *deleteLater()*，以确保程序的稳定性和安全性。
5. 不拥有；它只是目标销毁后自动清空的守卫指针。
6. 父子对象必须在同一线程，对象有 parent 时不能单独移动。
7. 布局管理几何位置，父窗口通过 QObject 父子关系管理控件生命周期。
8. 默认递归查找后代；可用 `Qt::FindDirectChildrenOnly` 限制为直接子对象。

---

## 总结

`QObject` 对象树是一套层级所有权机制：父对象销毁时递归销毁子对象，子对象提前销毁时会自动退出父对象列表。它能大幅简化生命周期管理，但前提是所有权必须清晰。尤其要记住栈对象的构造顺序、`deleteLater()` 对事件循环的依赖、原始指针不会自动清空、父子对象必须处于同一线程，以及布局关系不等于对象所有权。掌握这些规则后，信号与槽、事件系统、线程和 GUI 对象的行为才会真正连成一个整体。
