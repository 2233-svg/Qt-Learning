# QIcon

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 多状态图标资源，负责按模式、状态和尺寸提供合适的 pixmap。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QIcon`：多状态图标资源，负责按模式、状态和尺寸提供合适的 pixmap。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QIcon>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    // 设置画笔、画刷、字体或变换后进行绘制
    painter.restore();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Mode { Normal, Disabled, Active, Selected }`
- `enum State { On, Off }`
- `(since 6.7) enum class ThemeIcon { AddressBookNew, ApplicationExit, AppointmentNew, CallStart, CallStop, …, WeatherStorm }`

### 公有函数

- `QIcon()`
- `QIcon(QIconEngine *engine)`
- `QIcon(const QPixmap &pixmap)`
- `QIcon(const QString &fileName)`
- `QIcon(const QIcon &other)`
- `QIcon(QIcon &&other)`
- `~QIcon()`
- `QSize actualSize(const QSize &size, QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `void addFile(const QString &fileName, const QSize &size = QSize(), QIcon::Mode mode = Normal, QIcon::State state = Off)`
- `void addPixmap(const QPixmap &pixmap, QIcon::Mode mode = Normal, QIcon::State state = Off)`
- `QList<QSize> availableSizes(QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `qint64 cacheKey() const`
- `bool isMask() const`
- `bool isNull() const`
- `QString name() const`
- `void paint(QPainter *painter, const QRect &rect, Qt::Alignment alignment = Qt::AlignCenter, QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `void paint(QPainter *painter, int x, int y, int w, int h, Qt::Alignment alignment = Qt::AlignCenter, QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `QPixmap pixmap(const QSize &size, QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `QPixmap pixmap(int extent, QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `(since 6.0) QPixmap pixmap(const QSize &size, qreal devicePixelRatio, QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `QPixmap pixmap(int w, int h, QIcon::Mode mode = Normal, QIcon::State state = Off) const`
- `void setIsMask(bool isMask)`
- `void swap(QIcon &other)`
- `operator QVariant() const`
- `QIcon & operator=(QIcon &&other)`
- `QIcon & operator=(const QIcon &other)`

### 静态公有成员

- `QStringList fallbackSearchPaths()`
- `QString fallbackThemeName()`
- `QIcon fromTheme(const QString &name)`
- `(since 6.7) QIcon fromTheme(QIcon::ThemeIcon icon)`
- `(since 6.7) QIcon fromTheme(QIcon::ThemeIcon icon, const QIcon &fallback)`
- `QIcon fromTheme(const QString &name, const QIcon &fallback)`
- `bool hasThemeIcon(const QString &name)`
- `(since 6.7) bool hasThemeIcon(QIcon::ThemeIcon icon)`
- `void setFallbackSearchPaths(const QStringList &paths)`
- `void setFallbackThemeName(const QString &name)`
- `void setThemeName(const QString &name)`
- `void setThemeSearchPaths(const QStringList &paths)`
- `QString themeName()`
- `QStringList themeSearchPaths()`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &stream, const QIcon &icon)`
- `QDataStream & operator>>(QDataStream &stream, QIcon &icon)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QIcon::Mode`

**作用与语义：**

该枚举类型描述了像素映射所期望使用的模式。目前定义的模式包括：
- `QIcon::Normal`：`0`;当用户未与图标交互，但图标所代表的功能可用时，显示像素地图。
- `QIcon::Disabled`：`1`;当图标表示的功能不可用时，显示像素地图。
- `QIcon::Active`：`2`;当图标所代表的功能可用且用户与图标互动时，显示像素地图，例如将鼠标移动到图标上或点击。
- `QIcon::Selected`：`3`;当图标所代表的物品被选中时，显示像素映射。

### `enum QIcon::State`

**作用与语义：**

该枚举描述了像素映射所期望使用的状态。该状态可以是：
- `QIcon::On`：`0`;当小部件处于“开启”状态时显示像素地图
- `QIcon::Off`：`1`;当小部件处于“关闭”状态时显示像素地图

### `[since 6.7] enum class QIcon::ThemeIcon`

**作用与语义：**

该枚举提供了大多数图标主题实现提供的图标访问。
- `QIcon::ThemeIcon::AddressBookNew`：`0`;用于创建新通讯录的图标。
- `QIcon::ThemeIcon::ApplicationExit`：`1`;用于退出应用程序的图标。
- `QIcon::ThemeIcon::AppointmentNew`：`2`;用于创建新任命的动作图标。
- `QIcon::ThemeIcon::CallStart`：`3`;用于发起或接听电话的图标。
- `QIcon::ThemeIcon::CallStop`：`4`;用于停止当前通话的图标。
- `QIcon::ThemeIcon::ContactNew`：`5`;用于创建新联系人的动作图标。
- `QIcon::ThemeIcon::DocumentNew`：`6`;用于创建新文档的操作图标。
- `QIcon::ThemeIcon::DocumentOpen`：`7`;用于打开文档的操作图标。
- `QIcon::ThemeIcon::DocumentOpenRecent`：`8`;用于打开最近打开的文档的操作图标。
- `QIcon::ThemeIcon::DocumentPageSetup`：`9`;页面设置操作的图标。
- `QIcon::ThemeIcon::DocumentPrint`：`10`;印刷动作图标。
- `QIcon::ThemeIcon::DocumentPrintPreview`：`11`;用于印刷预览动作的图标。
- `QIcon::ThemeIcon::DocumentProperties`：`12`;用于查看文档属性的动作图标。
- `QIcon::ThemeIcon::DocumentRevert`：`13`;用于恢复到文档前版本的图标。
- `QIcon::ThemeIcon::DocumentSave`：`14`;用于豁免动作的图标。
- `QIcon::ThemeIcon::DocumentSaveAs`：`15`;作为动作存档的图标。
- `QIcon::ThemeIcon::DocumentSend`：`16`;发送动作的图标。
- `QIcon::ThemeIcon::EditClear`：`17`;清除动作的图标。
- `QIcon::ThemeIcon::EditCopy`：`18`;用于复制动作的图标。
- `QIcon::ThemeIcon::EditCut`：`19`;切割动作的图标。
- `QIcon::ThemeIcon::EditDelete`：`20`;用于删除操作的图标。
- `QIcon::ThemeIcon::EditFind`：`21`;寻找动作的图标。
- `QIcon::ThemeIcon::EditPaste`：`22`;粘贴动作图标。
- `QIcon::ThemeIcon::EditRedo`：`23`;重做动作的图标。
- `QIcon::ThemeIcon::EditSelectAll`：`24`;选择所有动作的图标。
- `QIcon::ThemeIcon::EditUndo`：`25`;撤销动作的图标。
- `QIcon::ThemeIcon::FolderNew`：`26`;用于创建新文件夹的图标。
- `QIcon::ThemeIcon::FormatIndentLess`：`27`;用于缩进格式化动作的图标。
- `QIcon::ThemeIcon::FormatIndentMore`：`28`;用于增加缩进格式操作的图标。
- `QIcon::ThemeIcon::FormatJustifyCenter`：`29`;中心对齐格式操作的图标。
- `QIcon::ThemeIcon::FormatJustifyFill`：`30`;填充对方格式操作的图标。
- `QIcon::ThemeIcon::FormatJustifyLeft`：`31`;左侧对齐格式操作的图标。
- `QIcon::ThemeIcon::FormatJustifyRight`：`32`;正确对齐动作的图标。
- `QIcon::ThemeIcon::FormatTextDirectionLtr`：`33`;用于从左到右的文本格式化操作图标。
- `QIcon::ThemeIcon::FormatTextDirectionRtl`：`34`;右向左格式化动作的图标。
- `QIcon::ThemeIcon::FormatTextBold`：`35`;用于粗体文本格式化动作的图标。
- `QIcon::ThemeIcon::FormatTextItalic`：`36`;斜体文本格式操作的图标。
- `QIcon::ThemeIcon::FormatTextUnderline`：`37`;用于下划线文本格式操作的图标。
- `QIcon::ThemeIcon::FormatTextStrikethrough`：`38`;用于删除文本格式化操作的图标。
- `QIcon::ThemeIcon::GoDown`：`39`;列表动作中“下降”的图标。
- `QIcon::ThemeIcon::GoHome`：`40`;前往主页位置操作的图标。
- `QIcon::ThemeIcon::GoNext`：`41`;列表动作中“前往下一个项目”的图标。
- `QIcon::ThemeIcon::GoPrevious`：`42`;列表操作中“前往上一个项目”的图标。
- `QIcon::ThemeIcon::GoUp`：`43`;列表动作中向上的图标。
- `QIcon::ThemeIcon::HelpAbout`：`44`;帮助菜单中关于项的图标。
- `QIcon::ThemeIcon::HelpFaq`：`45`;帮助菜单中常见问题项目的图标。
- `QIcon::ThemeIcon::InsertImage`：`46`;应用程序插入图像动作的图标。
- `QIcon::ThemeIcon::InsertLink`：`47`;应用程序插入链接动作的图标。
- `QIcon::ThemeIcon::InsertText`：`48`;应用程序插入文本动作的图标。
- `QIcon::ThemeIcon::ListAdd`：`49`;添加列表操作的图标。
- `QIcon::ThemeIcon::ListRemove`：`50`;用于“从列表中移除”操作的图标。
- `QIcon::ThemeIcon::MailForward`：`51`;前进动作的图标。
- `QIcon::ThemeIcon::MailMarkImportant`：`52`;标记作为重要动作的图标。
- `QIcon::ThemeIcon::MailMarkRead`：`53`;标记图标表示动作。
- `QIcon::ThemeIcon::MailMarkUnread`：`54`;标记图标为未读动作。
- `QIcon::ThemeIcon::MailMessageNew`：`55`;用于“写新邮件”操作的图标。
- `QIcon::ThemeIcon::MailReplyAll`：`56`;对所有动作的回复图标。
- `QIcon::ThemeIcon::MailReplySender`：`57`;回复发送者操作的图标。
- `QIcon::ThemeIcon::MailSend`：`58`;发送动作的图标。
- `QIcon::ThemeIcon::MediaEject`：`59`;媒体播放器或文件管理器的弹出动作图标。
- `QIcon::ThemeIcon::MediaPlaybackPause`：`60`;媒体播放器暂停动作的图标。
- `QIcon::ThemeIcon::MediaPlaybackStart`：`61`;媒体播放器开始播放动作的图标。
- `QIcon::ThemeIcon::MediaPlaybackStop`：`62`;媒体播放器停止动作的图标。
- `QIcon::ThemeIcon::MediaRecord`：`63`;媒体应用记录动作的图标。
- `QIcon::ThemeIcon::MediaSeekBackward`：`64`;媒体播放器的寻回动作图标。
- `QIcon::ThemeIcon::MediaSeekForward`：`65`;媒体播放器前进动作的图标。
- `QIcon::ThemeIcon::MediaSkipBackward`：`66`;媒体播放器向后跳动动作的图标。
- `QIcon::ThemeIcon::MediaSkipForward`：`67`;媒体播放器跳转动作的图标。
- `QIcon::ThemeIcon::ObjectRotateLeft`：`68`;对物体执行左旋动作的图标。
- `QIcon::ThemeIcon::ObjectRotateRight`：`69`;用于对物体进行右旋转动作的图标。
- `QIcon::ThemeIcon::ProcessStop`：`70`;在应用中停止动作的图标，这些动作可能需要较长时间处理，例如浏览器中的网页加载。
- `QIcon::ThemeIcon::SystemLockScreen`：`71`;锁屏动作图标。
- `QIcon::ThemeIcon::SystemLogOut`：`72`;登出操作图标。
- `QIcon::ThemeIcon::SystemSearch`：`73`;搜索动作的图标。
- `QIcon::ThemeIcon::SystemReboot`：`74`;重启动作的图标。
- `QIcon::ThemeIcon::SystemShutdown`：`75`;关机动作的图标。
- `QIcon::ThemeIcon::ToolsCheckSpelling`：`76`;用于校对拼写动作的图标。
- `QIcon::ThemeIcon::ViewFullscreen`：`77`;全屏动作图标。
- `QIcon::ThemeIcon::ViewRefresh`：`78`;刷新动作的图标。
- `QIcon::ThemeIcon::ViewRestore`：`79`;用于退出全屏视图的图标。
- `QIcon::ThemeIcon::WindowClose`：`80`;关闭窗口动作的图标。
- `QIcon::ThemeIcon::WindowNew`：`81`;新窗口动作的图标。
- `QIcon::ThemeIcon::ZoomFitBest`：`82`;最佳配合动作的图标。
- `QIcon::ThemeIcon::ZoomIn`：`83`;用于放大操作的图标。
- `QIcon::ThemeIcon::ZoomOut`：`84`;用于缩放动作的图标。
- `QIcon::ThemeIcon::AudioCard`：`85`;音频渲染设备的图标。
- `QIcon::ThemeIcon::AudioInputMicrophone`：`86`;麦克风音频输入设备的图标。
- `QIcon::ThemeIcon::Battery`：`87`;系统电池设备的图标。
- `QIcon::ThemeIcon::CameraPhoto`：`88`;数字静态相机设备的图标。
- `QIcon::ThemeIcon::CameraVideo`：`89`;视频摄像机设备的图标。
- `QIcon::ThemeIcon::CameraWeb`：`90`;网络摄像头设备的图标。
- `QIcon::ThemeIcon::Computer`：`91`;整个计算设备的图标。
- `QIcon::ThemeIcon::DriveHarddisk`：`92`;硬盘驱动器的图标。
- `QIcon::ThemeIcon::DriveOptical`：`93`;光盘驱动器（如CD和DVD）的图标。
- `QIcon::ThemeIcon::InputGaming`：`94`;游戏输入设备的图标。
- `QIcon::ThemeIcon::InputKeyboard`：`95`;键盘输入设备的图标。
- `QIcon::ThemeIcon::InputMouse`：`96`;鼠标输入设备的图标。
- `QIcon::ThemeIcon::InputTablet`：`97`;图形板输入设备的图标。
- `QIcon::ThemeIcon::MediaFlash`：`98`;闪存介质图标，如记忆棒。
- `QIcon::ThemeIcon::MediaOptical`：`99`;用于物理光媒体（如CD和DVD）的图标。
- `QIcon::ThemeIcon::MediaTape`：`100`;通用物理磁带介质的图标。
- `QIcon::ThemeIcon::MultimediaPlayer`：`101`;通用多媒体播放设备的图标。
- `QIcon::ThemeIcon::NetworkWired`：`102`;有线网络连接的图标。
- `QIcon::ThemeIcon::NetworkWireless`：`103`;无线网络连接的图标。
- `QIcon::ThemeIcon::Phone`：`104`;手机设备的图标。
- `QIcon::ThemeIcon::Printer`：`105`;打印机设备的图标。
- `QIcon::ThemeIcon::Scanner`：`106`;扫描仪的图标。
- `QIcon::ThemeIcon::VideoDisplay`：`107`;视频显示显示器的图标。
- `QIcon::ThemeIcon::AppointmentMissed`：`108`;当错过预约时的图标。
- `QIcon::ThemeIcon::AppointmentSoon`：`109`;预约即将到来的图标。
- `QIcon::ThemeIcon::AudioVolumeHigh`：`110`;用于表示高音量的图标。
- `QIcon::ThemeIcon::AudioVolumeLow`：`111`;用于表示低音量的图标。
- `QIcon::ThemeIcon::AudioVolumeMedium`：`112`;用于表示中等音量的图标。
- `QIcon::ThemeIcon::AudioVolumeMuted`：`113`;用于表示音频播放静音状态的图标。
- `QIcon::ThemeIcon::BatteryCaution`：`114`;电池电量低于40%时使用的图标。
- `QIcon::ThemeIcon::BatteryLow`：`115`;当电池电量低于20%时使用的图标。
- `QIcon::ThemeIcon::DialogError`：`116`;打开对话框时用来向用户解释错误状况的图标。
- `QIcon::ThemeIcon::DialogInformation`：`117`;打开对话时用来向用户提供可能与请求操作相关的信息的图标。
- `QIcon::ThemeIcon::DialogPassword`：`118`;当打开请求用户身份验证凭证的对话框时使用的图标。
- `QIcon::ThemeIcon::DialogQuestion`：`119`;打开对话框时用来向用户提问的图标。
- `QIcon::ThemeIcon::DialogWarning`：`120`;打开对话框时用来警告用户请求操作即将出现的问题图标。
- `QIcon::ThemeIcon::FolderDragAccept`：`121`;当可接受的对象被拖拽到文件夹时使用的图标。
- `QIcon::ThemeIcon::FolderOpen`：`122`;用于文件夹的图标，当其内容在同一窗口中显示时。
- `QIcon::ThemeIcon::FolderVisiting`：`123`;用于文件夹的图标，当其内容在另一个窗口中显示时。
- `QIcon::ThemeIcon::ImageLoading`：`124`;加载另一张图像时使用的图标。
- `QIcon::ThemeIcon::ImageMissing`：`125`;当无法加载另一张图片时使用的图标。
- `QIcon::ThemeIcon::MailAttachment`：`126`;包含附件的消息图标。
- `QIcon::ThemeIcon::MailUnread`：`127`;表示未读消息的图标。
- `QIcon::ThemeIcon::MailRead`：`128`;已读消息的图标。
- `QIcon::ThemeIcon::MailReplied`：`129`;已回复消息的图标。
- `QIcon::ThemeIcon::MediaPlaylistRepeat`：`130`;媒体播放器的重复模式图标。
- `QIcon::ThemeIcon::MediaPlaylistShuffle`：`131`;媒体播放器随机播放模式的图标。
- `QIcon::ThemeIcon::NetworkOffline`：`132`;用于表示设备未连接到网络的图标。
- `QIcon::ThemeIcon::PrinterPrinting`：`133`;打印作业成功传输到打印设备时使用的图标。
- `QIcon::ThemeIcon::SecurityHigh`：`134`;用于表示某物品安全等级已知较高的图标。
- `QIcon::ThemeIcon::SecurityLow`：`135`;用于表示某物品安全等级已知较低的图标。
- `QIcon::ThemeIcon::SoftwareUpdateAvailable`：`136`;用于表示有更新的图标。
- `QIcon::ThemeIcon::SoftwareUpdateUrgent`：`137`;用于表示紧急更新可用图标。
- `QIcon::ThemeIcon::SyncError`：`138`;当尝试在设备间同步数据时出现错误时使用的图标。
- `QIcon::ThemeIcon::SyncSynchronizing`：`139`;当数据成功同步时使用的图标。
- `QIcon::ThemeIcon::UserAvailable`：`140`;用于表示用户可用的图标。
- `QIcon::ThemeIcon::UserOffline`：`141`;用于表示用户不可用的图标。
- `QIcon::ThemeIcon::WeatherClear`：`142`;用于表示天空晴朗的图标。
- `QIcon::ThemeIcon::WeatherClearNight`：`143`;该图标用于表示夜间天空晴朗。
- `QIcon::ThemeIcon::WeatherFewClouds`：`144`;该图标用于表示天空部分多云。
- `QIcon::ThemeIcon::WeatherFewCloudsNight`：`145`;该图标用于表示夜间天空部分多云。
- `QIcon::ThemeIcon::WeatherFog`：`146`;用来表示天气有雾的图标。
- `QIcon::ThemeIcon::WeatherShowers`：`147`;该图标用于表示正在下雨。
- `QIcon::ThemeIcon::WeatherSnow`：`148`;用于表示下雪的图标。
- `QIcon::ThemeIcon::WeatherStorm`：`149`;该图标用于表示天气为暴风雨。
该枚举于Qt 6.7引入。

### `[noexcept] QIcon::QIcon()`

**作用与语义：**

构造一个空图标。

### `[explicit] QIcon::QIcon(QIconEngine *engine)`

**作用与语义：**

创建一个带有特定图标`engine`的图标。该图标拥有引擎的所有权。

### `QIcon::QIcon(const QPixmap &pixmap)`

**作用与语义：**

从`pixmap`构造一个图标。

### `[explicit] QIcon::QIcon(const QString &fileName)`

**作用与语义：**

从文件中构建带有指定`fileName`的图标。文件将按需加载。
如果`fileName`包含相对路径（例如仅文件名），则必须相对于运行时工作目录找到相关文件。
文件名可以指磁盘上的实际文件，也可以指应用程序的嵌入式资源之一。有关如何将镜像和其他资源文件嵌入应用程序可执行文件的详细信息，请参见资源系统概述。
使用`QImageReader::supportedImageFormats()`和`QImageWriter::supportedImageFormats()`功能检索支持的文件格式完整列表。

### `QIcon::QIcon(const QIcon &other)`

**作用与语义：**

构建一份`other`的副本。这速度非常快。

### `[noexcept] QIcon::QIcon(QIcon &&other)`

**作用与语义：**

Move构造一个QIcon实例，使其指向`other`所指向的同一个对象。

### `[noexcept] QIcon::~QIcon()`

**作用与语义：**

摧毁了图标。

### `QSize QIcon::actualSize(const QSize &size, QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

返回请求的`size`、`mode`和`state`图标的实际大小。结果可能比请求的要小，但绝不会大于请求。返回的大小以设备无关的像素为单位（这对高DPI像素映射尤为重要）。

### `void QIcon::addFile(const QString &fileName, const QSize &size = QSize(), QIcon::Mode mode = Normal, QIcon::State state = Off)`

**作用与语义：**

将文件中带有指定`fileName`的图片添加到图标中，作为`size`、`mode`和`state`的专用化。该文件将按需加载。注意：自定义图标引擎可以忽略额外添加的像素映射。
如果`fileName`包含相对路径（例如仅文件名），则必须相对于运行时工作目录找到相关文件。
文件名可以指磁盘上的实际文件，也可以指应用程序的嵌入式资源之一。有关如何将镜像和其他资源文件嵌入应用程序可执行文件的详细信息，请参见资源系统概述。
使用`QImageReader::supportedImageFormats()`和`QImageWriter::supportedImageFormats()`功能检索支持的文件格式完整列表。
如果存在高分辨率图像版本（由基名上的后缀 `@2x` 标识），则会自动加载并添加，设备像素比设置为 2。通过设置环境变量 `QT_HIGHDPI_DISABLE_2X_IMAGE_LOADING`（参见 `QImageReader`）可以禁用该功能。
注意：当你在`QIcon`中添加非空文件名时，图标会变成非空，即使文件不存在或指向损坏文件。

### `void QIcon::addPixmap(const QPixmap &pixmap, QIcon::Mode mode = Normal, QIcon::State state = Off)`

**作用与语义：**

为图标添加`pixmap`，作为`mode`和`state`的专精。
自定义图标引擎可以忽略额外添加的像素地图。

### `QList<QSize> QIcon::availableSizes(QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

返回指定`mode`和`state`可用的图标大小列表。

### `qint64 QIcon::cacheKey() const`

**作用与语义：**

返回一个编号，用于识别该`QIcon`对象的内容。如果不同`QIcon`对象指向相同内容，则可以拥有相同的密钥。
当图标通过`addPixmap()`或`addFile()`被修改时，cacheKey() 也会改变。
缓存密钥主要与缓存配合使用。

### `[static] QStringList QIcon::fallbackSearchPaths()`

**作用与语义：**

返回图标的备用搜索路径。
如果当前图标主题或备用图标主题未能提供图标查找结果，则会参考备援搜索路径以获取独立图标文件。
如果未设置，备份搜索路径将由平台定义。

### `[static] QString QIcon::fallbackThemeName()`

**作用与语义：**

返回备用图标主题的名称。
如果未设置，备用图标主题将由平台定义。
注意：平台备援图标主题目前仅在基于Freedesktop的系统上实现，图标主题取决于你的桌面设置。

### `[static] QIcon QIcon::fromTheme(const QString &name)`

**作用与语义：**

返回当前图标主题中对应`name`的`QIcon`。
如果当前主题没有提供`name`图标，则先参考备援图标主题，然后退回到备援图标搜索路径中查找独立图标文件。最后，会参考平台的原生图标库。
要从当前图标主题中获取图标：
如果图标主题未通过`setThemeName()`明确设置，则将使用平台定义的图标主题。

**官方示例：**

```cpp
 QIcon undoicon = QIcon::fromTheme(QIcon::ThemeIcon::EditUndo);
```

### `[static, since 6.7] QIcon QIcon::fromTheme(QIcon::ThemeIcon icon, const QIcon &fallback)`

**作用与语义：**

返回当前图标主题中对应`icon`的`QIcon`。
如果当前主题没有提供`icon`图标，则先参考备用图标主题，然后再退回到备用图标搜索路径中查找独立图标文件。最后，会参考平台的原生图标库。
如果找不到图标且提供了`fallback`，则返回`fallback`。这有助于提供保证的备选，无论当前的图标主题和备援路径是否支持请求的图标。
如果找不到图标且没有提供`fallback`，则会返回一个默认的空构造`QIcon`。

### `[static] QIcon QIcon::fromTheme(const QString &name, const QIcon &fallback)`

**作用与语义：**

返回当前图标主题中对应`icon`的`QIcon`。
如果当前主题没有提供`icon`图标，则先参考备用图标主题，然后再退回到备用图标搜索路径中查找独立图标文件。最后，会参考平台的原生图标库。
如果找不到图标且提供了`fallback`，则返回`fallback`。这有助于提供保证的备选，无论当前的图标主题和备援路径是否支持请求的图标。
如果找不到图标且没有提供`fallback`，则会返回一个默认的空构造`QIcon`。

### `[static] bool QIcon::hasThemeIcon(const QString &name)`

**作用与语义：**

如果当前图标主题或任何备用图标（如`fromTheme()`所述）中有可`name`的图标，返回`true`，否则返回`false`。

### `[static, since 6.7] bool QIcon::hasThemeIcon(QIcon::ThemeIcon icon)`

**作用与语义：**

如果当前图标主题或`fromTheme()`描述的备用方案中有可`icon`图标，`true`返回，否则返回`false`。

### `bool QIcon::isMask() const`

**作用与语义：**

如果该图标被标记为遮罩图像，则返回`true`。某些平台对遮罩图标的渲染方式不同（例如macOS上的菜单图标）。

### `bool QIcon::isNull() const`

**作用与语义：**

如果图标为空，返回`true`;否则返回`false`。
如果图标既没有像素映射也没有文件名，则该图标为空。
注意：即使是非空图标，也可能无法创建有效的像素图，例如，如果文件不存在或无法读取。

### `QString QIcon::name() const`

**作用与语义：**

如果有，返回创建图标时使用的名称。
根据图标的创建方式，它可能会有相应的名称。这适用于用`fromTheme()`创建的图标。

### `void QIcon::paint(QPainter *painter, const QRect &rect, Qt::Alignment alignment = Qt::AlignCenter, QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

利用`painter`将图标涂成指定`alignment`、所需`mode`，并`state`到矩形`rect`中。

### `void QIcon::paint(QPainter *painter, int x, int y, int w, int h, Qt::Alignment alignment = Qt::AlignCenter, QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

将图标绘制到矩形 `QRect`（`x`、`y`、`w`、`h`）。

### `QPixmap QIcon::pixmap(const QSize &size, QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

返回包含请求的 `size`、`mode` 和 `state` 像素映射，必要时生成一个像素映射。像素映射可能比请求的更小，但不会更大，除非返回的像素映射的设备像素比大于 1。

### `QPixmap QIcon::pixmap(int extent, QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

返回大小为`QSize`（`extent`， `extent`）的像素映射。像素映射可能比请求的尺寸小，但不会大于，除非返回的像素映射的设备-像素比大于1。

### `[since 6.0] QPixmap QIcon::pixmap(const QSize &size, qreal devicePixelRatio, QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

返回包含请求的`size`、`devicePixelRatio`、`mode`和`state`的像素图，必要时生成具有指定`mode`和`state`的像素图。像素图可能比请求的更小，但绝不会更大，除非返回的像素图的设备与像素比大于1。
注意：请求的 devicePixelRatio 可能与返回的 PixelRatio 不匹配。这会延迟`QPixmap`的缩放，直到后续绘制时才会被调整。
注意：在Qt 6.8之前，这个函数将设备相关的pixmap尺寸传递给了`QIconEngine::scaledPixmap()`，因为Qt 6.8是设备无关的尺寸（不按`devicePixelRatio`比例调整）。

### `QPixmap QIcon::pixmap(int w, int h, QIcon::Mode mode = Normal, QIcon::State state = Off) const`

**作用与语义：**

返回大小为`QSize`（`w`， `h`）的像素图。像素图可能比请求的要小，但不会更大，除非返回的像素图的设备-像素比大于1。

### `[static] void QIcon::setFallbackSearchPaths(const QStringList &paths)`

**作用与语义：**

将图标的备用搜索路径设置为`paths`。
如果当前图标主题或备用图标主题未能提供图标查找结果，则会参考备援搜索路径以获取独立图标文件。

**官方示例：**

```cpp
 QIcon::setFallbackSearchPaths(QIcon::fallbackSearchPaths() << "my/search/path");
```

### `[static] void QIcon::setFallbackThemeName(const QString &name)`

**作用与语义：**

将备用图标主题设置为`name`。
对于当前图标主题未提供的图标，或当前图标主题不存在时，会参考备用图标主题。
`name`应与`setThemeName()`文档格式一致，并会在`themeSearchPaths()`中查找。
注意：在创建`QGuiApplication`之前应设置备用图标主题，以确保初始化正确。

### `void QIcon::setIsMask(bool isMask)`

**作用与语义：**

表示该图标是遮罩图像（布尔`isMask`），因此可以根据显示位置进行修改。

### `[static] void QIcon::setThemeName(const QString &name)`

**作用与语义：**

将当前图标主题设置为`name`。
如果主题与已安装的字体名称匹配，该字体提供命名字形，那么与其中一个字形匹配的`QIcon::fromTheme`调用将生成该字形的图标。
否则，主题将在`themeSearchPaths()`中被查找。目前唯一支持的图标主题格式是Freedesktop图标主题规范。`name`应对应themeSearchPath()中的目录名，其中包含描述其内容的`index.theme`文件。

### `[static] void QIcon::setThemeSearchPaths(const QStringList &paths)`

**作用与语义：**

将图标主题的搜索路径设置为`paths`。
`paths`内容应遵循`setThemeName()`所记录的主题格式。

### `[noexcept] void QIcon::swap(QIcon &other)`

**作用与语义：**

将这个图标与`other`交换。这个操作非常快，而且从未失败过。

### `[static] QString QIcon::themeName()`

**作用与语义：**

返回当前图标主题的名称。
如果未设置，当前图标主题将由平台定义。
注意：平台图标主题目前仅在基于Freedesktop的系统上实现，图标主题取决于你的桌面设置。

### `[static] QStringList QIcon::themeSearchPaths()`

**作用与语义：**

返回图标主题的搜索路径。
默认的搜索路径由平台定义。所有平台也将以资源目录`:\icons`作为备用。

### `QIcon::operator QVariant() const`

**作用与语义：**

图标返回为`QVariant`。

### `[noexcept] QIcon &QIcon::operator=(QIcon &&other)`

**作用与语义：**

Move-assign `other`到这个`QIcon`实例。

### `QIcon &QIcon::operator=(const QIcon &other)`

**作用与语义：**

将`other`图标分配给该图标，并返回对该图标的引用。

### `QDataStream &operator<<(QDataStream &stream, const QIcon &icon)`

**作用与语义：**

将给定的`icon`写入给定`stream`，作为PNG图像。如果图标包含多个图像，所有图像都会写入流。注意，将流写入文件不会产生有效的图像文件。

### `QDataStream &operator>>(QDataStream &stream, QIcon &icon)`

**作用与语义：**

将给定`stream`中的图像或一组图像读取到给定的`icon`。

### `(since 6.7) QIcon fromTheme(QIcon::ThemeIcon icon)`

**作用与语义：**

返回当前图标主题中对应`name`的`QIcon`。
如果当前主题没有提供`name`图标，则会参考备援图标主题，然后退回到备用图标搜索路径中查找独立图标文件。最后，会参考平台的原生图标库。
如果找不到图标`fallback`则返回。
这有助于提供保证的后备，无论当前的图标主题和备用路径是否支持所请求的图标。

**官方示例：**

```cpp
 QIcon undoicon = QIcon::fromTheme(QIcon::ThemeIcon::EditUndo, QIcon(":/undo.png"));
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QIcon` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
