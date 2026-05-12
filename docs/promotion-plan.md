# Windrose Guides 上线推广方案

---

## 一、Google SEO 策略

### 1.1 提交与收录（上线当天）

| 事项 | 操作 | 工具 |
|------|------|------|
| 提交 sitemap | 将 `sitemap.xml` URL 提交到 Google | [Google Search Console](https://search.google.com/search-console) |
| 手动请求收录 | 首页 + 5 个核心 Hub 页逐个请求索引 | GSC URL Inspection |
| Bing 同步提交 | 同样提交到 Bing Webmaster Tools | [Bing Webmaster](https://www.bing.com/webmasters) |
| 验证 robots.txt | 确认未屏蔽关键目录 | GSC robots.txt Tester |

### 1.2 关键词策略

基于 Windrose 这款游戏的特点，按照**搜索意图**分层布局：

**第一层：高意图（用户立即需要答案）**

| 关键词（英文） | 对应页面 | 搜索量预估 |
|---|---|---|
| `Windrose beginner guide` | `/beginner-guide/` | 中高 |
| `Windrose crafting recipes` | `/crafting/` | 中高 |
| `Windrose copper location` | `/resources/copper/` | 中 |
| `Windrose boss guide` | `/bosses/` | 中高 |
| `Windrose best weapons` | `/weapons/` | 中 |
| `Windrose how to build ship` | `/ships/` | 中 |

**第二层：长尾关键词（蓝海机会）**

Windrose 是 2026 年新游戏，长尾关键词竞争很低，现在的窗口期至关重要：

- `Windrose best starter build`
- `Windrose Day 1 what to do first`
- `Windrose iron farming guide`
- `Windrose how to get gunpowder`
- `Windrose solo boss strategy`
- `Windrose all armor stats comparison`
- `Windrose frigate vs brigantine`
- `Windrose alchemy potion recipes`
- `Windrose faction reputation guide`
- `Windrose where to find rare materials`

**落地策略：** 每个长尾关键词确保有独立页面或页面锚点承载，标题（H1）中精确包含关键词，meta description 用自然语言写入。

### 1.3 内容优化清单

你目前 SEO 基础做得非常好（JSON-LD、OG、Canonical 齐全），但可以进一步强化：

- **每个子页面添加 FAQ 模块**（你已经在 FAQ 页面做了 Top 20，把对应问题也嵌入到相关子页面底部，如 copper 页底部加 "Where to find copper fast?"），每个子页面都带上 `FAQPage` Schema，争取 Google "People Also Ask" 富片段
- **为 Boss 页面添加 `VideoObject` Schema**（如果后续嵌入打法视频）
- **添加 `Speakable` Schema** 适配 Google Assistant 语音搜索
- **BreadcrumbList 已在大部分页面落地**，检查是否每个子页面都有

### 1.4 外链建设（Backlinks）

游戏攻略站最有效的白帽外链策略：

| 渠道 | 具体操作 | 链接类型 |
|------|----------|----------|
| **Steam 社区** | 在 Windrose Steam 社区中心的 "Guides" 板块发布攻略 | dofollow (Steam 攻略权重极高) |
| **Reddit** | 在 r/WindroseGame 等子版块发布攻略链接 | nofollow 但引流强 |
| **GameFAQs** | 提交攻略到 GameFAQs Windrose 页面 | dofollow |
| **Fandom/Wiki** | 在 Windrose Fandom Wiki 的 External Links 区域添加 | dofollow |
| **GitHub** | 如果开源了数据脚本，README 加链接 | dofollow |
| **YouTube 描述** | 如果做视频，描述区放链接 | nofollow 但引流 |

### 1.5 AI 搜索优化

你已经有 `llms.txt` 和 robots.txt 的 AI 爬虫白名单，这是非常好的前瞻布局。补充：

- 每页 `<meta name="description">` 保持 150-160 字符，清晰概括页面内容（AI 引用描述的概率很高）
- 保持结构化数据准确，AI Overview 引用时偏好 Schema 标记过的内容
- `llms.txt` 定期更新，确保涵盖所有新增页面

---

## 二、社区/论坛/博客推广

### 2.1 渠道优先级矩阵

按**投入产出比**排序：

| 优先级 | 平台 | 推广形式 | 预估效果 |
|--------|------|----------|----------|
| P0 | Steam 社区中心 | 发布完整攻略 + 链接 | 极高（精准用户，Steam 权重高） |
| P0 | Reddit | 攻略帖子 + 问答互动 | 极高（病毒传播潜力） |
| P1 | Discord | Windrose 官方/社区服 | 高（核心玩家聚集） |
| P1 | GameFAQs | 提交攻略文档 | 高（SEO 外链 + 历史留存） |
| P2 | YouTube | 视频攻略 + 描述链 | 高但制作成本大 |
| P2 | 博客/Medium | 深度分析文章 | 中（SEO 外链） |
| P3 | TikTok/Twitter | 短视频引流 | 中（需要持续运营） |
| P3 | 游戏论坛（IGN/GameSpot） | 评论区互动 | 低但零成本 |

### 2.2 Steam 社区中心 — 核心战场

**这是最重要的渠道**，因为 Windrose 刚发售，Steam 社区中心流量巨大：

**方案 A：发布 Steam 攻略（Guide）**

1. 将你的 `/beginner-guide/` 内容改写为一篇 **"Windrose Complete Beginner Guide: Day 1 to Day 10"** 的 Steam 攻略
2. 攻略末尾加一句：*"For more detailed guides including boss strategies, item locations, and build recommendations, check out the full wiki at https://windrose-guides.pages.dev"*
3. 再单独发布每个 Boss 的攻略
4. Steam 攻略会被 Google 索引，且通常排名靠前

**方案 B：Steam 论坛互动**

- 在 Windrose Steam 论坛的 "General Discussions" 中回答玩家问题
- 回答时自然引用你的网站链接："I wrote a detailed guide about this here: [link]"
- **注意频率**：每回答 10 个问题引用 1-2 次链接，避免被判定 spam

### 2.3 Reddit — 引流利器

**目标子版块：**
- `r/WindroseGame`（如果有）
- `r/Windrose`（如果有）
- `r/pcgaming`
- `r/SurvivalGaming`
- `r/PirateGames`
- `r/GameGuides`

**内容策略：**

| 内容类型 | 标题示例 | 发布频率 |
|----------|----------|----------|
| 完整攻略帖 | "I made a complete Windrose Crafting Recipe Database with all materials" | 每月 2 篇 |
| 数据可视化 | "Windrose Ship Comparison: Sloop vs Brigantine vs Frigate — full stats breakdown" | 每月 1 篇 |
| 问答互动 | 搜索 "Windrose" + "help" / "how to"，回答问题并附链接 | 每日 15 分钟 |
| 新闻同步 | 游戏更新时发帖总结变化 | 跟随更新 |

**Reddit 关键注意事项：**
- 遵循每个子版块的自推规则（通常 10:1 比例，即 10 条普通互动对应 1 条自推内容）
- 不要只发链接，正文要提供足够价值，让用户即使不点链接也觉得有用
- 使用 Reddit 自带图片/视频功能增强帖子可见性

### 2.4 Discord — 建立品牌认知

1. 加入 Windrose 官方 Discord（如果有）和主要的玩家社区 Discord
2. 在 `#guides` 或 `#resources` 频道分享你的网站
3. 把链接放在你的 Discord 个人资料签名中
4. 创建你自己网站的 Discord 服务器，作为读者社区聚集地（后期）

### 2.5 GameFAQs — 长期流量

GameFAQs 是游戏攻略的老牌站点，Google 权重极高：
1. 为 Windrose 游戏页面提交 FAQ/攻略文档
2. 文档中可以包含你的网站链接
3. GameFAQs 贡献者系统会给你信用，长期积累

### 2.6 博客/Medium/Dev.to

| 平台 | 内容方向 |
|------|----------|
| Medium | "How I Built a Complete Game Wiki with Pure HTML and Zero Frameworks"（技术类，吸引开发者关注） |
| Dev.to | 同上，偏技术实现 |
| 个人博客 | 游戏深度分析、数据挖掘文章 |

这类内容不直接带量，但能建立领域权威性，对 SEO 和品牌都有长期帮助。

---

## 三、内容日历（前 30 天）

| 天数 | 行动 |
|------|------|
| Day 1 | 提交 sitemap 到 GSC + Bing；Steam 发布第一篇新手攻略 Guide |
| Day 3 | Reddit 发布第一篇数据帖（如配方数据库介绍）；加入 5 个 Windrose 相关 Discord |
| Day 5 | 在 Steam 论坛开始回答问题（每日 3-5 个） |
| Day 7 | 发布第二篇 Steam Guide（Boss 攻略合集） |
| Day 10 | Reddit 发布第二篇帖子；GameFAQs 提交攻略 |
| Day 15 | 检查 GSC 数据，调整关键词策略；在相关子版块持续互动 |
| Day 20 | 考虑做一期 YouTube 视频攻略 |
| Day 30 | 首次月度数据复盘：GSC 点击量、外链数、Reddit 引流数据 |

---

## 四、监控与迭代

| 指标 | 工具 | 目标（30天） |
|------|------|-------------|
| Google 收录页面数 | GSC Coverage Report | 全部 39 个页面收录 |
| 日均自然搜索点击 | GSC Performance | 50-200（新站正常） |
| 核心关键词排名 | GSC / Ahrefs | 前 20 名 |
| 外链域名数 | GSC / Ahrefs | 5-10 个唯一域名 |
| Reddit 引流 | Cloudflare Analytics | 追踪 |

---

## 五、总结

你的网站技术基础和 SEO 架构已经远超大多数个人攻略站的水平。现在的核心策略是：

1. **Steam 社区是主战场** — 把攻略搬运过去，建立第一波权威外链
2. **Reddit 是流量放大器** — 高质量帖子能带来爆发式访问
3. **长尾关键词窗口期不能错过** — Windrose 是新游戏，现在布局长尾词，3 个月后就是你的护城河
4. **坚持 30 天** — 新站冷启动靠持续输出，前 30 天的社区活跃度决定了后续增速