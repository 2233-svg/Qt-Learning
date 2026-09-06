#!/usr/bin/env python3
"""Replace generic API prose with member-specific Qt documentation.

The script reads the locally installed Qt HTML documentation, matches each
Markdown API heading with its property/member documentation, translates the
useful prose to Simplified Chinese, and rewrites section 5 in place.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
from html.parser import HTMLParser
import http.cookiejar
import json
from pathlib import Path
import re
import threading
import time
import urllib.parse
import urllib.request


MODULES = {
    "QtCharts": "qtcharts",
    "QtConcurrent": "qtconcurrent",
    "QtCore": "qtcore",
    "QtD_Bus": "qtdbus",
    "QtGUI": "qtgui",
    "QtHelp": "qthelp",
    "QtMultimedia": "qtmultimedia",
    "QtNetwork": "qtnetwork",
    "QtPrint_Support": "qtprintsupport",
    "QtQml": "qtqml",
    "QtQuick": "qtquick",
    "QtQuick_3D": "qtquick3d",
    "QtQuick_Controls": "qtquickcontrols",
    "QtShader_Tools": "qtshadertools",
    "QtSpatial_Audio": "qtspatialaudio",
    "QtSQL": "qtsql",
    "QtSVG": "qtsvg",
    "QtTaskTree": "qttasktree",
    "QtTest": "qttestlib",
    "QtUI_Tools": "qtuitools",
    "QtWidgets": "qtwidgets",
    "QtXML": "qtxml",
}

SECTION_5 = "## 5. API 逐个说明"
GENERIC_MARKERS = (
    "调用后检查返回值、状态查询和错误信息",
    "用于计算、查询或取得与",
    "初始化或状态切换时通过",
    "适合直接完成转换、查找、工厂创建或一次性操作",
)
SKIP_PARAGRAPHS = (
    "Access functions:",
    "Notifier signal:",
    "This is an overloaded function.",
)


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag: str, attrs: dict[str, str] | None = None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children: list[Node | str] = []
        self.parent = parent


class TreeParser(HTMLParser):
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.current = self.root
        self.ignored_depth = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in {"script", "style"}:
            self.ignored_depth += 1
        if self.ignored_depth:
            return
        node = Node(tag, dict(attrs), self.current)
        self.current.children.append(node)
        if tag not in self.VOID_TAGS:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        if not self.ignored_depth:
            self.current.children.append(Node(tag.lower(), dict(attrs), self.current))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in {"script", "style"} and self.ignored_depth:
            self.ignored_depth -= 1
            return
        if self.ignored_depth:
            return
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.current = node.parent

    def handle_data(self, data):
        if not self.ignored_depth:
            self.current.children.append(data)


def walk(node: Node):
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def classes(node: Node) -> set[str]:
    return set(node.attrs.get("class", "").split())


def text_of(node: Node | str, code_ticks: bool = True) -> str:
    if isinstance(node, str):
        return node
    content = "".join(text_of(child, code_ticks) for child in node.children)
    should_quote = node.tag == "code" or (
        node.tag in {"a", "i"}
        and node.attrs.get("translate") == "no"
        and re.fullmatch(r"[A-Za-z_][\w:.<>/-]*(?:\(\))?", content.strip())
    )
    if code_ticks and should_quote:
        content = f"`{content.strip('` ')}`"
    if node.tag == "br":
        content += "\n"
    return content


def clean_text(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"`([^`]+)`::([A-Za-z_]\w*)", r"`\1::\2`", value)
    value = re.sub(r"`([^`]+)`\(\)", r"`\1()`", value)
    return value.strip()


def node_markdown(node: Node) -> list[str]:
    """Return useful English prose/list/table blocks from one source node."""
    if node.tag == "p":
        value = clean_text(text_of(node))
        if not value or any(value.startswith(prefix) for prefix in SKIP_PARAGRAPHS):
            return []
        if value in {"Example:", "For example:"}:
            return []
        if re.fullmatch(
            r"(?:This (?:function|property|signal|type)|The notifier signal|These functions?) "
            r"(?:was|were) introduced in Qt [\d.]+\.?",
            value,
        ):
            return []
        if value.startswith("See also "):
            return []
        return [value]

    if node.tag in {"ul", "ol"}:
        result = []
        for child in node.children:
            if isinstance(child, Node) and child.tag == "li":
                value = clean_text(text_of(child))
                if value:
                    result.append(f"- {value}")
        return result

    if node.tag == "div" and classes(node) & {"admonition", "admonition-note", "admonition-warning"}:
        value = clean_text(text_of(node))
        if not value or value.startswith("This is an overloaded function."):
            return []
        if "warning" in classes(node) or value.startswith("Warning:"):
            value = re.sub(r"^Warning:\s*", "", value)
            return [f"WARNING: {value}"]
        value = re.sub(r"^Note:\s*", "", value)
        return [f"NOTE: {value}"]

    table = node if node.tag == "table" else next((item for item in walk(node) if item.tag == "table"), None)
    if table is not None:
        if "alignedsummary" in classes(table):
            return []
        rows = []
        for tr in (item for item in walk(table) if item.tag == "tr"):
            cells = [clean_text(text_of(child)) for child in tr.children if isinstance(child, Node) and child.tag in {"td", "th"}]
            if len(cells) >= 2 and cells[0] != "Constant" and not any("Access functions" in cell for cell in cells):
                description = "; ".join(cell for cell in cells[1:] if cell)
                rows.append(f"- `{cells[0].strip('`')}`: {description}")
        return rows

    return []


def direct_blocks(container: Node) -> list[tuple[Node, list[Node]]]:
    result: list[tuple[Node, list[Node]]] = []
    headings: list[Node] = []
    body: list[Node] = []

    def flush():
        nonlocal headings, body
        for heading in headings:
            result.append((heading, list(body)))
        headings, body = [], []

    for child in container.children:
        if not isinstance(child, Node):
            continue
        if child.tag == "h3":
            flush()
            headings = [child]
        elif child.tag == "div" and "fngroup" in classes(child):
            flush()
            headings = [item for item in child.children if isinstance(item, Node) and item.tag == "h3"]
        elif headings and child.tag != "h2":
            body.append(child)
    flush()
    return result


def member_name(signature: str) -> str:
    signature = signature.strip("` ")
    signature = re.sub(r"^(?:\[[^]]+\]|\([^)]*\))\s*", "", signature)
    if re.match(r"(?:\[anonymous\]\s+)?enum(?:\s*\{|$)", signature):
        return "anonymous"
    prop_match = re.search(r"(?:^|\]\s*)([~\w.]+)\s*(?<!:):(?!:)\s*", signature)
    if prop_match and "(" not in signature:
        return prop_match.group(1).split("::")[-1]
    op_match = re.search(r"::(operator\s*[^ (]+|~?[A-Za-z_]\w*)\s*\(", signature)
    if op_match:
        return re.sub(r"\s+", "", op_match.group(1))
    free_op_match = re.search(r"\b(operator\s*[^ (]+)\s*\(", signature)
    if free_op_match:
        return re.sub(r"\s+", "", free_op_match.group(1))
    callable_matches = re.findall(r"(~?[A-Za-z_]\w*)\s*\(", signature)
    if callable_matches:
        return callable_matches[-1]
    type_match = re.search(r"(?:enum(?:\s+class)?|class|struct|typedef)\s+(?:[\w:]+::)?([A-Za-z_]\w*)", signature)
    if type_match:
        return re.sub(r"flags$", "", type_match.group(1))
    return signature.split("::")[-1].split()[-1]


def looks_like_api_heading(signature: str) -> bool:
    value = signature.strip("` ")
    value = re.sub(r"^(?:\[[^]]+\]|\([^)]*\))\s*", "", value)
    if value.endswith("."):
        return False
    if "(" in value:
        return True
    if re.match(r"(?:enum(?:\s+class)?|class|struct|flags|using|typedef)\b", value):
        return True
    if re.search(r"(?<!:):(?!:)", value):
        return True
    if re.fullmatch(r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)*", value):
        return True
    declaration = re.compile(
        r"(?:(?:extern|static|constexpr|const|unsigned|signed)\s+)*"
        r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)*(?:<[^>]+>)?[\s*&]+"
        r"[A-Za-z_]\w*(?:::[A-Za-z_]\w*)+"
    )
    return bool(declaration.fullmatch(value))


def source_member_name(heading: Node) -> str:
    ident = heading.attrs.get("id", "")
    if ident.endswith("-prop"):
        return ident[:-5]
    if ident.startswith("dtor."):
        return "~" + ident[5:]
    parsed = member_name(clean_text(text_of(heading, code_ticks=False)))
    if parsed and parsed not in {"enum", "class", "struct", "typedef"}:
        return parsed
    ident = re.sub(r"-\d+$", "", ident)
    ident = re.sub(r"-(?:enum|typedef)$", "", ident)
    if ident:
        return ident
    return member_name(clean_text(text_of(heading, code_ticks=False)))


def extract_source(path: Path) -> tuple[dict[str, list[dict]], str]:
    parser = TreeParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    by_name: dict[str, list[dict]] = {}
    brief = ""

    meta = next((n for n in walk(parser.root) if n.tag == "meta" and n.attrs.get("name") == "description"), None)
    if meta:
        brief = clean_text(meta.attrs.get("content", ""))

    containers = [
        n for n in walk(parser.root)
        if n.tag == "div" and classes(n) & {"prop", "func", "types", "vars", "macros", "relnonmem"}
    ]
    for container in containers:
        kind = "property" if "prop" in classes(container) else "member"
        for heading, body_nodes in direct_blocks(container):
            source_lines: list[str] = []
            code = ""
            for node in body_nodes:
                source_lines.extend(node_markdown(node))
                if not code and node.tag == "pre":
                    code = html.unescape(text_of(node, code_ticks=False)).strip("\r\n")
            name = source_member_name(heading)
            aliases: list[str] = []
            for node in walk(heading):
                if node.tag == "span" and "name" in classes(node):
                    alias = clean_text(text_of(node, code_ticks=False))
                    if re.fullmatch(r"[A-Za-z_]\w*", alias):
                        aliases.append(alias)
            if kind == "property":
                for body_node in body_nodes:
                    for node in walk(body_node):
                        if node.tag == "span" and "name" in classes(node):
                            alias = clean_text(text_of(node, code_ticks=False))
                            if re.fullmatch(r"[A-Za-z_]\w*", alias):
                                aliases.append(alias)
            item = {
                "name": name,
                "property_name": name if kind == "property" else None,
                "kind": kind,
                "heading": clean_text(text_of(heading, code_ticks=False)),
                "source": "\n".join(source_lines).strip(),
                "code": code,
                "aliases": aliases,
            }
            by_name.setdefault(name, []).append(item)
            for alias in aliases:
                if alias != name:
                    by_name.setdefault(alias, []).append(item)
    return by_name, brief


def extract_context(path: Path) -> tuple[str, str]:
    parser = TreeParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    meta = next((n for n in walk(parser.root) if n.tag == "meta" and n.attrs.get("name") == "description"), None)
    brief = clean_text(meta.attrs.get("content", "")) if meta else ""
    description = next((n for n in walk(parser.root) if n.tag == "div" and "descr" in classes(n)), None)
    lines = [brief] if brief else []
    code = ""
    if description:
        for node in description.children:
            if not isinstance(node, Node) or node.tag == "h2":
                continue
            blocks = node_markdown(node)
            for block in blocks:
                if block not in lines:
                    lines.append(block)
            if not code:
                pre = node if node.tag == "pre" else next((item for item in walk(node) if item.tag == "pre"), None)
                if pre:
                    code = html.unescape(text_of(pre, code_ticks=False)).strip("\r\n")
            if sum(map(len, lines)) >= 5000:
                break
    return "\n".join(lines).strip(), code


def normalize_class_name(value: str) -> str:
    value = value.replace("::", "_")
    return re.sub(r"[^A-Za-z0-9_]", "", value).lower()


def build_html_index(source_root: Path, module: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in (source_root / module).glob("*.html"):
        if path.name.endswith(("-members.html", "-obsolete.html")):
            continue
        head = path.read_text(encoding="utf-8", errors="replace")[:12000]
        match = re.search(r"<title>(.+?) (?:Class|Struct|Namespace) \|", head, re.I)
        if not match:
            continue
        title = clean_text(re.sub(r"<[^>]+>", "", match.group(1))).replace("::", "_")
        result.setdefault(normalize_class_name(title), path)
    return result


def accessor_property(name: str, properties: dict[str, dict]) -> tuple[dict | None, str | None]:
    if name in properties:
        return properties[name], "get"
    if name.startswith("set") and len(name) > 3:
        prop = name[3].lower() + name[4:]
        if prop in properties:
            return properties[prop], "set"
    if name.endswith("Changed"):
        prop = name[:-7]
        if prop in properties:
            return properties[prop], "signal"
    if name.startswith("is") and len(name) > 2:
        prop = name[2].lower() + name[3:]
        if prop in properties:
            return properties[prop], "get"
    if name.startswith("bindable") and len(name) > 8:
        prop = name[8].lower() + name[9:]
        if prop in properties:
            return properties[prop], "bindable"
    if name.startswith("reset") and len(name) > 5:
        prop = name[5].lower() + name[6:]
        if prop in properties:
            return properties[prop], "reset"
    return None, None


def select_source_items(headings: list[str], by_name: dict[str, list[dict]]) -> list[dict]:
    properties = {
        item["property_name"]: item
        for items in by_name.values()
        for item in items
        if item["kind"] == "property"
    }
    counters: dict[str, int] = {}
    selected = []
    for signature in headings:
        name = member_name(signature)
        items = by_name.get(name, [])
        index = counters.get(name, 0)
        item = items[min(index, len(items) - 1)] if items else None
        if items:
            counters[name] = index + 1
            if item is not None and not item.get("source"):
                donor = next((candidate for candidate in items if candidate.get("source")), None)
                if donor:
                    item = dict(item)
                    item["source"] = donor["source"]
                    item["code"] = donor.get("code", "")
        prop, role = accessor_property(name, properties)
        if item and item["kind"] == "property":
            prop = item
            property_name = item["property_name"]
            if name == property_name or name.startswith("is"):
                role = "get"
            elif name.startswith("set"):
                role = "set"
            elif name.startswith("bindable"):
                role = "bindable"
            elif name.startswith("reset"):
                role = "reset"
            elif name.endswith("Changed"):
                role = "signal"
            else:
                role = "get"
        if prop and (item is None or item["kind"] == "property"):
            item = dict(prop)
            item["role"] = role
            item["property_name"] = prop["name"]
        elif item is None:
            singulars = []
            if name.endswith("Flags"):
                singulars.append(name[:-1])
                singulars.append(name[:-5] + "Flag")
            if name.endswith("ies"):
                singulars.append(name[:-3] + "y")
            if name.endswith("s"):
                singulars.append(name[:-1])
            alias_item = next((by_name[candidate][0] for candidate in singulars if candidate in by_name), None)
            if alias_item:
                item = dict(alias_item)
                item["role"] = "flags"
                item["property_name"] = alias_item["name"]
        elif item:
            item = dict(item)
            item["role"] = None
        if item is None:
            item = {"name": name, "kind": "missing", "source": "", "code": "", "role": None}
        item["api_name"] = name
        selected.append(item)
    return selected


class BingTranslator:
    """Small client for Bing Translator's public web UI endpoint."""

    def __init__(self):
        jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Microsoft Windows 10.0.26200; zh-CN) PowerShell/7.6.5",
        }
        self.key = ""
        self.token = ""
        self.ig = ""
        self.counter = 0
        self.refresh()

    def refresh(self):
        request = urllib.request.Request("https://cn.bing.com/translator", headers=self.headers)
        page = self.opener.open(request, timeout=30).read().decode("utf-8", "replace")
        auth = re.search(r'params_AbusePreventionHelper\s*=\s*\[(\d+),"([^"]+)",', page)
        ig = re.search(r'IG:"([^"]+)"', page)
        if not auth or not ig:
            raise RuntimeError("Bing Translator authentication data was not found")
        self.key, self.token, self.ig = auth.group(1), auth.group(2), ig.group(1)
        self.counter = 0

    def translate(self, value: str) -> str:
        last_error = None
        for attempt in range(4):
            try:
                if self.counter >= 40:
                    self.refresh()
                self.counter += 1
                query = urllib.parse.urlencode({
                    "isVertical": "1",
                    "IG": self.ig,
                    "IID": f"translator.5028.{self.counter}",
                })
                body = urllib.parse.urlencode({
                    "fromLang": "en",
                    "text": value,
                    "to": "zh-Hans",
                    "token": self.token,
                    "key": self.key,
                }).encode()
                request = urllib.request.Request(
                    f"https://cn.bing.com/ttranslatev3?{query}",
                    data=body,
                    headers={**self.headers, "Content-Type": "application/x-www-form-urlencoded"},
                )
                payload = json.loads(self.opener.open(request, timeout=25).read())
                if not isinstance(payload, list) or not payload:
                    detail = payload.get("errorMessage", payload) if isinstance(payload, dict) else payload
                    raise RuntimeError(f"unexpected Bing response: {detail}")
                translated = payload[0]["translations"][0]["text"]
                if translated:
                    return translated
            except Exception as exc:  # network retries are intentionally broad
                last_error = exc
                if attempt == 1:
                    self.refresh()
                time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"translation failed: {last_error}")


_translator_local = threading.local()


def translate_preserving_code(client: BingTranslator, value: str) -> str:
    """Translate prose fragments separately so code spans cannot be changed."""
    pieces = re.split(r"(`[^`\n]+`)", value)
    translated = []
    for piece in pieces:
        if not piece:
            continue
        if piece.startswith("`") and piece.endswith("`"):
            translated.append(piece)
        elif piece.strip():
            translated.append(client.translate(piece))
        else:
            translated.append(piece)
    return "".join(translated).strip()


def translate_batch(batch: list[tuple[str, str]]) -> dict[str, str]:
    if not hasattr(_translator_local, "client"):
        _translator_local.client = BingTranslator()
    client: BingTranslator = _translator_local.client
    markers = [f"ZXQSEP{i:04d}ZXQ" for i in range(len(batch) - 1)]
    chunks = []
    protected_values: list[dict[str, str]] = []
    for index, (_, value) in enumerate(batch):
        protected: dict[str, str] = {}

        def protect(match: re.Match) -> str:
            marker = f"ZXQCODE{index:04d}X{len(protected):04d}ZXQ"
            protected[marker] = match.group(0)
            return marker

        chunks.append(re.sub(r"`[^`\n]+`", protect, value))
        protected_values.append(protected)
        if index < len(markers):
            chunks.append(markers[index])
    try:
        translated = client.translate("\n".join(chunks))
        pattern = "|".join(re.escape(marker) for marker in markers)
        parts = re.split(pattern, translated) if pattern else [translated]
    except Exception:
        parts = []
    if len(parts) != len(batch):
        result = {}
        for key, value in batch:
            result[key] = translate_preserving_code(client, value)
        return result
    result = {}
    for (key, _), part, protected in zip(batch, parts, protected_values):
        part = part.strip()
        for marker, original in protected.items():
            part = part.replace(marker, original)
        result[key] = part
    for key, value in batch:
        if re.search(r"ZXQ(?:CODE|SEP)|ZQQ", result[key], re.IGNORECASE):
            result[key] = translate_preserving_code(client, value)
    return result


def make_batches(items: list[tuple[str, str]], max_chars: int = 4200) -> list[list[tuple[str, str]]]:
    batches = []
    current = []
    size = 0
    for item in items:
        item_size = len(item[1]) + 20
        if current and size + item_size > max_chars:
            batches.append(current)
            current, size = [], 0
        current.append(item)
        size += item_size
    if current:
        batches.append(current)
    return batches


def split_source(value: str, max_chars: int = 3500) -> list[str]:
    if len(value) <= max_chars:
        return [value]
    lines = value.splitlines()
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for line in lines:
        pieces = [line]
        if len(line) > max_chars:
            pieces = re.split(r"(?<=[.!?])\s+", line)
        for piece in pieces:
            if current and size + len(piece) + 1 > max_chars:
                chunks.append("\n".join(current))
                current, size = [], 0
            if len(piece) > max_chars:
                for offset in range(0, len(piece), max_chars):
                    chunks.append(piece[offset:offset + max_chars])
                continue
            current.append(piece)
            size += len(piece) + 1
    if current:
        chunks.append("\n".join(current))
    return chunks


def load_cache(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_cache(path: Path, cache: dict[str, str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(cache, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def cache_key(source: str) -> str:
    return hashlib.sha256(source.encode()).hexdigest()


def translate_sources(sources: set[str], cache_path: Path, workers: int) -> dict[str, str]:
    cache = load_cache(cache_path)
    bad_keys = [
        key for key, value in cache.items()
        if re.search(r"ZXQ(?:CODE|SEP)|ZQQ", value, re.IGNORECASE)
    ]
    for key in bad_keys:
        del cache[key]
    if bad_keys:
        print(f"Discarded {len(bad_keys)} cached translations with damaged code markers.")
    source_chunks = {source: split_source(source) for source in sources}
    unique_chunks = {chunk for chunks in source_chunks.values() for chunk in chunks}
    pending = [(cache_key(value), value) for value in sorted(unique_chunks) if cache_key(value) not in cache]
    batches = make_batches(pending)
    if not batches:
        return {source: "\n".join(cache[cache_key(chunk)] for chunk in chunks) for source, chunks in source_chunks.items()}
    print(f"Translating {len(pending)} unique descriptions in {len(batches)} batches...")
    completed = 0
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
    futures = [executor.submit(translate_batch, batch) for batch in batches]
    try:
        for future in concurrent.futures.as_completed(futures):
            try:
                cache.update(future.result())
            except Exception:
                save_cache(cache_path, cache)
                raise
            completed += 1
            save_cache(cache_path, cache)
            if completed % 10 == 0 or completed == len(batches):
                print(f"  {completed}/{len(batches)} batches")
    except Exception:
        for future in futures:
            future.cancel()
        executor.shutdown(wait=False, cancel_futures=True)
        raise
    else:
        executor.shutdown()
    save_cache(cache_path, cache)
    return {source: "\n".join(cache[cache_key(chunk)] for chunk in chunks) for source, chunks in source_chunks.items()}


def format_translation(value: str) -> str:
    value = value.replace("WARNING:", "注意：").replace("NOTE:", "补充：")
    value = re.sub(r"(?m)^- ", "- ", value)
    value = value.replace("（）", "()")
    lines = []
    for line in value.strip().splitlines():
        line = line.strip()
        if line and not line.startswith("- ") and not re.search(r"[。！？；：.!?;:]$", line):
            line += "。"
        lines.append(line)
    value = "\n".join(lines)
    value = value.replace("该性质是否适用于", "该属性决定")
    value = value.replace("主界面（或默认界面）", "主屏幕（或默认屏幕）")
    value = value.replace("重制：", "重实现自：").replace("重实现：", "重实现自：")
    value = value.replace("关键事件", "按键事件")
    value = value.replace("所有未打开的文件", "所有已打开的文件")
    value = value.replace("旗帜", "标志")
    value = value.replace("方案 URI", "协议 URI")
    replacements = {
        "槽口功能": "槽函数",
        "插槽": "槽函数",
        "槽口": "槽函数",
        "时隙": "槽函数",
        "呼叫者": "调用者",
        "呼叫": "调用",
        "拨打": "调用",
        "过载": "重载",
        "重载解析": "重载决议",
        "财产": "属性",
        "性质": "属性",
        "插座": "套接字",
        "构造子": "构造函数",
        "级数": "系列",
        "刷子": "画刷",
        "记录仪": "录制器",
        "可寻性地位": "是否可跳转的状态",
        "丢弃尸体": "丢弃正文数据",
        "第 Qt 7": "Qt 7",
    }
    for source, replacement in replacements.items():
        value = value.replace(source, replacement)
    value = value.replace("该属性保持", "该属性表示")
    value = value.replace("该属性满足", "该属性表示")
    value = re.sub(r"`([A-Za-z_][\w:]*)`\(\)", r"`\1()`", value)
    return value.strip()


QGUIAPPLICATION_OVERRIDES = {
    "applicationDisplayName": (
        "该属性表示应用程序显示给用户看的名称，例如窗口标题、任务切换界面或桌面环境中的应用名称。"
        "它可以使用翻译后的文本；如果没有显式设置，Qt 会回退到 `QCoreApplication::applicationName()`。"
    ),
    "desktopFileName": (
        "该属性指定 Linux/freedesktop 桌面环境中代表本应用的 `.desktop` 文件基本名。"
        "只填写文件名，不含目录和 `.desktop` 后缀；例如桌面项为 "
        "`/usr/share/applications/org.example.Reader.desktop` 时应设置为 `org.example.Reader`。"
        "窗口系统用它把应用窗口与启动器、图标和桌面元数据准确关联，避免靠窗口标题猜测。"
    ),
    "layoutDirection": (
        "该属性控制应用的默认界面排列方向。`Qt::LeftToRight` 适用于中文、英文等语言，"
        "`Qt::RightToLeft` 适用于阿拉伯语、希伯来语等语言；设为 `Qt::LayoutDirectionAuto` 时，"
        "Qt 根据当前应用语言选择方向。改变它会影响随后采用应用默认方向的窗口和布局。"
    ),
    "platformName": (
        "该只读属性返回当前实际加载的 QPA 平台插件名称，例如 Windows 上通常是 `windows`，"
        "X11 环境是 `xcb`，Wayland 环境是 `wayland`，无界面测试可能是 `offscreen`。"
        "它适合用于诊断或只在特定后端可用的兼容处理，不应把某个平台名称当成应用正常运行的必要条件。"
    ),
    "primaryScreen": (
        "该只读属性返回应用当前的主屏幕。未明确指定屏幕的新 `QWindow` 通常先显示在这里。"
        "多显示器配置会在运行中变化，应监听 `primaryScreenChanged(QScreen *)`，不要长期缓存返回指针而不处理屏幕移除。"
    ),
    "quitOnLastWindowClosed": (
        "该属性决定最后一个可见主窗口关闭后，Qt 是否自动尝试退出应用；默认值为 `true`。"
        "托盘程序或没有常驻窗口的后台 GUI 应用通常把它设为 `false`。即使为 `true`，"
        "活动的 `QEventLoopLocker` 或被忽略的 `QEvent::Quit` 仍可能阻止进程真正退出。"
    ),
    "windowIcon": (
        "该属性设置应用窗口的默认图标。没有通过 `QWindow::setIcon()` 单独指定图标的窗口会采用它；"
        "任务栏、窗口标题栏等位置是否显示以及采用哪个尺寸由平台决定。"
    ),
    "~QGuiApplication": "销毁应用程序对象并结束由它管理的 GUI 平台资源。通常在 `main()` 返回时自动发生；应用中只能存在一个应用程序对象。",
    "event": "重实现 `QCoreApplication::event()`，处理发送给应用程序对象自身的事件。只有在子类需要截获应用级事件时才重写；未处理的事件必须交给基类。",
    "notify": "重实现 `QCoreApplication::notify()`，把一个事件分派给目标 `object`。返回值表示事件是否被处理。它是全局事件分派入口，重写时必须谨慎，并通常调用基类实现以维持 Qt 的正常事件传递。",
    "screenAt": (
        "返回包含全局坐标 `point` 的屏幕；点不在任何屏幕上时返回 `nullptr`。"
        "在存在多个彼此独立的虚拟桌面组时，若坐标同时匹配多个组，只返回第一个匹配项。"
    ),
    "sync": (
        "先处理 Qt 中待分派的事件，再让平台插件与底层窗口系统同步，最后再次处理同步过程中产生的事件。"
        "这个操作开销较大且官方不建议在常规业务代码中使用；不要把它当作强制重绘或刷新界面的通用办法。"
    ),
}


def member_translation_override(source_path: Path, signature: str, item: dict) -> str | None:
    """Chinese explanations for terse Qt entries that translation leaves as declarations."""
    page = source_path.name.lower()
    name = item["name"]

    enum_overrides = {
        ("qshaderdescription.html", "TessellationMode"): (
            "指定细分着色器生成图元的形状：`UnknownTessellationMode` 表示未知，`TrianglesTessellationMode` 生成三角形，"
            "`QuadTessellationMode` 生成四边形，`IsolineTessellationMode` 生成等值线。读取反射信息后应先排除未知值。"
        ),
        ("qshaderdescription.html", "TessellationPartitioning"): (
            "指定细分级别如何取整和分割：`EqualTessellationPartitioning` 使用等距整数分割，"
            "`FractionalEvenTessellationPartitioning` 和 `FractionalOddTessellationPartitioning` 分别使用偶数、奇数分数分割；"
            "`UnknownTessellationPartitioning` 表示着色器未提供可识别模式。"
        ),
        ("qshaderdescription.html", "TessellationWindingOrder"): (
            "指定细分后图元的顶点绕序。`CwTessellationWindingOrder` 为顺时针，`CcwTessellationWindingOrder` 为逆时针，"
            "`UnknownTessellationWindingOrder` 表示未知；绕序会影响正反面判断和背面剔除。"
        ),
        ("qtextlayout.html", "CursorMode"): (
            "控制光标移动的粒度：`SkipCharacters` 按字符位置移动，`SkipWords` 按单词边界移动。"
            "把它传给 `nextCursorPosition()` 或 `previousCursorPosition()`，Qt 会同时遵守双向文本和合法字形边界。"
        ),
        ("qtextline.html", "CursorPosition"): (
            "控制 `cursorToX()` 如何解释光标位置：`CursorBetweenCharacters` 把位置视为字符间隙，"
            "`CursorOnCharacter` 把位置视为字符本身。处理文本插入光标通常使用前者。"
        ),
        ("qtextline.html", "Edge"): (
            "指定文本行的逻辑边缘：`Leading` 是按文字方向开始的一侧，`Trailing` 是结束的一侧。"
            "它不是固定的左/右；在从右到左文本中两者方向会相反。"
        ),
        ("qtransform.html", "TransformationType"): (
            "描述矩阵中最复杂的变换成分，从 `TxNone`、平移、缩放、旋转、错切到 `TxProject` 投影逐级增加。"
            "`type()` 返回该分类，绘制和映射代码可据此选择更快路径；它不是让调用者手工设置的状态。"
        ),
        ("qprinter.html", "PrinterState"): (
            "表示打印机当前状态：`Idle` 空闲、`Active` 正在打印、`Aborted` 已中止、`Error` 出错。"
            "用 `printerState()` 查询；这是状态快照，打印失败时还应结合返回值和系统打印服务诊断。"
        ),
        ("qabstractslider.html", "SliderAction"): (
            "表示要对滑块执行的逻辑动作，包括不操作、单步加减、整页加减、跳到最小/最大值以及移动到指定位置。"
            "把它传给 `triggerAction()` 会按范围、步长和反向设置更新值，并触发相应信号。"
        ),
        ("qabstractspinbox.html", "StepType"): (
            "指定步进算法。`DefaultStepType` 始终使用 `singleStep`；`AdaptiveDecimalStepType` 根据当前数值的数量级自动调整步长，"
            "例如较大数值每次改变得更多。自适应模式下 `singleStep` 不参与实际步长计算。"
        ),
        ("qfiledialog.html", "AcceptMode"): (
            "决定文件对话框是在选择要打开的内容还是选择保存目标。`AcceptOpen` 使用打开语义，`AcceptSave` 使用保存语义，"
            "后者会影响确认按钮文字、文件存在检查和覆盖确认。"
        ),
        ("qfiledialog.html", "DialogLabel"): (
            "标识文件对话框中可改写的文字位置：查找目录、文件名、文件类型、接受按钮和拒绝按钮。"
            "把枚举值传给 `setLabelText()` 自定义对应标签；未设置的位置继续使用平台翻译。"
        ),
        ("qplaintextedit.html", "LineWrapMode"): (
            "控制纯文本编辑器的换行：`NoWrap` 保持逻辑行并允许水平滚动，`WidgetWidth` 按视口宽度折行。"
            "折行只改变显示，不会向文档插入换行符。"
        ),
        ("qstylehintreturn.html", "HintReturnType"): (
            "标识 `QStyleHintReturn` 实际承载的数据结构：`SH_Default` 为基础返回对象，`SH_Mask` 携带区域遮罩，"
            "`SH_Variant` 携带 `QVariant`。自定义样式写入前应核对调用者提供的 `type` 和 `version`。"
        ),
        ("qtextedit.html", "LineWrapMode"): (
            "控制富文本编辑器的视觉换行：不换行、按控件宽度、固定像素宽度或固定列数换行。"
            "固定模式还需用 `setLineWrapColumnOrWidth()` 给出宽度；换行只影响布局，不会改写文档内容。"
        ),
    }
    if (page, name) in enum_overrides:
        return enum_overrides[(page, name)]

    if page == "qgradient.html" and name == "QGradientStops":
        return (
            "渐变停止点列表类型，等价于 `QList<QGradientStop>`；每项由 0 到 1 的位置和该位置的颜色组成。"
            "用 `setStops()` 一次设置多个色标时通常按位置升序排列，超出有效范围的位置不应使用。"
        )
    if page == "qenablesharedfromthis.html" and name == "sharedFromThis" and "const T" in signature:
        return (
            "返回指向当前对象的 `QSharedPointer<const T>`，并与最初管理该对象的 `QSharedPointer` 共享引用计数。"
            "只有对象已经由 `QSharedPointer` 接管时结果才有效；不要对栈对象或仅由裸指针管理的对象依赖此接口。"
        )

    method_overrides = {
        ("qsavefile.html", "writeData"): (
            "把 `data` 中最多 `len` 字节写入 `QSaveFile` 的临时文件，返回实际接收的字节数，失败返回 -1。"
            "它由 `QIODevice::write()` 间接调用，不应直接调用；只有最后 `commit()` 成功后，目标文件才会被原子替换。"
        ),
        ("qstandarditemmodel.html", "dropMimeData"): (
            "把拖放数据 `data` 按 `action` 插入 `parent` 下的 `row`、`column` 位置，成功返回 `true`。"
            "`row` 或 `column` 为 -1 表示由模型选择合适位置；自定义 MIME 格式时应与 `mimeTypes()` 和 `mimeData()` 配套重实现。"
        ),
        ("qstandarditemmodel.html", "multiData"): (
            "一次读取 `index` 的多个角色并填入 `roleDataSpan`，避免逐个调用 `data()` 的开销。"
            "每个请求角色都应写回对应值；派生模型未处理的角色应交给基类实现。"
        ),
        ("qgraphicsvideoitem.html", "paint"): (
            "由图形视图框架调用，把当前视频帧绘制到该图元；`option` 提供绘制状态，`widget` 可能为 `nullptr`。"
            "通常不直接调用；子类扩展绘制时应保留视频内容的宽高比和 `boundingRect()` 约束。"
        ),
        ("qgraphicssvgitem.html", "paint"): (
            "由图形视图框架调用，使用关联的 `QSvgRenderer` 把 SVG 内容绘制到图元边界内。"
            "`option` 描述当前绘制状态，`widget` 可能为 `nullptr`；应用通常通过设置共享渲染器和元素 ID 控制内容。"
        ),
        ("qgraphicsproxywidget.html", "paint"): (
            "由场景调用，把代理所嵌入的 `QWidget` 及其当前样式绘制到图形视图。"
            "`option` 提供选择、变换等状态；通常不直接调用，派生类额外绘制后应保持代理控件的几何和缓存一致。"
        ),
        ("qabstractsocket.html", "readData"): (
            "从套接字接收缓冲区复制最多 `maxSize` 字节到 `data`，返回读取字节数，失败返回 -1。"
            "这是供 `QIODevice::read()` 调用的受保护实现；异步代码应先响应 `readyRead()`，不要直接调用它或阻塞轮询。"
        ),
        ("qabstractsocket.html", "writeData"): (
            "把最多 `size` 字节加入套接字发送缓冲区，返回已接受字节数，失败返回 -1。"
            "返回成功不表示数据已经到达对端；实际写出进度由 `bytesWritten()` 通知，错误用 `error()` 和 `errorString()` 检查。"
        ),
        ("qlocalsocket.html", "readData"): (
            "从本地套接字接收缓冲区复制最多 `c` 字节到 `data`，返回读取字节数，失败返回 -1。"
            "它由 `QIODevice::read()` 间接调用；应在 `readyRead()` 后读取，并处理断开和 `errorOccurred()`。"
        ),
        ("qlocalsocket.html", "writeData"): (
            "把最多 `c` 字节加入本地套接字发送缓冲区，返回已接受字节数，失败返回 -1。"
            "数据可能稍后才写入系统；用 `bytesWritten()` 或在确有阻塞需要时用 `waitForBytesWritten()` 判断进度。"
        ),
        ("qnetworkreply.html", "writeData"): (
            "实现 `QIODevice` 的写入入口，但普通 `QNetworkReply` 是由网络后端提供数据的只读顺序设备，应用不应向回复对象写数据。"
            "要发送请求正文，应把数据传给 `QNetworkAccessManager` 的 `post()`、`put()` 或 `sendCustomRequest()`。"
        ),
        ("qsctpsocket.html", "readData"): (
            "从 SCTP 接收缓冲区读取最多 `maxSize` 字节到 `data`，返回读取字节数，失败返回 -1。"
            "连续字节读取可能丢失数据报边界；需要保留 SCTP 消息信息时使用 `readDatagram()`。"
        ),
        ("qsctpsocket.html", "readLineData"): (
            "从 SCTP 接收数据中读取一行，最多写入 `maxlen` 字节并返回实际长度，失败返回 -1。"
            "它服务于 `QIODevice::readLine()`；二进制 SCTP 消息通常应使用数据报接口而不是按行读取。"
        ),
        ("qsslsocket.html", "readData"): (
            "从已经解密的 SSL 接收缓冲区复制最多 `maxlen` 字节到 `data`，返回读取字节数，失败返回 -1。"
            "它由 `QIODevice::read()` 间接调用；客户端通常应等到 `encrypted()` 且收到 `readyRead()` 后再读取。"
        ),
        ("qsslsocket.html", "writeData"): (
            "把最多 `len` 字节交给 SSL 层加密并排入发送缓冲区，返回已接受字节数，失败返回 -1。"
            "握手完成前写入的数据会排队；`bytesWritten()` 表示写出进度，不能据此假定对端已经处理。"
        ),
        ("qsqltablemodel.html", "data"): (
            "返回 `index` 在指定 `role` 下的数据。显示和编辑角色来自当前记录，其他角色按 `QSqlQueryModel`/`QAbstractItemModel` 规则处理；"
            "索引无效或角色不受支持时返回无效 `QVariant`。未提交的编辑会优先反映在返回值中。"
        ),
        ("qaccessiblewidget.html", "indexOfChild"): (
            "返回 `child` 在当前控件可访问子对象列表中的从 0 开始索引；不是直接子对象时返回 -1。"
            "传入接口必须仍然有效，结果应与 `childCount()` 和 `child(index)` 使用同一顺序。"
        ),
        ("qtreewidget.html", "setSelectionModel"): (
            "为树控件安装 `selectionModel`，使选择状态由该对象管理。它必须关联当前 `QTreeWidget` 使用的模型；"
            "替换后旧选择模型不会因这次调用自动删除，共享选择模型时也要自行保证生命周期。"
        ),
        ("qdomdocumenttype.html", "nodeType"): "始终返回 `QDomNode::DocumentTypeNode`，用于在通用 `QDomNode` 遍历中识别文档类型声明节点。",
    }
    if (page, name) in method_overrides:
        return method_overrides[(page, name)]

    if page in {"qquickview.html", "qquickwindow.html"} and name in {"keyPressEvent", "keyReleaseEvent"}:
        action = "按下" if name == "keyPressEvent" else "释放"
        return (
            f"窗口取得键盘焦点时，Qt 用该处理器把按键{action}事件 `e` 送入 Qt Quick 焦点项和输入系统。"
            "子类只应拦截确实处理的按键并接受事件；未处理的情况要调用基类实现，否则 QML 项可能收不到键盘事件。"
        )
    if page == "qquickwindow.html" and name == "resizeEvent":
        return (
            "窗口尺寸改变时接收 `ev`，并让 Qt Quick 场景和内容项按新尺寸更新。"
            "子类可在这里同步自定义资源，但应调用基类实现，且不要在事件处理中执行耗时布局或渲染。"
        )
    if page == "qquickwindow.html" and name == "wheelEvent":
        return (
            "接收窗口上的滚轮事件，并按指针位置把它分派给 Qt Quick 项和输入处理器。"
            "子类处理后应接受事件；未处理时调用基类，使 Flickable、WheelHandler 等 QML 组件仍能响应。"
        )
    if page in {"qgraphicsview.html", "qplaintextedit.html", "qtextedit.html"} and name == "keyPressEvent":
        roles = {
            "qgraphicsview.html": "场景、焦点图元以及视图自身的导航行为",
            "qplaintextedit.html": "纯文本输入、选择、删除和快捷键",
            "qtextedit.html": "富文本输入、选择、删除和快捷键",
        }
        return (
            f"处理按键事件 `event`，默认实现负责{roles[page]}。"
            "子类可拦截自定义按键；不处理时必须调用基类实现，否则标准编辑或场景键盘操作会失效。"
        )
    if page == "qscrollbar.html" and name == "wheelEvent":
        return (
            "把滚轮的像素或角度增量换算为滚动条值变化，并遵守方向、页面步长和反向控件设置。"
            "子类只在需要自定义滚动策略时重写；未处理的事件应交给基类。"
        )
    if page == "qproxystyle.html":
        proxy = {
            "drawComplexControl": "绘制由多个子控件组成的复杂控件；默认把 `control`、`option`、`painter` 和 `widget` 原样转交给基础样式。",
            "drawControl": "绘制按钮、标签等控件元素；默认委托基础样式，派生代理可在调用前后调整选项或追加绘制。",
            "drawPrimitive": "绘制框线、箭头等基础图元；默认委托基础样式，`option` 和 `widget` 可用于取得状态与调色板。",
            "hitTestComplexControl": "判断位置 `pos` 落在复杂控件的哪个子控件上；默认询问基础样式，未命中时返回 `SC_None`。",
            "pixelMetric": "查询 `metric` 对应的像素尺寸，例如边框宽度或图标大小；默认返回基础样式结果，`option`、`widget` 可为空。",
            "standardPixmap": "取得 `standardPixmap` 对应的平台风格位图；默认由基础样式生成，调用者按值接收结果，不管理样式内部资源。",
            "styleHint": "查询影响控件行为的样式提示并返回整数结果；某些提示会通过可选的 `returnData` 返回额外结构化数据。",
            "subElementRect": "计算 `element` 在控件选项中的矩形区域；默认委托基础样式，返回坐标相对于 `option` 描述的控件。",
        }
        if name in proxy:
            return proxy[name]
    return None


def manual_translation(source_path: Path, item: dict, signature: str = "") -> str | None:
    if item.get("manual_translation"):
        return item["manual_translation"]
    override = member_translation_override(source_path, signature, item)
    if override:
        return override
    if source_path.name.lower() != "qguiapplication.html":
        return None
    return QGUIAPPLICATION_OVERRIDES.get(item["name"])


def usage_override(source_path: Path, signature: str, item: dict) -> str | None:
    if source_path.name.lower() != "qguiapplication.html":
        return None
    name = item["api_name"]
    if name == "applicationDisplayName" and "(" not in signature:
        return (
            "在创建应用对象后、显示窗口前设置即可：\n\n"
            "```cpp\n"
            "QGuiApplication app(argc, argv);\n"
            "QGuiApplication::setApplicationDisplayName(QObject::tr(\"图片管理器\"));\n"
            "qInfo() << QGuiApplication::applicationDisplayName();\n"
            "```\n\n"
            "名称需要随语言切换时重新设置；依赖这个名称的界面可监听 `applicationDisplayNameChanged()`。"
        )
    overrides = {
        "setApplicationDisplayName": "传入希望用户看到的名称，通常在显示第一个窗口前调用；设置后会发出 `applicationDisplayNameChanged()`。",
        "setDesktopFileName": "传入 `.desktop` 文件的基本名，不要包含路径或 `.desktop` 后缀；应在创建窗口前设置。",
        "setQuitOnLastWindowClosed": "托盘程序调用 `setQuitOnLastWindowClosed(false)` 后，最后一个窗口关闭时事件循环仍会继续，退出动作要由菜单或业务逻辑显式触发。",
        "setWindowIcon": "传入包含合适尺寸资源的 `QIcon`，并在创建窗口前调用；需要例外图标的窗口再使用 `QWindow::setIcon()` 覆盖。",
    }
    return overrides.get(name)


def role_usage(item: dict) -> str:
    role = item.get("role")
    name = item["api_name"]
    prop = item.get("property_name", name)
    if role == "get":
        return f"调用 `{name}()` 读取当前值；它不会修改应用状态。"
    if role == "set":
        return f"调用 `{name}(...)` 修改 `{prop}`；传入的新值会成为后续查询和相关界面行为所使用的值。"
    if role == "signal":
        return f"这是变化通知信号。用 `connect()` 监听 `{prop}` 的变化，不要把它当作普通函数主动调用。"
    if role == "bindable":
        return f"调用 `{name}()` 取得 `{prop}` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。"
    if role == "reset":
        return f"调用 `{name}()` 撤销对 `{prop}` 的显式覆盖，让它重新采用继承值或默认值。"
    if role == "flags":
        return f"`{name}` 是 `{prop}` 枚举的 `QFlags` 组合类型，可用按位或 `|` 同时传入多个选项。"
    return ""


def replace_section(markdown: str, items: list[dict], translations: dict[str, str], source_path: Path) -> str:
    start = markdown.index(SECTION_5)
    prefix = clean_quick_reference(markdown[:start]).rstrip()
    old_section = markdown[start:]
    suffix_match = re.search(r"(?m)^## 6\.", old_section)
    if suffix_match:
        api_section = old_section[:suffix_match.start()]
        suffix = old_section[suffix_match.start():].strip()
    else:
        api_section = old_section
        suffix = ""
    heading_matches = list(re.finditer(r"(?m)^### (`[^\n]+`)\s*$", api_section))
    headings = [
        match.group(1)
        for match in heading_matches
        if looks_like_api_heading(match.group(1))
    ]
    if len(headings) != len(items):
        raise ValueError(
            f"heading/source mismatch in {source_path.name}: {len(headings)} != {len(items)}"
        )

    output = [
        SECTION_5,
        "",
        "本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。",
        "",
    ]
    for signature, item in zip(headings, items):
        source = item.get("source", "").strip()
        output.append(f"### {signature}")
        output.append("")
        if source:
            output.append("**作用与语义：**")
            output.append("")
            output.append(manual_translation(source_path, item, signature) or format_translation(translations[source]))
        else:
            output.append("**作用与语义：** Qt 6.11.1 原始类页没有为这个声明提供独立正文；它是本类公开接口的一部分，具体可用值或行为由同名类型/相关重载定义。")
        usage = usage_override(source_path, signature, item) or role_usage(item)
        if usage:
            output.extend(["", "**如何使用：** " + usage])
        if item.get("code"):
            output.extend(["", "**官方示例：**", "", "```cpp", item["code"], "```"])
        output.append("")
    rendered = prefix + "\n\n" + "\n".join(output).rstrip()
    if suffix:
        rendered += "\n\n" + suffix
    return rendered + "\n"


def clean_quick_reference(prefix: str) -> str:
    marker = "## 4. API 速查"
    if marker not in prefix:
        return prefix
    start = prefix.index(marker)
    before, section = prefix[:start], prefix[start:]
    intro_end = section.find("\n### ")
    if intro_end < 0:
        return prefix
    intro, groups_text = section[:intro_end], section[intro_end + 1:]
    groups = re.split(r"(?m)(?=^### )", groups_text)
    kept_groups = []
    for group in groups:
        lines = []
        for line in group.splitlines():
            match = re.match(r"- `(.+)`\s*$", line)
            if match and not looks_like_api_heading(match.group(1)):
                continue
            lines.append(line)
        if any(line.startswith("- `") for line in lines):
            kept_groups.append("\n".join(lines).rstrip())
    return before + intro.rstrip() + "\n\n" + "\n\n".join(kept_groups) + "\n"


def specific_fallback_translation(source_path: Path, heading: str, item: dict) -> str | None:
    """Explain declarations for which Qt publishes a signature but no member prose."""
    page = source_path.name.lower()
    name = item["name"]
    signature = heading.strip("` ")

    if page == "qdirlisting-sentinel.html":
        return (
            "比较迭代器与结束哨兵。迭代器已经到达目录遍历末尾时返回 `true`；此时不能再解引用该迭代器，"
            "否则行为未定义。它主要供范围 `for` 和标准库范围算法判断遍历是否结束。"
        )
    if page == "qitemselectionmodel.html" and name == "bindableModel":
        return (
            "返回 `model` 属性的 `QBindable<QAbstractItemModel *>` 包装，供 Qt 属性绑定系统跟踪选择模型所关联的数据模型。"
            "只想取得当前模型时调用 `model()`；只有需要建立或检查属性绑定时才使用该接口。"
        )
    if page == "qlatin1string.html":
        return (
            "`QLatin1String` 是 `QLatin1StringView` 的兼容别名，不会复制或拥有字符数据。新代码可以直接写 "
            "`QLatin1StringView`；底层 Latin-1 数据必须在视图使用期间保持有效。"
        )

    alias_pages = {"qlatin1stringview.html", "qlist.html", "qstring.html"}
    alias_descriptions = {
        "const_iterator": "只读的 STL 风格正向迭代器类型，用于从 `begin()`/`cbegin()` 遍历到 `end()`/`cend()`，不能通过它修改元素。",
        "const_reverse_iterator": "只读的 STL 风格反向迭代器类型，用于从 `rbegin()`/`crbegin()` 反向遍历到 `rend()`/`crend()`。",
        "iterator": "可修改元素的 STL 风格正向迭代器类型；容器发生分离或结构性修改后，已有迭代器可能失效。",
        "reverse_iterator": "可修改元素的 STL 风格反向迭代器类型；容器发生分离或结构性修改后，已有迭代器可能失效。",
        "const_reference": "元素只读引用类型，适合在不复制元素且不允许修改时作为返回值或局部别名使用。",
        "reference": "元素可写引用类型；它直接引用字符串或容器内部元素，所属对象修改、分离或销毁后不能继续使用。",
        "difference_type": "表示两个迭代器之间距离的有符号整数类型，主要供标准库迭代器算法和泛型代码使用。",
        "size_type": "表示字符串长度、容量或索引范围的整数类型；写泛型代码时用它与本类的尺寸 API 保持类型一致。",
        "value_type": "表示单个元素的类型；对 `QString` 而言元素是一个 UTF-16 码元 `QChar`，不一定等于完整的 Unicode 字符。",
        "parameter_type": "`QList<T>` 为高效传入单个 `T` 而选择的参数类型：按元素特征可能按值传递，也可能使用 `const T &`。它主要用于泛型实现。",
        "rvalue_ref": "`QList<T>` 接收可移动元素时使用的参数类型，通常对应 `T &&`；传入临时值或 `std::move(value)` 可避免不必要的复制。",
    }
    if page in alias_pages and name in alias_descriptions:
        description = alias_descriptions[name]
        if page == "qlatin1stringview.html":
            description += " `QLatin1StringView` 不拥有字符数据，原始 Latin-1 缓冲区必须在迭代器使用期间保持有效。"
        return description

    if page in {"qlist-const-iterator.html", "qlist-iterator.html"}:
        read_only = page == "qlist-const-iterator.html"
        access = "只读引用" if read_only else "可写引用"
        pointer = "只读指针" if read_only else "可写指针"
        invalidation = "所属 `QList` 发生分离或结构性修改后，已有迭代器可能失效。"
        iterator_ops = {
            "operator*": f"解引用当前迭代器并返回当前元素的{access}。不能解引用 `end()`；{invalidation}",
            "operator->": f"返回指向当前元素的{pointer}，用于 `it->member` 形式访问。不能对 `end()` 使用；{invalidation}",
            "operator++": f"把迭代器前移到下一个元素并返回自身；从最后一个元素前移一次会得到 `end()`。{invalidation}",
            "operator--": f"把迭代器后移到前一个元素并返回自身；可从 `end()` 后移到最后一个元素，但不能越过 `begin()`。{invalidation}",
            "operator+": f"返回前移 `offset` 个元素后的新迭代器，不改变原迭代器。结果必须仍位于同一列表的有效迭代范围内；{invalidation}",
            "operator-": f"返回当前迭代器与 `other` 之间的元素距离；两个迭代器必须来自同一个 `QList`。{invalidation}",
            "operator==": "比较两个迭代器是否指向同一列表中的同一位置；两个 `end()` 迭代器也可相等，但相等不表示可以解引用。",
        }
        if name in iterator_ops:
            return iterator_ops[name]

    if page == "qmessagelogcontext.html":
        if name == "QMessageLogContext":
            if "fileName" in signature:
                return (
                    "用源码文件名、行号、函数名和日志分类构造一条日志上下文。它通常由 Qt 日志宏自动创建；"
                    "四个字符串以指针保存而不复制，因此手工构造时必须保证它们在记录日志期间仍有效。"
                )
            return "构造空日志上下文：行号为 0，文件、函数和分类指针为 `nullptr`，版本字段设为 `CurrentVersion`。"
        message_fields = {
            "CurrentVersion": "当前日志上下文结构版本，Qt 6.11.1 中为 2。自定义消息处理器可用它判断哪些字段可安全读取。",
            "line": "产生日志调用的源码行号；无法取得位置信息时为 0。它与 `file` 和 `function` 一起用于定位日志来源。",
            "file": "产生日志调用的源码文件名指针；构建配置未保留上下文时可能为 `nullptr`，读取前应先判空。",
            "function": "产生日志调用的函数名指针；构建配置未保留上下文时可能为 `nullptr`，读取前应先判空。",
            "category": "该消息所属日志分类的名称指针；没有分类信息时可能为 `nullptr`，读取前应先判空。",
        }
        return message_fields.get(name)

    if page in {"qpropertychangehandler.html", "qpropertynotifier.html"}:
        type_name = "QPropertyChangeHandler" if page == "qpropertychangehandler.html" else "QPropertyNotifier"
        if name == type_name:
            if "const Property &property" in signature:
                return (
                    "保存无参数回调 `handler` 并立即订阅 `property`；属性值变化时调用该回调。"
                    f"必须保存返回的 `{type_name}` 对象，它销毁后订阅会自动解除。"
                )
            if "Functor handler" in signature:
                return (
                    "保存无参数回调 `handler`，但这个重载本身没有指定要观察的属性。"
                    "它主要供稍后关联属性的低层用法；常规代码应优先使用同时传入 `property` 的构造函数或 `addNotifier()`。"
                )
            return "构造一个尚未关联属性、也没有回调的通知器；在设置有效来源和处理函数前，属性变化不会触发任何操作。"

    if page == "qt-totally-ordered-wrapper.html":
        wrapper_ops = {
            "totally_ordered_wrapper": "保存传入的指针式对象 `pointer`，使该值的关系比较使用严格全序规则；这尤其用于避免直接比较无关裸指针时的未定义行为。",
            "get": "返回当前保存的底层指针式对象，不改变包装器；需要传给不接受包装类型的 API 时使用。",
            "reset": "用 `pointer` 替换当前保存的底层对象；它只更新包装值，不负责删除原对象或取得新对象的所有权。",
            "operator->": "返回底层指针以支持 `wrapper->member` 访问；底层值为空时不能解引用。",
            "operator*": "解引用底层指针并返回目标对象的引用；底层值为空或悬空时调用会产生未定义行为。",
            "operatorbool": "检查底层指针式对象是否为真，常用于 `if (wrapper)`；它不会验证指针所指对象的生命周期。",
        }
        return wrapper_ops.get(name)

    if page == "qaccessibleinterface.html" and name.endswith("Interface"):
        labels = {
            "selectionInterface": "选择",
            "actionInterface": "动作",
            "tableCellInterface": "表格单元格",
            "tableInterface": "表格",
            "textInterface": "文本",
            "valueInterface": "数值",
        }
        if name in labels:
            return (
                f"取得当前可访问对象的{labels[name]}专用接口。对象支持这项能力时返回相应接口指针，否则返回 `nullptr`；"
                "调用专用方法前必须判空，返回指针由可访问性对象管理，不要自行删除。"
            )

    fixed = {
        ("qpointerevent.html", "setAccepted"): (
            "设置整个指针事件的接受状态。传入 `true` 表示接收者已经处理该事件，并会隐式接受事件携带的所有触点；"
            "传入 `false` 允许未处理事件继续传播。若只想接受某个触点，应设置对应 `QEventPoint` 的接受状态。"
        ),
        ("qvulkandevicefunctions.html", "vkGetDeviceProcAddr"): (
            "对有效的 `VkDevice` 查询名为 `name` 的设备级 Vulkan 命令地址。命令不存在、扩展未启用或不能用于该设备时返回 `nullptr`；"
            "返回函数指针的签名和使用条件必须以对应 Vulkan 命令规范为准。"
        ),
        ("qvulkanfunctions.html", "vkEnumeratePhysicalDevices"): (
            "枚举 Vulkan 实例可见的物理设备。先把 `devices` 设为 `nullptr` 取得数量，再按 `count` 分配数组并再次调用；"
            "返回值是 `VkResult`，第二次调用仍应处理设备数变化导致的 `VK_INCOMPLETE`。"
        ),
        ("qdtls.html", "GeneratorParameters"): (
            "这是 `QDtlsClientVerifier::GeneratorParameters` 的别名，保存 DTLS Cookie 生成所用的哈希算法和密钥。"
            "它只用于服务器端，并应在握手开始前传给 `setCookieGeneratorParameters()`；密钥应由密码学安全随机源生成并定期轮换。"
        ),
        ("qprintpreviewwidget.html", "setVisible"): (
            "设置打印预览控件是否可见。传入 `true` 显示控件并让预览保持可用，传入 `false` 隐藏；"
            "常规代码通常调用 `show()`、`hide()` 或布局管理器间接触发它，不应绕过控件生命周期直接调用基类实现。"
        ),
        ("qsvggenerator.html", "initPainter"): (
            "当 `QPainter` 开始在此 SVG 生成器上绘制时，由 Qt 调用这个受保护钩子来初始化画笔状态。"
            "它是 Qt 6.11 起对 `QPaintDevice` 的内部重实现，应用代码不应直接调用；正常用法是 `QPainter painter(&generator)`。"
        ),
        ("qdateedit.html", "userDateChanged"): (
            "用户在日期编辑器中实际修改日期时发出，参数 `date` 是修改后的有效日期。"
            "只关心用户操作而不想响应程序调用 `setDate()` 时连接此信号；要监听所有变化则使用 `dateChanged()`。"
        ),
        ("qtimeedit.html", "userTimeChanged"): (
            "用户在时间编辑器中实际修改时间时发出，参数 `time` 是修改后的有效时间。"
            "只关心用户操作而不想响应程序调用 `setTime()` 时连接此信号；要监听所有变化则使用 `timeChanged()`。"
        ),
        ("qwidget.html", "style"): (
            "返回当前实际用于绘制该控件的 `QStyle`。控件未通过 `setStyle()` 单独指定时，结果来自父控件或应用样式；"
            "可用它查询像素指标、标准图标或绘制控件，但返回对象由 Qt 管理，不要删除或长期缓存。"
        ),
    }
    if (page, name) in fixed:
        return fixed[(page, name)]

    if page == "qttasktree-qdefaulttaskadapter.html":
        task_adapter = {
            "operator": (
                "把 `task` 接入任务树：连接它的 `done(DoneResult)` 或 `done(bool)` 完成信号，使结果转交给 `interface`，然后调用 `task->start()`。"
                "仅当 `Task` 继承 `QObject` 并满足这两个接口约定时才能使用默认适配器。"
            ),
            "start": "这是默认适配器要求 `Task` 提供的启动入口。调用后应开始任务且尽快返回，不能用长时间阻塞代替异步执行。",
            "done": (
                "这是默认适配器要求 `Task` 在结束时发出的信号；`result` 表示成功、失败或取消等完成结果。"
                "每次启动应只发出一次，适配器会把它转交给 `QTaskInterface::reportDone()`。"
            ),
        }
        return task_adapter.get(name)
    return None


def collect_documents(
    repo: Path,
    source_root: Path,
    selected_modules: set[str] | None,
    selected_classes: set[str] | None = None,
):
    documents = []
    indexes: dict[str, dict[str, Path]] = {}
    source_cache: dict[Path, tuple[dict[str, list[dict]], str]] = {}
    context_cache: dict[Path, tuple[str, str]] = {}

    def source_for(path: Path):
        if path not in source_cache:
            source_cache[path] = extract_source(path)
        return source_cache[path]

    def context_for(path: Path):
        if path not in context_cache:
            context_cache[path] = extract_context(path)
        return context_cache[path]

    for repo_module, source_module in MODULES.items():
        if selected_modules and repo_module not in selected_modules:
            continue
        indexes[repo_module] = build_html_index(source_root, source_module)
        for markdown_path in sorted((repo / repo_module).glob("*.md")):
            if markdown_path.name == "index.md":
                continue
            markdown = markdown_path.read_text(encoding="utf-8")
            class_match = re.match(r"#\s+(.+)", markdown)
            if not class_match or SECTION_5 not in markdown:
                continue
            class_name = class_match.group(1).strip()
            if selected_classes and class_name not in selected_classes:
                continue
            source_path = indexes[repo_module].get(normalize_class_name(class_name))
            if not source_path:
                documents.append({"path": markdown_path, "error": "source HTML not found", "class": class_name})
                continue
            section = markdown[markdown.index(SECTION_5):]
            headings = [
                heading for heading in re.findall(r"(?m)^### (`[^\n]+`)\s*$", section)
                if looks_like_api_heading(heading)
            ]
            by_name, _ = source_for(source_path)
            items = select_source_items(headings, by_name)
            class_context = None
            for item, heading in zip(items, headings):
                if item.get("source", "").startswith("Reimplements:"):
                    base_match = re.search(r"`?([A-Za-z_]\w*(?:::[A-Za-z_]\w*)*)::([~A-Za-z_]\w*)", item["source"])
                    if base_match:
                        owner = base_match.group(1).replace("::", "_")
                        base_path = indexes[repo_module].get(normalize_class_name(owner))
                        if base_path and base_path != source_path:
                            base_members, _ = source_for(base_path)
                            base_candidates = base_members.get(base_match.group(2), [])
                            base_item = next(
                                (candidate for candidate in base_candidates if candidate.get("source") and not candidate["source"].startswith("Reimplements:")),
                                None,
                            )
                            if base_item:
                                item["source"] += "\n" + base_item["source"]
                if item.get("source"):
                    continue
                nested_key = normalize_class_name(class_name.replace("::", "_") + "_" + item["name"])
                related_path = indexes[repo_module].get(nested_key)
                if related_path:
                    context, code = context_for(related_path)
                    if context:
                        item.update(kind="nested", source=context, code=code)
                        continue

                plain_heading = heading.strip("` ")
                owner_match = re.search(
                    rf"([A-Za-z_]\w*(?:::[A-Za-z_]\w*)*(?:<[^>]+>)?)::{re.escape(item['name'])}\s*\(?",
                    plain_heading,
                )
                if owner_match:
                    owner = re.sub(r"<.*>", "", owner_match.group(1)).replace("::", "_")
                    owner_path = indexes[repo_module].get(normalize_class_name(owner))
                    if owner_path and owner_path != source_path:
                        owner_members, _ = source_for(owner_path)
                        candidates = owner_members.get(item["name"], [])
                        candidate = next((entry for entry in candidates if entry["source"]), None)
                        if candidate:
                            api_name = item["api_name"]
                            item.update(candidate)
                            item.update(kind="related", role=None, api_name=api_name)
                            continue

                specific = specific_fallback_translation(source_path, heading, item)
                if specific:
                    item.update(
                        kind="specific",
                        source=f"Member-specific explanation for {class_name}: {heading}",
                        code="",
                        manual_translation=specific,
                    )
                    continue

                if class_context is None:
                    class_context = context_for(source_path)
                context, code = class_context
                if context:
                    item.update(kind="context", source=context, code=code)
            documents.append({
                "path": markdown_path,
                "source_path": source_path,
                "markdown": markdown,
                "headings": headings,
                "items": items,
                "class": class_name,
            })
    return documents


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-root", type=Path, default=Path("D:/QTforGui/qt/Docs/Qt-6.11.1"))
    parser.add_argument("--module", action="append", choices=sorted(MODULES), help="limit processing to a repository module")
    parser.add_argument("--class", dest="classes", action="append", help="limit processing to an exact class name")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-translate", action="store_true", help="extract and report only")
    args = parser.parse_args()

    repo = args.repo.resolve()
    source_root = args.source_root.resolve()
    if not source_root.is_dir():
        parser.error(f"Qt documentation directory does not exist: {source_root}")

    documents = collect_documents(
        repo,
        source_root,
        set(args.module or []) or None,
        set(args.classes or []) or None,
    )
    missing_html = [doc for doc in documents if doc.get("error")]
    matched = [doc for doc in documents if not doc.get("error")]
    missing_members = sum(1 for doc in matched for item in doc["items"] if item["kind"] == "missing")
    total_members = sum(len(doc["items"]) for doc in matched)
    sources = {
        item["source"]
        for doc in matched
        for item in doc["items"]
        if item.get("source") and not item.get("manual_translation")
    }
    print(f"Matched {len(matched)} class pages and {total_members} API entries.")
    print(f"Unique source descriptions: {len(sources)}; entries without independent source text: {missing_members}.")
    if missing_html:
        print(f"Source HTML not found for {len(missing_html)} pages:")
        for doc in missing_html[:30]:
            print(f"  {doc['path'].relative_to(repo)} ({doc['class']})")

    if args.dry_run or args.no_translate:
        return 0

    cache_path = repo / ".cache" / "qt_docs_zh_v2.json"
    translations = translate_sources(sources, cache_path, args.workers)
    rendered = [
        (doc, replace_section(doc["markdown"], doc["items"], translations, doc["source_path"]))
        for doc in matched
    ]
    for doc, updated in rendered:
        doc["path"].write_text(updated, encoding="utf-8", newline="\n")
    print(f"Rewrote {len(matched)} Markdown class pages.")

    residual = []
    for doc in matched:
        text = doc["path"].read_text(encoding="utf-8")
        if any(marker in text[text.index(SECTION_5):] for marker in GENERIC_MARKERS):
            residual.append(doc["path"])
    if residual:
        print(f"WARNING: generic API prose remains in {len(residual)} pages")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
