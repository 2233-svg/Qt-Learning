# Qt OpenGL（上）：上下文、QOpenGLWidget 与基础渲染

> Qt OpenGL 提供对 OpenGL 上下文、函数加载、缓冲和着色器的 Qt 封装。Qt 6 中 `QOpenGLWidget` 位于 Qt OpenGL Widgets，`QOpenGLContext` 仍位于 Qt Gui。所有 OpenGL 资源都依赖当前上下文，生命周期和线程规则是本篇重点。

## 1. 模块和最小 QOpenGLWidget

```cmake
find_package(Qt6 REQUIRED COMPONENTS OpenGL OpenGLWidgets Widgets)
target_link_libraries(mytarget PRIVATE
    Qt6::OpenGL
    Qt6::OpenGLWidgets
    Qt6::Widgets
)
```

```cpp
#include <QOpenGLFunctions>
#include <QOpenGLWidget>

class ColorWidget : public QOpenGLWidget,
                    protected QOpenGLFunctions
{
protected:
    void initializeGL() override
    {
        initializeOpenGLFunctions();
        glClearColor(0.08f, 0.10f, 0.14f, 1.0f);
    }

    void paintGL() override
    {
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    }

    void resizeGL(int width, int height) override
    {
        glViewport(0, 0, width, height);
    }
};
```

`initializeGL()` 在上下文创建后调用一次，适合初始化资源；`paintGL()` 每次需要重绘时调用；`resizeGL()` 更新视口和投影。不要在构造函数中调用 OpenGL 函数，因为此时上下文通常还未创建或未当前化。

## 2. QOpenGLContext 与当前上下文

OpenGL 函数只对当前线程的当前上下文有效：

```cpp
QOpenGLContext *context = QOpenGLContext::currentContext();
if (!context)
    return;

QOpenGLFunctions *functions = context->functions();
functions->glClear(GL_COLOR_BUFFER_BIT);
```

`QOpenGLWidget` 在 `initializeGL()`、`resizeGL()`、`paintGL()` 期间会自动使上下文当前。自建 `QOpenGLContext` 时使用 `makeCurrent(surface)` 和 `doneCurrent()` 成对管理。

上下文之间不能直接共享所有资源，创建时需要设置 `QOpenGLContext::setShareContext()` 或使用共享组。共享资源的删除仍必须在有效上下文中进行。

## 3. QOpenGLFunctions 与函数版本

Windows 等平台可能只在链接时提供少量 OpenGL 函数，其余函数需要运行时解析。`QOpenGLFunctions` 提供跨桌面的公共函数；需要特定版本时使用 `QOpenGLFunctions_3_3_Core` 等版本类。

```cpp
auto *f = QOpenGLContext::currentContext()->versionFunctions<
    QOpenGLFunctions_3_3_Core>();
if (!f || !f->initializeOpenGLFunctions())
    return;
```

不要在未确认上下文版本时直接调用高版本函数。桌面 OpenGL、OpenGL ES 和软件渲染的能力差异必须通过 `QSurfaceFormat` 和运行时检查处理。

## 4. QSurfaceFormat

```cpp
QSurfaceFormat format;
format.setVersion(3, 3);
format.setProfile(QSurfaceFormat::CoreProfile);
format.setDepthBufferSize(24);
format.setSamples(4);
QSurfaceFormat::setDefaultFormat(format);
```

默认格式应在创建应用窗口或 OpenGL widget 之前设置。深度缓冲、模板缓冲、MSAA 和交换行为都会影响性能和兼容性。请求的版本可能无法满足，应在上下文创建后读取 `context->format()` 确认实际格式。

## 5. QOpenGLBuffer

### 5.1 顶点缓冲

```cpp
QOpenGLBuffer vertexBuffer(QOpenGLBuffer::VertexBuffer);
vertexBuffer.create();
vertexBuffer.bind();
vertexBuffer.setUsagePattern(QOpenGLBuffer::StaticDraw);
vertexBuffer.allocate(vertices.constData(), vertices.size() * sizeof(Vertex));
vertexBuffer.release();
```

`create()`、`bind()`、`allocate()` 和 `destroy()` 都需要当前上下文。`StaticDraw`、`DynamicDraw`、`StreamDraw` 表达数据更新频率，选错会影响驱动优化。

### 5.2 映射缓冲

```cpp
if (vertexBuffer.bind()) {
    void *ptr = vertexBuffer.map(QOpenGLBuffer::WriteOnly);
    if (ptr) {
        std::memcpy(ptr, vertices.constData(), byteCount);
        vertexBuffer.unmap();
    }
    vertexBuffer.release();
}
```

`map()` 成功后必须 `unmap()`。映射失败应走备用的 `write()` 或重新分配路径，不要解引用空指针。

## 6. QOpenGLVertexArrayObject

VAO 保存顶点属性绑定状态，可减少每帧重复配置：

```cpp
vao.create();
vao.bind();
vertexBuffer.bind();
program->enableAttributeArray(0);
program->setAttributeBuffer(0, GL_FLOAT, offsetof(Vertex, position), 3,
                             sizeof(Vertex));
vao.release();
```

VAO 配置依赖当前绑定的 VBO 和 shader attribute。Core Profile 下绘制前通常必须绑定有效 VAO。

## 7. QOpenGLShaderProgram

### 7.1 顶点和片段着色器

```cpp
QOpenGLShaderProgram program;
program.addShaderFromSourceCode(QOpenGLShader::Vertex, R"(
    attribute vec3 position;
    uniform mat4 mvp;
    void main() { gl_Position = mvp * vec4(position, 1.0); }
)");
program.addShaderFromSourceCode(QOpenGLShader::Fragment, R"(
    uniform vec4 color;
    void main() { gl_FragColor = color; }
)");
program.link();
```

生产代码应检查每一步返回值和 `log()`：

```cpp
if (!program.link())
    qWarning() << program.log();
program.bind();
program.setUniformValue("color", QVector4D(0.2f, 0.7f, 1.0f, 1.0f));
```

不同 OpenGL 版本的 shader 语法不同。Core Profile 通常使用 `in`/`out` 和显式布局；示例中的旧式 `attribute`/`gl_FragColor` 只适合兼容上下文或旧版 GLSL。

## 8. 绘制顺序和状态管理

```cpp
program.bind();
vao.bind();
glDrawArrays(GL_TRIANGLES, 0, vertexCount);
vao.release();
program.release();
```

OpenGL 是状态机。深度测试、混合、剔除、绑定对象和视口都会影响后续绘制。自定义 widget 应在绘制前设置所需状态，绘制后尽量恢复会影响 Qt 或其他渲染器的状态。

## 9. QPainter 与 OpenGL 混用

在 `QOpenGLWidget::paintGL()` 中可以使用 `QPainter` 绘制 2D 叠加，但要让 QPainter 生命周期包住其绘制操作：

```cpp
QPainter painter(this);
painter.setPen(Qt::white);
painter.drawText(10, 20, QStringLiteral("FPS: 60"));
```

混用会产生状态切换开销。复杂 2D 内容应评估纯 QPainter、Qt Quick 或单独纹理合成方案。

## 10. 更新和动画

```cpp
void ColorWidget::setAngle(float value)
{
    angle = value;
    update(); // 请求下一帧，不要在 setter 中直接调用 paintGL
}
```

使用 `QTimer` 或动画驱动属性，再调用 `update()`。不要在循环中手动反复调用 `paintGL()`，这会绕过 Qt 的更新调度和交换流程。

## 11. 资源和上下文生命周期

`QOpenGLTexture`、VBO、VAO、FBO 和 shader program 都是上下文相关资源。窗口销毁或上下文重建时，应在 `makeCurrent()` 后释放资源；`QOpenGLWidget` 的上下文可能因窗口重建而重新创建，不能永久假设资源 ID 有效。

## 12. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| OpenGL 调用崩溃 | 没有当前上下文 | 只在 initialize/paint/resize 或 makeCurrent 后调用 |
| 黑屏 | 未清屏、视口为零或 shader 未 link | 检查 glClear、glViewport 和 log |
| Core Profile 报错 | 使用旧式 shader/未绑定 VAO | 使用匹配版本语法并绑定 VAO |
| 资源删除失败 | 删除时上下文不当前 | `makeCurrent()` 后 destroy |
| resize 后比例错误 | 未更新投影/视口 | 在 resizeGL 中更新 |
| 帧率低 | 每帧大量状态切换或同步映射 | 批量提交、减少 map 和状态变更 |

## 13. 自测题

1. QOpenGLWidget 的三个核心虚函数分别在什么阶段调用？
2. 为什么构造函数中不应直接调用 glClear？
3. QOpenGLFunctions 解决了什么平台问题？
4. QOpenGLBuffer::map 后为什么必须 unmap？
5. OpenGL 资源为什么不能脱离上下文管理？

### 参考答案

1. initializeGL 初始化资源，resizeGL 处理尺寸变化，paintGL 执行绘制。
2. 构造时上下文可能尚未创建或未当前化。
3. 运行时解析不同平台上不一定能直接链接的 OpenGL 函数。
4. 映射建立 CPU 与 GPU 缓冲访问关系，unmap 释放映射并提交/恢复资源状态。
5. 资源 ID 和删除操作由具体上下文拥有，脱离上下文无法保证有效。

## 14. 小结

Qt OpenGL 的基础是上下文纪律：在正确阶段创建资源，在当前上下文中绑定和绘制，在重建或销毁时及时释放。`QOpenGLWidget` 负责与 Qt 更新循环衔接，`QOpenGLFunctions`、Buffer、VAO 和 ShaderProgram 负责把 OpenGL 状态管理组织成可维护代码。
