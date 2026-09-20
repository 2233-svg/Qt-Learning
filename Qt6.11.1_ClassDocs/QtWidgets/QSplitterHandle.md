# QSplitterHandle

> Qt 6.11.1 · Qt Widgets · 来自 `QSplitterHandle`

## 1. 先建立直觉

`QSplitterHandle` 是 `QSplitter` 中间那条可以拖动的分隔柄。多数应用不需要直接创建它，因为 `QSplitter` 会按子控件数量自动管理；真正需要关心它，通常是为了改变分隔柄的外观、命中区域或拖动交互。

它的定位很窄：不负责保存布局状态，不负责决定各面板尺寸策略，也不负责添加子控件。它只代表一个“可拖动的手柄”。如果你想持久化用户调整后的左右宽度，应看 `QSplitter::saveState()` / `restoreState()`；如果你想定制手柄绘制或拖动行为，才进入 `QSplitterHandle`。

## 2. 类说明

`QSplitterHandle` 继承自 `QWidget`，由 `QSplitter::createHandle()` 创建，并和所属 splitter 绑定。它知道自己的方向，也可以通过 `splitter()` 回到拥有它的 `QSplitter`。

常见做法是继承 `QSplitter` 并重写 `createHandle()`，返回自定义的 `QSplitterHandle` 子类。这样比事后查找内部 handle 更稳，因为 Qt 能在 splitter 重建 handle 时继续使用你的实现。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSplitterHandle(Qt::Orientation, QSplitter *)` | 构造一个指定方向、归属某个 splitter 的分隔柄。通常只在自定义 `QSplitter::createHandle()` 中使用。 |
| `orientation()` | 获取分隔方向。水平 splitter 的 handle 垂直显示，拖动改变左右面板；垂直 splitter 的 handle 水平显示，拖动改变上下区域。 |
| `splitter()` | 返回所属 `QSplitter`，便于读取相邻控件、调用 `moveSplitter()` 或查询尺寸。 |
| `closestLegalPosition(int)` | 把目标位置修正到 splitter 允许的位置，避免拖到越界或突破最小尺寸。 |
| `moveSplitter(int)` | 请求 splitter 把当前 handle 移动到指定位置。自定义拖动逻辑时比直接改 geometry 更正确。 |
| `opaqueResize()` | 判断拖动时是否实时调整子控件尺寸；关闭时通常只显示预览线，释放后才应用。 |
| `sizeHint()` | 返回 handle 的建议尺寸。可重写以加宽可拖动区域。 |
| `paintEvent()` | 绘制 handle。自定义视觉样式时常重写。 |
| `mouseMoveEvent()` | 响应拖动。高级场景可拦截并加入吸附、限制或提示。 |
| `mousePressEvent()` / `mouseReleaseEvent()` | 处理拖动起止状态。适合做高亮、拖动提示或埋点。 |
| `resizeEvent()` | handle 尺寸变化时更新内部子控件位置，例如放一个折叠按钮。 |

## 4. 关键用法

最常见的扩展不是直接 new 一个 handle 塞进 splitter，而是这样分层：

```cpp
class FancySplitter : public QSplitter {
protected:
    QSplitterHandle *createHandle() override
    {
        return new FancySplitterHandle(orientation(), this);
    }
};
```

在 handle 内部，如果你只是要改变视觉，优先通过 `QStyle` 绘制，让平台主题仍然接管细节：

```cpp
void FancySplitterHandle::paintEvent(QPaintEvent *)
{
    QStyleOption opt;
    opt.initFrom(this);

    QPainter p(this);
    style()->drawControl(QStyle::CE_Splitter, &opt, &p, this);
}
```

如果你想把“拖到某个位置自动吸附”做进去，可以在 `mouseMoveEvent()` 中计算目标值，然后先交给 `closestLegalPosition()` 修正，再调用 `moveSplitter()`。这里的重点是让 `QSplitter` 继续负责约束、折叠规则和子控件尺寸分配。

## 5. 使用场景

适合使用 `QSplitterHandle` 的场景包括：IDE 左侧项目树和编辑区之间的可拖边界、图像查看器中的参数面板折叠条、数据库管理工具中结果表与日志窗格的高度调整，以及需要在 handle 上放置折叠按钮或拖动提示的专业工具界面。

不适合把它当作普通分隔线使用。静态分隔线用 `QFrame` 更直接；需要布局留白用 `QSpacerItem`；需要用户调大小才考虑 `QSplitter` / `QSplitterHandle`。

## 6. 常见坑与经验

`QSplitterHandle` 的宽度和可拖动命中区域不一定等于你画出来的线宽。很多成熟应用会画一条细线，但把 `sizeHint()` 做得略宽，让鼠标更容易抓住。

不要在 handle 内直接移动相邻 widget。splitter 内部维护尺寸列表、折叠规则、最小尺寸和 RTL 布局方向，绕开它很容易造成状态不一致。

如果要加折叠按钮，按钮应作为 handle 的子控件，并在 `resizeEvent()` 中摆放；不要把按钮放在 splitter 的普通子控件列表中，否则它会参与分区布局。
