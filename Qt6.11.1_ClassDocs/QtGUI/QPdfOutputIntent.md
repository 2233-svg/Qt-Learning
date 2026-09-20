# QPdfOutputIntent

> Qt 6.11.1 · Qt GUI · 来自 `QPdfOutputIntent`

## 1. 先建立直觉

`QPdfOutputIntent` 描述 PDF 文档的目标输出条件：这份 PDF 是按什么色彩配置文件、什么印刷/显示条件来准备的。它常和 `QPdfWriter` 配合，尤其在需要 PDF/X-4 这类面向印刷交换的格式时很重要。

它不是“把所有颜色自动转成正确颜色”的按钮。它更像 PDF 元数据里的承诺：我声明这份文档的颜色应按这个 ICC profile 和输出条件解释。应用程序仍然要保证写入 PDF 的颜色空间、图片和绘制内容与这个 profile 匹配。

## 2. 类说明

- 头文件：`#include <QPdfOutputIntent>`
- CMake：`Qt6::Gui`
- 类型性质：值类型，可复制、可移动、可交换
- 主要协作类：`QPdfWriter`
- 默认语义：sRGB IEC61966 v2.1 with black scaling

输出意图通常包含四部分：人可读的输出条件、机器可识别的条件标识符、注册表 URL、以及实际的 `QColorSpace` 输出 profile。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPdfOutputIntent()` | 创建默认输出意图，默认使用 sRGB v2 相关配置。 |
| `outputCondition()` / `setOutputCondition()` | 读写人类可读的输出条件说明。 |
| `outputConditionIdentifier()` / `setOutputConditionIdentifier()` | 读写输出条件的标识符；有注册表时应匹配注册条目。 |
| `registryName()` / `setRegistryName()` | 读写特征化条件注册表 URL，默认通常指向 color.org。 |
| `outputProfile()` / `setOutputProfile()` | 读写输出设备色彩配置文件，类型为 `QColorSpace`。 |
| `swap()` | 快速交换两个输出意图。 |
| 拷贝/移动构造与赋值 | 按值传递和保存输出意图配置。 |

## 4. 关键用法

### 为 PDF 写入器设置输出意图

```cpp
QPdfOutputIntent intent;
intent.setOutputCondition("sRGB IEC61966 v2.1 with black scaling");
intent.setOutputConditionIdentifier("sRGB_IEC61966-2-1_black_scaled");
intent.setRegistryName(QUrl("http://www.color.org"));
intent.setOutputProfile(QColorSpace::SRgb);

writer.setOutputIntent(intent);
```

这类配置通常在创建 PDF 页面前完成。若目标是印刷工作流，应使用印厂或规范要求的 ICC profile，而不是随意声明 sRGB。

### 区分说明文字与标识符

`outputCondition()` 面向人，例如“FOGRA39 coated paper”；`outputConditionIdentifier()` 面向规范和注册表，例如某个标准化 reference condition 名称。两者可以表达同一个意图，但用途不同。

### PDF/X-4 场景

PDF/X-4 要求文档色彩声明和实际内容保持一致。调用 `setOutputProfile()` 只设置输出意图；你仍然要检查图片、渐变、绘制颜色、透明度以及外部资源是否符合目标色域和输出条件。

## 5. 使用场景

- 生成 PDF/X-4 或面向印刷交换的 PDF。
- 为企业报表、出版物、票据或广告素材声明目标色彩环境。
- 将 `QPdfWriter` 输出接入印厂、预检工具或归档流程。
- 在生成 PDF 时嵌入标准 sRGB 或特定印刷 ICC profile。
- 为色彩敏感内容保留可验证的输出条件元数据。

## 6. 常见坑与经验

- **输出意图不等于色彩转换。** 它声明目标 profile，但不会自动修正你已经画进去的错误颜色。
- **PDF/X 要求更严格。** 如果声明了某 profile，文档中的所有颜色规格也要匹配；这是应用层责任。
- **标识符和注册表要成对考虑。** 设置了 `registryName()` 后，`outputConditionIdentifier()` 应能在对应注册表里找到意义。
- **默认 sRGB 适合屏幕和通用 PDF。** 面向印刷时通常需要印厂给出的 CMYK/ICC 工作条件。
- **`QColorSpace` 可能无效或不合适。** 设置 profile 前检查来源，避免把占位或错误 profile 写入正式文档。
- **人可读条件不是唯一标识。** 说明文字可以本地化或描述性更强，但自动化流程更依赖 identifier。

## 7. 知识点覆盖

- PDF 输出意图、ICC profile 和色彩管理
- PDF/X-4 对输出条件和文档颜色一致性的要求
- `QColorSpace` 与 PDF 元数据的关系
- `outputCondition`、`outputConditionIdentifier`、`registryName` 的分工
- sRGB 默认配置与印刷 profile 的差异
- `QPdfWriter` 生成色彩敏感 PDF 时的责任边界
