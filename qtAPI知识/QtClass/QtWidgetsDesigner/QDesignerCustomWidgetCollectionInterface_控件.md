# QDesignerCustomWidgetCollectionInterface 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerCustomWidgetCollectionInterface>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerCustomWidgetCollectionInterface` 用于把多个自定义 widget 插件接口打包到同一个 Qt Designer 插件动态库中。单个自定义控件可以直接由一个实现 `QDesignerCustomWidgetInterface` 的插件对象导出；当一个库里有一组相关控件时，collection 接口让 Designer 一次拿到它们的全部接口列表。

它解决的不是“创建控件集合 UI”，也不是替代 `QDesignerCustomWidgetInterface`。collection 只是插件发现层的聚合器：

```text
一个 Designer 插件库
    -> 一个 collection plugin 对象
        -> 多个 QDesignerCustomWidgetInterface 对象
            -> 多个实际 QWidget 子类
```

例如，一个图表库可以把折线图、柱状图、饼图三个 Designer 控件放进同一个插件 DLL，通过 collection 统一导出。

## 实现方式

collection 插件通常同时继承 `QObject` 和本接口，在构造函数里创建各个单控件插件接口对象，并把它们放进列表。每个接口对象通常以 collection 为父对象，由 QObject 父子关系管理。

```cpp
class ChartWidgetsPlugin final
    : public QObject
    , public QDesignerCustomWidgetCollectionInterface
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID
        "org.qt-project.Qt.QDesignerCustomWidgetCollectionInterface")
    Q_INTERFACES(QDesignerCustomWidgetCollectionInterface)

public:
    explicit ChartWidgetsPlugin(QObject *parent = nullptr)
        : QObject(parent)
    {
        widgets.append(new LineChartPlugin(this));
        widgets.append(new BarChartPlugin(this));
        widgets.append(new PieChartPlugin(this));
    }

    QList<QDesignerCustomWidgetInterface *> customWidgets() const override
    {
        return widgets;
    }

private:
    QList<QDesignerCustomWidgetInterface *> widgets;
};
```

每个 `LineChartPlugin` 等对象仍需独立实现 `QDesignerCustomWidgetInterface`，包括 `name()`、`createWidget()`、`includeFile()` 等。collection 不会替它们生成任何控件描述。

## 什么时候需要它

适合使用 collection 的情况：

- 一个插件库中包含多个同类控件；
- 希望它们共享资源、版本号、构建目标和安装位置；
- 希望 Designer 只加载一个插件库就发现整组控件。

只有一个自定义控件时，直接导出 `QDesignerCustomWidgetInterface` 通常更简单。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QDesignerCustomWidgetCollectionInterface()` | 销毁 collection 接口对象。 | 通过接口指针释放派生对象时依赖虚析构。 |
| 纯虚接口 | `QList<QDesignerCustomWidgetInterface *> customWidgets() const` | 返回该插件库中所有自定义 widget 接口对象。 | 返回的是接口指针列表；每个指针必须在 Designer 使用期间保持有效。 |

## 易错点

1. collection 不是 widget 本体，也不是普通 `QList<QWidget *>`；它收集的是自定义控件插件接口。
2. 不能只返回临时创建的接口对象。`customWidgets()` 返回后，Designer 仍会使用这些接口，因此它们需要有稳定生命周期。
3. collection 只需要一个 `Q_PLUGIN_METADATA` 导出点；列表中各单控件接口对象不应各自再作为独立插件入口导出。
4. 每个子接口仍要正确实现 `name()`、`includeFile()`、`createWidget()` 等；collection 不会替你补齐这些信息。

### 一句话总结

`QDesignerCustomWidgetCollectionInterface` 用一个插件入口导出多个 `QDesignerCustomWidgetInterface`，适合把一组相关自定义控件打包到同一个 Designer 插件库。
