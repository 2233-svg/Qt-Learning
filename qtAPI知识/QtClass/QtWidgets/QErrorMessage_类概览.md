# Qt QErrorMessage 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QErrorMessage>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QDialog -> QErrorMessage`  
> 定位：可抑制重复消息的错误对话框

## 1. QErrorMessage 解决什么问题

`QErrorMessage` 用来集中显示错误或警告信息，尤其适合那些可能在短时间内重复出现的消息。它会让用户有机会选择“不再显示这条消息”，从而避免同一个错误不断弹窗打断工作。

它适合处理：

- 文件读取失败；
- 配置解析错误；
- 外部设备或网络操作的错误提示；
- 调试阶段需要把 Qt 消息显示成对话框的场景。

它不是日志系统，也不是异常处理器。它负责的是“把错误以用户可读的对话框展示出来，并记住用户对重复消息的选择”。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 显示一条错误

```cpp
#include <QApplication>
#include <QErrorMessage>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QErrorMessage errors;
    errors.showMessage("配置文件读取失败，请检查文件权限。");

    return app.exec();
}
```

如果错误来自某个窗口，通常把那个窗口作为父对象：

```cpp
auto *errors = new QErrorMessage(mainWindow);
errors->showMessage("无法打开项目文件。");
```

## 3. 核心使用模型

### 3.1 `showMessage()` 是非阻塞的显示入口

`showMessage()` 会显示错误对话框，但调用本身不是让当前函数停在那里等待用户选择。它适合从信号槽、异步任务完成回调和错误处理路径里调用。

如果业务逻辑必须根据用户选择决定下一步，不要把 `showMessage()` 当成同步返回值接口，而应设计自己的确认对话框或监听对话框完成流程。

### 3.2 type 用来区分“同类消息”

两参数版本：

```cpp
errors.showMessage(message, "network");
```

第二个参数是消息类型标识。它可以帮助 `QErrorMessage` 区分重复消息类别，并让“不再显示”这类选择有稳定的归类依据。实际使用时应给同一类错误使用稳定的 type，而不是每次拼一个随机字符串。

### 3.3 用户可以抑制重复消息

同一消息或同一类型的消息被用户选择忽略后，后续再次显示可能会被抑制。这正是它和普通 `QMessageBox` 的主要区别之一。

因此它适合“可能反复发生、但用户不需要每次都被打断”的错误；必须每次确认的关键操作，不应依赖它的抑制行为。

### 3.4 `qtHandler()` 是应用级错误消息处理器入口

`qtHandler()` 返回 Qt 可复用的错误消息处理对象。它适合在需要把 Qt 的消息处理接到 `QErrorMessage` 时使用，但不要把它和应用自己的业务错误对象混为一谈。

## 4. 适合用在哪里

- 桌面工具中的用户可见错误；
- 不希望重复弹窗的后台操作提示；
- 原型和调试阶段的 Qt 消息可视化；
- 需要按消息类别记住用户抑制选择的场景。

如果消息很多、需要检索和持久化，应使用日志面板或日志系统；如果要让用户确认危险操作，应使用 `QMessageBox`。

## 5. 常见误区

### 5.1 把它当成日志窗口

它只适合展示错误对话框，不提供日志列表、筛选和持久化。

### 5.2 每次都创建一个新的 QErrorMessage

这样会失去重复消息抑制的连续状态。通常应在应用或窗口范围内复用一个实例。

### 5.3 type 每次都变化

type 应该稳定地代表错误类别，否则抑制规则很难达到预期。

### 5.4 在工作线程直接调用

它是 QWidget/QDialog，必须在 GUI 线程创建和使用。工作线程应通过信号把错误传回主线程。

### 5.5 把 `showMessage()` 当同步函数

它负责安排显示，不返回用户选择。需要同步决策时要选择合适的模态对话框方案。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QErrorMessage(QWidget *parent = nullptr)` | 创建错误消息对话框。 | 通常在应用或主窗口生命周期内复用。 |
| 析构 | `~QErrorMessage()` | 销毁错误消息对话框。 | 父对象存在时由对象树管理。 |
| 工厂/查询 | `qtHandler()` | 返回 Qt 可复用的错误消息处理对象。 | 它是应用级入口，不等同于业务错误管理器。 |
| 槽 | `showMessage(const QString &message)` | 显示一条错误消息。 | 非阻塞显示；可能受到用户抑制设置影响。 |
| 槽 | `showMessage(const QString &message, const QString &type)` | 按消息类型显示一条错误消息。 | type 应稳定表示错误类别。 |
| 对话框钩子 | `done(int result)` | 在对话框结束时处理关闭结果。 | 通常由 Qt 内部调用，子类化时才重写。 |
| 状态变化 | `changeEvent(QEvent *event)` | 处理语言、字体、样式等变化事件。 | 通常保留基类处理。 |

## 7. 一句话总结

`QErrorMessage` 是带重复消息抑制能力的错误对话框，适合集中展示不希望反复打断用户的错误，不适合替代日志系统或确认对话框。
