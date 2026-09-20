# Qt QShaderVersion：着色器语言版本与 GLSL ES 标志

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshader.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 继承：无  
> 类型定位：`QShaderKey` 使用的轻量值类型

## 1. 它解决什么问题

`QShaderVersion` 把 shader 代码的版本号和版本标志放在一起。`QShaderKey` 需要同时知道：

- 代码属于哪种 source，例如 GLSL、HLSL 或 SPIR-V；
- 该 source 使用什么版本；
- 是否是 GLSL ES；
- 同一 source/version 下使用哪个 shader variant。

只保存一个整数版本号不够区分桌面 GLSL 和 GLSL ES，因此 Qt 通过 `Flags` 保存 `GlslEs` 标志。

## 2. 构建与基本用法

```cpp
#include <rhi/qshader.h>

QShaderVersion desktopGlsl(450);
QShaderVersion glslEs(QShaderVersion(300, QShaderVersion::GlslEs));
```

更常见的是把它交给 `QShaderKey`：

```cpp
QShaderKey key(
    QShader::GlslShader,
    QShaderVersion(300, QShaderVersion::GlslEs));
```

版本值的具体合法范围由 source、生成工具和目标后端决定。`QShaderVersion` 本身不会编译代码，也不会检查某个版本是否被目标 GPU 支持。

## 3. 成员类型

```cpp
enum Flag {
    GlslEs = 0x01
};
Q_DECLARE_FLAGS(Flags, Flag)
```

`GlslEs` 是一个 flags 位，用于说明版本号对应 GLSL ES。当前头文件只有这个 flag，但代码仍应按 flags 处理：

```cpp
if (version.flags().testFlag(QShaderVersion::GlslEs)) {
    // 这是 GLSL ES 版本
}
```

没有 `GlslEs` 时通常表示桌面 GLSL 或不需要 ES 标记的 source。对 HLSL、MSL、WGSL 等 source，version 的具体解释要以生成器和 `QShaderKey` 使用约定为准。

## 4. 默认值和初始化

头文件中的字段默认值是：

```cpp
int m_version = 100;
Flags m_flags;
```

因此：

```cpp
QShaderVersion version;
qDebug() << version.version(); // 100
qDebug() << version.flags();   // 空 flags
```

默认值只是一个可构造的初始值，不表示“当前平台支持 GLSL 100”，也不表示一个通配版本。若要查询 `QShader` 中的代码，应该构造与实际条目完全匹配的 `QShaderKey`。

## 5. 实际使用场景

### 5.1 创建 GLSL ES key

```cpp
QShaderKey esKey(
    QShader::GlslShader,
    QShaderVersion(300, QShaderVersion::GlslEs),
    QShader::StandardShader);
```

### 5.2 在不同版本之间选择

版本对象可用于构造候选 key，但它不会自动执行“向下兼容”或“选择最接近版本”：

```cpp
QShaderCode code = shader.shader(esKey);
if (code.shader().isEmpty()) {
    // 该精确 source/version/variant key 不存在
}
```

应用需要自己定义 fallback 顺序，例如先尝试目标后端生成的 GLSL ES，再尝试桌面 GLSL。不能把 `QShaderVersion(300, GlslEs)` 与 `QShaderVersion(450)` 当作同一个版本。

## 6. 成员函数

### `QShaderVersion::QShaderVersion()`

默认构造版本对象，版本为 `100`，flags 为空。它适合构造对象后再设置字段，不表示未初始化或通配符。

### `QShaderVersion::QShaderVersion(int v, QShaderVersion::Flags f = Flags())`

用版本号和 flags 构造对象。`f` 默认为空：

```cpp
QShaderVersion desktop(450);
QShaderVersion es(300, QShaderVersion::GlslEs);
```

构造函数不会验证 `v` 是否符合 source，也不会验证 `GlslEs` 是否适用于即将使用的 source。

### `int QShaderVersion::version() const`

返回版本号。它是 `QShaderKey` 的一部分，比较和查找时要和 flags 一起考虑。

### `void QShaderVersion::setVersion(int v)`

替换版本号。修改后，使用该对象构造的 `QShaderKey` 会指向另一个精确条目；它不会修改已经存储在 `QShader` 中的 key，也不会转换 shader code。

### `QShaderVersion::Flags QShaderVersion::flags() const`

返回版本 flags。当前主要检查 `GlslEs`。

### `void QShaderVersion::setFlags(QShaderVersion::Flags f)`

替换全部 flags。它不会对现有 shader source 做转换，也不会自动更新 `QShader` 中已有的代码。

## 7. 比较运算符

### `bool operator==(const QShaderVersion &, const QShaderVersion &) noexcept`

比较版本号和 flags。版本号相同但一个带 `GlslEs`、另一个不带时，二者不相等。

### `bool operator!=(const QShaderVersion &, const QShaderVersion &) noexcept`

返回相等比较的逻辑反值。

### `bool operator<(const QShaderVersion &, const QShaderVersion &) noexcept`

为有序容器和 `QShaderKey` 的排序提供严格弱序。它用于组织 key，不表示“版本较大一定更兼容”或“版本较小一定可以作为 fallback”。

## 8. 常见误区

- 把整数版本相同的桌面 GLSL 和 GLSL ES 当成同一个版本。
- 认为默认版本 `100` 是通配符。
- 修改 `QShaderVersion` 后期待已有 `QShader` 条目自动迁移。
- 用 `operator<` 判断 GPU 或后端能力。
- 认为 `QShaderVersion` 会验证版本和 source 是否匹配。
- 只比较 `version()` 而忽略 `flags()`。
- 传入 `GlslEs` 后期待 Qt 自动把桌面 GLSL 转成 ES。

## 9. 与相关类型协作

| 类型 | 关系 |
| --- | --- |
| `QShaderKey` | 把 `Source`、`QShaderVersion` 和 `Variant` 组成精确代码索引 |
| `QShader` | 用 `QShaderKey` 查询或存储 shader code |
| `QShaderCode` | 保存代码和入口点，本类不保存代码 |
| `QShaderBaker` | 生成与目标 source/version 对应的代码条目 |

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 枚举 | `Flag::GlslEs` | 标识 GLSL ES 版本 | 是 flags 位，不是独立 source |
| 类型 | `Flags` | 保存版本 flags | 当前主要检查 `GlslEs` |
| 构造 | `QShaderVersion()` | 创建默认版本 | 默认 version 为 100，非通配符 |
| 构造 | `QShaderVersion(int v, Flags f = Flags())` | 创建指定版本 | 不验证 source、版本和后端能力 |
| 查询 | `version() const` | 读取版本号 | 要和 flags 一起比较 |
| 修改 | `setVersion(int v)` | 设置版本号 | 不迁移已有 shader 条目 |
| 查询 | `flags() const` | 读取版本 flags | 空 flags 不等于错误 |
| 修改 | `setFlags(Flags f)` | 设置全部 flags | 不转换 shader code |
| 比较 | `operator==` | 比较版本号和 flags | ES 标志不同则不相等 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |
| 排序 | `operator<` | 为有序容器排序 | 不是兼容性或优先级判断 |

---

### 一句话总结

`QShaderVersion` 是 `QShaderKey` 的版本维度：整数版本必须和 `GlslEs` flags 一起理解，默认值不是通配符；比较排序只服务于精确 key 和容器，不会替应用做版本回退或后端能力判断。
