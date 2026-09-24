#include "MyQwidgets.h"

#include <QLabel>
#include <QThread>
#include <QVBoxLayout>
#include <QWidget>

MyQwidgets::MyQwidgets(QWidget* parent)
    : QMainWindow(parent)
{
    auto* widget = new QWidget(this);
    auto* layout = new QVBoxLayout(widget);

    lab = new QLabel(QStringLiteral("正在计算..."), widget);
    layout->addWidget(lab);

    setCentralWidget(widget);
    resize(320, 180);
}

void Worker::doWork(int n)
{
    int sum = 0;
    while (sum != 10)
    {
        for (int i = 1; i <= n; ++i) {
            sum += i;
            QThread::msleep(1);
        }
        emit resultReady(sum);
    }
}

void MyQwidgets::test()
{
    QThread* thread = new QThread;
    Worker* worker = new Worker;
    worker->moveToThread(thread);

    connect(thread, &QThread::started, worker, [worker] {
        worker->doWork(100);
        });
    connect(worker, &Worker::resultReady, this, [this](int sum) {
        lab->setText(QString("结果：%1").arg(sum));  // 主线程更新 UI
        });
    connect(worker, &Worker::resultReady, thread, &QThread::quit);
    connect(thread, &QThread::finished, worker, &QObject::deleteLater);
    connect(thread, &QThread::finished, thread, &QObject::deleteLater);

    thread->start();
}
