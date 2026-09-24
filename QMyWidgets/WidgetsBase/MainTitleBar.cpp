#include "MainTitleBar.h"

#include <QFontMetrics>
#include <QIcon>
#include <QMouseEvent>
#include <QPainter>
#include <QPainterPath>
#include <QResizeEvent>

MainTitleBar::MainTitleBar(QWidget* parent)
    : QWidget(parent)
{
    setFixedHeight(kTitleHeight);
    setMouseTracking(true);

    if (QWidget* hostWindow = window()) {
        connect(hostWindow, &QWidget::windowTitleChanged, this,
            [this](const QString&) { update(); });
        connect(hostWindow, &QWidget::windowIconChanged, this,
            [this](const QIcon&) { update(); });
    }
}

QSize MainTitleBar::sizeHint() const
{
    return {minimumSizeHint().width(), kTitleHeight};
}

void MainTitleBar::paintEvent(QPaintEvent* event)
{
    Q_UNUSED(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    QPainterPath backgroundPath;
    constexpr qreal radius = 6.0;
    backgroundPath.moveTo(0, height());
    backgroundPath.lineTo(0, radius);
    backgroundPath.quadTo(0, 0, radius, 0);
    backgroundPath.lineTo(width() - radius, 0);
    backgroundPath.quadTo(width(), 0, width(), radius);
    backgroundPath.lineTo(width(), height());
    backgroundPath.closeSubpath();
    painter.drawPath(backgroundPath);

    QPixmap titlePix = QIcon(":/resources/title.png").pixmap(rect().size());
    painter.drawPixmap(rect(),titlePix);

    const QWidget* hostWindow = window();
    const QString title = hostWindow ? hostWindow->windowTitle() : windowTitle();
    const QIcon icon = hostWindow ? hostWindow->windowIcon() : windowIcon();

    painter.setPen(Qt::black);
    const QRect titleRect(40, 0, width() - 3 * kButtonWidth - 40, height());
    const QFontMetrics fontMetrics(painter.font());
    const int baseline =
        titleRect.top() +
        (titleRect.height() - fontMetrics.height()) / 2 +
        fontMetrics.ascent();
    painter.drawText(titleRect.left(), baseline, title);

    const QRect iconRect(rect().left()+8, rect().top()+3, 24, 24);
    painter.drawPixmap(iconRect, icon.pixmap(iconRect.size()));

    paintButton(painter, Button::Minimize, buttonRect(Button::Minimize));
    paintButton(painter, Button::Maximize, buttonRect(Button::Maximize));
    paintButton(painter, Button::Close, buttonRect(Button::Close));
}

void MainTitleBar::mousePressEvent(QMouseEvent* event)
{
    if (event->button() != Qt::LeftButton) {
        QWidget::mousePressEvent(event);
        return;
    }

    const Button button = buttonAt(event->position().toPoint());
    if (button != Button::None) {
        m_pressedButton = button;
        update();
        event->accept();
        return;
    }

    QWidget* hostWindow = window();
    if (hostWindow && !hostWindow->isMaximized()) {
        m_dragPosition =
            event->globalPosition().toPoint() - hostWindow->frameGeometry().topLeft();
        m_dragging = true;
        event->accept();
        return;
    }

    QWidget::mousePressEvent(event);
}

void MainTitleBar::mouseMoveEvent(QMouseEvent* event)
{
    const Button hoveredButton = buttonAt(event->position().toPoint());
    if (hoveredButton != m_hoveredButton) {
        m_hoveredButton = hoveredButton;
        update();
    }

    QWidget* hostWindow = window();
    if (m_dragging && hostWindow && (event->buttons() & Qt::LeftButton)) {
        hostWindow->move(event->globalPosition().toPoint() - m_dragPosition);
        event->accept();
        return;
    }

    QWidget::mouseMoveEvent(event);
}

void MainTitleBar::mouseReleaseEvent(QMouseEvent* event)
{
    if (event->button() == Qt::LeftButton) {
        const Button button = buttonAt(event->position().toPoint());
        if (button != Button::None && button == m_pressedButton) {
            if (QWidget* hostWindow = window()) {
                switch (button) {
                case Button::Minimize:
                    hostWindow->showMinimized();
                    break;
                case Button::Maximize:
                    toggleMaximized();
                    break;
                case Button::Close:
                    hostWindow->close();
                    break;
                case Button::None:
                    break;
                }
            }
        }

        m_pressedButton = Button::None;
        m_dragging = false;
        update();
        event->accept();
        return;
    }

    QWidget::mouseReleaseEvent(event);
}

void MainTitleBar::mouseDoubleClickEvent(QMouseEvent* event)
{
    if (event->button() == Qt::LeftButton &&
        buttonAt(event->position().toPoint()) == Button::None) {
        toggleMaximized();
        event->accept();
        return;
    }

    QWidget::mouseDoubleClickEvent(event);
}

void MainTitleBar::leaveEvent(QEvent* event)
{
    m_hoveredButton = Button::None;
    update();
    QWidget::leaveEvent(event);
}

void MainTitleBar::resizeEvent(QResizeEvent* event)
{
    updateMenuBarGeometry();
    QWidget::resizeEvent(event);
}

QRect MainTitleBar::buttonRect(Button button) const
{
    switch (button) {
    case Button::Close:
        return {width() - kButtonWidth, kTitleHeight / 3-3, kButtonWidth, kTitleHeight/2+4};
    case Button::Maximize:
        return {width() - 2 * kButtonWidth, kTitleHeight / 3-3, kButtonWidth, kTitleHeight/2+4};
    case Button::Minimize:
        return {width() - 3 * kButtonWidth, kTitleHeight / 3-3, kButtonWidth, kTitleHeight/2+4};
    case Button::None:
        return {};
    }

    return {};
}

MainTitleBar::Button MainTitleBar::buttonAt(const QPoint& position) const
{
    if (buttonRect(Button::Close).contains(position)) {
        return Button::Close;
    }
    if (buttonRect(Button::Maximize).contains(position)) {
        return Button::Maximize;
    }
    if (buttonRect(Button::Minimize).contains(position)) {
        return Button::Minimize;
    }
    return Button::None;
}

void MainTitleBar::paintButton(
    QPainter& painter, Button button, const QRect& rect) const
{
    QString resourcePath;
    switch (button) {
    case Button::Minimize:
        resourcePath = QStringLiteral(":/resources/minimize.png");
        break;
    case Button::Maximize:
        resourcePath = QStringLiteral(":/resources/maximize.png");
        break;
    case Button::Close:
        resourcePath = QStringLiteral(":/resources/close.png");
        break;
    case Button::None:
        return;
    }

    if (m_hoveredButton == button) {
        painter.fillRect(rect, QColor(255, 255, 255, 35));
    }
    if (m_pressedButton == button) {
        painter.fillRect(rect, QColor(0, 0, 0, 35));
    }

    painter.drawPixmap(rect, QIcon(resourcePath).pixmap(rect.size()));
}

void MainTitleBar::toggleMaximized()
{
    if (QWidget* hostWindow = window()) {
        if (hostWindow->isMaximized()) {
            hostWindow->showNormal();
        } else {
            hostWindow->showMaximized();
        }
        update();
    }
}

void MainTitleBar::insertMenuBar(MainMenuBar* menu_bar)
{
    if (!menu_bar) {
        return;
    }

    m_menuBar = menu_bar;
    m_menuBar->setParent(this);
    m_menuBar->setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);

    // 让菜单栏“融进”标题栏：背景透明、去掉多余内边距
    m_menuBar->setStyleSheet(R"(
        QMenuBar {
            background: transparent;
            padding-left: 6px;
        }
        QMenuBar::item {
            background: transparent;
            padding: 4px 10px;
            border-radius: 4px;
        }
        QMenuBar::item:selected { background: rgba(255,255,255,0.15); }
        QMenuBar::item:pressed  { background: rgba(255,255,255,0.25); }
    )");

    m_menuBar->adjustSize();
    updateMenuBarGeometry();
    m_menuBar->show();
    m_menuBar->raise();
}

void MainTitleBar::updateMenuBarGeometry()
{
    if (!m_menuBar) {
        return;
    }

    const QSize menuSize = m_menuBar->sizeHint();
    m_menuBar->resize(menuSize);

    const int x = qMax(0, (width() - menuSize.width()) / 3);
    const int y = qMax(0, (height() - menuSize.height()) / 2);
    m_menuBar->move(x, y);
}
