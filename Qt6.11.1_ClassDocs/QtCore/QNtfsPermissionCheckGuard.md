# QNtfsPermissionCheckGuard
> Qt 6.11.1 · Qt Core · 来自 `QNtfsPermissionCheckGuard`

## 作用定位
`QNtfsPermissionCheckGuard` 是 Windows NTFS 权限查询的 RAII 守卫，用于临时启用或恢复 Qt 对 NTFS ACL 权限检查的行为。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 | 保存当前检查状态并设置新的启用状态。|
| 析构函数 | 自动恢复此前状态。|
| `isPermissionCheckEnabled()` | 查询当前 NTFS 权限检查状态。|

## 使用场景
Windows 专用的文件管理、诊断或部署工具需要准确展示 NTFS 访问权限时，在有限作用域中启用检查。

## 常见坑与经验
- 权限检查可能增加文件元数据查询成本，不应在大规模目录扫描热路径无差别开启。
- 文件 ACL 结果只是某个时刻的观察；实际打开文件仍可能因权限、锁或竞态失败。
- 这是 Windows/NTFS 专用行为，跨平台代码要提供条件编译或退化逻辑。

## 知识点覆盖
NTFS ACL、RAII、文件权限、Windows 平台差异、性能、TOCTOU。
