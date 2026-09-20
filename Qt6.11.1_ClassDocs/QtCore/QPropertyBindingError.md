# QPropertyBindingError
> Qt 6.11.1 · Qt Core · 来自 `QPropertyBindingError`

## 作用定位
`QPropertyBindingError` 是属性绑定求值失败时携带的诊断值。它不负责建立绑定；它回答的是“这次绑定为什么没有得到可靠结果”。常见来源是属性依赖形成环，或绑定表达式本身在执行时失败。

它适合被上层代码记录、展示或转交，而不是拿来驱动正常业务流程。正常的绑定应当始终能重算出值；错误分支应促使你修正依赖图或表达式。

## API 速查
| API | 是做什么的 |
|---|---|
| `QPropertyBindingError()` | 构造“无错误”状态。 |
| `QPropertyBindingError(Type, QString)` | 以错误类别和可读说明构造诊断结果。 |
| `type()` | 取得机器可判断的错误类别。 |
| `description()` | 取得适合日志、调试面板的补充说明。 |
| `NoError` | 绑定求值没有错误。 |
| `BindingLoop` | 依赖链回到了自身，Qt 停止此次求值。 |
| `EvaluationError` | 表达式执行失败，但并非依赖环；QML 绑定异常是典型来源。 |
| `UnknownError` | 其他无法归入前两类的失败，优先查看说明文本。 |
| 拷贝、移动、赋值 | 传递或保存诊断值；移动后的源对象回到默认状态。 |

## 使用场景

### 排查循环绑定
```cpp
// 错误示意：width 的计算又读回了 width。
QProperty<int> width([&] { return width.value() + 10; });
```
绑定表达式应只读取真正的输入属性，例如 `contentWidth`、`padding`，不要读取它正在产出的同一个属性，也要警惕 A 读 B、B 又读 A 的间接环。

### 将错误写入诊断日志
当某个框架或封装把绑定错误交给你时，先按 `type()` 分类，再输出 `description()`。前者适合统计和分支，后者适合定位现场；不要依赖说明文字做程序逻辑，因为文字并不是稳定协议。

```cpp
void reportBindingError(const QPropertyBindingError &error)
{
    if (error.type() == QPropertyBindingError::NoError)
        return;
    qWarning() << "property binding failed:" << error.type()
               << error.description();
}
```

## 常见坑与经验
- `NoError` 是一个正常值，不要仅用“描述是否为空”判断成功。
- `BindingLoop` 不一定只由一行表达式造成；检查整个属性依赖图以及通知回调里是否反写输入属性。
- 绑定表达式应接近纯函数：读取依赖、计算、返回。写文件、发网络请求、修改其他属性都会让重算时机变得不可控。
- `EvaluationError` 在混合 C++/QML 时尤其值得记录：它往往说明 QML 表达式抛出了异常或访问了无效对象。

## 知识点覆盖
属性绑定、依赖图、循环依赖、惰性/重新求值、QML 与 C++ 属性互操作、错误分类、日志诊断、纯函数式计算。
