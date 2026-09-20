# Qt QGraphicsItemGroup 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QGraphicsItemGroup>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QGraphicsItemGroup`  
> 定位：图元分组容器

## 1. QGraphicsItemGroup 解决什么问题

`QGraphicsItemGroup` 用来把一组图元当成一个整体处理。常见场景是演示工具、流程图编辑器、画布编辑器里，用户选中多个 item 后想一起移动、缩放、复制或统一控制显示状态。

它解决的问题不是“存一堆 item”，而是“让一堆现有 item 共享一个上层父项，并且整体移动时还能保持各自的场景相对位置和变换”。

```text
QGraphicsItem
  └─ QGraphicsItemGroup
```

如果你只是想把 item 放到另一个 item 下面当子项，直接 `setParentItem()` 也可以；但如果你想把一组现有 item 以“组合”的语义管理，`QGraphicsItemGroup` 更贴切。

## 2. 最小可用代码

### 2.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

### 2.2 用 createItemGroup() 分组

```cpp
#include <QApplication>
#include <QGraphicsEllipseItem>
#include <QGraphicsRectItem>
#include <QGraphicsScene>
#include <QGraphicsView>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QGraphicsScene scene;
    auto *rect = scene.addRect(0, 0, 80, 40);
    auto *ellipse = scene.addEllipse(90, 0, 60, 60);
    auto *group = scene.createItemGroup({rect, ellipse});
    group->setPos(30, 30);

    QGraphicsView view(&scene);
    view.show();

    return app.exec();
}
```

### 2.3 手动分组和拆组

```cpp
scene.addItem(group);
group->addToGroup(rect);
group->addToGroup(ellipse);

group->removeFromGroup(rect);
scene.destroyItemGroup(group);
```

## 3. 核心使用模型

### 3.1 分组后仍保持场景相对位置

`addToGroup()` 的关键语义是：把 item 及其子项重新挂到 group 下面，但它们在场景中的相对位置和变换保持不变。你看到的视觉位置不会因为分组这一步突然跳掉。

### 3.2 拆组也保持场景相对位置

`removeFromGroup()` 会把 item 挂回 group 的父项下，或者没有父项时变成顶层 item。它同样保持 item 的场景相对位置和变换。

### 3.3 分组容器把一整组当成一个 item

组的 `boundingRect()` 会覆盖所有子项的包围范围。换句话说，组能参与场景命中、选中和可见性判断，但它的几何是整组子项几何的组合。

### 3.4 适合批量操作，不适合复杂业务容器

如果你只是想表达层级归属，普通父子 item 就够了。`QGraphicsItemGroup` 更适合“临时组合一组项并整体操作”。

## 4. 适合用在哪里

- 画布里把多个元素打包为一个整体；
- 选择多项后统一移动或旋转；
- 演示文档、流程图、白板编辑器；
- 需要临时组合和解除组合的交互。

## 5. 常见误区

### 5.1 把分组当复制

不会复制 item。它只是重新组织父子关系。

### 5.2 以为 addToGroup() 会改变场景中的视觉位置

不会。它会保持场景相对位置和变换。

### 5.3 以为 removeFromGroup() 会把 item 丢回任意地方

不会。它会回到 group 的父项下，或者没有父项时变成顶层 item。

### 5.4 以为组一定需要自己 delete

如果你是通过 `QGraphicsScene::createItemGroup()` 创建的，通常由场景管理它；拆组时用 `destroyItemGroup()` 更符合语义。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `Type` | 返回组图元的类型编号。 | 用于 `type()` 判断或类型转换。 |
| 构造 | `QGraphicsItemGroup(QGraphicsItem *parent = nullptr)` | 创建一个图元分组容器。 | 常由 `QGraphicsScene::createItemGroup()` 间接创建。 |
| 析构 | `~QGraphicsItemGroup()` | 销毁分组容器。 | 如果是场景创建的组，通常由场景管理生命周期。 |
| 添加 | `addToGroup(QGraphicsItem *item)` | 把一个图元及其子项加入分组。 | 会重设父子关系，但保持场景相对位置和变换。 |
| 移除 | `removeFromGroup(QGraphicsItem *item)` | 把一个图元从分组中移除。 | 会重新挂到组的父项下，或变成顶层项。 |
| 几何 | `boundingRect() const` | 返回整个组的包围矩形。 | 包含所有子项的范围。 |
| 遮挡 | `isObscuredBy(const QGraphicsItem *item) const` | 判断是否被其它 item 遮挡。 | 影响可见性和绘制优化。 |
| 遮挡 | `opaqueArea() const` | 返回组的不透明区域。 | 用于遮挡判断。 |
| 绘制 | `paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)` | 组本身的绘制入口。 | 通常组本身不画内容，主要依赖子项。 |
| 类型查询 | `type() const` | 返回组的图元类型。 | 可用于 `qgraphicsitem_cast`。 |

## 7. 一句话总结

`QGraphicsItemGroup` 是把现有图元组合成一个整体的容器，重点在于保持场景位置和变换不变，方便批量操作和临时分组。
