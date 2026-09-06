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

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[bindable] objectName : QString`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含该对象的名称。
你可以用`findChild()`来按名称（和类型）找到对象。你可以用`findChildren()`找到一组对象。
默认情况下，该属性包含空字符串。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `objectName()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 qDebug("MyClass::setPrecision(): (%s) invalid precision %f",
        qPrintable(objectName()), newPrecision);
```

### `[explicit invokable] QObject::QObject(QObject *parent = nullptr)`

**作用与语义：**

构造一个带有父对象`parent`的对象。
对象的父节点可以被视为对象的所有者。例如，对话框是其所包含的确认和取消按钮的父节点。
父对象的解散器会销毁所有子对象。
将 `parent` 设置为 `nullptr` 构建一个没有父的对象。如果该对象是控件，它将成为顶层窗口。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual noexcept] QObject::~QObject()`

**作用与语义：**

销毁该对象，删除其所有子对象。
所有与对象之间的信号都会自动断开连接，任何待发布的事件都会从事件队列中移除。然而，使用`deleteLater()`通常比直接删除`QObject`子类更安全。
警告：所有子对象均已删除。如果这些对象中的任何一个在栈或全局中，迟早你的程序会崩溃。我们不建议从父对象外部持有指向子对象的指针。如果你仍然这样做，`destroyed()`信号会给你机会检测对象是否被销毁。
警告：在`QObject`处理已送达事件时删除可能导致崩溃。如果`QObject`存在于与当前执行线程不同的线程中，千万不要直接删除。请使用`deleteLater()`，这会导致事件循环在所有待处理事件交付后删除该对象。

### `[noexcept] bool QObject::blockSignals(bool block)`

**作用与语义：**

如果`block`为真，该对象发出的信号会被阻断（即发射信号不会调用与之相关的任何东西）。如果`block`为假，则不会发生此类阻断。
返回值是之前的`signalsBlocked()`值。
注意，即使该物体的信号被阻挡，`destroyed()`信号仍会被发射。
被阻断时发出的信号不会被缓冲。

### `[virtual protected] void QObject::childEvent(QChildEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现以接收子事件。事件通过`event`参数传递。
在添加或移除子节点时，`QEvent::ChildAdded`和`QEvent::ChildRemoved`事件会发送到对象。在这两种情况下，你只能依赖子节点是`QObject`，或者如果`isWidgetType()`返回`true`，则是`QWidget`。（这是因为在`ChildAdded`情况下，子节点尚未完全构造，而在`ChildRemoved`情况下，子节点可能已经被摧毁了。）。
`QEvent::ChildPolished`事件在子节点被精炼时发送到小部件，或者当子节点被添加时。如果你收到子节点精炼事件，子节点的构建通常已完成。但这并不保证，在小部件构造函数执行过程中可能会传递多个精炼事件。
每当有子小部件，你会收到一个`ChildAdded`事件、零个或多个`ChildPolished`事件和一个`ChildRemoved`事件。
如果`ChildPolished`事件在添加后立即被移除，则该事件被省略。如果一个孩子在建设和拆除过程中多次被抛光，你可能会为同一孩子收到多个子抛光事件，每次都是不同的虚拟表。

### `const QObjectList &QObject::children() const`

**作用与语义：**

返回子对象列表。`QObjectList`类在`<QObject>`头文件中定义如下：
第一个添加的子节点是列表中`first`对象，最后一个子节点是列表中`last`对象，即新子节点会被附加在末尾。
注意，当`QWidget`子节点被`raised`或`lowered`时，列表顺序会发生变化。被提升的控件成为列表中的最后一个对象，而被降低的控件则成为列表中的第一个对象。

**官方示例：**

```cpp
 typedef QList<QObject*> QObjectList;
```

### `[static] QMetaObject::Connection QObject::connect(const QObject *sender, const QMetaMethod &signal, const QObject *receiver, const QMetaMethod &method, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

从`sender`对象的`signal`创建给定`type`到`receiver`对象`method`的连接。返回连接的句柄，可用于后续断开连接。
如果连接句柄无法创建连接，比如参数无效，连接句柄将无效。你可以通过将`QMetaObject::Connection`投射为布尔值来检查它是否有效。
该函数的工作原理与`connect(const QObject *sender, const char *signal, const QObject *receiver, const char *method, Qt::ConnectionType type)`相同，但它使用`QMetaMethod`来指定信号和方法。

### `[static] QMetaObject::Connection QObject::connect(const QObject *sender, const char *signal, const QObject *receiver, const char *method, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

创建给定`type`从`sender`对象`signal`到`receiver`对象`method`的连接。返回连接的句柄，可用于后续断开连接。
在指定`signal`和`method`时，您必须使用`SIGNAL()`和`SLOT()`宏，例如：
此示例确保标签始终显示当前滚动条值。注意信号和槽位参数不得包含变量名，只能包含类型。例如，以下方法不工作，返回 false：
信号也可以连接到另一个信号：
在这个例子中，`MyWidget`构造函数中继来自私有成员变量的信号，并以与`MyWidget`相关的名称提供。
一个信号可以连接到多个槽函数和信号。一个槽函数可以连接多个信号。
如果信号连接到多个槽函数，信号发出时槽函数按连接顺序激活。
如果函数成功将信号连接到槽函数，函数会返回一个代表连接的句柄`QMetaObject::Connection`。如果连接句柄无法创建连接，例如`QObject`无法验证`signal`或`method`的存在，或者它们的签名不兼容，连接句柄将无效。你可以通过将句柄转换为布尔值来检测句柄是否有效。
默认情况下，每次连接都会发出一个信号;重复连接会发出两个信号。你可以通过一次`disconnect()`调用切断所有这些连接。如果你通过`Qt::UniqueConnection` `type`，只有当连接不是重复时才会建立。如果已经有重复（完全相同的信号到同一对象的完全相同的槽函数），连接将失败，连接将返回无效`QMetaObject::Connection`。
注意：Qt：：UniqueConnections 不适用于 lambda、非成员函数和函子;它们仅适用于连接成员函数。
可选的`type`参数描述了要建立的连接类型。特别地，它决定了某个特定信号是立即送入槽位，还是排队等待后续传递。如果信号被排队，参数必须是Qt元对象系统已知的类型，因为Qt需要复制参数以在幕后事件中存储。如果你尝试使用队列连接并收到错误信息。
在建立连接前，先调用`qRegisterMetaType()`注册数据类型。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 QLabel *label = new QLabel;
 QScrollBar *scrollBar = new QScrollBar;
 QObject::connect(scrollBar, SIGNAL(valueChanged(int)),
                  label,  SLOT(setNum(int)));
```

### `[static] template <typename PointerToMemberFunction, typename Functor> QMetaObject::Connection QObject::connect(const QObject *sender, PointerToMemberFunction signal, Functor functor)`

**作用与语义：**

从`sender`对象中的`signal`创建连接到`functor`，并返回连接的句柄。
信号必须是标头中声明为信号的函数。槽函数可以是任何可以连接到信号的函数或函子。如果信号的参数数至少与槽函数相同，那么槽函数可以连接到给定信号。信号中对应参数类型与槽之间必须存在隐式转换。
还可以使用λ表达式：
如果发送端被摧毁，连接会自动断开。不过，你应该注意在信号发出时，函子内使用的任何对象仍然活着。
因此，建议使用 connect() 的超载，同时也将 `QObject` 作为接收/上下文。通过定义 `QT_NO_CONTEXTLESS_CONNECT` 宏，可以禁用无上下文超载的使用。
重载函数可以通过`qOverload`来解决。
注意：该功能会超载`QObject::connect()`。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 void someFunction();
 //...
 void someOtherFunction()
 {
     QPushButton *button = new QPushButton;
     QObject::connect(button, &QPushButton::clicked, someFunction);
 }
```

### `QMetaObject::Connection QObject::connect(const QObject *sender, const char *signal, const char *method, Qt::ConnectionType type = Qt::AutoConnection) const`

**作用与语义：**

将`sender`对象的`signal`连接到该对象的 `method`。
相当于connect（`sender`、`signal`、`this`、`method`、`type`）。
你建立的每个连接都会发出一个信号，所以重复连接会发出两个信号。你可以用`disconnect()`断开连接。
注意：该功能会`QObject::connect()`重载。
注意：该功能是线程安全的。

### `[static] template <typename PointerToMemberFunction, typename Functor> QMetaObject::Connection QObject::connect(const QObject *sender, PointerToMemberFunction signal, const QObject *context, Functor functor, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

从对象中的`signal`创建给定`type`的连接`sender`到`functor`，放置在特定事件循环中的`context`，并返回连接的句柄。
注意：Qt：：UniqueConnections 不适用于 lambda、非成员函数和函子;它们仅适用于连接成员函数。
信号必须是标头中声明为信号的函数。槽函数可以是任何可以连接到信号的函数或函子。如果信号的参数数至少与槽函数相同，那么槽函数可以连接到给定信号。信号中对应参数类型与槽之间必须存在隐式转换。
还可以使用λ表达式：
如果发送方或上下文被破坏，连接会自动断开。不过，你应该注意在信号发出时，函子内使用的任何对象仍然活着。
重载函数可以通过`qOverload`来解决。
注意：该功能会让`QObject::connect()`重载。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 void someFunction();
 //...
 void someOtherFunction()
 {
     QPushButton *button = new QPushButton;
     QObject::connect(button, &QPushButton::clicked, this, someFunction, Qt::QueuedConnection);
 }
```

### `[static] template <typename PointerToMemberFunction> QMetaObject::Connection QObject::connect(const QObject *sender, PointerToMemberFunction signal, const QObject *receiver, PointerToMemberFunction method, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

创建给定`type`从`sender`对象`signal`到`receiver`对象`method`的连接。返回连接的句柄，可用于后续断开连接。
信号必须是标头中声明为信号的函数。槽函数可以是任何可以连接到信号的成员函数。如果该信号的参数数至少与该槽位相同，并且信号中对应参数类型与槽之间存在隐式转换，那么该槽就可以连接到某个信号。
此示例确保标签始终显示当前行编辑文本。
一个信号可以连接到多个槽函数和信号。一个槽函数可以连接多个信号。
如果信号连接到多个槽函数，信号发出时槽函数的激活顺序与连接顺序相同。
如果函数成功将信号连接到槽函数，则返回连接的句柄。如果连接句柄无法创建连接，例如`QObject`无法验证`signal`的存在（如果它未被声明为信号）则无效。您可以通过将`QMetaObject::Connection`投射为布尔值来验证其有效性。
默认情况下，每连接一个信号都会发出;重复连接会发出两个信号。你可以用一次`disconnect()`调用切断所有这些连接。如果你通过`Qt::UniqueConnection` `type`，只有当连接不是重复时才会建立。如果已经有重复（完全相同的信号到同一对象的完全相同的槽），连接将失败，连接会返回无效`QMetaObject::Connection`。
可选的`type`参数描述了要建立的连接类型。特别地，它决定了某个特定信号是立即送达到某个槽函数，还是排队等待稍后传递。如果信号被排队，参数必须是Qt元对象系统已知的类型，因为Qt需要复制参数以在幕后事件中存储。如果你尝试使用队列连接并收到错误信息。
一定要用 `Q_DECLARE_METATYPE` 声明参数类型。
重载函数可以通过`qOverload`来解决。
注意：该功能会让`QObject::connect()`重载。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 QLabel *label = new QLabel;
 QLineEdit *lineEdit = new QLineEdit;
 QObject::connect(lineEdit, &QLineEdit::textChanged,
                 label,  &QLabel::setText);
```

### `[virtual protected] void QObject::connectNotify(const QMetaMethod &signal)`

**作用与语义：**

当该对象中的某物连接到`signal`时，调用了这个虚拟函数。
如果你想将`signal`与特定信号进行比较，可以使用以下`QMetaMethod::fromSignal()`：
警告：该函数违反面向对象的模块化原则。不过，当你需要执行昂贵操作时，只有在某物连接到信号时，它可能有用。
警告：该函数是从执行连接的线程调用的，该线程可能与该对象所在线程不同。该函数也可能被调用时`QObject`内部互斥体被锁定。因此，不允许重新输入任何`QObject`函数，包括`isSignalConnected()`，来自你的重实现。如果你在重实现中锁定了互斥体，请确保不要调用`QObject`函数，否则会导致死锁。

**官方示例：**

```cpp
     if (signal == QMetaMethod::fromSignal(&MyObject::valueChanged)) {
         // signal is valueChanged
     }
```

### `[virtual protected] void QObject::customEvent(QEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现以接收自定义事件。自定义事件是用户定义的事件，其类型值至少与`QEvent::Type`枚举的`QEvent::User`项相当，通常是`QEvent`子类。事件通过`event`参数传递。

### `[slot] void QObject::deleteLater()`

**作用与语义：**

将该对象排入删除。
当控件返回事件循环时，该对象将被删除。如果在调用该函数时事件循环未运行（例如，在`QCoreApplication::exec()`之前的对象上调用了deleteLater()，则在事件循环启动后该对象将被删除。如果在主事件循环停止后调用deleteLater()，则该对象不会被删除。如果在没有运行事件循环的线程中调用deleteLater()，则该对象在线程结束时将被销毁。
在`QThread`中使用工作`QObject`时，一个常见的模式是将线程的`finished()`信号连接到工作者的`deleteLater()`槽，以确保安全删除：
注意，进入和离开新的事件循环（例如打开模态对话框）不会执行延迟删除;要删除对象，控件必须返回调用deleteLater()的事件循环。这不适用于在之前嵌套事件循环仍在运行时被删除的对象：Qt事件循环会在新的嵌套事件循环开始时立即删除这些对象。
在 Qt 未通过 `QCoreApplication::exec()` 或 `QEventLoop::exec()` 驱动事件调度器的情况下，延迟删除不会自动处理。为确保此情景中的延迟删除，可以使用以下变通方法：
注意：该功能是线程安全的。

**官方示例：**

```cpp
 connect(thread, &QThread::finished, worker, &QObject::deleteLater);
```

### `[signal] void QObject::destroyed(QObject *obj = nullptr)`

**作用与语义：**

该信号在物体`obj`被摧毁前立即发出，且在任何`QPointer`实例被通知后，且无法被阻挡。
该信号发出后，所有物体的子节点都会立即被摧毁。

### `[static] bool QObject::disconnect(const QMetaObject::Connection &connection)`

**作用与语义：**

断开连接。
如果`connection`无效或已被断开，则不做任何操作并返回false。

### `[static] bool QObject::disconnect(const QObject *sender, const QMetaMethod &signal, const QObject *receiver, const QMetaMethod &method)`

**作用与语义：**

将对象`sender`中的`signal`与对象`receiver`中的`method`断开连接。如果连接成功断开，返回`true`;否则返回`false`。
该函数提供与`disconnect(const QObject *sender, const char *signal, const QObject *receiver, const char *method)`相同的可能性，但使用`QMetaMethod`表示信号和断开方法。
此外，如果以下情况，该函数返回false且没有信号和断开的槽函数：
- `signal`不是发送者类或其父类的成员。
- `method` 不是接收者类或其父类的成员。
- `signal`实例表示不是一个信号。
注意：在`connect()`及相应的disconnect()调用中，使用相同的语法，指针到成员函数或基于字符串的函数，使用`SIGNAL`和`SLOT`宏。
为避免不匹配，存储`connect()`返回的连接句柄，并在调用`disconnect()`时使用它。
注意：如果排队连接断开，已排程的事件仍可能被传递，导致接收端在连接断开后被调用。
QMetaMethod() 可作为通配符，意为“任意信号”或“接收对象中的任意槽”。同样，`nullptr` 也可以用于“任意接收对象”中的 `receiver`。此时方法也应为 QMetaMethod()。`sender`参数绝不应`nullptr`。
注意：断开所有信号槽连接也会断开`QObject::destroyed()`信号（如果已连接的话）。这样做可能会对依赖该信号清理资源的类产生不利影响。建议仅断开通过应用代码连接的特定信号。

### `[static] bool QObject::disconnect(const QObject *sender, const char *signal, const QObject *receiver, const char *method)`

**作用与语义：**

在对象`sender`中断开`signal`与对象`receiver`中的`method`。如果连接成功断开，返回`true`;否则返回`false`。
当任一物体被摧毁时，信号槽连接会被移除。
disconnect() 通常有三种用法，如下示例所示。
- 断开所有连接到物体信号的设备：
`QObject::disconnect`（myObject， nullptr， nullptr， nullptr）;

等价于非静态超载函数。

myObject->disconnect();
- 断开所有连接到特定信号的设备：
`QObject::disconnect`（myObject， SIGNAL（mySignal()）， nullptr， nullptr）;

等价于非静态超载函数。

myObject->disconnect（SIGNAL（mySignal()）;
- 断开特定接收机：
`QObject::disconnect`（myObject， nullptr， myReceiver， nullptr）;

等价于非静态超载函数。

myObject->disconnect（myReceiver）;
注意：在`connect()`及相应的 disconnect() 调用中，使用相同的语法、指针到成员函数或基于字符串的 `SLOT` `SIGNAL` Scripter 到 Member-function 或基于字符串的宏，使用和相应的 disconnect() 调用。
为避免不匹配，存储`connect()`返回的连接句柄，并在调用`disconnect()`时使用它。
注意：如果排队连接断开，已排程的事件仍可能被传递，导致接收端在连接断开后被调用。
`nullptr`可用作万用牌，分别表示“任意信号”、“任何接收对象”或“接收对象中的任意槽位”。
`sender`可能永远不会`nullptr`。（你不能在一次通话中断开多个物体的信号。）。
如果`signal` `nullptr`，则断开`receiver`并`method`任何信号。如果不，则仅断开指定的信号。
如果`receiver` `nullptr`，它会断开所有连接到`signal`的东西。如果不`receiver`，其他物体的槽位不会断开。
如果`method` `nullptr`，则断开所有连接到`receiver`的设备。如果不连接，只有名为`method`的槽被断开，其他槽位保持原样。如果`receiver`被排除，`method`必须`nullptr`，因此你不能断开所有物体上具体命名的槽。
注意：断开所有信号槽连接也会切断`QObject::destroyed()`信号（如果已连接）也断开。这样做可能会对依赖该信号清理资源的类产生不利影响。建议仅断开通过应用代码连接的特定信号。
注意：该功能是线程安全的。

### `bool QObject::disconnect(const QObject *receiver, const char *method = nullptr) const`

**作用与语义：**

切断该物体中所有信号与`receiver` `method`的连接。
注意：在`connect()`及相应的disconnect()调用中，使用相同的语法，指针到成员函数或基于字符串的，使用`SIGNAL`和`SLOT`宏。
为避免不匹配，存储`connect()`返回的连接句柄，并在调用`disconnect()`时使用它。
注意：如果排队连接断开，已排程的事件仍可能被传递，导致接收端在连接断开后被调用。
当任一物体被摧毁时，信号槽连接会被移除。
注意：该功能会让`QObject::disconnect()`重载。

### `bool QObject::disconnect(const char *signal = nullptr, const QObject *receiver = nullptr, const char *method = nullptr) const`

**作用与语义：**

切断`signal`与`receiver` `method`连接。
注意：在`connect()`及相应的disconnect()调用中，使用相同的语法、指针到成员函数或基于字符串的函数，使用`SIGNAL`和`SLOT`宏。
为避免不匹配，存储`connect()`返回的连接句柄，并在调用 `disconnect()` 时使用它。
注意：如果排队连接断开，已排程的事件仍可能被传递，导致接收端在连接断开后被调用。
当任一物体被摧毁时，信号槽连接会被移除。
注意：断开所有信号槽连接也会断开`QObject::destroyed()`信号（如果已连接）。这样做可能会对依赖该信号清理资源的类产生不利影响。建议仅断开通过应用代码连接的特定信号。
注意：该功能会超载`QObject::disconnect()`。
注意：该功能是线程安全的。

### `[static] template <typename PointerToMemberFunction> bool QObject::disconnect(const QObject *sender, PointerToMemberFunction signal, const QObject *receiver, PointerToMemberFunction method)`

**作用与语义：**

将对象`sender`中的`signal`与对象`receiver`中的`method`断开连接。如果连接成功断开，返回`true`;否则返回`false`。
当任一物体被摧毁时，信号槽连接会被移除。
disconnect() 通常有三种用法，如下示例所示。
- 断开所有连接到物体信号的设备：
`QObject::disconnect`（myObject， nullptr， nullptr， nullptr）;
- 断开所有连接到特定信号的设备：
`QObject::disconnect`（myObject， &MyObject：：mySignal， nullptr， nullptr）;
- 断开特定接收机：
`QObject::disconnect`（myObject， nullptr， myReceiver， nullptr）;
- 断开一个特定信号到特定槽函数的连接：
`QObject::disconnect`（lineEdit， &`QLineEdit::textChanged`，。
标签，`QLabel::setText`）;
`nullptr`可用作万用牌，分别表示“任意信号”、“任何接收对象”或“接收对象中的任意槽函数”。
`sender`可能永远不会`nullptr`。（你不能在一次通话中断开多个物体的信号。）。
如果`signal` `nullptr`，则断开`receiver`和`method`任何信号。如果不，则仅断开指定的信号。
如果`receiver` `nullptr`，则断开所有连接到`signal`的设备。如果不，则仅断开指定接收器中的槽函数。非空`receiver`的 disconnect() 也会断开以 `receiver` 作为上下文对象连接的槽函数函数。
如果`method` `nullptr`，则断开所有与`receiver`连接的设备。如果不连接，只有名为`method`的槽会断开，其他所有槽函数保持原样。如果`receiver`被排除，`method`必须`nullptr`，因此你不能断开所有对象上特定命名的槽。
注意：无法利用该重载断开与函子或λ表达式相关的信号。这是因为无法比较它们。相反，使用需要一个`QMetaObject::Connection`的重载。
注意：除非`nullptr` `method`，否则该函数也不会断开使用基于字符串版本的`connect()`建立的连接。要断开此类连接，请使用相应的基于字符串的重载 disconnect()。
注意：该功能会超载`QObject::disconnect()`。
注意：该功能是线程安全的。

### `[virtual protected] void QObject::disconnectNotify(const QMetaMethod &signal)`

**作用与语义：**

当该对象中的某部分从`signal`断开时，调用了这个虚拟函数。
请参见`connectNotify()`，了解如何将`signal`与特定信号进行比较。
如果所有信号都与该对象断开连接（例如，`disconnect()`的信号参数被`nullptr`），disconnectNotify() 只调用一次，且该`signal`将是无效的`QMetaMethod`（`QMetaMethod::isValid()`返回 `false`）。
警告：该函数违反面向对象的模块化原则。不过，它可能有助于优化对昂贵资源的访问。
警告：该函数是从执行断开连接的线程调用的，该线程可能与该对象所在线程不同。该函数也可能被调用时内部`QObject`互斥体被锁定。因此，不允许重新输入任何`QObject`函数，包括`isSignalConnected()`，来自你的重实现版本。如果你在重实现中锁定了互斥体，务必确保不要调用`QObject`函数，否则会导致死锁。

### `void QObject::dumpObjectInfo() const`

**作用与语义：**

将该对象的信号连接等信息转储到调试输出。
注意：在Qt 5.9之前，这个函数不是const。

### `void QObject::dumpObjectTree() const`

**作用与语义：**

将子节点树转储到调试输出。
注意：在Qt 5.9之前，这个函数不是const。

### `QList<QByteArray> QObject::dynamicPropertyNames() const`

**作用与语义：**

返回所有用`setProperty()`动态添加到对象上的属性名称。

### `[virtual] bool QObject::event(QEvent *e)`

**作用与语义：**

该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回为真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

**官方示例：**

```cpp
 class MyClass : public QWidget
 {
     Q_OBJECT

 public:
     MyClass(QWidget *parent = nullptr);
     ~MyClass();

     bool event(QEvent* ev) override
     {
         if (ev->type() == QEvent::PolishRequest) {
             // overwrite handling of PolishRequest if any
             doThings();
             return true;
         } else  if (ev->type() == QEvent::Show) {
             // complement handling of Show if any
             doThings2();
             QWidget::event(ev);
             return true;
         }
         // Make sure the rest of events are handled
         return QWidget::event(ev);
     }
 };
```

### `[virtual] bool QObject::eventFilter(QObject *watched, QEvent *event)`

**作用与语义：**

如果该对象已作为`watched`对象的事件过滤器安装，则过滤事件。
在你对该函数的重新实现中，如果你想过滤掉`event`，即停止继续处理，返回 true;否则返回 false。
请注意，在上述示例中，未处理的事件会传递给基类的 eventFilter() 函数，因为基类可能为自身内部目的重新实现了 eventFilter()。
某些事件，如`QEvent::ShortcutOverride`，必须被明确接受（通过调用`accept()`来防止传播。
警告：如果你删除了该函数中的接收对象，请务必返回 true。否则，Qt 会将事件转发给已删除的对象，程序可能会崩溃。

**官方示例：**

```cpp
 class MainWindow : public QMainWindow
 {
 public:
     MainWindow();

 protected:
     bool eventFilter(QObject *obj, QEvent *ev) override;

 private:
     QTextEdit *textEdit;
 };

 MainWindow::MainWindow()
 {
     textEdit = new QTextEdit;
     setCentralWidget(textEdit);

     textEdit->installEventFilter(this);
 }

 bool MainWindow::eventFilter(QObject *obj, QEvent *event)
 {
     if (obj == textEdit) {
         if (event->type() == QEvent::KeyPress) {
             QKeyEvent *keyEvent = static_cast<QKeyEvent*>(event);
             qDebug() << "Ate key press" << keyEvent->key();
             return true;
         } else {
             return false;
         }
     } else {
         // pass the event on to the parent class
         return QMainWindow::eventFilter(obj, event);
     }
 }
```

### `template <typename T> T QObject::findChild(QAnyStringView name, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**作用与语义：**

返回该对象的子节点，可以转换为类型T，称为`name`，若不存在则称为`nullptr`。空`name`参数使所有对象匹配。空且非空`name`仅匹配`objectName`为空的对象。搜索以递归方式进行，除非`options`指定FindDirectChildrenOnly选项。
如果有多个子节点匹配搜索，则返回最直接祖先。如果有多个最直接祖先，则返回`children()`中的第一个子节点。在这种情况下，最好使用`findChildren()`获取所有子节点的完整列表。
这个例子返回了一个名为`"button1"`的子节点`QPushButton`，即使该按钮不是父按钮的直接子`parentWidget`：
此示例返回`parentWidget`的`QListWidget`子：
本例返回`parentWidget`（其直接父节点）的一个子节点`QPushButton`，名为`"button1"`：
本示例返回`parentWidget`的`QListWidget`子，的直接父：
注意：在6.7之前的Qt版本中，该函数将`name`视为`QString`，而非作为`QAnyStringView`。

**官方示例：**

```cpp
 QPushButton *button = parentWidget->findChild<QPushButton *>("button1");
```

### `[since 6.7] template <typename T> T QObject::findChild(Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**作用与语义：**

返回该对象的子节点，可以转换为类型 T，若无类型则转换为 `nullptr`。搜索是递归进行的，除非`options`指定 FindDirectChildrenOnly 选项。
如果有多个子节点匹配搜索，则返回最直接祖先。如果有多个最直接祖先，则返回`children()`中的第一个子节点。在这种情况下，最好使用`findChildren()`获取所有子节点的完整列表。

### `template <typename T> QList<T> QObject::findChildren(QAnyStringView name, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**作用与语义：**

返回该对象的所有子节点，并返回可转换为类型T的给定`name`，若无此类对象则返回空列表。空`name`参数使所有对象匹配，空参数仅匹配`objectName`为空的对象。搜索以递归方式进行，除非`options`指定FindDirectChildrenOnly选项。
以下示例展示了如何找到指定`parentWidget`的子`QWidget`列表，该`widgetname`：
本示例返回所有 `QPushButton`，这些 ZXQQ 是 `parentWidget` 的子节点：
本示例返回所有直接子 `parentWidget` 的 `QPushButton`：
注意：在6.7之前的Qt版本中，该函数将`name`视为`QString`，而非作为`QAnyStringView`。

**官方示例：**

```cpp
 QList<QWidget *> widgets = parentWidget->findChildren<QWidget *>("widgetname");
```

### `[since 6.3] template <typename T> QList<T> QObject::findChildren(Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**作用与语义：**

返回该对象的所有子节点，这些子节点可以被转换为类型 T，或者如果没有此类对象则返回空列表。除非`options`指定 FindDirectChildrenOnly 选项，否则搜索是递归进行的。

### `template <typename T> QList<T> QObject::findChildren(const QRegularExpression &re, Qt::FindChildOptions options = Qt::FindChildrenRecursively) const`

**作用与语义：**

返回该对象的子节点，这些子节点可以被转换为类型 T，且名称与正则表达式 `re` 一致;如果没有此类对象，则返回空列表。除非`options`指定 FindDirectChildrenOnly 选项，否则搜索是递归进行的。
注意：该功能会超载`QObject::findChildren()`。

### `bool QObject::inherits(const char *className) const`

**作用与语义：**

如果该对象是继承`className`的类实例或继承`className`的`QObject`子类，返回`true`;否则返回`false`。
类被视为继承自身。
如果你需要判断某个对象是否为某个特定类的实例来施放，可以考虑使用 `qobject_cast`<类型 *>（object）。

**官方示例：**

```cpp
 QTimer *timer = new QTimer;         // QTimer inherits QObject
 timer->inherits("QTimer");          // returns true
 timer->inherits("QObject");         // returns true
 timer->inherits("QAbstractButton"); // returns false

 // QVBoxLayout inherits QObject and QLayoutItem
 QVBoxLayout *layout = new QVBoxLayout;
 layout->inherits("QObject");        // returns true
 layout->inherits("QLayoutItem");    // returns true (even though QLayoutItem is not a QObject)
```

### `void QObject::installEventFilter(QObject *filterObj)`

**作用与语义：**

在此对象上安装事件过滤器`filterObj`。例如：
事件过滤器是一个接收所有发送到该对象事件的对象。过滤器可以停止事件或转发到该对象。事件过滤器`filterObj`通过其`eventFilter()`函数接收事件。如果事件需要被过滤，`eventFilter()`函数必须返回true（即停止）;否则必须返回false。
如果单个对象安装了多个事件过滤器，则最先激活最后安装的过滤器。
如果`filterObj`已经为该对象安装，这个功能会移动它，使其表现得就像是最后安装的一样。
这里有一个`KeyPressEater`类，它会吞噬其监控对象的按键操作：
以下是如何在两个小部件上安装它的方法：
例如，`QShortcut`类就利用这种技术拦截快捷键的按键。
警告：如果你在`eventFilter()`函数中删除接收对象，请务必返回true。如果你返回false，Qt会将事件发送给已删除的对象，程序将崩溃。
注意，过滤对象必须与该对象处于同一线程中。如果`filterObj`在不同线程中，该函数不做任何事。如果调用该函数后`filterObj`或该对象被移动到不同线程，事件过滤器不会调用，直到两个对象再次拥有相同的线程亲和力（事件未被移除）。

**官方示例：**

```cpp
 monitoredObj->installEventFilter(filterObj);
```

### `[noexcept, since 6.11] bool QObject::isQmlExposed() const`

**作用与语义：**

返回对象是由QML引擎创建，还是所有权通过`QJSEngine::setObjectOwnership()`明确设置。

### `[since 6.4] bool QObject::isQuickItemType() const`

**作用与语义：**

如果对象是`QQuickItem`，返回`true`;否则返回`false`。
调用该函数等同于调用`inherits("QQuickItem")`，只是速度更快。

### `[protected] bool QObject::isSignalConnected(const QMetaMethod &signal) const`

**作用与语义：**

如果`signal`至少连接到一个接收器，返回`true`，否则返回`false`。
`signal`必须是该对象的信号成员，否则行为未定义。
正如上面代码片段所示，你可以利用这个函数避免昂贵的操作或发出没人注意的信号。
警告：在多线程应用中，连续调用该函数并不保证得到相同的结果。
警告：该函数违反面向对象模块化原则。特别地，该函数不得通过覆盖`connectNotify()`或`disconnectNotify()`调用，因为这些都可能被任何线程调用。

**官方示例：**

```cpp
     static const QMetaMethod valueChangedSignal = QMetaMethod::fromSignal(&MyObject::valueChanged);
     if (QObject::isSignalConnected(valueChangedSignal)) {
         QByteArray data;
         data = get_the_value();       // expensive operation
         emit valueChanged(data);
     }
```

### `bool QObject::isWidgetType() const`

**作用与语义：**

如果对象是小部件，返回`true`;否则返回`false`。
调用该函数等同于调用`inherits("QWidget")`，但速度更快。

### `bool QObject::isWindowType() const`

**作用与语义：**

如果对象是窗口，返回`true`;否则返回`false`。
调用该函数等同于调用`inherits("QWindow")`，只是速度更快。

### `void QObject::killTimer(int id)`

**作用与语义：**

用计时器标识符终止计时器，`id`。
计时器标识符在计时器事件启动时由`startTimer()`返回。

### `[since 6.8] void QObject::killTimer(Qt::TimerId id)`

**作用与语义：**

用计时器标识符终止计时器，`id`。
计时器标识符在计时器事件启动时由`startTimer()`返回。

### `[virtual] const QMetaObject *QObject::metaObject() const`

**作用与语义：**

返回指向该对象元对象的指针。
元对象包含继承`QObject`类的信息，例如类名、上类名、属性、信号和槽位。每个包含`Q_OBJECT`宏的`QObject`子类都会有一个元对象。
元对象信息由信号/槽连接机制和属性系统要求。`inherits()`函数也利用元对象。
如果你没有指向实际对象实例的指针，但仍想访问类的元对象，你可以用`staticMetaObject`。

**官方示例：**

```cpp
 QObject *obj = new QPushButton;
 obj->metaObject()->className();             // returns "QPushButton"

 QPushButton::staticMetaObject.className();  // returns "QPushButton"
```

### `bool QObject::moveToThread(QThread *targetThread)`

**作用与语义：**

改变该对象及其子节点的线程亲和性，成功时返回`true`。如果对象有父对象，则无法移动。事件处理将在`targetThread`中继续。
要将对象移动到主线程，使用`QApplication::instance()`获取当前应用程序的指针，然后用`QApplication::thread()`获取应用所在的线程。例如：
如果`targetThread` `nullptr`，该对象及其子节点的所有事件处理将停止，因为它们不再关联任何线程。
注意，该对象的所有活跃定时器都会被重置。计时器首先在当前线程中停止，并在`targetThread`中以相同间隔重新启动。因此，不断移动对象在线程之间可能会无限期推迟计时器事件。
在线程亲和性改变之前，会发送一个`QEvent::ThreadChange`事件到该对象。你可以处理该事件来执行任何特殊处理。注意，任何发布到该对象的新事件都会在`targetThread`中处理，前提是该事件不`nullptr`：当事件被`nullptr`时，该对象及其子节点将无法处理事件，因为它们不再关联任何线程。
警告：该函数不支持线程安全;当前线程必须与当前线程亲和力相同。换句话说，该函数只能将对象从当前线程“推送”到另一个线程，不能将任意线程中的对象“拉取”到当前线程。不过，这一规则有一个例外：没有线程亲和力的对象可以被“拉取”到当前线程。
在 6.7 之前的 Qt 版本中，该函数没有返回值（`void`）。

**官方示例：**

```cpp
 myObject->moveToThread(QApplication::instance()->thread());
```

### `[private signal] void QObject::objectNameChanged(const QString &objectName)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含该对象的名称。
你可以用`findChild()`来按名称（和类型）找到对象。你可以用`findChildren()`找到一组对象。
默认情况下，该属性包含空字符串。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `objectName` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 qDebug("MyClass::setPrecision(): (%s) invalid precision %f",
        qPrintable(objectName()), newPrecision);
```

### `QObject *QObject::parent() const`

**作用与语义：**

返回指向父对象的指针。

### `QVariant QObject::property(const char *name) const`

**作用与语义：**

返回对象`name`属性的值。
如果不存在这样的属性，返回的变体无效。
所有可用房产的信息均通过`metaObject()`和`dynamicPropertyNames()`提供。

### `[protected] int QObject::receivers(const char *signal) const`

**作用与语义：**

返回连接到`signal`的接收机数量。
由于槽函数和信号都可以作为信号接收器，且相同的连接可以多次进行，因此接收机的数量与该信号连接的数量相同。
调用该函数时，您可以使用`SIGNAL()`宏传递特定信号：
正如上面代码片段所示，你可以利用这个函数避免昂贵的操作或发出没人注意的信号。
警告：在多线程应用中，连续调用该函数并不保证得到相同的结果。
警告：该函数违反面向对象模块化原则。特别地，该函数不得通过覆盖`connectNotify()`或`disconnectNotify()`调用，因为这些功能可能被任何线程调用。

**官方示例：**

```cpp
 if (receivers(SIGNAL(valueChanged(QByteArray))) > 0) {
     QByteArray data;
     get_the_value(&data);       // expensive operation
     emit valueChanged(data);
 }
```

### `void QObject::removeEventFilter(QObject *obj)`

**作用与语义：**

从该对象中移除`obj`事件过滤器对象。如果未安装此类事件过滤器，请求将被忽略。
当该对象被销毁时，所有针对该对象的事件过滤器都会自动移除。
即使在事件过滤器激活期间（即从`eventFilter()`函数中移除事件过滤器）总是安全的。

### `[protected] QObject *QObject::sender() const`

**作用与语义：**

如果在被信号激活的槽中调用，则返回发送信号对象的指针;否则返回`nullptr`。该指针仅在执行该对象线程上下文中调用该函数的槽位时有效。
如果发送端被销毁，或该槽函数与发送方信号断开，该函数返回的指针将失效。
警告：该功能违反面向对象模块化原则。然而，当多个信号连接到单一槽函数时，访问发送端可能有用。
警告：如上所述，当`Qt::DirectConnection`通过与该对象线程不同的线程调用该槽位时，该函数的返回值不有效。请勿在此类场景中使用该函数。

### `[protected] int QObject::senderSignalIndex() const`

**作用与语义：**

返回调用当前执行槽函数的信号的元方法索引，该槽函数属于`sender()`返回的类。如果被信号激活的槽函数外调用，返回-1。
对于带有默认参数的信号，该函数总是返回包含所有参数的索引，无论`connect()`中使用了哪个参数。例如，信号`destroyed(QObject *obj = \nullptr)`会有两个不同的索引（带参数和不带参数），但该函数总是返回带参数的索引。当信号带不同参数时，这种情况不适用。
警告：该功能违反面向对象的模块化原则。然而，当多个信号连接到单一槽函数时，访问信号索引可能非常有用。
警告：当该槽位通过与该对象线程不同的线程调用`Qt::DirectConnection`时，该函数的返回值无效。请勿在此场景中使用该函数。

### `void QObject::setObjectName(const QString &name)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含该对象的名称。
你可以用`findChild()`来按名称（和类型）找到对象。你可以用`findChildren()`找到一组对象。
默认情况下，该属性包含空字符串。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `setObjectName(...)` 修改 `objectName`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 qDebug("MyClass::setPrecision(): (%s) invalid precision %f",
        qPrintable(objectName()), newPrecision);
```

### `[since 6.4] void QObject::setObjectName(QAnyStringView name)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含该对象的名称。
你可以用`findChild()`来按名称（和类型）找到对象。你可以用`findChildren()`找到一组对象。
默认情况下，该属性包含空字符串。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `setObjectName(...)` 修改 `objectName`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 qDebug("MyClass::setPrecision(): (%s) invalid precision %f",
        qPrintable(objectName()), newPrecision);
```

### `void QObject::setParent(QObject *parent)`

**作用与语义：**

使该物体成为`parent`子。

### `bool QObject::setProperty(const char *name, const QVariant &value)`

**作用与语义：**

将对象`name`属性的值设置为`value`。
如果该属性在类中用 `Q_PROPERTY` 定义，则成功时返回 true，否则返回 false。如果该属性未用 `Q_PROPERTY` 定义，因此未列入元对象，则作为动态属性添加，false 返回。
所有可用房产的信息均通过`metaObject()`和`dynamicPropertyNames()`提供。
动态属性可以通过`property()`再次查询，并通过将属性值设置为无效`QVariant`来移除。更改动态属性的值会向对象发送`QDynamicPropertyChangeEvent`。
注意：以“_q_”开头的动态属性保留用于内部用途。

### `[since 6.6] bool QObject::setProperty(const char *name, QVariant &&value)`

**作用与语义：**

注意：该功能会超载`QObject::setProperty`。

### `[noexcept] bool QObject::signalsBlocked() const`

**作用与语义：**

如果信号被阻塞，返回`true`;否则返回`false`。
信号默认不会被阻挡。

### `int QObject::startTimer(int interval, Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

这是一个超载函数，会启动类型为`timerType`的定时器，超时为`interval`毫秒。这等同于调用：
从Qt 6.10开始，设置负值间隔会触发运行时警告，值会重置为1毫秒。Qt 6.10之前，Qt Timer允许你设置负值间隔，但表现令人意外（例如如果计时器运行时停止，或者根本不启动）。

**官方示例：**

```cpp
 startTimer(std::chrono::milliseconds{interval}, timerType);
```

### `int QObject::startTimer(std::chrono::nanoseconds interval, Qt::TimerType timerType = Qt::CoarseTimer)`

**作用与语义：**

启动一个计时器并返回计时器标识符，如果无法启动计时器则返回零。
计时器事件将每 `interval` 发生一次，直到调用 `killTimer()`。如果 `interval` 等于 `std::chrono::duration::zero()`，则计时器事件在每次控制返回事件循环时发生一次，即当没有本地窗口系统事件可处理时。
从 Qt 6.10 开始，设置负间隔将导致运行时警告，并将值重置为 1 毫秒。在 Qt 6.10 之前，Qt 计时器允许设置负间隔，但行为可能令人意外（例如，如果计时器正在运行则停止计时器，或者根本不启动计时器）。
当计时器事件发生时，虚函数 `timerEvent()` 使用 `QTimerEvent` 事件参数类被调用。重新实现此函数以获取计时器事件。
如果有多个计时器在运行，可以使用 `QTimerEvent::id()` 方法来确定哪个计时器被激活。
请注意，计时器的精度取决于底层操作系统和硬件。
`timerType` 参数允许自定义计时器的精度。有关不同计时器类型的信息，请参见 `Qt::TimerType`。大多数平台支持 20 毫秒的精度；有些平台提供更高精度。如果 Qt 无法提供请求数量的计时器事件，它将默默丢弃一些事件。
`QTimer` 和 `QChronoTimer` 类提供高级编程接口，可以使用单触发计时器和计时器信号而不是事件。此外，还有一个 `QBasicTimer` 类，比 `QChronoTimer` 更轻量，但比直接使用计时器 ID 不那么笨重。
注意：从 Qt 6.8 开始，`interval` 的类型为 `std::chrono::nanoseconds`，在此之前为 `std::chrono::milliseconds`。此更改与旧版 Qt 向后兼容。
注意：在 Qt 6.8 中，`QObject` 已更改为使用 `Qt::TimerId` 来表示计时器 ID。此方法将 `TimerId` 转换为 int 以实现向后兼容，但您可以使用 `Qt::TimerId` 检查此方法返回的值，例如：

**官方示例：**

```cpp
 class MyObject : public QObject
 {
     Q_OBJECT

 public:
     MyObject(QObject *parent = nullptr);

 Q_SIGNALS:
     void valueChanged();

 protected:
     void timerEvent(QTimerEvent *event) override;
 };

 MyObject::MyObject(QObject *parent)
     : QObject(parent)
 {
     using namespace std::chrono_literals;

     startTimer(50ms);
     startTimer(5s);
     startTimer(10min);
     startTimer(1h);
 }

 void MyObject::timerEvent(QTimerEvent *event)
 {
     qDebug() << "Timer ID:" << event->id();
 }
```

### `QThread *QObject::thread() const`

**作用与语义：**

返回该对象所在的线程。

### `[virtual protected] void QObject::timerEvent(QTimerEvent *event)`

**作用与语义：**

该事件处理程序可以被重新实现到子类中，以接收该对象的定时器事件。
`QChronoTimer` 提供了定时器功能的更高级接口，以及关于定时器的更通用信息。定时器事件通过 `event` 参数传递。

### `[static] QString QObject::tr(const char *sourceText, const char *disambiguation = nullptr, int n = -1)`

**作用与语义：**

返回 `sourceText` 的翻译版本，包含复数的字符串可选择基于 `disambiguation` 字符串和 `n` 值;否则如果没有合适的翻译字符串，返回 `QString::fromUtf8`（`sourceText`）。
如果同一上下文中同一`sourceText`在不同角色中使用，可能会在`disambiguation`中传递额外的识别字符串（默认`nullptr`）。
关于 Qt 翻译机制的详细描述，请参见“编写翻译源代码”，以及“消歧义相同文本”部分，了解消歧义信息。
警告：只有在调用此方法前安装所有翻译器时，此方法才会重录。不支持在执行翻译时安装或移除翻译器。这样做可能导致崩溃或其他不良行为。

**官方示例：**

```cpp
 void SpreadSheet::setupMenuBar()
 {
     QMenu *fileMenu = menuBar()->addMenu(tr("&File"));
     ...
```

### `const QMetaObject QObject::staticMetaObject`

**作用与语义：**

该变量存储类的元对象。
元对象包含继承`QObject`类的信息，例如类名、超类名、属性、信号和槽。每个包含`Q_OBJECT`宏的类也会有一个元对象。
元对象信息由信号/槽连接机制和属性系统要求。`inherits()`函数也利用元对象。
如果你有一个指向某个对象的指针，可以用`metaObject()`获取与该对象关联的元对象。

**官方示例：**

```cpp
 QPushButton::staticMetaObject.className();  // returns "QPushButton"

 QObject *obj = new QPushButton;
 obj->metaObject()->className();             // returns "QPushButton"
```

### `QObjectList`

**作用与语义：**

`QList`<`QObject`的同义词是*>。

### `[since 6.8] enum class TimerId`

**作用与语义：**

它用于表示计时器ID（例如`QTimer`和 `QChronoTimer`）。底层类型是`int`。你可以用`qToUnderlying()`将Qt：：TimerId转换为`int`。
- `QObject::TimerId::Invalid`：`0`;表示无操作计时器ID;其使用方式取决于上下文，例如，这是`QObject::startTimer()`返回的值，表示未启动计时器;而`QChronoTimer::id()`在计时器非激活时返回该值，即`timer.isActive()`返回`false`。
这个枚举是在Qt 6.8引入的。

### `template <typename T> T qobject_cast(const QObject *object)`

**作用与语义：**

如果对象属于类型T（或子类），则返回给定的`object`，投射为类型T;否则返回`nullptr`。如果`object`被`nullptr`，则返回`nullptr`。
类 T 必须直接或间接继承 `QObject`，并用 `Q_OBJECT` 宏声明。
类被视为继承自身。
`qobject_cast()`函数的行为类似于标准的C `dynamic_cast()`，优点是不需要RTTI支持，并且可以跨动态库边界工作。
`qobject_cast()`也可以与接口结合使用。
警告：如果 T 未用 `Q_OBJECT` 宏声明，该函数的返回值未定义。

**官方示例：**

```cpp
 QObject *obj = new QTimer;          // QTimer inherits QObject

 QTimer *timer = qobject_cast<QTimer *>(obj);
 // timer == (QObject *)obj

 QAbstractButton *button = qobject_cast<QAbstractButton *>(obj);
 // button == nullptr
```

### `[since 6.7] QT_NO_CONTEXTLESS_CONNECT`

**作用与语义：**

定义该宏将使信号与函子连接的重载`QObject::connect()`失效，同时不指定接收/上下文对象的`QObject`（即`QObject::connect()`的三参数超载）。
使用无上下文重载容易出错，因为它很容易连接到依赖接收端某个局部状态的函子。如果该局部状态被破坏，连接不会自动断开。
此外，这类连接总是直接连接，在多线程场景中可能会引发问题（例如信号来自另一线程）。
该宏在Qt 6.7引入。

### `QT_NO_NARROWING_CONVERSIONS_IN_CONNECT`

**作用与语义：**

定义该宏将禁用信号携带参数与槽接受参数之间的窄角和浮点积分转换，当信号和槽函数使用 PMF 语法连接时。

### `Q_CLASSINFO(Name, Value)`

**作用与语义：**

该宏将额外信息关联到类，该信息通过`QObject::metaObject()`获取。额外信息以`Name`字符串和`Value`字面字符串的形式出现。
Qt 在 Qt D-Bus 和 Qt Qml 模块中使用宏。例如，在 C 语言中定义 QML 对象类型时，可以指定一个属性为默认属性：

**官方示例：**

```cpp
 class MyClass : public QObject
 {
     Q_OBJECT
     Q_CLASSINFO("Author", "Pierre Gendron")
     Q_CLASSINFO("URL", "http://www.my-organization.qc.ca")

 public:
     //...
 };
```

### `Q_EMIT`

**作用与语义：**

当你想用第三方信号/槽机制使用Qt Signals and Slots时，可以用这个宏替换`emit`关键词来发射信号。
当`no_keywords`在`.pro`文件中用`CONFIG`变量指定时，通常使用宏，但即使未指定`no_keywords`也可以使用。

### `Q_ENUM(...)`

**作用与语义：**

该宏向元对象系统注册一个枚举类型。它必须置于枚举声明之后，且类中有 `Q_OBJECT`、`Q_GADGET` 或 `Q_GADGET_EXPORT` 宏。命名空间则使用 `Q_ENUM_NS()`。
用Q_ENUM申报的枚举会在附信`QMetaObject`中登记其`QMetaEnum`。你也可以用`QMetaEnum::fromType()`获取`QMetaEnum`。
注册枚举也会自动注册到Qt元类型系统，使`QMetaType`无需使用`Q_DECLARE_METATYPE()`即可知晓。这将启用有用的功能;例如，如果在`QVariant`中使用，你可以将其转换为字符串。同样，传递给`QDebug`会打印出它们的名称。

**官方示例：**

```cpp
 class MyClass : public QObject
 {
     Q_OBJECT

 public:
     MyClass(QObject *parent = nullptr);
     ~MyClass();

     enum Priority { High, Low, VeryHigh, VeryLow };
     Q_ENUM(Priority)
     void setPriority(Priority priority);
     Priority priority() const;
 };
```

### `Q_ENUM_NS(...)`

**作用与语义：**

该宏在元对象系统中注册一个枚举类型。它必须置于枚举声明之后，且命名空间中包含`Q_NAMESPACE`宏。它与`Q_ENUM`相同，但位于命名空间中。
用Q_ENUM_NS申报的枚举记录`QMetaEnum`会在附带的`QMetaObject`中登记。你也可以用`QMetaEnum::fromType()`获取`QMetaEnum`。
注册枚举也会自动注册到Qt元类型系统，使`QMetaType`无需使用`Q_DECLARE_METATYPE()`即可被知晓。这将启用有用的功能;例如，如果在`QVariant`中使用，你可以将其转换为字符串。同样，传递给`QDebug`会打印出它们的名称。

### `Q_FLAG(...)`

**作用与语义：**

该宏在元对象系统中注册单一标志类型。通常用于类定义中声明给定枚举的值可以作为标志使用，并通过按位 OR 运算符组合。命名空间则使用 `Q_FLAG_NS()`。
宏必须置于枚举声明之后。标志类型的声明使用`Q_DECLARE_FLAGS()`宏完成。
例如，在`QItemSelectionModel`中，`SelectionFlags`旗的宣告方式如下：
注意：Q_FLAG宏负责在元对象系统中注册单个标志值，因此无需额外使用`Q_ENUM()`。

**官方示例：**

```cpp
 class Q_CORE_EXPORT QItemSelectionModel : public QObject
 {
     Q_OBJECT
     ...
 public:

     enum SelectionFlag {
         NoUpdate       = 0x0000,
         Clear          = 0x0001,
         Select         = 0x0002,
         Deselect       = 0x0004,
         Toggle         = 0x0008,
         Current        = 0x0010,
         Rows           = 0x0020,
         Columns        = 0x0040,
         SelectCurrent  = Select | Current,
         ToggleCurrent  = Toggle | Current,
         ClearAndSelect = Clear | Select
     };

     Q_DECLARE_FLAGS(SelectionFlags, SelectionFlag)
     Q_FLAG(SelectionFlags)

 };
```

### `Q_FLAG_NS(...)`

**作用与语义：**

该宏在元对象系统中注册一个标志类型。它用于拥有`Q_NAMESPACE`宏的命名空间，声明给定枚举的值可以作为标志使用，并通过按位的 OR 运算符组合。它与 `Q_FLAG` 相同，但属于命名空间。
宏必须放在枚举声明之后。
注意：Q_FLAG_NS宏负责在元对象系统中注册单个标志值，因此无需额外使用`Q_ENUM_NS()`。

### `Q_GADGET`

**作用与语义：**

Q_GADGET宏是`Q_OBJECT`宏的轻量版，适用于那些不继承`QObject`但仍希望使用`QMetaObject`部分反射功能的类。
注意：本宏扩展以`private`：访问指定符结束。如果你在该宏之后立即声明成员，这些成员也将是私有的。要在宏后立即添加公共（或受保护）成员，请使用`public:`（或`protected:`）访问指定符。
Q_GADGETs可以有`Q_ENUM`信号、信号`Q_PROPERTY`和`Q_INVOKABLE`，但不能有信号或槽函数。
Q_GADGET使类成员`staticMetaObject`可用。`staticMetaObject`属于类型`QMetaObject`，提供访问`Q_ENUM`声明的枚举。

### `[since 6.3] Q_GADGET_EXPORT(EXPORT_MACRO)`

**作用与语义：**

Q_GADGET_EXPORT宏的工作原理与`Q_GADGET`宏完全相同。然而，提供的`staticMetaObject`变量（见 `Q_GADGET`）声明时会用提供的 `EXPORT_MACRO` 限定符。这在需要从动态库导出对象但整个包含类不应该导出时非常有用（例如因为它主要由内联函数组成）。
注意：本宏扩展以`private`：访问指定符结束。如果你在该宏之后立即声明成员，这些成员也将是私有的。要在宏之后添加公共（或受保护）成员，请使用`public:`（或`protected:`）访问指定符。
该宏是在第6.3期引入的。

**官方示例：**

```cpp
 class Point {
     Q_GADGET_EXPORT(EXPORT_MACRO)
     Q_PROPERTY(int x MEMBER x)
     Q_PROPERTY(int y MEMBER y)
     ~~~
```

### `Q_INTERFACES(...)`

**作用与语义：**

该宏告诉 Qt 类实现了哪些接口。这用于实现插件。

### `Q_INVOKABLE`

**作用与语义：**

将该宏应用于成员函数的声明，以便通过元对象系统调用它们。宏写入返回类型之前，如下示例所示：
`invokableMethod()`函数通过Q_INVOKABLE标记，使其在元对象系统中注册，并允许使用`QMetaObject::invokeMethod()`调用。由于`normalMethod()`函数未以这种方式注册，无法通过`QMetaObject::invokeMethod()`调用。
如果可调用成员函数返回指向`QObject`的`QObject`或子类的指针，且该指针是从 QML 调用的，则适用特殊的所有权规则。更多信息请参见 QML 与 C 之间的数据类型转换。

**官方示例：**

```cpp
 class Window : public QWidget
 {
     Q_OBJECT

 public:
     Window();
     void normalMethod();
     Q_INVOKABLE void invokableMethod();
 };
```

### `[since 6.0] Q_MOC_INCLUDE`

**作用与语义：**

Q_MOC_INCLUDE宏可以在类内或类外使用，并告诉元对象编译器添加包含。
如果你用作属性或信号/槽参数的类型是前向声明的，这很有用。
该宏在Qt 6.0中引入。

**官方示例：**

```cpp
 // Put this in your code and the generated code will include this header.
 Q_MOC_INCLUDE("myheader.h")
```

### `Q_NAMESPACE`

**作用与语义：**

Q_NAMESPACE宏可用于为命名空间添加`QMetaObject`能力。
Q_NAMESPACEs可以有`Q_CLASSINFO`、`Q_ENUM_NS`、`Q_FLAG_NS`，但不能有`Q_ENUM`、`Q_FLAG`、`Q_PROPERTY`、`Q_INVOKABLE`、信号或槽函数。
Q_NAMESPACE 使外部变量 `staticMetaObject` 可用。`staticMetaObject` 类型为 `QMetaObject`，提供访问以 `Q_ENUM_NS`/`Q_FLAG_NS` 声明的枚举。

**官方示例：**

```cpp
 namespace test {
 Q_NAMESPACE
 ...
```

### `Q_NAMESPACE_EXPORT(EXPORT_MACRO)`

**作用与语义：**

Q_NAMESPACE_EXPORT宏可用于为命名空间添加`QMetaObject`功能。
它的工作原理和 `Q_NAMESPACE` 宏完全一样。不过，命名空间中定义的外部 `staticMetaObject` 变量会用提供的 `EXPORT_MACRO` 限定符声明。如果需要从动态库导出对象，这非常有用。

**官方示例：**

```cpp
 namespace test {
 Q_NAMESPACE_EXPORT(EXPORT_MACRO)
 ...
```

### `Q_OBJECT`

**作用与语义：**

Q_OBJECT宏用于启用元对象特征，如动态属性、信号和槽。
你可以将Q_OBJECT宏添加到类定义中任何声明自身信号和槽位，或使用 Qt 元对象系统其他服务的部分。
注意：本宏扩展以`private`：访问指定符结束。如果你在该宏之后立即声明成员，这些成员也将是私有的。要在宏之后立即添加公共（或受保护）成员，请使用`public:`（或`protected:`）访问指定符。
注意：该宏要求类必须是`QObject`的子类。使用`Q_GADGET`或`Q_GADGET_EXPORT`代替Q_OBJECT以启用元对象系统对非`QObject`子类的枚举支持。

**官方示例：**

```cpp
 #include <QObject>

 class Counter : public QObject
 {
     Q_OBJECT

 // Note. The Q_OBJECT macro starts a private section.
 // To declare public members, use the 'public:' access modifier.
 public:
     Counter() { m_value = 0; }

     int value() const { return m_value; }

 public slots:
     void setValue(int value);

 signals:
     void valueChanged(int newValue);

 private:
     int m_value;
 };
```

### `Q_PROPERTY(...)`

**作用与语义：**

该宏用于在继承`QObject`类中声明属性。属性的行为类似于类数据成员，但它们通过元对象系统具有额外功能。
属性名称、类型以及`READ`函数是必需的。类型可以是`QVariant`支持的任何类型，也可以是用户自定义类型。其他项是可选的，但`WRITE`函数是常见的。属性默认为true，唯独`USER`默认为false。
关于如何使用该宏的更多细节及更详细的示例，请参见关于Qt属性系统的讨论。

**官方示例：**

```cpp
 Q_PROPERTY(type name
            (READ getFunction [WRITE setFunction] |
             MEMBER memberName [(READ getFunction | WRITE setFunction)])
            [RESET resetFunction]
            [NOTIFY notifySignal]
            [REVISION int | REVISION(int[, int])]
            [DESIGNABLE bool]
            [SCRIPTABLE bool]
            [STORED bool]
            [USER bool]
            [BINDABLE bindableProperty]
            [CONSTANT]
            [FINAL]
            [VIRTUAL]
            [OVERRIDE]
            [REQUIRED])
```

### `Q_REVISION`

**作用与语义：**

将该宏应用于成员函数的声明，并在元对象系统中为其标记修订号。宏写入返回类型之前，如下示例所示：
这在使用元对象系统动态暴露对象到另一个 API 时非常有用，因为你可以匹配多个版本对该 API 的预期版本。请考虑以下简化示例：
使用与前述相同的 Window 类，newProperty 和 newMethod 仅在预期版本达到 `2.1` 或更高时才会暴露。
由于所有方法若未被标记，都被视为修订`0`，`Q_REVISION(0)`或`Q_REVISION(0, 0)`标签无效且被忽略。
你可以传递一个或两个整数参数给`Q_REVISION`。如果你传递一个参数，它只表示次要版本。这意味着主要版本未被指定。如果你传递两个，第一个参数是主要版本，第二个参数是次要版本。
该标签不被元对象系统本身使用。目前仅由`QtQml`模块使用。
关于更通用的字符串标签，请参见`QMetaMethod::tag()`。

**官方示例：**

```cpp
 class Window : public QWidget
 {
     Q_OBJECT
     Q_PROPERTY(int normalProperty READ normalProperty)
     Q_PROPERTY(int newProperty READ newProperty REVISION(2, 1))

 public:
     Window();
     int normalProperty();
     int newProperty();
 public slots:
     void normalMethod();
     Q_REVISION(2, 1) void newMethod();
 };
```

### `Q_SET_OBJECT_NAME(Object)`

**作用与语义：**

该宏将`Object` `objectName`分配为“对象”。
无论`Object`是否是指针，宏自己都会判断。

### `Q_SIGNAL`

**作用与语义：**

这是一个额外的宏，可以让你将单个函数标记为信号。它非常有用，尤其是当你使用第三方源代码解析器，无法理解`signals`或`Q_SIGNALS`组时。
当你想用第三方信号/槽机制使用 Qt 信号和槽时，可以用这个宏替换类声明中的 `signals` 关键字。
当 `.pro` 文件中 `CONFIG` 变量指定 `no_keywords` 时，宏通常被使用，但即使未指定 `no_keywords` 也可以使用。

### `Q_SIGNALS`

**作用与语义：**

当你想用第三方信号/槽机制使用 Qt 信号和槽函数时，可以用这个宏替换类声明中的 `signals` 关键字。
宏通常用于`.pro`文件中`CONFIG`变量指定`no_keywords`，但即使未指定`no_keywords`也可以使用。

### `Q_SLOT`

**作用与语义：**

这是一个额外的宏，可以让你将单个函数标记为槽函数。它非常有用，尤其是当你使用第三方源代码解析器，因为它不理解`slots`或`Q_SLOTS`组时。
当你想用第三方信号/槽机制使用 Qt 信号和槽函数时，可以用这个宏替换类声明中的 `slots` 关键字。
当`no_keywords`在`.pro`文件中指定`CONFIG`变量时，宏通常被使用，但即使未指定`no_keywords`也可以使用。

### `Q_SLOTS`

**作用与语义：**

当你想用第三方信号/槽函数机制使用 Qt 信号和槽函数时，可以用这个宏替换类声明中的 `slots` 关键字。
当`.pro`文件中`CONFIG`变量指定`no_keywords`时，宏通常使用，但即使未指定`no_keywords`也可以使用。

### `QBindable<QString> bindableObjectName()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含该对象的名称。
你可以用`findChild()`来按名称（和类型）找到对象。你可以用`findChildren()`找到一组对象。
默认情况下，该属性包含空字符串。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `bindableObjectName()` 取得 `objectName` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

**官方示例：**

```cpp
 qDebug("MyClass::setPrecision(): (%s) invalid precision %f",
        qPrintable(objectName()), newPrecision);
```

### `QString objectName() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含该对象的名称。
你可以用`findChild()`来按名称（和类型）找到对象。你可以用`findChildren()`找到一组对象。
默认情况下，该属性包含空字符串。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `objectName()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 qDebug("MyClass::setPrecision(): (%s) invalid precision %f",
        qPrintable(objectName()), newPrecision);
```

### `T qobject_cast(QObject *object)`

**作用与语义：**

如果对象属于类型T（或子类），则返回给定的`object`，投射为类型T;否则返回`nullptr`。如果`object`被`nullptr`，则返回`nullptr`。
类 T 必须直接或间接继承 `QObject`，并用 `Q_OBJECT` 宏声明。
类被视为继承自身。
`qobject_cast()`函数的行为类似于标准的C `dynamic_cast()`，优点是不需要RTTI支持，并且可以跨动态库边界工作。
`qobject_cast()`也可以与接口结合使用。
警告：如果 T 未用 `Q_OBJECT` 宏声明，该函数的返回值未定义。

**官方示例：**

```cpp
 QObject *obj = new QTimer;          // QTimer inherits QObject

 QTimer *timer = qobject_cast<QTimer *>(obj);
 // timer == (QObject *)obj

 QAbstractButton *button = qobject_cast<QAbstractButton *>(obj);
 // button == nullptr
```

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
