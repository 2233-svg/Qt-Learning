#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_DOCS_ROOT = Path(r"C:\Qt\Docs\Qt-6.11.1")
DEFAULT_OUTPUT_ROOT = Path.cwd()
GENERATED_MARKER = "<!-- 自动生成：tools/generate_qt_notes.py，来源：Qt 6.11.1 离线文档。-->"


SECTION_TITLES = {
    "properties": "属性",
    "public-functions": "公共函数",
    "public-slots": "公共槽",
    "signals": "信号",
    "static-public-members": "静态公共成员",
    "protected-functions": "受保护函数",
    "related-non-members": "相关非成员",
    "macros": "宏",
    "details": "详细说明",
}


MEMBER_DOCUMENTATION_TITLES = {
    "member type documentation": "成员类型",
    "property documentation": "属性",
    "member function documentation": "成员函数",
    "signal documentation": "信号",
    "macro documentation": "宏",
}


DETAIL_SUBSECTION_TITLES = {
    "thread-affinity": "线程亲和性",
    "no-copy-constructor-or-assignment-operator": "不可复制",
    "auto-connection": "自动连接",
    "dynamic-properties": "动态属性",
    "internationalization-i18n": "国际化",
    "overview": "概览",
    "examples": "示例",
    "properties": "属性",
    "signals": "信号",
    "slots": "槽",
    "public-functions": "公共函数",
    "public-slots": "公共槽",
    "static-public-members": "静态公共成员",
    "protected-functions": "受保护函数",
    "macros": "宏",
    "accuracy-and-timer-resolution": "定时器精度与分辨率",
    "alternatives-to-qtimer": "QTimer 的替代方案",
    "layout-management": "布局管理",
    "model-subclassing-reference": "模型派生实现参考",
    "using-the-convenience-classes": "使用便捷类",
}


MODULE_COMPONENT_RE = re.compile(r"^Qt\s+(.+?)\s+C\+\+\s+Classes$", re.I)


BRIEF_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^The ([\w:]+) class is the base class of all (.+)\.$", re.I), r"\2基类"),
    (re.compile(r"^The abstract base class for (.+)\.$", re.I), r"\1抽象基类"),
    (re.compile(r"^The abstract base class of (.+)\.$", re.I), r"\1抽象基类"),
    (re.compile(r"^The base class of (.+)\.$", re.I), r"\1基类"),
    (re.compile(r"^The base of all (.+)$", re.I), r"所有\1的基类"),
    (re.compile(r"^Interface to manage (.+)\.$", re.I), r"\1管理接口"),
    (re.compile(r"^Interface for (.+)\.$", re.I), r"\1接口"),
    (re.compile(r"^A convenience class that (.+)\.$", re.I), r"便捷封装：\1"),
    (re.compile(r"^Convenience class that (.+)\.$", re.I), r"便捷封装：\1"),
    (re.compile(r"^Wrapper around (.+)\.$", re.I), r"\1封装"),
    (re.compile(r"^Way to (.+)\.$", re.I), r"用于\1"),
    (re.compile(r"^Used to (.+)\.$", re.I), r"用于\1"),
    (re.compile(r"^Provides (.+)\.$", re.I), r"\1支持"),
    (re.compile(r"^Represents (.+)\.$", re.I), r"\1表示"),
    (re.compile(r"^Container for (.+)\.$", re.I), r"\1容器"),
    (re.compile(r"^Container to (.+)\.$", re.I), r"用于\1的容器"),
    (re.compile(r"^The base class of widgets that can have a frame\.$", re.I), r"带边框控件基类"),
    (re.compile(r"^Repetitive and single-shot timers\.$", re.I), r"周期单次定时器"),
    (re.compile(r"^Fast way to calculate elapsed times\.$", re.I), r"耗时测量"),
    (re.compile(r"^Marks a deadline in the future\.$", re.I), r"未来截止时间"),
    (re.compile(r"^Means of entering and leaving an event loop\.$", re.I), r"进入和退出事件循环的方式"),
    (re.compile(r"^The base class of all event classes\. Event objects contain event parameters\.$", re.I), r"事件基类"),
    (re.compile(r"^The base class of button widgets, providing functionality common to buttons\.$", re.I), r"按钮控件基类"),
    (re.compile(r"^The abstract interface for item model classes\.$", re.I), r"项目模型抽象接口"),
]


WORD_REPLACEMENTS = [
    ("animations", "动画"),
    ("animation", "动画"),
    ("thread affinity", "线程亲和性"),
    ("thread safety", "线程安全"),
    ("event loop", "事件循环"),
    ("event queue", "事件队列"),
    ("object tree", "对象树"),
    ("dynamic properties", "动态属性"),
    ("signal and slots", "信号槽"),
    ("signal and slot", "信号槽"),
    ("single-shot", "单次"),
    ("repetitive", "周期"),
    ("elapsed", "耗时"),
    ("deadline", "截止时间"),
    ("base class", "基类"),
    ("abstract base class", "抽象基类"),
    ("convenience class", "便捷类"),
    ("convenience", "便捷"),
    ("wrapper", "封装"),
    ("container", "容器"),
    ("interface", "接口"),
    ("manager", "管理器"),
    ("engine", "引擎"),
    ("helper", "辅助"),
    ("plugin", "插件"),
    ("subclassing", "派生实现"),
    ("safety", "安全"),
    ("classes", "类"),
    ("class", "类"),
    ("models", "模型"),
    ("model", "模型"),
    ("views", "视图"),
    ("view", "视图"),
    ("objects", "对象"),
    ("object", "对象"),
    ("timers", "定时器"),
    ("widget", "控件"),
    ("widgets", "控件"),
    ("window", "窗口"),
    ("dialog", "对话框"),
    ("application", "应用"),
    ("timer", "定时器"),
    ("thread", "线程"),
    ("threads", "线程"),
    ("event", "事件"),
    ("events", "事件"),
    ("property", "属性"),
    ("properties", "属性"),
    ("signal", "信号"),
    ("signals", "信号"),
    ("slot", "槽"),
    ("slots", "槽"),
    ("model", "模型"),
    ("view", "视图"),
    ("array", "数组"),
    ("list", "列表"),
    ("items", "项目"),
    ("item", "项目"),
    ("map", "映射"),
    ("hash", "哈希"),
    ("file", "文件"),
    ("directory", "目录"),
    ("process", "进程"),
    ("permission", "权限"),
    ("lock", "锁"),
    ("mutex", "互斥锁"),
    ("read-write", "读写"),
    ("graphics", "图形"),
    ("network", "网络"),
    ("audio", "音频"),
    ("video", "视频"),
    ("sql", "SQL"),
    ("xml", "XML"),
    ("json", "JSON"),
]


MODULE_FOLDER_HINTS = {
    "qt": "Qt",
}


TOPIC_KEYWORDS = [
    ("TimerInfo", "定时器信息"),
    ("AbstractItemModel", "项目模型抽象接口"),
    ("AbstractListModel", "列表模型抽象基类"),
    ("AbstractTableModel", "表格模型抽象基类"),
    ("AbstractProxyModel", "代理模型抽象基类"),
    ("IdentityProxyModel", "透明代理模型"),
    ("SortFilterProxyModel", "排序过滤代理模型"),
    ("ItemSelectionModel", "项目选择模型"),
    ("ModelIndex", "模型索引"),
    ("PersistentModelIndex", "持久模型索引"),
    ("AbstractAnimation", "动画抽象基类"),
    ("AnimationGroup", "动画组"),
    ("PropertyAnimation", "属性动画"),
    ("VariantAnimation", "变体值动画"),
    ("EventDispatcher", "事件分发器"),
    ("EventLoop", "事件循环"),
    ("Application", "应用对象"),
    ("CommandLineParser", "命令行解析器"),
    ("CommandLineOption", "命令行选项"),
    ("FileSystemWatcher", "文件系统监视器"),
    ("FileInfo", "文件信息"),
    ("FileDevice", "文件设备"),
    ("SaveFile", "安全保存文件"),
    ("TemporaryFile", "临时文件"),
    ("TemporaryDir", "临时目录"),
    ("IODevice", "I/O 设备"),
    ("Buffer", "内存缓冲设备"),
    ("DataStream", "二进制数据流"),
    ("TextStream", "文本流"),
    ("Settings", "配置存储"),
    ("Process", "外部进程"),
    ("Timer", "定时器"),
    ("Deadline", "截止时间"),
    ("Elapsed", "耗时测量"),
    ("ThreadPool", "线程池"),
    ("Thread", "线程"),
    ("MutexLocker", "互斥锁 RAII 管理"),
    ("Mutex", "互斥锁"),
    ("Semaphore", "信号量"),
    ("WaitCondition", "等待条件"),
    ("ReadWriteLock", "读写锁"),
    ("ReadLocker", "读锁 RAII 管理"),
    ("WriteLocker", "写锁 RAII 管理"),
    ("SharedPointer", "共享智能指针"),
    ("WeakPointer", "弱引用智能指针"),
    ("ScopedPointer", "作用域智能指针"),
    ("Pointer", "指针辅助类型"),
    ("ByteArrayMatcher", "字节数组匹配器"),
    ("ByteArrayView", "字节数组视图"),
    ("ByteArray", "字节数组"),
    ("AnyStringView", "通用字符串视图"),
    ("Latin1StringView", "Latin-1 字符串视图"),
    ("StringView", "字符串视图"),
    ("StringMatcher", "字符串匹配器"),
    ("RegularExpressionMatchIterator", "正则匹配迭代器"),
    ("RegularExpressionMatch", "正则匹配结果"),
    ("RegularExpression", "正则表达式"),
    ("CollatorSortKey", "本地化排序键"),
    ("Collator", "本地化字符串比较器"),
    ("Locale", "本地化格式转换"),
    ("Translator", "翻译器"),
    ("DateTime", "日期时间"),
    ("TimeZone", "时区"),
    ("Time", "时间"),
    ("Date", "日期"),
    ("Calendar", "日历系统"),
    ("JsonDocument", "JSON 文档"),
    ("JsonObject", "JSON 对象"),
    ("JsonArray", "JSON 数组"),
    ("JsonValue", "JSON 值"),
    ("JsonParseError", "JSON 解析错误"),
    ("CborStreamReader", "CBOR 流读取器"),
    ("CborStreamWriter", "CBOR 流写入器"),
    ("CborValue", "CBOR 值"),
    ("CborMap", "CBOR 映射"),
    ("CborArray", "CBOR 数组"),
    ("XmlStreamReader", "XML 流读取器"),
    ("XmlStreamWriter", "XML 流写入器"),
    ("XmlStream", "XML 流"),
    ("NetworkAccessManager", "网络访问管理器"),
    ("NetworkReply", "网络响应"),
    ("NetworkRequest", "网络请求"),
    ("TcpSocket", "TCP 套接字"),
    ("TcpServer", "TCP 服务器"),
    ("UdpSocket", "UDP 套接字"),
    ("SslSocket", "SSL 套接字"),
    ("HostInfo", "主机信息"),
    ("DnsLookup", "DNS 查询"),
    ("UrlQuery", "URL 查询"),
    ("Url", "URL"),
    ("SqlDatabase", "SQL 数据库连接"),
    ("SqlQueryModel", "SQL 查询模型"),
    ("SqlTableModel", "SQL 表模型"),
    ("SqlRelationalTableModel", "SQL 关系表模型"),
    ("SqlQuery", "SQL 查询"),
    ("SqlRecord", "SQL 记录"),
    ("SqlField", "SQL 字段"),
    ("PainterPath", "绘制路径"),
    ("Painter", "绘制器"),
    ("PaintDevice", "绘制设备"),
    ("PaintEvent", "绘制事件"),
    ("Pixmap", "像素图"),
    ("ImageReader", "图像读取器"),
    ("ImageWriter", "图像写入器"),
    ("Image", "图像"),
    ("Bitmap", "位图"),
    ("Color", "颜色"),
    ("Brush", "画刷"),
    ("Pen", "画笔"),
    ("Font", "字体"),
    ("Icon", "图标"),
    ("Palette", "调色板"),
    ("Transform", "变换"),
    ("Matrix", "矩阵"),
    ("Vector", "向量"),
    ("Quaternion", "四元数"),
    ("OpenGL", "OpenGL 资源"),
    ("ShaderProgram", "着色器程序"),
    ("Shader", "着色器"),
    ("Widget", "控件"),
    ("DialogButtonBox", "对话框按钮盒"),
    ("Dialog", "对话框"),
    ("LayoutItem", "布局项"),
    ("BoxLayout", "盒式布局"),
    ("GridLayout", "网格布局"),
    ("FormLayout", "表单布局"),
    ("Layout", "布局管理器"),
    ("MainWindow", "主窗口"),
    ("ActionGroup", "动作组"),
    ("Action", "动作"),
    ("MenuBar", "菜单栏"),
    ("Menu", "菜单"),
    ("ToolBar", "工具栏"),
    ("StatusBar", "状态栏"),
    ("PushButton", "按钮"),
    ("AbstractButton", "按钮抽象基类"),
    ("CheckBox", "复选框"),
    ("RadioButton", "单选按钮"),
    ("ComboBox", "下拉框"),
    ("LineEdit", "单行文本编辑器"),
    ("TextEdit", "富文本编辑器"),
    ("PlainTextEdit", "纯文本编辑器"),
    ("Label", "标签"),
    ("Slider", "滑块"),
    ("SpinBox", "数值输入框"),
    ("ProgressBar", "进度条"),
    ("ScrollArea", "滚动区域"),
    ("ScrollBar", "滚动条"),
    ("GraphicsScene", "图形场景"),
    ("GraphicsView", "图形视图"),
    ("GraphicsItem", "图形项"),
    ("Graphics", "Graphics View 类型"),
    ("QuickItem", "Qt Quick 项"),
    ("Quick", "Qt Quick 类型"),
    ("Qml", "QML 类型"),
    ("QML", "QML 类型"),
    ("JSEngine", "JavaScript 引擎"),
    ("JS", "JavaScript 类型"),
    ("Audio", "音频类型"),
    ("Video", "视频类型"),
    ("Media", "媒体类型"),
    ("Permission", "权限对象"),
    ("Plugin", "插件接口"),
    ("Factory", "工厂"),
    ("Iterator", "迭代器"),
    ("Iterable", "可迭代封装"),
    ("Map", "映射容器"),
    ("Hash", "哈希容器"),
    ("List", "列表容器"),
    ("Vector", "向量容器"),
    ("Queue", "队列容器"),
    ("Stack", "栈容器"),
    ("Set", "集合容器"),
    ("Cache", "缓存容器"),
    ("Event", "事件对象"),
    ("StateMachine", "状态机"),
    ("State", "状态"),
]


@dataclass(frozen=True)
class ClassEntry:
    name: str
    href: str
    brief: str


@dataclass
class MemberDoc:
    category: str
    signatures: list[str]
    paragraphs: list[str]
    code_blocks: list[str]
    value_rows: list[tuple[str, ...]]


@dataclass
class ClassPage:
    module_dir: str
    module_name: str
    module_folder: str
    class_name: str
    class_page_path: Path
    brief: str
    header: str | None
    cmake: str | None
    qmake: str | None
    inherits: str | None
    inherited_by: list[str]
    public_types: list[str]
    properties: list[str]
    public_functions: list[str]
    public_slots: list[str]
    signals: list[str]
    static_members: list[str]
    protected_functions: list[str]
    related_non_members: list[str]
    macros: list[str]
    code_blocks: list[str]
    detailed_sections: list[tuple[str, str]]
    raw_detail_text: str
    member_docs: list[MemberDoc]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Qt class notes from offline docs.")
    parser.add_argument("--docs-root", type=Path, default=DEFAULT_DOCS_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--modules", nargs="*", help="Optional module directory names to process.")
    parser.add_argument("--classes", nargs="*", help="Optional exact class names to process.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing notes with matching class prefixes.")
    parser.add_argument("--clean", action="store_true", help="Remove notes previously generated by this script before generating.")
    parser.add_argument("--limit", type=int, default=0, help="Limit generated notes for testing.")
    args = parser.parse_args()

    docs_root = args.docs_root
    output_root = args.output_root

    removed = clean_generated_notes(output_root) if args.clean else 0
    module_pages = collect_module_pages(docs_root, args.modules)
    if not module_pages:
        raise SystemExit(f"No module pages found under {docs_root}")

    existing = collect_existing_markdown_stems(output_root)

    generated = 0
    skipped = 0
    missing_pages = 0
    written: list[Path] = []

    for module_dir, module_page in module_pages:
        module_info = parse_module_page(module_dir, module_page)
        if module_info is None:
            continue
        module_name, module_folder = module_info
        class_entries = parse_module_classes(module_page)
        for entry in class_entries:
            if args.classes and entry.name not in args.classes:
                continue
            if args.limit and generated >= args.limit:
                break
            page_path = resolve_class_page(docs_root, module_dir, entry.href)
            if page_path is None:
                missing_pages += 1
                continue
            if not args.overwrite and is_covered(entry.name, existing):
                skipped += 1
                continue
            class_page = parse_class_page(module_dir, module_name, module_folder, entry, page_path)
            if class_page is None:
                missing_pages += 1
                continue
            out_path = make_output_path(output_root, class_page)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(render_markdown(class_page), encoding="utf-8")
            existing.add(out_path.stem)
            generated += 1
            written.append(out_path)
        if args.limit and generated >= args.limit:
            break

    summary = [
        f"generated={generated}",
        f"skipped={skipped}",
        f"missing_pages={missing_pages}",
        f"modules={len(module_pages)}",
        f"removed={removed}",
    ]
    print(" ".join(summary))
    if written:
        print(f"first={written[0]}")
        print(f"last={written[-1]}")
    return 0


def collect_module_pages(docs_root: Path, selected_modules: list[str] | None) -> list[tuple[str, Path]]:
    items: list[tuple[str, Path]] = []
    for module_dir in sorted(p for p in docs_root.iterdir() if p.is_dir()):
        if selected_modules and module_dir.name not in selected_modules:
            continue
        module_page = module_dir / f"{module_dir.name}-module.html"
        if module_page.exists():
            items.append((module_dir.name, module_page))
    return items


def parse_module_page(module_dir: str, module_page: Path) -> tuple[str, str] | None:
    html_text = module_page.read_text(encoding="utf-8", errors="ignore")
    title = extract_title(html_text)
    if not title:
        return None
    module_name = title.split("|", 1)[0].strip()
    module_folder = title_to_folder(module_name)
    if not module_folder:
        module_folder = pretty_module_folder(module_dir)
    return module_name, module_folder


def title_to_folder(module_title: str) -> str:
    title = module_title.strip()
    title = re.sub(r"\s+C\+\+\s+Classes\s*$", "", title, flags=re.I)
    title = re.sub(r"\s+(Module|Manual)$", "", title, flags=re.I)
    title = title.replace("D-Bus", "DBus")
    title = title.replace(" ", "")
    return title


def pretty_module_folder(module_dir: str) -> str:
    name = module_dir
    if name.lower().startswith("qt"):
        rest = name[2:]
        return "Qt" + rest[:1].upper() + rest[1:]
    return name


def parse_module_classes(module_page: Path) -> list[ClassEntry]:
    html_text = module_page.read_text(encoding="utf-8", errors="ignore")
    classes_section = extract_section_by_heading(html_text, "classes")
    if not classes_section:
        return []
    entries: list[ClassEntry] = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", classes_section, flags=re.S | re.I):
        match = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>', row, flags=re.S | re.I)
        if not match:
            continue
        href = html.unescape(match.group(1))
        name = html_fragment_to_text(match.group(2))
        if not name:
            continue
        desc_match = re.search(r'<td class="tblDescr"><p>(.*?)</p></td>', row, flags=re.S | re.I)
        brief = html_fragment_to_text(desc_match.group(1)) if desc_match else ""
        entries.append(ClassEntry(name=name, href=href, brief=brief))
    return entries


def resolve_class_page(docs_root: Path, module_dir: str, href: str) -> Path | None:
    target = href.split("#", 1)[0]
    if not target:
        return None
    candidate = (docs_root / module_dir / target).resolve()
    if candidate.exists():
        return candidate
    alt = (docs_root / module_dir / target.lstrip("./")).resolve()
    if alt.exists():
        return alt
    return None


def parse_class_page(module_dir: str, module_name: str, module_folder: str, entry: ClassEntry, page_path: Path) -> ClassPage | None:
    html_text = page_path.read_text(encoding="utf-8", errors="ignore")
    title = extract_title(html_text)
    if not title:
        return None
    header_table = extract_requisites_table(html_text)
    header = header_table.get("Header")
    cmake = header_table.get("CMake")
    qmake = header_table.get("qmake")
    inherits = header_table.get("Inherits")
    inherited_by = split_links(header_table.get("Inherited By", ""))
    public_types = collect_section_items(html_text, "public-types")
    properties = collect_section_items(html_text, "properties")
    public_functions = collect_section_items(html_text, "public-functions")
    public_slots = collect_section_items(html_text, "public-slots")
    signals = collect_section_items(html_text, "signals")
    static_members = collect_section_items(html_text, "static-public-members")
    protected_functions = collect_section_items(html_text, "protected-functions")
    related_non_members = collect_section_items(html_text, "related-non-members")
    macros = collect_section_items(html_text, "macros")
    code_blocks = extract_code_blocks(html_text)
    detailed_sections, raw_detail_text = extract_detailed_sections(html_text)
    member_docs = extract_member_docs(html_text)

    class_name = entry.name
    brief = entry.brief or extract_meta_description(html_text) or ""

    return ClassPage(
        module_dir=module_dir,
        module_name=module_name,
        module_folder=module_folder,
        class_name=class_name,
        class_page_path=page_path,
        brief=brief,
        header=header,
        cmake=cmake,
        qmake=qmake,
        inherits=inherits,
        inherited_by=inherited_by,
        public_types=public_types,
        properties=properties,
        public_functions=public_functions,
        public_slots=public_slots,
        signals=signals,
        static_members=static_members,
        protected_functions=protected_functions,
        related_non_members=related_non_members,
        macros=macros,
        code_blocks=code_blocks,
        detailed_sections=detailed_sections,
        raw_detail_text=raw_detail_text,
        member_docs=member_docs,
    )


def extract_title(html_text: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html_text, flags=re.S | re.I)
    if not match:
        return ""
    return html_fragment_to_text(match.group(1))


def extract_meta_description(html_text: str) -> str:
    match = re.search(r'<meta name="description" content="([^"]*)"', html_text, flags=re.I)
    if not match:
        return ""
    return html.unescape(match.group(1)).strip()


def extract_requisites_table(html_text: str) -> dict[str, str]:
    match = re.search(r'<table class="alignedsummary requisites"[^>]*>(.*?)</table>', html_text, flags=re.S | re.I)
    if not match:
        return {}
    table_html = match.group(1)
    info: dict[str, str] = {}
    for row in re.findall(r"<tr>(.*?)</tr>", table_html, flags=re.S | re.I):
        label_match = re.search(r'<td class="memItemLeft[^>]*">\s*([^<:]+):</td>', row, flags=re.S | re.I)
        value_match = re.search(r'<td class="memItemRight[^>]*>(.*?)</td>', row, flags=re.S | re.I)
        if not label_match or not value_match:
            continue
        label = html_fragment_to_text(label_match.group(1))
        value = normalize_text(html_fragment_to_text(value_match.group(1), preserve_breaks=True))
        if label and value:
            info[label] = value
    return info


def extract_section_by_heading(html_text: str, heading_id: str) -> str:
    match = re.search(rf'<h2 id="{re.escape(heading_id)}">.*?</h2>', html_text, flags=re.S | re.I)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r'<h2\b', html_text[start:], flags=re.S | re.I)
    end = start + next_match.start() if next_match else len(html_text)
    return html_text[start:end]


def collect_section_items(html_text: str, heading_id: str) -> list[str]:
    section = extract_section_by_heading(html_text, heading_id)
    if not section:
        return []
    items: list[str] = []
    for li in re.findall(r"<li[^>]*>(.*?)</li>", section, flags=re.S | re.I):
        text = normalize_text(html_fragment_to_text(li, preserve_breaks=True))
        if text and text not in items:
            items.append(text)
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", section, flags=re.S | re.I):
        if "<li" in row.lower():
            continue
        text = normalize_text(html_fragment_to_text(row, preserve_breaks=True))
        if text and text not in items:
            items.append(text)
    return items


def extract_code_blocks(html_text: str) -> list[str]:
    blocks: list[str] = []
    for raw in re.findall(r"<pre[^>]*>(.*?)</pre>", html_text, flags=re.S | re.I):
        code = html_fragment_to_code(raw)
        code = code.strip("\n")
        if code and code not in blocks:
            blocks.append(code)
    return blocks


def extract_detailed_sections(html_text: str) -> tuple[list[tuple[str, str]], str]:
    detail_html = extract_section_by_heading(html_text, "details")
    if not detail_html:
        return [], ""
    sections: list[tuple[str, str]] = []
    h3_matches = list(re.finditer(r'<h3 id="([^"]+)">(.*?)</h3>', detail_html, flags=re.S | re.I))
    if h3_matches:
        intro_html = detail_html[:h3_matches[0].start()]
        intro_text = detail_section_text(intro_html)
        for idx, match in enumerate(h3_matches):
            section_id = html.unescape(match.group(1))
            title = html_fragment_to_text(match.group(2))
            start = match.end()
            end = h3_matches[idx + 1].start() if idx + 1 < len(h3_matches) else len(detail_html)
            body = detail_html[start:end]
            text = detail_section_text(body)
            if text:
                sections.append((title, text))
    else:
        intro_text = detail_section_text(detail_html)
        text = detail_section_text(detail_html)
        if text:
            sections.append(("详细说明", text))
    return sections, intro_text


def extract_member_docs(html_text: str) -> list[MemberDoc]:
    docs: list[MemberDoc] = []
    headings = list(re.finditer(r"<h2\b[^>]*>(.*?)</h2>", html_text, flags=re.S | re.I))
    for index, heading in enumerate(headings):
        title = normalize_text(html_fragment_to_text(heading.group(1)))
        category = MEMBER_DOCUMENTATION_TITLES.get(title.lower())
        if not category:
            continue
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(html_text)
        docs.extend(extract_member_docs_from_section(html_text[start:end], category))
    return docs


def extract_member_docs_from_section(section_html: str, category: str) -> list[MemberDoc]:
    docs: list[MemberDoc] = []
    markers = list(re.finditer(r"<!--\s*\$\$\$.*?-->", section_html, flags=re.S))
    for index, marker in enumerate(markers):
        start = marker.end()
        end_marker = re.search(r"<!--\s*@@@.*?-->", section_html[start:], flags=re.S)
        next_marker_start = markers[index + 1].start() if index + 1 < len(markers) else len(section_html)
        end = start + end_marker.start() if end_marker else next_marker_start
        if end > next_marker_start:
            end = next_marker_start
        fragment = section_html[start:end]
        heading_matches = list(
            re.finditer(
                r'<h3\b[^>]*class="[^"]*\bfn\b[^"]*"[^>]*>(.*?)</h3>',
                fragment,
                flags=re.S | re.I,
            )
        )
        if not heading_matches:
            continue
        signatures = [
            normalize_text(html_fragment_to_text(match.group(1), preserve_breaks=True))
            for match in heading_matches
        ]
        signatures = [signature for signature in signatures if signature]
        if not signatures:
            continue
        body = fragment[heading_matches[-1].end():]
        paragraphs = extract_documentation_paragraphs(body)
        code_blocks = extract_code_blocks(body)
        value_rows = extract_value_rows(body) if category == "成员类型" else []
        docs.append(
            MemberDoc(
                category=category,
                signatures=unique(signatures),
                paragraphs=paragraphs,
                code_blocks=code_blocks,
                value_rows=value_rows,
            )
        )
    return docs


def extract_documentation_paragraphs(fragment: str) -> list[str]:
    paragraphs: list[str] = []
    for raw in re.findall(r"<p[^>]*>(.*?)</p>", fragment, flags=re.S | re.I):
        text = normalize_text(html_fragment_to_text(raw, preserve_breaks=True))
        if not text or text.startswith("See also") or text == "Access functions:":
            continue
        if text not in paragraphs:
            paragraphs.append(text)
    for raw in re.findall(r"<li[^>]*>(.*?)</li>", fragment, flags=re.S | re.I):
        text = normalize_text(html_fragment_to_text(raw, preserve_breaks=True))
        if text and text not in paragraphs:
            paragraphs.append(text)
    return paragraphs


def extract_value_rows(fragment: str) -> list[tuple[str, ...]]:
    rows: list[tuple[str, ...]] = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", fragment, flags=re.S | re.I):
        cells = [
            normalize_text(html_fragment_to_text(cell, preserve_breaks=True))
            for cell in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, flags=re.S | re.I)
        ]
        cells = [cell for cell in cells if cell]
        if len(cells) < 2:
            continue
        if cells[0] in {"Constant", "Value", "Description"}:
            continue
        value = tuple(cells[:3])
        if value not in rows:
            rows.append(value)
    return rows


def detail_section_text(fragment: str) -> str:
    paragraphs = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>", fragment, flags=re.S | re.I):
        text = normalize_text(html_fragment_to_text(p))
        if text:
            paragraphs.append(text)
        if len(paragraphs) >= 2:
            break
    if not paragraphs:
        for li in re.findall(r"<li[^>]*>(.*?)</li>", fragment, flags=re.S | re.I):
            text = normalize_text(html_fragment_to_text(li))
            if text:
                paragraphs.append(f"- {text}")
            if len(paragraphs) >= 3:
                break
    return "\n\n".join(paragraphs)


def split_links(text: str) -> list[str]:
    if not text:
        return []
    parts = []
    for chunk in re.split(r"[,，]|\band\b|\bor\b", text, flags=re.I):
        chunk = normalize_text(chunk)
        chunk = re.sub(r"^(and|or)\s+", "", chunk, flags=re.I)
        if chunk:
            parts.append(chunk)
    return parts


def html_fragment_to_code(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"</p>", "\n\n", fragment, flags=re.I)
    fragment = re.sub(r"</tr>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"</td>", "\t", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    fragment = html.unescape(fragment)
    fragment = fragment.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in fragment.split("\n")]
    return "\n".join(lines)


def html_fragment_to_text(fragment: str, preserve_breaks: bool = False) -> str:
    if not fragment:
        return ""
    fragment = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    fragment = re.sub(r"<script.*?</script>", "", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<style.*?</style>", "", fragment, flags=re.S | re.I)
    fragment = fragment.replace("&nbsp;", " ")
    if preserve_breaks:
        fragment = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.I)
        fragment = re.sub(r"</p>", "\n\n", fragment, flags=re.I)
        fragment = re.sub(r"</li>", "\n", fragment, flags=re.I)
        fragment = re.sub(r"</tr>", "\n", fragment, flags=re.I)
        fragment = re.sub(r"</h[1-6]>", "\n\n", fragment, flags=re.I)
    else:
        fragment = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
        fragment = re.sub(r"</p>", " ", fragment, flags=re.I)
        fragment = re.sub(r"</li>", " ", fragment, flags=re.I)
        fragment = re.sub(r"</tr>", " ", fragment, flags=re.I)
        fragment = re.sub(r"</h[1-6]>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    fragment = html.unescape(fragment)
    if preserve_breaks:
        fragment = re.sub(r"[ \t]+\n", "\n", fragment)
        fragment = re.sub(r"\n{3,}", "\n\n", fragment)
        return fragment.strip()
    return normalize_text(fragment)


def normalize_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    return text.strip()


def make_output_path(output_root: Path, class_page: ClassPage) -> Path:
    suffix = guess_suffix(class_page.class_name, class_page.brief)
    base = normalize_class_name(class_page.class_name)
    stem = f"{base}_{suffix}" if suffix else base
    stem = sanitize_filename(stem)
    if len(stem) > 120:
        stem = stem[:120].rstrip(" _-.")
    return output_root / class_page.module_folder / f"{stem}.md"


def sanitize_filename(name: str) -> str:
    name = name.replace("/", "_").replace("\\", "_")
    name = re.sub(r'[<>:"|?*]', "_", name)
    name = re.sub(r"\s+", "", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("._ ")


def normalize_class_name(class_name: str) -> str:
    return class_name.replace("::", "__")


def guess_suffix(class_name: str, brief: str) -> str:
    candidate = topic_from_name(class_name)
    if not candidate:
        brief = normalize_text(brief)
        candidate = translate_brief(brief)
    if not candidate or looks_bad_suffix(candidate):
        candidate = "类概览"
    candidate = candidate.replace("：", "")
    candidate = re.sub(r"[().,;:/\\|!?\"'`]+", "", candidate)
    candidate = re.sub(r"\s+", "", candidate)
    if len(candidate) > 20:
        candidate = candidate[:20]
    candidate = candidate.strip("_-")
    return candidate or "概览"


def translate_brief(text: str) -> str:
    if not text:
        return ""
    stripped = text.strip()
    for pattern, replacement in BRIEF_RULES:
        match = pattern.match(stripped)
        if match:
            return expand_replacement(replacement, match)
    result = stripped
    for src, dst in sorted(WORD_REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
        result = sub_word(result, src, dst)
    result = result.replace("The ", "").replace("the ", "")
    result = result.replace("  ", " ")
    result = result.replace(" .", ".")
    result = result.strip()
    return result


def expand_replacement(replacement: str, match: re.Match[str]) -> str:
    text = replacement
    for idx in range(1, len(match.groups()) + 1):
        text = text.replace(f"\\{idx}", match.group(idx))
    return translate_phrase(text)


def translate_phrase(text: str) -> str:
    result = text
    for src, dst in sorted(WORD_REPLACEMENTS, key=lambda item: len(item[0]), reverse=True):
        result = sub_word(result, src, dst)
    result = result.replace("  ", " ")
    return result.strip()


def sub_word(text: str, src: str, dst: str) -> str:
    pattern = rf"(?<![A-Za-z0-9_]){re.escape(src)}(?![A-Za-z0-9_])"
    return re.sub(pattern, dst, text, flags=re.I)


def looks_bad_suffix(text: str) -> bool:
    if not text:
        return True
    if re.search(r"[A-Za-z]{4,}", text):
        return True
    return len(text) > 24


def is_covered(class_name: str, existing_stems: set[str]) -> bool:
    normalized = normalize_class_name(class_name)
    bare = class_name.split("::")[-1]
    for stem in existing_stems:
        if stem_matches_class(stem, normalized) or stem_matches_class(stem, class_name) or stem_matches_class(stem, bare):
            return True
    return False


def stem_matches_class(stem: str, class_name: str) -> bool:
    if not class_name:
        return False
    if stem == class_name:
        return True
    if not stem.startswith(class_name):
        return False
    if len(stem) == len(class_name):
        return True
    next_char = stem[len(class_name)]
    return next_char in "_（(" or not next_char.isascii()


def collect_existing_markdown_stems(root: Path) -> set[str]:
    stems: set[str] = set()
    if not root.exists():
        return stems
    for path in root.rglob("*.md"):
        stems.add(path.stem)
    return stems


def clean_generated_notes(root: Path) -> int:
    if not root.exists():
        return 0
    removed = 0
    for path in root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        is_current_generated = GENERATED_MARKER in text
        is_previous_generated = (
            text.startswith("# Qt ")
            and "\n- 离线来源：`C:\\Qt\\Docs\\Qt-6.11.1\\" in text
        )
        if is_current_generated or is_previous_generated:
            path.unlink()
            removed += 1
    prune_empty_directories(root)
    return removed


def prune_empty_directories(root: Path) -> None:
    for directory in sorted((path for path in root.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True):
        if directory == root:
            continue
        try:
            directory.rmdir()
        except OSError:
            pass


def render_markdown(page: ClassPage) -> str:
    topic = topic_for_page(page)
    lines: list[str] = []
    lines.append(GENERATED_MARKER)
    lines.append("")
    lines.append(f"# Qt {page.class_name} 深入笔记")
    lines.append("")
    lines.append("> 适用版本：Qt 6.11.1  ")
    if page.header:
        lines.append(f"> 头文件：`{page.header}`  ")
    lines.append(f"> 所属模块：`{guess_qt_target(page)}`  ")
    if page.inherits:
        lines.append(f"> 继承：`{render_inheritance(page.inherits, page.class_name)}`  ")
    else:
        lines.append("> 继承：无  ")
    lines.append(f"> 定位：{topic}")
    lines.append("")
    render_overview_section(lines, page, topic)
    render_build_section(lines, page)
    render_minimal_example(lines, page, topic)
    render_core_model(lines, page, topic)
    render_member_guide(lines, page)
    render_detail_guide(lines, page)
    render_edges(lines, page)
    render_extension_section(lines, page)
    render_full_member_docs(lines, page)
    render_member_sections(lines, page)
    render_summary(lines, page, topic)
    return "\n".join(lines).rstrip() + "\n"


def render_inheritance(inherits: str, base_name: str) -> str:
    chain = inherits
    if "->" in chain:
        return chain
    return f"{chain} -> {base_name}"


def first_paragraph(text: str) -> str:
    for chunk in re.split(r"\n{2,}", normalize_text(text)):
        chunk = chunk.strip()
        if chunk:
            return chunk
    return ""


def topic_for_page(page: ClassPage) -> str:
    explicit = topic_from_name(page.class_name)
    if explicit:
        return explicit
    if page.brief:
        translated = translate_brief(page.brief)
        if translated and not looks_bad_suffix(translated):
            return translated
    if page.class_name.startswith("QAbstract"):
        return "抽象基类"
    if page.class_name.endswith("Permission"):
        return "权限对象"
    if page.class_name.endswith("Iterator"):
        return "迭代器"
    return "Qt 类概览"


def topic_from_name(class_name: str) -> str:
    compact = class_name.replace("::", "")
    if "::" in class_name:
        tail = class_name.split("::")[-1]
        for key, topic in TOPIC_KEYWORDS:
            if key in tail:
                return topic
    for key, topic in TOPIC_KEYWORDS:
        if key in compact:
            return topic
    return ""


def intro_paragraph(page: ClassPage, topic: str) -> str:
    target = guess_qt_target(page)
    class_name = page.class_name
    pieces = [f"`{class_name}` 是 `{target}` 模块中的{topic}。"]
    if page.inherits:
        pieces.append(f"它继承自 `{page.inherits}`，因此使用时要同时遵守基类带来的生命周期、事件分发和所有权规则。")
    else:
        pieces.append("它通常作为值类型、辅助类型或接口类型使用，重点在于构造、拷贝/移动语义以及和其它 Qt 类之间的配合。")
    return "".join(pieces)


def render_overview_section(lines: list[str], page: ClassPage, topic: str) -> None:
    lines.append("## 1. 先建立整体认识：它解决什么问题")
    lines.append("")
    lines.append(intro_paragraph(page, topic))
    brief = normalize_text(page.brief)
    translated_brief = translate_brief(brief)
    if translated_brief and not re.search(r"[A-Za-z]{4,}", translated_brief):
        lines.append("")
        lines.append(f"官方摘要可以概括为：{translated_brief}。")
    lines.append("")
    if page.inherits:
        lines.append("继承关系可以先这样理解：")
        lines.append("")
        lines.append("```text")
        lines.append(render_inheritance_tree(page.inherits, page.class_name))
        lines.append("```")
        lines.append("")
    lines.append(overall_explanation(page, topic))
    lines.append("")


def render_inheritance_tree(inherits: str, class_name: str) -> str:
    parts = [part.strip() for part in re.split(r"\s*->\s*", inherits) if part.strip()]
    if not parts:
        return class_name
    if parts[-1] != class_name:
        parts.append(class_name)
    lines = [parts[0]]
    indent = ""
    for part in parts[1:]:
        indent += "  "
        lines.append(f"{indent}└─ {part}")
    return "\n".join(lines)


def overall_explanation(page: ClassPage, topic: str) -> str:
    name = page.class_name
    if is_abstract(page):
        pure = pure_virtual_functions(page)
        if pure:
            methods = "、".join(f"`{method}()`" for method in pure[:5])
            return (
                f"`{name}` 的核心价值在于定义一套稳定契约，而不是直接提供完整行为。"
                f"实际项目通常选择现成派生类，或通过派生实现 {methods} 等接口，把具体策略接入 Qt 框架。"
            )
        return (
            f"`{name}` 主要用于规定派生类的行为边界。理解它时先看继承层次、可重写函数和状态变化通知，"
            "再决定是直接使用现有派生类还是实现自己的子类。"
        )
    if is_model_related(page):
        return (
            f"`{name}` 位于模型/视图协作链路中。模型负责描述数据及其变化，视图和代理负责展示与交互；"
            "因此最重要的不是单个 getter，而是索引、角色数据与变化通知之间是否保持一致。"
        )
    if is_widget_related(page):
        return (
            f"`{name}` 属于界面对象体系。它的状态通常要通过父子对象、布局、事件循环和信号槽共同管理；"
            "不要把它当作只靠固定坐标或一次性赋值就能稳定工作的普通数据结构。"
        )
    if is_io_related(page):
        return (
            f"`{name}` 处理外部资源或数据通道。使用时围绕“创建或打开、执行操作、检查结果、关闭或等待完成”"
            "组织代码，并把失败状态、超时和资源释放视为正常流程的一部分。"
        )
    if is_container_related(page):
        return (
            f"`{name}` 是用于组织数据的 Qt 类型。除了增删查改，还要特别留意值语义、隐式共享、迭代器有效性"
            "以及把容器传给其它 Qt API 时发生的拷贝或引用行为。"
        )
    if is_thread_related(page):
        return (
            f"`{name}` 面向并发或同步场景。核心问题不是“能不能调用”，而是对象归属、阻塞时机、超时语义"
            "和多个线程访问同一状态时的边界。"
        )
    if is_qobject_related(page):
        return (
            f"`{name}` 处于 QObject 对象模型中。它的使用通常同时涉及父子对象生命周期、事件循环、"
            "信号槽和属性系统；理解这些协作关系比孤立记忆成员函数更重要。"
        )
    return (
        f"`{name}` 可以先按“创建对象、设置必要状态、调用核心操作、读取结果或响应通知”的流程理解。"
        "遇到复杂行为时，再回到本页的成员分组和官方详细说明确认前置条件与生命周期。"
    )


def usage_points(page: ClassPage, topic: str) -> list[str]:
    points: list[str] = []
    class_name = page.class_name
    if is_abstract(page):
        pure = pure_virtual_functions(page)
        if pure:
            names = "、".join(f"`{name}`" for name in pure[:5])
            points.append(f"这是需要派生实现的类型，至少关注纯虚接口 {names}。")
        else:
            points.append("类名或继承结构表明它主要作为抽象基类使用，通常通过派生类或工厂返回的实例间接使用。")
    elif is_qobject_related(page):
        points.append("作为 QObject 体系内的类型，通常用父子对象管理生命周期，并通过信号槽、事件或属性和外部协作。")
    else:
        points.append("优先按普通 C++ 对象理解它：创建对象、调用成员函数、把结果传给相关 Qt API。")

    if is_widget_related(page):
        points.append("GUI 控件只能在 GUI 线程中创建和访问；可见性、尺寸和父子关系通常交给 QWidget/QLayout 体系管理。")
    if is_event_related(page):
        points.append("事件对象通常在事件处理函数中短时间使用，处理完成后不应长期保存裸指针。")
    if is_model_related(page):
        points.append("模型类和视图/代理通过 QModelIndex、角色数据和变化信号协作；修改结构时要成对使用 begin/end 通知。")
    if is_io_related(page):
        points.append("I/O 类型通常围绕 open/read/write/close 或流式读写工作，错误状态和打开模式要作为正常控制流处理。")
    if is_container_related(page):
        points.append("容器和值类型通常支持拷贝、移动和迭代；修改共享数据前要理解隐式共享或迭代器失效规则。")
    if is_thread_related(page):
        points.append("线程与同步类型的重点是所有权、阻塞点、超时语义和跨线程调用边界。")
    if page.properties:
        points.append(f"属性表包含 {len(page.properties)} 项，可通过 getter/setter、绑定接口或 NOTIFY 信号观察状态。")
    if page.signals:
        points.append(f"信号表包含 {len(page.signals)} 项，状态变化应优先通过连接信号响应，而不是轮询内部状态。")
    if page.protected_functions:
        points.append(f"受保护函数有 {len(page.protected_functions)} 项，说明该类支持通过重写钩子扩展行为。")
    if not points:
        points.append(f"把它当作 `{topic}` 使用，先从构造函数、核心成员和相关类关系入手。")
    return unique(points)


def edge_points(page: ClassPage) -> list[str]:
    points: list[str] = []
    if is_qobject_related(page):
        points.append("不要跨线程直接调用依赖对象状态的成员函数；需要跨线程协作时使用 queued signal/slot 或 QMetaObject::invokeMethod。")
        points.append("带 parent 的对象会随父对象析构而销毁；不要再用其它所有权机制重复释放同一个 QObject。")
    if is_widget_related(page):
        points.append("不要用固定坐标替代布局系统；字体、缩放、翻译文本和平台风格都会改变控件尺寸。")
    if is_abstract(page):
        points.append("抽象基类的文档重点通常在重写契约，而不是直接构造；实现派生类时要维护基类要求的信号、状态和返回值约定。")
    if is_model_related(page):
        points.append("模型数据变化必须通知视图；结构变化、数据变化和布局变化对应不同信号，不能混用。")
    if is_io_related(page):
        points.append("检查返回值和 errorString()；文件、网络和流式 API 的失败通常不是异常，而是状态。")
    if is_container_related(page):
        points.append("遍历时避免一边持有旧迭代器一边修改容器；必要时先收集键或索引再修改。")
    if is_thread_related(page):
        points.append("避免在持锁期间发信号、等待线程或执行用户回调；这些组合很容易造成死锁或重入。")
    if has_detail_title(page, "Thread Safety") or "thread-safe" in page.raw_detail_text.lower():
        points.append("线程安全说明要按类页逐条看：reentrant、thread-safe 和 GUI-thread-only 含义不同。")
    if not points:
        points.append("先确认对象由谁创建、由谁销毁、是否可拷贝，以及调用是否依赖事件循环或平台资源。")
    return unique(points)


def is_abstract(page: ClassPage) -> bool:
    return page.class_name.startswith("QAbstract") or any(is_pure_virtual_signature(item) for item in all_member_items(page))


def is_qobject_related(page: ClassPage) -> bool:
    text = inheritance_text(page)
    return "QObject" in text or page.class_name in {"QObject", "QCoreApplication", "QGuiApplication", "QApplication"}


def is_widget_related(page: ClassPage) -> bool:
    text = inheritance_text(page)
    name = page.class_name
    return "QWidget" in text or "QLayout" in text or name.endswith("Widget") or "Widget" in name or "Layout" in name


def is_event_related(page: ClassPage) -> bool:
    text = inheritance_text(page)
    return "QEvent" in text or page.class_name.endswith("Event")


def is_model_related(page: ClassPage) -> bool:
    return "Model" in page.class_name or any("QModelIndex" in item for item in all_member_items(page))


def is_io_related(page: ClassPage) -> bool:
    name = page.class_name
    text = inheritance_text(page)
    needles = ["File", "Dir", "IODevice", "Stream", "Socket", "Network", "Buffer", "Process"]
    return any(word in name or word in text for word in needles)


def is_container_related(page: ClassPage) -> bool:
    name = page.class_name
    needles = ["List", "Map", "Hash", "Vector", "Queue", "Stack", "Set", "Array", "Cache", "Iterator"]
    return any(word in name for word in needles)


def is_thread_related(page: ClassPage) -> bool:
    name = page.class_name
    needles = ["Thread", "Mutex", "Lock", "Semaphore", "WaitCondition", "Atomic", "Future"]
    return any(word in name for word in needles)


def has_detail_title(page: ClassPage, title: str) -> bool:
    return any(existing.lower() == title.lower() for existing, _ in page.detailed_sections)


def pure_virtual_functions(page: ClassPage) -> list[str]:
    names = []
    for item in all_member_items(page):
        if not is_pure_virtual_signature(item):
            continue
        match = re.search(r"([A-Za-z_][A-Za-z0-9_:~]*)\s*\(", item)
        if match:
            names.append(match.group(1))
    return unique(names)


def is_pure_virtual_signature(item: str) -> bool:
    return bool(re.search(r"=\s*0\s*$", item))


def all_member_items(page: ClassPage) -> list[str]:
    return (
        page.properties
        + page.public_functions
        + page.public_slots
        + page.signals
        + page.static_members
        + page.protected_functions
        + page.related_non_members
        + page.macros
    )


def inheritance_text(page: ClassPage) -> str:
    return " ".join([page.inherits or "", page.class_name])


def unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def render_build_section(lines: list[str], page: ClassPage) -> None:
    lines.append("## 2. 构建与包含")
    lines.append("")
    lines.append("CMake 工程需要链接所属模块；头文件只负责声明可见性，不会替代链接步骤。")
    if page.cmake:
        lines.append("")
        lines.append("```cmake")
        lines.append(page.cmake)
        lines.append("```")
    if page.header:
        lines.append("")
        lines.append("```cpp")
        lines.append(page.header)
        lines.append("```")
    if page.qmake:
        lines.append("")
        lines.append(f"qmake 工程使用：`{page.qmake}`。")
    lines.append("")


def render_minimal_example(lines: list[str], page: ClassPage, topic: str) -> None:
    lines.append("## 3. 最小可用代码")
    lines.append("")
    lines.append("下面的骨架只展示对象进入 Qt 程序的最小方式；具体参数、目标对象和错误处理要按本类的语义补全。")
    lines.append("")
    lines.append("```cpp")
    if page.class_name == "QBoxLayout":
        render_qboxlayout_example(lines)
    elif page.class_name == "QTimer":
        render_qtimer_example(lines)
    else:
        render_generic_example(lines, page)
    lines.append("```")
    lines.append("")
    example = select_example_code(page)
    if example:
        lines.append("### 3.1 文档中的使用片段")
        lines.append("")
        lines.append("```cpp")
        lines.extend(example.splitlines())
        lines.append("```")
        lines.append("")


def render_qboxlayout_example(lines: list[str]) -> None:
    lines.extend(
        [
            "#include <QApplication>",
            "#include <QBoxLayout>",
            "#include <QLabel>",
            "#include <QLineEdit>",
            "#include <QPushButton>",
            "#include <QWidget>",
            "",
            "int main(int argc, char *argv[])",
            "{",
            "    QApplication app(argc, argv);",
            "",
            "    QWidget window;",
            "    auto *layout = new QBoxLayout(QBoxLayout::TopToBottom, &window);",
            '    layout->addWidget(new QLabel("用户名："));',
            "    layout->addWidget(new QLineEdit);",
            '    layout->addWidget(new QPushButton("登录"));',
            "",
            "    window.resize(360, 180);",
            "    window.show();",
            "    return app.exec();",
            "}",
        ]
    )


def render_qtimer_example(lines: list[str]) -> None:
    lines.extend(
        [
            "#include <QCoreApplication>",
            "#include <QDebug>",
            "#include <QTimer>",
            "",
            "int main(int argc, char *argv[])",
            "{",
            "    QCoreApplication app(argc, argv);",
            "",
            "    QTimer timer;",
            "    timer.setInterval(1000);",
            "    QObject::connect(&timer, &QTimer::timeout, [] {",
            '        qInfo() << "tick";',
            "    });",
            "    timer.start();",
            "",
            "    QTimer::singleShot(5000, &app, &QCoreApplication::quit);",
            "    return app.exec();",
            "}",
        ]
    )


def render_generic_example(lines: list[str], page: ClassPage) -> None:
    if is_abstract(page):
        if page.header:
            lines.append(page.header)
            lines.append("")
        derived = page.inherited_by[0] if page.inherited_by else "合适的具体派生类"
        lines.append(f"// {page.class_name} 是抽象类型，不能直接实例化。")
        lines.append(f"// 从 `{derived}` 或自行实现派生类开始使用。")
    elif can_default_construct(page):
        render_complete_default_construction_example(lines, page)
    else:
        if page.header:
            lines.append(page.header)
            lines.append("")
        lines.append(f"void use{safe_identifier(page.class_name)}(/* 按文档传入依赖参数 */)")
        lines.append("{")
        lines.append(f"    // 按 {page.class_name} 的构造函数契约创建对象。")
        lines.append("    // 创建后检查操作结果、状态或通知信号。")
        lines.append("}")


def render_complete_default_construction_example(lines: list[str], page: ClassPage) -> None:
    variable = example_variable_name(page.class_name)
    if is_widget_related(page) and ("QWidget" in inheritance_text(page) or page.class_name.endswith("Widget")):
        lines.append("#include <QApplication>")
        if page.header:
            lines.append(page.header)
        lines.append("")
        lines.append("int main(int argc, char *argv[])")
        lines.append("{")
        lines.append("    QApplication app(argc, argv);")
        lines.append("")
        lines.append(f"    {page.class_name} {variable};")
        lines.append(f"    {variable}.show();")
        lines.append("    return app.exec();")
        lines.append("}")
        return
    if is_qobject_related(page):
        lines.append("#include <QCoreApplication>")
        if page.header:
            lines.append(page.header)
        lines.append("")
        lines.append("int main(int argc, char *argv[])")
        lines.append("{")
        lines.append("    QCoreApplication app(argc, argv);")
        lines.append(f"    {page.class_name} {variable};")
        lines.append(f"    (void){variable};")
        lines.append("    return 0;")
        lines.append("}")
        return
    if page.header:
        lines.append(page.header)
        lines.append("")
    lines.append("int main()")
    lines.append("{")
    lines.append(f"    {page.class_name} {variable};")
    lines.append(f"    (void){variable};")
    lines.append("    return 0;")
    lines.append("}")


def can_default_construct(page: ClassPage) -> bool:
    pattern = re.compile(rf"\b{re.escape(page.class_name)}\s*\(([^)]*)\)")
    for item in page.public_functions:
        match = pattern.search(item)
        if not match:
            continue
        params = match.group(1).strip()
        if not params or all("=" in parameter for parameter in split_top_level_parameters(params)):
            return True
    return False


def split_top_level_parameters(params: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    for index, char in enumerate(params):
        if char in "(<[{" :
            depth += 1
        elif char in ")>]}" and depth:
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(params[start:index].strip())
            start = index + 1
    parts.append(params[start:].strip())
    return [part for part in parts if part]


def example_variable_name(class_name: str) -> str:
    tail = class_name.split("::")[-1]
    compact = re.sub(r"^Q", "", tail)
    if not compact:
        return "object"
    return compact[:1].lower() + compact[1:]


def safe_identifier(class_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "", class_name.replace("::", ""))


def select_example_code(page: ClassPage) -> str:
    for block in page.code_blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        nonempty = [line for line in lines if line.strip()]
        if not 2 <= len(nonempty) <= 60:
            continue
        text = "\n".join(lines).strip()
        if page.class_name in text or ("Q" in text and ";" in text):
            return text
    return ""


def render_core_model(lines: list[str], page: ClassPage, topic: str) -> None:
    lines.append("## 4. 核心使用模型")
    lines.append("")
    lines.append("可以把使用过程拆成以下几个问题：")
    points = usage_points(page, topic)
    for index, point in enumerate(points, start=1):
        lines.append(f"{index}. {point}")
    if page.public_types:
        shown = "、".join(f"`{member_type_name(item)}`" for item in page.public_types[:6])
        lines.append(f"{len(points) + 1}. 公开类型中常见的状态、枚举或标志包括：{shown}；先确认取值含义，再把它们传给成员函数。")
    lines.append("")


def render_member_guide(lines: list[str], page: ClassPage) -> None:
    groups = [
        ("属性", page.properties, "属性表示可观察状态。先区分只读、可写和 bindable 属性，状态变化优先监听相应 NOTIFY 信号。"),
        ("公共函数", page.public_functions, "公共函数是日常调用入口。先看构造、核心操作和返回值，再确认失败或边界条件。"),
        ("公共槽", page.public_slots, "槽通常代表可由信号触发的状态切换或命令操作；连接时注意对象生命周期和线程上下文。"),
        ("信号", page.signals, "信号描述异步状态变化。优先响应信号，而不是在定时器中轮询对象内部状态。"),
        ("静态公共成员", page.static_members, "静态成员通常用于工厂、全局查询或类型级配置；确认它是否依赖应用初始化或平台资源。"),
        ("受保护函数", page.protected_functions, "受保护函数是派生扩展点。重写时保持基类契约，并在需要时调用基类实现。"),
        ("相关非成员", page.related_non_members, "非成员函数往往承担比较、序列化、流输出或辅助创建等职责，适合与对象 API 配套使用。"),
        ("宏", page.macros, "宏通常影响编译期能力或平台行为；使用前确认其适用范围和包含顺序。"),
    ]
    groups = [(title, items, explanation) for title, items, explanation in groups if items]
    lines.append("## 5. 关键 API 如何阅读")
    if not groups:
        lines.append("")
        lines.append("该类页没有单独列出常规成员分组。优先从构造函数、参数类型、返回值和相关非成员函数确认其使用方式。")
    for title, items, explanation in groups:
        lines.append("")
        lines.append(f"### {title}")
        lines.append("")
        lines.append(explanation)
        shown = "、".join(f"`{member_name(item)}`" for item in items[:6])
        if shown:
            suffix = f" 等 {len(items)} 项" if len(items) > 6 else ""
            lines.append("")
            lines.append(f"本组优先关注：{shown}{suffix}。")
    lines.append("")


def render_detail_guide(lines: list[str], page: ClassPage) -> None:
    detail_titles = [translate_section_title(title) for title, _ in page.detailed_sections]
    lines.append("## 6. 状态、类型与扩展点")
    lines.append("")
    if page.public_types:
        lines.append("### 6.1 公开类型")
        lines.append("")
        lines.append("以下类型通常承载枚举、标志、策略或结果值。不要只记名称，应确认每个取值触发的实际行为：")
        lines.append("")
        for item in page.public_types[:12]:
            lines.append(f"- `{item}`")
        if len(page.public_types) > 12:
            lines.append(f"- 以及其他 {len(page.public_types) - 12} 项")
        lines.append("")
    if detail_titles:
        lines.append("### 6.2 官方详细说明的阅读重点")
        lines.append("")
        shown = "、".join(f"`{title}`" for title in detail_titles[:10])
        lines.append(f"离线类页额外覆盖：{shown}。这些章节通常说明成员函数列表之外的状态机、线程边界、扩展契约或使用限制；遇到行为不符合预期时，应先回到对应章节核对。")
        lines.append("")
    if not page.public_types and not detail_titles:
        lines.append("本类没有单独列出的公开类型或概念章节。重点应放在构造方式、核心成员的前置条件，以及它与参数类型之间的协作关系。")
        lines.append("")


def render_full_member_docs(lines: list[str], page: ClassPage) -> None:
    lines.append("## 9. 逐项 API 说明")
    if not page.member_docs:
        lines.append("")
        lines.append("该类页没有提供可展开的成员说明。此类通常以类型定义、模板能力或相关非成员函数为主要接口。")
        lines.append("")
        return

    category_order = ("成员类型", "属性", "成员函数", "信号", "宏")
    for category in category_order:
        docs = [doc for doc in page.member_docs if doc.category == category]
        if not docs:
            continue
        lines.append("")
        lines.append(f"### {category}")
        for doc in docs:
            render_single_member_doc(lines, page, doc)
    lines.append("")


def render_single_member_doc(lines: list[str], page: ClassPage, doc: MemberDoc) -> None:
    signature = doc.signatures[0]
    if len(doc.signatures) == 1:
        lines.append("")
        lines.append(f"#### `{signature}`")
    else:
        lines.append("")
        lines.append(f"#### `{documentation_member_name(signature)}` 的重载")
        lines.append("")
        lines.append("签名：")
        for overload in doc.signatures:
            lines.append(f"- `{overload}`")

    lines.append("")
    lines.append(f"**作用：** {member_purpose(page, doc)}")

    translated_notes: list[str] = []
    for paragraph in doc.paragraphs:
        translated = translate_member_paragraph(paragraph, page, doc)
        if translated:
            translated_notes.append(translated)
    translated_notes.extend(member_behavior_rules(page, doc))

    if translated_notes:
        lines.append("")
        lines.append("**行为与规则：**")
        for note in unique(translated_notes):
            lines.append(f"- {note}")

    if doc.value_rows:
        lines.append("")
        lines.append("**取值：**")
        lines.append("")
        lines.append("| 常量 | 值 | 含义 |")
        lines.append("| --- | --- | --- |")
        for row in doc.value_rows:
            constant = escape_table_cell(row[0])
            value = escape_table_cell(row[1]) if len(row) > 1 else ""
            description = escape_table_cell(row[2]) if len(row) > 2 else ""
            lines.append(f"| `{constant}` | `{value}` | {enum_value_purpose(constant, description)} |")

    if doc.code_blocks:
        lines.append("")
        lines.append("**对应代码：**")
        for block in doc.code_blocks:
            lines.append("")
            lines.append("```cpp")
            lines.extend(block.splitlines())
            lines.append("```")

def documentation_member_name(signature: str) -> str:
    signature = re.sub(r"\[[^\]]+\]\s*", "", signature).strip()
    enum_match = re.search(r"\benum(?:\s+class)?\s+(?:[A-Za-z_][A-Za-z0-9_:]*::)?([A-Za-z_][A-Za-z0-9_]*)", signature)
    if enum_match:
        return enum_match.group(1)
    scoped_names = re.findall(r"([~A-Za-z_][A-Za-z0-9_:]*)::([~A-Za-z_][A-Za-z0-9_]*)\s*\(", signature)
    if scoped_names:
        return scoped_names[0][1]
    names = re.findall(r"([~A-Za-z_][A-Za-z0-9_]*)\s*\(", signature)
    if names:
        return names[0]
    property_match = re.search(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", signature)
    if property_match:
        return property_match.group(1)
    return signature


def member_purpose(page: ClassPage, doc: MemberDoc) -> str:
    signature = doc.signatures[0]
    name = documentation_member_name(signature)
    lower_name = name.lstrip("~")
    if doc.category == "成员类型":
        return f"定义 `{name}` 的可选取值、策略或辅助类型，用来表达 `{page.class_name}` 的状态和行为模式。"
    if doc.category == "属性":
        return f"`{name}` 属性用于保存或公开 `{page.class_name}` 的一项状态；通过属性访问器读取或修改时，要同时留意其通知和默认值。"
    if is_signal_signature(signature):
        return f"这是 `{page.class_name}` 的状态通知信号；当签名所代表的事件发生时，已连接的槽或 lambda 会被调用。"
    if name.startswith("~"):
        return f"销毁 `{page.class_name}` 对象；析构时是否释放关联资源要按对象所有权规则判断。"
    if lower_name == page.class_name.split("::")[-1]:
        return f"构造 `{page.class_name}` 对象，并按参数建立初始状态或父子对象关系。"

    for prefix, description in [
        ("set", "设置或修改对象状态"),
        ("add", "向对象管理的集合、布局或关系中追加内容"),
        ("insert", "在指定位置插入内容"),
        ("remove", "从对象中移除内容"),
        ("take", "取出内容并把后续所有权交给调用方"),
        ("clear", "清空或重置当前状态"),
        ("start", "启动或重新启动对象的工作过程"),
        ("stop", "停止正在进行的工作过程"),
        ("pause", "暂停当前过程"),
        ("resume", "恢复被暂停的过程"),
        ("open", "打开底层资源或建立可用状态"),
        ("close", "关闭底层资源并结束当前使用"),
        ("read", "读取数据或查询可读内容"),
        ("write", "写入数据或提交内容"),
        ("find", "查找满足条件的对象、索引或结果"),
        ("create", "创建新的关联对象或资源"),
        ("connect", "建立对象之间的通信连接"),
        ("disconnect", "解除已有连接"),
        ("begin", "开始一段需要成对结束的操作或通知"),
        ("end", "结束与 begin 对应的操作或通知"),
        ("is", "查询布尔状态"),
        ("has", "查询是否具备某项能力或状态"),
    ]:
        if lower_name.startswith(prefix):
            return f"`{name}()` 用于{description}。"
    return f"`{name}()` 是 `{page.class_name}` 的公开操作，用于完成签名所描述的查询、配置或行为调用。"


def is_signal_signature(signature: str) -> bool:
    return "[signal]" in signature.lower()


def translate_member_paragraph(text: str, page: ClassPage, doc: MemberDoc) -> str:
    source = normalize_text(text)
    if not source:
        return ""
    name = documentation_member_name(doc.signatures[0])
    lower = source.lower()

    if lower.startswith("reimplements:"):
        parent = source.split(":", 1)[1].strip()
        return f"这是对基类 `{parent}` 的重写；通常由 Qt 框架在相应生命周期中调用。"
    if lower.startswith("this property supports"):
        return "该属性支持 `QProperty` 绑定，可通过 bindable 访问器接入绑定系统。"
    if lower.startswith("this property holds"):
        return f"该属性保存 `{documentation_member_name(doc.signatures[0])}` 对应的运行时状态。"
    if lower.startswith("the default value for this property is"):
        return "该属性有明确默认值；创建对象后若未主动设置，会从默认状态开始工作。"
    if lower.startswith("returns "):
        return f"返回 `{documentation_member_name(doc.signatures[0])}()` 查询到的结果；无效状态的特殊返回值见下方规则。"
    if lower.startswith("sets "):
        return f"调用后会修改 `{documentation_member_name(doc.signatures[0])}()` 相关的对象状态。"
    if lower.startswith("adds "):
        return f"调用后会把传入对象追加到 `{page.class_name}` 管理的结构中。"
    if lower.startswith("inserts "):
        return "调用后会把传入对象插入到指定位置；索引的边界和负值语义见下方规则。"
    if lower.startswith("removes "):
        return "调用后会从当前对象中移除目标内容；是否同时销毁目标对象要看所有权规则。"
    if lower.startswith("constructs "):
        return f"使用签名中给出的参数构造 `{page.class_name}` 对象。"
    if lower.startswith("destroys "):
        return f"销毁 `{page.class_name}` 对象。"
    if lower.startswith("starts or restarts "):
        return "启动或重新启动当前过程；若对象已在运行，通常会以新的参数重新开始。"
    if lower.startswith("starts "):
        return "启动当前过程。"
    if lower.startswith("stops "):
        return "停止当前过程。"
    if lower.startswith("pauses "):
        return "暂停当前过程。"
    if lower.startswith("resumes "):
        return "恢复此前暂停的过程。"
    if lower.startswith("this signal is emitted"):
        return "该信号在相应状态变化发生时发出。"
    if lower.startswith("this static function calls"):
        return "这是静态便捷函数：无需长期保存对象，即可在指定时机调用槽或回调。"
    if lower.startswith("this function is reentrant"):
        return "该函数是可重入的；不同线程可分别在不同实例上调用，但不代表同一实例可无同步地并发访问。"
    if lower.startswith("this function is thread-safe"):
        return "该函数标记为线程安全；仍需遵守对象生命周期和回调/锁的调用约束。"
    if lower.startswith("this function was introduced in qt"):
        version = re.sub(r"^This function was introduced in\s+", "", source, flags=re.I).rstrip(".")
        return f"该函数从 `{version}` 开始提供，使用时要确认项目的最低 Qt 版本。"
    if lower.startswith("note:"):
        note = translate_doc_fragment(source[len("Note:"):].strip())
        if not re.search(r"[A-Za-z]{4,}", note):
            return f"注意：{note}"
    return ""


def member_behavior_rules(page: ClassPage, doc: MemberDoc) -> list[str]:
    source = "\n".join(doc.paragraphs).lower()
    rules: list[str] = []
    name = documentation_member_name(doc.signatures[0])

    if "ownership of" in source and "passed to" in source:
        rules.append("传入对象的所有权会转交给当前对象；交接后不要再由其它智能指针或手工 `delete` 重复释放。")
    if "becomes a child" in source:
        rules.append("加入后，传入对象成为当前对象管理的子对象；其生命周期和几何/状态更新会随父对象体系变化。")
    if "only one top-level layout" in source:
        rules.append("一个 `QWidget` 只能有一个顶层布局；传入 parent 的布局会直接成为该控件的顶层布局。")
    if "default value" in source:
        rules.append("文档定义了默认值；依赖默认状态前，要确认它是否适合当前平台、样式或业务场景。")
    if "reentrant" in source:
        rules.append("该成员是可重入的：不同线程操作各自对象通常安全，但同一个实例的并发访问仍需同步。")
    if "thread-safe" in source:
        rules.append("该成员标记为线程安全；仍不能忽略对象销毁、回调重入和关联对象线程归属。")
    if "event loop" in source:
        rules.append("该行为依赖目标线程的事件循环；线程没有运行事件循环时，延迟回调、定时器或投递事件不会按预期执行。")
    if "context" in source and "destroyed" in source:
        rules.append("传入 context 后，context 在操作完成前销毁会阻止回调执行；lambda 捕获对象时优先使用该形式保护生命周期。")
    if "negative interval" in source:
        rules.append("Qt 6.10 起负时间间隔会报警并被重置为 1ms；业务代码仍应在调用前主动校验。")
    if "zero-timer" in source or "interval of 0" in source:
        rules.append("0 间隔会在事件队列暂时清空后尽快触发；持续占用事件循环容易造成界面卡顿和不可预测的调度。")
    if "stopped and restarted" in source:
        rules.append("对象已运行时再次启动或修改时间间隔会先停止再重启；依赖运行 ID 或剩余时间的代码应重新读取状态。")
    if "single-shot" in source and ("only once" in source or "fires only once" in source):
        rules.append("单次模式只触发一次，触发后对象转为未激活；需要再次触发时必须重新启动。")
    if "stretch factor applies only" in source:
        rules.append("stretch 只沿布局主轴分配剩余空间；所有项 stretch 均为 0 时，Qt 会回退到 `QSizePolicy` 协商。")
    if "default alignment is 0" in source:
        rules.append("默认 alignment 为 0，控件会填满自己的布局单元；需要局部对齐时显式传入 `Qt::Alignment`。")
    if "negative or" in source and "index" in source and "added at the end" in source:
        rules.append("插入接口的负索引通常表示追加到末尾；其余索引必须处于 `0..count()` 的有效范围。")
    if "returns" in source and ("-1" in source or "invalid" in source):
        rules.append("返回值可能使用 `-1`、`0`、`Invalid` 或空值表示未运行、无效或已到期状态；调用方不能把这些值当作正常结果。")
    if name.startswith("set") and "running" in source:
        rules.append("该 setter 可能影响正在运行的对象；设置后应重新检查活动状态、ID、事件安排或缓存结果。")
    if "layout's widgets aren't destroyed" in source:
        rules.append("销毁布局本身不会直接销毁已管理的控件；控件通常由父 `QWidget` 的对象树负责销毁。")
    if "creates a connection" in source:
        rules.append("该接口会建立信号到槽或回调的连接，并返回 `QMetaObject::Connection` 供后续断开或保存。")
    if "equivalent to calling" in source:
        rules.append("这是对常规 Qt 调用的便捷封装；需要精细控制连接类型、上下文或生命周期时可改用底层 API。")
    if "not available when" in source:
        rules.append("该重载可能受编译期开关限制；项目关闭相应特性时，应改用文档指定的替代重载。")
    if "overloaded function" in source or "this slot is overloaded" in source:
        rules.append("该成员存在重载；连接信号槽时使用 `qOverload` 或 lambda 明确选择目标签名。")
    if "parameter can be" in source and "chrono" in source:
        rules.append("时间参数同时支持传统整数毫秒和 `std::chrono` 时长；新代码优先使用 `std::chrono` 避免单位混淆。")
    if "read-only" in doc.signatures[0].lower():
        rules.append("该属性是只读状态，只能通过对象运行过程或对应操作间接改变，不能直接写入。")
    if "bindable" in doc.signatures[0].lower():
        rules.append("该属性支持绑定接口；需要响应式状态同步时，可通过对应 `bindable...()` 访问器接入 `QProperty`。")
    return unique(rules)


def enum_value_purpose(constant: str, description: str) -> str:
    source = description.lower()
    if "left to right" in source:
        return "沿水平方向从左到右排列。"
    if "right to left" in source:
        return "沿水平方向从右到左排列。"
    if "top to bottom" in source:
        return "沿垂直方向从上到下排列。"
    if "bottom to top" in source:
        return "沿垂直方向从下到上排列。"
    if "not running" in source or "stopped" in source:
        return "表示对象未运行或已经停止的状态。"
    if "running" in source:
        return "表示对象正在运行或处理中的状态。"
    if "paused" in source:
        return "表示对象暂时暂停，可在满足条件后恢复。"
    if "read" in source and "write" in source:
        return "表示读写能力或读写模式的组合。"
    if "read" in source:
        return "表示读取相关的状态、能力或模式。"
    if "write" in source:
        return "表示写入相关的状态、能力或模式。"
    if "default" in source:
        return "表示默认策略或由 Qt 自动选择的行为。"
    return f"`{constant}` 是该类型定义的一种状态、策略或标志取值；与其它取值的区别由使用位置决定。"


def translate_doc_fragment(text: str) -> str:
    result = text.strip().rstrip(".")
    phrases = [
        ("the timeout interval in milliseconds", "以毫秒为单位的超时间隔"),
        ("the remaining time in milliseconds", "以毫秒为单位的剩余时间"),
        ("whether the timer is a single-shot timer", "定时器是否为单次定时器"),
        ("the direction of a box layout", "盒式布局的排列方向"),
        ("the direction of the box", "当前盒式布局的方向"),
        ("the current thread", "当前线程"),
        ("the parent widget", "父控件"),
        ("the parent object", "父对象"),
        ("the given parent", "给定的父对象"),
        ("the specified", "指定的"),
        ("the current", "当前"),
        ("this layout", "当前布局"),
        ("this timer", "当前定时器"),
        ("this object", "当前对象"),
        ("this function", "该函数"),
        ("this property", "该属性"),
        ("the timer", "定时器"),
        ("the layout", "布局"),
        ("the widget", "控件"),
        ("the item", "项目"),
        ("the interval", "时间间隔"),
        ("the value", "该值"),
        ("if the timer is inactive", "若定时器未运行"),
        ("if the timer is running", "若定时器正在运行"),
        ("if the timer is overdue", "若定时器已到期"),
        ("only once", "仅一次"),
        ("every", "每隔"),
        ("milliseconds", "毫秒"),
        ("milliseconds", "毫秒"),
        ("running", "运行中"),
        ("inactive", "未激活"),
        ("active", "激活"),
        ("default value", "默认值"),
        ("event loop", "事件循环"),
        ("signal", "信号"),
        ("slot", "槽"),
        ("parent", "父对象"),
        ("child", "子对象"),
        ("direction", "方向"),
        ("stretch factor", "伸缩因子"),
        ("stretch", "伸缩"),
        ("spacing", "间距"),
        ("size", "尺寸"),
        ("index", "索引"),
        ("layout", "布局"),
        ("widget", "控件"),
        ("timer", "定时器"),
        ("interval", "时间间隔"),
    ]
    for english, chinese in phrases:
        result = re.sub(re.escape(english), chinese, result, flags=re.I)
    return translate_phrase(result)


def render_member_sections(lines: list[str], page: ClassPage) -> None:
    lines.append("## 10. API 速查表")
    lines.append("")
    lines.append("| 类别 | API | 是做什么的 | 使用时重点注意 |")
    lines.append("| --- | --- | --- | --- |")
    if page.member_docs:
        for doc in page.member_docs:
            purpose = member_purpose(page, doc)
            caution = member_caution(doc)
            for signature in doc.signatures:
                lines.append(
                    f"| {doc.category} | `{escape_table_cell(signature)}` | "
                    f"{purpose} | {caution} |"
                )
    else:
        groups = [
            ("公共类型", page.public_types),
            ("属性", page.properties),
            ("公共函数", page.public_functions),
            ("公共槽", page.public_slots),
            ("信号", page.signals),
            ("静态公共成员", page.static_members),
            ("受保护函数", page.protected_functions),
            ("相关非成员", page.related_non_members),
            ("宏", page.macros),
        ]
        for title, items in groups:
            for item in items:
                lines.append(f"| {title} | `{escape_table_cell(item)}` | {member_focus(title)} | {member_focus(title)} |")
        if not any(items for _, items in groups):
            lines.append("| 类页结构 | 未列出常规成员表 | 结合构造函数、相关类型和详细说明阅读。 | 确认对象生命周期和前置条件。 |")
    lines.append("")


def member_caution(doc: MemberDoc) -> str:
    signature = doc.signatures[0]
    name = documentation_member_name(signature)
    lower_name = name.lstrip("~")
    if doc.category == "成员类型":
        return "先确认每个枚举或标志取值的状态语义。"
    if doc.category == "属性":
        return "确认只读/可写、默认值、绑定能力和状态变更通知。"
    if is_signal_signature(signature):
        return "连接时提供 context，并注意发射线程与接收对象生命周期。"
    if lower_name.startswith("take"):
        return "返回后通常由调用方接管对象或布局项的后续释放。"
    if lower_name.startswith(("add", "insert")):
        return "确认加入后的父子关系、所有权以及索引或伸缩等附加参数。"
    if lower_name.startswith(("set", "start", "stop", "open", "close")):
        return "调用可能改变对象状态；检查是否需要事件循环、资源已打开或线程归属正确。"
    if lower_name.startswith(("read", "write")):
        return "检查返回值、错误状态和读写位置，不能把失败当作异常自动处理。"
    if lower_name.startswith(("begin", "end")):
        return "必须与对应的 begin/end 成对调用，避免让框架观察到不一致状态。"
    return "结合本节的行为与规则确认参数、返回值、版本和所有权约定。"


def render_edges(lines: list[str], page: ClassPage) -> None:
    points = edge_points(page)
    if not points:
        return
    lines.append("## 7. 常见误区与排查顺序")
    for index, point in enumerate(points, start=1):
        lines.append("")
        lines.append(f"### 7.{index} {edge_title(page, index)}")
        lines.append("")
        lines.append(point)
    lines.append("")


def render_extension_section(lines: list[str], page: ClassPage) -> None:
    lines.append("## 8. 进一步延伸：它和哪些类型协作")
    lines.append("")
    if page.inherits:
        lines.append(f"- 上级类型：`{page.inherits}`。先理解基类提供的对象模型和通用契约，再阅读本类新增的能力。")
    if page.inherited_by:
        shown = "、".join(f"`{name}`" for name in page.inherited_by[:8])
        suffix = f" 等 {len(page.inherited_by)} 个类型" if len(page.inherited_by) > 8 else ""
        lines.append(f"- 常见派生类型：{shown}{suffix}。派生类通常给抽象能力补上具体策略或平台实现。")
    detail_titles = [title for title, _ in page.detailed_sections]
    if detail_titles:
        shown = "、".join(f"`{translate_section_title(title)}`" for title in detail_titles[:8])
        lines.append(f"- 文档重点：{shown}。")
    if not page.inherits and not page.inherited_by:
        lines.append("- 先从本类的构造函数、核心成员函数和参数类型反向查找协作对象；Qt 的值类型通常通过返回值、容器或流 API 组合。")
    lines.append("")


def member_type_name(item: str) -> str:
    match = re.search(r"(?:class|struct|enum(?:\s+class)?|typedef|using)?\s*([A-Za-z_][A-Za-z0-9_:<>]*)", item)
    return match.group(1) if match else item


def member_name(item: str) -> str:
    names = re.findall(r"([~A-Za-z_][A-Za-z0-9_:]*)\s*\(", item)
    if names:
        return names[-1]
    property_match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", item)
    if property_match:
        return property_match.group(1)
    return item


def escape_table_cell(item: str) -> str:
    return item.replace("|", "\\|").replace("\n", " ")


def member_focus(title: str) -> str:
    focuses = {
        "公共类型": "确认枚举、标志或策略的每个取值。",
        "属性": "区分读写、绑定和状态变化通知。",
        "公共函数": "检查参数前置条件、返回值和所有权。",
        "公共槽": "适合命令式调用，也可由信号触发。",
        "信号": "响应异步变化，不要依赖轮询。",
        "静态公共成员": "确认是否依赖初始化或全局状态。",
        "受保护函数": "仅供派生类重写或调用。",
        "相关非成员": "多用于辅助、比较或序列化。",
        "宏": "影响编译期或平台相关行为。",
    }
    return focuses[title]


def edge_title(page: ClassPage, index: int) -> str:
    titles: list[str] = []
    if is_qobject_related(page):
        titles.extend(["对象归属与跨线程调用", "父子对象与重复释放"])
    if is_widget_related(page):
        titles.append("界面对象不能绕过布局和 GUI 线程规则")
    if is_abstract(page):
        titles.append("不要把抽象类型当作完整实现")
    if is_model_related(page):
        titles.append("模型变更必须发出正确通知")
    if is_io_related(page):
        titles.append("I/O 失败是状态，不一定是异常")
    if is_container_related(page):
        titles.append("修改容器时注意迭代器和共享数据")
    if is_thread_related(page):
        titles.append("阻塞、锁和回调组合要防止死锁")
    if has_detail_title(page, "Thread Safety") or "thread-safe" in page.raw_detail_text.lower():
        titles.append("不要把可重入和线程安全混为一谈")
    if index <= len(titles):
        return titles[index - 1]
    return "先确认生命周期、所有权和调用前置条件"


def render_summary(lines: list[str], page: ClassPage, topic: str) -> None:
    lines.append("---")
    lines.append("")
    lines.append("### 一句话总结")
    lines.append("")
    summary = f"`{page.class_name}` 是 {topic}；"
    if is_abstract(page):
        summary += "把它当作派生实现必须遵守的契约，重点看纯虚函数、状态变化和扩展钩子。"
    elif is_qobject_related(page):
        summary += "用 QObject 的生命周期、事件循环和信号槽模型理解它，再结合本类的状态与核心操作。"
    elif is_io_related(page):
        summary += "按资源或数据通道的生命周期组织代码，并始终检查状态、错误和异步完成时机。"
    elif is_container_related(page):
        summary += "在基本容器操作之外，留意值语义、共享数据和迭代器有效性。"
    else:
        summary += "先从构造方式、核心成员和协作类型建立使用流程，再用 API 速查表核对细节。"
    lines.append(summary)
    lines.append("")


def translate_section_title(title: str) -> str:
    key = slugify(title)
    if key in DETAIL_SUBSECTION_TITLES:
        return DETAIL_SUBSECTION_TITLES[key]
    if title in DETAIL_SUBSECTION_TITLES.values():
        return title
    text = translate_phrase(title)
    if text and not re.search(r"[A-Za-z]{4,}", text):
        return text
    return "相关专题说明"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def guess_qt_target(page: ClassPage) -> str:
    if page.cmake:
        match = re.search(r"Qt6::[A-Za-z0-9_]+", page.cmake)
        if match:
            return match.group(0)
    if page.module_name.startswith("Qt"):
        return "Qt6::" + page.module_name[2:].replace(" ", "")
    return page.module_name


if __name__ == "__main__":
    raise SystemExit(main())
