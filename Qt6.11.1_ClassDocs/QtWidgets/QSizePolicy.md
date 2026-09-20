# QSizePolicy

> Qt 6.11.1 · Qt Widgets · 来自 `QSizePolicy`

## 1. 先建立直觉

`QSizePolicy` 是 QWidget 告诉布局系统“我愿意怎么变大、怎么变小”的规则。布局不是只看 `sizeHint()`，还会看水平/垂直 policy、stretch、height-for-width 和控件类型。

它适合解决按钮不该变高、文本框应横向扩展、侧边栏保持宽度、隐藏控件是否保留空间等问题。多数布局疑难，最后都会落到 size hint、minimum/maximum size、size policy 和 stretch 的组合上。

## 2. 类说明

- 头文件：`#include <QSizePolicy>`
- 模块：`Qt6::Widgets`
- 继承自：无
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

这是值类型，通过 `QWidget::setSizePolicy()` 使用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSizePolicy()` | 创建默认策略。 |
| `QSizePolicy(horizontal, vertical, type)` | 创建水平/垂直策略和控件类型。 |
| `horizontalPolicy()` / `setHorizontalPolicy()` | 水平方向伸缩策略。 |
| `verticalPolicy()` / `setVerticalPolicy()` | 垂直方向伸缩策略。 |
| `horizontalStretch()` / `setHorizontalStretch()` | 水平拉伸因子。 |
| `verticalStretch()` / `setVerticalStretch()` | 垂直拉伸因子。 |
| `expandingDirections()` | 返回愿意扩展的方向。 |
| `setHeightForWidth()` / `hasHeightForWidth()` | 高度是否依赖宽度，常见于自动换行文本。 |
| `setWidthForHeight()` / `hasWidthForHeight()` | 宽度是否依赖高度，较少见。 |
| `setRetainSizeWhenHidden()` / `retainSizeWhenHidden()` | 隐藏后是否仍占布局空间。 |
| `setControlType()` / `controlType()` | 告诉 style 这是什么控件类型。 |
| `transpose()` / `transposed()` | 交换水平和垂直策略。 |
| `operator QVariant()` | 转为 QVariant。 |
| `operator==` / `operator!=` | 比较策略。 |
| `qHash()` / stream operators | 哈希和序列化支持。 |

## 4. 知识点覆盖

`Fixed` 表示尺寸基本固定；`Preferred` 是普通控件默认感觉；`Expanding` 表示愿意吃掉额外空间；`MinimumExpanding` 表示至少要 size hint，并且也想扩展；`Ignored` 会弱化 size hint，让布局尽量分配空间。

stretch 只有在同一布局方向上多个控件都参与分配时才明显。policy 决定“能不能伸”，stretch 决定“都能伸时谁多拿”。

`retainSizeWhenHidden` 适合切换可见性但不希望界面跳动的场景，例如高级选项暂时隐藏但空间仍保留。普通隐藏通常不保留空间。

## 5. 常见坑与经验

- `setFixedSize()` 会强力覆盖布局弹性，少用。
- 只改 stretch 不改 policy，有时看不出效果，因为控件根本不愿扩展。
- `QLabel` 自动换行常需要 height-for-width，布局高度才会随宽度变化。
- `Ignored` 很激进，适合绘图区域等特殊控件，不适合普通表单。
- 控件类型会影响 style 的间距判断，复杂自定义控件可设置合适 control type。
