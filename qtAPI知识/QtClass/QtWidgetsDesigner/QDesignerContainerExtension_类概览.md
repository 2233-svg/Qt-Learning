# QDesignerContainerExtension 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDesignerContainerExtension>`  
> 所属模块：`Qt6::Designer`  
> 继承：无

## 它解决什么问题

`QDesignerContainerExtension` 让 Qt Widgets Designer 能编辑自定义的多页容器控件。一个 widget 即使运行时支持页面、选项卡或堆叠页面，Designer 也不会自动知道如何添加页、插入页、切换当前页或删除页；这个接口把这些页面管理能力暴露给 Designer。

它适用于行为类似 `QTabWidget`、`QStackedWidget`、向导页容器的自定义控件。它不负责绘制控件，也不负责保存 UI 文件，而是让 Designer 的上下文菜单、对象树与页面编辑操作能够正确调用你的容器 API。

仅在插件接口的 `isContainer()` 中返回 `true` 不够。那只是声明该 widget 可以容纳子 widget；要让“添加页面”“插入页面”“移除当前页”等 Designer 操作真正工作，还要实现本接口并通过 `QExtensionFactory` 注册。

## 需要保持一致的页面模型

Designer 会把你实现的这些函数当成同一份页面模型的不同视图：

- `count()`：一共有几页；
- `widget(index)`：某个索引对应哪一页；
- `currentIndex()` / `setCurrentIndex()`：当前展示的是哪页；
- `addWidget()` / `insertWidget()` / `remove()`：怎样改变页面集合。

这些结果必须与自定义容器实际运行时的行为一致。比如 `insertWidget(0, page)` 后，`count()` 应增加，`widget(0)` 应返回新页，索引和当前页状态也要符合你的控件约定。

```cpp
class MyStackExtension final
    : public QObject
    , public QDesignerContainerExtension
{
    Q_OBJECT
    Q_INTERFACES(QDesignerContainerExtension)

public:
    explicit MyStackExtension(MyStack *stack, QObject *parent = nullptr)
        : QObject(parent), stack(stack) {}

    int count() const override { return stack->count(); }
    QWidget *widget(int index) const override { return stack->widget(index); }
    int currentIndex() const override { return stack->currentIndex(); }
    void setCurrentIndex(int index) override { stack->setCurrentIndex(index); }
    void addWidget(QWidget *page) override { stack->addWidget(page); }
    void insertWidget(int index, QWidget *page) override
    {
        stack->insertWidget(index, page);
    }
    void remove(int index) override { stack->removePage(index); }
    bool canAddWidget() const override { return true; }
    bool canRemove(int index) const override { return index >= 0 && count() > 1; }

private:
    MyStack *stack;
};
```

## 固定单页容器

像 `QScrollArea`、`QDockWidget` 这类只能持有一个固定内容 widget 的容器，不应让 Designer 显示“添加页”“删除页”操作。此时 `canAddWidget()` 和 `canRemove(index)` 应返回 `false`，即使你仍实现了页查询相关 API。

## 注册方式

实现类要继承 `QObject` 和接口，并使用 `Q_INTERFACES(QDesignerContainerExtension)`。随后用 `QExtensionFactory` 注册：

```cpp
manager->registerExtensions(
    new MyExtensionFactory(manager),
    Q_TYPEID(QDesignerContainerExtension));
```

factory 仅在对象是你的容器且 IID 匹配时创建 `MyStackExtension`。Designer 在需要编辑页面时才会请求它。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 析构 | `virtual ~QDesignerContainerExtension()` | 销毁容器扩展接口。 | 通常通过 QObject 父子关系管理具体扩展对象。 |
| 页面追加 | `addWidget(QWidget *page)` | 把页面追加到容器页面列表末尾。 | 必须同步修改容器真实页面集合，而不是只维护扩展内部列表。 |
| 可添加判断 | `canAddWidget() const` | 告诉 Designer 是否启用添加、插入页面操作。 | 单页固定容器应返回 `false`。 |
| 可删除判断 | `canRemove(int index) const` | 告诉 Designer 指定页面是否可以删除。 | 处理索引范围和最低页数约束，例如必须至少保留一页。 |
| 页数 | `count() const` | 返回容器当前页数。 | 要和 `widget(index)`、插入、删除操作保持一致。 |
| 当前页 | `currentIndex() const` | 返回当前可见或选中的页面索引。 | 无当前页时用你的容器约定的无效值；不要返回越界索引。 |
| 页面插入 | `insertWidget(int index, QWidget *page)` | 在指定索引插入页面。 | 明确处理 `index` 边界，且要正确设置 page 的父对象或交给容器 API 处理。 |
| 页面删除 | `remove(int index)` | 从容器移除指定索引的页面。 | 明确“移除”是否销毁 page；要与自定义容器运行时所有权规则一致。 |
| 当前页切换 | `setCurrentIndex(int index)` | 将指定索引设为当前页。 | 应验证索引；切换后 Designer 和容器画面要同步。 |
| 页面读取 | `widget(int index) const` | 返回指定索引的页面 widget。 | 越界时返回 `nullptr`，不要返回错误页面。 |

## 易错点

1. 只实现 `isContainer()` 而没有注册 `QDesignerContainerExtension`，Designer 往往无法正确编辑多页结构。
2. 不要让扩展维护一份与控件分离的“影子页面列表”；所有 API 都应代理到真实容器状态。
3. `canRemove()` 不只是界面提示，它决定 Designer 是否启用删除页面动作；必须反映业务限制。
4. `remove()` 的所有权语义由容器决定。不要无意中既让父对象删除 page，又手动重复释放它。

### 一句话总结

`QDesignerContainerExtension` 是自定义多页容器在 Designer 中的页面管理适配层：它把真实容器的页数、当前页、增删插入能力同步给 Designer。
