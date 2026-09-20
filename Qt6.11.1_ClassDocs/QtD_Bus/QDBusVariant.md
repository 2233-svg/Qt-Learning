# QDBusVariant
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusVariant`

## 作用定位

`QDBusVariant` 表示 D-Bus 协议里的 `variant`：一个运行时才确定实际类型的值。Qt 已有 `QVariant`，但 D-Bus 的 variant 是协议层显式类型，所以 Qt 用 `QDBusVariant` 标明“这里要按 D-Bus variant 封送”，而不只是普通 QVariant 容器。

## 类说明

- 头文件：`#include <QDBusVariant>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承
- 内容：内部持有一个 `QVariant`

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusVariant()` | 创建空 variant。 |
| `QDBusVariant(const QVariant &)` | 用 QVariant 构造 D-Bus variant。 |
| `setVariant()` | 替换内部值。 |
| `variant()` | 读取内部 QVariant。 |
| `swap()` | 快速交换两个 variant。 |

## 典型用法

```cpp
QVariantMap props;
props.insert("Volume", QVariant::fromValue(QDBusVariant(80)));
props.insert("Muted", QVariant::fromValue(QDBusVariant(false)));
```

在很多 D-Bus 属性接口中，字典类型是 `a{sv}`：key 是字符串，value 是 variant。这里的 `v` 就需要 `QDBusVariant` 来表达。

## 使用场景

- 处理 `org.freedesktop.DBus.Properties` 的属性值。
- 传递 `a{sv}` 这类“字符串到任意类型”的字典。
- 远端接口要求参数签名为 `v`，而不是具体的 `s`、`u`、`b`。

## 常见坑与经验

- `QVariant` 和 `QDBusVariant` 不等价；前者是 Qt 容器，后者告诉 D-Bus 签名里要出现 `v`。
- 内部 QVariant 仍然必须是可封送类型，自定义类型还是要注册 D-Bus 元类型。
- 读取属性字典时，常见结构是 `QVariantMap` 里包着 `QDBusVariant`，需要拆两层。
- 空 QVariant 不能随意发送，D-Bus 需要明确可编码的类型。

## 知识点覆盖

- D-Bus variant 签名 `v`
- `a{sv}` 属性字典
- QVariant 与协议类型的区别
- 动态类型值的封送限制
