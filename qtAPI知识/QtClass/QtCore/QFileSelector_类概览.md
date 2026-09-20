# Qt QFileSelector 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFileSelector>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QFileSelector`  
> 定位：按平台、语言环境和自定义 selector 在同一套资源目录中选择最合适的文件变体

## 1. QFileSelector 解决什么问题

`QFileSelector` 解决“同一个逻辑文件在不同运行环境下有不同版本”的问题。它让代码始终请求基础路径，而变体文件放在带 `+selector` 名称的子目录里：

```text
data/defaults.conf
data/+linux/defaults.conf
data/+windows/defaults.conf
data/+linux/+zh_CN/defaults.conf
```

代码只写：

```cpp
QFileSelector selector;
QFile file(selector.select("data/defaults.conf"));
```

运行时，`QFileSelector` 根据当前平台、locale、环境变量和你设置的 extra selectors，返回最匹配的实际路径。

它适合：

- 平台差异配置，例如 Windows 和 Linux 使用不同默认配置；
- locale 差异资源，例如 `+zh_CN`、`+en_GB` 的文本或图片；
- 同一应用在不同设备、渠道、用户角色或实验组使用不同资源；
- 需要在部署之后仍能通过添加文件变体改变行为的场景。

它不适合：

- 所有环境永远只使用同一个文件；
- 性能极敏感的热路径中频繁做文件选择；
- 根据文件内容、MIME 类型或业务数据动态选择；
- 没有基础文件、只想在 `+selector` 目录中找变体的布局。

## 2. 基础文件是 fallback，也是入口

`select(filePath)` 的输入是基础文件路径。只有基础文件存在时，selector 才会寻找变体；如果基础文件不存在，函数直接返回原始 `filePath`。

```cpp
QFileSelector selector;
const QString path = selector.select("images/background.png");
```

推荐目录布局：

```text
images/background.png              # 必须有，用作默认或错误处理 fallback
images/+linux/background.png
images/+windows/background.png
images/+admin/background.png
images/+admin/+linux/background.png
```

不要只提供：

```text
images/+linux/background.png
```

如果 `images/background.png` 不存在，`select("images/background.png")` 不会因为 `+linux` 版本存在就返回它，而是返回原始基础路径。这样设计的目的，是让应用始终有一个明确的默认文件或错误处理文件。

`QFileSelector` 只返回路径，不打开文件。选择之后仍要用 `QFile`、`QImageReader`、`QQmlComponent` 等实际消费者检查读取是否成功。

## 3. selector 目录规则

变体目录的命名格式是 `+` 加 selector 名称：

```text
data/+android/defaults.conf
data/+ios/defaults.conf
data/+linux/+en_GB/defaults.conf
```

查找时，`QFileSelector` 从基础文件所在目录开始，看是否存在匹配当前 active selectors 的 `+selector` 子目录；如果存在同名文件，就优先使用变体文件。selector 目录可以嵌套，表示多个条件同时满足。

例如：

```text
images/background.png
images/+android/background.png
images/+android/+en_GB/background.png
```

在 Android 且 locale 为 `en_GB` 时，可能选择更具体的 `+android/+en_GB/background.png`。如果只有 `+android` 存在，则选择 Android 变体；如果没有任何匹配变体，则返回基础文件。

selector 是目录名，不是文件名后缀。`background+linux.png` 不会参与 `QFileSelector` 的规则。

## 4. 默认 selector 来源

Qt 默认提供两类 selector：

| 来源 | 示例 |
| --- | --- |
| 平台 | `android`、`ios`、`osx`、`darwin`、`mac`、`macos`、`linux`、`qnx`、`unix`、`windows` |
| locale | `QLocale().name()`，例如 `zh_CN`、`en_GB` |

在 Linux 上，如果 Qt 能识别发行版，还可能加入发行版名称，例如 `debian`、`fedora` 或 `opensuse`。文档说明平台列表不是穷尽列表，因此业务代码不应把 `allSelectors()` 的内容写死成固定全集。

selector 初始集合会在第一次使用时计算一次。当前 locale、平台和环境变量变化后，不应假设已有进程中的静态 selector 会自动刷新。

## 5. `QT_FILE_SELECTORS` 环境变量

环境变量 `QT_FILE_SELECTORS` 可以添加额外 selector，格式是逗号分隔：

```text
QT_FILE_SELECTORS=staging,tablet
```

它适合：

- 测试或预发布环境加载不同资源；
- 打包同一程序后通过运行环境选择渠道资源；
- 命令行或启动器注入实验变体。

边界：

- 该环境变量只读取一次；
- 如果应用运行中修改环境变量，selector 不会可靠更新；
- 它属于进程级输入，影响所有使用静态 selector 的 `QFileSelector` 实例；
- 不要让不可信环境变量直接决定敏感文件路径。

## 6. extra selectors：每个实例自己的运行时条件

应用可以通过 `setExtraSelectors()` 设置自定义 selector：

```cpp
QFileSelector selector;
selector.setExtraSelectors(QStringList{
    QStringLiteral("admin"),
    QStringLiteral("tablet")
});

const QString path = selector.select("images/background.png");
```

extra selectors 适合表达应用自己的运行时状态，例如：

- 当前用户角色；
- 主题或品牌；
- A/B 实验分组；
- 硬件能力或屏幕类别；
- 命令行选项解析后的模式。

每个 `QFileSelector` 实例都有自己的 extra selectors；静态 selector 集合与其他实例相同。修改 extra selector 列表后，后续 `select()` 调用会使用新列表，可能返回不同路径。已经打开的文件不会自动切换。

## 7. 多个 selector 同时匹配时的优先级

当多个 selector 都能应用于同一个基础文件时，文档规定“第一个匹配的 selector 被选中”。检查顺序是：

1. `setExtraSelectors()` 设置的 selector，按列表顺序；
2. `QT_FILE_SELECTORS` 环境变量中的 selector，从左到右；
3. locale；
4. platform。

这意味着 extra selectors 优先于平台 selector。

例如：

```text
images/background.png
images/+linux/background.png
images/+windows/background.png
images/+admin/background.png
images/+admin/+linux/background.png
```

如果程序运行在 Linux 且设置了 `admin`：

- 第一层优先匹配 `+admin`；
- 在 `+admin` 目录内继续根据剩余 selector 找更具体变体；
- 如果存在 `+admin/+linux/background.png`，最终选择它；
- 如果不存在该嵌套文件，则可能选择 `+admin/background.png`。

如果没有 `admin`，Linux 上会选择 `+linux/background.png`。

优先级会影响目录布局。把 selector 命名成“更强的业务条件”时，通常放在 extra selectors 中；把环境级或平台级条件交给默认 selector 和环境变量。

## 8. QString 和 QUrl 两种 select

### 8.1 `select(QString)`

```cpp
const QString selected =
    selector.select("data/defaults.conf");
```

返回值是被选中的路径。如果没有可用变体，返回原始路径；如果原始基础文件不存在，也返回原始路径。

这意味着调用方仍然必须检查文件是否能打开：

```cpp
QFile file(selector.select("data/defaults.conf"));
if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    qWarning() << file.errorString();
    return;
}
```

`select()` 的返回值不是“文件存在证明”，只是选择算法的结果。

### 8.2 `select(QUrl)`

```cpp
const QUrl selectedUrl =
    selector.select(QUrl("qrc:/themes/default.css"));
```

`QUrl` 重载只对 `file` 和 `qrc` scheme 应用选择。其他 scheme 会原样返回：

```cpp
QUrl remote("https://example.com/defaults.conf");
Q_ASSERT(selector.select(remote) == remote);
```

对 `file` 或 `qrc` URL，选择只应用到 URL 的 path 部分，其他 URL 组成部分保持不变。它适合 QML、资源系统和需要 URL 参数的接口，但不改变“基础文件必须存在才能选择变体”的规则。

## 9. 性能和部署边界

`QFileSelector` 要检查文件是否存在，并尝试多个 selector 组合。文档建议避免在性能关键路径中使用它。

合理做法：

- 启动时或状态切换时选择一次，并缓存结果；
- 对 UI 图标、配置、模板等相对静态资源使用；
- extra selector 变化时重新选择相关资源；
- 不在每帧绘制、每个网络包处理或大量循环中反复调用。

选择器目录布局有部署优势：同一代码可以带多套资源，运行时才选择适合的版本。文档也提到，将来某些 selector 可能被标记为部署时静态并在部署步骤优化处理；因此不要依赖选择算法产生副作用，应该只把它当作“返回更合适路径”的纯查询。

## 10. 常见误区

### 10.1 只放变体文件，不放基础文件

`select()` 要求基础文件存在，基础路径也是 fallback。只放 `+linux/defaults.conf` 而不放 `defaults.conf`，选择不会如你所愿。

### 10.2 把 selector 写成文件后缀

规则是目录名 `+selector`，不是文件名后缀。`logo+dark.png` 不会被自动选择。

### 10.3 以为环境变量会运行时刷新

`QT_FILE_SELECTORS` 只读取一次。运行中改变环境变量不能作为可靠的资源切换机制；需要动态切换时使用 `setExtraSelectors()`。

### 10.4 以为 select 会打开或验证文件

`select()` 返回路径或 URL。真正加载文件时，仍要检查打开、解析和读取结果。

### 10.5 忽略优先级

extra selectors 排在环境变量、locale 和 platform 之前。一个 `+admin` 目录可能压过 `+linux` 或 `+windows`。目录设计前先确认优先级。

## 11. API 逐项说明

### 11.1 生命周期

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QFileSelector(QObject *parent = nullptr)` | 创建选择器实例。 | 每个实例有自己的 extra selectors；静态 selector 集合与其他实例一致。 |
| `~QFileSelector()` | 销毁选择器。 | 不影响已经返回的路径，也不会关闭任何文件。 |

### 11.2 选择文件

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `select(const QString &filePath) const` | 根据当前 selector 返回选中的路径。 | 基础文件不存在时返回原始路径；没有变体时也返回原始路径。 |
| `select(const QUrl &filePath) const` | 对 `file` 或 `qrc` URL 的 path 应用选择。 | 其他 scheme 原样返回；URL 其他部分保持不变。 |

### 11.3 selector 列表

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `extraSelectors() const` | 返回当前实例的 extra selectors。 | 只包含程序设置的额外 selector，不是完整列表。 |
| `setExtraSelectors(const QStringList &list)` | 设置当前实例的 extra selectors。 | 优先级最高，按列表顺序检查；影响后续 `select()`。 |
| `allSelectors() const` | 返回当前实例完整、有序的 selector 列表。 | 包含 extra、环境变量、locale 和 platform；静态部分首次使用后不应期待自动刷新。 |

### 11.4 相关继承能力

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QObject` parent | 管理 `QFileSelector` 生命周期。 | 选择器没有自己的信号；通常栈上创建或作为资源管理对象成员即可。 |
| `moveToThread()` | 改变对象线程亲和性。 | `select()` 本身是查询型调用；跨线程共享同一 QObject 仍应避免无保护并发访问。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 定位 | `QFileSelector` | 按 active selectors 选择文件变体。 | 只返回路径，不打开文件。 |
| 构造 | `QFileSelector(parent)` | 创建选择器实例。 | static selectors 共享，extra selectors 属于实例。 |
| 析构 | `~QFileSelector()` | 销毁选择器。 | 不影响已返回路径。 |
| 选择 | `select(QString)` | 返回选中的文件路径。 | 基础文件不存在时返回原始路径。 |
| 选择 | `select(QUrl)` | 对 file/qrc URL 选择变体。 | 非 file/qrc scheme 原样返回。 |
| extra | `extraSelectors()` | 读取实例 extra selectors。 | 不包含平台、locale 或环境变量 selector。 |
| extra | `setExtraSelectors(QStringList)` | 设置实例 extra selectors。 | 优先级最高，按列表顺序生效。 |
| 全部 | `allSelectors()` | 返回完整有序 selector 列表。 | 顺序决定冲突选择结果。 |
| 目录规则 | `+selector` | 在基础文件同级目录中放置变体。 | selector 是目录名，不是文件名后缀。 |
| fallback | 基础文件 | 默认文件和选择入口。 | 没有基础文件就不会只选变体。 |
| 环境变量 | `QT_FILE_SELECTORS` | 添加进程级 selector。 | 逗号分隔，只读取一次。 |
| 默认 selector | platform | 根据运行平台加入 selector。 | 平台名称集合不是穷尽列表。 |
| 默认 selector | locale | 使用 `QLocale().name()`。 | locale selector 在 platform 之前检查。 |
| 优先级 | extra -> env -> locale -> platform | 冲突时先匹配靠前来源。 | extra selector 会压过平台变体。 |
| 性能 | 文件存在性查询 | 选择过程会访问文件系统或资源系统。 | 不适合高频热路径。 |

### 一句话总结

`QFileSelector` 让代码始终请求基础文件，把平台、locale 和业务差异藏到 `+selector` 目录中。基础文件必须存在，extra selectors 优先级最高，环境变量只读一次，`select()` 只是返回候选路径，真正加载文件仍要检查失败。

