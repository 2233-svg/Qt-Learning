#pragma once

#include <QPoint>
#include <QRect>
#include <QSize>
#include <QWidget>

#include "MainMenuBar.h"

class QEvent;
class QMouseEvent;
class QPainter;
class QPaintEvent;
class QResizeEvent;

class MainTitleBar final : public QWidget
{
public:
    explicit MainTitleBar(QWidget* parent = nullptr);

    QSize sizeHint() const override;
    void insertMenuBar(MainMenuBar* menu_bar);
    auto titleRect() const -> QRect;
protected:
    void paintEvent(QPaintEvent* event) override;
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;
    void mouseDoubleClickEvent(QMouseEvent* event) override;
    void leaveEvent(QEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;

private:
    enum class Button
    {
        None,
        Minimize,
        Maximize,
        Close
    };

    QRect buttonRect(Button button) const;
    Button buttonAt(const QPoint& position) const;
    void paintButton(QPainter& painter, Button button, const QRect& rect) const;
    void toggleMaximized();
    void updateMenuBarGeometry();

    static constexpr int kTitleHeight = 30;
    static constexpr int kButtonWidth = 24;

    QPoint m_dragPosition;
    bool m_dragging = false;
    Button m_hoveredButton = Button::None;
    Button m_pressedButton = Button::None;
    MainMenuBar* m_menuBar = nullptr;
};
