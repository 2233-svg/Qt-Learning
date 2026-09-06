#include "MainWindow.h"

#include <QAction>
#include <QApplication>
#include <QCoreApplication>
#include <QDesktopServices>
#include <QDir>
#include <QFile>
#include <QFileDialog>
#include <QFileInfo>
#include <QFontDatabase>
#include <QHeaderView>
#include <QKeySequence>
#include <QLabel>
#include <QLineEdit>
#include <QMap>
#include <QMenu>
#include <QMenuBar>
#include <QMessageBox>
#include <QProcess>
#include <QSettings>
#include <QScrollBar>
#include <QSet>
#include <QSplitter>
#include <QStatusBar>
#include <QTextBrowser>
#include <QTextDocument>
#include <QTimer>
#include <QToolBar>
#include <QTreeWidget>
#include <QUrl>
#include <QVBoxLayout>
#include <QWidget>
#include <QStyle>

namespace {

const QString fallbackDocumentDirectory = QStringLiteral("D:/工作目录/Qt6.11.1_ClassDocs");

QString firstLine(const QString &markdown)
{
    const int lineEnd = markdown.indexOf('\n');
    return (lineEnd < 0 ? markdown : markdown.left(lineEnd)).trimmed();
}

QString moduleDirectoryName(const QString &module)
{
    static const QHash<QString, QString> names{
        {QStringLiteral("Qt Charts"), QStringLiteral("QtCharts")},
        {QStringLiteral("Qt Concurrent"), QStringLiteral("QtConcurrent")},
        {QStringLiteral("Qt Core"), QStringLiteral("QtCore")},
        {QStringLiteral("Qt D-Bus"), QStringLiteral("QtD_Bus")},
        {QStringLiteral("Qt GUI"), QStringLiteral("QtGUI")},
        {QStringLiteral("Qt Help"), QStringLiteral("QtHelp")},
        {QStringLiteral("Qt Multimedia"), QStringLiteral("QtMultimedia")},
        {QStringLiteral("Qt Network"), QStringLiteral("QtNetwork")},
        {QStringLiteral("Qt Print Support"), QStringLiteral("QtPrint_Support")},
        {QStringLiteral("Qt Qml"), QStringLiteral("QtQml")},
        {QStringLiteral("Qt Quick"), QStringLiteral("QtQuick")},
        {QStringLiteral("Qt Quick 3D"), QStringLiteral("QtQuick_3D")},
        {QStringLiteral("Qt Quick Controls"), QStringLiteral("QtQuick_Controls")},
        {QStringLiteral("Qt SQL"), QStringLiteral("QtSQL")},
        {QStringLiteral("Qt SVG"), QStringLiteral("QtSVG")},
        {QStringLiteral("Qt Shader Tools"), QStringLiteral("QtShader_Tools")},
        {QStringLiteral("Qt Spatial Audio"), QStringLiteral("QtSpatial_Audio")},
        {QStringLiteral("Qt TaskTree"), QStringLiteral("QtTaskTree")},
        {QStringLiteral("Qt Test"), QStringLiteral("QtTest")},
        {QStringLiteral("Qt UI Tools"), QStringLiteral("QtUI_Tools")},
        {QStringLiteral("Qt Widgets"), QStringLiteral("QtWidgets")},
        {QStringLiteral("Qt XML"), QStringLiteral("QtXML")}
    };
    return names.value(module, module);
}

} // namespace

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle(QStringLiteral("Qt 文档中心"));
    resize(1440, 920);
    setMinimumSize(980, 620);

    setupUi();

    QSettings settings;
    const QString bundledDirectory = QDir(QCoreApplication::applicationDirPath()).filePath(QStringLiteral("Qt6.11.1_ClassDocs"));
    QString directory = settings.value(QStringLiteral("documentDirectory")).toString();
    if (directory.isEmpty() || !QDir(directory).exists()) {
        if (QDir(bundledDirectory).exists())
            directory = bundledDirectory;
        else
            directory = fallbackDocumentDirectory;
    }
    setDocumentDirectory(directory);
}

void MainWindow::setupUi()
{
    auto *fileMenu = menuBar()->addMenu(QStringLiteral("文件"));
    auto *viewMenu = menuBar()->addMenu(QStringLiteral("视图"));
    auto *helpMenu = menuBar()->addMenu(QStringLiteral("帮助"));

    auto *toolBar = addToolBar(QStringLiteral("导航"));
    toolBar->setMovable(false);
    toolBar->setIconSize(QSize(18, 18));

    backAction_ = toolBar->addAction(style()->standardIcon(QStyle::SP_ArrowBack), QStringLiteral("后退"));
    backAction_->setToolTip(QStringLiteral("后退 (Alt+Left)"));
    backAction_->setShortcut(QKeySequence(Qt::ALT | Qt::Key_Left));
    backAction_->setEnabled(false);
    connect(backAction_, &QAction::triggered, this, &MainWindow::goBack);

    forwardAction_ = toolBar->addAction(style()->standardIcon(QStyle::SP_ArrowForward), QStringLiteral("前进"));
    forwardAction_->setToolTip(QStringLiteral("前进 (Alt+Right)"));
    forwardAction_->setShortcut(QKeySequence(Qt::ALT | Qt::Key_Right));
    forwardAction_->setEnabled(false);
    connect(forwardAction_, &QAction::triggered, this, &MainWindow::goForward);

    toolBar->addSeparator();
    QAction *homeAction = toolBar->addAction(style()->standardIcon(QStyle::SP_DirHomeIcon), QStringLiteral("文档首页"));
    homeAction->setToolTip(QStringLiteral("打开文档首页"));
    connect(homeAction, &QAction::triggered, this, &MainWindow::goHome);

    QAction *refreshAction = toolBar->addAction(style()->standardIcon(QStyle::SP_BrowserReload), QStringLiteral("重新扫描"));
    refreshAction->setToolTip(QStringLiteral("重新扫描 Markdown 文档 (F5)"));
    refreshAction->setShortcut(QKeySequence::Refresh);
    connect(refreshAction, &QAction::triggered, this, &MainWindow::rescanDocuments);

    QAction *openAction = toolBar->addAction(style()->standardIcon(QStyle::SP_DirOpenIcon), QStringLiteral("选择目录"));
    openAction->setToolTip(QStringLiteral("选择 Markdown 文档目录 (Ctrl+O)"));
    openAction->setShortcut(QKeySequence::Open);
    connect(openAction, &QAction::triggered, this, &MainWindow::chooseDocumentDirectory);

    toolBar->addSeparator();
    QAction *zoomInAction = toolBar->addAction(style()->standardIcon(QStyle::SP_ArrowUp), QStringLiteral("放大"));
    zoomInAction->setToolTip(QStringLiteral("放大正文 (Ctrl+=)"));
    zoomInAction->setShortcut(QKeySequence(Qt::CTRL | Qt::Key_Equal));
    connect(zoomInAction, &QAction::triggered, this, &MainWindow::zoomIn);

    QAction *zoomOutAction = toolBar->addAction(style()->standardIcon(QStyle::SP_ArrowDown), QStringLiteral("缩小"));
    zoomOutAction->setToolTip(QStringLiteral("缩小正文 (Ctrl+-)"));
    zoomOutAction->setShortcut(QKeySequence(Qt::CTRL | Qt::Key_Minus));
    connect(zoomOutAction, &QAction::triggered, this, &MainWindow::zoomOut);

    QAction *fileOpenAction = fileMenu->addAction(QStringLiteral("选择文档目录..."), this, &MainWindow::chooseDocumentDirectory);
    fileOpenAction->setShortcut(QKeySequence::Open);
    QAction *fileRefreshAction = fileMenu->addAction(QStringLiteral("重新扫描文档"));
    fileRefreshAction->setShortcut(QKeySequence::Refresh);
    connect(fileRefreshAction, &QAction::triggered, this, &MainWindow::rescanDocuments);
    fileMenu->addSeparator();
    QAction *quitAction = fileMenu->addAction(QStringLiteral("退出"));
    quitAction->setShortcut(QKeySequence::Quit);
    connect(quitAction, &QAction::triggered, this, &QWidget::close);

    viewMenu->addAction(backAction_);
    viewMenu->addAction(forwardAction_);
    viewMenu->addAction(homeAction);
    viewMenu->addSeparator();
    viewMenu->addAction(zoomInAction);
    viewMenu->addAction(zoomOutAction);

    QAction *aboutAction = helpMenu->addAction(QStringLiteral("关于 Qt 文档中心"));
    connect(aboutAction, &QAction::triggered, this, [this] {
        QMessageBox::about(this, QStringLiteral("关于 Qt 文档中心"),
                           QStringLiteral("本地 Markdown 文档查看器\n\n"
                                          "用于浏览 Qt 6.11.1 C++ 类文档。\n"
                                          "支持目录扫描、全文搜索、内部链接和浏览历史。"));
    });

    auto *splitter = new QSplitter(Qt::Horizontal, this);
    splitter->setChildrenCollapsible(false);

    auto *navigationPanel = new QWidget(splitter);
    navigationPanel->setMinimumWidth(260);
    navigationPanel->setMaximumWidth(480);
    auto *navigationLayout = new QVBoxLayout(navigationPanel);
    navigationLayout->setContentsMargins(10, 10, 8, 10);
    navigationLayout->setSpacing(8);

    auto *navigationHeading = new QLabel(QStringLiteral("文档目录"), navigationPanel);
    navigationHeading->setStyleSheet(QStringLiteral("font-size: 16px; font-weight: 600;"));
    navigationLayout->addWidget(navigationHeading);

    searchEdit_ = new QLineEdit(navigationPanel);
    searchEdit_->setPlaceholderText(QStringLiteral("搜索类名、模块或正文..."));
    searchEdit_->setClearButtonEnabled(true);
    searchEdit_->setToolTip(QStringLiteral("搜索类名、模块名称和 Markdown 正文"));
    connect(searchEdit_, &QLineEdit::textChanged, this, &MainWindow::filterDocuments);
    navigationLayout->addWidget(searchEdit_);

    searchSummary_ = new QLabel(navigationPanel);
    searchSummary_->setStyleSheet(QStringLiteral("color: palette(mid);"));
    navigationLayout->addWidget(searchSummary_);

    navigationTree_ = new QTreeWidget(navigationPanel);
    navigationTree_->setHeaderHidden(true);
    navigationTree_->setUniformRowHeights(true);
    navigationTree_->setIndentation(18);
    navigationTree_->setRootIsDecorated(true);
    navigationTree_->setSelectionMode(QAbstractItemView::SingleSelection);
    navigationTree_->setAlternatingRowColors(true);
    connect(navigationTree_, &QTreeWidget::itemClicked, this, &MainWindow::activateTreeItem);
    navigationLayout->addWidget(navigationTree_, 1);

    auto *readerPanel = new QWidget(splitter);
    auto *readerLayout = new QVBoxLayout(readerPanel);
    readerLayout->setContentsMargins(0, 0, 0, 0);
    readerLayout->setSpacing(0);

    auto *readerHeader = new QWidget(readerPanel);
    readerHeader->setObjectName(QStringLiteral("readerHeader"));
    readerHeader->setStyleSheet(QStringLiteral(
        "#readerHeader { border-bottom: 1px solid palette(midlight); }"
        "QLabel#documentTitle { font-size: 22px; font-weight: 600; }"
        "QLabel#documentPath { color: palette(mid); }"));
    auto *readerHeaderLayout = new QVBoxLayout(readerHeader);
    readerHeaderLayout->setContentsMargins(20, 14, 20, 12);
    readerHeaderLayout->setSpacing(4);

    documentTitle_ = new QLabel(readerHeader);
    documentTitle_->setObjectName(QStringLiteral("documentTitle"));
    documentTitle_->setText(QStringLiteral("Qt 文档中心"));
    documentTitle_->setWordWrap(true);
    readerHeaderLayout->addWidget(documentTitle_);

    documentPath_ = new QLabel(readerHeader);
    documentPath_->setObjectName(QStringLiteral("documentPath"));
    documentPath_->setText(QStringLiteral("请选择或扫描一个 Markdown 文档目录"));
    documentPath_->setTextInteractionFlags(Qt::TextSelectableByMouse);
    readerHeaderLayout->addWidget(documentPath_);
    readerLayout->addWidget(readerHeader);

    documentBrowser_ = new QTextBrowser(readerPanel);
    documentBrowser_->setOpenLinks(false);
    documentBrowser_->setOpenExternalLinks(false);
    documentBrowser_->setUndoRedoEnabled(false);
    documentBrowser_->setReadOnly(true);
    documentBrowser_->document()->setDefaultStyleSheet(QStringLiteral(
        "body { line-height: 1.35; }"
        "h1 { margin-top: 0.2em; }"
        "h2 { margin-top: 1.1em; }"
        "h3 { margin-top: 0.9em; }"
        "pre { background: #f3f4f6; padding: 8px; }"
        "code { background: #f3f4f6; }"
        "a { color: #2672c8; }"));
    connect(documentBrowser_, &QTextBrowser::anchorClicked, this, &MainWindow::followLink);
    readerLayout->addWidget(documentBrowser_, 1);

    splitter->addWidget(navigationPanel);
    splitter->addWidget(readerPanel);
    splitter->setStretchFactor(0, 0);
    splitter->setStretchFactor(1, 1);
    splitter->setSizes({320, 1120});
    setCentralWidget(splitter);

    statusLabel_ = new QLabel(statusBar());
    statusBar()->addPermanentWidget(statusLabel_, 1);
    statusBar()->showMessage(QStringLiteral("就绪"));
}

void MainWindow::setDocumentDirectory(const QString &directory)
{
    const QString absoluteDirectory = cleanPath(QFileInfo(directory).absoluteFilePath());
    if (!QDir(absoluteDirectory).exists()) {
        statusBar()->showMessage(QStringLiteral("找不到文档目录：%1").arg(absoluteDirectory));
        return;
    }

    documentDirectory_ = absoluteDirectory;
    QSettings settings;
    settings.setValue(QStringLiteral("documentDirectory"), documentDirectory_);
    buildDocumentIndex();
    history_.clear();
    historyIndex_ = -1;
    currentPath_.clear();
    buildNavigation();
    goHome();
}

void MainWindow::buildDocumentIndex()
{
    documents_.clear();
    documentIndexes_.clear();

    auto addDocument = [this](const QString &path, const QString &fallbackModule, bool isClass) {
        const QString markdown = readUtf8File(path);
        if (markdown.isEmpty())
            return;

        DocumentEntry entry;
        entry.path = cleanPath(path);
        entry.title = markdownTitle(markdown, QFileInfo(path).baseName());
        entry.module = markdownModule(markdown, fallbackModule);
        entry.markdown = markdown;
        entry.searchText = entry.title + QLatin1Char(' ') + entry.module + QLatin1Char(' ') + markdown;
        entry.isClass = isClass;
        documentIndexes_.insert(entry.path, documents_.size());
        documents_.append(std::move(entry));
    };

    const QString overviewPath = QDir(documentDirectory_).filePath(QStringLiteral("README.md"));
    if (QFileInfo::exists(overviewPath))
        addDocument(overviewPath, QStringLiteral("文档总览"), false);

    const QDir root(documentDirectory_);
    const QFileInfoList moduleDirectories = root.entryInfoList(QDir::Dirs | QDir::NoDotAndDotDot, QDir::Name);
    for (const QFileInfo &moduleDirectory : moduleDirectories) {
        const QString moduleIndexPath = QDir(moduleDirectory.absoluteFilePath()).filePath(QStringLiteral("index.md"));
        QString moduleName = moduleDirectory.fileName();
        if (QFileInfo::exists(moduleIndexPath)) {
            const QString indexMarkdown = readUtf8File(moduleIndexPath);
            moduleName = markdownModule(indexMarkdown, moduleName);
            addDocument(moduleIndexPath, moduleName, false);
        }

        const QDir moduleDir(moduleDirectory.absoluteFilePath());
        const QFileInfoList classFiles = moduleDir.entryInfoList({QStringLiteral("*.md")}, QDir::Files, QDir::Name);
        for (const QFileInfo &classFile : classFiles) {
            if (classFile.fileName().compare(QStringLiteral("index.md"), Qt::CaseInsensitive) == 0)
                continue;
            addDocument(classFile.absoluteFilePath(), moduleName, true);
        }
    }
}

void MainWindow::buildNavigation(const QString &filter)
{
    navigationTree_->setUpdatesEnabled(false);
    navigationTree_->clear();
    treeItems_.clear();

    const QString query = filter.trimmed();
    QMap<QString, QList<int>> moduleDocuments;
    int overviewIndex = -1;
    for (int index = 0; index < documents_.size(); ++index) {
        const DocumentEntry &entry = documents_.at(index);
        if (entry.module == QStringLiteral("文档总览"))
            overviewIndex = index;
        else
            moduleDocuments[entry.module].append(index);
    }

    if (overviewIndex >= 0) {
        const DocumentEntry &overview = documents_.at(overviewIndex);
        if (query.isEmpty() || overview.searchText.contains(query, Qt::CaseInsensitive)) {
            auto *overviewItem = new QTreeWidgetItem(navigationTree_);
            overviewItem->setText(0, QStringLiteral("文档总览"));
            overviewItem->setData(0, Qt::UserRole, overview.path);
            overviewItem->setToolTip(0, overview.path);
            treeItems_.insert(overview.path, overviewItem);
        }
    }

    int visibleDocuments = 0;
    for (auto moduleIt = moduleDocuments.cbegin(); moduleIt != moduleDocuments.cend(); ++moduleIt) {
        const QString moduleName = moduleIt.key();
        const QList<int> &indexes = moduleIt.value();
        int moduleIndex = -1;
        for (int index : indexes) {
            if (!documents_.at(index).isClass) {
                moduleIndex = index;
                break;
            }
        }

        bool moduleMatches = query.isEmpty() || moduleName.contains(query, Qt::CaseInsensitive);
        bool anyClassMatches = false;
        for (int index : indexes)
            anyClassMatches = anyClassMatches || !documents_.at(index).isClass || documents_.at(index).searchText.contains(query, Qt::CaseInsensitive);
        if (!moduleMatches && !anyClassMatches)
            continue;

        auto *moduleItem = new QTreeWidgetItem(navigationTree_);
        moduleItem->setText(0, moduleName);
        if (moduleIndex >= 0) {
            const DocumentEntry &entry = documents_.at(moduleIndex);
            moduleItem->setData(0, Qt::UserRole, entry.path);
            moduleItem->setToolTip(0, entry.path);
            treeItems_.insert(entry.path, moduleItem);
        }

        bool hasVisibleChild = false;
        for (int index : indexes) {
            const DocumentEntry &entry = documents_.at(index);
            if (!entry.isClass || (!query.isEmpty() && !moduleMatches && !entry.searchText.contains(query, Qt::CaseInsensitive)))
                continue;
            auto *classItem = new QTreeWidgetItem(moduleItem);
            classItem->setText(0, entry.title);
            classItem->setData(0, Qt::UserRole, entry.path);
            classItem->setToolTip(0, entry.path);
            treeItems_.insert(entry.path, classItem);
            hasVisibleChild = true;
            ++visibleDocuments;
        }
        if (query.isEmpty()) {
            visibleDocuments += indexes.size();
            moduleItem->setExpanded(false);
        } else {
            moduleItem->setExpanded(true);
        }
        if (!hasVisibleChild && moduleIndex < 0)
            delete moduleItem;
    }

    navigationTree_->setUpdatesEnabled(true);
    selectTreePath(currentPath_);
    updateSearchSummary(query);
}

void MainWindow::openDocument(const QString &path, bool addToHistory)
{
    const QString normalizedPath = cleanPath(path);
    const int index = documentIndex(normalizedPath);
    if (index < 0)
        return;

    if (addToHistory) {
        if (historyIndex_ >= 0 && history_.value(historyIndex_) == normalizedPath) {
            loadCurrentDocument();
            return;
        }
        while (history_.size() > historyIndex_ + 1)
            history_.removeLast();
        history_.append(normalizedPath);
        historyIndex_ = history_.size() - 1;
    }

    currentPath_ = normalizedPath;
    loadCurrentDocument();
}

void MainWindow::loadCurrentDocument()
{
    const int index = documentIndex(currentPath_);
    if (index < 0)
        return;

    const DocumentEntry &entry = documents_.at(index);
    documentTitle_->setText(entry.title);
    documentPath_->setText(QStringLiteral("%1  ·  %2").arg(entry.module, entry.path));
    documentBrowser_->setMarkdown(entry.markdown);
    documentBrowser_->verticalScrollBar()->setValue(0);
    setWindowTitle(QStringLiteral("%1 - Qt 文档中心").arg(entry.title));
    statusBar()->showMessage(QStringLiteral("正在浏览：%1").arg(entry.title));
    statusLabel_->setText(QStringLiteral("%1 个文档 · %2").arg(documents_.size()).arg(entry.module));
    selectTreePath(currentPath_);
    updateHistoryActions();
}

void MainWindow::filterDocuments(const QString &text)
{
    buildNavigation(text);
    if (!text.trimmed().isEmpty())
        statusBar()->showMessage(QStringLiteral("搜索：%1").arg(text.trimmed()));
    else
        statusBar()->showMessage(QStringLiteral("就绪"));
}

void MainWindow::activateTreeItem(QTreeWidgetItem *item, int column)
{
    Q_UNUSED(column);
    if (!item)
        return;
    const QString path = item->data(0, Qt::UserRole).toString();
    if (path.isEmpty())
        return;

    openDocument(path);

    const QString markTextPath = QStringLiteral("D:/markdown/marktext-win-x64-0.19.1/marktext.exe");
    if (!QFileInfo::exists(markTextPath)) {
        QMessageBox::warning(this, QStringLiteral("找不到 MarkText"),
                             QStringLiteral("未找到 MarkText：\n%1").arg(markTextPath));
        return;
    }

    const QString workingDirectory = QFileInfo(markTextPath).absolutePath();
    if (QProcess::startDetached(markTextPath, {path}, workingDirectory)) {
        statusBar()->showMessage(QStringLiteral("已使用 MarkText 打开：%1").arg(QFileInfo(path).fileName()));
    } else {
        QMessageBox::warning(this, QStringLiteral("打开失败"),
                             QStringLiteral("无法启动 MarkText 打开文档：\n%1").arg(path));
    }
}

void MainWindow::followLink(const QUrl &url)
{
    if (url.isEmpty())
        return;
    if (url.scheme() == QStringLiteral("http") || url.scheme() == QStringLiteral("https")) {
        QDesktopServices::openUrl(url);
        return;
    }
    if (url.path().isEmpty() && !url.fragment().isEmpty()) {
        documentBrowser_->scrollToAnchor(url.fragment());
        return;
    }

    QString linkPath = url.isLocalFile() ? url.toLocalFile() : url.path();
    if (linkPath.isEmpty())
        return;
    const QString target = cleanPath(QDir(QFileInfo(currentPath_).absolutePath()).absoluteFilePath(linkPath));
    if (!isWithinDocumentDirectory(target))
        return;
    if (documentIndex(target) >= 0) {
        const QString fragment = url.fragment();
        openDocument(target);
        if (!fragment.isEmpty())
            QTimer::singleShot(0, this, [this, fragment] { documentBrowser_->scrollToAnchor(fragment); });
    }
}

void MainWindow::goBack()
{
    if (historyIndex_ <= 0)
        return;
    --historyIndex_;
    currentPath_ = history_.at(historyIndex_);
    loadCurrentDocument();
}

void MainWindow::goForward()
{
    if (historyIndex_ < 0 || historyIndex_ + 1 >= history_.size())
        return;
    ++historyIndex_;
    currentPath_ = history_.at(historyIndex_);
    loadCurrentDocument();
}

void MainWindow::goHome()
{
    const QString homePath = QDir(documentDirectory_).filePath(QStringLiteral("README.md"));
    if (documentIndex(homePath) >= 0)
        openDocument(homePath);
}

void MainWindow::chooseDocumentDirectory()
{
    const QString directory = QFileDialog::getExistingDirectory(this, QStringLiteral("选择 Markdown 文档目录"), documentDirectory_);
    if (!directory.isEmpty())
        setDocumentDirectory(directory);
}

void MainWindow::rescanDocuments()
{
    if (documentDirectory_.isEmpty())
        return;
    const QString previousPath = currentPath_;
    buildDocumentIndex();
    history_.clear();
    historyIndex_ = -1;
    currentPath_.clear();
    buildNavigation(searchEdit_->text());
    if (documentIndex(previousPath) >= 0)
        openDocument(previousPath);
    else
        goHome();
    statusBar()->showMessage(QStringLiteral("扫描完成，共发现 %1 个 Markdown 文档").arg(documents_.size()));
}

void MainWindow::zoomIn()
{
    documentBrowser_->zoomIn(1);
}

void MainWindow::zoomOut()
{
    documentBrowser_->zoomOut(1);
}

void MainWindow::updateHistoryActions()
{
    backAction_->setEnabled(historyIndex_ > 0);
    forwardAction_->setEnabled(historyIndex_ >= 0 && historyIndex_ + 1 < history_.size());
}

void MainWindow::updateSearchSummary(const QString &filter)
{
    if (filter.isEmpty()) {
        searchSummary_->setText(QStringLiteral("%1 个类文档 · %2 个模块").arg([this] {
            int count = 0;
            for (const DocumentEntry &entry : documents_)
                count += entry.isClass;
            return count;
        }()).arg([this] {
            QSet<QString> modules;
            for (const DocumentEntry &entry : documents_)
                if (entry.isClass)
                    modules.insert(entry.module);
            return modules.size();
        }()));
        return;
    }

    int matches = 0;
    for (const DocumentEntry &entry : documents_)
        matches += entry.searchText.contains(filter, Qt::CaseInsensitive);
    searchSummary_->setText(QStringLiteral("找到 %1 个匹配文档").arg(matches));
}

void MainWindow::selectTreePath(const QString &path)
{
    if (path.isEmpty() || !treeItems_.contains(path))
        return;
    QTreeWidgetItem *item = treeItems_.value(path);
    navigationTree_->blockSignals(true);
    navigationTree_->setCurrentItem(item);
    navigationTree_->scrollToItem(item, QAbstractItemView::PositionAtCenter);
    navigationTree_->blockSignals(false);
}

QString MainWindow::readUtf8File(const QString &path)
{
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly))
        return {};
    return QString::fromUtf8(file.readAll());
}

QString MainWindow::markdownTitle(const QString &markdown, const QString &fallback)
{
    QString title = firstLine(markdown);
    if (title.startsWith(QLatin1Char('#'))) {
        title.remove(0, 1);
        title = title.trimmed();
    }
    title.replace(QStringLiteral(" 类索引"), QString());
    return title.isEmpty() ? fallback : title;
}

QString MainWindow::markdownModule(const QString &markdown, const QString &fallback)
{
    const QStringList lines = markdown.split(QLatin1Char('\n'));
    for (const QString &line : lines) {
        const QString trimmed = line.trimmed();
        if (trimmed.startsWith(QLatin1Char('>')) && trimmed.contains(QStringLiteral("·"))) {
            const QStringList parts = trimmed.mid(1).split(QStringLiteral("·"));
            if (parts.size() >= 2)
                return parts.last().trimmed();
        }
    }
    const QString title = firstLine(markdown);
    if (title.endsWith(QStringLiteral("类索引")))
        return title.left(title.size() - 3).trimmed();
    return fallback;
}

QString MainWindow::cleanPath(const QString &path)
{
    return QDir::cleanPath(QFileInfo(path).absoluteFilePath());
}

bool MainWindow::isWithinDocumentDirectory(const QString &path) const
{
    const QString root = cleanPath(documentDirectory_);
    const QString target = cleanPath(path);
    return target.compare(root, Qt::CaseInsensitive) == 0
        || target.startsWith(root + QDir::separator(), Qt::CaseInsensitive);
}

int MainWindow::documentIndex(const QString &path) const
{
    return documentIndexes_.value(cleanPath(path), -1);
}
