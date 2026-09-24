#pragma once

#include <QMainWindow>

#include "MainMenuBar.h"

class MainTitleBar;

class MainWindow final : public QMainWindow
{
public:
    explicit MainWindow(QWidget* parent = nullptr);
    void connectSign();
    void onNewFile();
    void onOpenFile();
    void onSaveFile();
protected:
    void paintEvent(QPaintEvent* event) override;

private:
    MainTitleBar* m_titleBar = nullptr;
    MainMenuBar* m_menu_bar = nullptr;
};
