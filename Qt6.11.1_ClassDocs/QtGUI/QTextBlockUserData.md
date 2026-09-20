# QTextBlockUserData
> Qt 6.11.1 · Qt GUI · 来自 `QTextBlockUserData`

## 1. 先建立直觉

`QTextBlockUserData` 是挂在 `QTextBlock` 上的自定义数据基类。它常用于代码编辑器：每一行保存括号位置、语法 token、诊断信息、折叠状态等缓存。

## 2. 类说明

- 头文件：`#include <QTextBlockUserData>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：可继承基类
- 所有权：交给 `QTextBlock::setUserData()` 或 highlighter 后由文档管理

block 删除时，关联 user data 会被删除。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 构造/析构 | 基类提供虚析构，便于多态删除 |

这个类 API 很少，价值在“作为每个 block 的自定义缓存挂点”。

## 4. 关键用法

```cpp
struct BlockData : QTextBlockUserData {
    QVector<int> bracketPositions;
};

auto *data = new BlockData;
data->bracketPositions = positions;
setCurrentBlockUserData(data);
```

读取时用 `dynamic_cast<BlockData *>(block.userData())`。

## 5. 使用场景

语法高亮缓存 token、括号匹配、代码折叠、每行错误警告、断点信息、增量解析状态。

## 6. 常见坑与经验

- 所有权给文档后不要手动 delete。
- user data 跟 block 走，文本编辑导致 block 分裂或删除时要重新计算。
- 只放和该 block 强相关的数据；全局索引放外部结构更好维护。

## 7. 知识点覆盖

块级自定义缓存、语法高亮辅助、所有权、动态转换、编辑器行状态。
