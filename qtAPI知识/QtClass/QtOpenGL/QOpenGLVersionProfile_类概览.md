# QOpenGLVersionProfile 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOpenGLVersionProfile>`  
> 所属模块：`Qt6::OpenGL`  
> 继承：无  
> 定位：描述一个 OpenGL 版本以及适用时的 core/compatibility profile

## 它解决什么问题

`QOpenGLVersionProfile` 是一个小型值对象，用来表达“我需要哪个 OpenGL 版本和 profile”。它通常传给 `QOpenGLContext::versionFunctions()` 或 `QOpenGLVersionFunctionsFactory::get()`，以获取对应的 `QOpenGLFunctions_*` 函数对象。

OpenGL 不是单纯的版本数字问题。3.2 之后引入 core/compatibility profile，同样是 3.3，core profile 没有固定管线和废弃函数，compatibility profile 保留旧 API。这个类把版本号和 profile 放在一起，避免只用 `(major, minor)` 造成误判。

## 实际使用场景

- 从 `QSurfaceFormat` 提取 context 的版本/profile，用来请求版本化函数对象；
- 明确请求 `3.3 Core` 或 `4.5 Compatibility` 函数集；
- 在库代码中把所需 OpenGL 能力作为参数传递，而不是到处散落版本整数；
- 在调试日志中输出当前请求的 OpenGL 版本/profile。

## 基本用法

```cpp
#include <QOpenGLVersionProfile>
#include <QOpenGLVersionFunctionsFactory>

QOpenGLVersionProfile profile;
profile.setVersion(3, 3);
profile.setProfile(QSurfaceFormat::CoreProfile);

auto *functions = QOpenGLVersionFunctionsFactory::get(profile);
if (!functions) {
    // current context cannot satisfy this version/profile
}
```

也可以从 `QSurfaceFormat` 构造：

```cpp
QOpenGLVersionProfile profile(context->format());
```

默认构造的对象是无效的，`isValid()` 返回 `false`，需要设置版本或从有效 format 初始化后再用。

## 核心语义

### version 是 major/minor 二元组

`setVersion(major, minor)` 设置 OpenGL 版本，`version()` 返回 `std::pair<int, int>`。版本本身不代表 profile 是否有意义。

### profile 只在 3.2+ 有意义

`hasProfiles()` 判断当前版本是否支持 profile。OpenGL 3.2 起才有 core/compatibility profile；更早版本没有 profile 概念。

### legacy version 是 3.1 及以下

`isLegacyVersion()` 用来判断版本是否包含 deprecated 函数且不支持 profile，即 OpenGL <= 3.1。写兼容旧固定管线代码时，这个判断比只看 profile 更准确。

### 它是描述，不是能力保证

`QOpenGLVersionProfile` 只是描述请求条件。真正能否满足，要看具体 `QOpenGLContext` 以及 `QOpenGLVersionFunctionsFactory::get()` 是否返回非空。

## API 速查表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QOpenGLVersionProfile()` | 创建默认版本/profile 对象。 | 默认无效，`isValid()` 为 `false`。 |
| `QOpenGLVersionProfile(const QSurfaceFormat &format)` | 从 surface format 提取版本和 profile。 | 适合基于已创建 context 的 format 请求函数对象。 |
| `QOpenGLVersionProfile(const QOpenGLVersionProfile &other)` | 拷贝构造。 | 值对象语义，可安全传递。 |
| `~QOpenGLVersionProfile()` | 销毁对象。 | 不拥有 OpenGL 资源。 |
| `operator=(const QOpenGLVersionProfile &rhs)` | 赋值版本和 profile。 | 普通值赋值。 |
| `setVersion(int majorVersion, int minorVersion)` | 设置 OpenGL major/minor 版本。 | 设置后再用 `isValid()`、`hasProfiles()` 检查语义。 |
| `version() const` | 返回 `(major, minor)`。 | 返回类型是 `std::pair<int, int>`。 |
| `setProfile(QSurfaceFormat::OpenGLContextProfile profile)` | 设置 core/compatibility/no profile。 | 只有支持 profile 的版本才有实际意义。 |
| `profile() const` | 返回当前 profile 设置。 | 对 legacy 版本不要强行解读。 |
| `hasProfiles() const` | 判断该版本是否支持 OpenGL profile。 | OpenGL 3.2+ 才返回 true。 |
| `isLegacyVersion() const` | 判断是否为 OpenGL <= 3.1 的 legacy 版本。 | legacy 版本含 deprecated 函数且无 profile 概念。 |
| `isValid() const` | 判断版本号是否有效。 | 默认构造无效；无效对象不适合表达明确请求。 |
| `operator==` / `operator!=` | 比较版本和 profile 是否相同。 | 可用于缓存键或条件判断。 |
| `qHash(const QOpenGLVersionProfile &)` | 作为哈希键使用。 | 适合 `QHash` 等容器。 |
| `operator<<(QDebug, QOpenGLVersionProfile)` | 调试输出版本/profile。 | 仅在 debug stream 可用时提供。 |

## 常见误区

### 把默认对象当作“当前 context profile”

默认构造是无效 profile，不会自动读取当前 context。要从 `context->format()` 构造，或显式设置版本/profile。

### 对 OpenGL 3.1 及以下设置 core profile

这些版本没有 profile 概念。`setProfile()` 可以设置值，但语义上只有 3.2+ 才有意义。

### 以为 profile 请求一定能成功

一个 `QOpenGLVersionProfile` 描述的是需求，不是平台能力。最终必须检查工厂或 `versionFunctions()` 的返回值。

## 一句话总结

`QOpenGLVersionProfile` 是 OpenGL 版本和 profile 的描述对象；它让函数对象请求更明确，但真正可用性仍要由当前 context 验证。
