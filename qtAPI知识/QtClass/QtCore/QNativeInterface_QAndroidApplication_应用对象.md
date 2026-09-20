# Qt QNativeInterface::QAndroidApplication：访问 Android 应用 Context 与 UI 线程

> 适用版本：Qt 6.11.1  
> 引入版本：Qt 6.2  
> 头文件：`#include <QCoreApplication>`  
> 所属模块：`Qt6::Core`  
> 平台：仅 Android  
> 类型性质：`QCoreApplication` 的 native interface；不能作为普通值对象创建、复制、移动或销毁

## 1. 它解决什么问题

Qt 应用通常通过跨平台 API 工作；但有些 Android 功能只能依赖 Java/Kotlin 的 `Context`、`Activity`、`Window` 或 Android UI thread。例如：

- 调用应用自己的 Java/Kotlin 接口；
- 创建或配置 Android 原生 View；
- 修改窗口 flag、状态栏或系统 UI；
- 读取运行设备的 Android API level；
- 控制 Qt for Android 提供的启动画面。

`QNativeInterface::QAndroidApplication` 是 Qt 暴露这些应用级 Android 能力的窄接口。它不创建 Android 应用、不拥有 `Activity`，也不把 Java API 封装成通用 Qt API；它提供到 Android runtime 的入口。

可把它理解为下面三件事：

```text
取得当前 Android Context
            +
把短小的原生 UI 操作切换到 Android UI thread
            +
访问少量 Qt for Android 的应用级信息和启动画面控制
```

这是 native interface API。Qt 的公开头文件明确提示：这类 API 在未来 Qt 版本中可能出现源代码或二进制兼容性变化。将它集中在 Android 平台适配层，而不是散落在业务代码中，升级成本更低。

## 2. 何时使用，何时不用

### 2.1 适合的场景

### 调用应用自带的 Java/Kotlin 接口

例如 C++ 需要把当前 `Context` 传给 Java 工厂方法，创建一个原生对象：

```cpp
#ifdef Q_OS_ANDROID
#  include <QCoreApplication>
#  include <QJniObject>
#endif

QJniObject createNativeHelper()
{
#ifdef Q_OS_ANDROID
    const auto context = QNativeInterface::QAndroidApplication::context();
    return QJniObject("com/example/app/NativeHelper",
                      "(Landroid/content/Context;)V",
                      context);
#else
    return {};
#endif
}
```

构造后仍须用 `QJniObject::isValid()` 检查 JNI 类、构造函数签名和对象是否有效。

### 在 Android UI thread 操作 View 或 Window

`View` 层级、窗口 flag 和多数 Activity UI API 必须由 Android UI thread 操作。使用 `runOnAndroidMainThread()` 投递一个短任务：

```cpp
#ifdef Q_OS_ANDROID
void keepScreenOn()
{
    QNativeInterface::QAndroidApplication::runOnAndroidMainThread([] {
        if (!QNativeInterface::QAndroidApplication::isActivityContext())
            return;

        const auto activity = QNativeInterface::QAndroidApplication::context();
        activity.callObjectMethod("getWindow", "()Landroid/view/Window;")
                .callMethod<void>("addFlags", "(I)V", 0x00000080); // FLAG_KEEP_SCREEN_ON
    });
}
#endif
```

这里的 Android UI thread 不应机械等同于 Qt 对象所属线程或 `QGuiApplication` 的 GUI thread。涉及 Android `View`、`Window`、Activity 生命周期回调时，以 Android 的线程规则为准。

### 让 Qt 启动画面停留到应用准备完成

如果 Android manifest 设置了 `android.app.splash_screen_sticky=true`，Qt 启动画面会一直显示到显式调用 `hideSplashScreen()`。这适合在 QML/窗口首帧、关键资源或初始化流程准备好后再平滑进入主界面：

```cpp
#ifdef Q_OS_ANDROID
void MainController::finishStartup()
{
    QNativeInterface::QAndroidApplication::hideSplashScreen(180);
}
#endif
```

### 根据运行设备版本选择 Android 行为

```cpp
#ifdef Q_OS_ANDROID
const bool supportsNewApi =
        QNativeInterface::QAndroidApplication::sdkVersion() >= 35;
#endif
```

`sdkVersion()` 表示正在运行应用的设备 API level；它不是构建项目设置的 `compileSdkVersion`，也不是 manifest 中声明的 `targetSdkVersion`。

### 2.2 不适合的场景

- 只需 Qt 跨平台能力时，不要为了“以后可能要 Android 支持”提前引入 JNI。
- 后台计算、网络请求、数据库或长 I/O 不应放到 Android UI thread。
- 想在普通后台 `Service` 中调用 Activity 专属 API 时，不能把 `context()` 返回的 Service 当成 Activity。
- 想显示桌面 Qt 的 `QSplashScreen` 时，不使用本接口；它管理的是 Qt for Android 的 Android 启动画面。

## 3. 获取接口与跨平台组织

`QAndroidApplication` 由 `QCoreApplication` 的 native interface 机制提供。文档规定可通过 `QCoreApplication::nativeInterface()` 访问：

```cpp
#ifdef Q_OS_ANDROID
auto *coreApp = QCoreApplication::instance();
auto *androidApp = coreApp
        ? coreApp->nativeInterface<QNativeInterface::QAndroidApplication>()
        : nullptr;

if (androidApp) {
    androidApp->runOnAndroidMainThread([] {
        // Android UI thread 上的短操作
    });
}
#endif
```

当前公开成员都是静态函数，因此直接写 `QNativeInterface::QAndroidApplication::context()` 也可以。通过 `nativeInterface()` 取得指针的写法有两个实际价值：

- 表达该能力来自当前 Qt 应用的平台实现；
- 在封装层中可以检查接口指针，避免假设平台接口一定可用。

该类型只在 `Q_OS_ANDROID` 条件下声明。不要让非 Android 编译单元无条件引用它：

```cpp
class PlatformUi
{
public:
    void requestFullscreen()
    {
#ifdef Q_OS_ANDROID
        QNativeInterface::QAndroidApplication::runOnAndroidMainThread([] {
            // Android-specific work
        });
#endif
    }
};
```

更干净的工程结构是将 JNI 和 native interface 代码放入单独 Android 源文件，由平台条件决定是否编译该文件。

## 4. Context：Activity 与 Service 是不同能力集合

### 4.1 `context()` 的返回规则

`context()` 返回 `QtJniTypes::Context`。文档中显示为 `QJniObject`，它本质上是可用于 JNI 调用的 Qt 包装对象。建议用 `auto` 接收，既保留类型信息，也不把实现细节写死：

```cpp
const auto context = QNativeInterface::QAndroidApplication::context();
if (!context.isValid())
    return;
```

选择规则是：

```text
最近启动的 Activity 对象有效 -> 返回该 Activity Context
否则                         -> 返回 Service Context
```

这意味着“有一个 Context”不等于“有一个可操作窗口的 Activity”。

### 4.2 调用 Activity API 前先判断

`Activity` 才有 `getWindow()`、`runOnUiThread()` 等 Activity 专属能力。调用前使用 `isActivityContext()`：

```cpp
QNativeInterface::QAndroidApplication::runOnAndroidMainThread([] {
    if (!QNativeInterface::QAndroidApplication::isActivityContext())
        return;

    const auto activity = QNativeInterface::QAndroidApplication::context();
    // 现在才可以调用明确要求 Activity 的 JNI 方法。
});
```

不要仅凭变量名是 `context` 就进行 Java 强制转换，或把 Service Context 传给只接受 Activity 的第三方 SDK。应用转入后台、Activity 销毁重建或以 Service 方式运行时，这类假设很容易失效。

### 4.3 JNI 对象生命周期

返回的是值语义的 JNI wrapper，而非由调用方释放的裸 `jobject`。保持 `QJniObject` 或 `QtJniTypes::Context` 的 C++ 值对象即可；不要手动 `DeleteLocalRef()` 它内部管理的引用。

但 wrapper 存在不代表底层 Java 对象在业务语义上永久可用：

- Activity 可能已停止、销毁或被新的 Activity 取代；
- JNI 类名、方法签名和权限不正确时，调用仍会失败；
- 把对象交给异步操作前，应重新考虑 Android 生命周期，而不是长期缓存一个 Activity。

每次执行 JNI 调用都应按 `QJniObject` 的错误检查规则处理异常和 `isValid()` 状态。

## 5. `runOnAndroidMainThread()`：投递模型、Future 与超时

### 5.1 运行位置

```cpp
QFuture<QVariant> QAndroidApplication::runOnAndroidMainThread(
    const std::function<QVariant()> &runnable,
    QDeadlineTimer timeout = QDeadlineTimer::Forever);
```

函数把 `runnable` 投递到 Android main thread，并在 Android UI thread 执行：

- 调用者已经位于 Android UI thread 时，`runnable` 立即执行；
- 否则任务进入 Android main thread 队列；
- Android 应用 paused 或主 Activity 为空时，任务仍进入该主线程队列，等待其能够处理。

因此，任务被接受并不等于它会在某个固定时刻执行。依赖当前 Activity 的工作应在 runnable 内再次确认 `isActivityContext()`，而不是只在投递前检查一次。

### 5.2 有返回值的重载

返回值必须放进 `QVariant`：

```cpp
#ifdef Q_OS_ANDROID
QFuture<QVariant> queryPackageName()
{
    return QNativeInterface::QAndroidApplication::runOnAndroidMainThread([] {
        const auto context = QNativeInterface::QAndroidApplication::context();
        const auto packageName =
                context.callObjectMethod("getPackageName", "()Ljava/lang/String;");
        return QVariant::fromValue(packageName.toString());
    });
}
#endif
```

取结果时先等待完成或在 continuation 中读取，再用 `QVariant::value<T>()` / `toXxx()` 恢复实际类型：

```cpp
auto future = queryPackageName();
future.then([](QFuture<QVariant> completed) {
    const QString packageName = completed.result().toString();
    qDebug() << packageName;
});
```

把自定义 C++ 类型放入 `QVariant` 前，必须满足 Qt 元类型注册要求；不能直接返回任意不可复制或未注册的对象。

### 5.3 `void` 任务的模板重载

Qt 6.11.1 头文件还提供文档成员表未单列的模板重载：

```cpp
template <class F>
QFuture<void> QAndroidApplication::runOnAndroidMainThread(
    const F &runnable,
    QDeadlineTimer timeout = QDeadlineTimer::Forever);
```

当可调用对象无返回值时选中它：

```cpp
QFuture<void> future =
        QNativeInterface::QAndroidApplication::runOnAndroidMainThread([] {
            // 只执行 UI 操作，不产生结果。
        });

future.then([] {
    qDebug() << "UI task finished";
});
```

它内部把 `void` 任务适配为返回空 `QVariant` 的任务，再转换为 `QFuture<void>`。不要为了调用它硬写 `return QVariant();`；直接返回 `void` 更清楚。

这两个重载仅在 Qt 构建启用了 `future` 且未定义 `QT_NO_QOBJECT` 时提供。常规完整 Qt Core 构建通常满足此条件；裁剪版 Qt 或极简配置中应以本机头文件和构建配置为准。

### 5.4 `timeout` 不是取消机制

`timeout` 限制的是阻塞式等待。若等待超过期限，`QFuture::waitForFinished()` 和 `QFuture::result()` 会结束等待；但是 runnable 一旦已经开始执行，Qt 不会取消它。

```cpp
const auto future =
        QNativeInterface::QAndroidApplication::runOnAndroidMainThread(
            [] {
                updateNativeUi();
            },
            QDeadlineTimer(500));

future.waitForFinished(); // 最多等待约 500 ms；并不撤销已开始的更新
```

据此设计代码：

- 不要把 timeout 当成停止 Android 操作的办法；
- runnable 应短小、可预测，必要时自行检查时间预算或取消标志；
- 避免捕获会在任务执行前销毁的裸指针或引用；
- 如果任务必须完成才可继续，考虑 Android paused、队列延迟和生命周期变化，而不是盲目无限同步等待。

### 5.5 不要阻塞 Android UI

Android UI thread 同时负责绘制和输入分发。Qt 文档特别提醒：长操作会卡住界面；通常超过约 5 秒就可能触发“应用无响应”风险。

适合放入 runnable 的内容：

- 一两次 View/Window 属性设置；
- 创建或调用很快结束的 JNI 对象；
- 将 UI 工作拆为多个很短的阶段。

不适合放入 runnable 的内容：

- 网络、磁盘、数据库和大文件处理；
- 等锁、等待其它线程、递归等待 Qt 事件循环；
- 在 UI thread 上调用会反过来等待当前调用线程的逻辑。

## 6. 启动画面：Qt splash 与 Android 12 系统 splash

`hideSplashScreen(int duration)` 隐藏的是 Qt for Android 配置的 Qt splash screen：

```cpp
QNativeInterface::QAndroidApplication::hideSplashScreen(250);
```

- `duration` 是淡出时长，单位为毫秒；
- 默认值 `0`，应用启动后立即隐藏；
- 设置 `android.app.splash_screen_sticky=true` 时，画面会保留到这次调用；
- `android.app.splash_screen_drawable`、`android.app.splash_screen_drawable_portrait` 和 `android.app.splash_screen_drawable_landscape` 用于配置 Qt splash 资源。

Android 12 及以后另有系统默认 splash screen，通常在应用第一帧之前显示，默认可能使用应用图标。它与 Qt splash 是两个层次：`hideSplashScreen()` 不等价于控制 Android 12 系统 splash 的全部行为。若启动过程中同时出现两者，应分别检查 Android theme 和 Qt manifest metadata。

## 7. 生命周期与线程边界

### 7.1 不要实例化或保存为值

`QAndroidApplication` 的 native-interface 宏使其默认构造函数存在，但复制、移动均被禁用，析构函数也受保护。它由 Qt 平台层实现和管理：

```cpp
// 不要这样做；它不是给应用代码创建的普通对象。
// QNativeInterface::QAndroidApplication androidApp;
```

正确方式是使用 `nativeInterface()` 取得的非拥有指针，或调用静态函数。不要 `new`、`delete`、按值返回、放入容器，也不要保存指针超过 `QCoreApplication` 生命周期。

### 7.2 捕获对象时按异步任务处理

投递后 runnable 可能稍后才开始。以下写法有悬空引用风险：

```cpp
void configureLater()
{
    QJniObject temporary = makeHelper();
    QNativeInterface::QAndroidApplication::runOnAndroidMainThread([&] {
        useHelper(temporary); // 函数返回后 temporary 已销毁
    });
}
```

按值捕获可复制、可安全保存的对象；对 `QObject` 使用 `QPointer` 或 context-aware 的后续逻辑；涉及 Android Activity 时优先在 runnable 内重新取得当前 Context。

### 7.3 同步等待可能造成死锁或卡顿

`waitForFinished()` 在后台工作线程偶尔可用于短任务同步化，但仍需设定合理超时。不要在 Android UI thread 上等待一个需要 Android UI thread 继续处理的 Future；虽然当前线程调用会立即执行 runnable，复杂的 continuation、锁和相互等待仍可能让代码难以推断。

默认优先使用 `then()` 等异步 continuation，把结果送回适当的 Qt 线程或对象上下文。

## 8. 常见错误

### 8.1 在非 Android 目标中引用类名

类的声明本身受 `Q_OS_ANDROID` 控制，不只是运行时能力受限。用条件编译隔离 Android 代码。

### 8.2 认为 `context()` 永远是 Activity

后台、Service 或 Activity 不可用时会返回 Service Context。调用窗口、权限弹窗或 View API 前先执行 `isActivityContext()`。

### 8.3 从任意线程直接修改 Android View

JNI 能调用方法不代表线程合法。原生 UI 操作应通过 `runOnAndroidMainThread()`。

### 8.4 在 runnable 中执行长任务

这会阻塞绘制和输入。将重计算和 I/O 放到工作线程，只把最终的 UI 更新投递回 Android UI thread。

### 8.5 误把 timeout 当作任务取消

timeout 结束的是阻塞等待；已开始的 runnable 仍会继续运行。任务自身需要能容忍调用方不再等待结果。

### 8.6 缓存 Activity Context 很久

Activity 有生命周期，旋转屏幕、后台恢复和重建都可能使旧对象不再适合作为当前 UI 容器。临近使用时重新取 Context 并检查类型。

### 8.7 混淆 Qt splash 和 Android 12 系统 splash

`hideSplashScreen()` 管理 Qt splash。系统 splash 的主题、图标和过渡需由 Android 对应配置处理。

## 9. 逐项 API 说明

### 9.1 `context()`

```cpp
static QtJniTypes::Context context();
```

取得当前可用 Android `Context` 的 JNI wrapper。文档视图显示返回类型为 `QJniObject`。

- 最近启动的 Activity 有效时返回 Activity Context；
- 否则返回 Service Context；
- 返回值不转移 Java 对象所有权；
- Activity 专属调用前配合 `isActivityContext()`；
- 应检查 `isValid()`，并避免跨越很长生命周期缓存 Activity。

### 9.2 `isActivityContext()`

```cpp
static bool isActivityContext();
```

判断此刻 `context()` 是否提供 Activity Context。

- `true`：可以按 Activity 使用当前 Context；
- `false`：当前为 Service Context 或不存在可用 Activity；
- 检查与实际调用之间仍可能发生 Android 生命周期变化，关键操作应尽量相邻完成；
- 它不检查 Activity 是否处于前台、是否已完成权限，也不检查某个 JNI 方法是否存在。

### 9.3 `sdkVersion()`

```cpp
static int sdkVersion();
```

返回运行设备的 Android SDK/API level。

- 用于运行时 API 分支；
- 不表示 compile SDK；
- 不表示 target SDK；
- 不应替代 feature detection、权限检查或具体 API 调用的错误处理。

### 9.4 `hideSplashScreen()`

```cpp
static void hideSplashScreen(int duration = 0);
```

隐藏 Qt for Android 启动画面。

- `duration` 为淡出时长，单位毫秒；
- 省略或传入 `0` 时立即隐藏；
- 与 `android.app.splash_screen_sticky=true` 配合时，可延迟到应用真正就绪；
- 不负责 Android 12 系统 splash 的全部配置和控制；
- 应在 Android 启动流程中调用，反复调用是否有可见效果取决于画面是否仍存在。

### 9.5 `runOnAndroidMainThread()`：有返回值

```cpp
static QFuture<QVariant> runOnAndroidMainThread(
    const std::function<QVariant()> &runnable,
    QDeadlineTimer timeout = QDeadlineTimer::Forever);
```

投递返回 `QVariant` 的任务到 Android UI thread。

- Android UI thread 调用时立即执行，其他线程调用时排队；
- app paused 或主 Activity 为空时仍进入 Android main queue；
- 通过 `QFuture<QVariant>` 异步接收结果；
- `timeout` 只限制 `waitForFinished()` / `result()` 的阻塞等待；
- 已开始的任务不会因 timeout 取消；
- 任务必须短小，不能阻塞 UI。

### 9.6 `runOnAndroidMainThread()`：`void` 模板重载

```cpp
template <class F>
static QFuture<void> runOnAndroidMainThread(
    const F &runnable,
    QDeadlineTimer timeout = QDeadlineTimer::Forever);
```

Qt 6.11.1 头文件提供的无返回值便利重载。

- 只接受可调用且返回 `void` 的对象；
- 返回 `QFuture<void>`；
- 行为、排队规则和 timeout 边界与 `QVariant` 重载相同；
- 需要 Qt `future` 功能且未禁用 `QObject`；
- 不适合需要传回普通 C++ 返回值的任务，此时显式包装为 `QVariant`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 入口 | `QCoreApplication::nativeInterface<QNativeInterface::QAndroidApplication>()` | 取得 Qt 管理的 Android 应用接口 | 非拥有指针；先有 `QCoreApplication`，并在 Android 条件编译内使用 |
| Context | `context()` | 返回当前 Activity 或 Service Context 的 JNI wrapper | 先判断 `isValid()`；不是永远的 Activity |
| Context 类型 | `isActivityContext()` | 判断当前 Context 是否为 Activity | Activity 专属 Java API 的必要前置检查 |
| 设备版本 | `sdkVersion()` | 返回运行设备 API level | 不是 target/compile SDK，也不能取代权限或功能检查 |
| UI 线程 | `runOnAndroidMainThread(QVariant runnable, timeout)` | 在 Android UI thread 执行并返回 `QFuture<QVariant>` | 返回值装入 `QVariant`；timeout 不取消已开始的任务 |
| UI 线程 | `runOnAndroidMainThread(void runnable, timeout)` | 执行无返回值 Android UI 任务 | Qt 6.11.1 头文件模板重载；返回 `QFuture<void>` |
| 启动画面 | `hideSplashScreen(duration)` | 淡出或立即隐藏 Qt splash | `duration` 为毫秒；配合 sticky metadata；不要和 Android 12 系统 splash 混淆 |
| JNI 协作 | `QJniObject::isValid()` | 检查 JNI wrapper 是否有效 | Context、类、构造函数和方法调用都可能失败 |
| 平台保护 | `#ifdef Q_OS_ANDROID` | 隔离 Android 专属声明和实现 | 非 Android 编译单元无法引用该类型 |

## 11. 一句话总结

`QNativeInterface::QAndroidApplication` 是 Qt 应用进入 Android runtime 的应用级接口：用 `context()` 取得当前 Activity 或 Service，用 `runOnAndroidMainThread()` 执行短小的原生 UI 工作，并把 JNI、线程和 Activity 生命周期边界明确封装在 Android 平台代码中。
