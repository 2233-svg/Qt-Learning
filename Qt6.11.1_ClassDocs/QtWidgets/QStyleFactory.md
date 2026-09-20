# QStyleFactory

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleFactory`

## 1. 先建立直觉

`QStyleFactory` 是按名字创建 Qt style 的工厂。它能告诉你当前环境有哪些 style key，也能根据 key 创建 `QStyle` 实例。

它常用于应用启动时切换主题、偏好设置中的外观选择、测试不同平台风格。

## 2. 类说明

`QStyleFactory` 不是 QObject，也不需要实例化。它提供静态函数 `keys()` 和 `create()`。

可用 style 取决于平台、Qt 构建和插件。比如 `Fusion` 通常较稳定，平台原生 style 的名字和可用性则可能不同。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `keys()` | 返回当前可创建的 style key 列表。 |
| `create(const QString &key)` | 按 key 创建 style；失败返回 `nullptr`。 |
| `QApplication::setStyle(QStyle *)` | 把创建出的 style 应用到应用。 |
| `QApplication::style()` | 获取当前 style。 |
| `QProxyStyle` | 可包装 factory 创建出的 style 再做微调。 |

## 4. 关键用法

```cpp
const QStringList styles = QStyleFactory::keys();

if (QStyle *style = QStyleFactory::create("Fusion"))
    QApplication::setStyle(style);
```

给用户偏好设置：

```cpp
for (const QString &key : QStyleFactory::keys())
    combo->addItem(key);
```

应用选择时要处理失败：

```cpp
auto *style = QStyleFactory::create(selectedKey);
if (style)
    qApp->setStyle(style);
```

## 5. 使用场景

适合主题切换、外观设置页、跨平台 UI 测试、固定使用 Fusion 风格、创建 base style 给 `QProxyStyle` 包装。

如果只是想改变颜色，不一定要换 style；用 palette 或 stylesheet 可能更直接。

## 6. 常见坑与经验

不要假设某个 key 在所有系统都存在。发布前用 `keys()` 检查，或者提供 fallback。

`create()` 返回的是新对象，交给 `QApplication::setStyle()` 后通常由应用管理。

换 style 会影响整个 Widgets 应用的尺寸、绘制、标准图标和行为提示，不只是颜色变化。
