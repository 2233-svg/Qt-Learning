# QRandomGenerator64
> Qt 6.11.1 · Qt Core · 来自 `QRandomGenerator64`

## 作用定位
`QRandomGenerator64` 是 `QRandomGenerator` 的 64 位适配版本，主要区别是 `generate()` 与函数调用运算符返回完整 `quint64`，可以直接满足 STL 的 64 位随机位生成器约定。

除了返回宽度外，种子、`bounded()`、安全随机源与全局实例的选择规则都继承自 `QRandomGenerator`。

## API 速查
| API | 是做什么的 |
|---|---|
| `generate()` | 生成完整 64 位无符号随机值。 |
| `operator()()` | 与 `generate()` 等价，便于传给标准库随机算法。 |
| `result_type` | `quint64`，表明此生成器的原生输出宽度。 |
| 继承的 `bounded()` | 在给定半开区间内生成均匀随机数。 |
| 继承的 `global()` / `system()` | 分别获得一般用途或操作系统随机源。 |

## 使用场景
```cpp
QRandomGenerator64 local(1234);
const quint64 idPart = local.generate();

// 需要正 qint64 时，清掉符号位。
const qint64 positive =
    qint64(local.generate() & std::numeric_limits<qint64>::max());
```

适合需要 64 位随机字段、64 位哈希采样、随机跳表层级或调用要求 64 位 `result_type` 的标准库算法。若只是选择一个不大的数组下标，普通 `QRandomGenerator` 已足够。

## 常见坑与经验
- `quint64` 转 `qint64` 后最高位可能使结果为负；若业务需要非负数，先掩去符号位。
- 64 位输出不自动等于“更安全”；安全性仍取决于是否选用了 `system()` 或安全播种。
- 不能以 `generate() % n` 替代 `bounded(n)`，除非 `n` 恰好整除输出范围；否则会产生模偏差。
- 继承来的 `bounded()` 上界仍是排他的，空范围和逆序范围要在调用前处理。

## 知识点覆盖
64 位随机位、无符号与有符号转换、模偏差、标准库随机接口、可复现序列、密码学熵源。
