# QSignalSpy
> Qt 6.11.1 · Qt Test · 来自 `QSignalSpy`

## 1. 先建立直觉

`QSignalSpy` 是测试里观察 Qt 信号的记录器。它连接到某个信号，每次信号发出，就把本次参数保存成一行 `QVariantList`。你可以断言信号发了几次、参数是什么，也可以等待异步信号出现。

它特别适合测 QObject API 的行为边界：点击按钮是否发 `clicked`，网络对象是否发 `finished`，模型操作是否发 `rowsInserted`。

## 2. 类说明

保留类说明：这些 API 来自 `QSignalSpy`，属于 Qt Test 模块，用于在测试中捕获和检查 QObject 信号。

`QSignalSpy` 继承自 `QList<QList<QVariant>>` 风格的容器语义，所以 `count()`、`takeFirst()`、`at()` 等列表操作也常用。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSignalSpy(object, &Class::signal)` | 类型安全地监听信号，推荐写法。 |
| `QSignalSpy(obj, QMetaMethod)` | 运行时通过元对象方法监听信号。 |
| `QSignalSpy(object, SIGNAL(...))` | 旧式字符串信号写法，兼容老代码。 |
| `isValid()` | 判断 spy 是否成功连接到有效信号。 |
| `signal()` | 返回正在监听的信号签名。 |
| `wait(int timeout)` | 等待信号出现，超时返回 false。 |
| `wait(std::chrono::milliseconds)` | chrono 版本等待，Qt 6.6 起可用，默认 5 秒。 |
| `count()` / `size()` | 继承列表 API：查看捕获次数。 |
| `takeFirst()` / `at(i)` | 读取某次信号参数。 |
| `clear()` | 清掉已捕获记录，开始观察后续信号。 |

## 4. 典型流程

```cpp
QSignalSpy spy(button, &QPushButton::clicked);
QVERIFY(spy.isValid());

QTest::mouseClick(button, Qt::LeftButton);
QCOMPARE(spy.count(), 1);
```

检查参数：

```cpp
QSignalSpy spy(model, &QAbstractItemModel::dataChanged);
editCell();
QCOMPARE(spy.count(), 1);
const auto args = spy.takeFirst();
QCOMPARE(args.at(0).value<QModelIndex>(), expectedTopLeft);
```

异步信号：

```cpp
QSignalSpy finished(reply, &QNetworkReply::finished);
QVERIFY(finished.wait(std::chrono::seconds(3)));
```

## 5. 使用场景

| 场景 | 检查重点 |
| --- | --- |
| UI 交互测试 | 点击、输入后信号次数和参数是否正确。 |
| 异步对象测试 | 用 `wait()` 等完成信号，避免固定 sleep。 |
| 模型/数据类测试 | 检查 `dataChanged`、`rowsInserted` 等通知。 |
| API 回归测试 | 断言某操作不会多发或漏发信号。 |

## 6. 常见坑与经验

先 `QVERIFY(spy.isValid())`。信号签名写错、对象为空、监听了不存在的重载时，后面的 `count()` 只会让失败变得很难读。

`wait()` 等的是“下一次信号”。如果信号在调用 `wait()` 之前已经发出，`wait()` 不会为旧记录成功；这种情况先看 `count()`，不够再等。

跨线程信号通常经过事件循环投递。测试里不要用固定 `qWait(100)` 碰运气，优先用 `QSignalSpy::wait()` 或 `QTRY_COMPARE` 一类重试断言。

参数存在 `QVariant` 里，自定义类型需要能被元类型系统识别。必要时先 `Q_DECLARE_METATYPE` / `qRegisterMetaType`。

## 7. 知识点覆盖

- QObject 信号捕获和参数记录。
- 类型安全信号指针、`QMetaMethod`、旧式宏签名。
- 异步信号等待和事件循环。
- `QVariant` 参数读取与元类型注册。
- 信号次数、顺序、参数的测试设计。
