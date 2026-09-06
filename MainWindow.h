#pragma once

#include <QHash>
#include <QStringList>
#include <QVector>

#include <QMainWindow>

class QLabel;
class QAction;
class QLineEdit;
class QTextBrowser;
class QTreeWidget;
class QTreeWidgetItem;
class QUrl;

class MainWindow final : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private slots:
    void chooseDocumentDirectory();
    void rescanDocuments();
    void filterDocuments(const QString &text);
    void activateTreeItem(QTreeWidgetItem *item, int column);
    void followLink(const QUrl &url);
    void goBack();
    void goForward();
    void goHome();
    void zoomIn();
    void zoomOut();

private:
    struct DocumentEntry
    {
        QString title;
        QString module;
        QString path;
        QString markdown;
        QString searchText;
        bool isClass = false;
    };

    void setupUi();
    void setDocumentDirectory(const QString &directory);
    void buildDocumentIndex();
    void buildNavigation(const QString &filter = {});
    void openDocument(const QString &path, bool addToHistory = true);
    void loadCurrentDocument();
    void updateHistoryActions();
    void updateSearchSummary(const QString &filter);
    void selectTreePath(const QString &path);

    static QString readUtf8File(const QString &path);
    static QString markdownTitle(const QString &markdown, const QString &fallback);
    static QString markdownModule(const QString &markdown, const QString &fallback);
    static QString cleanPath(const QString &path);
    bool isWithinDocumentDirectory(const QString &path) const;
    int documentIndex(const QString &path) const;

    QString documentDirectory_;
    QVector<DocumentEntry> documents_;
    QHash<QString, int> documentIndexes_;
    QHash<QString, QTreeWidgetItem *> treeItems_;
    QStringList history_;
    int historyIndex_ = -1;
    QString currentPath_;

    QLineEdit *searchEdit_ = nullptr;
    QLabel *searchSummary_ = nullptr;
    QLabel *documentTitle_ = nullptr;
    QLabel *documentPath_ = nullptr;
    QLabel *statusLabel_ = nullptr;
    QTreeWidget *navigationTree_ = nullptr;
    QTextBrowser *documentBrowser_ = nullptr;
    QAction *backAction_ = nullptr;
    QAction *forwardAction_ = nullptr;
};
