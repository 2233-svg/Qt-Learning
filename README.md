# Qt Assistant Viewer

本项目是 Qt Markdown 文档查看器的源码项目。

## 目录说明

- `main.cpp`、`MainWindow.*`：查看器源码。
- `Qt6.11.1_ClassDocs/`：随源码项目携带的 Qt 类文档。
- `qtAPI知识/`：Qt API 知识库项目的 Markdown 文档和生成脚本。
- `marktext-win-x64-0.19.1/`：双击文档时调用的 MarkText。
- `dist/Qt-assisiant/`：本项目自己的可运行程序输出目录。
- `build/`、`out/`、`.vs/`：旧的或本地生成目录，忽略提交。

构建后还会复制一份运行包到：

`D:/笔记/qtAPI知识/_viewer/Qt-assisiant-viewer`

这份副本用于浏览 `D:/笔记/qtAPI知识` 知识库项目。
