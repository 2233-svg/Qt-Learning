#include "MainWindow.h"

#include <QString>
#include <QPainter>
#include <QPushButton>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle(QStringLiteral("GenSine Start"));
    setWindowFlags(
        Qt::Window |
        Qt::ExpandedClientAreaHint |
        Qt::NoTitleBarBackgroundHint);
    resize(800, 600);
}
void MainWindow::paintEvent(QPaintEvent* event)
{
    QPainter painter(this);
    QRect titleRect(0,0,804,30);

    painter.setPen(Qt::black);
    painter.setBrush(Qt::white);
    painter.drawRoundedRect(titleRect,4,4);
}
