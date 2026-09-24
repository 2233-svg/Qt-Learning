#pragma once

#include <QMainWindow>

class QLabel;

class Worker final : public QObject
{
    Q_OBJECT
public slots:
    void doWork(int n);

signals:
    void resultReady(int sum);
};

class MyQwidgets final : public QMainWindow
{
    Q_OBJECT

public:
    explicit MyQwidgets(QWidget* parent = nullptr);

public slots:
    void test();

private:
    QLabel* lab = nullptr;
};
