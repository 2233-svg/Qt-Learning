# QRegularExpressionMatchIterator
> Qt 6.11.1 · Qt Core · 来自 `QRegularExpressionMatchIterator`

## 作用定位
`QRegularExpressionMatchIterator` 是 `globalMatch()` 返回的前向迭代器，按文本从左到右惰性产生每次匹配。它适合扫描日志、标记文本、抽取所有字段。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasNext()` | 判断是否还有下一项。 |
| `next()` | 取出下一次匹配；无下一项时不能调用。 |
| `peekNext()` | 查看下一次匹配但不前进。 |
| `isValid()` | 判断迭代器是否关联了有效的匹配操作。 |
| `regularExpression()` | 取得扫描所使用的模式。 |
| `matchType()` / `matchOptions()` | 查询运行参数。 |

## 使用场景
```cpp
auto it = QRegularExpression(R"(\b\d+\b)").globalMatch(text);
while (it.hasNext()) {
    const auto match = it.next();
    numbers.append(match.captured().toInt());
}
```

## 常见坑与经验
- 永远以 `hasNext()` 守卫 `next()`；迭代器不是 STL 的 end 比较接口。
- 每次 `next()` 只取得一个值，处理过程中不要忘记保存需要的结果。
- 基于 `QStringView` 的全局匹配依赖原始文本生命周期；异步保存 iterator 或 match 前先拥有文本。
- 零长度模式也可能匹配，虽然 Qt 会推进扫描位置防止无限循环，业务仍要确认这种结果是否有意义。

## 知识点覆盖
惰性迭代、全局匹配、流式文本处理、捕获组、零长度匹配、源文本生命周期。
