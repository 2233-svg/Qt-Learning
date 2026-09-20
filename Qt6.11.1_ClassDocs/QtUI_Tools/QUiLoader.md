# QUiLoader
> Qt 6.11.1 · Qt UI Tools · 来自 `QUiLoader`

## 1. 先建立直觉

`QUiLoader` 用来在运行时加载 Qt Designer 生成的 `.ui` 文件。和 `uic` 把 `.ui` 编译成 C++ 代码不同，`QUiLoader` 是运行时解释表单：从 `QIODevice` 读 XML，动态创建 widget、layout、action，并按 `.ui` 里的属性把界面搭起来。

它最适合“界面结构要晚一点才知道”的程序，例如插件宿主、表单设计器、低代码配置界面、工具软件的用户自定义面板。普通业务窗口如果结构固定，`uic` 生成类通常更安全、更快，也更容易重构。

## 2. 类说明

`QUiLoader` 本身不是 widget，而是工厂和加载器。它创建出来的根 widget 由调用者接收并负责安排所有权；`.ui` 内部子对象会按 Qt 对象树归属到对应父对象。

保留类说明：这些 API 来自 `QUiLoader`，它属于 Qt UI Tools 模块，服务于 QWidget/Designer `.ui` 运行时加载。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QUiLoader(QObject *parent = nullptr)` | 创建加载器对象。 |
| `load(QIODevice *device, QWidget *parentWidget = nullptr)` | 从设备读取 `.ui` 并返回根 widget。 |
| `errorString()` | `load()` 失败后读取人类可读错误。 |
| `addPluginPath(path)` | 添加自定义 widget 插件查找目录。 |
| `clearPluginPaths()` | 清空插件查找目录。 |
| `pluginPaths()` | 查看当前插件路径列表。 |
| `availableWidgets()` | 返回加载器当前能创建的 widget 类名。 |
| `availableLayouts()` | 返回加载器当前能创建的 layout 类名。 |
| `createWidget(className, parent, name)` | 虚函数：创建 widget，可在子类中拦截或替换。 |
| `createLayout(className, parent, name)` | 虚函数：创建 layout，可支持自定义布局策略。 |
| `createAction(parent, name)` | 虚函数：创建 action。 |
| `createActionGroup(parent, name)` | 虚函数：创建 action group。 |
| `setWorkingDirectory(dir)` | 设置相对资源路径的解析目录。 |
| `workingDirectory()` | 查询当前工作目录。 |
| `setLanguageChangeEnabled(enabled)` | 控制是否处理语言变化事件以刷新文本。 |
| `isLanguageChangeEnabled()` | 查询语言变化支持是否开启。 |

## 4. 典型流程

```cpp
QFile file(":/forms/preferences.ui");
if (!file.open(QIODevice::ReadOnly))
    return;

QUiLoader loader;
loader.setWorkingDirectory(QFileInfo(file).absoluteDir());

QWidget *page = loader.load(&file, parentWidget);
if (!page) {
    qWarning() << loader.errorString();
    return;
}

auto *nameEdit = page->findChild<QLineEdit *>("nameEdit");
```

动态加载后的对象没有编译期成员变量，所以 `objectName` 很重要。Designer 里给关键控件设置稳定名称，代码里用 `findChild<T*>()` 获取。

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 插件系统让插件提供 `.ui` | 宿主无需重新编译就能加载不同表单。 |
| 内部工具的可配置面板 | 表单可以随配置文件、脚本或项目模板变化。 |
| Qt Designer/预览器类软件 | 本来就需要按文件实时创建界面。 |
| 快速原型或主题实验 | 设计人员改 `.ui` 后重启即可看到结构变化。 |

## 6. 常见坑与经验

自定义 widget 不是“文件里写了类名就会自动存在”。要么把对应 Designer 插件放进插件路径，要么继承 `QUiLoader` 并重写 `createWidget()`，在遇到指定 `className` 时自己 new 出对象。

动态加载牺牲了类型安全。`ui->okButton` 这种编译期检查没有了，`findChild()` 写错名字会返回空指针。关键对象获取后要立即检查，失败时把 `.ui` 文件名、对象名和 `errorString()` 一起记录。

不要盲目加载不可信 `.ui`。它虽不是任意 C++ 代码，但会创建对象、设置属性、解析资源和插件路径；在插件目录可控性差的环境里，安全边界要更清楚。

`parentWidget` 不是“把加载出来的根 widget 塞进布局”。它只参与父子关系。你仍然需要把返回的根 widget 加到某个布局中，或作为窗口显示。

## 7. 知识点覆盖

- `.ui` 的两条路线：`uic` 编译期绑定与 `QUiLoader` 运行时加载。
- Qt 对象树、根 widget 所有权、`objectName` 查找。
- Designer 自定义 widget 插件机制。
- 相对资源路径和 `workingDirectory()`。
- 动态 UI 的类型安全、错误处理和安全边界。
