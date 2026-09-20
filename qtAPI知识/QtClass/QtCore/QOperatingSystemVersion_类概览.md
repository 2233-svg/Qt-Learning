# Qt QOperatingSystemVersion：以产品版本而非内核版本做运行时分支

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOperatingSystemVersion>`  
> 所属模块：`Qt6::Core`  
> 类型性质：轻量值类型；无 `QObject`、无父子所有权、无信号槽、无线程亲和性  
> 支持的运行时系统：Android、Apple 平台、Windows

## 1. 它解决什么问题

程序有时需要根据**正在运行的操作系统产品版本**启用 API、选择兼容路径或绕开已知平台问题：

```cpp
const auto os = QOperatingSystemVersion::current();

if (os >= QOperatingSystemVersion::Windows11_24H2) {
    enableNewWindowsIntegration();
}
```

`QOperatingSystemVersion` 把这件事表示为一组不可变值：

```text
操作系统家族 + major + minor + micro
例如 Windows + 10 + 0 + 26100
```

它解决的不是“当前内核版本是多少”，也不是“系统营销名称是什么”。它提供开发者通常用于功能分支的产品版本：

- Android：通常解析 `android.os.Build.VERSION.RELEASE`；解析失败时用 API level 推导 major/minor；
- Apple 平台：使用 `NSProcessInfo.operatingSystemVersion` 的 major/minor/patch；
- Windows：使用 `RtlGetVersion` 的 major/minor/build，读取底层系统版本，不受 `GetVersionEx` 兼容 shim 的 manifest 影响。

与 `QSysInfo` 的若干版本函数相比，这是其核心定位：`QOperatingSystemVersion` 用于判断操作系统产品版本，`QSysInfo` 的 kernel 信息不应替代它来决定产品 API 可用性。

## 2. 典型使用场景

### 2.1 启用某个系统版本后的能力

```cpp
using OS = QOperatingSystemVersion;

const OS os = OS::current();
if (os >= OS::Windows11_23H2)
    useNewWindowsBehavior();
else
    useCompatibleWindowsBehavior();
```

版本判断只是“该路径的候选前置条件”。动态库、权限、厂商 ROM、设备特性和单独 API 的调用失败仍要分别处理。

### 2.2 用一条表达式覆盖多个平台

不同 OS 类型的比较结果是不可排序，因此可以安全地用逻辑或组合平台阈值：

```cpp
using OS = QOperatingSystemVersion;
const auto os = OS::current();

if (os >= OS::MacOSVentura || os >= OS(OS::IOS, 16)) {
    enableModernApplePath();
}
```

在 macOS 13 及以上时左侧为真；在 iOS 16 及以上时右侧为真；Windows 和 Android 两侧都为假。无需先写一长串 `type() == ...` 才能避免“13 大于 10”这种跨系统数字误判。

### 2.3 仅判断系统家族

不需要版本时，`currentType()` 不必构造版本对象：

```cpp
using OS = QOperatingSystemVersion;

if (OS::currentType() == OS::Android)
    configureAndroidOnlyBehavior();
```

若已经持有版本对象，使用 `isAnyOfType()` 处理一组平台：

```cpp
const auto os = QOperatingSystemVersion::current();
if (os.isAnyOfType({
        QOperatingSystemVersion::IOS,
        QOperatingSystemVersion::TvOS,
        QOperatingSystemVersion::WatchOS,
        QOperatingSystemVersion::VisionOS
    })) {
    configureAppleFamilyBehavior();
}
```

### 2.4 记录诊断信息

```cpp
const auto os = QOperatingSystemVersion::current();
qDebug() << os.name()
         << os.majorVersion()
         << os.minorVersion()
         << os.microVersion();
```

`name()` 只返回系统家族的字符串表示，例如 `Windows`、`Android` 或 `macOS`；它不是“Windows 11 24H2”之类完整营销版本文本。

## 3. 构建与类型模型

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QOperatingSystemVersion>
```

它是普通值类型：

- 可复制、可移动、可按值传递；
- 不管理资源，也没有析构时的外部副作用；
- 没有事件循环、父对象或线程亲和性要求；
- 头文件将其标记为 `Q_PRIMITIVE_TYPE`，适合放在轻量数据结构中。

Qt 6.3 起，许多原本直接出现在 `QOperatingSystemVersion` 上的实现被提到公开基类 `QOperatingSystemVersionBase`，以保持 API/ABI 兼容。实践中通常写 `auto` 接收常量和 `current()` 返回值即可；新版常量的声明类型也可能显示为 `QOperatingSystemVersionBase`，这不影响读取、比较或传给以基类为参数的比较运算。

## 4. 最重要的规则：比较不是全序

### 4.1 同一 OS 类型才按版本号排序

同一 `OSType` 中按 `major`、`minor`、`micro` 依次比较：

```cpp
using OS = QOperatingSystemVersion;

const OS older(OS::Windows, 10, 0, 19045);
const OS newer(OS::Windows, 10, 0, 22631);
Q_ASSERT(newer > older);
```

### 4.2 不同 OS 类型是 unordered

若 OS 类型不同，三路比较的结果是 `unordered`。对通常的关系运算而言，下面两个表达式都可能为 `false`：

```cpp
using OS = QOperatingSystemVersion;

const OS macOS(OS::MacOS, 10, 12);
const OS ios(OS::IOS, 9);

const bool a = macOS >= ios; // false
const bool b = macOS < ios;  // false
```

这不是矛盾，而是刻意避免跨平台数字比较。macOS 10.12 不能因为数字 `10 > 9` 就被误判为 “iOS 9 以上”。

因此：

- 可以用跨 OS 阈值与 `||` 组合；
- 不要把 `a >= b` 为假推导成 `a < b`；
- 不要对混合 `OSType` 的版本排序、求最小值或最大值；
- 需要先分组时，先用 `type()` 或 `isAnyOfType()`。

在支持 C++20 三路比较的构建中，底层语义对应 `std::partial_ordering`；较早语言模式下 Qt 仍提供关系运算，但保持相同的“不同 OS 不可排序”规则。

## 5. 版本段与未知段

构造函数接受最多三段版本：

```cpp
constexpr QOperatingSystemVersion(
    OSType osType, int vmajor, int vminor = -1, int vmicro = -1);
```

- `majorVersion()`：第 1 段；
- `minorVersion()`：第 2 段；
- `microVersion()`：第 3 段；
- `-1`：该段未知或缺失；
- `segmentCount()`：保存的连续版本段数；
- `version()`：以 `QVersionNumber` 返回三个版本段。

正确地表示只知道 major：

```cpp
const QOperatingSystemVersion version(
    QOperatingSystemVersion::Windows, 10);

Q_ASSERT(version.majorVersion() == 10);
Q_ASSERT(version.minorVersion() == -1);
Q_ASSERT(version.microVersion() == -1);
Q_ASSERT(version.segmentCount() == 1);
```

应将未知段保持在末尾。不要构造“major 未知但 minor 已知”这类没有自然版本含义的组合：

```cpp
// 不推荐：构造函数不替你校验版本语义。
const QOperatingSystemVersion malformed(
    QOperatingSystemVersion::Windows, -1, 0);
```

版本段缺失不等于数值 `0`：`10.0` 表示已知 minor 为零，`10` 表示 minor 未提供。判断阈值时按需要选择具体常量或明确构造相应段数。

## 6. 系统家族与当前值

### 6.1 `OSType`

| 枚举值 | 数值 | 表示 |
| --- | ---: | --- |
| `Unknown` | 0 | Qt 当前不支持或无法识别的系统 |
| `Windows` | 1 | Microsoft Windows |
| `MacOS` | 2 | Apple macOS |
| `IOS` | 3 | Apple iOS |
| `TvOS` | 4 | Apple tvOS |
| `WatchOS` | 5 | Apple watchOS |
| `Android` | 6 | Google Android |
| `VisionOS` | 7 | Apple visionOS |

`OSType` 表示系统家族，不表示发行版、小版本、CPU 架构或设备型号。

### 6.2 `currentType()` 与 `current()`

```cpp
const auto type = QOperatingSystemVersion::currentType();
const auto full = QOperatingSystemVersion::current();
```

两者用途不同：

| API | 得到什么 | 适用场景 |
| --- | --- | --- |
| `currentType()` | 当前编译目标 OS 的类型 | 仅按平台分支，不要版本号 |
| `current()` | 运行系统的类型和完整可得版本段 | API 阈值、诊断、版本比较 |

`currentType()` 是 `constexpr`，其实现由编译时的 `Q_OS_*` 宏选择；它不需要探测运行系统版本。`current()` 才访问平台版本信息。

在非 Android、Apple 平台和 Windows 的目标上，`current()` 可能返回 `Unknown` 类型或无法提供完整产品版本。跨平台产品应为 `Unknown` 准备保守回退路径，而不是假定所有 Qt 支持的平台都能产生可比较的完整版本。

## 7. 预定义版本常量

常量让常见阈值避免手写数字。它们是**版本比较基准**，不是 API 可用性的绝对保证。

### 7.1 Android 常量

| 常量 | 版本元组 | Android API level | Qt 引入 |
| --- | --- | ---: | --- |
| `AndroidJellyBean` | `Android 4.1` | 16 | 初始提供 |
| `AndroidJellyBean_MR1` | `Android 4.2` | 17 | 初始提供 |
| `AndroidJellyBean_MR2` | `Android 4.3` | 18 | 初始提供 |
| `AndroidKitKat` | `Android 4.4` | 19 | 初始提供 |
| `AndroidLollipop` | `Android 5.0` | 21 | 初始提供 |
| `AndroidLollipop_MR1` | `Android 5.1` | 22 | 初始提供 |
| `AndroidMarshmallow` | `Android 6.0` | 23 | 初始提供 |
| `AndroidNougat` | `Android 7.0` | 24 | 初始提供 |
| `AndroidNougat_MR1` | `Android 7.1` | 25 | 初始提供 |
| `AndroidOreo` | `Android 8.0` | 26 | 初始提供 |
| `AndroidOreo_MR1` | `Android 8.1` | 27 | 6.1 |
| `AndroidPie` | `Android 9.0` | 28 | 6.1 |
| `Android10` | `Android 10.0` | 29 | 6.1 |
| `Android11` | `Android 11.0` | 30 | 6.1 |
| `Android12` | `Android 12.0` | 31 | 6.5 |
| `Android12L` | `Android 12.0` | 32 | 6.5 |
| `Android13` | `Android 13.0` | 33 | 6.5 |
| `Android14` | `Android 14.0` | 34 | 6.7 |

**Android 12 与 12L 边界：** 两个常量的版本元组都是 `Android 12.0`。因此 `QOperatingSystemVersion` 的比较无法区分 API level 31 和 32；若功能门槛本质上是 Android API level，使用 Android 专属的 `QNativeInterface::QAndroidApplication::sdkVersion()`，或在 JNI 中查询 `Build.VERSION.SDK_INT`。

### 7.2 macOS 常量

| 常量 | 版本元组 | Qt 引入 |
| --- | --- | --- |
| `OSXMavericks` | `macOS 10.9` | 初始提供 |
| `OSXYosemite` | `macOS 10.10` | 初始提供 |
| `OSXElCapitan` | `macOS 10.11` | 初始提供 |
| `MacOSSierra` | `macOS 10.12` | 初始提供 |
| `MacOSHighSierra` | `macOS 10.13` | 初始提供 |
| `MacOSMojave` | `macOS 10.14` | 初始提供 |
| `MacOSCatalina` | `macOS 10.15` | 初始提供 |
| `MacOSBigSur` | `macOS 11` | 6.0 |
| `MacOSMonterey` | `macOS 12` | 6.3 |
| `MacOSVentura` | `macOS 13` | 6.4 |
| `MacOSSonoma` | `macOS 14` | 6.5 |
| `MacOSSequoia` | `macOS 15` | 6.8 |
| `MacOSTahoe` | `macOS 26` | 6.10 |

常量名保留了历史的 `OSX...` 命名，代码中仍以版本元组比较，不要通过常量前缀推断当前 Apple 产品品牌。

### 7.3 Windows 常量

| 常量 | 版本元组 | Qt 引入 |
| --- | --- | --- |
| `Windows7` | `Windows 6.1` | 初始提供 |
| `Windows8` | `Windows 6.2` | 初始提供 |
| `Windows8_1` | `Windows 6.3` | 初始提供 |
| `Windows10` | `Windows 10` | 初始提供 |
| `Windows10_1809` | `Windows 10.0.17763` | 6.3 |
| `Windows10_1903` | `Windows 10.0.18362` | 6.3 |
| `Windows10_1909` | `Windows 10.0.18363` | 6.3 |
| `Windows10_2004` | `Windows 10.0.19041` | 6.3 |
| `Windows10_20H2` | `Windows 10.0.19042` | 6.3 |
| `Windows10_21H1` | `Windows 10.0.19043` | 6.3 |
| `Windows10_21H2` | `Windows 10.0.19044` | 6.3 |
| `Windows10_22H2` | `Windows 10.0.19045` | 6.5 |
| `Windows11` / `Windows11_21H2` | `Windows 10.0.22000` | 6.3 / 6.4 |
| `Windows11_22H2` | `Windows 10.0.22621` | 6.4 |
| `Windows11_23H2` | `Windows 10.0.22631` | 6.6 |
| `Windows11_24H2` | `Windows 10.0.26100` | 6.8.1 |
| `Windows11_25H2` | `Windows 10.0.26200` | 6.11 |

Windows 11 的产品名并不意味着底层 version major 会变成 11。Qt 使用的底层版本元组仍是 `10.0.build`，因此应比较 `Windows11...` 常量或 build 阈值，而不是手写 `QOperatingSystemVersion(Windows, 11)`。

## 8. 常见错误

### 8.1 用 `QSysInfo::kernelVersion()` 判断产品 API

内核版本、产品版本和营销版本不是同一个概念。系统功能门槛应优先用 `QOperatingSystemVersion`，或在特定平台调用官方 feature/API 检测。

### 8.2 跨 OS 按数字大小比较

不同 `OSType` 不是“版本小或大”，而是 unordered。不要把比较失败理解成必定低于。

### 8.3 忽略缺失段的 `-1`

`minorVersion() == -1` 不是 `0`。不要把未知版本拼接、格式化或比较为已知的 `x.0`。

### 8.4 用 `name()` 做机器逻辑

`name()` 面向展示和日志。机器判断用 `type()`、`currentType()` 或 `isAnyOfType()`；不要依赖字符串语言、大小写或完整营销名。

### 8.5 用 Android 版本名判断 API level 32

`Android12` 和 `Android12L` 的版本元组相同。需要区分 API 31/32 时查询 SDK/API level。

### 8.6 硬编码 Windows 11 为 major 11

真实底层元组为 `10.0.22000` 及之后 build。使用 `Windows11` 或具体版本常量。

### 8.7 把版本检查当成最终成功保证

即便系统版本满足，功能仍可能受权限、动态库、OEM 改动、企业策略或运行时状态影响。真正的 API 调用必须保留失败处理。

## 9. 逐项 API 说明

### 9.1 构造函数

```cpp
constexpr QOperatingSystemVersion(
    OSType osType, int vmajor, int vminor = -1, int vmicro = -1);
```

创建一个指定系统家族和至多三段版本的不可变值。

- `vminor`、`vmicro` 缺省为 `-1`，表示未知/缺失；
- 构造函数不做“这个版本是否真实存在”的平台验证；
- 用于阈值、测试数据和明确的兼容分支；
- 一般不需要手写当前系统值，应使用 `current()`。

Qt 6.11.1 头文件还暴露转换构造：

```cpp
constexpr QOperatingSystemVersion(
    const QOperatingSystemVersionBase &osversion);
```

它用于从基类版本值恢复派生类型，主要服务于 Qt 6 的兼容类型布局。日常代码通常用 `auto`，无需显式调用。

### 9.2 `current()`

```cpp
static QOperatingSystemVersion current();
```

返回当前运行系统的 `OSType` 和可获得的产品版本段。

- 适合运行时版本阈值；
- 支持 Android、Apple 平台和 Windows；
- 其他系统可能得到 `Unknown` 或不完整版本；
- 不要把结果当作内核版本；
- 返回值是独立值，不拥有平台句柄。

### 9.3 `currentType()`

```cpp
static constexpr OSType currentType();
```

返回当前编译目标的系统家族，不构造版本对象。

- 适合简单的编译目标平台分支；
- 不读取 running OS 的版本号；
- 未命中 Qt 已知 `Q_OS_*` 宏时返回 `Unknown`；
- 若需要版本阈值，改用 `current()`。

### 9.4 `isAnyOfType()`

```cpp
bool isAnyOfType(std::initializer_list<OSType> types) const;
```

判断该对象的 OS 类型是否属于给定集合。

- 只比较 `OSType`，不比较版本段；
- 空列表返回 `false`；
- 用于 Apple 系列等多平台分组；
- 不修改对象。

### 9.5 `type()` 与 `name()`

```cpp
constexpr OSType type() const;
QString name() const;
```

`type()` 返回机器可判断的枚举；`name()` 返回该 OS 家族的字符串表示。

- `type()` 用于条件分支；
- `name()` 用于日志、诊断和展示；
- 二者都不包含版本段；
- 不要把 `name()` 返回字符串当作稳定协议字段。

### 9.6 版本段访问器

```cpp
constexpr int majorVersion() const;
constexpr int minorVersion() const;
constexpr int microVersion() const;
constexpr int segmentCount() const;
QVersionNumber version() const; // Qt 6.1 起
```

读取保存的版本信息。

- 三个段访问器中 `-1` 表示未知或不存在；
- `segmentCount()` 返回存储的段数，范围通常为 0 到 3；
- `version()` 便于同使用 `QVersionNumber` 的代码协作；
- 要保持“缺失段只出现在结尾”的业务约定。

### 9.7 比较运算

`<`、`<=`、`>`、`>=` 由 Qt 的部分序比较实现支持。

- 相同 `OSType`：按版本元组比较；
- 不同 `OSType`：无序，关系运算不代表一方更小；
- 可以用于“macOS 阈值或 iOS 阈值”的 `||` 表达式；
- 不要用于跨系统排序。

### 9.8 调试输出

```cpp
QDebug operator<<(QDebug debug, const QOperatingSystemVersion &version);
```

Qt 未禁用 debug stream 时提供。它适合输出诊断日志，不是稳定的持久化或跨进程序列化格式。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 查询 | `current()` | 取得当前 OS 产品版本 | Android、Apple、Windows 最有意义；处理 `Unknown` |
| 查询 | `currentType()` | 取得编译目标 OS 类型 | 不探测版本；适合纯平台分支 |
| 构造 | `QOperatingSystemVersion(type, major, minor, micro)` | 创建版本阈值/测试值 | 缺失段为 `-1`；不验证版本是否真实存在 |
| 类型 | `OSType` | 表示 Windows、Apple 各平台、Android 或 Unknown | 只表示家族，不含版本和架构 |
| 类型判断 | `isAnyOfType({ ... })` | 判断是否属于任一 OS 家族 | 只比较类型，不比较版本 |
| 类型读取 | `type()` | 返回枚举 OS 类型 | 用于机器逻辑 |
| 显示 | `name()` | 返回 OS 家族文本 | 只用于展示/日志，不是完整版本名 |
| 版本段 | `majorVersion()` | 返回第 1 段 | `-1` 表示缺失 |
| 版本段 | `minorVersion()` | 返回第 2 段 | `-1` 不等于 `0` |
| 版本段 | `microVersion()` | 返回第 3 段 | Windows 中通常承载 build |
| 版本段 | `segmentCount()` | 返回已保存的段数 | 由 `-1` 是否缺失决定 |
| 版本对象 | `version()` | 转为 `QVersionNumber` | Qt 6.1 起；仍需保留 OS 类型判断 |
| 比较 | `<`, `<=`, `>`, `>=` | 比较同 OS 类型的版本 | 不同 `OSType` 无序，不能跨系统排序 |
| Android 常量 | `AndroidJellyBean` 至 `Android14` | 常见 Android 产品版本阈值 | `Android12` 与 `Android12L` 均为 12.0；API level 要另查 |
| macOS 常量 | `OSXMavericks` 至 `MacOSTahoe` | 常见 macOS 版本阈值 | 产品版本会跨过 10、11、12...26；按常量比较 |
| Windows 常量 | `Windows7` 至 `Windows11_25H2` | 常见 Windows build 阈值 | Windows 11 元组仍是 `10.0.build` |
| 调试 | `operator<<(QDebug, version)` | 输出版本诊断信息 | 不作为稳定数据格式 |

## 11. 一句话总结

`QOperatingSystemVersion` 是用于运行时产品版本分支的轻量值类型：先用 `current()` 取得系统和版本，再只在同一 OS 家族内比较；不同家族视为无序，Android API level 与 Windows/macOS 的产品命名边界则应使用对应常量或平台专属检测补足。
