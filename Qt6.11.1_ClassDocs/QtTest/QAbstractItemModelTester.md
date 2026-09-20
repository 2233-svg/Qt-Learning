# QAbstractItemModelTester
> Qt 6.11.1 · Qt Test · 来自 `QAbstractItemModelTester`

## 1. 先建立直觉

`QAbstractItemModelTester` 是模型/视图开发的自动体检器。把它挂到你的 `QAbstractItemModel` 上，它会检查索引、父子关系、行列数、数据变更信号、插入删除协议等是否符合 Qt Model/View 的基本契约。

它不能证明你的业务数据正确，但很擅长抓出“模型实现不守规矩”导致的视图崩溃、断言、随机刷新错误。

## 2. 类说明

保留类说明：这些 API 来自 `QAbstractItemModelTester`，属于 Qt Test 模块，用于验证 `QAbstractItemModel` 子类是否遵守模型协议。

它继承 `QObject`，通常作为测试用例对象或模型对象的子对象存在。只要 tester 活着，它就会监听模型变化并做检查。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QAbstractItemModelTester(model, parent)` | 以默认 `QtTest` 失败报告模式测试模型。 |
| `QAbstractItemModelTester(model, mode, parent)` | 指定失败报告方式。 |
| `model()` | 返回正在测试的模型。 |
| `failureReportingMode()` | 查询当前失败报告模式。 |
| `setUseFetchMore(bool)` | Qt 6.4 起控制是否在测试中触发 `fetchMore()`。 |
| `FailureReportingMode::QtTest` | 把违规报告为 Qt Test 失败。 |
| `FailureReportingMode::Warning` | 只向 `qt.modeltest` 日志输出警告。 |
| `FailureReportingMode::Fatal` | 违规时 `qFatal()` 终止程序。 |

## 4. 典型流程

```cpp
MyTreeModel model;
QAbstractItemModelTester tester(
    &model,
    QAbstractItemModelTester::FailureReportingMode::QtTest);

populateModel();
insertRows();
removeRows();
changeData();
```

对懒加载模型：

```cpp
tester.setUseFetchMore(false); // 避免测试主动拉取远程/昂贵数据
```

## 5. 使用场景

| 场景 | 为什么有用 |
| --- | --- |
| 新写模型类 | 快速验证 index/parent/rowCount/columnCount 契约。 |
| 树模型调试 | 父子关系错是最常见崩溃源，tester 能早发现。 |
| 复杂插入删除 | 检查 begin/end 信号和行列范围是否匹配。 |
| 代理模型或懒加载模型 | 暴露源模型与代理模型的协议问题。 |

## 6. 常见坑与经验

tester 只能发现模型协议错误，不会验证你的业务值对不对。比如金额算错但信号和索引都合法，它不会帮你发现。

`fetchMore()` 可能触发数据库、网络或大文件读取。对懒加载模型，如果自动 fetch 会让测试慢或有副作用，就关闭 `setUseFetchMore(false)`，再针对加载逻辑单独测试。

失败模式要按环境选择。单元测试用 `QtTest`；调试应用运行期模型可以用 `Warning`；CI 中想立即停止可考虑 `Fatal`，但它会让后续诊断机会变少。

模型必须在自己的线程里被访问。大多数模型和视图在 GUI 线程，测试也应该在同一线程操作它。

## 7. 知识点覆盖

- Qt Model/View 基本契约。
- index/parent、行列数、数据变更、插入删除信号。
- 模型测试失败报告策略。
- `fetchMore()` 与懒加载模型测试。
- tester 生命周期和模型线程边界。
