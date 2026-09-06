#include "MainWindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication application(argc, argv);
    application.setOrganizationName(QStringLiteral("QtDocViewer"));
    application.setApplicationName(QStringLiteral("QtDocViewer"));

    MainWindow window;
    window.show();

    return application.exec();
}
