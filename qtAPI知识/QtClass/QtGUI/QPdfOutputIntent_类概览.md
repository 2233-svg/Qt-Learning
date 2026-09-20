# QPdfOutputIntent：声明 PDF 面向的印刷输出条件

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.8  
> 头文件：`#include <QPdfOutputIntent>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`

`QPdfOutputIntent` 是交给 `QPdfWriter::setOutputIntent()` 的值对象，用来描述 PDF 的绘制数据是针对哪一种印刷输出条件准备的。它保存 ICC 输出 profile、给人阅读的条件说明、机器可引用的条件标识符，以及可选的特性化注册表 URL。

它不进行颜色转换、不校验 PDF/X 合规性，也不会改变已经交给 `QPainter` 的颜色。它只是把“本文件的目标印刷条件是什么”写成可嵌入 PDF 的色彩管理元数据。

## 它适合什么场景

普通屏幕阅读 PDF 通常可以使用默认输出意图。面向印刷厂、归档流程或 PDF/X 交付时，则需要选择与实际输出工作流相符的 ICC profile 和条件标识：

```cpp
QColorSpace coatedProfile = QColorSpace::fromIccProfile(iccBytes);

QPdfOutputIntent intent;
intent.setOutputProfile(coatedProfile);
intent.setOutputCondition("Coated printing condition");
intent.setOutputConditionIdentifier("My-Coated-ICC");
intent.setRegistryName(QUrl("https://example.invalid/color-registry"));

QPdfWriter writer("proof.pdf");
writer.setColorModel(QPdfWriter::ColorModel::CMYK);
writer.setOutputIntent(intent);
```

`QPdfOutputIntent` 要在开始 `QPainter` 绘制前配置给 writer。PDF 的颜色模型、源 `QColor` / `QColorSpace` 和 profile 必须由生成方一起规划；单独给文件附加 output intent 并不会把 RGB 内容变成正确的印刷颜色。

## 四项数据分别代表什么

| 字段 | 含义 |
| --- | --- |
| `outputProfile` | 目标输出设备/印刷条件的 `QColorSpace`，通常承载 ICC profile。 |
| `outputCondition` | 给操作人员看的简短条件说明。 |
| `outputConditionIdentifier` | 条件的标识符；若设置注册表，应与该注册表中的引用名称匹配。 |
| `registryName` | 描述该条件的特性化注册表 URL。 |

默认对象已有 sRGB v2 相关默认值：说明为 `sRGB IEC61966 v2.1 with black scaling`，标识符为 `sRGB_IEC61966-2-1_black_scaled`，注册表为 `http://www.color.org`，profile 为可用的 sRGB v2 profile。默认值对普通 PDF 有意义，但不能据此推断文件满足某个印刷规范。

## PDF/X-4 的关键边界

当以 PDF/X-4 为目标并设置 `outputProfile` 时，文档中的**所有颜色规格**必须与该 profile 的颜色空间相匹配。这是应用程序的责任。

因此下面的组合并不自动成立：

```cpp
writer.setColorModel(QPdfWriter::ColorModel::CMYK);
writer.setOutputIntent(cmykIntent);
// 之后仍可能有不匹配的图像、渐变、嵌入内容或颜色规格。
```

`ColorModel::CMYK` 会要求 writer 以 CMYK 写出颜色，但它不等价于从业务素材到 PDF/X 的完整印前转换与预检。交付前仍应使用目标工作流的验证工具检查 profile、嵌入图像、字体和 PDF/X 约束。

## 值语义与生命周期

该类是隐式共享值类型：复制、赋值、移动和 `swap()` 都可用于组装配置；`QPdfWriter::setOutputIntent()` 接收常量引用，但应用应把传入后 writer 内部状态视为独立配置，不应依赖后续修改原对象能同步到 writer。

它不属于 `QObject`，没有父对象、事件循环或线程亲和性。作为纯配置数据可以按值传递；真正的 PDF 写入仍应由同一线程内的 `QPdfWriter`、`QPainter` 和输出设备协调。

## 常见错误

- 把 output intent 当作颜色转换器：它描述目标，不会修正绘制内容。
- 设置了注册表 URL，却给出与该注册表无关的标识符：外部色彩工作流无法可靠解析条件。
- 用 `QColorSpace()` 的无效/不匹配 profile 生成印刷交付：先验证 `QColorSpace` 来源和目标印刷条件。
- 仅凭设置 `ColorModel::CMYK` 和 output intent 声称 PDF/X-4 合规：还必须保证每个颜色规格匹配 profile 并完成外部预检。
- 在 painter 已开始后才修改意图：应在文档首个绘制命令前完成配置。

## API 速查表

| API | 语义与使用边界 |
| --- | --- |
| `QPdfOutputIntent()` | 构造默认 sRGB 输出意图；适合普通输出的起点，不代表印刷规范合规。 |
| 拷贝/移动构造、赋值 | 隐式共享值语义，便于按值传递配置。 |
| `swap(QPdfOutputIntent &)` | 高效交换两个输出意图配置。 |
| `outputProfile()` | 返回目标输出设备的 `QColorSpace` / ICC profile。 |
| `setOutputProfile(const QColorSpace &)` | 设置输出 profile；PDF/X-4 下应用必须保证文件所有颜色规格与它的颜色空间匹配。 |
| `outputCondition()` | 返回给人阅读的印刷条件说明。 |
| `setOutputCondition(const QString &)` | 设置简短、可读的目标输出条件说明。 |
| `outputConditionIdentifier()` | 返回印刷条件标识符。 |
| `setOutputConditionIdentifier(const QString &)` | 设置条件标识符；设置了 registry 时应匹配其条目的引用名。 |
| `registryName()` | 返回特性化注册表 URL。 |
| `setRegistryName(const QUrl &)` | 设置条件注册表 URL；它是元数据引用，不会联网下载 profile。 |
| `QPdfWriter::setOutputIntent()` | 将该意图附给 PDF writer；应在 `QPainter` 开始前调用。 |
