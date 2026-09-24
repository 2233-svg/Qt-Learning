#include <MainMenuBar.h>

#include <QMenu>
#include <QAction>
#include <QPainter>
#include <QMouseEvent>
#include <QApplication>
#include <QFontMetrics>

namespace
{
	constexpr int kHeight = 30;
	constexpr int KPadLeft = 8;
	constexpr int KItemPadX = 12;
	constexpr int KMarginY = 4;
}

MainMenuBar::MainMenuBar(QWidget* parent)
	:QWidget(parent)
{
	setObjectName(QStringLiteral("MainMenuBar"));

	setFixedHeight(kHeight);
	setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
	setMouseTracking(true);
	setFocusPolicy(Qt::StrongFocus);
	
	// 允许在菜单栏空白处拖动窗口（配合无边框标题栏更自然）
	// 由主窗口自行决定是否处理，这里只保证菜单栏可交互
	createFileMenu();
	createEditMenu();
	createViewMenu();
	createHelpMenu();
}

MainMenuBar::~MainMenuBar() = default;

QMenu* MainMenuBar::addMenu(const QString& title)
{
	auto* menu = new QMenu(title, this);
	Item it;
	it.title = title;
	it.plain = QString(title);
	it.plain.remove(QLatin1Char('&'));
	it.menu = menu;
	m_items.append(it);

	// 弹出菜单悬停 → 转发 statusTip
	connect(menu, &QMenu::hovered, this, [this](QAction* a) {
		emit status_tip_hovered(a ? a->statusTip() : QString());
		});

	recomputeLayout();
	update();
	return menu;
}

void MainMenuBar::addMenu(QMenu* menu)
{
	if (!menu)
	{
		return;
	}
	Item it;
	it.title = menu->title();
	it.plain = it.title; it.plain.remove(QLatin1Char('&'));
	it.menu = menu;
	menu->setParent(this);
	m_items.append(it);
	recomputeLayout();
	update();
}

QList<QAction*> MainMenuBar::actions() const
{
	QList<QAction*> r;
	for (const auto &it:m_items)
	{
		if (it.menu)
		{
			r.append(it.menu->menuAction());
		}
	}
	return r;
}

void MainMenuBar::recomputeLayout()
{
	QFontMetrics fm(font());
	int x = KPadLeft;
	const int h = height();
	for (auto &it:m_items)
	{
		const int w = fm.horizontalAdvance(it.plain) + 2 * KItemPadX;
		it.rect = QRect(x, KMarginY, w, h - 2 * KMarginY);
		x += w;
	}
	m_hintWidth = x + KPadLeft;
}

int MainMenuBar::indexAt(const QPoint& pos) const
{
	for (int i = 0; i < m_items.size(); ++i)
	{
		if (m_items[i].rect.contains(pos))
		{
			return i;
		}
	}
	return -1;
}

void MainMenuBar::updateIndex(const QPoint& pos)
{
	int idx = indexAt(pos);
	m_activeIndex = idx;
}

void MainMenuBar::paintEvent(QPaintEvent* event)
{
	QPainter p(this);
	p.setRenderHint(QPainter::Antialiasing);
	p.setFont(font());

	for (int i = 0; i < m_items.size(); ++i)
	{
		const Item& it = m_items[i];
		const bool lit = (i == m_activeIndex) || (i == m_hoverIndex);
		if (lit)
		{
			p.setPen(Qt::NoPen);
			p.setBrush(QColor(255,255,255,36));
			p.drawRoundedRect(it.rect,4,4);
		}
		p.setPen(QColor("#e0e0e0"));
		p.drawText(it.rect, Qt::AlignCenter, it.plain);
	}
}

void MainMenuBar::mousePressEvent(QMouseEvent* event)
{
	if (event->button() != Qt::LeftButton)
	{
		QWidget::mousePressEvent(event);
		return;
	}
	const int idx = indexAt(event->pos());
	if (idx != m_activeIndex)
	{
		updateIndex(event->pos());
	}
	if (idx < 0)
	{
		m_hoverIndex = idx;
		update();
		return;
	}
	if (idx == m_activeIndex)
	{
		if (m_openMenu)
		{
			m_openMenu->hide();
		}
		else
		{
			openMenuAt(idx);
		}
	}
	event->accept();
}

void MainMenuBar::mouseMoveEvent(QMouseEvent* event)
{
	const int idx = indexAt(event->pos());
	
	if (idx != m_hoverIndex )
	{
		m_hoverIndex = idx;
		update();
	}
	
	if (m_activeIndex >= 0 && idx >= 0 && idx != m_activeIndex)
	{
		openMenuAt(idx);// 已展开时滑到别的菜单，切换
	}
	QWidget::mouseMoveEvent(event);
}

void MainMenuBar::mouseReleaseEvent(QMouseEvent* event)
{
	event->accept();
}

void MainMenuBar::leaveEvent(QEvent* event)
{
	if (m_activeIndex < 0)
	{
		m_hoverIndex = -1;
		update();
	}
	QWidget::leaveEvent(event);
}

void MainMenuBar::resizeEvent(QResizeEvent* event)
{
	QWidget::resizeEvent(event);
	recomputeLayout();
}

void MainMenuBar::openMenuAt(int index)
{
	if (index < 0 || index > m_items.size())
	{
		return;
	}
	Item& it = m_items[index];
	if (!it.menu)
	{
		return;
	}
	if (m_openMenu && m_openMenu != it.menu)
	{
		m_openMenu->hide();
		m_activeIndex = index;
		update();
		m_openMenu = it.menu;
	}
	if (m_menuConn)
	{
		QObject::disconnect(m_menuConn);
		m_menuConn = connect(it.menu,&QMenu::aboutToHide,this,[this]
		{
				m_activeIndex = -1;
				m_openMenu = nullptr;
				update();
		});

	}
	it.menu->popup(mapToGlobal(QPoint(it.rect.left(), it.rect.bottom() +1)));
}

QSize MainMenuBar::sizeHint() const
{
	return {m_hintWidth, kHeight};
}

QSize MainMenuBar::minimumSizeHint() const
{
	return sizeHint();
}

QAction* MainMenuBar::makeAction(QMenu* menu, const QString& text, const QKeySequence& shortcut, const QString& statusTip, bool checkable)
{
	QAction* act = menu->addAction(text);
	if (!shortcut.isEmpty())
		act->setShortcut(shortcut);
	if (!statusTip.isEmpty())
		act->setStatusTip(statusTip);   // 会自动显示到 QStatusBar
	if (checkable)
		act->setCheckable(true);
	return act;
}

/* ---------------- 文件(&F) ---------------- */
void MainMenuBar::createFileMenu()
{
	QMenu* fileMenu = addMenu(tr("文件(&F)"));

	actNew = makeAction(fileMenu, tr("新建(&N)"),
		QKeySequence::New,
		tr("新建文件"));
	actOpen = makeAction(fileMenu, tr("打开(&O)..."),
		QKeySequence::Open,
		tr("打开已有文件"));

	recentMenu = fileMenu->addMenu(tr("最近打开(&R)"));

	QAction* emptyAct = recentMenu->addAction(tr("(空)"));
	emptyAct->setEnabled(false);
	fileMenu->addSeparator();

	actSave = makeAction(fileMenu, tr("保存(&S)"),
		QKeySequence::Save,
		tr("保存当前文件"));

	actSaveAs = makeAction(fileMenu, tr("另存为(&A)..."),
		QKeySequence::SaveAs,
		tr("将当前文件另存"));

	actClose = makeAction(fileMenu, tr("关闭(&C)"),
		QKeySequence::Close,
		tr("关闭当前文件"));

	fileMenu->addSeparator();

	actExit = makeAction(fileMenu, tr("退出(&X)"),
		QKeySequence(QStringLiteral("Ctrl+Q")),
		tr("退出程序"));
}

/* ---------------- 编辑(&E) ---------------- */
void MainMenuBar::createEditMenu()
{
	QMenu* editMenu = addMenu(tr("编辑(&E)"));

	actUndo = makeAction(editMenu, tr("撤销(&U)"),
		QKeySequence::Undo,
		tr("撤销上一步操作"));
	actRedo = makeAction(editMenu, tr("重做(&R)"),
		QKeySequence::Redo,
		tr("重做被撤销的操作"));

	editMenu->addSeparator();

	actCut = makeAction(editMenu, tr("剪切(&T)"), QKeySequence::Cut, tr("剪切到剪贴板"));
	actCopy = makeAction(editMenu, tr("复制(&C)"), QKeySequence::Copy, tr("复制到剪贴板"));
	actPaste = makeAction(editMenu, tr("粘贴(&P)"), QKeySequence::Paste, tr("从剪贴板粘贴"));
	actDelete = makeAction(editMenu, tr("删除(&D)"), QKeySequence::Delete, tr("删除选中内容"));

	editMenu->addSeparator();

	actSelectAll = makeAction(editMenu, tr("全选(&A)"),
		QKeySequence::SelectAll,
		tr("选中全部内容"));

	actFind = makeAction(editMenu, tr("查找(&F)..."),
		QKeySequence::Find,
		tr("在当前文档中查找"));
}

/* ---------------- 视图(&V) ---------------- */
void MainMenuBar::createViewMenu()
{
	QMenu* viewMenu = addMenu(tr("视图(&V)"));

	actToggleToolBar = makeAction(viewMenu, tr("工具栏"),
		QKeySequence(),
		tr("显示/隐藏工具栏"),
		/*checkable=*/true);
	actToggleToolBar->setChecked(true);

	viewMenu->addSeparator();

	actToggleDockLeft = makeAction(viewMenu, tr("左侧面板"),
		QKeySequence(), tr("显示/隐藏左侧停靠窗口"), true);
	actToggleDockRight = makeAction(viewMenu, tr("右侧面板"),
		QKeySequence(), tr("显示/隐藏右侧停靠窗口"), true);
	actToggleDockLeft->setChecked(true);
	actToggleDockRight->setChecked(true);

	viewMenu->addSeparator();

	actToggleStatusBar = makeAction(viewMenu, tr("状态栏"),
		QKeySequence(), tr("显示/隐藏状态栏"), true);
	actToggleStatusBar->setChecked(true);

	actFullScreen = makeAction(viewMenu, tr("全屏(&F)"),
		QKeySequence(QStringLiteral("F11")),
		tr("切换全屏显示"),
		/*checkable=*/true);
}

/* ---------------- 帮助(&H) ---------------- */
void MainMenuBar::createHelpMenu()
{
	QMenu* helpMenu = addMenu(tr("帮助(&H)"));

	actHelp = makeAction(helpMenu, tr("使用手册(&M)"),
		QKeySequence::HelpContents,
		tr("打开使用手册"));

	helpMenu->addSeparator();

	actAbout = makeAction(helpMenu, tr("关于(&A)..."),
		QKeySequence(),
		tr("关于本软件"));
	actAbout->setMenuRole(QAction::AboutRole);

	actAboutQt = makeAction(helpMenu, tr("关于 Qt(&Q)..."),
		QKeySequence(),
		tr("关于 Qt 版本信息"));
	actAboutQt->setMenuRole(QAction::AboutQtRole);

	// “关于 Qt”直接连到 Qt 内置对话框
	connect(actAboutQt, &QAction::triggered,
		qApp, &QApplication::aboutQt);
}
