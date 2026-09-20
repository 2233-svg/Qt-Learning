# QIcon

> Qt 6.11.1 · Qt GUI · 来自 `QIcon`

## 1. 先建立直觉

`QIcon` 不是一张图片，而是一组可根据**尺寸、设备像素比、交互模式和开关状态**选择最佳资源的图标描述。一个图标可以同时拥有 16/24/32 像素、Normal/Disabled/Active/Selected、On/Off，以及 raster、SVG 或主题图标来源。

因此控件优先接受 `QIcon` 而不是 `QPixmap`：按钮知道自己禁用、悬停、选中还是 checked，Qt 就能让 icon engine 选择/生成正确外观。需要真正绘制或缓存像素时，再调用 `pixmap()` 或 `paint()`。

## 2. 类说明

- 头文件：`#include <QIcon>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：隐式共享值类型；保存资源集合或 `QIconEngine`。
- 不直接处理像素；显示资源最终为 `QPixmap`，所以一般在 GUI 线程使用。
- 主题图标配置是进程级状态：主题名、搜索路径和 fallback 会影响全应用的 `fromTheme()` 结果。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QIcon(fileName)` / `QIcon(pixmap)` | 用单一文件或 pixmap 创建图标 |
| `QIcon(engine)` | 以自定义 `QIconEngine` 创建高级图标 |
| `addFile()` | 为某个尺寸、Mode、State 添加资源文件 |
| `addPixmap()` | 为某个尺寸、Mode、State 添加 pixmap |
| `pixmap(size[, dpr], mode, state)` | 请求指定显示条件下的最终 pixmap |
| `paint(painter, rect, alignment, mode, state)` | 直接在目标矩形中绘制图标 |
| `actualSize()` | 查询请求尺寸下真正可提供的逻辑尺寸 |
| `availableSizes()` | 查询特定 Mode/State 的可用尺寸 |
| `isNull()` | 判断是否没有可用 icon 数据 |
| `isMask()` / `setIsMask()` | 标识图标是否作为单色 mask 语义使用 |
| `name()` | 查询主题图标或引擎记录的名称（若有） |
| `cacheKey()` | 判断 icon 数据是否更改，适合本地缓存失效 |
| `fromTheme(name[, fallback])` | 从 Freedesktop 风格主题取图标 |
| `fromTheme(ThemeIcon[, fallback])` | Qt 6.7 起用类型安全的通用主题图标枚举 |
| `hasThemeIcon()` | 预先检查主题是否提供名称/枚举图标 |
| `setThemeName()` / `themeName()` | 配置/查询当前应用主题 |
| `setThemeSearchPaths()` / `themeSearchPaths()` | 配置/查询主题目录 |
| `setFallbackThemeName()` | 当前主题缺图时的后备主题 |
| `setFallbackSearchPaths()` | 当前主题系统不可用时的后备查找路径 |
| `swap()` / QVariant / 数据流运算符 | 管理、存储或序列化图标值 |

## 4. Mode 与 State 的区别

| 维度 | 值 | 它表达什么 |
| --- | --- | --- |
| `Mode` | `Normal` | 可用且未处于特殊交互状态 |
|  | `Disabled` | 功能不可用，通常由控件自动请求 |
|  | `Active` | 悬停、按下或当前活动交互状态 |
|  | `Selected` | 项目被选中，例如列表选中项 |
| `State` | `Off` | 非开关状态或未选中 |
|  | `On` | 可切换控件/动作处于开启或 checked |

两者相乘而非替代。例如被禁用的 checked 工具按钮可能请求 `Disabled + On`。

## 5. 关键用法

### 给多状态工具按钮准备资源

```cpp
QIcon favorite;
favorite.addFile(":/icons/star-outline.svg", {}, QIcon::Normal, QIcon::Off);
favorite.addFile(":/icons/star-filled.svg",  {}, QIcon::Normal, QIcon::On);

ui->favoriteButton->setCheckable(true);
ui->favoriteButton->setIcon(favorite);
```

控件会随 checked 状态自动请求 On/Off 变体。若只添加 Normal/Off，Qt 会尽力从已有资源生成其他状态，但颜色、对比度和语义未必符合设计意图。

### 正确处理高 DPI pixmap 请求

```cpp
const qreal dpr = devicePixelRatioF();
const QPixmap pm = icon.pixmap(QSize(20, 20), dpr,
                               QIcon::Normal, QIcon::Off);
painter.drawPixmap(target.topLeft(), pm);
```

`size` 是逻辑像素，`dpr` 告诉图标引擎应产出多少物理像素。不要手工把 `20` 乘 dpr 再调用旧重载，否则可能得到双重缩放或错误的逻辑大小。控件 API 通常已自行处理 DPR，只有自绘时才需要显式考虑。

### 使用主题图标并提供品牌回退

```cpp
const QIcon fallback(":/icons/document-save.svg");
const QIcon save = QIcon::fromTheme(
    QIcon::ThemeIcon::DocumentSave, fallback);
saveAction->setIcon(save);
```

Qt 6.7 的 `ThemeIcon` 避免手写 `"document-save"` 这类字符串。主题图标能融入桌面环境，但不能作为唯一资产：Windows、打包应用、定制主题或极简系统可能没有相应主题，永远提供 fallback。

### 在启动阶段配置主题搜索

```cpp
QIcon::setThemeSearchPaths({
    QCoreApplication::applicationDirPath() + "/icons",
    ":/icon-themes"
});
QIcon::setThemeName("MyApp");
QIcon::setFallbackThemeName("hicolor");
```

这是进程级策略，应在创建大量控件和调用 `fromTheme()` 前完成。运行中换主题时，已有 `QIcon` 是否重取资源取决于来源和控件重绘路径；产品级动态换肤应集中管理并显式刷新 UI。

## 6. 使用场景

- `QAction`、菜单、工具栏、按钮和项目视图的可访问状态图标。
- 同时维护普通/禁用/选中/checked 的品牌图标。
- 按图标主题规范融入 Linux/桌面环境，同时提供应用自带回退。
- 高 DPI 自绘控件或图标预览器。

## 7. 常见坑与经验

- **加载顺序会固定引擎类型。** 第一个添加的资源会影响 icon engine 的选择；不要在同一个图标里随意混入不兼容来源，尤其是 SVG 与普通 raster 的处理期待不同。
- **不要把 disabled 效果完全交给默认生成。** 它可用，但品牌或无障碍对比要求高时应提供设计过的 Disabled 资源。
- **`availableSizes()` 是某一状态的集合。** 查询 `Normal/Off` 得到的列表不保证适用于 `On` 或 `Selected`。
- **`actualSize()` 可能小于请求。** raster 资源没有合适大图时，Qt 不会无条件放大到请求尺寸；布局要容忍真实大小。
- **主题路径不是资源文件路径列表。** 它们应是 icon theme 的目录根，且包含 `index.theme` 等主题结构。
- **`cacheKey()` 不代表渲染结果。** 它不含请求尺寸、DPR、状态和主题环境；自己的 pixmap 缓存键必须包含这些因素。
- **`isMask()` 只是语义标记。** 不会自动把多彩图变成单色，也不替代正确的图标着色策略。

## 8. 知识点覆盖

多状态图标、图标主题、主题回退、高 DPI、SVG 与 raster、QIconEngine、控件状态、缓存键、进程级主题配置、无障碍视觉状态。
