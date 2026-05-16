# 海外游戏攻略站开发规范 v1.1

> 目标：面向海外玩家，以纯静态HTML构建高性能游戏攻略站，最大化Google搜索流量与AI搜索曝光，通过Google AdSense变现。

---

## 如何使用本规范

本文档是**通用游戏攻略站开发规范**，适用于任何游戏的攻略站项目。它定义了 SEO、AI 搜索优化、AdSense、性能、多语言等通用标准。

具体游戏项目的执行方案（阶段划分、数据文件清单、脚本使用方式、内容补全策略等），请参阅对应的项目开发方案文档：

- Windrose Guides：`docs/windrose-dev-plan.md`

---

## 一、核心目标与原则

### 1.1 业务目标

| 指标 | 目标 |
|---|---|
| Google自然搜索流量 | 站点上线3个月内核心关键词进入前10页 |
| Core Web Vitals | 全绿（LCP < 2.5s, INP < 200ms, CLS < 0.1） |
| Google AdSense | 申请通过率100%，广告收益最大化 |
| AI搜索引用率 | 被ChatGPT/Perplexity/Google AI Overview引用 |
| 页面规模 | 单游戏站点 50-200个页面 |

### 1.2 技术原则

1. **纯静态HTML** — 零后端依赖，CDN直接分发
2. **SEO First** — 每个页面都是为搜索引擎设计的落地页
3. **AI Ready** — 结构化数据 + llms.txt，让AI爬虫能理解并引用
4. **自动化数据更新** — 脚本定时抓取游戏数据，自动更新HTML
5. **多语言扩展** — 一套代码支持多语言部署

---

## 二、技术架构

### 2.1 技术栈

```
┌─────────────────────────────────────────────────┐
│                    用户浏览器                      │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              Cloudflare Pages (CDN)               │
│  ┌───────────────────────────────────────────┐  │
│  │           纯静态 HTML/CSS/JS               │  │
│  │  • 每个页面独立 .html 文件                   │  │
│  │  • 内联关键CSS                              │  │
│  │  • 最小化JS（仅交互逻辑）                    │  │
│  └───────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────┐  ┌──────────────┐  ┌──────────┐
│ Google   │  │ AI Crawlers  │  │  用户     │
│ Search   │  │ ChatGPT/     │  │  直接     │
│ Console  │  │ Perplexity/  │  │  访问     │
│          │  │ Claude       │  │          │
└──────────┘  └──────────────┘  └──────────┘
```

### 2.2 目录结构

```
project-root/
├── index.html                    # 首页
├── codes.html                    # 兑换码
├── fish.html                     # 鱼类图鉴
├── recipes.html                  # 食谱
├── privacy.html                  # 隐私政策（AdSense必须）
├── about.html                    # 关于站点（AdSense必须）
├── contact.html                  # 联系方式（AdSense必须）
├── terms.html                    # 服务条款
├── 404.html                      # 404错误页面
├── _redirects                    # Cloudflare URL重写规则
├── ...                           # 其他页面
├── tools/
│   ├── index.html                # 工具入口
│   ├── checklist.html            # 每日清单
│   ├── calculator.html           # 计算器
│   └── timer.html                # 计时器
├── villagers/
│   ├── index.html                # NPC总览
│   ├── npc-name.html             # 单个NPC页面
│   └── ...
├── events/
│   ├── index.html                # 活动日程
│   └── event-slug.html           # 单个活动
├── es/                           # 西班牙语版本
├── de/                           # 德语版本
├── ja/                           # 日语版本
├── ko/                           # 韩语版本
├── fr/                           # 法语版本
├── pl/                           # 波兰语版本
├── id/                           # 印尼语版本
├── it/                           # 意大利语版本
├── llms.txt                      # AI爬虫引导文件
├── robots.txt                    # 爬虫控制
├── sitemap.xml                   # 站点地图
├── ads.txt                       # Google AdSense授权
├── imgs/                         # 图片资源（WebP格式）
│   ├── og.webp                   # Open Graph默认图
│   ├── fish/                     # 鱼类图片
│   └── ...
├── css/
│   └── theme.css                 # 全局主题（可选，也可内联）
├── js/
│   ├── site-chrome.js            # 导航/菜单/语言切换
│   ├── copy-code.js              # 兑换码复制
│   └── tools.js                  # 工具页面交互
├── scripts/                      # 自动化脚本（不部署到线上）
│   ├── update-codes.py           # 兑换码更新
│   ├── update-events.py          # 活动更新
│   ├── update-fish.py            # 图鉴数据更新
│   ├── build.py                  # HTML构建/模板渲染
│   ├── translate.py              # 多语言翻译
│   └── deploy.sh                 # 部署脚本
├── templates/                    # HTML模板（不部署）
│   ├── base.html                 # 基础模板
│   ├── codes.html.j2             # 兑换码模板
│   └── ...
├── data/                         # 结构化数据源（不部署到线上，确保不被CDN分发）
│   ├── codes.json
│   ├── fish.json
│   ├── recipes.json
│   ├── events.json
│   └── ...
└── docs/                         # 文档
```

### 2.3 托管与部署

| 项目 | 选择 | 理由 |
|---|---|---|
| **托管** | Cloudflare Pages | 免费额度大、全球CDN、自动HTTPS、Git集成 |
| **域名** | `.gg` / `.wiki` / `.guide` | 游戏站常用TLD，用户信任度高 |
| **版本控制** | GitHub Private Repo | 与Cloudflare Pages自动集成CI/CD |
| **CDN** | Cloudflare内置 | 300+边缘节点，TTFB极低 |
| **图片** | WebP + Cloudflare Image Resizing | 自动压缩、响应式 |

**部署流程**：
```
本地 scripts/build.py 渲染HTML
        │
        ▼
git push to main branch
        │
        ▼
Cloudflare Pages 自动构建部署（秒级）
        │
        ▼
全球CDN生效
```

---

## 三、SEO优化规范

### 3.1 页面级SEO要求

每个HTML页面**必须包含**以下元素：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- 1. 基础Meta -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- 2. Title — 格式: "核心关键词 - 修饰词 | 站名" -->
    <title>Heartopia Fish Guide - Locations, Sell Prices & Rare Fish (2026)</title>

    <!-- 3. Description — 150-160字符，含关键词，有行动召唤 -->
    <meta name="description" content="Complete Heartopia fish guide with all fish locations, sell prices, seasons, and rare fish catching tips. Updated for 2026.">

    <!-- 4. Canonical URL -->
    <link rel="canonical" href="https://yoursite.gg/fish">

    <!-- 5. Robots -->
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

    <!-- 6. Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://yoursite.gg/fish">
    <meta property="og:title" content="Heartopia Fish Guide - All Fish Locations & Prices">
    <meta property="og:description" content="Complete fish database with locations, seasons, and sell prices.">
    <meta property="og:image" content="https://yoursite.gg/imgs/og-fish.webp">
    <meta property="og:site_name" content="YourSite.gg">
    <meta property="article:published_time" content="2026-01-15">
    <meta property="article:modified_time" content="2026-04-14">

    <!-- 7. Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Heartopia Fish Guide - All Fish Locations & Prices">
    <meta name="twitter:description" content="Complete fish database with locations, seasons, and sell prices.">
    <meta name="twitter:image" content="https://yoursite.gg/imgs/og-fish.webp">

    <!-- 8. Hreflang（多语言页面必须） -->
    <link rel="alternate" hreflang="en" href="https://yoursite.gg/fish">
    <link rel="alternate" hreflang="es" href="https://yoursite.gg/es/fish">
    <link rel="alternate" hreflang="ja" href="https://yoursite.gg/ja/fish">
    <link rel="alternate" hreflang="x-default" href="https://yoursite.gg/fish">

    <!-- 9. JSON-LD 结构化数据（见3.2节） -->
    <script type="application/ld+json">...</script>
</head>
```

### 3.2 JSON-LD 结构化数据规范

每个页面**至少包含**以下Schema类型：

#### 3.2.1 所有页面必须

```json
{
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "url": "https://yoursite.gg/",
            "name": "YourSite.gg - Game Wiki & Database",
            "publisher": { "@id": "https://yoursite.gg/#org" }
        },
        {
            "@type": "Organization",
            "@id": "https://yoursite.gg/#org",
            "name": "YourSite.gg",
            "url": "https://yoursite.gg/",
            "sameAs": ["Discord链接", "Twitter链接"]
        },
        {
            "@type": "WebPage",
            "url": "https://yoursite.gg/fish",
            "name": "Fish Guide",
            "dateModified": "2026-04-14",
            "isPartOf": { "@id": "https://yoursite.gg/#website" },
            "breadcrumb": { "@id": "https://yoursite.gg/#breadcrumb" }
        },
        {
            "@type": "BreadcrumbList",
            "@id": "https://yoursite.gg/#breadcrumb",
            "itemListElement": [
                { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://yoursite.gg/" },
                { "@type": "ListItem", "position": 2, "name": "Fish Guide", "item": "https://yoursite.gg/fish" }
            ]
        }
    ]
}
```

#### 3.2.2 按页面类型添加

> **重要**：页面专属 Schema（`FAQPage`、`HowTo`、`ItemList` 等）需作为 `@graph` 数组中的独立顶层条目添加，不要嵌套在其他 Schema 内部，否则 Google 可能无法正确解析富片段。

| 页面类型 | 额外Schema | 用途 |
|---|---|---|
| 首页 | `VideoGame` | 声明游戏元数据 |
| 兑换码页 | `HowTo` | "How to redeem codes" 富片段 |
| FAQ相关 | `FAQPage` | Google FAQ富片段 |
| 数据库页 | `ItemList` + `Dataset` | 列表型富片段 |
| 活动页 | `Event` | 活动富片段 |
| 攻略页 | `HowTo` + `Article` | 操作指南富片段 |
| NPC/角色 | `Person` | 角色信息富片段 |
| 工具页 | `SoftwareApplication` | 工具型富片段 |

#### 3.2.3 VideoGame Schema（首页必须）

```json
{
    "@type": "VideoGame",
    "name": "Game Name",
    "alternateName": ["中文名", "日文名"],
    "description": "游戏描述",
    "genre": ["Life Simulation", "Casual", "Multiplayer"],
    "gamePlatform": ["iOS", "Android", "PC", "Steam"],
    "author": {
        "@type": "Organization",
        "name": "开发商名称"
    },
    "datePublished": "2026-01-07",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.5",
        "ratingCount": "50000"
    }
}
```

### 3.3 URL规范

| 规则 | 示例 |
|---|---|
| 全小写 | `/fish` 不是 `/Fish` |
| 连字符分隔 | `/flower-crossbreeding` 不是 `/flowerCrossbreeding` |
| 语义化 | `/beginner-guide` 不是 `/page12` |
| 扁平结构 | 最多2层 `/villagers/npc-name` |
| 年份标记 | 标题含 `(2026)` 提升时效性CTR |

**无扩展名 URL 实现方式**（二选一）：

| 方案 | 说明 | 目录结构示例 |
|---|---|---|
| **目录方案（推荐）** | 每个页面创建同名目录，`index.html`放其中 | `fish/index.html` → 访问 `/fish` |
| **重写方案** | 平铺 `.html`，Cloudflare `_redirects` 重写 | `fish.html` → `_redirects` 映射 `/fish` |

Cloudflare Pages 默认支持目录方案，无需额外配置。重写方案需在根目录放置 `_redirects` 文件：

```
/fish              /fish.html              200
/codes             /codes.html             200
/tools/*           /tools/:splat.html      200
```

### 3.4 内容SEO要求

#### 标题层级

```html
<h1>页面主标题（每页仅1个）</h1>
  <h2>主要板块标题</h2>
    <h3>子板块标题</h3>
      <h4>细分内容标题</h4>
```

#### 内容密度要求

| 指标 | 要求 |
|---|---|
| H1 | 每页1个，含核心关键词 |
| H2 | 每页3-8个，含相关关键词 |
| 正文字数 | 数据页 1500-3000字，攻略页 2000-5000字 |
| 图片 | 每页至少3张，含alt属性 |
| 内链 | 每页至少5个站内链接 |
| 外链 | 至少1个权威外链（官方站点） |

#### 关键词策略

```
主关键词:    "game name fish guide"        → Title, H1, Meta Description
次关键词:    "game name fish locations"    → H2, 正文前100字
长尾关键词:  "how to catch rare fish in game name" → H3, FAQ
LSI关键词:  "fishing rod, bait, river, ocean"    → 正文自然分布
```

#### 内链策略

| 链接类型 | 说明 | 示例 |
|---|---|---|
| **Hub→子页** | 列表页链接到每个详情页 | `/fish` 链接到每个鱼种页面 |
| **子页→Hub** | 详情页链接回所属列表页 | 鱼种页链接回 `/fish` |
| **上下文内链** | 内容中自然引用相关页面 | 食谱页提到某鱼 → 链接到该鱼页面 |
| **相关推荐** | 页面底部推荐相关页面 | "你可能还需要：钓鱼指南" |
| **面包屑** | 每页显示层级导航 | Home > Fish Guide > Golden Carp |

### 3.5 Sitemap规范

```xml
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://yoursite.gg/fish</loc>
    <lastmod>2026-04-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
    <!-- 多语言版本 -->
    <xhtml:link rel="alternate" hreflang="en" href="https://yoursite.gg/fish"/>
    <xhtml:link rel="alternate" hreflang="es" href="https://yoursite.gg/es/fish"/>
  </url>
</urlset>
```

**更新频率策略**：

| 页面类型 | changefreq | priority |
|---|---|---|
| 首页 | daily | 1.0 |
| 兑换码 | daily | 0.9 |
| 活动 | weekly | 0.8 |
| 图鉴/数据库 | weekly | 0.8 |
| 攻略 | monthly | 0.7 |
| 工具 | monthly | 0.6 |
| 静态页(about/terms) | yearly | 0.3 |

---

## 四、AI搜索优化规范

### 4.1 llms.txt 文件

每个站点根目录**必须**包含 `llms.txt`，引导AI爬虫理解站点结构：

```markdown
# SiteName.gg

> One-line description of the site and what it covers.

## About This Site

Brief description of the site's purpose, scope, and maintenance.

## Main Sections

### [Section Name](https://yoursite.gg/section)
- [Page Name](https://yoursite.gg/page): One-line description of the page content

### [Section Name](https://yoursite.gg/section2)
- [Page Name](https://yoursite.gg/page2): Description

## Key Topics

- Topic 1: brief description
- Topic 2: brief description

## Contact

Website: https://yoursite.gg
```

**要求**：
- 保持与站点结构同步更新
- 每个页面条目包含URL和一句话描述
- 总长度控制在2000字以内
- 使用Markdown格式

### 4.2 robots.txt AI爬虫配置

```txt
# 搜索引擎
User-agent: *
Allow: /
Disallow: /.git/
Disallow: /scripts/
Disallow: /data/
Disallow: /templates/
Disallow: /docs/

# AI爬虫 - 允许并引导到llms.txt
User-agent: GPTBot
Allow: /
Allow: /llms.txt

User-agent: ChatGPT-User
Allow: /
Allow: /llms.txt

User-agent: ClaudeBot
Allow: /
Allow: /llms.txt

User-agent: Claude-Web
Allow: /
Allow: /llms.txt

User-agent: anthropic-ai
Allow: /
Allow: /llms.txt

User-agent: PerplexityBot
Allow: /
Allow: /llms.txt

User-agent: GoogleOther
Allow: /
Allow: /llms.txt

User-agent: Google-Extended
Allow: /
Allow: /llms.txt

User-agent: Applebot-Extended
Allow: /
Allow: /llms.txt

User-agent: cohere-ai
Allow: /
Allow: /llms.txt

User-agent: Meta-ExternalAgent
Allow: /
Allow: /llms.txt

# 内容信号
Content-Signal: search=yes,ai-train=no

Sitemap: https://yoursite.gg/sitemap.xml
```

### 4.3 AI友好内容结构

AI搜索引擎偏好以下内容结构，每个页面应尽量包含：

#### 4.3.1 FAQ区块（每个页面底部）

```html
<section id="faq">
    <h2>Frequently Asked Questions</h2>

    <details>
        <summary>What is the rarest fish in [Game]?</summary>
        <p>The rarest fish is [Fish Name], found only in [Location] during [Season]...</p>
    </details>

    <details>
        <summary>How do I unlock fishing in [Game]?</summary>
        <p>Fishing is unlocked after completing the tutorial quest...</p>
    </details>
</section>
```

同时在JSON-LD中添加 `FAQPage` Schema。

#### 4.3.2 定义/解释区块

```html
<section>
    <h2>What is [Concept]?</h2>
    <p><strong>[Concept]</strong> is [clear, concise definition in one sentence].
    [2-3 sentences of elaboration with key details.]</p>
</section>
```

#### 4.3.3 步骤指南区块

```html
<section>
    <h2>How to [Action] in [Game]</h2>
    <ol>
        <li><strong>Step 1:</strong> [Action description]</li>
        <li><strong>Step 2:</strong> [Action description]</li>
    </ol>
</section>
```

同时在JSON-LD中添加 `HowTo` Schema。

#### 4.3.4 数据表格

```html
<table>
    <caption>Complete Fish List in [Game]</caption>
    <thead>
        <tr>
            <th>Fish Name</th>
            <th>Location</th>
            <th>Season</th>
            <th>Sell Price</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Golden Carp</td>
            <td>River</td>
            <td>Spring</td>
            <td>500 Gold</td>
        </tr>
    </tbody>
</table>
```

### 4.4 AI搜索优化检查清单

每个页面发布前检查：

- [ ] JSON-LD结构化数据完整且无错误
- [ ] 至少1个FAQ条目（含FAQPage Schema）
- [ ] 至少1个清晰的定义段落
- [ ] 数据以`<table>`呈现而非图片
- [ ] H1-H4层级清晰无跳级
- [ ] 正文首段包含页面核心问题的答案
- [ ] 内容使用自然语言，适合被AI引用
- [ ] llms.txt已同步更新（如新增页面）

---

## 五、Google AdSense规范

### 5.1 广告位布局

```
┌─────────────────────────────────────────┐
│  Header / Navigation                     │
├─────────────────────────────────────────┤
│  [AdSense Banner 728x90 - Desktop]      │
├────────────────────┬────────────────────┤
│                    │                    │
│  Main Content      │  Sidebar           │
│                    │  [Ad 300x250]      │
│  H1 Title          │                    │
│  ...content...     │  [Ad 300x250]      │
│                    │                    │
│  H2 Section        │  Related Links     │
│  ...content...     │                    │
│                    │                    │
│  [In-Article Ad]   │                    │
│                    │                    │
│  H2 Section        │                    │
│  ...content...     │                    │
│                    │                    │
│  FAQ Section       │                    │
│                    │                    │
├────────────────────┴────────────────────┤
│  [AdSense Banner 728x90 - Before Footer]│
├─────────────────────────────────────────┤
│  Footer                                  │
└─────────────────────────────────────────┘
```

### 5.2 广告位规范

| 位置 | 尺寸 | 类型 | 限制 |
|---|---|---|---|
| Header下方 | 728x90 (桌面) / 320x50 (移动) | Display | 仅桌面端展示 |
| 内容区中段 | 自适应 | In-Article | 段落之间，不少于300字间隔 |
| 侧边栏 | 300x250 | Display | 仅桌面端，sticky |
| 底部 | 728x90 | Display | 内容区结束后 |
| 移动端锚定 | 320x50 | Anchor | 底部固定 |

### 5.3 AdSense申请前置条件

站点上线前**必须满足**：

| 条件 | 要求 |
|---|---|
| 原创内容 | 至少30个高质量页面 |
| 隐私政策 | `/privacy` 页面必须存在 |
| 关于页面 | `/about` 页面必须存在 |
| 联系方式 | `/contact` 页面必须存在 |
| 导航结构 | 清晰的菜单和面包屑 |
| 内容质量 | 无抄袭、无自动生成痕迹 |
| 域名年龄 | 建议至少1个月 |
| 流量 | 无硬性要求，但有自然流量更易通过 |
| ads.txt | 根目录放置Google提供的ads.txt |

### 5.4 广告密度控制

- 每个屏幕视口最多1个广告
- 内容与广告面积比不低于 70:30
- 移动端广告间距不小于300px
- 不在首屏放置超过1个广告
- 不在纯文本段落中插入广告（仅在段落之间）

**CLS 防护**：广告加载是 Cumulative Layout Shift 的主要来源，必须为广告容器预留空间：

```css
.ad-slot {
    min-height: 90px;
    background: #f5f5f5;
}
.ad-slot-sidebar {
    min-height: 250px;
    background: #f5f5f5;
}
@media (max-width: 768px) {
    .ad-slot { min-height: 50px; }
}
```

---

## 六、游戏攻略站模块规范

### 6.1 模块分类总览

根据游戏类型，攻略站应包含以下模块。标注 `[必选]` 的为所有游戏类型都应包含的模块。

```
┌─────────────────────────────────────────────────────┐
│                  通用模块 [所有游戏必选]                │
├─────────────────────────────────────────────────────┤
│  首页 / 兑换码 / 新手指南 / 下载指南 / 活动日程         │
│  版本更新 / FAQ / 工具集 / 社区链接 / 多语言            │
├─────────────────────────────────────────────────────┤
│                 游戏类型专属模块                        │
├─────────────────────────────────────────────────────┤
│  生存建造 / 开放世界 / RPG / 卡牌/抽卡 / 竞技/MOBA     │
│  模拟经营 / 沙盒 / 恐怖/解谜 / 音游                    │
└─────────────────────────────────────────────────────┘
```

---

### 6.2 通用模块（所有游戏攻略站必选）

#### 6.2.1 首页 `/`

| 元素 | 说明 |
|---|---|
| Hero区 | 游戏名 + 一句话定位 + CTA按钮（兑换码/新手指南） |
| 快速导航 | 8个核心入口卡片（图标+标题+描述） |
| 最新兑换码 | 展示3-5个最新有效码 |
| 最新活动 | 当前进行中的活动 |
| 数据库入口 | 图鉴/食谱等数据库板块入口 |
| 热门攻略 | Top 5热门攻略链接 |
| 工具入口 | 交互工具入口 |
| FAQ | 5-8个常见问题 |
| 社区链接 | Discord/Twitter/Reddit |
| 关于站点 | 简短介绍 |

#### 6.2.2 兑换码页 `/codes`

| 元素 | 说明 |
|---|---|
| 有效码列表 | 卡片式展示：码字 + 奖励描述 + 一键复制 + 过期时间 |
| 过期码归档 | 分区展示，标注已过期 |
| 兑换教程 | HowTo Schema，步骤式说明 |
| 更新频率说明 | "每日更新"提示 |
| 订阅提醒 | .ics日历订阅链接 |
| FAQ | 多少个码、能否重复用、码从哪来 |

**数据结构** (`data/codes.json`)：

```json
{
    "lastUpdated": "2026-04-14",
    "active": [
        {
            "code": "keepsmiling2026",
            "rewards": "Wishing Star x5, Mermaid Fish Attractor x3",
            "expiryDate": "2026-06-29",
            "isNew": true,
            "verifiedDate": "2026-04-12"
        }
    ],
    "expired": [
        {
            "code": "launch2026",
            "rewards": "Gold x1000",
            "expiryDate": "2026-02-01"
        }
    ]
}
```

#### 6.2.3 新手指南 `/beginner-guide`

| 元素 | 说明 |
|---|---|
| 游戏简介 | What is [Game]? 定义段落 |
| 初始流程 | 前30分钟/前1小时该做什么 |
| 核心系统介绍 | 列出所有核心玩法系统 + 链接 |
| 新手常犯错误 | 编号列表 |
| 进阶路线图 | 从新手到进阶的路径 |
| FAQ | 新手最常问的问题 |

#### 6.2.4 下载指南 `/download`

| 元素 | 说明 |
|---|---|
| 平台列表 | iOS/Android/PC/Switch 各平台下载按钮 |
| 系统要求 | 每个平台的最低/推荐配置 |
| 下载教程 | HowTo Schema |
| 跨平台说明 | 是否支持跨平台、跨存档 |
| FAQ | 安全性、APK风险等 |

#### 6.2.5 活动日程 `/events`

| 元素 | 说明 |
|---|---|
| 当前活动 | 进行中的活动卡片（名称+时间+奖励+链接） |
| 即将到来 | 预告活动 |
| 历史活动 | 已结束活动归档 |
| Banner/卡池日程 | 如适用 |
| 日历视图 | 月度活动总览 |

**数据结构** (`data/events.json`)：

```json
{
    "lastUpdated": "2026-04-21",
    "current": [
        {
            "name": "My Little Pony Collaboration",
            "slug": "my-little-pony",
            "startDate": "2026-04-30",
            "endDate": "2026-05-30",
            "description": "Limited-time collaboration event",
            "rewards": "Exclusive furniture, outfits",
            "status": "upcoming"
        }
    ],
    "past": []
}
```

#### 6.2.6 版本更新 `/version-history`

| 元素 | 说明 |
|---|---|
| 最新版本 | 版本号 + 发布日期 + 更新内容 |
| 历史版本 | 按时间倒序排列 |
| 版本对比 | 新增/修复/移除内容 |

#### 6.2.7 工具集 `/tools`

根据游戏类型提供不同工具：

| 工具类型 | 适用游戏 | 示例 |
|---|---|---|
| 利润计算器 | 经营/模拟 | 计算最佳售卖物品 |
| 每日清单 | 所有游戏 | 每日任务追踪 |
| 计时器 | 所有游戏 | 重置倒计时 |
| 规划器 | 经营/建造 | 农作物/建筑规划 |
| 追踪器 | 收集类 | 收集进度追踪 |
| 搜索器 | 数据库类 | 物品/食谱搜索 |
| 模拟器 | RPG/卡牌 | 配装/抽卡模拟 |

#### 6.2.8 多语言首页

每个语言版本首页 (`/es`, `/ja`, `/ko` 等) 应包含：

- 该语言的完整导航
- hreflang指向所有语言版本
- 翻译后的内容（非机翻痕迹）
- 本地化的关键词策略

---

### 6.3 游戏类型专属模块

#### 6.3.1 生活模拟/休闲类 (如 Heartopia, Stardew Valley, Animal Crossing)

```
├── /fish                    [必选] 鱼类图鉴
│   └── 鱼名、位置、季节、时间、售价、稀有度、钓法
├── /bugs                    [必选] 昆虫图鉴
│   └── 昆虫名、位置、出现条件、售价
├── /birds                   [可选] 鸟类图鉴
├── /flowers                 [必选] 花卉图鉴
│   └── /flower-crossbreeding  杂交指南
├── /crops                   [必选] 农作物图鉴
│   └── 种子名、生长时间、利润、季节
├── /recipes                 [必选] 烹饪食谱
│   └── 菜名、食材、售价、解锁条件
├── /materials               [必选] 材料图鉴
├── /furniture               [必选] 家具图鉴
│   └── /blueprints          蓝图列表
├── /outfits                 [必选] 服装图鉴
├── /villagers/              [必选] NPC页面
│   └── /villagers/{name}    单个NPC详情
│       └── 位置、喜好礼物、日程、解锁条件
├── /npc-gifts               [必选] NPC送礼攻略
├── /pets                    [必选] 宠物系统
│   └── /cat-breeds, /dog-breeds
├── /wild-animals            [可选] 野生动物
├── /building                [必选] 建造指南
│   └── /home-plots          地块解锁
│   └── /house-designs       房屋设计
│   └── /storage             仓库系统
├── /gardening               [必选] 园艺系统
├── /hobbies                 [必选] 爱好/技能系统
├── /shops                   [必选] 商店列表
├── /economy                 [必选] 经济系统
│   └── /money-guide         赚钱攻略
│   └── /selling-guide       出售指南
├── /multiplayer             [必选] 多人联机
└── /gallery/                [可选] 设计灵感图库
```

#### 6.3.2 开放世界/动作RPG类 (如 Genshin Impact, Wuthering Waves)

```
├── /characters              [必选] 角色列表
│   └── /characters/{name}   角色详情
│       └── 技能、命座、武器、圣遗物、配队
├── /tier-list               [必选] 角色强度排行
├── /weapons                 [必选] 武器图鉴
├── /artifacts               [必选] 圣遗物/遗器
├── /teams                   [必选] 配队推荐
│   └── /teams/{character}   按角色查配队
├── /enemies                 [必选] 敌人/BOSS图鉴
│   └── 弱点、掉落物、打法
├── /quests                  [必选] 任务攻略
│   └── /quests/{quest-slug} 单个任务详解
├── /map                     [必选] 交互地图
│   └── 宝箱、神瞳、采集点、BOSS位置
├── /materials               [必选] 突破材料
│   └── 材料获取路线
├── /events                  [必选] 活动攻略
├── /codes                   [必选] 兑换码
├── /spiral-abyss            [可选] 深渊/挑战
│   └── 每期阵容推荐
├── /builds                  [必选] 角色养成方案
│   └── /builds/{character}  单角色养成
├── /lore                    [可选] 剧情/世界观
└── /guides/
    ├── beginner-guide       [必选]
    ├── resin-guide          [必选] 体力系统
    ├── gacha-guide          [必选] 抽卡机制
    └── exploration-guide    [可选] 探索攻略
```

#### 6.3.3 卡牌/抽卡/二次元手游类 (如 Honkai Star Rail, Blue Archive, Nikke)

```
├── /characters              [必选] 角色列表
│   └── /characters/{name}   角色详情
│       └── 技能倍率、养成材料、推荐装备
├── /tier-list               [必选] 角色/武器排行
├── /teams                   [必选] 编队推荐
├── /gacha                   [必选] 卡池日程/概率分析
│   └── /gacha/simulator     抽卡模拟器
├── /codes                   [必选] 兑换码
├── /events                  [必选] 活动攻略
├── /raids                   [可选] Raid/BOSS攻略
├── /pvp                     [可选] PVP/竞技场
│   └── 阵容推荐、赛季排名
├── /stages                  [可选] 关卡攻略
│   └── /stages/{chapter}    章节关卡
├── /items                   [必选] 物品/装备图鉴
├── /calculator/
│   ├── damage-calculator    [推荐] 伤害计算器
│   ├── gacha-calculator     [推荐] 抽卡概率计算器
│   └── resource-calculator  [推荐] 资源规划器
└── /guides/
    ├── beginner-guide       [必选]
    ├── reroll-guide         [必选] 刷初始指南
    ├── progression-guide    [必选] 养成路线
    └── currency-guide       [必选] 货币系统
```

#### 6.3.4 竞技/MOBA/FPS类 (如 Valorant, Apex Legends, Mobile Legends)

```
├── /agents                  [必选] 角色/英雄列表
│   └── /agents/{name}       角色详情
│       └── 技能、打法、最佳地图
├── /tier-list               [必选] 英雄/武器强度排行
├── /maps                    [必选] 地图攻略
│   └── /maps/{name}         单地图详情
│       └── 报点、烟位、架枪位
├── /weapons                 [必选] 武器/装备数据
├── /crosshairs              [可选] 准星分享
├── /lineups                 [可选] 技能点位
│   └── /lineups/{agent}     按角色查点位
├── /codes                   [可选] 兑换码
├── /patch-notes             [必选] 版本更新
├── /ranked                  [必选] 排位系统指南
├── /esports                 [可选] 电竞资讯
│   └── 赛程、战队、选手
├── /settings                [必选] 最佳设置推荐
│   └── 灵敏度、画质、键位
└── /guides/
    ├── beginner-guide       [必选]
    ├── aim-guide            [必选] 枪法/操作指南
    ├── economy-guide        [可选] 经济系统
    └── agent-guides         [必选] 角色攻略合集
```

#### 6.3.5 生存/沙盒类 (如 Minecraft, Terraria, Palworld)

```
├── /items                   [必选] 物品图鉴
│   └── 物品ID、获取方式、用途
├── /crafting                [必选] 合成表
│   └── /crafting/{item}     单物品合成路径
├── /mobs                    [必选] 生物图鉴
│   └── 生成条件、掉落物、行为
├── /biomes                  [必选] 生态群系
├── /enchantments            [可选] 附魔系统
├── /redstone                [可选] 红石/电路
├── /farms                   [必选] 自动化农场
│   └── /farms/{type}        各类农场教程
├── /builds                  [必选] 建筑教程
├── /seeds                   [可选] 种子分享
├── /commands                [可选] 指令/命令
├── /mods                    [可选] Mod推荐
├── /servers                 [可选] 服务器推荐
├── /codes                   [可选] 兑换码
└── /guides/
    ├── beginner-guide       [必选]
    ├── survival-guide       [必选] 生存指南
    ├── boss-guide           [必选] BOSS攻略
    ├── farming-guide        [必选] 刷资源指南
    └── progression-guide    [必选] 流程攻略
```

#### 6.3.6 模拟经营类 (如 Cities Skylines, Two Point Hospital)

```
├── /buildings               [必选] 建筑列表
├── /resources               [必选] 资源系统
├── /economy                 [必选] 经济系统
├── /maps                    [必选] 地图/布局
├── /guides/
    ├── beginner-guide       [必选]
    ├── budget-guide         [必选] 财政指南
    ├── traffic-guide        [可选] 交通规划
    ├── efficiency-guide     [必选] 效率优化
    └── mod-guide            [可选] Mod推荐
└── /calculator/
    ├── profit-calculator    [必选] 利润计算
    └── layout-planner       [推荐] 布局规划
```

#### 6.3.7 恐怖/解谜类 (如 Phasmophobia, Lethal Company)

```
├── /ghosts                  [必选] 鬼魂/敌人图鉴
│   └── 特征、弱点、识别方法
├── /maps                    [必选] 地图攻略
│   └── 房间分布、安全点、道具位置
├── /equipment               [必选] 装备/道具
├── /evidence                [必选] 证据系统
├── /contracts               [可选] 任务/合同
├── /guides/
    ├── beginner-guide       [必选]
    ├── evidence-guide       [必选] 证据识别
    ├── survival-guide       [必选] 生存技巧
    └── speedrun-guide       [可选] 速通攻略
└── /tools/
    ├── evidence-tracker     [必选] 证据追踪器
    └── ghost-identifier     [必选] 鬼魂识别器
```

#### 6.3.8 音乐/节奏类 (如 Project Sekai, Bandori)

```
├── /characters              [必选] 角色列表
├── /songs                   [必选] 曲目列表
│   └── /songs/{name}        曲目详情
│       └── 难度、谱面分析、AP技巧
├── /cards                   [必选] 卡牌图鉴
├── /events                  [必选] 活动攻略
├── /tier-list               [必选] 卡牌强度排行
├── /teams                   [必选] 编队推荐
├── /gacha                   [必选] 卡池日程
├── /codes                   [必选] 兑换码
└── /guides/
    ├── beginner-guide       [必选]
    ├── ap-guide             [必选] 全Perfect攻略
    ├── event-guide          [必选] 活动刷分
    └── resource-guide       [必选] 资源规划
```

---

## 七、自动化数据更新系统

### 7.1 架构总览

```
┌──────────────────────────────────────────────────────┐
│                  定时调度 (Cron/GitHub Actions)         │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ 每日任务  │  │ 每周任务  │  │ 事件驱动  │            │
│  │          │  │          │  │          │            │
│  │ • 兑换码  │  │ • 图鉴   │  │ • 版本更新│            │
│  │ • 活动   │  │ • 数据校验│  │ • 新活动  │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       │              │              │                  │
│       ▼              ▼              ▼                  │
│  ┌─────────────────────────────────────────────────┐  │
│  │              数据采集层 (Data Scrapers)           │  │
│  │                                                  │  │
│  │  • 官方API（如有）                                │  │
│  │  • 官方社交媒体爬取（Discord/Twitter）              │  │
│  │  • Wiki数据爬取                                   │  │
│  │  • 游戏数据包解析                                  │  │
│  │  • 社区数据聚合                                    │  │
│  └──────────────────────┬──────────────────────────┘  │
│                         │                              │
│                         ▼                              │
│  ┌─────────────────────────────────────────────────┐  │
│  │              数据处理层 (Data Processing)         │  │
│  │                                                  │  │
│  │  data/codes.json                                 │  │
│  │  data/fish.json                                  │  │
│  │  data/events.json                                │  │
│  │  data/recipes.json                               │  │
│  │  ...                                             │  │
│  └──────────────────────┬──────────────────────────┘  │
│                         │                              │
│                         ▼                              │
│  ┌─────────────────────────────────────────────────┐  │
│  │              HTML构建层 (Build)                   │  │
│  │                                                  │  │
│  │  templates/*.j2  +  data/*.json                  │  │
│  │              │                                    │  │
│  │              ▼                                    │  │
│  │         输出 HTML 文件                            │  │
│  └──────────────────────┬──────────────────────────┘  │
│                         │                              │
│                         ▼                              │
│  ┌─────────────────────────────────────────────────┐  │
│  │              部署层 (Deploy)                      │  │
│  │                                                  │  │
│  │  git commit + push → Cloudflare Pages            │  │
│  │  更新 sitemap.xml lastmod                        │  │
│  │  更新 llms.txt                                   │  │
│  └─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### 7.2 数据源定义

#### 7.2.1 兑换码数据源

```python
# scripts/update_codes.py
"""
数据源优先级：
1. 官方Discord频道（webhook/RSS）
2. 官方Twitter/X API
3. 官方社区公告
4. 社区Wiki更新
5. 人工提交（GitHub PR）

采集频率：每6小时
"""

SOURCES = [
    {
        "name": "official_discord",
        "type": "webhook",  # 或 RSS
        "url": "https://discord.com/api/webhooks/...",
        "parser": "parse_discord_codes"
    },
    {
        "name": "official_twitter",
        "type": "api",
        "credentials": "env:TWITTER_BEARER_TOKEN",
        "query": "from:game_official code",
        "parser": "parse_twitter_codes"
    },
    {
        "name": "community_wiki",
        "type": "scraper",
        "url": "https://game.fandom.com/wiki/Codes",
        "parser": "parse_wiki_codes"
    }
]
```

#### 7.2.2 活动数据源

```python
# scripts/update_events.py
"""
数据源：
1. 游戏内公告API（如可用）
2. 官方公告页面爬取
3. 官方社交媒体
4. 社区维护的活动日历

采集频率：每12小时
"""
```

#### 7.2.3 图鉴数据源

```python
# scripts/update_database.py
"""
数据源：
1. 游戏数据包（datamining）
2. 官方Wiki
3. 社区维护的数据库
4. GitHub社区贡献的JSON数据

采集频率：每周1次（游戏更新时触发）
"""
```

### 7.3 模板系统

使用 Jinja2 模板引擎，将数据渲染为HTML：

```python
# scripts/build.py
"""
构建流程：
1. 加载 data/*.json
2. 加载 templates/*.j2
3. 渲染为 HTML
4. 输出到站点根目录
5. 更新 sitemap.xml
6. 更新 llms.txt
"""

from jinja2 import Environment, FileSystemLoader
import json
import os

def build_page(template_name, output_name, data):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    html = template.render(**data)

    with open(output_name, 'w', encoding='utf-8') as f:
        f.write(html)

# 示例：构建兑换码页面
codes_data = json.load(open('data/codes.json'))
build_page('codes.html.j2', 'codes.html', {
    'codes': codes_data,
    'page_title': f"Game Codes - All Active Codes ({codes_data['lastUpdated']})",
    'meta_description': f"All active game codes as of {codes_data['lastUpdated']}...",
    'canonical_url': 'https://yoursite.gg/codes',
    # ... 其他SEO数据
})
```

### 7.4 模板示例

```html
{# templates/codes.html.j2 #}
<!DOCTYPE html>
<html lang="en">
<head>
    {% include 'partials/head.html.j2' %}
    <title>{{ page_title }}</title>
    <meta name="description" content="{{ meta_description }}">
    <link rel="canonical" href="{{ canonical_url }}">

    <!-- HowTo Schema -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to Redeem Codes in {{ game_name }}",
        "step": [
            {% for step in redeem_steps %}
            {
                "@type": "HowToStep",
                "position": {{ loop.index }},
                "name": "{{ step.name }}",
                "text": "{{ step.text }}"
            }{% if not loop.last %},{% endif %}
            {% endfor %}
        ]
    }
    </script>
</head>
<body>
    {% include 'partials/header.html.j2' %}

    <main>
        <h1>{{ game_name }} Codes - All Active Codes</h1>
        <span class="update-badge">Last Updated: {{ codes.lastUpdated }}</span>

        <!-- 有效码 -->
        <section>
            <h2>Active Codes</h2>
            <div class="code-list">
                {% for code in codes.active %}
                <div class="code-item {% if code.isNew %}new{% endif %}"
                     data-status="active">
                    <div class="code-info">
                        <span class="code-text">{{ code.code }}</span>
                        {% if code.isNew %}
                        <span class="new-badge">NEW VERIFIED</span>
                        {% endif %}
                        <p class="code-reward">
                            {{ code.rewards }}
                            {% if code.expiryDate %}
                            • Expires: {{ code.expiryDate }}
                            {% else %}
                            • No listed end date yet
                            {% endif %}
                        </p>
                    </div>
                    <button class="copy-btn"
                            onclick="copyCode('{{ code.code }}', this)">
                        Copy
                    </button>
                </div>
                {% endfor %}
            </div>
        </section>

        <!-- 兑换教程 -->
        <section>
            <h2>How to Redeem Codes</h2>
            <ol>
                {% for step in redeem_steps %}
                <li><strong>{{ step.name }}:</strong> {{ step.text }}</li>
                {% endfor %}
            </ol>
        </section>

        <!-- FAQ -->
        {% include 'partials/faq.html.j2' %}
    </main>

    {% include 'partials/footer.html.j2' %}
    <script src="/js/site-chrome.js" defer></script>
</body>
</html>
```

### 7.5 GitHub Actions 自动化

> **注意**：每个定时任务应拆分为独立的 workflow 文件，因为 GitHub Actions 的 `schedule` 事件无法在 `if` 条件中区分具体是哪个 cron 触发的。

**`.github/workflows/update-codes.yml`** — 每6小时检查兑换码：

```yaml
name: Update Codes Data

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      - name: Update codes data
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          TWITTER_TOKEN: ${{ secrets.TWITTER_TOKEN }}
        run: python scripts/update_codes.py
      - name: Build HTML
        run: python scripts/build.py
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --cached --quiet || git commit -m "chore: update codes [skip ci]"
          git push
```

**`.github/workflows/update-events.yml`** — 每天检查活动：

```yaml
name: Update Events Data

on:
  schedule:
    - cron: '0 8 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      - name: Update events data
        run: python scripts/update_events.py
      - name: Build HTML
        run: python scripts/build.py
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --cached --quiet || git commit -m "chore: update events [skip ci]"
          git push
```

**`.github/workflows/update-database.yml`** — 每周一更新图鉴：

```yaml
name: Update Database

on:
  schedule:
    - cron: '0 6 * * 1'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      - name: Update database
        run: python scripts/update_database.py
      - name: Build HTML
        run: python scripts/build.py
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --cached --quiet || git commit -m "chore: update database [skip ci]"
          git push
```

### 7.6 数据校验

```python
# scripts/validate_data.py
"""
每次数据更新后自动校验：
1. JSON格式正确
2. 必填字段完整
3. 日期格式正确
4. 无重复条目
5. URL可访问
6. 码字格式符合游戏规则
"""

import json
import re
from datetime import datetime

def validate_codes(data):
    errors = []
    seen_codes = set()

    for code in data.get('active', []):
        # 检查必填字段
        if not code.get('code'):
            errors.append(f"Missing code field")
        if not code.get('rewards'):
            errors.append(f"Missing rewards for {code['code']}")

        # 检查重复
        if code['code'] in seen_codes:
            errors.append(f"Duplicate code: {code['code']}")
        seen_codes.add(code['code'])

        # 检查日期格式
        if code.get('expiryDate'):
            try:
                datetime.strptime(code['expiryDate'], '%Y-%m-%d')
            except ValueError:
                errors.append(f"Invalid date format for {code['code']}")

    return errors
```

---

## 八、多语言策略

### 8.1 优先级

| 优先级 | 语言 | 代码 | 市场规模 | 理由 |
|---|---|---|---|---|
| P0 | 英语 | en | 最大 | 全球通用，搜索量最大 |
| P1 | 西班牙语 | es | 大 | 拉美+西班牙，手游市场增长快 |
| P1 | 葡萄牙语 | pt | 大 | 巴西市场巨大 |
| P2 | 日语 | ja | 中 | 日本游戏市场核心 |
| P2 | 韩语 | ko | 中 | 韩国游戏市场核心 |
| P2 | 德语 | de | 中 | 欧洲高价值市场 |
| P2 | 法语 | fr | 中 | 欧洲+非洲法语区 |
| P3 | 印尼语 | id | 中 | 东南亚增长最快 |
| P3 | 波兰语 | pl | 小 | 东欧游戏社区活跃 |
| P3 | 意大利语 | it | 小 | 欧洲补充 |

### 8.2 翻译规范

1. **不使用机器直译** — 使用AI翻译后人工校对关键页面
2. **本地化关键词** — 不是翻译关键词，而是用目标语言的搜索习惯
3. **hreflang标签** — 每个页面必须指向所有语言版本
4. **独立URL** — `/es/fish`, `/ja/fish` 而非查询参数
5. **渐进翻译** — 先翻译P0-P1页面，再扩展P2-P3

### 8.3 翻译自动化

```python
# scripts/translate.py
"""
翻译流程：
1. 读取英文源数据 (data/*.json)
2. 使用 Claude/GPT API 翻译
3. 人工校对关键术语
4. 输出到 data/{lang}/*.json
5. 构建对应语言的HTML
"""
```

---

## 九、性能规范

### 9.1 Core Web Vitals 目标

| 指标 | 目标 | 实现方式 |
|---|---|---|
| **LCP** | < 2.5s | 内联关键CSS、预加载字体、WebP图片 |
| **INP** | < 200ms | 最小化JS、无框架开销 |
| **CLS** | < 0.1 | 图片设定尺寸、字体预加载 |

### 9.2 性能优化清单

| 优化项 | 实现方式 |
|---|---|
| CSS | 内联关键CSS（< 14KB），非关键CSS异步加载 |
| JS | 仅交互逻辑，总计 < 50KB，全部defer |
| 图片 | WebP/AVIF格式，响应式srcset，lazy loading |
| 字体 | 预连接Google Fonts，font-display: swap |
| 缓存 | HTML短缓存（~1h），静态资源长缓存（~1y + 文件名哈希），`Cache-Control: public, max-age=31536000, immutable` |
| 压缩 | Cloudflare自动Brotli/Gzip |
| HTTP/2 | Cloudflare自动启用 |
| 预连接 | `<link rel="preconnect">` 外部资源 |

### 9.3 图片规范

```html
<!-- 正确的响应式图片（WebP + AVIF fallback） -->
<picture>
    <source srcset="/imgs/fish/golden-carp.avif" type="image/avif">
    <source srcset="/imgs/fish/golden-carp.webp" type="image/webp">
    <img src="/imgs/fish/golden-carp.webp"
         srcset="/imgs/fish/golden-carp-300.webp 300w,
                 /imgs/fish/golden-carp-600.webp 600w,
                 /imgs/fish/golden-carp-900.webp 900w"
         sizes="(max-width: 600px) 100vw, 600px"
         alt="Golden Carp fish in Heartopia - found in rivers during Spring"
         width="600" height="400"
         loading="lazy">
</picture>
```

> **图片格式选择**：优先提供 AVIF（压缩率比 WebP 小 20-30%），WebP 作为 fallback。Cloudflare Image Resizing 可自动按需转换格式。

### 9.4 无障碍（Accessibility）规范

Google 越来越重视页面无障碍性，且与 SEO 正相关。游戏攻略站面向全球玩家，应满足基本无障碍要求：

| 要求 | 说明 | 实现 |
|---|---|---|
| 键盘可操作 | 所有交互元素可通过键盘访问 | 使用原生 `<button>`/`<a>`，确保 `:focus-visible` 样式 |
| 表格语义化 | 数据表格正确关联表头 | `<th scope="col">` / `<th scope="row">` |
| 颜色对比度 | 正文与背景对比度 ≥ 4.5:1 | 使用 [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) 验证 |
| 跳过导航 | 提供跳转到主内容的链接 | `.skip-link { position: absolute; }` |
| 表单标签 | 所有表单控件有 `<label>` | `<label for="email">` + `<input id="email">` |
| 图片alt | 所有 `<img>` 有描述性 `alt` | `alt="Golden Carp in Heartopia"` |
| 页面语言 | 声明页面语言 | `<html lang="en">` |

---

## 十、上线检查清单

### 10.1 技术检查

- [ ] 所有页面HTML验证通过
- [ ] 所有页面有canonical URL
- [ ] sitemap.xml 包含所有页面
- [ ] robots.txt 配置正确
- [ ] llms.txt 存在且内容完整
- [ ] ads.txt 已放置
- [ ] HTTPS正常工作
- [ ] 404页面存在且有导航
- [ ] 移动端响应式正常
- [ ] Core Web Vitals全绿

### 10.2 SEO检查

- [ ] 每页有唯一Title
- [ ] 每页有Meta Description
- [ ] H1-H4层级正确
- [ ] JSON-LD结构化数据无错误
- [ ] 通过 [Google Rich Results Test](https://search.google.com/test/rich-results) 验证富片段
- [ ] 通过 [Schema Markup Validator](https://validator.schema.org/) 验证
- [ ] Open Graph标签完整
- [ ] Twitter Card标签完整
- [ ] hreflang标签正确（如有多语言）
- [ ] 内链结构完整
- [ ] 面包屑导航存在
- [ ] 图片都有alt属性

### 10.3 内容检查

- [ ] 至少30个高质量页面
- [ ] 无空白/占位页面
- [ ] FAQ区块存在
- [ ] 兑换码页面有效
- [ ] 无拼写错误
- [ ] 无翻译错误（多语言）
- [ ] 所有链接可访问
- [ ] 隐私政策/条款/关于页面存在

### 10.4 广告检查

- [ ] AdSense代码正确放置
- [ ] 广告密度不超过30%
- [ ] 移动端广告体验良好
- [ ] 广告不遮挡内容
- [ ] 无弹窗广告

---

## 附录A：新游戏攻略站启动流程

```
1. 调研游戏
   └── 确定游戏类型、核心玩法、目标用户

2. 确定模块
   └── 根据6.3节选择对应类型的模块

3. 搭建项目
   └── 复制模板目录结构
   └── 配置Cloudflare Pages
   └── 配置GitHub Actions

4. 填充内容
   └── 编写data/*.json数据文件
   └── 编写templates/*.j2模板
   └── 运行 build.py 生成HTML
   └── 手动补充攻略类页面内容

5. SEO配置
   └── 配置JSON-LD
   └── 生成sitemap.xml
   └── 编写llms.txt
   └── 配置robots.txt

6. 多语言
   └── 翻译P1语言的核心页面
   └── 配置hreflang

7. 部署上线
   └── 推送到main分支
   └── Cloudflare自动部署

8. 申请AdSense
   └── 确保30+页面
   └── 提交申请

9. 监控优化
   └── Google Search Console监控
   └── 根据搜索词优化内容
   └── 持续更新兑换码和活动
```

---

## 附录B：关键词研究模板

| 关键词 | 月搜索量 | 竞争度 | 对应页面 | 当前排名 | 目标排名 |
|---|---|---|---|---|---|
| game name codes | 10K-50K | 中 | /codes | - | Top 5 |
| game name fish guide | 5K-10K | 低 | /fish | - | Top 3 |
| game name beginner guide | 5K-10K | 中 | /beginner-guide | - | Top 10 |
| game name recipes | 1K-5K | 低 | /recipes | - | Top 3 |
| game name tier list | 10K-50K | 高 | /tier-list | - | Top 10 |

---

## 附录C：竞品参考站点

| 站点 | 游戏类型 | 特点 | 值得学习 |
|---|---|---|---|
| heartopia.gg | 生活模拟 | SEO极佳、多语言、llms.txt | 结构化数据、AI优化 |
| prydwen.gg | 二次元手游 | 角色数据库、tier list | 数据库交互设计 |
| game8.co | 综合 | 多游戏覆盖、日语优先 | 内容更新速度 |
| stardewvalleywiki.com | 生活模拟 | 社区驱动、MediaWiki | 数据完整性 |
| gameslantern.com | 开放世界 | Build系统、数据库 | 工具设计 |
| pokemongo.gamepress.gg | 手游 | 专业数据分析 | 数据驱动内容 |
