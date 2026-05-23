"""
i18n 多语言翻译模块

用法：
    from i18n import t, load_locale, SUPPORTED, DEFAULT, LANG_NAMES, lang_url

    t("nav.home", "es")          → "Inicio"
    t("database.showing", n=42)  → "Showing 42 items"
    lang_url("/beginner-guide", "es") → "/es/beginner-guide"
"""
import json
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parents[1] / "locales"
SUPPORTED = ["en", "es", "pt", "de", "fr", "zh"]
DEFAULT = "en"

# 语言的本地化显示名（用于语言切换器）
LANG_NAMES = {
    "en": "English",
    "es": "Español",
    "pt": "Português",
    "de": "Deutsch",
    "fr": "Français",
    "zh": "中文",
}

# HTML lang 属性值
LANG_HTML = {
    "en": "en",
    "es": "es",
    "pt": "pt-BR",
    "de": "de",
    "fr": "fr",
    "zh": "zh-CN",
}

# 缓存已加载的语言文件
_cache = {}


def load_locale(lang):
    """加载指定语言的翻译字典，带缓存"""
    if lang in _cache:
        return _cache[lang]
    path = LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        if lang == DEFAULT:
            raise FileNotFoundError(f"Missing default locale file: {path}")
        # 回退到默认语言
        _cache[lang] = load_locale(DEFAULT)
        return _cache[lang]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    _cache[lang] = data
    return data


def _get_nested(data, key):
    """按 dot-separated key 获取嵌套字典值，如 'nav.home'"""
    parts = key.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def t(key, lang=DEFAULT, **kwargs):
    """
    获取翻译文本，支持变量插值。

    t("nav.home", "es")         → "Inicio"
    t("database.showing", "en", n=42) → "Showing 42 items"
    """
    if lang not in SUPPORTED:
        lang = DEFAULT
    data = load_locale(lang)
    value = _get_nested(data, key)

    # 回退到默认语言
    if value is None and lang != DEFAULT:
        data_default = load_locale(DEFAULT)
        value = _get_nested(data_default, key)

    if value is None:
        return key  # 找不到时返回 key 本身，方便调试

    if isinstance(value, str) and kwargs:
        try:
            return value.format(**kwargs)
        except (KeyError, IndexError):
            return value
    return value


def lang_url(path, lang=DEFAULT):
    """
    生成带语言前缀的 URL。

    lang_url("/beginner-guide", "en")  → "/beginner-guide"
    lang_url("/beginner-guide", "es")  → "/es/beginner-guide"
    lang_url("", "es")                 → "/es"
    """
    if lang == DEFAULT:
        return "/" if path == "" else path
    prefix = f"/{lang}"
    if path == "":
        return prefix
    return f"{prefix}{path}"


def hreflang_tags(slug, site="https://windrosewiki.games"):
    """
    生成所有语言的 hreflang 替代链接标签。

    hreflang_tags("beginner-guide")
    → ['<link rel="alternate" hreflang="en" href=".../beginner-guide">',
       '<link rel="alternate" hreflang="es" href=".../es/beginner-guide">',
       ...,
       '<link rel="alternate" hreflang="x-default" href=".../beginner-guide">']
    """
    tags = []
    path = "/" if slug == "" else f"/{slug}"
    for lang in SUPPORTED:
        href = site + lang_url(path, lang)
        tags.append(f'<link rel="alternate" hreflang="{LANG_HTML[lang]}" href="{href}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{site}{path}">')
    return tags


def lang_switcher_html(current_lang, current_path=""):
    """
    生成语言切换器下拉菜单 HTML。

    current_path: 当前页面路径，可以是 "tools"、"/tools"、"/zh/tools" 等。
    内部会规范化为以 "/" 开头(或为空字符串)的基础路径,然后用 lang_url
    生成各语言对应的链接。
    """
    import html as html_mod

    # 规范化：确保以 "/" 开头（除非完全为空）
    if current_path and not current_path.startswith("/"):
        current_path = "/" + current_path

    # 移除当前语言前缀，得到基础路径（如 "/tools" 或 ""）
    base_path = current_path
    for lang in SUPPORTED:
        prefix = f"/{lang}"
        if current_path == prefix:
            base_path = ""
            break
        if current_path.startswith(prefix + "/"):
            base_path = current_path[len(prefix):]
            break

    items_html = ""
    for lang in SUPPORTED:
        href = lang_url(base_path, lang)
        active = ' class="lang-active"' if lang == current_lang else ""
        name = LANG_NAMES[lang]
        items_html += f'<li><a href="{href}"{active}>{html_mod.escape(name)}</a></li>'

    current_name = LANG_NAMES.get(current_lang, current_lang)
    return f'''<div class="lang-switcher">
  <button class="lang-btn" aria-label="Language" aria-expanded="false">{html_mod.escape(current_name)} ▾</button>
  <ul class="lang-dropdown">{items_html}</ul>
</div>'''
