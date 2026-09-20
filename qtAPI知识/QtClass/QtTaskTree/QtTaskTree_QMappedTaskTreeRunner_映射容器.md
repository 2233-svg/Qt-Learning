# QMappedTaskTreeRunner：按 key 管理并行任务树

> Qt 6.11.1 · `#include <qtasktreerunner.h>` · 模块：`Qt6::TaskTree`

`QMappedTaskTreeRunner<Key>` 是带业务 key 的并行 runner。它内部用 `std::unordered_map<Key, std::unique_ptr<QTaskTree>>` 保存任务树，让你能按“文件路径、请求 ID、模型对象指针、账号 ID”等 key 启动、替换、取消或查询某一棵树。

## 解决的问题

很多 UI 和服务逻辑不是“只能跑一个”或“全部平行无名”，而是“每个对象最多一个任务”。例如每个文档只能有一个索引任务；同一个下载 URL 的新请求应覆盖旧请求；不同 tab 的刷新可以并行，但关闭某个 tab 时只取消它自己的任务树。`QMappedTaskTreeRunner` 正是这个形状。

## key 的替换语义

`start(key, recipe, ...)` 会为该 key 启动新树。如果同一个 key 已经有树在运行，旧树会被替换；其他 key 不受影响。不同 key 的树并行运行，完成后自动从 map 中移除。

因为实现基于 `std::unordered_map`，`Key` 必须可哈希、可比较相等，并且在任务生命周期内用于查找的值应稳定。若 key 是指针，要确保对象销毁前先 `cancelKey()` 或 `resetKey()`，避免业务层再用悬空指针当身份。

## cancel 与 reset

`cancelKey()` 只取消指定 key 的树，并按取消流程触发对应 done handler。`resetKey()` 直接移除指定 key 的树，不调用 done handler。`cancel()` 和 `reset()` 是全局版本：前者取消全部并按规则通知，后者直接清空。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QMappedTaskTreeRunner<Key>()` | 构造空映射 runner；`Key` 需满足 `std::unordered_map` 的 hash/equality 要求。 |
| `~QMappedTaskTreeRunner()` | 清理所有仍保存的树；不把析构当作业务 done 通知。 |
| `isRunning() const` | map 非空即为 true，表示至少有一个 key 正在运行。 |
| `isKeyRunning(const Key &key) const` | 查询指定 key 是否已有运行树。 |
| `start(key, recipe, setup, done, callDone)` | 启动或替换指定 key 的树；不同 key 可并行。 |
| `setupHandler(QTaskTree &)` | 该 key 的新树启动前调用。 |
| `doneHandler(const QTaskTree &, DoneWith)` | 该 key 的树完成后调用；完成时 runner 会先安排树 `deleteLater()` 并移除 key。 |
| `cancelKey(const Key &key)` | 正常取消指定 key；会按 `CallDone` 触发 done handler。 |
| `resetKey(const Key &key)` | 无通知丢弃指定 key；不调用 done handler。 |
| `cancel()` | 取消全部 key；循环取消直到 map 清空。 |
| `reset()` | 直接清空全部 key；不调用 done handler。 |
| `CallDone` | 每次 `start()` 单独设置，过滤对应 key 的 done handler。 |
