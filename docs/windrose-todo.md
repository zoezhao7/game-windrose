# Windrose 攻略站 — 纯静态 HTML 开发 TODO

> 基于 `windrose-dev-plan.md` | 纯静态 HTML | 无后端 | 所有内容直接从网络搜索写入

---

## 一、CSS 与基础样式（先完成，全站复用）

- [ ] **1.1** 创建 `css/style.css`
  - 移动优先（max-width: 860px 居中容器）
  - 系统字体栈（`-apple-system, BlinkMacSystemFont, 'Segoe UI'...`）
  - CSS 变量：`--bg`, `--text`, `--accent`, `--border`, `--card-bg`
  - 表格样式（`border-collapse`, `<caption>` 样式, `<th scope>` 区分, 斑马纹 `:nth-child(even)`）
  - 速查卡片（`.quick-stats` 水平排列 `display: flex; gap: 1rem; flex-wrap: wrap`）
  - FAQ `<details>` 展开动画、面包屑 `.breadcrumb`、Related Guides 侧边栏
  - 响应式断点：768px（平板）/ 480px（手机）
  - 导航：顶部固定栏 + 汉堡菜单（< 768px）
  - 打印样式 `@media print`（隐藏导航/广告）

- [ ] **1.2** 创建 `css/style.css` 中的通用类
  - `.container` 居中容器
  - `.card` 内容卡片（padding, border-radius, box-shadow）
  - `.btn` / `.btn-primary` 按钮样式
  - `.badge` 标签样式（稀有度标注）
  - `.table-responsive` 移动端横向滚动包装

- [ ] **1.3** 创建 `imgs/` 目录 + 放置占位图
  - `imgs/og.webp` — Open Graph 默认缩略图（1200x630，海盜船主题）
  - `imgs/logo.svg` — 站点 Logo（简单文字或图标）

---

## 二、首页 `index.html`（全站入口）

- [ ] **2.1** 编写完整 HTML 结构
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <!-- Title/Description/OG/Twitter/Robots/Canonical/JSON-LD -->
  </head>
  <body>
    <!-- Header含导航 -->
    <!-- Hero区 -->
    <!-- 快速导航卡片 -->
    <!-- 最新动态 -->
    <!-- Footer -->
  </body>
  </html>
  ```
- [ ] **2.2** 填充实际内容
  - **Title**: `Windrose Guides — Unofficial Wiki, Crafting Recipes & Boss Guides (2026)`
  - **Meta Description**: `Complete Windrose guide database: all workbench crafting recipes (Lv1-3), copper/iron/clay/gunpowder resource locations, boss strategies, ship guides, beginner tips. Updated 2026.`
  - **Hero 区**内容（直接从网络收集）：
    - 游戏名称 + 一句话定位："Your Ultimate Windrose Companion — All Crafting Recipes, Resource Locations & Boss Strategies in One Place"
    - 游戏简介：Kraken Express 开发，2026.4.14 发布 EA，海盗主题生存冒险，融合建造/制作/魂系战斗/海战，Steam 愿望单 #6，首周销量百万
    - 核心特色：3 个生态区（沿海丛林/丘陵/？）、30+ 岛屿、3 艘船、90+ 地下城、50-70h 主线
    - CTA：跳转新手指南、工作台配方、资源列表
  - **快速导航卡片**（8 个入口，每个带图标 + 描述 + 链接）：
    1. Beginner Guide → `/beginner-guide` — "Day 1 to Day 10 walkthrough"
    2. Workbench Recipes → `/crafting/workbench` — "All Lv1/Lv2/Lv3 recipes"
    3. Resource Locations → `/resources` — "Copper, Iron, Clay, Gunpowder & more"
    4. Boss Strategies → `/bosses` — "Beat Charon's Obols & others"
    5. Ship Building → `/ships` — "Sloop, Brigantine, Frigate guide"
    6. Weapons & Armor → `/weapons` — "Melee, Ranged, Armor tier list"
    7. FAQ → `/faq` — "Top 20 most asked questions"
    8. News & Updates → `/news` — "Latest patch notes & community news"
  - JSON-LD: `@graph` [WebSite, Organization, VideoGame]
    - **VideoGame**: name="Windrose", developer="Kraken Express", publisher="Kraken Express / Pocketpair Publishing", releaseDate="2026-04-14", playMode="SinglePlayer / CoOp / MultiPlayer", gamePlatform="PC", applicationCategory="Game", description=海盗生存冒险...

---

## 三、新手指南 `beginner-guide/index.html`

- [ ] **3.1** 创建目录 `beginner-guide/` + `index.html`
- [ ] **3.2** 填充内容（全部从网络搜索获取）：

  **3.2.1 难度选择**
  - Calm Waters — 降低敌人伤害和压力（新手首选）
  - High Seas — 100% 属性，标准体验（有生存游戏经验选此）
  - Storm's Edge — 敌人伤害/血量更高（挑战者）
  - Captain's Choice — 自定义滑块，最高 500%

  **3.2.2 开局生存（前 30 分钟）**
  - 砍树收集 5 个 Wood → 建造篝火 (Bonfire)
  - 用 5 个 Wood → 建造工作台 (Workbench)
  - 用 3 Wood + 3 Stone → 建造烹饪火 (Cooking Fire)
  - 用 4 Wood + 10 Plant Fiber → 建造帐篷 (Tent)
  - 击杀 Boar 获取 Rough Hide → 建造护甲工坊 (Armor Workshop，需要屋顶!)
  - 制作 Survivor's Boots (2 Rough Hide + 2 Coarse Fabric)

  **3.2.3 Island 任务推进**
  - 制作 Stone Pickaxe (3 Stone + 3 Wood) → 去洞穴挖 Poor Copper Ore
  - 建造 Charcoal Kiln (25 Wood + 20 Clay) → 1 Wood = 1 Charcoal
  - 建造 Smelting Furnace (15 Clay + 30 Stone) → 6 Copper Ore + 1 Charcoal = 1 Copper Ingot
  - 建造 Weaponsmith Workshop (10 Wood + 5 Copper Ingot, 需要屋顶!)
  - 制作近战武器 Saber/Rapier/Club
  - 完成后获得免费的第一艘船 + 解锁 "Rescuing the Crew" 和 "I Need a Bigger Boat" 任务

  **3.2.4 战斗基础**
  - 轻魂系战斗 (Soulslite) — 需要管理耐力 (Stamina)
  - 按 Ctrl 闪避，格挡招架
  - 打 1-2 下 → 后撤 → 敌人靠近 → 重击/冲刺攻击循环
  - 按 T 锁定敌人（设置里可开启自动锁定）
  - 死亡掉落物品（可跑尸捡回）
  - 敌人脱战不回血（可磨血战术）

  **3.2.5 基地建造**
  - 按 B 进入建造模式，Q 微调位置，V 切换俯视角
  - 几乎任何地点都可建造
  - 初期不要在固定地方建大本营，哪里资源多就在哪建临据点
  - 升级营地：在 Decoration 类别建不同子类物品可延长 Rested buff

  **3.2.6 新手必知技巧**
  - 背包扩容：制作 Torn Sailcloth Bag (2 Coarse Fabric + 1 Rope)
    - Coarse Fabric: 3 Plant Fiber → Workbench
    - Rope: 3 Plant Fiber → Workbench
  - 椰子是最佳早期食物（棕榈树采摘，补充水和饥饿）
  - 多备绷带 (Bandage): 1 Coarse Fabric → Workbench
  - 海滩捡 Shipwreck Debris → Wood + Nails
  - 右键点击蛤蜊外壳有机会出珍珠（紧急弹药）
  - 游戏没有暂停!! 开菜单/背包前确保周围安全
  - 按右键标记地图，勾选"Show on minimap"标记家/资源点

---

## 四、工作台配方 `crafting/workbench/index.html`

- [ ] **4.1** 创建目录 `crafting/workbench/` + `index.html`
- [ ] **4.2** 填充 Lv1 配方表格（全部从网络收集的数据）：

  | 名称 | 材料 |
  |:--|:--|
  | Stone Axe | 3 Stone + 3 Wood |
  | Stone Pickaxe | 3 Stone + 3 Wood |
  | Stone Bullet (x5) | 3 Stone |
  | Copper Axe | 5 Copper Ingot + 5 Wood |
  | Copper Pickaxe | 5 Copper Ingot + 5 Wood |
  | Copper Bullets (x5) | 1 Copper Ingot |
  | Copper Nails (x5) | 1 Copper Ingot |
  | Copper Pot | 5 Copper Ingot |
  | Shovel | 3 Copper Ingot + 10 Wood |
  | Empty Lamp | 4 Copper Ingot + 1 Rope |
  | Fast Travel Bell | 10 Copper Ingot + 3 Rope |
  | Bandage | 1 Coarse Fabric |
  | Clay Pot | 6 Clay |
  | Coarse Fabric | 3 Plant Fiber |
  | Combat Repair Kit | 3 Wooden Plank + 1 Rum Bottle + 1 Steel Nails |
  | Iron Nails (x10) | 1 Foothills Iron Ingot |
  | Repair Kit | 10 Wood |
  | Rope | 3 Plant Fiber |
  | Torn Sailcloth Bag | 2 Coarse Fabric + 1 Rope |

  **4.2.2 Lv2 配方表格：**

  | 名称 | 材料 |
  |:--|:--|
  | Anvil | 30 Foothills Iron Ingot |
  | Iron Axe | 5 Foothills Iron Ingot + 5 Wood |
  | Iron Pickaxe | 5 Foothills Iron Ingot + 5 Wood |
  | Iron Bullet (x5) | 1 Foothills Iron Ingot |
  | Ironware | 5 Foothills Iron Ingot |
  | Master Combat Repair Kit | 2 Timer + 5 Rum Bottle + 3 Steel Nails |
  | Sailor Backpack | 1 Torn Sailcloth Bag + 5 Rough Hide + 2 Copper Ingot |
  | Simple Fishing Rod | 5 Hardwood + 3 Rope + 2 Foothills Iron Ingot |
  | Wooden Plank | 2 Wood |

  **4.2.3 Lv3 配方表格：**

  | 名称 | 材料 |
  |:--|:--|
  | Bosun Backpack | 1 Sailor Backpack + 5 Tanned Leather + 2 Foothills Iron Ingot |
  | Timber | 3 Hardwood |

  **4.3** 配方页顶部说明文字：
  - "工作台是 Windrose 的工具和物品制作中心，共 3 个等级。升级需推进主线剧情。部分配方需探索解锁后才显示。"

  **4.4** FAQ `<details>` 区块：
  - Q: 如何升级工作台 Lv2？ → A: 推进主线剧情，到达 Foothills 区域后会解锁。
  - Q: 配方不显示怎么办？ → A: 需要先探索收集到对应材料或推进剧情。

---

## 五、锻造/冶炼页 `crafting/smelting/index.html`

- [ ] **5.1** 创建目录 `crafting/smelting/` + `index.html`
- [ ] **5.2** 填充内容：
  - 铜矿冶炼：6 Copper Ore + 1 Charcoal → 1 Copper Ingot (Smelting Furnace)
  - 铁矿冶炼：X Iron Ore + 1 Charcoal → 1 Foothills Iron Ingot (Smelting Furnace)
  - 前置建筑：Charcoal Kiln (25 Wood + 20 Clay) → 产 Charcoal
  - 前置建筑：Smelting Furnace (15 Clay + 30 Stone)
  - 说明文字：冶炼炉将矿石转化为金属锭，是所有金属工具和装备的必经之路

---

## 六、资源页（铜/铁/黏土/火药）

### 6.1 铜矿 `resources/copper/index.html`

- [ ] **6.1.1** 创建目录 + HTML
- [ ] **6.1.2** 填充内容（网络收集数据）：
  - 速查卡片：Rarity: ★★☆☆☆ | Tool: Stone Pickaxe | Found: Copper Deposit Mines (洞穴)
  - **如何获取**：地图上找小型十字镐图标 → 进入洞穴 → 用 Stone Pickaxe 挖掘 Poor Copper Ore → 带回 Smelting Furnace → 6 Ore + 1 Charcoal = 1 Copper Ingot
  - **注意事项**：洞穴内可能有 Drowned 敌人 → 带武器+绷带；洞穴黑暗 → 按 B 放火把照明
  - **铜的用途**：
    - 制作工具：Copper Pickaxe, Copper Axe, Shovel
    - 制作钉子 (Copper Nails) → 仓储配方
    - 制作 Fast Travel Bell (快速旅行铃铛)
    - 相关配方表格（从 Lv1 配方中筛选所有含 Copper Ingot 的）

### 6.2 铁矿石 `resources/iron/index.html`

- [ ] **6.2.1** 创建目录 + HTML
- [ ] **6.2.2** 填充内容：
  - 速查卡片：Rarity: ★★★☆☆ | Found: Foothills 区域 | Tool: Copper Pickaxe
  - **如何获取**：到达 Foothills (山麓) 区域 → 找到 Iron Ore 矿脉 → 用 Copper Pickaxe 挖掘 → 回 Smelting Furnace 冶炼成 Foothills Iron Ingot
  - **用途**：Lv2 工作台全部金属配方、Anvil、Iron Pickaxe/Axe、Iron Bullets、Sailor Backpack、修理包等

### 6.3 黏土 `resources/clay/index.html`

- [ ] **6.3.1** 创建目录 + HTML
- [ ] **6.3.2** 填充内容：
  - 速查卡片：Rarity: ★★☆☆☆ | Tool: Stone Pickaxe | Found: 水边/河岸
  - **如何获取**：地图随机生成，起始岛屿常见。深色大片泥土材质 → 用 Stone Pickaxe 挖掘
  - **用途**：
    - Clay Pot (6 Clay) — 炼金/烹饪
    - Clay Bottle — 制作炼金基底 (药水必备)
    - 高级建筑配方需要（扩展基地）
    - Charcoal Kiln (25 Wood + 20 Clay)
    - Smelting Furnace (15 Clay + 30 Stone)

### 6.4 火药 `resources/gunpowder/index.html`

- [ ] **6.4.1** 创建目录 + HTML
- [ ] **6.4.2** 填充内容：
  - **前期获取（推荐）**：
    - 沿海丛林第一个岛屿 → 走私者宝藏点 (Smuggler's Treasure) → 打破木堆 → 下楼梯 → 击败 Drowned → 右侧宝箱含 10 Gunpowder + 4 Rum Bottles
    - 黑胡子海盗营地 (Blackbeard Pirate Camp) — 清剿敌人掉火药 + 搜刮补给箱
    - 每个营地的地图图标下方有分数 (0/3) 表示宝箱进度
  - **后期制作**：
    - 需要到达 Foothills → 用 Iron Pickaxe 采集 Sulfur (硫磺)
    - 需要 Charcoal Kiln → 收集 Ash (灰烬)
    - 在 Millstone (磨盘) 中合成：10 Sulfur + 20 Ash = 10 Gunpowder
    - Millstone 需要 Iron Ore 制作
  - **使用**：火药 + 弹药自动进入 ammo 槽 → 配合枪支使用；弹药 Lv: Stone Bullet → Copper Bullet → Iron Bullet

---

## 七、资源总览页 `resources/index.html`

- [ ] **7.1** 创建目录 `resources/` + `index.html`
- [ ] **7.2** 分类列出所有资源，每个带缩略卡片 + 链接到详情页：
  - 金属类：Copper, Iron
  - 建材类：Clay, Wood, Stone, Hardwood
  - 消耗品类：Gunpowder, Charcoal, Plant Fiber, Rough Hide
  - 快速对照表：资源 → 获取工具 → 主要位置 → 用途概要

---

## 八、Boss 攻略

### 8.1 Boss 总览 `bosses/index.html`

- [ ] **8.1.1** 创建目录 + HTML
- [ ] **8.1.2** 填充已知 Boss 信息（网络搜索获取）：
  - **Charon's Obols** — 第三个 Boss，有独立攻略页面
  - **Blackbeard** — 主线最终目标之一
  - **新手 Boss** — B站/Bilibili 有实况视频，位于起始区域
  - 更多 Boss 等待网络资料补充

### 8.2 Charon's Obols `bosses/charons-obols/index.html`

- [ ] **8.2.1** 创建目录 + HTML
- [ ] **8.2.2** 填充内容（已有 MMOGAH 攻略数据 + Windrose Beginner Guide）：
  - 战斗准备建议
  - 阶段策略
  - 掉落奖励
  - 战后解锁内容
  - FAQ：常见问答

---

## 九、船只系统 `ships/`

### 9.1 船只总览 `ships/index.html`

- [ ] **9.1.1** 创建目录 + HTML
- [ ] **9.1.2** 填充三艘船的基础信息（网络搜索获取）：
  - **Sloop (双桅纵帆船)** — 灵活快速，适合单人侦察/小型海战
  - **Brigantine (双桅横帆船)** — 全能型，速度与火力均衡
  - **Frigate (大型护卫舰)** — 威猛重火，火力强大但速度最慢
  - 每艘船特性对比表格（速度/火力/装甲/操控性/载员）

### 9.2 Sloop `ships/sloop/index.html`
- [ ] **9.2.1** 创建目录 + HTML，详细参数 + 推荐配置 + 使用场景

### 9.3 Brigantine `ships/brigantine/index.html`
- [ ] **9.3.1** 创建目录 + HTML

### 9.4 Frigate `ships/frigate/index.html`
- [ ] **9.4.1** 创建目录 + HTML

- [ ] **9.5** 海战系统概览（放在总览页或独立区块）
  - 海战可远程炮火对轰 / 近距离登船肉搏
  - 多人模式：船员共同操控武器系统
  - 无缝"陆地—船只"切换

---

## 十、武器与装备 `weapons/`

- [ ] **10.1** 武器总览 `weapons/index.html`
  - 按近战 / 远程分类
  - Saber (弯刀), Rapier (细剑), Club (棍棒), Musket (火枪), Blunderbuss (霰弹枪), Spear (长矛), Halberd (戟) 等
  - 弹药等级：Stone Bullet → Copper Bullet → Iron Bullet

- [ ] **10.2** 近战武器 `weapons/melee/index.html`
- [ ] **10.3** 远程武器 `weapons/ranged/index.html`
- [ ] **10.4** 盔甲套装 `weapons/armor/index.html`

---

## 十一、Build 配置 `builds/`

- [ ] **11.1** Build 总览 `builds/index.html`
- [ ] **11.2** 新手 Build `builds/beginner-builds/index.html`
  - 属性加点建议、推荐武器组合、早期装备路线
- [ ] **11.3** DPS Build `builds/dps-builds/index.html`
- [ ] **11.4** 坦克 Build `builds/tank-builds/index.html`

---

## 十二、FAQ 页面 `faq/index.html`

- [ ] **12.1** 创建目录 + HTML
- [ ] **12.2** 填充 Top 15-20 FAQ（`<details>` + 加粗关键词标记）：
  1. Q: How do I get copper in Windrose?
  2. Q: How do I upgrade the Workbench to Level 2?
  3. Q: How do I get my first ship?
  4. Q: How do I fast travel?
     A: Craft a Fast Travel Bell at the Workbench (10 Copper Ingot + 3 Rope).
  5. Q: How do I get gunpowder early?
  6. Q: Where do I find clay?
  7. Q: How do I craft a bigger backpack?
  8. Q: What's the best difficulty for beginners?
  9. Q: Can I pause the game?
     A: No! Windrose has no pause. Always ensure your surroundings are safe before opening menus or inventory.
  10. Q: How do I heal?
      A: Craft Bandages at the Workbench (1 Coarse Fabric each). Use before you're at critical health.
  11. Q: How many players can play co-op?
      A: Up to 8 players in co-op mode.
  12. Q: What are pearls used for?
      A: Right-click scallop shells from beach enemies — pearls work as emergency ammo when gunpowder runs out.
  13. Q: How do I get more inventory space?
      A: Craft Torn Sailcloth Bag (2 Coarse Fabric + 1 Rope) → later upgrade to Sailor Backpack → Bosun Backpack.
  14. Q: Can I change difficulty mid-game?
      A: No, difficulty is locked when you create the world.
  15. Q: What happens when I die?
      A: You drop your items where you died. You can return to recover them. Enemies don't regenerate health.

---

## 十三、新闻页 `news/index.html`

- [ ] **13.1** 创建目录 + HTML
- [ ] **13.2** 手动录入最新几条新闻（从 Steam 新闻/Reddit 收集）：
  - 5月4日：Steam 云存档修复更新
  - 4月20日：工作台全配方指南（Mobalytics）
  - 4月14日：游戏正式发布 Early Access，首周销量破百万
  - 页面底部标注更新日期
- [ ] **13.3** 后续：如果内容多，拆分 `news/` 子目录 + 分页

---

## 十四、SEO / 合规页面

- [ ] **14.1** `privacy/index.html` — 隐私政策
- [ ] **14.2** `about/index.html` — 关于本站（社区维护，非官方，EA 阶段数据可能变化）
- [ ] **14.3** `contact/index.html` — 联系方式
- [ ] **14.4** `terms/index.html` — 服务条款
- [ ] **14.5** `404.html` — 自定义 404 页

---

## 十五、SEO 基础设施文件

- [ ] **15.1** `robots.txt` — 含 AI 爬虫白名单 (GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot 等) + Content-Signal
- [ ] **15.2** `llms.txt` — 含 About/Main Sections/Key Topics/Contact 完整格式，所有 URL 无 .html
- [ ] **15.3** `sitemap.xml` — 手动列出所有页面 URL（当前 MVP 约 30+ 页）
- [ ] **15.4** `ads.txt` — Google AdSense 占位

---

## 十六、JSON-LD 结构化数据检查

> 每页 `<head>` 中必须包含单一 `<script type="application/ld+json">` 内含 `@graph` 数组

- [ ] **16.1** 所有页面 `@graph` 必含项：
  ```json
  [WebSite(@id), Organization(@id), WebPage(url, name, dateModified, isPartOf, breadcrumb), BreadcrumbList(@id, itemListElement)]
  ```
- [ ] **16.2** 首页额外含 `VideoGame` Schema（name/developer/publisher/releaseDate/playMode/gamePlatform/description）
- [ ] **16.3** 数据页额外含 `Article`（headline/datePublished/dateModified/author）
- [ ] **16.4** FAQ 页额外含 `FAQPage`（mainEntity 数组含问答对）
- [ ] **16.5** `@id` 引用一致：`#website` / `#org` / `#breadcrumb` 跨页相同

---

## 十七、每页 SEO 检查

每创建一个页面，确保以下全部完成：
- [ ] Title 格式：`{核心关键词} (2026) | Windrose Guides`
- [ ] Meta Description：150-160 字符，含关键词 + 行动召唤
- [ ] `<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">`
- [ ] `<link rel="canonical" href="https://windrosewiki.games/...">` 无 .html
- [ ] OG 标签：og:type / og:url / og:title / og:description / og:image / og:site_name
- [ ] article:published_time / article:modified_time（数据页）
- [ ] Twitter Card：summary_large_image
- [ ] JSON-LD `@graph` 完整
- [ ] 页面 `<body>` 含：面包屑导航 + H1 + H2-H3 层级
- [ ] 数据表格含：`<caption>` + `<th scope="col">` / `<th scope="row">`
- [ ] FAQ `<details>` 区块（每个数据页底部 3-5 个问答）
- [ ] Related Guides 内链（底部关联页面链接）
- [ ] 所有 `<img>` 含 `alt` + `width`/`height`
- [ ] 移动端 375px / 768px 测试通过

---

## 📊 开发优先级

| 优先级 | 章节 | 页面数 | 说明 |
|:--|:--|:--:|:--|
| **P0 — 立刻** | 一、CSS基础 | — | 全站样式，所有页面依赖 |
| **P0 — 立刻** | 二、首页 | 1 | 入口 + VideoGame Schema |
| **P0 — 第一天** | 三、新手指南 | 1 | 新手最需要 |
| **P0 — 第一天** | 四、工作台配方 | 1 | 核心数据，SEO 吸引搜索量最大 |
| **P0 — 第一天** | 六、铜矿页 | 1 | 搜索量大 |
| **P1 — 第二天** | 五、冶炼页 | 1 | 跟铜矿互补 |
| **P1 — 第二天** | 六、铁/黏土/火药 | 3 | 全部核心资源 |
| **P1 — 第二天** | 七、资源总览 | 1 | 列表 Hub 页 |
| **P1 — 第三天** | 八、Boss攻略 | 2 | Charon's Obols + 总览 |
| **P1 — 第三天** | 九、船只系统 | 4 | 总览+3艘 |
| **P2 — 第四天** | 十、武器装备 | 4 | 总览+近战+远程+盔甲 |
| **P2 — 第四天** | 十二、FAQ | 1 | SEO 富片段 |
| **P2 — 第五天** | 十一、Build | 4 | 扩展内容 |
| **P2 — 第五天** | 十三、新闻 | 1 | 手动维护 |
| **P2 — 后续** | 十四、SEO页面 | 5 | 隐私/关于/联系/条款/404 |
| **P2 — 后续** | 十五、SEO文件 | 4 | robots/llms/sitemap/ads |
| **持续** | 十六+十七 | — | 每页 JSON-LD + SEO 检查 |

**当前估算总页面数**: ~35 个纯静态 HTML 页面

---

## 🔧 每页 HTML 模板骨架

新建任意页面的起始代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{页面Title} | Windrose Guides</title>
    <meta name="description" content="{150-160字符Description}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <link rel="canonical" href="https://windrosewiki.games/{slug}">
    <link rel="stylesheet" href="/css/style.css">

    <meta property="og:type" content="article">
    <meta property="og:url" content="https://windrosewiki.games/{slug}">
    <meta property="og:title" content="{og标题}">
    <meta property="og:description" content="{og描述}">
    <meta property="og:image" content="https://windrosewiki.games/imgs/og.webp">
    <meta property="og:site_name" content="Windrose Guides">
    <meta property="article:published_time" content="2026-05-12">
    <meta property="article:modified_time" content="2026-05-12">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{twitter标题}">
    <meta name="twitter:description" content="{twitter描述}">
    <meta name="twitter:image" content="https://windrosewiki.games/imgs/og.webp">

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@graph": [
            { "@type": "WebSite", "@id": "https://windrosewiki.games/#website", "url": "https://windrosewiki.games/", "name": "Windrose Guides", "publisher": { "@id": "https://windrosewiki.games/#org" } },
            { "@type": "Organization", "@id": "https://windrosewiki.games/#org", "name": "Windrose Guides", "url": "https://windrosewiki.games/" },
            { "@type": "WebPage", "@id": "https://windrosewiki.games/{slug}#webpage", "url": "https://windrosewiki.games/{slug}", "name": "{页面名}", "dateModified": "2026-05-12", "isPartOf": { "@id": "https://windrosewiki.games/#website" }, "breadcrumb": { "@id": "https://windrosewiki.games/#breadcrumb" } },
            { "@type": "BreadcrumbList", "@id": "https://windrosewiki.games/#breadcrumb", "itemListElement": [{面包屑}] }
        ]
    }
    </script>
</head>
<body>
    <nav aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/{parent}">{Parent}</a></li><li>{Page}</li></ol></nav>
    <main>
        <h1>{页面标题H1}</h1>
        <!-- 内容区 -->
        <section id="faq"><h2>FAQ</h2><details><summary>Q</summary><p>A</p></details></section>
    </main>
    <aside><h2>Related Guides</h2><ul><!-- 3-5个内链 --></ul></aside>
</body>
</html>
```