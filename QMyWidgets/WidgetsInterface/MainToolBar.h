//#pragma once
//
//#include <QToolBar>
//#include <initializer_list>//统一支持列表初始化列表
//
//class QAction;
//
//class MainToolBar : public QToolBar
//{
//	Q_OBJECT
//public:
//	explicit MainToolBar(const QString& title = QString(), QWidget* parent = nullptr);
//	// ---------- 链式便捷 API ----------
//	MainToolBar* addActs(std::initializer_list<QAction*> actions);//批量添加
//	MainToolBar* addSeparatorLine();                                // 竖线分隔符
//	MainToolBar* addGap(int px = 8);                                // 固定宽度空白
//	MainToolBar* addSpring();                                       // 弹性空白（右侧对齐用）
//
//	// ---------- 样式 ----------
//	void applyDarkStyle();
//	void applyLightStyle();
//
//protected:
//	// 禁用 QToolBar 默认的右键“工具栏列表”菜单（改由“视图”菜单统一管理）
//	void contextMenuEvent(QContextMenuEvent* e) override;
//
//private:
//	void initDefaults();
//};
