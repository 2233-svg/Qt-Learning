# QRegularExpressionMatch
> Qt 6.11.1 · Qt Core · 来自 `QRegularExpressionMatch`

## 作用定位
`QRegularExpressionMatch` 是一次正则执行的结果快照：它保存成功、部分成功或失败状态，以及整体匹配和各捕获组在主题文本中的内容与位置。

## API 速查
| API | 是做什么的 |
|---|---|
| `hasMatch()` | 是否取得完整匹配。 |
| `hasPartialMatch()` | 是否有可能因文本未结束而产生的部分匹配。 |
| `captured(n/name)` | 取得整体或某捕获组文本。 |
| `capturedView(n/name)` | 以视图返回捕获文本；主题字符串需继续有效。 |
| `capturedStart/End/Length()` | 取得捕获组的 UTF-16 位置范围。 |
| `lastCapturedIndex()` | 找到最后一个参与匹配的捕获组。 |
| `regularExpression()` | 取得产生结果的模式。 |
| `matchType()` / `matchOptions()` | 了解本次运行采用的匹配策略。 |

## 使用场景
```cpp
const auto m = QRegularExpression(R"((\d{4})-(\d{2})-(\d{2}))").match(text);
if (m.hasMatch()) {
    const int year = m.captured(1).toInt();
    const int month = m.captured(2).toInt();
}
```

## 常见坑与经验
- `captured()` 返回空字符串可能表示“组未参与”，也可能表示“匹配到空串”；需结合 `capturedStart()` 是否为 `-1` 区分。
- 位置以 UTF-16 code unit 计，不等于用户可见字符数；处理 emoji、组合字符时不要直接当字形索引。
- `capturedView()` 可减少分配，但不能比主题文本活得更久。
- 部分匹配只适合流式输入或补全文本等场景，普通验证通常只判断 `hasMatch()`。

## 知识点覆盖
正则结果、捕获组、命名捕获、UTF-16 索引、部分匹配、零拷贝字符串视图。
