# QOpenGLVersionFunctionsFactory 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLVersionFunctionsFactory>`  
> 所属模块：`Qt6::OpenGL`  
> 定位：按 OpenGL 版本/profile 获取对应 `QOpenGLFunctions_*` 函数对象

## 它解决什么问题

Qt 为很多 OpenGL 版本和 profile 生成了专门的函数包装类，例如 `QOpenGLFunctions_3_3_Core`、`QOpenGLFunctions_4_5_Compatibility`。`QOpenGLVersionFunctionsFactory` 是这些函数对象的工厂：给它一个 `QOpenGLVersionProfile` 或模板类型，它会根据指定 `QOpenGLContext` 返回匹配的函数集合对象。

它解决的是“我手上有一个 context，想安全拿到某个版本/profile 的函数入口”这个问题。直接构造具体 `QOpenGLFunctions_*` 类需要自己初始化和判断是否兼容；工厂会按 context 能力匹配，不能满足时返回 `nullptr`。

## 实际使用场景

- 在运行时检测到 context 是 OpenGL 3.3 core 后，获取 `QOpenGLFunctions_3_3_Core`；
- 库代码接受任意 `QOpenGLContext *`，按需要请求某个最低版本的函数对象；
- 想避免把函数对象作为成员长期手工管理，让 context 缓存并拥有对象；
- 按 `QSurfaceFormat` 或用户配置构造 `QOpenGLVersionProfile`，再请求对应函数集。

## 基本用法

```cpp
#include <QOpenGLVersionFunctionsFactory>
#include <QOpenGLFunctions_3_3_Core>

bool init(QOpenGLContext *context)
{
    auto *gl = QOpenGLVersionFunctionsFactory::get<QOpenGLFunctions_3_3_Core>(context);
    if (!gl)
        return false;

    gl->glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    return true;
}
```

如果传入的 `context` 当前已经 current，通常不需要再手动调用 `initializeOpenGLFunctions()`。如果 context 没有 current 就调用工厂，返回对象后由调用方负责在合适时机初始化。

## 核心语义

### 返回对象由 context 拥有

通过这个工厂拿到的函数对象由 `QOpenGLContext` 持有和缓存。调用方不应该 delete 返回指针，也不应该在 context 销毁后继续保存并使用它。

### 可以请求低版本，不能请求不兼容版本

假设 context 是 3.3 core，请求 3.1 通常可以成功，因为 3.1 功能可由该 context 满足；请求 4.3 core 会失败，因为缺少 4.0 到 4.3 新增函数；请求 3.3 compatibility 也可能失败，因为 core context 不提供 deprecated compatibility 函数。

### 模板版本更少出错

模板 `get<TYPE>()` 会用 `TYPE::versionProfile()` 自动构造请求条件，并把结果 cast 成目标类型。非模板版本返回 `QAbstractOpenGLFunctions *`，适合运行时决定版本/profile 的情况。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `static QAbstractOpenGLFunctions *get(const QOpenGLVersionProfile &versionProfile = QOpenGLVersionProfile(), QOpenGLContext *context = nullptr)` | 按指定版本/profile 和 context 获取通用函数对象指针。 | `nullptr` context 表示当前 context；失败返回 `nullptr`；返回对象由 context 拥有。 |
| `template<class TYPE> static TYPE *get(QOpenGLContext *context = nullptr)` | 按具体 `QOpenGLFunctions_*` 类型获取强类型函数对象。 | 推荐用法；目标类型必须有可满足的 `versionProfile()`。 |
| 返回对象的 `initializeOpenGLFunctions()` | 在 context 未 current 时获取对象后，稍后手动初始化函数入口。 | context 已 current 时通常无需手动初始化；未 current 时调用方负责。 |
| `QOpenGLVersionProfile` 参数 | 描述所需 OpenGL major/minor/profile。 | profile 不匹配会失败，尤其是 core 与 compatibility 的 deprecated 函数差异。 |

## 常见误区

### 对返回指针手动 delete

工厂返回的对象由 `QOpenGLContext` 缓存和管理。手动删除会破坏 context 内部缓存。

### 只看版本号，不看 profile

OpenGL 3.3 core 和 3.3 compatibility 的函数集合并不一样。core context 无法提供很多固定管线/废弃函数。

### 在 context 未 current 时忘记初始化

工厂允许这种调用，但不会神奇地完成函数解析。之后必须在正确 context current 后调用 `initializeOpenGLFunctions()`。

## 一句话总结

`QOpenGLVersionFunctionsFactory` 是按 context 获取版本化 OpenGL 函数对象的入口；用它能少写初始化胶水，但版本/profile 匹配、返回空指针和 context 所有权必须认真处理。
