#pragma once

#include <QWidget>
#include <QList>
#include <QPointer>

class QAction;
class QMenu;

class MainMenuBar : public QWidget
{
	Q_OBJECT
public:
	explicit MainMenuBar(QWidget* parent = nullptr);
    ~MainMenuBar() override;

    QMenu* addMenu(const QString &title);
    void addMenu(QMenu* menu);
    QList<QAction*> actions() const;
    void updateIndex(const QPoint& pos);

    // ---------- 文件 ----------
    QAction* actNew = nullptr;
    QAction* actOpen = nullptr;
    QAction* actSave = nullptr;
    QAction* actSaveAs = nullptr;
    QAction* actClose = nullptr;
    QAction* actExit = nullptr;

    // ---------- 编辑 ----------
    QAction* actUndo = nullptr;
    QAction* actRedo = nullptr;
    QAction* actCut = nullptr;
    QAction* actCopy = nullptr;
    QAction* actPaste = nullptr;
    QAction* actDelete = nullptr;
    QAction* actSelectAll = nullptr;
    QAction* actFind = nullptr;

    // ---------- 视图 ----------
    QAction* actToggleToolBar = nullptr;
    QAction* actToggleDockLeft = nullptr;
    QAction* actToggleDockRight = nullptr;
    QAction* actToggleStatusBar = nullptr;
    QAction* actFullScreen = nullptr;

    // ---------- 帮助 ----------
    QAction* actHelp = nullptr;
    QAction* actAbout = nullptr;
    QAction* actAboutQt = nullptr;

    // 最近打开文件子菜单（外部可动态填充）
    QMenu* recentMenu = nullptr;

    QSize sizeHint() const override;
    QSize minimumSizeHint() const override;

    signals:
        void status_tip_hovered(const QString &tip);
protected:
    void paintEvent(QPaintEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;
    void leaveEvent(QEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;

private:
    struct Item
    {
        QString title;
        QString plain;
        QMenu* menu = nullptr;
        QRect rect;
    };

    void createFileMenu();
    void createEditMenu();
    void createViewMenu();
    void createHelpMenu();

    QAction* makeAction(QMenu* menu, const QString &text, const QKeySequence &shortcut = QKeySequence(), const QString &statusTip = QString(), bool checkable = false);
	
    void recomputeLayout();
    int indexAt(const QPoint& pos) const;
    void openMenuAt(int index);

    QList<Item> m_items;
    int m_hoverIndex = -1;
    int m_activeIndex = -1;
    int m_hintWidth = 200;
    QPointer<QMenu> m_openMenu;
    QMetaObject::Connection m_menuConn;
};
