# QQuickItem::ItemChangeData：itemChange() 的联合附加数据

> Qt 6.11.1 · 定义于 `QQuickItem` · 模块：`Qt6::Quick`

`QQuickItem::ItemChangeData` 是传给 `QQuickItem::itemChange()` 的 union。它本身不携带类型标签，具体应该读取哪个成员完全由同一次回调里的 `ItemChange` 枚举决定。

## 使用场景

覆写 `itemChange(change, data)` 时，Qt Quick 会在父子关系、窗口归属、焦点、可见性、透明度、变换等状态改变后通知 Item。`ItemChangeData` 提供这一变化的附加值：有时是相关 Item，有时是新窗口，有时是布尔或数值。

```cpp
void MyItem::itemChange(ItemChange change, const ItemChangeData &data)
{
    if (change == ItemSceneChange)
        m_window = data.window;
    else if (change == ItemVisibleHasChanged)
        m_visibleNow = data.boolValue;
}
```

## 边界

这是 union，不是 `QVariant`。读取与 `change` 不匹配的成员没有意义，也容易把随机位模式解释成指针或数值。不要保存对 `data` 的引用；若需要长期使用，拷贝其中与当前 change 对应的具体值。

`item` 指针可能表示被添加/移除的子项，也可能表示新父项，语义同样由 `ItemChange` 决定。`window` 在 Item 离开窗口时可以为 `nullptr`，释放图形资源或断开窗口信号时必须处理空值。

## API 速查表

| 成员 | 语义与边界 |
|---|---|
| `item` | 对应子项添加/移除或父项变化时的相关 `QQuickItem *`；具体含义由 `ItemChange` 决定。 |
| `window` | 对应场景/窗口变化时的新 `QQuickWindow *`；移出窗口时为 `nullptr`。 |
| `realValue` | 对应 `opacity`、`rotation`、`scale` 或设备像素比变化等数值结果。 |
| `boolValue` | 对应 `visible`、`enabled`、`activeFocus`、`antialiasing` 等布尔状态变化。 |
| `QQuickItem::itemChange(change, data)` | 唯一正常消费入口；先判断 `change`，再读取匹配成员。 |
