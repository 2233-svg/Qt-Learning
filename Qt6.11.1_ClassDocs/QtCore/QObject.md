# QObject

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QObject` 是 Qt 对象模型的根。绝大多数需要信号与槽、事件、属性、父子对象树或运行时类型信息的 Qt 类都直接或间接继承它。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QObject` 是 Qt 对象模型的根。绝大多数需要信号与槽、事件、属性、父子对象树或运行时类型信息的 Qt 类都直接或间接继承它。

**内部模型：** 把 QObject 看成一个带有生命周期和事件入口的运行时对象，而不只是一个普通 C++ 基类。parent 决定对象树所有权，信号/槽连接行为受事件循环和线程归属影响，元对象系统则让属性、动态调用和反射式查询成为可能。

**适用场景：** 自定义控件、后台 worker、定时器、网络对象、模型和需要异步通知的业务对象都通常应继承 QObject。只保存数据的值类型不需要为了使用 Qt 容器而继承它。

**典型调用链：** 创建对象并设置 parent -> 暴露 signals/slots 或普通成员函数 -> 通过 connect 建立通信 -> 在需要时处理 event/eventFilter -> 由 parent 或 deleteLater 回收。跨线程时先安排对象归属，再决定连接类型。

**先记住的坑：** 不要复制 QObject；不要在错误线程直接销毁或启动定时器；异步回调对象要用 context 或 parent 管理生命周期；deleteLater 需要事件循环真正运行。

## 2. 依赖与对象关系

- 头文件：`#include <QObject>`
- 继承自：未在类页中列出
- 直接派生类：Q3DGraphsWidgetItem、Q3DObject、Q3DScene、Q3DTheme、QAbstract3DAxis、QAbstract3DInputHandler、QAbstract3DSeries、QAbstractAnimation、QAbstractAxis、QAbstractDataProxy、QAbstractEventDispatcher、QAbstractHttpServer、QAbstractItemDelegate、QAbstractItemModel、QAbstractItemModelTester、QAbstractNetworkCache、QAbstractOAuth、QAbstractOAuthReplyHandler、QAbstractSeries、QAbstractState、QAbstractTextDocumentLayout、QAbstractTransition、QAccessibilityHints、QAccessiblePlugin、QAction、QActionGroup、QAmbientSound、QAudioBufferInput、QAudioBufferOutput、QAudioDecoder、QAudioEngine、QAudioInput、QAudioListener、QAudioOutput、QAudioRoom、QAudioSink、QAudioSource、QAxBaseObject、QAxFactory、QAxScript、QAxScriptManager、QBarModelMapper、QBarSet、QBluetoothDeviceDiscoveryAgent、QBluetoothLocalDevice、QBluetoothServer、QBluetoothServiceDiscoveryAgent、QBoxSet、QButtonGroup、QCamera、QCanBus、QCanBusDevice、QCandlestickModelMapper、QCandlestickSet、QChronoTimer、QClipboard、QCoapClient、QCompleter、QCoreApplication、QCustom3DItem、QDataWidgetMapper、QDBusAbstractAdaptor、QDBusAbstractInterface、QDBusPendingCallWatcher、QDBusServer、QDBusServiceWatcher、QDBusVirtualObject、QDesignerFormEditorInterface、QDesignerFormWindowManagerInterface、QDnsLookup、QDrag、QDtls、QDtlsClientVerifier、QEventLoop、QExtensionFactory、QExtensionManager、QFileSelector、QFileSystemWatcher、QFutureWatcher、QGenericPlugin、QGeoAreaMonitorSource、QGeoCodeReply、QGeoCodingManager、QGeoCodingManagerEngine、QGeoPositionInfoSource、QGeoRouteReply、QGeoRoutingManager、QGeoRoutingManagerEngine、QGeoSatelliteInfoSource、QGeoServiceProvider、QGesture、QGraphicsAnchor、QGraphicsEffect、QGraphicsItemAnimation、QGraphicsObject、QGraphicsScene、QGraphicsTransform、QGraphsTheme、QGrpcClientBase、QGrpcOperation、QGrpcOperationContext、QHelpEngineCore、QHelpFilterEngine、QHelpSearchEngine、QHelpSearchEngineCore、QHttpMultiPart、QIconEnginePlugin、QImageCapture、QImageIOPlugin、QInputDevice、QInputMethod、QIODevice、QItemSelectionModel、QJSEngine、QLayout、QLegendMarker、QLibrary、QLocalServer、QLowEnergyController、QLowEnergyService、QMaskGenerator、QMediaCaptureSession、QMediaDevices、QMediaPlayer、QMediaRecorder、QMimeData、QModbusDevice、QModbusReply、QMovie、QMqttClient、QMqttSubscription、QNearFieldManager、QNearFieldTarget、QNetworkAccessManager、QNetworkCookieJar、QNetworkInformation、QObjectCleanupHandler、QOffscreenSurface、QOpcUaClient、QOpcUaGdsClient、QOpcUaGenericStructHandler、QOpcUaHistoryReadResponse、QOpcUaKeyPair、QOpcUaNode、QOpcUaProvider、QOpenGLContext、QOpenGLContextGroup、QOpenGLDebugLogger、QOpenGLShader、QOpenGLShaderProgram、QOpenGLTimeMonitor、QOpenGLTimerQuery、QOpenGLVertexArrayObject、QPdfDocument、QPdfPageNavigator、QPdfPageRenderer、QPdfWriter、QPieModelMapper、QPieSlice、QPlaceManager、QPlaceManagerEngine、QPlaceReply、QPluginLoader、QQmlComponent、QQmlContext、QQmlEngineExtensionPlugin、QQmlExpression、QQmlExtensionPlugin、QQmlFileSelector、QQmlImageProviderBase、QQmlPropertyMap、QQuick3DObject、QQuickAttachedPropertyPropagator、QQuickImageResponse、QQuickItem、QQuickItemGrabResult、QQuickRenderControl、QQuickTextDocument、QQuickTextureFactory、QQuickWebEngineProfile、QRemoteObjectAbstractPersistedStore、QRemoteObjectNode、QRemoteObjectPendingCallWatcher、QRemoteObjectReplica、QRestAccessManager、QScreen、QScreenCapture、QScroller、QScxmlDataModel、QScxmlInvokableService、QScxmlInvokableServiceFactory、QScxmlStateMachine、QSensor、QSensorBackend、QSensorReading、QSessionManager、QSettings、QSGTexture、QSGTextureProvider、QSharedMemory、QShortcut、QSignalMapper、QSocketNotifier、QSoundEffect、QSpatialSound、QSqlDriver、QSqlDriverPlugin、QStyle、QStyleHints、QStylePlugin、QSvgRenderer、QSyntaxHighlighter、QSystemTrayIcon、Qt3DAnimation::QAbstractAnimation、Qt3DAnimation::QAnimationController、Qt3DAnimation::QAnimationGroup、Qt3DAnimation::QMorphTarget、Qt3DCore::QAbstractAspect、Qt3DCore::QAspectEngine、Qt3DCore::QNode、Qt3DCore::Quick::QQmlAspectEngine、Qt3DInput::QKeyEvent、Qt3DInput::QMouseEvent、Qt3DInput::QWheelEvent、Qt3DRender::QGraphicsApiFilter、Qt3DRender::QPickEvent、Qt3DRender::QRenderCapabilities、Qt3DRender::QRenderCaptureReply、Qt3DRender::QStencilOperationArguments、Qt3DRender::QStencilTestArguments、Qt3DRender::QTextureWrapMode、QTcpServer、QTextDocument、QTextObject、QTextToSpeech、QThread、QThreadPool、QTimeLine、QTimer、QTranslator、QtTaskTree::QBarrier、QtTaskTree::QNetworkReplyWrapper、QtTaskTree::QTaskInterface、QtTaskTree::QTaskTree、QtTaskTree::QTcpSocketWrapper、QUiLoader、QUndoGroup、QUndoStack、QValidator、QValue3DAxisFormatter、QVideoFrameInput、QVideoSink、QVirtualKeyboardAbstractInputMethod、QVirtualKeyboardDictionary、QVirtualKeyboardDictionaryManager、QVirtualKeyboardInputContext、QVirtualKeyboardInputEngine、QVirtualKeyboardObserver、QVirtualKeyboardTrace、QWaylandClient、QWaylandClientExtension、QWaylandObject、QWaylandQuickShellIntegration、QWaylandSurfaceGrabber、QWaylandView、QWaylandXdgOutputV1、QWaylandXdgPopup、QWaylandXdgToplevel、QWebChannel、QWebChannelAbstractTransport、QWebEngineClientHints、QWebEngineContextMenuRequest、QWebEngineCookieStore、QWebEngineDownloadRequest、QWebEngineExtensionManager、QWebEngineHistory、QWebEngineNavigationRequest、QWebEngineNewWindowRequest、QWebEngineNotification、QWebEnginePage、QWebEngineProfile、QWebEngineUrlRequestInterceptor、QWebEngineUrlRequestJob、QWebEngineUrlSchemeHandler、QWebEngineWebAuthUxRequest、QWebSocket、QWebSocketServer、QWidget、QWindow、QWindowCapture、QWinEventNotifier,、QXYModelMapper

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

把 QObject 看成一个带有生命周期和事件入口的运行时对象，而不只是一个普通 C++ 基类。parent 决定对象树所有权，信号/槽连接行为受事件循环和线程归属影响，元对象系统则让属性、动态调用和反射式查询成为可能。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

自定义控件、后台 worker、定时器、网络对象、模型和需要异步通知的业务对象都通常应继承 QObject。只保存数据的值类型不需要为了使用 Qt 容器而继承它。 使用时通常按这个过程组织：创建对象并设置 parent -> 暴露 signals/slots 或普通成员函数 -> 通过 connect 建立通信 -> 在需要时处理 event/eventFilter -> 由 parent 或 deleteLater 回收。跨线程时先安排对象归属，再决定连接类型。

```cpp
#include <QObject>

class Worker final : public QObject
{
    Q_OBJECT

public slots:
    void run() { emit finished(QStringLiteral("done")); }

 signals:
    void finished(const QString &result);
};

// QObject::connect(worker, &Worker::finished, receiver, &Receiver::onFinished);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `objectName : QString`

### 公有函数

- `QObject(QObject *parent = nullptr)`
- `virtual ~QObject()`
- `QBindable<QString> bindableObjectName()`
- `bool blockSignals(bool block)`
- `const QObjectList & children() const`
- `QMetaObject::Connection connect(const QObject *sender, const char *signal, const char *method, Qt::ConnectionType type = Qt::AutoConnection) const`
- `bool disconnect(const QObject *receiver, const char *method = nullptr) const`
- `bool disconnect(const char *signal = nullptr, const QObject *receiver = nullptr, const char *method = nullptr) const`
- `void dumpObjectInfo() const`
- `void dumpObjectTree() const`
- `QList<QByteArray> dynamicPropertyNames() const`
- `virtual bool event(QEvent *e)`
- `virtual bool eventFilter(QObject *watched, QEvent *event)`
- `T findChild(QAnyStringView name, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`
- `(since 6.7) T findChild(Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`
- `QList<T> findChildren(QAnyStringView name, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`
- `(since 6.3) QList<T> findChildren(Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`
- `QList<T> findChildren(const QRegularExpression &re, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`
- `bool inherits(const char *className) const`
- `void installEventFilter(QObject *filterObj)`
- `(since 6.11) bool isQmlExposed() const`
- `(since 6.4) bool isQuickItemType() const`
- `bool isWidgetType() const`
- `bool isWindowType() const`
- `void killTimer(int id)`
- `(since 6.8) void killTimer(Qt::TimerId id)`
- `virtual const QMetaObject * metaObject() const`
- `bool moveToThread(QThread *targetThread)`
- `QString objectName() const`
- `QObject * parent() const`
- `QVariant property(const char *name) const`
- `void removeEventFilter(QObject *obj)`
- `void setObjectName(const QString &name)`
- `(since 6.4) void setObjectName(QAnyStringView name)`
- `void setParent(QObject *parent)`
- `bool setProperty(const char *name, const QVariant &value)`
- `(since 6.6) bool setProperty(const char *name, QVariant &&value)`
- `bool signalsBlocked() const`
- `int startTimer(int interval, Qt::TimerType timerType = Qt::CoarseTimer)`
- `int startTimer(std::chrono::nanoseconds interval, Qt::TimerType timerType = Qt::CoarseTimer)`
- `QThread * thread() const`

### 公有槽函数

- `void deleteLater()`

### 信号

- `void destroyed(QObject *obj = nullptr)`
- `void objectNameChanged(const QString &objectName)`

### 静态公有成员

- `QMetaObject::Connection connect(const QObject *sender, const QMetaMethod &signal, const QObject *receiver, const QMetaMethod &method, Qt::ConnectionType type = Qt::AutoConnection)`
- `QMetaObject::Connection connect(const QObject *sender, const char *signal, const QObject *receiver, const char *method, Qt::ConnectionType type = Qt::AutoConnection)`
- `QMetaObject::Connection connect(const QObject *sender, PointerToMemberFunction signal, Functor functor)`
- `QMetaObject::Connection connect(const QObject *sender, PointerToMemberFunction signal, const QObject *context, Functor functor, Qt::ConnectionType type = Qt::AutoConnection)`
- `QMetaObject::Connection connect(const QObject *sender, PointerToMemberFunction signal, const QObject *receiver, PointerToMemberFunction method, Qt::ConnectionType type = Qt::AutoConnection)`
- `bool disconnect(const QMetaObject::Connection &connection)`
- `bool disconnect(const QObject *sender, const QMetaMethod &signal, const QObject *receiver, const QMetaMethod &method)`
- `bool disconnect(const QObject *sender, const char *signal, const QObject *receiver, const char *method)`
- `bool disconnect(const QObject *sender, PointerToMemberFunction signal, const QObject *receiver, PointerToMemberFunction method)`
- `const QMetaObject staticMetaObject`
- `QString tr(const char *sourceText, const char *disambiguation = nullptr, int n = -1)`

### 保护函数

- `virtual void childEvent(QChildEvent *event)`
- `virtual void connectNotify(const QMetaMethod &signal)`
- `virtual void customEvent(QEvent *event)`
- `virtual void disconnectNotify(const QMetaMethod &signal)`
- `bool isSignalConnected(const QMetaMethod &signal) const`
- `int receivers(const char *signal) const`
- `QObject * sender() const`
- `int senderSignalIndex() const`
- `virtual void timerEvent(QTimerEvent *event)`

### 相关非成员函数

- `QObjectList`
- `(since 6.8) enum class TimerId { Invalid }`
- `T qobject_cast(QObject *object)`
- `T qobject_cast(const QObject *object)`

### 公开宏

- `(since 6.7) QT_NO_CONTEXTLESS_CONNECT`
- `QT_NO_NARROWING_CONVERSIONS_IN_CONNECT`
- `Q_CLASSINFO(Name, Value)`
- `Q_EMIT`
- `Q_ENUM(...)`
- `Q_ENUM_NS(...)`
- `Q_FLAG(...)`
- `Q_FLAG_NS(...)`
- `Q_GADGET`
- `(since 6.3) Q_GADGET_EXPORT(EXPORT_MACRO)`
- `Q_INTERFACES(...)`
- `Q_INVOKABLE`
- `(since 6.0) Q_MOC_INCLUDE`
- `Q_NAMESPACE`
- `Q_NAMESPACE_EXPORT(EXPORT_MACRO)`
- `Q_OBJECT`
- `Q_PROPERTY(...)`
- `Q_REVISION`
- `Q_SET_OBJECT_NAME(Object)`
- `Q_SIGNAL`
- `Q_SIGNALS`
- `Q_SLOT`
- `Q_SLOTS`

### 相关非成员函数

- `Constant Value Description`
- `QObject::TimerId::Invalid 0 Represents a no-op timer ID; its usage depends on the context, for example, this is the value returned by QObject::startTimer() to indicate it failed to start a timer; whereas QChronoTimer::id() returns this value when the timer is inactive, that is, timer.isActive() returns false.`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 95 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[bindable] objectName : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QObject` 的配置属性。初始化或状态切换时通过 `setObjectName(...)` 设置，之后用 `objectName()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`objectName`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit invokable] QObject::QObject(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QObject` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QObject::~QObject()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QObject` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QObject::blockSignals(bool block)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::blockSignals` 用于计算、查询或取得与“阻塞或屏蔽、Signals”相关的操作。调用时要先确认当前状态和 `block` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `block`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QObject::childEvent(QChildEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::childEvent` 用于执行与“child、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QChildEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QObjectList &QObject::children() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::children` 用于计算、查询或取得与“children”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QObjectList &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QObjectList &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMetaObject::Connection QObject::connect(const QObject *sender, const QMetaMethod &signal, const QObject *receiver, const QMetaMethod &method, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `connect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMetaObject::Connection`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `const QMetaMethod &`。没有默认值，调用时必须提供。传入 `const QMetaMethod &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `const QMetaMethod &`。没有默认值，调用时必须提供。传入 `const QMetaMethod &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 通常与信号、槽、context 或 `QMetaObject::Connection` 一起使用；断开或 context 销毁后回调不应再访问旧对象。

### `[static] QMetaObject::Connection QObject::connect(const QObject *sender, const char *signal, const QObject *receiver, const char *method, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `connect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMetaObject::Connection`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 通常与信号、槽、context 或 `QMetaObject::Connection` 一起使用；断开或 context 销毁后回调不应再访问旧对象。

### `[static] template <typename PointerToMemberFunction, typename Functor> QMetaObject::Connection QObject::connect(const QObject *sender, PointerToMemberFunction signal, Functor functor)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `connect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename PointerToMemberFunction, typename Functor> QMetaObject::Connection`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `PointerToMemberFunction`。没有默认值，调用时必须提供。传入 `PointerToMemberFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `functor`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与信号、槽、context 或 `QMetaObject::Connection` 一起使用；断开或 context 销毁后回调不应再访问旧对象。

### `QMetaObject::Connection QObject::connect(const QObject *sender, const char *signal, const char *method, Qt::ConnectionType type = Qt::AutoConnection) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connect`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QMetaObject::Connection`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `method`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 通常与信号、槽、context 或 `QMetaObject::Connection` 一起使用；断开或 context 销毁后回调不应再访问旧对象。

### `[static] template <typename PointerToMemberFunction, typename Functor> QMetaObject::Connection QObject::connect(const QObject *sender, PointerToMemberFunction signal, const QObject *context, Functor functor, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `connect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename PointerToMemberFunction, typename Functor> QMetaObject::Connection`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `PointerToMemberFunction`。没有默认值，调用时必须提供。传入 `PointerToMemberFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `context`：类型为 `const QObject *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `functor`：类型为 `Functor`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 通常与信号、槽、context 或 `QMetaObject::Connection` 一起使用；断开或 context 销毁后回调不应再访问旧对象。

### `[static] template <typename PointerToMemberFunction> QMetaObject::Connection QObject::connect(const QObject *sender, PointerToMemberFunction signal, const QObject *receiver, PointerToMemberFunction method, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `connect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename PointerToMemberFunction> QMetaObject::Connection`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `PointerToMemberFunction`。没有默认值，调用时必须提供。传入 `PointerToMemberFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `PointerToMemberFunction`。没有默认值，调用时必须提供。传入 `PointerToMemberFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 通常与信号、槽、context 或 `QMetaObject::Connection` 一起使用；断开或 context 销毁后回调不应再访问旧对象。

### `[virtual protected] void QObject::connectNotify(const QMetaMethod &signal)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectNotify`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `signal`：类型为 `const QMetaMethod &`。没有默认值，调用时必须提供。传入 `const QMetaMethod &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与信号、槽、context 或 `QMetaObject::Connection` 一起使用；断开或 context 销毁后回调不应再访问旧对象。

### `[virtual protected] void QObject::customEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::customEvent` 用于执行与“custom、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QObject::deleteLater()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `deleteLater`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常与异步完成信号、线程退出和事件循环一起使用；它不是立即 delete。

### `[signal] void QObject::destroyed(QObject *obj = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QObject` 发出的通知信号 `destroyed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `obj`：类型为 `QObject *`。默认值为 `nullptr`。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QObject::disconnect(const QMetaObject::Connection &connection)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `disconnect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `connection`：类型为 `const QMetaObject::Connection &`。没有默认值，调用时必须提供。传入 `const QMetaObject::Connection &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QObject::disconnect(const QObject *sender, const QMetaMethod &signal, const QObject *receiver, const QMetaMethod &method)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `disconnect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `const QMetaMethod &`。没有默认值，调用时必须提供。传入 `const QMetaMethod &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `const QMetaMethod &`。没有默认值，调用时必须提供。传入 `const QMetaMethod &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QObject::disconnect(const QObject *sender, const char *signal, const QObject *receiver, const char *method)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `disconnect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QObject::disconnect(const QObject *receiver, const char *method = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `disconnect`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `const char *`。默认值为 `nullptr`。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QObject::disconnect(const char *signal = nullptr, const QObject *receiver = nullptr, const char *method = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `disconnect`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `signal`：类型为 `const char *`。默认值为 `nullptr`。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。默认值为 `nullptr`。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `const char *`。默认值为 `nullptr`。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] template <typename PointerToMemberFunction> bool QObject::disconnect(const QObject *sender, PointerToMemberFunction signal, const QObject *receiver, PointerToMemberFunction method)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `disconnect`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`template <typename PointerToMemberFunction> bool`。
- 参数 `sender`：类型为 `const QObject *`。没有默认值，调用时必须提供。发送者对象。它是信号/事件来源，不等于当前处理对象。
- 参数 `signal`：类型为 `PointerToMemberFunction`。没有默认值，调用时必须提供。传入 `PointerToMemberFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `method`：类型为 `PointerToMemberFunction`。没有默认值，调用时必须提供。传入 `PointerToMemberFunction` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QObject::disconnectNotify(const QMetaMethod &signal)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `disconnectNotify`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `signal`：类型为 `const QMetaMethod &`。没有默认值，调用时必须提供。传入 `const QMetaMethod &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QObject::dumpObjectInfo() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::dumpObjectInfo` 用于执行与“dump、Object、Info”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QObject::dumpObjectTree() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::dumpObjectTree` 用于执行与“dump、Object、Tree”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QByteArray> QObject::dynamicPropertyNames() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::dynamicPropertyNames` 用于计算、查询或取得与“dynamic、Property、Names”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QByteArray>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QByteArray>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QObject::event(QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常要先判断事件类型，再决定 accept/ignore 和是否调用基类实现。

### `[virtual] bool QObject::eventFilter(QObject *watched, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::eventFilter` 用于计算、查询或取得与“event、Filter”相关的操作。调用时要先确认当前状态和 `watched`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `watched`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 通常要先判断事件类型，再决定 accept/ignore 和是否调用基类实现。

### `template <typename T> T QObject::findChild(QAnyStringView name, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::findChild` 用于计算、查询或取得与“查找、Child”相关的操作。调用时要先确认当前状态和 `name`、`options` 的有效范围；返回类型是 `template <typename T> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `options`：类型为 `Qt::FindChildOptions`。默认值为 `Qt::FindChildrenRecursively`。传入 `Qt::FindChildOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] template <typename T> T QObject::findChild(Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::findChild` 用于计算、查询或取得与“查找、Child”相关的操作。调用时要先确认当前状态和 `options` 的有效范围；返回类型是 `template <typename T> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数 `options`：类型为 `Qt::FindChildOptions`。默认值为 `Qt::FindChildrenRecursively`。传入 `Qt::FindChildOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QList<T> QObject::findChildren(QAnyStringView name, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::findChildren` 用于计算、查询或取得与“查找、Children”相关的操作。调用时要先确认当前状态和 `name`、`options` 的有效范围；返回类型是 `template <typename T> QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> QList<T>`。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `options`：类型为 `Qt::FindChildOptions`。默认值为 `Qt::FindChildrenRecursively`。传入 `Qt::FindChildOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename T> QList<T> QObject::findChildren(Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::findChildren` 用于计算、查询或取得与“查找、Children”相关的操作。调用时要先确认当前状态和 `options` 的有效范围；返回类型是 `template <typename T> QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> QList<T>`。
- 参数 `options`：类型为 `Qt::FindChildOptions`。默认值为 `Qt::FindChildrenRecursively`。传入 `Qt::FindChildOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> QList<T> QObject::findChildren(const QRegularExpression &re, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::findChildren` 用于计算、查询或取得与“查找、Children”相关的操作。调用时要先确认当前状态和 `re`、`options` 的有效范围；返回类型是 `template <typename T> QList<T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> QList<T>`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `Qt::FindChildOptions`。默认值为 `Qt::FindChildrenRecursively`。传入 `Qt::FindChildOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QObject::inherits(const char *className) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::inherits` 用于计算、查询或取得与“inherits”相关的操作。调用时要先确认当前状态和 `className` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `className`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QObject::installEventFilter(QObject *filterObj)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QObject` 添加依赖、数据或子对象的 API `installEventFilter`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `filterObj`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.11] bool QObject::isQmlExposed() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isQmlExposed`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] bool QObject::isQuickItemType() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isQuickItemType`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] bool QObject::isSignalConnected(const QMetaMethod &signal) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSignalConnected`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `signal`：类型为 `const QMetaMethod &`。没有默认值，调用时必须提供。传入 `const QMetaMethod &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QObject::isWidgetType() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isWidgetType`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QObject::isWindowType() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isWindowType`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QObject::killTimer(int id)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::killTimer` 用于执行与“kill、Timer”相关的操作。调用时要先确认当前状态和 `id` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QObject::killTimer(Qt::TimerId id)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::killTimer` 用于执行与“kill、Timer”相关的操作。调用时要先确认当前状态和 `id` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `Qt::TimerId`。没有默认值，调用时必须提供。传入 `Qt::TimerId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] const QMetaObject *QObject::metaObject() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::metaObject` 用于计算、查询或取得与“meta、Object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QMetaObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QMetaObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QObject::moveToThread(QThread *targetThread)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::moveToThread` 用于计算、查询或取得与“移动、转换输出、Thread”相关的操作。调用时要先确认当前状态和 `targetThread` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `targetThread`：类型为 `QThread *`。没有默认值，调用时必须提供。传入 `QThread *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[private signal] void QObject::objectNameChanged(const QString &objectName)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `objectNameChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `objectName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject *QObject::parent() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::parent` 用于计算、查询或取得与“父对象”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QObject::property(const char *name) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::property` 用于计算、查询或取得与“property”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] int QObject::receivers(const char *signal) const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::receivers` 用于计算、查询或取得与“receivers”相关的操作。调用时要先确认当前状态和 `signal` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `signal`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QObject::removeEventFilter(QObject *obj)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeEventFilter`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `obj`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] QObject *QObject::sender() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QObject` 的核心操作 `sender`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] int QObject::senderSignalIndex() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QObject` 的核心操作 `senderSignalIndex`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QObject::setObjectName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setObjectName`。调用它会改变 `QObject` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] void QObject::setObjectName(QAnyStringView name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setObjectName`。调用它会改变 `QObject` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QObject::setParent(QObject *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setParent`。调用它会改变 `QObject` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `QObject *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QObject::setProperty(const char *name, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProperty`。调用它会改变 `QObject` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] bool QObject::setProperty(const char *name, QVariant &&value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProperty`。调用它会改变 `QObject` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `QVariant &&`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QObject::signalsBlocked() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::signalsBlocked` 用于计算、查询或取得与“signals、Blocked”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QObject::startTimer(int interval, Qt::TimerType timerType = Qt::CoarseTimer)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startTimer`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`int`。
- 参数 `interval`：类型为 `int`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。
- 参数 `timerType`：类型为 `Qt::TimerType`。默认值为 `Qt::CoarseTimer`。传入 `Qt::TimerType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QObject::startTimer(std::chrono::nanoseconds interval, Qt::TimerType timerType = Qt::CoarseTimer)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startTimer`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`int`。
- 参数 `interval`：类型为 `std::chrono::nanoseconds`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。
- 参数 `timerType`：类型为 `Qt::TimerType`。默认值为 `Qt::CoarseTimer`。传入 `Qt::TimerType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QThread *QObject::thread() const`

**API 类别：** 成员函数说明

**中文解读：** `QObject::thread` 用于计算、查询或取得与“thread”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QThread *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QThread *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QObject::timerEvent(QTimerEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QObject::timerEvent` 用于执行与“timer、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QTimerEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QObject::tr(const char *sourceText, const char *disambiguation = nullptr, int n = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `tr`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `sourceText`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `disambiguation`：类型为 `const char *`。默认值为 `nullptr`。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `n`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QMetaObject QObject::staticMetaObject`

**API 类别：** Member Variable Documentation

**中文解读：** 这是 `QObject` 的配置属性。初始化或状态切换时通过 `setStaticMetaObject(...)` 设置，之后用 `staticMetaObject()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:staticMetaObject`。
- 属性名：`QObject`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObjectList`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QObject` 的 `Q、Object、List` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] enum class TimerId`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QObject` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T> T qobject_cast(const QObject *object)`

**API 类别：** 相关非成员函数

**中文解读：** `QObject::qobject_cast` 用于计算、查询或取得与“qobject、cast”相关的操作。调用时要先确认当前状态和 `object` 的有效范围；返回类型是 `template <typename T> T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> T`。
- 参数 `object`：类型为 `const QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QT_NO_CONTEXTLESS_CONNECT`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `连接` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QT_NO_NARROWING_CONVERSIONS_IN_CONNECT`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `连接` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_CLASSINFO(Name, Value)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_CLASSINFO` 用于执行与“CLASSINFO”相关的操作。调用时要先确认当前状态和 `Name`、`Value` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `Name`：类型为 `未标注`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `Value`：类型为 `未标注`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_EMIT`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `EMIT` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ENUM(...)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_ENUM` 用于执行与“ENUM”相关的操作。调用时要先确认当前状态和 `...` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ENUM_NS(...)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_ENUM_NS` 用于执行与“NS”相关的操作。调用时要先确认当前状态和 `...` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_FLAG(...)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_FLAG` 用于执行与“FLAG”相关的操作。调用时要先确认当前状态和 `...` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_FLAG_NS(...)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_FLAG_NS` 用于执行与“NS”相关的操作。调用时要先确认当前状态和 `...` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_GADGET`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `GADGET` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] Q_GADGET_EXPORT(EXPORT_MACRO)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_GADGET_EXPORT` 用于执行与“EXPORT”相关的操作。调用时要先确认当前状态和 `EXPORT_MACRO` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `EXPORT_MACRO`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_INTERFACES(...)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_INTERFACES` 用于执行与“INTERFACES”相关的操作。调用时要先确认当前状态和 `...` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_INVOKABLE`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `INVOKABLE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] Q_MOC_INCLUDE`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `INCLUDE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_NAMESPACE`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `NAMESPACE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_NAMESPACE_EXPORT(EXPORT_MACRO)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_NAMESPACE_EXPORT` 用于执行与“EXPORT”相关的操作。调用时要先确认当前状态和 `EXPORT_MACRO` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `EXPORT_MACRO`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_OBJECT`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `OBJECT` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_PROPERTY(...)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_PROPERTY` 用于执行与“PROPERTY”相关的操作。调用时要先确认当前状态和 `...` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_REVISION`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `REVISION` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_SET_OBJECT_NAME(Object)`

**API 类别：** 宏说明

**中文解读：** `QObject::Q_SET_OBJECT_NAME` 用于执行与“名称”相关的操作。调用时要先确认当前状态和 `Object` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `Object`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_SIGNAL`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `SIGNAL` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_SIGNALS`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `SIGNALS` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_SLOT`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `SLOT` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_SLOTS`

**API 类别：** 宏说明

**中文解读：** 这是 `QObject` 的 `SLOTS` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<QString> bindableObjectName()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableObjectName`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<QString>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString objectName() const`

**API 类别：** 公有函数

**中文解读：** `QObject::objectName` 用于计算、查询或取得与“object、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QMetaObject staticMetaObject`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `const`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T qobject_cast(QObject *object)`

**API 类别：** 相关非成员函数

**中文解读：** `QObject::qobject_cast` 用于计算、查询或取得与“qobject、cast”相关的操作。调用时要先确认当前状态和 `object` 的有效范围；返回类型是 `T`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`T`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Constant Value Description`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QObject` 的 `Constant` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject::TimerId::Invalid 0 Represents a no-op timer ID; its usage depends on the context, for example, this is the value returned by QObject::startTimer() to indicate it failed to start a timer; whereas QChronoTimer::id() returns this value when the timer is inactive, that is, timer.isActive() returns false.`

**API 类别：** 相关非成员函数

**中文解读：** 这是启动/建立资源的 API `startTimer`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QObject::TimerId::Invalid 0 Represents a no-op timer ID; its usage depends on the context, for example, this is the value returned by`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不要复制 QObject；不要在错误线程直接销毁或启动定时器；异步回调对象要用 context 或 parent 管理生命周期；deleteLater 需要事件循环真正运行。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QObject` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
