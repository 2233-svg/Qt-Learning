# Qt QStyleFactory 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QStyleFactory>`  
> 所属模块：`Qt6::Widgets`  
> 继承：无  
> 定位：样式工厂

## 1. QStyleFactory 解决什么问题

`QStyleFactory` 负责按名字创建样式对象。Qt 的样式不只有一种，平台样式、内置样式和插件样式都可能存在，而这个类就是它们的统一入口。

它本身不绘制界面，也不保存样式状态，主要做两件事：

1. 列出当前可用的样式键；
2. 根据键创建 `QStyle` 对象。

```text
QStyleFactory
  ├─ keys()
  └─ create(key)
```

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 查询可用样式

```cpp
#include <QApplication>
#include <QStyleFactory>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    qDebug() << QStyleFactory::keys();
    return 0;
}
```

### 2.3 按键创建样式

```cpp
QStyle *style = QStyleFactory::create("Fusion");
if (style)
    QApplication::setStyle(style);
```

`create()` 返回的是新建样式对象。项目里通常要么立刻交给 `QApplication::setStyle()`，要么自己保管并在合适时机释放。

## 3. 核心使用模型

### 3.1 `keys()` 是“有哪些可选项”

它返回当前工厂能创建的样式键列表。平台不同，可见的键也不同。

### 3.2 `create()` 是“把键变成对象”

`create()` 会先检查内置样式，再查样式插件。匹配成功就返回对应 `QStyle *`，找不到就返回 `nullptr`。

键是大小写不敏感的，所以 `"Fusion"` 和 `"fusion"` 通常都能工作。

### 3.3 它常和 `QApplication::setStyle()` 连用

最典型的场景就是：

```cpp
QApplication::setStyle(QStyleFactory::create("Fusion"));
```

这样可以在程序启动时统一切换风格，而不用依赖平台默认样式。

## 4. 使用场景

- 提供主题切换或样式选择功能；
- 在跨平台项目里固定基础样式；
- 启动时强制选择某个样式；
- 列出当前环境支持哪些样式。

## 5. 常见误区

### 5.1 以为它负责样式修改

不负责。它只负责创建样式对象。

### 5.2 以为键名大小写敏感

不是。键名大小写不敏感。

### 5.3 以为所有平台都支持同样的键

不对。可用键和平台、插件、构建环境有关，应该先调用 `keys()`。

### 5.4 以为 `create()` 一定成功

不会。找不到匹配项时会返回 `nullptr`，必须判空。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 静态公共成员 | `create(const QString &key)` | 按样式键创建一个 `QStyle` 对象。 | 键大小写不敏感；找不到时返回 `nullptr`。 |
| 静态公共成员 | `keys()` | 返回当前工厂可创建的样式键列表。 | 可用项和平台、插件、构建环境有关。 |

## 7. 一句话总结

`QStyleFactory` 是样式对象的名字入口，适合用来列出可用风格并按键创建 `QStyle`。
