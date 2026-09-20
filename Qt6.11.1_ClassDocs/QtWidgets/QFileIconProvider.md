# QFileIconProvider

> Qt 6.11.1 · Qt Widgets · 来自 `QFileIconProvider`

## 1. 先建立直觉

`QFileIconProvider` 是 Widgets 模块里的文件图标提供者。它根据文件类型、目录、驱动器、桌面、回收站等信息返回合适的 `QIcon`，常被文件浏览器、文件选择器、`QFileSystemModel` 相关视图使用。

它不是文件读取类，也不负责列目录。它只回答一个问题：这个 `QFileInfo` 或文件系统类别应该显示什么图标。

## 2. 类说明

`QFileIconProvider` 继承自 `QAbstractFileIconProvider`。默认实现会尽量使用当前平台的文件图标风格，使 Qt 文件界面看起来像系统原生应用。

如果你要做文件管理器、资源选择器、项目树，通常可以直接用默认 provider；如果产品需要特殊文件类型图标、云同步状态叠加、版本控制状态，你可以继承它并重写 `icon()`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFileIconProvider()` | 创建默认文件图标提供者。 |
| `icon(IconType)` | 按标准类别取图标，例如文件夹、文件、计算机、桌面、回收站等。 |
| `icon(const QFileInfo &)` | 按具体文件信息取图标，通常根据后缀、目录属性或平台关联决定。 |
| `QAbstractFileIconProvider::IconType` | 标准图标类别枚举。 |
| `QFileSystemModel::setIconProvider()` | 把自定义 provider 接入文件系统模型。 |

## 4. 关键用法

接入 `QFileSystemModel`：

```cpp
auto *model = new QFileSystemModel(this);
model->setIconProvider(new QFileIconProvider);
model->setRootPath(projectRoot);
```

自定义某些后缀图标：

```cpp
class ProjectIconProvider : public QFileIconProvider {
public:
    QIcon icon(const QFileInfo &info) const override
    {
        if (info.suffix() == "qrc")
            return QIcon(":/icons/resource-file.svg");
        return QFileIconProvider::icon(info);
    }
};
```

这里保留基类回退很重要，否则目录、驱动器和系统特殊位置的原生图标会丢失。

## 5. 使用场景

适合文件树、打开最近项目列表、资源管理器、项目浏览器、插件资源选择器、导入向导、文件对话框的自定义模型，以及需要让文件类型视觉上更容易区分的工具。

如果只是按钮上固定一个图标，不需要 `QFileIconProvider`；直接用 `QIcon`。如果要枚举文件，用 `QDirIterator`、`QFileSystemModel` 或 `QDir`。

## 6. 常见坑与经验

获取平台文件图标可能不是完全免费的。大型目录里如果每一项都同步请求复杂图标，滚动可能变慢。自定义 provider 中应避免做磁盘扫描、网络请求或读取文件内容。

`icon(QFileInfo)` 应该是纯显示策略，不要顺手改变文件或模型状态。视图绘制过程中调用它时，副作用会非常难排查。

跨平台图标差异是正常的。文件关联、主题图标、驱动器图标在 Windows、macOS、Linux 上不完全一致，产品如果需要强一致视觉，就用自己的图标体系覆盖关键类型。
