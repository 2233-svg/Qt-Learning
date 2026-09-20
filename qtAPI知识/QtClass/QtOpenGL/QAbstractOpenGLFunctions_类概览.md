# QAbstractOpenGLFunctions 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractOpenGLFunctions>`  
> 所属模块：`Qt6::OpenGL`  
> 类型：OpenGL 函数对象的抽象基类

## 它解决什么问题

不同平台能够在链接阶段直接提供的 OpenGL 符号并不一致。例如 Windows 的系统 OpenGL ABI 只保证早期函数，较新的函数必须在运行时从实际 context 中解析。手工调用 `QOpenGLContext::getProcAddress()` 虽然可行，却需要维护一批函数指针、空指针检查和版本判断。

`QAbstractOpenGLFunctions` 是 Qt 版本化 OpenGL 函数类的共同基类。`QOpenGLFunctions_3_3_Core`、`QOpenGLFunctions_4_5_Core` 等具体类从它继承，并以成员函数方式暴露对应版本/profile 的 OpenGL API。基类负责把函数对象与 OpenGL context 关联，并在初始化时解析所需函数地址。

它的价值在于把两类错误尽量提前暴露：

- 编译期：具体函数类没有声明的 API 不能调用；
- 运行期：当前 context 不满足版本/profile 要求时，`initializeOpenGLFunctions()` 返回 `false`。

## 实际使用场景

### 在渲染控件中固定使用某个版本

`QOpenGLWidget::initializeGL()`、`QOpenGLWindow::initializeGL()` 运行时已经有 current context，适合在这里初始化一个具体函数对象。之后在 `paintGL()` 中通过该对象调用 OpenGL 函数。

### 依据实际 context 选择函数集合

要兼容多种显卡与驱动时，可以结合 `QOpenGLVersionFunctionsFactory` 取得匹配当前 version/profile 的函数对象。工厂路径避免了应用自行维护函数对象缓存。

### 让 OpenGL 调用在渲染线程集中执行

函数对象不是线程同步机制。它只是已经解析的 API 入口集合；创建资源、调用 `gl*` 函数时仍要保证正确的 `QOpenGLContext` 已在当前线程中 current。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS OpenGL)
target_link_libraries(mytarget PRIVATE Qt6::OpenGL)
```

```cpp
#include <QOpenGLContext>
#include <QOpenGLFunctions_3_3_Core>

void clearWithCurrentContext()
{
    Q_ASSERT(QOpenGLContext::currentContext());

    QOpenGLFunctions_3_3_Core functions;
    if (!functions.initializeOpenGLFunctions()) {
        // 当前 context 并不提供所请求的 3.3 Core 函数集合。
        return;
    }

    functions.glClearColor(0.08f, 0.08f, 0.10f, 1.0f);
    functions.glClear(GL_COLOR_BUFFER_BIT);
}
```

实际项目中，函数对象通常是渲染类成员，而不是每帧创建：

```cpp
class Renderer
{
public:
    bool initialize()
    {
        return m_gl.initializeOpenGLFunctions();
    }

    void render()
    {
        m_gl.glClear(GL_COLOR_BUFFER_BIT);
    }

private:
    QOpenGLFunctions_3_3_Core m_gl;
};
```

`QAbstractOpenGLFunctions` 本身不能直接实例化，应使用它的具体派生类。

## 关键语义与边界

### 初始化依赖 current context

`initializeOpenGLFunctions()` 从**当前** OpenGL context 解析函数地址。调用之前必须已将正确 context 设为 current；仅构造一个函数对象不代表它已经能调用 OpenGL。

如果具体函数类要求的版本或 profile 不在当前 context 中，初始化会失败。失败后不能继续调用该类暴露的 `gl*` API。

### “初始化一次”只针对一个对象与其关联 context

对同一个函数对象，一般只需成功初始化一次。但这不代表任意 context 都能共用该对象：函数入口与初始化时的 context 相关。切换 context、跨线程渲染或使用不同版本/profile 时，应重新设计函数对象的所有权与初始化位置。

### 工厂对象的所有权

从 `QOpenGLVersionFunctionsFactory::get()` 获得的对象由 `QOpenGLContext` 保留和管理，以便缓存与复用。应用不应自行释放工厂返回的对象。

自行作为成员创建的具体函数对象则遵循普通 C++ 生命周期。

### Core 与 Compatibility 的选择

OpenGL 3.2 引入 profile。Core profile 不含 OpenGL 3.1 移除的旧 API；Compatibility profile 保留兼容接口。新渲染代码通常应请求 Core profile；遗留固定管线代码则可能依赖 Compatibility profile。请求的 `QSurfaceFormat`、实际创建的 context 和选用的函数类必须相互匹配。

### 不可拷贝

基类禁用拷贝。函数对象表达一组绑定到 context 的已解析函数入口，复制它并不能创建另一个独立的 context 绑定。

## 常见误区

### 只看请求格式，不看初始化返回值

`QSurfaceFormat` 是请求，不是驱动一定兑现的承诺。必须检查实际 context 以及 `initializeOpenGLFunctions()` 的结果。

### 没有 current context 就调用初始化或 `gl*`

函数对象不能取代 context。初始化、资源创建和实际 OpenGL 调用都受 current context 约束。

### 从一个线程把函数对象直接交给另一个线程

对象地址可以传递，但 context 的 current 状态不会随之迁移。跨线程渲染必须按照 `QOpenGLContext` 的线程归属和 `makeCurrent()` 规则组织。

## 逐项 API 说明

### 公共函数

#### `virtual bool QAbstractOpenGLFunctions::initializeOpenGLFunctions()`

解析当前 context 所需的 OpenGL 函数地址。

- 返回 `true`：函数集合可用，可以调用对应派生类的 `gl*` 成员。
- 返回 `false`：没有合适的 current context，或 context 不包含该版本/profile 所需函数。
- 应在调用任意派生 OpenGL 函数前检查返回值。

#### `virtual noexcept QAbstractOpenGLFunctions::~QAbstractOpenGLFunctions()`

虚析构函数，允许通过基类指针正确销毁具体函数对象。它不等同于销毁纹理、buffer、shader 等 OpenGL server 资源。

### 受保护函数

#### `QAbstractOpenGLFunctions::QAbstractOpenGLFunctions()`

构造抽象基类部分。仅供派生类调用，不能直接创建 `QAbstractOpenGLFunctions`。

#### `bool QAbstractOpenGLFunctions::isInitialized() const`

查询函数对象是否已经完成函数地址解析。仅表示本对象的初始化状态，不保证调用线程当前仍绑定了正确 context。

#### `void QAbstractOpenGLFunctions::setOwningContext(const QOpenGLContext *context)`

设置函数对象关联的 context。该接口供 Qt 的函数类/工厂实现维护，普通业务代码不应借此把对象强行复用于不匹配的 context。

#### `QOpenGLContext *QAbstractOpenGLFunctions::owningContext() const`

返回关联 context。拿到指针不代表该 context 当前就在本线程，也不自动保证其生命周期仍有效。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 公共函数 | `initializeOpenGLFunctions()` | 为当前 context 解析具体 OpenGL 函数。 | 必须有 current context；返回 `false` 后不能调用派生 `gl*` API。 |
| 公共函数 | `~QAbstractOpenGLFunctions()` | 通过基类安全销毁派生函数对象。 | 不负责替代纹理、buffer 等 GPU 资源的生命周期。 |
| 受保护函数 | `QAbstractOpenGLFunctions()` | 初始化抽象基类部分。 | 只能由派生类构造。 |
| 受保护函数 | `isInitialized()` | 查询函数地址是否已经解析。 | 不等于当前 context 仍然正确或 current。 |
| 受保护函数 | `setOwningContext(const QOpenGLContext *)` | 关联函数对象与 context。 | 由派生类/工厂维护，不用于任意跨 context 复用。 |
| 受保护函数 | `owningContext()` | 查询关联 context。 | 返回指针不代表 context 当前或仍有效。 |

### 一句话总结

`QAbstractOpenGLFunctions` 为 Qt 的版本化 OpenGL API 提供“按当前 context 解析函数”的共同基础；先初始化成功，再在匹配的 current context 中调用具体函数类。
