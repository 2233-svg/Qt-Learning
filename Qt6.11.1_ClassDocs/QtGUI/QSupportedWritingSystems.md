# QSupportedWritingSystems

> Qt 6.11.1 · Qt GUI · 来自 `QSupportedWritingSystems`

## 1. 先建立直觉

`QSupportedWritingSystems` 是一个紧凑的“字体声明支持哪些大类书写系统”的集合。它以 `QFontDatabase::WritingSystem` 为键保存布尔值，主要给字体数据库、字体引擎或插件实现者描述能力。

它不是字符串语言检测器，也不能证明具体字符可画。比如“支持简体中文”只是粗粒度元数据；罕见字、emoji 组合、变体选择符是否有效仍应检查具体字体和具体文本。

## 2. 类说明

- 头文件：`#include <QSupportedWritingSystems>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：轻量值类型；只保存 `WritingSystem -> bool` 状态。
- 关联类型：枚举定义在 `QFontDatabase`；一般应用开发中更常查询 `QFontDatabase::writingSystems()` 或 `QRawFont::supportedWritingSystems()`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QSupportedWritingSystems()` | 创建所有书写系统均未标记支持的集合 |
| `setSupported(writingSystem, true)` | 标记支持某一书写系统 |
| `setSupported(writingSystem, false)` | 清除某一书写系统的支持标记 |
| `supported(writingSystem)` | 查询对应标记是否为真 |
| 拷贝构造、赋值 | 复制这份能力集合 |
| `QFontDatabase::WritingSystem` | 枚举 Latin、Arabic、SimplifiedChinese、Japanese 等书写系统 |

## 4. 关键用法

### 在字体插件中声明能力

```cpp
QSupportedWritingSystems systems;
systems.setSupported(QFontDatabase::Latin);
systems.setSupported(QFontDatabase::SimplifiedChinese);
systems.setSupported(QFontDatabase::Japanese);
```

这是声明“该字体/后端面向这些书写系统”，适合插件或字体发现代码向 Qt 汇报元数据。它不装载字体，也不会改变 `QFont` 的回退策略。

### 作为过滤信息而不是最终校验

```cpp
if (systems.supported(QFontDatabase::Arabic))
    showArabicPreviewOption();
```

这种筛选适合减少字体选择器中的噪声。但当用户输入真正的阿拉伯文字时，仍须靠正常字体匹配和塑形；要验证某个码点，使用 `QRawFont::supportsCharacter()`，要验证整段文字，使用 `QTextLayout`。

## 5. 使用场景

- `QFontDatabase` 相关插件、字体引擎或内部字体元数据实现。
- 字体浏览器中按大类文字系统筛选和展示。
- 为预览界面选择对应书写系统的示例文本。

## 6. 常见坑与经验

- **书写系统不等于语言。** Latin 可服务多种语言；中文、日文、韩文共享许多 CJK 字符，不能仅靠这个枚举决定本地化字体。
- **支持标记不等于 glyph 覆盖。** 罕见字符、私用区、emoji 与组合序列需要更具体的验证。
- **不要把它用于文本方向。** RTL/LTR 由 Unicode bidi 与 `QTextOption` 等布局规则决定，不由是否支持 Arabic 简化替代。
- **这是能力描述，不是配置入口。** 不能用它给应用添加字体或指定 fallback；那些由 `QFontDatabase` 的注册与回退 API 完成。

## 7. 知识点覆盖

书写系统、字体元数据、粗粒度能力声明、语言与脚本差异、字符覆盖、复杂文本塑形、字体插件接口。
