# Qt QScopedValueRollback：作用域结束时恢复变量

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QScopedValueRollback>`  
> 所属模块：`Qt6::Core`  
> 类型性质：模板化、不可复制移动的值回滚守卫  
> 相关类型：`QAtomicScopedValueRollback`、`QScopeGuard`

## 1. 它解决什么问题

函数经常需要临时改变一个状态，并保证离开作用域后恢复原值，例如：

- 临时设置“正在更新”标志；
- 递归遍历时暂时改变当前上下文；
- 进入内部调用前临时关闭某个行为；
- 异常或早退时恢复嵌套调用所依赖的状态；
- 在测试或解析阶段临时切换模式。

手工保存和恢复容易漏掉早退出路径：

```cpp
const bool oldValue = updating;
updating = true;
// 中途 return 时容易忘记恢复 oldValue
updating = oldValue;
```

`QScopedValueRollback<T>` 把保存的旧值和恢复动作绑定到作用域：

```cpp
QScopedValueRollback<bool> rollback(updating, true);
// 当前作用域内 updating == true
// 离开作用域时恢复进入前的值
```

## 2. 它不是什么

`QScopedValueRollback` 不是：

- 互斥锁；
- 原子变量操作；
- 事务系统；
- 深拷贝快照；
- 可复制的 guard；
- 自动检测数据竞争的同步工具。

它保存的是变量当前值的一份 `T` 对象，并通过引用写回原变量。原变量必须在 guard 析构前保持有效。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QScopedValueRollback>
```

这是类模板，模板参数通常由被管理变量的类型显式写出：

```cpp
QScopedValueRollback<bool> rollback(flag, true);
```

## 4. 最小可用代码

```cpp
#include <QScopedValueRollback>

class Parser
{
public:
    void parseNode()
    {
        QScopedValueRollback<bool> rollback(inParse, true);
        parseChildren();
    }

private:
    bool inParse = false;

    void parseChildren();
};
```

如果 `parseChildren()` 递归调用 `parseNode()`，每层 guard 都会保存自己的进入前状态，并在对应层退出时恢复，不需要手工区分嵌套深度。

## 5. 两个构造函数的区别

### 5.1 `QScopedValueRollback(T &var)`：只保存，不立即修改

```cpp
int mode = 1;
{
    QScopedValueRollback<int> rollback(mode);
    mode = 2;
} // mode 恢复为 1
```

第一个构造函数复制保存 `var` 当前值，但不改变 `var`。之后由调用方在作用域内执行临时修改。

### 5.2 `QScopedValueRollback(T &var, T value)`：保存并立即赋值

```cpp
int mode = 1;
{
    QScopedValueRollback<int> rollback(mode, 2);
    // 此时 mode == 2
} // mode 恢复为 1
```

实现会先保存旧值，再把传入的 `value` 移入 `var`。这个构造函数适合表达“进入作用域就切换状态”。

## 6. 析构恢复和 `commit()` 语义

### 6.1 析构恢复到最近一次保存值

析构函数把内部保存的 `oldValue` 移回被引用变量：

```cpp
int value = 10;
{
    QScopedValueRollback<int> rollback(value, 20);
    value = 30;
} // value == 10
```

它不关心作用域内发生了多少次赋值，最终都会恢复保存的值。

### 6.2 `commit()` 是提交一个新基线，不是禁用回滚

```cpp
int value = 10;
{
    QScopedValueRollback<int> rollback(value, 20);
    value = 30;
    rollback.commit();
    value = 40;
} // value == 30
```

`commit()` 把当前 `var` 的值复制到内部 `oldValue`。它不会销毁 guard，也不会让后续修改永久保留。上例中析构时仍会回滚，只是回滚目标从 `10` 更新成了 `30`。

因此：

- 想完全取消恢复动作时，`QScopedValueRollback` 不是最直白的工具；
- 想在阶段性处理后建立新的恢复基线时，使用 `commit()`；
- 想把任意清理动作变成一次性可取消守卫，可以考虑 `QScopeGuard`。

## 7. 类型要求和对象生命周期

### 7.1 `T` 必须支持值保存和恢复

两个构造函数、`commit()` 和析构过程会用到 `T` 的复制或移动构造/赋值能力。`T` 需要能够：

- 从 `var` 保存一份旧值；
- 接收构造函数提供的新值；
- 在析构时赋回；
- 在 `commit()` 时更新保存值。

对不可复制或不可赋值类型不能直接使用本模板，应设计专用状态对象或使用其他回滚策略。

### 7.2 引用目标必须活得更久

```cpp
QScopedValueRollback<int> makeBadRollback()
{
    int local = 0;
    return QScopedValueRollback<int>(local, 1);
}
```

返回后的 guard 仍引用已经销毁的 `local`，析构时会产生未定义行为。正确做法是让被管理变量由调用方或外层对象拥有。

### 7.3 guard 不可复制移动

Qt 6.11.1 对本类使用 `Q_DISABLE_COPY_MOVE`。一个 guard 保存对特定变量的引用和一个回滚值，复制或移动都会模糊谁负责最终写回，因此这些操作都被禁用。

把它放在明确的局部作用域中，不要放进需要搬移元素的容器，也不要从函数返回。

## 8. 线程安全边界

`QScopedValueRollback<T>` 只执行普通的读取、赋值和移动操作，不提供原子性或内存序。多个线程同时访问同一个 `var`，仍然需要互斥锁或其他同步协议。

如果被管理的是原子状态，应查看 `QAtomicScopedValueRollback`；即便使用原子版本，也要根据业务需要选择正确的内存序和整体状态协议。原子写回不等于复合操作自动成为事务。

## 9. 嵌套使用和回滚顺序

嵌套 guard 会形成栈式恢复：

```cpp
int state = 0;
{
    QScopedValueRollback<int> outer(state, 1);
    {
        QScopedValueRollback<int> inner(state, 2);
        // state == 2
    } // state == 1
} // state == 0
```

内层先恢复到进入内层时的值，外层再恢复到最初值。这正适合递归解析、嵌套模式和临时上下文。

如果在 guard 生命周期内通过其他别名销毁或替换了被管理变量，回滚引用就会失效；不要让 guard 跨越所有权变更。

## 10. 逐项 API 语义

### 10.1 `QScopedValueRollback(T &var)`

```cpp
explicit constexpr QScopedValueRollback(T &var);
```

保存 `var` 当前值，不修改 `var`。析构时把保存值写回。`var` 必须在 guard 析构前有效。

### 10.2 `QScopedValueRollback(T &var, T value)`

```cpp
explicit constexpr QScopedValueRollback(T &var, T value);
```

保存 `var` 的旧值，并立即把 `value` 移入 `var`。析构时恢复旧值。传入的 `value` 是按值接收的，适合用临时值或可移动值。

### 10.3 `~QScopedValueRollback()`

```cpp
constexpr ~QScopedValueRollback();
```

把内部保存值移回关联变量。它没有“是否已回滚”的公开状态，也没有取消析构恢复的成员函数。

### 10.4 `commit()`

```cpp
constexpr void commit();
```

把当前 `var` 的值复制到内部保存值，更新未来析构时的回滚目标。它不是“永久提交并禁用析构”的操作。

## 11. 实际使用模式

### 11.1 临时设置递归状态

```cpp
void Parser::parseNode()
{
    QScopedValueRollback<bool> rollback(inParse, true);
    parseCurrentNode();
}
```

无论 `parseCurrentNode()` 如何返回，`inParse` 都会恢复。

### 11.2 临时切换模式

```cpp
void Renderer::renderPreview()
{
    QScopedValueRollback<RenderMode> rollback(mode, RenderMode::Preview);
    render();
}
```

调用方不需要知道进入前是普通模式还是其他模式。

### 11.3 分阶段更新回滚基线

```cpp
int phase = 0;
QScopedValueRollback<int> rollback(phase, 1);

phase = 2;
rollback.commit(); // 后续退出时恢复到 2
phase = 3;
```

作用域结束后 `phase` 恢复为 `2`，不是初始的 `0`。

## 12. 常见错误

### 12.1 把 `commit()` 当成 `dismiss()`

`commit()` 仍然会保留析构恢复，只是更新恢复目标。想要完全不再回滚，应使用其他控制结构，或用 `QScopeGuard` 并调用 `dismiss()`。

### 12.2 在回滚变量销毁后让 guard 继续存在

guard 的引用不会延长变量生命周期。不要返回、异步保存或跨越所有权变更保存 guard。

### 12.3 把普通变量回滚当作线程同步

回滚前后的读写仍可能与其他线程并发。需要线程安全时先设计同步协议，再选择普通或原子版本。

### 12.4 在回滚对象上使用复杂副作用赋值

析构时会执行 `varRef = std::move(oldValue)`。如果 `T` 的赋值会触发回调、重新进入代码或抛出异常，必须确认这些副作用适合发生在作用域退出阶段。

### 12.5 作用域太大

guard 存活越久，变量保持临时状态的时间越长。把它放在最小的局部作用域，避免让后续无关代码看到错误的临时状态。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QScopedValueRollback(T &var)` | 保存当前值，等待调用方临时修改 | 构造不改变变量；析构恢复原值 |
| `QScopedValueRollback(T &var, T value)` | 保存旧值并立即写入新值 | `value` 移入变量；变量和 guard 生命周期必须匹配 |
| `~QScopedValueRollback()` | 把保存值写回变量 | 无取消机制；会执行 `T` 的赋值 |
| `commit()` | 把当前变量值设为新的回滚基线 | 不是禁用回滚；后续退出仍会恢复到新基线 |

## 14. 一句话总结

`QScopedValueRollback` 用一个不可复制移动的 guard 管理普通变量的临时状态：构造时保存旧值，可选地立即写入新值，析构时恢复；`commit()` 只更新未来的恢复基线，不会取消回滚，也不提供线程同步。
