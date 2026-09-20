# QPageSize

> Qt 6.11.1 · Qt GUI · 来自 `QPageSize`

## 1. 先建立直觉

`QPageSize` 表示“纸张有多大”，不是“内容如何排版”。A4、Letter、Legal、自定义标签纸、信封尺寸都可以用它表达；页边距、方向、可打印区域和内容矩形则属于 `QPageLayout` 或打印设备的职责。

它最容易被误用的地方，是把“纸张尺寸”和“横竖方向”混在一起。`QPageSize` 关注的是尺寸本身，构造时可以通过匹配策略把某个宽高识别成标准纸型；真正的 portrait/landscape 页面语义通常交给 `QPageLayout` 处理。

## 2. 类说明

- 头文件：`#include <QPageSize>`
- CMake：`Qt6::Gui`
- 类型性质：值类型，可复制、可移动、可交换
- 主要协作类：`QPageLayout`、`QPagedPaintDevice`、`QPdfWriter`、`QPrinter`
- 标准来源：PostScript PPD 标准纸型，并带有 Windows `DMPAPER` 映射

`QPageSize` 保存的不只是宽高，还可能保存标准纸型 id、定义单位、内部 key、展示名称和 Windows id。对于标准纸型，`definitionSize()` / `definitionUnits()` 会尽量保留标准定义的原始单位，例如 A 系列常以毫米定义，Letter 常以英寸定义。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `PageSizeId` | 标准纸型枚举，如 `A4`、`Letter`、`Legal`、`EnvelopeDL`、`Custom`。 |
| `Unit` | 尺寸单位：毫米、点、英寸、派卡、Didot、Cicero。 |
| `SizeMatchPolicy` | 自定义尺寸匹配标准纸型时的策略：模糊、允许方向互换、精确。 |
| `QPageSize()` | 创建无效页尺寸，常用于延迟赋值。 |
| `QPageSize(PageSizeId)` | 根据标准纸型创建，例如 `QPageSize(QPageSize::A4)`。 |
| `QPageSize(QSize, QString, SizeMatchPolicy)` | 用 point 尺寸创建，可尝试匹配标准纸型。 |
| `QPageSize(QSizeF, Unit, QString, SizeMatchPolicy)` | 用指定单位创建自定义或匹配后的标准纸型。 |
| `isValid()` | 判断对象是否表示有效尺寸。 |
| `id()` | 返回标准纸型 id；自定义或无法识别时通常为 `Custom` 或无效语义。 |
| `name()` | 返回面向用户的名称，适合 UI 展示。 |
| `key()` | 返回内部/PPD 风格 key，适合系统集成，不适合当作界面文案。 |
| `definitionSize()` | 返回纸型定义时的尺寸，单位由 `definitionUnits()` 指定。 |
| `size(Unit)` | 以指定单位返回宽高，适合布局计算。 |
| `sizePoints()` | 以 point 返回尺寸，适合绘图和 PDF。 |
| `sizePixels(int resolution)` | 按 DPI 转成像素，适合栅格化预览。 |
| `rect(Unit)` / `rectPoints()` / `rectPixels()` | 返回从 `(0,0)` 开始的页面矩形。 |
| `windowsId()` | 返回 Windows `DMPAPER` id；无映射时可能为 `0`。 |
| `isEquivalentTo()` | 判断两个尺寸是否在物理尺寸上等价。 |
| `operator==` | 判断对象是否相等，比“尺寸相近”更严格。 |
| 静态 `id(...)` | 从 Windows id、point 尺寸或指定单位尺寸反查标准纸型。 |
| 静态 `name/key/size/windowsId(...)` | 不构造对象也能查询标准纸型元数据。 |

## 4. 关键用法

### 选择标准纸型

```cpp
QPageSize pageSize(QPageSize::A4);
pageLayout.setPageSize(pageSize);
```

标准纸型优先使用 `PageSizeId`，这样比手写 `210 x 297 mm` 更稳定，也更容易映射到打印机和 PDF 元数据。

### 创建自定义纸张

```cpp
QPageSize label(QSizeF(100.0, 150.0),
                QPageSize::Millimeter,
                "100 x 150 mm Label",
                QPageSize::ExactMatch);
```

如果你真的需要自定义尺寸，可以给出清晰名称。`ExactMatch` 表示只有完全符合标准尺寸时才识别为标准纸型；否则更接近“我就是要这个自定义尺寸”的语义。

### 把物理尺寸转成预览像素

```cpp
const QSize previewSize = pageSize.sizePixels(144); // 144 DPI
QImage preview(previewSize, QImage::Format_ARGB32_Premultiplied);
```

屏幕预览应明确 DPI。不要把 point、像素和毫米混在一起，否则 PDF、打印和屏幕预览会出现比例不一致。

### 判断两个纸型是否物理等价

```cpp
if (a.isEquivalentTo(b)) {
    // 物理尺寸足够接近，可视为同一页面大小
}
```

`isEquivalentTo()` 关注尺寸等价；`operator==` 更像对象等价。两个对象可能尺寸等价，但名称、id 或来源不同。

## 5. 使用场景

- PDF 导出：为 `QPdfWriter` 或 `QPagedPaintDevice` 设置 A4、Letter 或自定义页面。
- 打印设置界面：列出常见纸型，同时保存用户自定义尺寸。
- 报表和发票：保证页面物理尺寸稳定，不被屏幕 DPI 影响。
- 标签、票据、信封：使用非标准或地区特定尺寸。
- 跨平台打印：在 Qt 标准纸型、PostScript key 和 Windows `DMPAPER` 之间做映射。

## 6. 常见坑与经验

- **纸张大小不等于页面布局。** 横向、页边距、完整矩形、可打印矩形应看 `QPageLayout`。
- **`name()` 和 `key()` 目的不同。** `name()` 给人看，`key()` 更偏系统/PPD 标识，不要拿 key 做本地化界面。
- **`windowsId()` 可能没有值。** 自定义尺寸或某些标准纸型不一定能映射到 Windows id。
- **匹配策略会影响 id。** `FuzzyOrientationMatch` 可能把宽高互换后识别为同一标准纸型；这对纸型识别很方便，但不应替代页面方向设置。
- **标准尺寸保留定义单位。** A4 的标准来源是毫米，Letter 常来自英寸；计算时用 `size(Unit)` 统一单位，不要硬编码换算。
- **像素尺寸必须带 DPI。** `sizePixels(300)` 和 `sizePixels(96)` 表示完全不同的栅格化目标。

## 7. 知识点覆盖

- 标准纸型、自定义纸型和无效纸型的区别
- point、毫米、英寸、像素与 DPI 的转换
- `QPageSize` 与 `QPageLayout` 的职责分离
- PostScript PPD key、用户展示名、Windows `DMPAPER` id 的不同用途
- 精确匹配、模糊匹配、方向匹配的取舍
- PDF、打印、预览和报表系统中的页面尺寸建模
