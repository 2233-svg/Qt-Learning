//#include "MainToolBar.h"
//
//#include <QAction>
//#include <QWidget>
//#include <QSizePolicy>
//#include <QContextMenuEvent>
//#include <QLayout>
//
//MainToolBar::MainToolBar(const QString& title, QWidget* parent)
//	:QToolBar(title, parent)
//{
//	initDefaults();
//	applyDarkStyle();
//}
//
//void MainToolBar::initDefaults()
//{
//    setObjectName(QStringLiteral("AppToolBar"));
//    setMovable(true);                                        // 允许拖动换位置
//    setFloatable(true);                                      // 允许脱离主窗口浮动
//    setAllowedAreas(Qt::TopToolBarArea | Qt::BottomToolBarArea);
//    setIconSize(QSize(18, 18));
//    setToolButtonStyle(Qt::ToolButtonIconOnly);              // 只显示图标
//    setContextMenuPolicy(Qt::PreventContextMenu);            // 显隐交给“视图”菜单
//    setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
//    layout()->setSpacing(2);
//    layout()->setContentsMargins(4, 2, 4, 2);
//}
