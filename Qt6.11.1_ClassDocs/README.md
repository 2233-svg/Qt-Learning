# Qt 6.11.1 C++ 公开类知识库

这套文档根据本机 Qt Assistant 随附的 Qt 6.11.1 类页整理，每个公开 C++ 类对应一个独立 Markdown 文件。正文直接说明类的用途、工作方式、API 参数、组合方式、示例和常见问题。

## 覆盖范围

共生成 **1119** 个类文档，来源是 `D:/QTforGui/qt/Docs/Qt-6.11.1` 中标题为 `Class | Qt ...` 的 C++ 类页。覆盖 Qt Core、Gui、Widgets、Network、Quick、Multimedia、SQL 等已安装模块。

每份文档包含：

- 中文的模块背景、类职责和使用边界；
- 头文件、CMake、继承关系和派生类信息；
- 能体现真实调用关系的针对性代码示例；
- Properties、Public Functions、Signals、Slots、Protected Functions 等 API 分类；
- 每个类页面可提取的公开成员签名，并为每个 API 补充中文用途、调用方式、返回结果和边界提示；
- 类之间的继承关系和相关 API 说明，便于在实际代码中组合使用。

## 模块索引

| 模块 | 类数量 | 索引 |
|---|---:|---|
| Qt Charts | 49 | [Qt Charts 类索引](QtCharts/index.md) |
| Qt Concurrent | 1 | [Qt Concurrent 类索引](QtConcurrent/index.md) |
| Qt Core | 319 | [Qt Core 类索引](QtCore/index.md) |
| Qt D-Bus | 20 | [Qt D-Bus 类索引](QtD_Bus/index.md) |
| Qt GUI | 243 | [Qt GUI 类索引](QtGUI/index.md) |
| Qt Help | 17 | [Qt Help 类索引](QtHelp/index.md) |
| Qt Multimedia | 33 | [Qt Multimedia 类索引](QtMultimedia/index.md) |
| Qt Network | 58 | [Qt Network 类索引](QtNetwork/index.md) |
| Qt Print Support | 8 | [Qt Print Support 类索引](QtPrint_Support/index.md) |
| Qt Qml | 28 | [Qt Qml 类索引](QtQml/index.md) |
| Qt Quick | 43 | [Qt Quick 类索引](QtQuick/index.md) |
| Qt Quick 3D | 18 | [Qt Quick 3D 类索引](QtQuick_3D/index.md) |
| Qt Quick Controls | 2 | [Qt Quick Controls 类索引](QtQuick_Controls/index.md) |
| Qt SQL | 16 | [Qt SQL 类索引](QtSQL/index.md) |
| Qt SVG | 4 | [Qt SVG 类索引](QtSVG/index.md) |
| Qt Shader Tools | 1 | [Qt Shader Tools 类索引](QtShader_Tools/index.md) |
| Qt Spatial Audio | 5 | [Qt Spatial Audio 类索引](QtSpatial_Audio/index.md) |
| Qt TaskTree | 35 | [Qt TaskTree 类索引](QtTaskTree/index.md) |
| Qt Test | 9 | [Qt Test 类索引](QtTest/index.md) |
| Qt UI Tools | 1 | [Qt UI Tools 类索引](QtUI_Tools/index.md) |
| Qt Widgets | 192 | [Qt Widgets 类索引](QtWidgets/index.md) |
| Qt XML | 17 | [Qt XML 类索引](QtXML/index.md) |

## 文档说明

每个类页都直接讲它有什么用、怎么创建、怎么和相关类配合、API 的参数和返回值代表什么，以及常见错误会造成什么现象。布局类页面会进一步解释空间分配、stretch、spacing、alignment 和尺寸约束之间的关系。

第 5 节共整理 **29104** 个 API 条目。每项说明都从 Qt 6.11.1 对应的属性、成员函数、类型、变量或相关非成员函数正文中提取，而不是根据函数名拆词生成。属性的 getter、setter、变化信号、绑定和重置接口会回到同一属性语义；只有“这是重载函数”的条目会继承同名重载的完整说明；重实现函数会继续追溯基类行为。

Qt 原始页只给出声明、没有独立正文的少数类型别名和低层接口，文档依据公开签名、相关类型页和随 Qt 安装的头文件补充成员级说明，并明确实际用途和限制，不使用类概述兜底。API 签名保留 C++ 名称，方便直接对应 Qt Creator 和编译器提示；解释和示例使用中文。

## 重新生成 API 说明

重建工具位于 `tools/rebuild_api_docs.py`，默认读取 `D:/QTforGui/qt/Docs/Qt-6.11.1` 并更新全部类页：

```powershell
python -u tools/rebuild_api_docs.py --workers 4
```

可用 `--module QtCore` 或 `--class QGuiApplication` 只处理指定范围，使用 `--dry-run` 仅检查匹配数量。翻译缓存保存在 `.cache/qt_docs_zh_v2.json`，可在网络中断后继续，不会加入版本库。

最后重建：2026-09-06；Qt 版本：6.11.1。
