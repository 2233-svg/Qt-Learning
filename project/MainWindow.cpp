#include "MainWindow.h"

#include "MainTitleBar.h"

#include <QIcon>
#include <QPainter>
#include <QPainterPath>
#include <QVBoxLayout>
#include <QWidget>
#include <QDebug>

MainWindow::MainWindow(QWidget* parent)
    : QMainWindow(parent)
{
    setWindowTitle(QStringLiteral("GenSine Start"));
    setWindowFlag(Qt::FramelessWindowHint);
    setAttribute(Qt::WA_TranslucentBackground);
    setWindowIcon(QIcon(QStringLiteral(":/resources/logo.jpg")));
    setMinimumSize(600, 400);

    auto* centralWidget = new QWidget(this);
    auto* layout = new QVBoxLayout(centralWidget);
    layout->setContentsMargins(1, 1, 1, 1);
    layout->setSpacing(0);

    m_titleBar = new MainTitleBar(centralWidget);
    m_menu_bar = new MainMenuBar(m_titleBar);
    m_titleBar->insertMenuBar(m_menu_bar);
    layout->addWidget(m_titleBar);
    layout->addStretch();

    setCentralWidget(centralWidget);
    connectSign();
}

void MainWindow::paintEvent(QPaintEvent* event)
{
    Q_UNUSED(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    const QRect backgroundRect = rect().adjusted(0, 0, 0, 0);
    QPainterPath backgroundPath;
    backgroundPath.addRoundedRect(backgroundRect, 6, 6);

    painter.fillPath(backgroundPath, Qt::white);
    painter.setPen(QPen(Qt::black, 1));
    painter.drawPath(backgroundPath);
}

void MainWindow::connectSign()
{
    connect(m_menu_bar->actNew, &QAction::triggered, this, &MainWindow::onNewFile);
    connect(m_menu_bar->actOpen, &QAction::triggered, this, &MainWindow::onOpenFile);
    connect(m_menu_bar->actSave, &QAction::triggered, this, &MainWindow::onSaveFile);
    connect(m_menu_bar->actExit, &QAction::triggered, this, &QWidget::close);
}

void MainWindow::onNewFile()
{
    qDebug() << "New file";
}

void MainWindow::onOpenFile()
{
    qDebug() << "Open file";
}

void MainWindow::onSaveFile()
{
    qDebug() << "Save file";
}
