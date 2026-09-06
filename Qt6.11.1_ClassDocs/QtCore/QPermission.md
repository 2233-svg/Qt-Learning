# QPermission

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QPermission` 是平台权限描述类型，用于查询和请求某项设备或系统能力的授权状态。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPermission` 是 应用权限机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 权限类型本身是描述“要访问什么能力”的轻量值对象，不负责弹窗，也不直接打开摄像头、麦克风或定位设备。真正的状态查询和运行时请求由 `QCoreApplication::checkPermission()`、`requestPermission()` 完成，结果通过回调返回 `QPermission`。

**适用场景：** 先创建具体权限类型，例如 `QCameraPermission{}`，用 `checkPermission()` 查询；未确定时调用 `requestPermission()`，在回调中检查 `permission.status()`，获准后再创建相机、麦克风或定位会话。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 权限描述对象不是设备对象；请求权限不等于设备初始化成功；不要只处理 granted 分支而忽略 denied；还要按平台要求配置构建声明和系统权限说明。

## 2. 依赖与对象关系

- 头文件：`#include <QPermissions>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

权限类型本身是描述“要访问什么能力”的轻量值对象，不负责弹窗，也不直接打开摄像头、麦克风或定位设备。真正的状态查询和运行时请求由 `QCoreApplication::checkPermission()`、`requestPermission()` 完成，结果通过回调返回 `QPermission`。

### 状态、生命周期和线程

**生命周期：** 权限描述对象可以临时构造和按值传递；权限请求的回调必须绑定到仍然有效的 context 或对象生命周期。权限状态可能因平台、用户设置和应用运行阶段改变，不能只在启动时缓存一次。

**状态与结果：** `Granted` 表示当前允许，`Denied` 表示当前拒绝或平台不适用，`Undetermined` 表示还没有得到用户决定。查询得到 `Undetermined` 时要请求权限；请求回调返回后再根据状态决定是否创建真正的设备对象。

**线程与事件循环：** 权限请求依赖应用事件循环和平台 GUI/权限系统，通常在应用主线程发起。回调不要阻塞，也不要在权限结果返回前假定设备已经可用。

## 3. 直接使用

先创建具体权限类型，例如 `QCameraPermission{}`，用 `checkPermission()` 查询；未确定时调用 `requestPermission()`，在回调中检查 `permission.status()`，获准后再创建相机、麦克风或定位会话。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QCoreApplication>
#include <QPermissions>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    QCameraPermission permission;
    const auto status = app.checkPermission(permission);
    if (status == Qt::PermissionStatus::Undetermined) {
        app.requestPermission(permission, [](const QPermission &result) {
            if (result.status() == Qt::PermissionStatus::Granted) {
                // 现在才创建实际的设备或服务对象
            }
        });
    }
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QPermission(const T &type)`
- `Qt::PermissionStatus status() const`
- `QMetaType type() const`
- `std::optional<T> value() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 4 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `template <typename T, QPermission::if_permission<T> = true> QPermission::QPermission(const T &type)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QPermission` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `const T &`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::PermissionStatus QPermission::status() const`

**API 类别：** 成员函数说明

**中文解读：** `QPermission::status` 用于计算、查询或取得与“状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::PermissionStatus`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::PermissionStatus`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMetaType QPermission::type() const`

**API 类别：** 成员函数说明

**中文解读：** `QPermission::type` 用于计算、查询或取得与“类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMetaType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMetaType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T, QPermission::if_permission<T> = true> std::optional<T> QPermission::value() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QPermission` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`template <typename T, QPermission::if_permission<T> = true> std::optional<T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

权限描述对象可以临时构造和按值传递；权限请求的回调必须绑定到仍然有效的 context 或对象生命周期。权限状态可能因平台、用户设置和应用运行阶段改变，不能只在启动时缓存一次。

### 状态和错误边界

`Granted` 表示当前允许，`Denied` 表示当前拒绝或平台不适用，`Undetermined` 表示还没有得到用户决定。查询得到 `Undetermined` 时要请求权限；请求回调返回后再根据状态决定是否创建真正的设备对象。

### 线程边界

权限请求依赖应用事件循环和平台 GUI/权限系统，通常在应用主线程发起。回调不要阻塞，也不要在权限结果返回前假定设备已经可用。

### 最容易出现的错误

权限描述对象不是设备对象；请求权限不等于设备初始化成功；不要只处理 granted 分支而忽略 denied；还要按平台要求配置构建声明和系统权限说明。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPermission` 所属机制类型：应用权限机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
