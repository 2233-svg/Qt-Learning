# QAbstractFormBuilder 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QAbstractFormBuilder>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QAbstractFormBuilder` 提供从 Qt `.ui` XML 文件构造 QWidget 树、以及把 QWidget 树保存回 `.ui` XML 的基础实现。它面向嵌入 Qt Widgets Designer 的应用、自定义组件和需要控制 UI 文件构造过程的工具。

它不是通常意义上的“布局构建器”，也不是 Qt Designer 主窗口接口。它关心的是 UI 文件格式：

- `load()`：从任意 `QIODevice` 读取 `.ui` XML，创建 widget 树；
- `save()`：把 widget 树写成标准 `.ui` XML；
- `workingDirectory()`：决定 UI 中相对资源路径的解析基准；
- `errorString()`：说明最近一次 load 失败的原因。

这个类不建议直接作为业务入口。运行时仅需加载 `.ui` 时，优先考虑 `QUiLoader`；需要基于 UI 文件构造自定义组件或扩展 form builder 行为时，使用其具体派生类 `QFormBuilder`。

## 从 `.ui` 创建界面

```cpp
#include <QFile>
#include <QFormBuilder>

QFile file(":/forms/settings.ui");
if (!file.open(QIODevice::ReadOnly))
    return;

QFormBuilder builder;
QWidget *form = builder.load(&file, parentWidget);
if (!form) {
    qWarning() << builder.errorString();
    return;
}
```

`load()` 返回空指针表示加载失败。不要只检查 `QFile::open()`，XML 格式、widget 类、资源引用等问题都可能导致构造失败，此时读取 `errorString()`。

传给 `load()` 的 parent 会成为根 widget 的父对象。若 UI 根 widget 需要独立窗口语义，则根据你的界面嵌入方式选择合适 parent，而不是一律传 `nullptr`。

## 相对资源路径

UI 文件可能引用图标、图片或其它资源。`workingDirectory` 是 form builder 用于解析相对路径的基准目录：

```cpp
QFormBuilder builder;
builder.setWorkingDirectory(QDir("D:/app/forms"));
```

当 UI 文件从内存、网络、压缩包或非文件系统 `QIODevice` 读取时，builder 无法自动从设备路径推断资源目录，显式设置 working directory 尤其重要。

## 保存时为什么需要过滤属性

`save()` 会把 widget 的 XML 表示写入设备，但和 Qt Widgets Designer 原生保存不同，它会写出所有属性值。原因是普通 QWidget 的 Qt 属性系统并不普遍保存“该属性是否被用户改过”的状态。

这会产生两个实际问题：

- 输出的 `.ui` 可能非常冗余；
- 某些属性彼此依赖或只适合运行时，全部保存后重新加载可能产生意外行为。

如果要生成可长期维护的 `.ui`，应在保存前过滤不需要的属性，或在派生类中重写 `computeProperties()` 返回明确的属性集合。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAbstractFormBuilder()` | 创建 form builder 基础对象。 | 通常改用具体的 `QFormBuilder`，不要把抽象基础实现当作完整业务工具。 |
| 析构 | `virtual ~QAbstractFormBuilder()` | 销毁 form builder。 | builder 不拥有已成功返回给调用方的根 widget 的外部使用权；按 parent 和 Qt 对象树管理界面。 |
| 错误信息 | `errorString() const` | 返回最近一次 `load()` 失败的人类可读说明。 | 只对加载问题有意义；`load()` 返回空指针时立即读取，避免后续调用覆盖上下文。 |
| 加载 UI | `load(QIODevice *device, QWidget *parent = nullptr)` | 读取 UI XML 并构造根 widget。 | 失败返回 `nullptr`；检查设备已可读、资源路径和 `errorString()`。 |
| 保存 UI | `save(QIODevice *device, QWidget *widget)` | 将 widget 树写为标准 `.ui` XML。 | 会写出所有属性值，输出可能冗余；必要时过滤属性后再保存。 |
| 设置资源基准 | `setWorkingDirectory(const QDir &directory)` | 设置相对资源引用的解析目录。 | 从内存或非本地文件设备加载 UI 时尤其重要。 |
| 查询资源基准 | `workingDirectory() const` | 返回当前相对资源解析目录。 | 保持与 UI 文件实际资源位置一致。 |

## 易错点

1. `QAbstractFormBuilder` 不等于 `QBoxLayout` 等布局工具，它处理 `.ui` XML 与 QWidget 树的互转。
2. `load()` 失败不只可能是文件打不开；XML、资源、未知 widget 类都可能导致失败，务必读 `errorString()`。
3. `save()` 不会像 Designer 原生编辑器那样只保存被修改属性，可能写出大量属性。
4. UI 包含相对图片或图标时，不能忽略 `workingDirectory()`。
5. 一般运行时动态加载需求优先用 `QUiLoader`；需要 form builder 扩展能力时使用 `QFormBuilder`。

### 一句话总结

`QAbstractFormBuilder` 是 Qt `.ui` XML 与 QWidget 树之间的基础构造器：用它加载、保存和定位相对资源；保存时尤其要注意它会写出全部属性值。
