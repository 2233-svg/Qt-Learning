# QAbstractFileIconProvider

> Qt 6.11.1 · Qt GUI · 来自 `QAbstractFileIconProvider`

## 1. 先建立直觉

`QAbstractFileIconProvider` 定义“根据文件或特殊位置提供图标和类型文字”的协议。文件浏览器模型会把 `QFileInfo` 交给它，由实现决定显示文件夹、磁盘、网络位置或某个文件的图标；Qt 自带的实用实现是 `QFileIconProvider`。

这个类看似只是图标查询，实际会触及文件系统和桌面主题。尤其是网络共享、U 盘与自定义文件夹图标，查询成本可能远高于一次普通 `QIcon` 查找。

## 2. 类说明

- 头文件：`#include <QAbstractFileIconProvider>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 来源类：抽象基类；通常直接使用 `QFileIconProvider`，仅在文件浏览器需要替换图标策略时派生。
- 核心输入：`QFileInfo`，它描述路径、文件类型、权限和文件系统状态。

## 3. API 速查

| API | 用途 |
|---|---|
| `icon(const QFileInfo &info)` | 为具体文件或目录返回图标。 |
| `icon(IconType type)` | 为计算机、桌面、磁盘、文件夹等通用位置返回图标。 |
| `type(const QFileInfo &info)` | 返回面向用户显示的文件类型字符串。 |
| `options()` / `setOptions()` | 读取或设置图标查询策略。 |
| `DontUseCustomDirectoryIcons` | 忽略目录自定义图标，换取稳定性能。 |
| `Computer` / `Desktop` / `Trashcan` / `Network` | 系统位置图标类别。 |
| `Drive` / `Folder` / `File` | 通用驱动器、目录与文件图标类别。 |

## 4. 关键用法

### 为自定义文件列表提供图标

```cpp
#include <QFileIconProvider>
#include <QFileInfo>

QFileIconProvider provider;
const QFileInfo info(u"/tmp/report.pdf"_s);
const QIcon icon = provider.icon(info);
const QString label = provider.type(info);
```

文件路径不存在时，`QFileInfo` 仍是可构造的对象，但图标和类型可能退化为通用结果。界面层不应以“图标为空”判断路径有效性，路径检查应使用 `QFileInfo::exists()` 等文件信息 API。

### 为远程或大量目录扫描优化

```cpp
QFileIconProvider provider;
provider.setOptions(
    QAbstractFileIconProvider::DontUseCustomDirectoryIcons);
```

此选项的语义不是换一个主题，而是禁止探测目录自定义图标。对于网络挂载、可移动介质或几千个目录的树视图，它可以避免 UI 因文件系统元数据查询而卡顿；代价是显示的目录图标不再体现用户的个性化设置。

### 自定义扩展名图标策略

派生时可重写 `icon(info)`：先根据业务扩展名、工作区状态或版本控制状态返回自定义 `QIcon`，其余路径交给基类/默认提供者。不要在该函数中同步读取大文件、请求网络服务或启动外部进程，因为模型通常会频繁调用它。

## 5. 使用场景

| 场景 | 建议 |
|---|---|
| 文件选择器、资源管理器、项目树 | 使用 `QFileIconProvider` 或将其交给文件系统模型。 |
| 特殊文件类型的品牌图标 | 继承后按 `QFileInfo` 规则覆盖 `icon(info)`。 |
| 远程目录和海量目录 | 启用 `DontUseCustomDirectoryIcons` 并缓存可复用结果。 |
| 只需固定系统图标 | 调用 `icon(Folder)`、`icon(Drive)` 等，不必伪造路径。 |
| 需要 MIME 类型或真实内容识别 | 图标提供者只负责表现；另用 `QMimeDatabase` 或业务解析。 |

## 6. 常见坑与经验

- `type(info)` 是用于界面显示的本地化文本，不是稳定的机器可读文件类别；不要据此写业务分支。
- 图标会受操作系统、当前主题和文件管理器策略影响，不能把像素外观当作跨平台约定。
- 缓存键至少应考虑文件/目录属性和主题变化；单按扩展名缓存会误伤可执行文件、符号链接或特殊目录。
- 默认实现涉及桌面平台资源，应在 GUI 线程为界面生成和使用 `QIcon`。

## 7. 知识点覆盖

- `QFileInfo` 驱动的文件表现层
- 抽象图标提供者与 `QFileIconProvider`
- 系统图标类别、主题与本地化类型名称
- 文件系统 I/O 对界面性能的影响
- 自定义策略与缓存边界
