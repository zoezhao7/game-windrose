# Windrose 攻略站开发方案

> 方案版本：v1.0
> 日期：2026-05-12
> 站点暂定域名：[windrose-guides.com] / [windrose.wiki]
> 技术路线：纯静态 HTML + 极简 JS + Python 数据驱动生成

---

## 一、游戏数据基线

| 属性 | 值 |
|------|-----|
| 开发商 | Kraken Express |
| 发行商 | Kraken Express / Pocketpair Publishing (日本) |
| 发售日 | 2026-04-14 (Early Access) |
| EA 持续时间 | 预计 1.5 - 2.5 年 |
| 售价 | $30 USD / ¥205 |
| Steam Wishlist | 150万+ |
| Demo 下载 | 85万+ |
| 通关时长 | 50-70 小时 |
| 联机 | 1-4 人 Co-op（计划扩展至 8 人） |
| 完整版新增 | 约 50% 内容 (更多生物群系、Boss、船只、故事) |
| 下次大更新 | 灰烬之地 (Ashlands)，至少 6 个月后 |
| 当前版本 | v0.10.0.5.120 (2026-05-04) |

### 已确认的核心系统

```
工作台 Lv1-3     → 制作配方（工具/武器/盔甲/建材）
冶炼炉           → 矿石 → 锭（铜/铁/...）
炼金台           → 药水基底 / 药水制作
建筑系统         → 自由建造（海上/陆地）
船只系统         → 双桅纵帆船 / 双桅横帆船 / 大型护卫舰
   ├── 海战      → 远程炮击 + 接舷近战
   ├── 船员      → 雇佣 NPC 船员
   └── 船歌      → Sea Shanties
战斗系统         → Soulslite（攻/防/闪/耐力管理）
派系系统         → 派系任务 / 声望 / NPC 工人
角色成长         → 属性 + 天赋树 + 装备系统
```

### 已确认的资源

| 资源 | 获取方式 | 用途 |
|------|----------|------|
| 木材 / 石头 | 基础采集 | 初级工具、建筑 |
| 铜矿 | 铜矿洞穴（Cross镐图标），冶炼 | 铜锭 → 铜工具/钉子/仓储 |
| 铁 | 后期矿点 | 高级装备 |
| 黏土 | 随机生成(水边)，石镐采集 | 罐子/瓶子/药剂基底/高级建材 |
| 硫磺 | 矿点 | 火药相关 |
| 火药 | 走私者藏匿点 / 海盗营地掉落 | 枪支弹药 |
| 盐 / 土壤 | 野外采集 | 多种配方 |

### 已确认的 Boss

- 多个 Boss（Charon's Obols 为第三 Boss）
- 以真实历史人物为原型 + 超自然力量
- Soulslite 式战斗 = 攻略需求高

---

## 二、网站总体架构

### 2.1 页面结构树

```
windrose-guides.com/
├── index.html                        # 首页 — 快速导航 + 最新动态
├── beginner-guide/
│   └── index.html                    # 新手指南 — 第一天到第十天
├── crafting/                         # 制作配方数据库
│   ├── index.html                    # 全部配方总览（分类筛选）
│   ├── workbench/
│   │   └── index.html                # 工作台 Lv1/2/3 配方
│   ├── smelting/
│   │   └── index.html                # 冶炼配方
│   ├── alchemy/
│   │   └── index.html                # 炼金/药水配方
│   ├── cooking/
│   │   └── index.html                # 烹饪配方
│   └── building/
│       └── index.html                # 建筑材料配方
├── resources/                        # 资源位置指南
│   ├── index.html                    # 全部资源总览
│   ├── copper/
│   │   └── index.html                # 铜矿获取指南
│   ├── iron/
│   │   └── index.html                # 铁矿获取指南
│   ├── clay/
│   │   └── index.html                # 黏土获取指南
│   ├── gunpowder/
│   │   └── index.html                # 火药获取指南
│   └── rare-materials/
│       └── index.html                # 稀有材料
├── bosses/                           # Boss 攻略
│   ├── index.html                    # 全 Boss 总览
│   ├── boss-01/
│   │   └── index.html                # Boss 1
│   ├── boss-02/
│   │   └── index.html                # Boss 2
│   ├── charons-obols/
│   │   └── index.html                # Charon's Obols (第三Boss)
│   └── ...
├── ships/                            # 船只与海战
│   ├── index.html                    # 船只总览
│   ├── sloop/
│   │   └── index.html                # 双桅纵帆船
│   ├── brigantine/
│   │   └── index.html                # 双桅横帆船
│   └── frigate/
│       └── index.html                # 大型护卫舰
├── weapons/                          # 武器与装备
│   ├── index.html                    # 武器总览（Tier List）
│   ├── melee/
│   │   └── index.html                # 近战武器
│   ├── ranged/
│   │   └── index.html                # 远程武器
│   └── armor/
│       └── index.html                # 盔甲套装
├── builds/                           # Build 配置推荐
│   ├── index.html                    # Build 总览
│   ├── beginner-builds/
│   │   └── index.html                # 新手 Build
│   ├── dps-builds/
│   │   └── index.html                # 输出 Build
│   └── tank-builds/
│       └── index.html                # 坦克 Build
├── building/                         # 基地建造
│   ├── index.html                    # 建造入门
│   ├── layout-ideas/
│   │   └── index.html                # 布局设计灵感
│   └── defense/
│       └── index.html                # 防御工事
├── news/                             # 最新动态
│   └── index.html                    # 新闻 / 更新日志列表
├── faq/
│   └── index.html                    # 常见问题
├── privacy/
│   └── index.html                    # 隐私政策（AdSense必须）
├── about/
│   └── index.html                    # 关于站点（AdSense必须）
├── contact/
│   └── index.html                    # 联系方式（AdSense必须）
├── terms/
│   └── index.html                    # 服务条款
├── 404.html                          # 404错误页面
├── ads.txt                           # Google AdSense授权
├── llms.txt                          # AI 搜索引擎友好文件
├── sitemap.xml                       # 站点地图
└── robots.txt                        # 爬虫规则
```

> **URL 策略**：采用目录方案（每个页面一个目录 + `index.html`），Cloudflare Pages 自动映射 `/crafting/workbench` → `crafting/workbench/index.html`。对外 URL 无 `.html` 后缀，简洁专业，且方便未来换技术栈时 URL 不变。

### 2.2 URL 设计原则

```
✅ 正确：     /crafting/workbench.html
✅ 正确：     /resources/copper.html
✅ 正确：     /bosses/charons-obols.html
❌ 避免：     /page?id=123
❌ 避免：     /crafting.php?type=workbench
❌ 避免：     /2026/05/12/copper-guide/
```

规则：**纯静态 .html 文件 + 语义化目录 + 短 URL 路径。**

---

## 三、数据模型设计

### 3.1 配方数据模型 (recipes.json)

```json
{
  "recipes": [
    {
      "id": "stone-pickaxe",
      "name": "Stone Pickaxe",
      "category": "tool",
      "station": "workbench",
      "station_level": 1,
      "materials": [
        { "item": "Stone", "quantity": 3 },
        { "item": "Wood", "quantity": 3 }
      ],
      "result": { "item": "Stone Pickaxe", "quantity": 1 },
      "unlock_condition": "Default",
      "tips": "Your first mining tool. Required to mine Clay, Copper, Iron."
    }
  ]
}
```

### 3.2 资源数据模型 (resources.json)

```json
{
  "resources": [
    {
      "id": "copper-ore",
      "name": "Copper Ore",
      "rarity": "common",
      "biome": ["coastal-jungle"],
      "source": "Copper Deposit Mines (cave icon on map)",
      "tool_required": "Stone Pickaxe or better",
      "refined_to": "Copper Ingot (Smelting Furnace)",
      "used_in": ["copper-pickaxe", "copper-axe", "nails", "storage-recipes"],
      "tips": "Bring torches and weapons. Drowned enemies may lurk inside caves."
    }
  ]
}
```

### 3.3 Boss 数据模型 (bosses.json)

```json
{
  "bosses": [
    {
      "id": "charons-obols",
      "name": "Charon's Obols",
      "order": 3,
      "location": "待确认",
      "recommended_level": "待确认",
      "phases": [
        {
          "phase": 1,
          "attacks": [],
          "strategy": ""
        }
      ],
      "drops": [],
      "preparation": [],
      "tips": ""
    }
  ]
}
```

---

## 四、页面 Wireframe（一页到底式设计）

以「资源页面」为例，所有数据页采用统一的 Schema 结构：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Copper Ore - Windrose Guide | How to Get & Use Copper</title>
    <meta name="description" content="...">
    
    <!-- Schema.org 结构化数据 (Article) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Windrose Copper Guide",
      "datePublished": "2026-05-12",
      "dateModified": "2026-05-12"
    }
    </script>
    
    <!-- Schema.org 结构化数据 (ItemList - 配方页) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "numberOfItems": 3,
      "itemListElement": [...]
    }
    </script>

    <!-- Schema.org 结构化数据 (FAQ - 常见问题页) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [...]
    }
    </script>

    <link rel="canonical" href="https://windrose-guides.com/resources/copper.html">
</head>
<body>
    <!-- 面包屑 -->
    <nav aria-label="Breadcrumb">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/resources/">Resources</a></li>
        <li>Copper Ore</li>
      </ol>
    </nav>

    <!-- H1 -->
    <h1>Windrose Copper Ore Guide: Where to Find & How to Use</h1>

    <!-- 速查卡片 -->
    <div class="quick-stats">
      <div>Rarity: ★★☆☆☆</div>
      <div>Biome: Coastal Jungle</div>
      <div>Tool: Stone Pickaxe</div>
    </div>

    <!-- 正文 -->
    <article>
      <h2>Where to Find Copper Ore</h2>
      <p>...</p>

      <h2>How to Mine Copper</h2>
      <p>...</p>

      <h2>How to Smelt into Copper Ingots</h2>
      <table>...</table>

      <h2>All Recipes Using Copper</h2>
      <table>
        <tr><td>Copper Pickaxe</td><td>...</td></tr>
        <tr><td>Nails</td><td>...</td></tr>
      </table>

      <h2>Tips & Tricks</h2>
      <ul><li>...</li></ul>
    </article>

    <!-- 关联内容 -->
    <aside>
      <h2>Related Guides</h2>
      <ul>
        <li><a href="/resources/clay.html">Clay Guide</a></li>
        <li><a href="/crafting/workbench.html">Workbench Recipes</a></li>
      </ul>
    </aside>
</body>
</html>
```

### 设计规范

| 规则 | 说明 |
|------|------|
| **无框架** | 不使用 React/Vue/Svelte。纯手写 HTML + 内联 CSS（或单一 style.css） |
| **无外部依赖** | 无 jQuery、无 Bootstrap CDN（避免渲染阻塞） |
| **Zero JS（数据页）** | 数据页不包含 JS。首页只需极少量 JS 做搜索过滤 |
| **语义化 HTML5** | `<article>`, `<section>`, `<nav>`, `<aside>`, `<table>` |
| **H1-H3 层级清晰** | H1=页面唯一标题, H2=大段, H3=子段 |
| **面包屑** | 每个页面必有 schema.org BreadcrumbList |
| **Table 展示数据** | 配方/资源/Boss 全部用 `<table>`，方便爬虫解析 |
| **Canonical URL** | 每页 `<link rel="canonical">` 防止重复内容 |

---

## 五、SEO & AI 搜索引擎友好策略

### 5.1 对 Google 友好

| 策略 | 实现方式 |
|------|----------|
| Title 含主关键词 + 年份 | `<title>Windrose Copper Guide: Mining Locations & Recipes (2026) | Windrose Guides</title>` |
| Meta Description 独特 | 每页手写，150-160字符，含关键词 + 行动召唤 |
| Open Graph | 每页 og:title/description/image/type + article:published_time/modified_time |
| Twitter Card | summary_large_image，与 OG 共用图片 |
| Robots Meta | `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` |
| JSON-LD（单一 @graph） | WebSite + Organization + WebPage + BreadcrumbList + 页面专属 Schema |
| Sitemap.xml | 自动生成，按页面类型分级 priority + lastmod |
| Robots.txt | 允许所有爬虫 + 显式允许 AI 爬虫 + Content-Signal 标签 |
| 内链网络 | 每个页面有 "Related Guides" 区块 + 上下文内链 + 面包屑 |
| 图片 Alt 文本 | `<img alt="Windrose Copper Deposit Mine cave icon on map" width="..." height="...">` |
| 移动端适配 | `viewport` meta + 移动优先响应式 CSS |
| Core Web Vitals | 纯静态 HTML，0 JS 阻塞，目标 LCP < 2.5s / INP < 200ms / CLS < 0.1 |

### 5.1.1 内链策略

| 链接类型 | 说明 | 示例 |
|---|---|---|
| **Hub→子页** | 列表页链接到每个详情页 | `/resources` 链接到 `/resources/copper` |
| **子页→Hub** | 详情页链接回所属列表页 | 铜矿页链接回 `/resources` |
| **上下文内链** | 正文中自然引用相关页面 | 配方页提到铜矿 → 链接到铜矿资源页 |
| **Related Guides** | 页面底部推荐相关页面 | 铜矿页推荐黏土、铁矿指南 |
| **面包屑** | 每页显示层级导航 | Home > Resources > Copper Ore |

### 5.2 对 AI 搜索引擎友好 (llms.txt)

根目录创建 **`/llms.txt`**：

```markdown
# Windrose Guides

> Unofficial Windrose guide website — crafting recipes, resource locations, boss strategies, and ship guides. Game by Kraken Express.

## About This Site

Windrose Guides is a community-maintained database and wiki covering all aspects of the survival RPG Windrose. Data is collected from gameplay, official patch notes, and community contributions. Updated regularly as new content is released during Early Access.

## Main Sections

### [Getting Started](https://windrose-guides.com/beginner-guide)
- [Beginner Guide](https://windrose-guides.com/beginner-guide): Day 1 to Day 10 walkthrough, first tools, base building basics

### [Crafting Recipes](https://windrose-guides.com/crafting)
- [Workbench Lv1-3](https://windrose-guides.com/crafting/workbench): Tools, weapons, armor, building materials
- [Smelting](https://windrose-guides.com/crafting/smelting): Ore to ingot recipes
- [Alchemy](https://windrose-guides.com/crafting/alchemy): Potions and alchemy recipes
- [Cooking](https://windrose-guides.com/crafting/cooking): Food and cooking recipes
- [Building Materials](https://windrose-guides.com/crafting/building): Construction recipes

### [Resources](https://windrose-guides.com/resources)
- [Copper Ore](https://windrose-guides.com/resources/copper): Mining locations, smelting, and copper recipes
- [Iron Ore](https://windrose-guides.com/resources/iron): Iron mining locations and usage
- [Clay](https://windrose-guides.com/resources/clay): Clay gathering spots and recipes

### [Bosses](https://windrose-guides.com/bosses)
- [Charon's Obols](https://windrose-guides.com/bosses/charons-obols): Phase-by-phase strategy, drops, preparation tips

### [Ships](https://windrose-guides.com/ships)
- [Sloop](https://windrose-guides.com/ships/sloop): Small ship stats and sailing tips
- [Brigantine](https://windrose-guides.com/ships/brigantine): Mid-size ship guide
- [Frigate](https://windrose-guides.com/ships/frigate): Large warship guide

### [Weapons & Builds](https://windrose-guides.com/weapons)
- [Melee Weapons](https://windrose-guides.com/weapons/melee): Sword, axe, and melee weapon stats
- [Ranged Weapons](https://windrose-guides.com/weapons/ranged): Guns and ranged weapon stats
- [Armor Sets](https://windrose-guides.com/weapons/armor): Complete armor set list
- [Builds](https://windrose-guides.com/builds): DPS, tank, and beginner builds

### [FAQs](https://windrose-guides.com/faq)
- [Frequently Asked Questions](https://windrose-guides.com/faq): Common questions about gameplay, progress, and systems

### [News](https://windrose-guides.com/news)
- [Latest Updates](https://windrose-guides.com/news): Game updates, patch notes, and community news

## Key Topics

- Copper mining locations in Coastal Jungle biome
- Smelting ore into ingots for advanced crafting
- Soulslite combat system with stamina management
- Ship building and naval combat mechanics
- Boss strategies for Charon's Obols and others
- Build recommendations for DPS, tank, and beginner playstyles

## Contact

- Website: https://windrose-guides.com
```

### 5.3 Robots.txt & AI 爬虫配置

```txt
# 搜索引擎
User-agent: *
Allow: /
Disallow: /scripts/
Disallow: /data/
Disallow: /templates/

# AI爬虫 - 允许并引导到llms.txt
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: GoogleOther
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

# 内容信号
Content-Signal: search=yes,ai-train=no

Sitemap: https://windrose-guides.com/sitemap.xml
```

### 5.4 Schema 类型覆盖

| 页面类型 | Schema Type | 说明 |
|----------|-------------|------|
| 首页 | WebSite + VideoGame | 站点元数据 + 游戏信息（开发商/评分/平台） |
| 数据页（资源/配方/Boss） | Article | 攻略文章 |
| 配方总览页 | ItemList | 配方列表 |
| FAQ 页 | FAQPage | 常见问题富片段 |
| 所有页面 | WebSite + Organization + WebPage + BreadcrumbList | 通过 `@graph` 合并为单个 JSON-LD |
| HowTo 页面 | HowTo | 逐步教程 |

---

## 六、性能目标与规范

### 6.1 Core Web Vitals 目标

| 指标 | 目标 | 实现方式 |
|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | 纯静态 HTML，无 JS/CSS 阻塞 |
| **INP** (Interaction to Next Paint) | < 200ms | 数据页 Zero JS，交互页仅极简 JS |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 图片设定 width/height，字体 font-display: swap |

### 6.2 图片优化规范

```html
<picture>
    <source srcset="/imgs/resources/copper-deposit.avif" type="image/avif">
    <source srcset="/imgs/resources/copper-deposit.webp" type="image/webp">
    <img src="/imgs/resources/copper-deposit.webp"
         srcset="/imgs/resources/copper-deposit-600.webp 600w,
                 /imgs/resources/copper-deposit-900.webp 900w"
         sizes="(max-width: 600px) 100vw, 600px"
         alt="Windrose Copper Deposit Mine cave icon on map"
         width="900" height="600"
         loading="lazy">
</picture>
```

### 6.3 无障碍（Accessibility）要求

| 要求 | 说明 | 实现 |
|---|---|---|
| 键盘可操作 | 交互元素可通过键盘访问 | 使用原生 `<button>`/`<a>`，`:focus-visible` 样式 |
| 表格语义化 | 表头正确关联 | `<th scope="col">` / `<th scope="row">` |
| 颜色对比度 | 正文 ≥ 4.5:1 | 深色正文 (#333) + 白色背景 |
| 图片 alt | 所有 `<img>` 有描述性 alt | ✅ 已在规范中要求 |

### 6.4 缓存策略

| 资源类型 | 缓存策略 |
|---|---|
| HTML 页面 | 短缓存 ~15min（Cloudflare Pages 默认） |
| CSS/JS | 长缓存 1年 + 文件名哈希 |
| 图片 | 长缓存 1年 + `immutable` |

---

## 七、数据来源汇总

### 7.1 各模块数据来源

| 模块 | 数据来源 | 获取方式 | 可靠性 |
|------|----------|----------|:------:|
| **制作配方** | 游戏内实测 + Fandom Wiki + ProGameGuides/Mobalytics | 手动录入 + 脚本抓取 | ⭐⭐⭐ |
| **资源位置** | Reddit r/Windrose + 游戏实测 + Dot Esports 攻略 | 手动汇总 | ⭐⭐⭐ |
| **Boss 攻略** | 游戏实测 + YouTube 视频解析 + MmoGah 攻略 | 手动撰写 + 视频参考 | ⭐⭐⭐⭐ |
| **Build 配置** | Reddit 社区 + YouTube 创作者 + 自研分析 | 社区采集 + 实测 | ⭐⭐⭐ |
| **武器数据** | 游戏内数据挖掘 + Fandom Wiki | 手动录入 | ⭐⭐⭐⭐ |
| **船只数据** | 游戏内实测 + 官方文档 | 手动录入 | ⭐⭐⭐⭐⭐ |
| **更新日志** | Steam 官方公告 + Kraken Express 社交媒体 | 脚本自动抓取 | ⭐⭐⭐⭐⭐ |
| **最新动态** | GameSpot / EscapistMagazine / Reddit / Twitter | 脚本自动抓取 | ⭐⭐⭐⭐ |

### 7.2 数据源 URL 清单

```python
DATA_SOURCES = {
    "steam_news": "https://store.steampowered.com/news/app/<appid>",
    "steam_discussions": "https://steamcommunity.com/app/<appid>/discussions/",
    "reddit": "https://www.reddit.com/r/Windrose/",
    "escabit_mag": "https://www.escapistmagazine.com/",
    "gamespot": "https://www.gamespot.com/",
    "mmogah": "https://www.mmogah.com/",
    "youtube_guides": "https://www.youtube.com/results?search_query=windrose+guide",
    "twitch": "https://www.twitch.tv/directory/category/windrose",
    "steamdb": "https://steamdb.info/app/<appid>/",
}
```

---

## 八、更新策略 & 自动化脚本

### 8.1 模块更新频率与方案

| 模块 | 更新频率 | 更新方式 | 数据源 |
|------|:--------:|----------|--------|
| 新闻/更新日志 | **每日** | 脚本自动抓取 → 生成 HTML | Steam API + RSS |
| 首页「最新动态」 | **每日** | 脚本更新 | 新闻模块联动 |
| 制作配方 | **每版本** | 手动验证 + 脚本生成 HTML | 游戏实测 |
| 资源位置 | **每版本** | 手动验证 + 脚本生成 HTML | 社区 + 实测 |
| Boss 攻略 | **新Boss时** | 手动撰写 | 实测 + 视频 |
| Build 配置 | **每版本** | 手动撰写 + 社区调研 | Reddit/YT |
| 武器/装备 | **每版本** | JSON 数据 → 脚本生成 HTML | 数据挖掘 |
| FAQ | **不定期** | 手动追加 | 社区问题 |
| Sitemap | **每次内容更新后** | 脚本自动生成 | 扫描 HTML 文件 |
| llms.txt | **新增页面时** | 手动更新 | — |

### 8.2 一级更新（全自动）

#### 8.2.1 脚本架构

```
scripts/
├── requirements.txt           # Python 依赖
├── config.py                  # 配置文件（数据源URL、路径）
├── fetch_news.py              # 抓取 Steam/GameSpot/Reddit 新闻
├── generate_html.py           # 从 JSON 数据库生成 HTML 页面
├── generate_sitemap.py        # 自动生成 sitemap.xml
├── deploy.py                  # 一键部署（可选）
├── data/
│   ├── recipes.json           # 配方数据库
│   ├── resources.json         # 资源数据库
│   ├── bosses.json            # Boss 数据库
│   ├── weapons.json           # 武器数据库
│   ├── ships.json             # 船只数据库
│   └── news.json              # 新闻缓存
├── templates/
│   ├── base.html              # 基础 HTML 模板
│   ├── recipe-table.html      # 配方表格组件
│   ├── resource-page.html     # 资源页模板
│   ├── boss-page.html         # Boss 页模板
│   └── news-item.html         # 新闻条目组件
└── output/                    # 生成的 HTML 输出（可直接部署）
```

#### 8.2.2 核心脚本设计

**fetch_news.py** — 每日自动抓取新闻：

```python
"""
每天运行一次，抓取 Windrose 相关新闻。
可配置为：
  - 本地手动运行:    python fetch_news.py
  - GitHub Actions:  每日 UTC 0:00 自动运行
  - 服务器 cron:     0 0 * * * cd /path && python fetch_news.py
"""
import requests
import json
import re
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
NEWS_FILE = DATA_DIR / "news.json"
OUTPUT_DIR = Path(__file__).parent.parent / "news"

STEAM_APP_ID = "待确认"  # Windrose Steam App ID

def fetch_steam_news():
    """从 Steam API 抓取官方新闻"""
    url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/"
    params = {
        "appid": STEAM_APP_ID,
        "count": 20,
        "maxlength": 500,
        "format": "json"
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    items = []
    for item in data.get("appnews", {}).get("newsitems", []):
        items.append({
            "source": "steam",
            "title": item["title"],
            "url": item["url"],
            "date": datetime.fromtimestamp(item["date"]).isoformat(),
            "summary": item["contents"][:200]
        })
    return items

def fetch_escapist_news():
    """从 Escapist Magazine 抓取 Windrose 相关文章"""
    # 简单 RSS 或 HTML 解析
    url = "https://www.escapistmagazine.com/"
    resp = requests.get(url)
    # 正则提取包含 "Windrose" 的链接
    pattern = r'href="([^"]*)"[^>]*>([^<]*Windrose[^<]*)</a>'
    matches = re.findall(pattern, resp.text)
    return [
        {"source": "escapist", "title": m[1], "url": m[0],
         "date": datetime.now().isoformat()}
        for m in matches
    ]

def fetch_reddit_hot():
    """从 Reddit API 抓取热帖（无需 API Key 的 JSON 端点）"""
    url = "https://www.reddit.com/r/Windrose/hot.json?limit=15"
    headers = {"User-Agent": "WindroseGuidesBot/1.0"}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    items = []
    for post in data.get("data", {}).get("children", []):
        p = post["data"]
        items.append({
            "source": "reddit",
            "title": p["title"],
            "url": f"https://reddit.com{p['permalink']}",
            "date": datetime.fromtimestamp(p["created_utc"]).isoformat(),
            "score": p["score"],
            "comments": p["num_comments"]
        })
    return items

def merge_and_deduplicate(existing, new_items):
    """合并新闻，去重，按日期排序"""
    seen_urls = {item["url"] for item in existing}
    for item in new_items:
        if item["url"] not in seen_urls:
            existing.append(item)
            seen_urls.add(item["url"])
    existing.sort(key=lambda x: x["date"], reverse=True)
    return existing[:50]  # 只保留最近50条

def generate_news_html(news_items):
    """根据新闻 JSON 生成 news/index.html"""
    with open("templates/news-page.html", "r", encoding="utf-8") as f:
        template = f.read()
    
    news_html = ""
    with open("templates/news-item.html", "r", encoding="utf-8") as f:
        item_template = f.read()
    
    for item in news_items:
        news_html += item_template.format(
            title=item["title"],
            url=item["url"],
            source=item["source"],
            date=item["date"][:10],
            summary=item.get("summary", "")
        )
    
    output = template.replace("{{NEWS_ITEMS}}", news_html)
    output = output.replace("{{LAST_UPDATED}}", datetime.now().strftime("%Y-%m-%d"))
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(output)

def main():
    existing = []
    if NEWS_FILE.exists():
        existing = json.loads(NEWS_FILE.read_text(encoding="utf-8"))
    
    new_items = []
    new_items.extend(fetch_steam_news())
    new_items.extend(fetch_escapist_news())
    new_items.extend(fetch_reddit_hot())
    
    merged = merge_and_deduplicate(existing, new_items)
    NEWS_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    
    generate_news_html(merged)
    print(f"[{datetime.now()}] Updated: {len(new_items)} new items, "
          f"total {len(merged)}")

if __name__ == "__main__":
    main()
```

**generate_html.py** — 从 JSON 数据库生成所有 HTML 页面：

```python
"""
每次手动更新 JSON 数据库后运行一次，重新生成所有数据页面。
用法：python generate_html.py
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
TEMPLATE_DIR = Path(__file__).parent / "templates"
OUTPUT_BASE = Path(__file__).parent.parent  # 网站根目录

def load_template(name):
    path = TEMPLATE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")

def generate_crafting_pages():
    """从 recipes.json 生成所有配方页面"""
    recipes = json.loads((DATA_DIR / "recipes.json").read_text(encoding="utf-8"))
    page_template = load_template("recipe-page.html")
    
    # 按工作台分组
    stations = {}
    for r in recipes["recipes"]:
        key = f"{r['station']}-lv{r.get('station_level', 1)}"
        stations.setdefault(key, []).append(r)
    
    # 生成每个工作台页面
    for station_key, station_recipes in stations.items():
        table_rows = ""
        for r in station_recipes:
            materials = ", ".join(
                f"{m['quantity']}x {m['item']}" for m in r["materials"]
            )
            table_rows += f"""
            <tr>
                <td>{r['name']}</td>
                <td>{materials}</td>
                <td>{r['result']['quantity']}x {r['result']['item']}</td>
            </tr>"""
        
        page = page_template.replace("{{TABLE_ROWS}}", table_rows)
        page = page.replace("{{STATION_NAME}}", station_key.replace("-", " ").title())
        page = page.replace("{{LAST_UPDATED}}", datetime.now().strftime("%Y-%m-%d"))
        
        out_path = OUTPUT_BASE / "crafting" / f"{station_key}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page, encoding="utf-8")
        print(f"  Generated: {out_path}")

def generate_resource_pages():
    """从 resources.json 生成每个资源页面"""
    resources = json.loads((DATA_DIR / "resources.json").read_text(encoding="utf-8"))
    page_template = load_template("resource-page.html")
    
    for resource in resources["resources"]:
        page = page_template
        page = page.replace("{{RESOURCE_NAME}}", resource["name"])
        page = page.replace("{{RARITY}}", resource["rarity"])
        page = page.replace("{{BIOME}}", ", ".join(resource.get("biome", [])))
        page = page.replace("{{SOURCE}}", resource["source"])
        page = page.replace("{{TOOL_REQUIRED}}", resource.get("tool_required", "None"))
        page = page.replace("{{REFINED_TO}}", resource.get("refined_to", "—"))
        page = page.replace("{{USED_IN}}", ", ".join(resource.get("used_in", [])))
        page = page.replace("{{TIPS}}", resource.get("tips", ""))
        page = page.replace("{{LAST_UPDATED}}", datetime.now().strftime("%Y-%m-%d"))
        
        slug = resource["id"]
        out_path = OUTPUT_BASE / "resources" / f"{slug}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page, encoding="utf-8")
        print(f"  Generated: {out_path}")

def generate_sitemap():
    """扫描所有 HTML 文件生成 sitemap.xml"""
    urls = []
    base_url = "https://windrose-guides.com"
    
    for html_file in OUTPUT_BASE.rglob("*.html"):
        relative = html_file.relative_to(OUTPUT_BASE)
        # lastmod 用文件修改时间
        lastmod = datetime.fromtimestamp(html_file.stat().st_mtime).strftime("%Y-%m-%d")
        url_path = str(relative).replace("\\", "/")
        urls.append(f"""  <url>
    <loc>{base_url}/{url_path}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    
    (OUTPUT_BASE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  Generated: sitemap.xml ({len(urls)} URLs)")

if __name__ == "__main__":
    print("Generating crafting pages...")
    generate_crafting_pages()
    print("Generating resource pages...")
    generate_resource_pages()
    print("Generating sitemap...")
    generate_sitemap()
    print("Done!")
```

#### 8.2.3 自动化执行方案

```
方案 A（推荐 — GitHub Actions，免费）
  触发：每天 UTC 00:00 / 每次 push / 手动触发
  步骤：
    1. checkout 仓库
    2. pip install -r scripts/requirements.txt
    3. python scripts/fetch_news.py          # 抓取新闻
    4. python scripts/generate_html.py       # 重新生成页面
    5. python scripts/generate_sitemap.py    # 更新 sitemap
    6. git commit & push                     # 提交变更
    7. (可选) deploy 到 Vercel/Cloudflare Pages

  优点：完全免费，自动生成 + 自动部署

方案 B（本地 Python 脚本）
  适合：纯手动管理
  频率：每周手动运行 1-2 次
  命令：
    python scripts/fetch_news.py
    python scripts/generate_html.py
    # 手动 FTP 上传到服务器

方案 C（Linux 服务器 cron）
  适合：有 VPS 的情况
  crontab：
    0 2 * * * cd /var/www/windrose && python scripts/fetch_news.py
    0 3 * * 1 cd /var/www/windrose && python scripts/generate_html.py
```

### 8.3 二级更新（手动 + 脚本辅助）

| 模块 | 工作流 |
|------|--------|
| **配方数据库** | 1. 游戏版本更新 → 2. 手动验证新/改配方 → 3. 修改 `recipes.json` → 4. 运行 `generate_html.py` |
| **资源位置** | 1. 社区发现新资源/新位置 → 2. 验证 → 3. 修改 `resources.json` → 4. 运行生成脚本 |
| **Boss 攻略** | 1. 新 Boss 出现 → 2. 手动撰写 Markdown → 3. 脚本转为 HTML → 4. 推送 |
| **Build 配置** | 1. 元环境变化 → 2. Reddit/YT 调研 → 3. 手动撰写 → 4. 推送 |

---

## 九、首期内容上线计划（MVP）

### Phase 1 — 上线前（第 1-2 周）

| 序号 | 内容 | 优先级 |
|:----:|------|:------:|
| 1 | HTML 模板搭建（base + 各组件） | P0 |
| 2 | 首页 + 导航结构 | P0 |
| 3 | **新手指南**（Beginner Guide） | P0 |
| 4 | **工作台 Lv1 全配方表** | P0 |
| 5 | **核心资源页**（铜/铁/黏土/火药） | P0 |
| 6 | 冶炼配方表 | P1 |
| 7 | FAQ 页面 | P1 |
| 8 | llms.txt | P1 |
| 9 | sitemap.xml + robots.txt | P1 |
| 10 | 脚本基础设施（fetch_news + generate_html） | P0 |

### Phase 2 — 上线后第 1 个月

| 序号 | 内容 |
|:----:|------|
| 1 | 工作台 Lv2/Lv3 配方 |
| 2 | 全部 Boss 攻略（至少 3 个） |
| 3 | 船只指南（Sloop + Brigantine + Frigate） |
| 4 | 武器 Tier List |
| 5 | 基地建造指南 |
| 6 | 炼金药水配方 |
| 7 | 新闻页面上线 + 每日自动更新 |

### Phase 3 — 第 2-3 个月

| 序号 | 内容 |
|:----:|------|
| 1 | Build 配置区（新手/DPS/坦克） |
| 2 | 烹饪配方 |
| 3 | 稀有材料指南 |
| 4 | 建筑布局灵感集 |
| 5 | 交互式地图（Leaflet.js，需要时可加JS） |

---

## 十、开发规范清单

### 10.1 文件命名规范

```
✅ 使用小写 + 连字符：   beginner-guide/ (目录方案)
✅ 短而描述性：          copper/  (不是 how-to-get-copper-in-windrose/)
✅ 目录式组织：          resources/copper/index.html
❌ 禁止：               beginner_guide / BeginnerGuide
❌ 禁止：               copper.html (对外URL不暴露.html)
```

### 10.2 HTML 编码规范

```
✅ <!DOCTYPE html> 在第一行
✅ <html lang="en">
✅ <meta charset="UTF-8"> 在 head 最前面
✅ <meta name="viewport" content="width=device-width, initial-scale=1.0">
✅ 所有 img 标签有 alt 属性
✅ 所有 a 标签有描述性锚文本（不写 "click here"）
✅ table 使用 thead/tbody
✅ 不使用 <br> 做间距（用 CSS margin）
✅ 不写行内 style（统一在 style.css）
```

### 10.3 CSS 规范

```css
/* 不使用任何 CSS 框架 */
/* 单一 style.css，总量 < 15KB */
/* 移动优先的响应式设计 */
/* 仅使用 CSS Grid + Flexbox */
/* 字体使用系统默认字体栈（无外部字体加载） */

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    max-width: 860px;
    margin: 0 auto;
    padding: 1rem;
}
```

---

## 十一、域名与托管建议

| 选项 | 域名 | 托管 |
|------|------|------|
| **推荐** | windrose.wiki / windrose-guides.com | Cloudflare Pages（免费，全球CDN） |
| 备选 | windrose.gg | GitHub Pages（免费）+ Cloudflare DNS |
| 备选 | roseguides.net | Vercel（免费100GB/月） |

---

> **下一步**：确认方案后，我将开始编写 HTML 模板、CSS、JSON 数据结构、Python 脚本，以及首批 10 个页面。