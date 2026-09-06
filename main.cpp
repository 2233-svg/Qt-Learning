#include "MainWindow.h"

#include <QCoreApplication>
#include <QGuiApplication>
#include <QApplication>
#include <QToolBar>
#include <QWindow>
//QCoreApplication: 为非GUI应用程序提供主事件循环
//                  处理和分发来自操作系统和其他源的所有事件
//                  处理应用程序的初始化与终止
//                  处理系统范围和应用程序范围的设置
//QGuiApplication: 为GUI应用程序提供主事件循环
//QApplication: 为Qt Widget模块的应用程序提供主事件循环
  //继承关系：
  //        QObject《-QCoreApplication《-QGuiApplication《-QApplication

//int main(int argc, char* argv[])//argc：表示传递给程序的参数数量，包括程序本身的名称
//								//argv：包含了每一个传递给程序的参数
//{
//	QCoreApplication a(argc,argv);//进入主事件循环并等待直到调用exec（）
//
//	return a.exec();
//}

//int main(int argc, char* argv[])//argc：表示传递给程序的参数数量，包括程序本身的名称
//								//argv：包含了每一个传递给程序的参数
//{
//	QGuiApplication a(argc, argv);//进入主事件循环并等待直到调用exec（）
//
//	QWindow window;
//	window.show();
//
//	return a.exec();
//}

int main(int argc, char* argv[])//argc：表示传递给程序的参数数量，包括程序本身的名称
								//argv：包含了每一个传递给程序的参数
{
	QApplication a(argc,argv);//进入主事件循环并等待直到调用exec（）

	QMainWindow window;
	window.show();

	return a.exec();
}