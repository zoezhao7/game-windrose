# 数据采集经验记录

本文档用于记录 Windrose Guides 在采集数据过程中积累的经验：哪些数据源适合采集哪些类型的数据、可信度如何、有哪些注意事项。后续每次采集新数据或发现新来源，都应该更新本文档。

## 数据源分级

| 可信度 | 数据源类型 | 使用方式 |
|---|---|---|
| `official` | Steam、官网、官方公告、官方 dedicated server guide | 可作为页面核心事实来源 |
| `verified` | 自己实测、截图、可重复复现的游戏内数据 | 可进入正式数据表和详情页 |
| `community` | Wiki、攻略站、视频、Reddit、Discord、Steam 社区 | 可采集，但需要交叉验证 |
| `unconfirmed` | 单一来源、版本不明、无实测 | 只放 tracker 或 notes，不创建薄详情页 |
| `outdated` | 旧版本内容、补丁前数据 | 需标注版本或移除 |

## 已确认有价值的数据源

### Steam 商店页

| 项目 | 说明 |
|---|---|
| URL | `https://store.steampowered.com/app/3041230/Windrose/` |
| 适合采集 | 游戏名称、发售日期、开发商、发行商、类型、平台、Steam 功能、语言、Early Access 范围、官方描述 |
| 不适合采集 | 具体 Boss 掉落、配方数值、资源刷新点 |
| 可信度 | `official` |
| 用途 | `/download/`、首页 VideoGame Schema、About、Sources、News |
| 注意事项 | Steam 页面会随版本调整，推广前应重新核对发售日期、EA 描述和功能列表 |

### 官方 Windrose Dedicated Server Guide

| 项目 | 说明 |
|---|---|
| URL | `https://playwindrose.com/dedicated-server-guide/` |
| 适合采集 | SteamCMD app id、服务器安装流程、Windows-only 状态、UPnP/NAT punch-through、服务器配置项、防火墙注意事项 |
| 不适合采集 | 游戏玩法数据、Boss、配方、资源位置 |
| 可信度 | `official` |
| 用途 | `/server-guide/`、FAQ、News |
| 注意事项 | 服务器文档可能随版本变动。涉及命令、端口、配置字段时必须重新核对官方页面 |

### 官方 Steam 新闻 / 公告

| 项目 | 说明 |
|---|---|
| URL | Steam App 新闻页或 Steam 社区公告 |
| 适合采集 | 补丁日期、版本更新、服务器/云存档/平衡调整、官方事件 |
| 不适合采集 | 详细数据库条目，除非公告明确列出 |
| 可信度 | `official` |
| 用途 | `/news/`、受影响页面的更新时间、版本说明 |
| 注意事项 | 不要全文复制公告，应该写原创摘要和“对攻略页的影响” |

### 官方网站 / 开发者网站

| 项目 | 说明 |
|---|---|
| URL | `https://playwindrose.com/` 及其子页面 |
| 适合采集 | 官方指南、服务器说明、游戏定位、开发团队信息、支持链接 |
| 不适合采集 | 未列出的隐藏数据、社区猜测 |
| 可信度 | `official` |
| 用途 | Sources、About、Server Guide、Download |
| 注意事项 | 官网路径可能变化，引用时尽量记录访问日期 |

### 社区 Wiki / 数据库站

| 项目 | 说明 |
|---|---|
| 适合采集 | Boss 名称、资源名称、配方条目、掉落、NPC、区域信息 |
| 不适合采集 | 未标版本的数据直接进入正式表 |
| 可信度 | `community` |
| 用途 | `data/bosses.json`、`data/recipes.json`、`data/resources.json` 的初稿 |
| 注意事项 | 必须交叉验证。若只有一个社区来源，字段标为 `unconfirmed` 或 `community`，并在 notes 写明风险 |

#### Windrose Wiki: game.wiki

| 项目 | 说明 |
|---|---|
| URL | `https://game.wiki/windrose/` |
| 本轮使用页面 | `https://game.wiki/windrose/bosses`、`https://game.wiki/windrose/workbench` |
| 适合采集 | Boss roster、Biome、推荐等级、前置任务、Workbench recipe 表、comfort 解锁要求 |
| 不适合采集 | 需要版本精确验证的掉落概率、路线细节、战斗阶段机制 |
| 可信度 | `community` |
| 本轮结论 | Boss 列表和 Workbench 表格结构化程度较高，适合作为 `data/bosses.json` 和 `data/recipes.json` 的第一版种子数据 |
| 注意事项 | 与其他 Wiki/攻略站存在命名差异。例如现有站点曾把 `Charon's Obols` 当 Boss 页，但 game.wiki 更像把 `Charon's Obol` 作为奖励/物品处理，需要实测确认 |

#### The Games Wiki

| 项目 | 说明 |
|---|---|
| URL | `https://thegameswiki.com/windrose/wiki/bosses` |
| 适合采集 | Boss 详情补充、推荐等级、掉落、解锁区域、optional encounter 线索 |
| 不适合采集 | 单独作为最终事实来源 |
| 可信度 | `community` |
| 本轮结论 | 对 `Thomas Richards`、`Israel Hands`、`High Priestess`、`Ghost Captain` 提供了比总览更细的描述，适合补 tracker 和 notes |
| 注意事项 | 与 game.wiki 需要交叉核对；未实测前掉落和 optional boss 分类保持 `community` 或 `unconfirmed` |

### 攻略站 / 博客文章

| 项目 | 说明 |
|---|---|
| 适合采集 | 新手路线、Boss 策略、资源获取方法、Build 思路、工具/配方列表 |
| 不适合采集 | 直接复制长段攻略正文 |
| 可信度 | `community` |
| 用途 | Beginner Guide、Boss 页面、Build 页面、Resources 页面 |
| 注意事项 | 只能提炼事实和策略结构，页面正文必须重新组织；来源放入 `sources` 字段 |

#### Mobalytics / GameSpot

| 项目 | 说明 |
|---|---|
| URL | `https://mobalytics.gg/news/guides/how-to-upgrade-workbench-windrose`、`https://www.gamespot.com/articles/how-to-upgrade-workbench-levels-in-windrose/1100-6539435/` |
| 适合采集 | Workbench 升级流程、Sawhorse、Toolbox、comfort 等机制说明 |
| 不适合采集 | 完整配方数据库替代、Boss 详情 |
| 可信度 | `community` |
| 本轮结论 | 两者适合作为 Workbench upgrade 机制的交叉验证来源，已用于 `data/recipes.json` 中 Sawhorse / Toolbox 相关记录 |
| 注意事项 | 站点内容可能是攻略摘要，具体材料仍应回到游戏内或 Wiki 表格验证 |

#### PC Gamer

| 项目 | 说明 |
|---|---|
| URL | `https://www.pcgamer.com/games/survival-crafting/windrose-gunpowder/`、`https://www.pcgamer.com/games/survival-crafting/windrose-clay/` |
| 适合采集 | 资源获取路线、资源解锁前置、实用提示、资源用途 |
| 不适合采集 | 完整资源数据库、精确刷新机制 |
| 可信度 | `community` |
| 本轮结论 | Gunpowder 页面质量高，提供了 `10 Sulfur + 20 Ash`、Millstone、Foothills、Sulfur/Ash 获取关系；Clay 页面适合补充 clay 获取位置和用途 |
| 注意事项 | 资源路线类信息受版本影响较大，应在数据中保留 `community` 可信度并后续实测 |

### YouTube / 视频攻略

| 项目 | 说明 |
|---|---|
| 适合采集 | Boss 阶段、地图路线、资源点位置、战斗动作、实际掉落截图 |
| 不适合采集 | 难以确认的数值、没有展示的结论 |
| 可信度 | `community` 或 `verified`，取决于是否能从画面复核 |
| 用途 | Boss 详情、资源路线、Build 实战说明 |
| 注意事项 | 记录视频 URL、发布时间、时间戳；不要只凭标题采信 |

### Reddit / Discord / Steam 讨论区

| 项目 | 说明 |
|---|---|
| 适合采集 | 玩家常见问题、Bug、版本变化反馈、隐藏机制线索 |
| 不适合采集 | 直接当作最终事实 |
| 可信度 | `community` 或 `unconfirmed` |
| 用途 | FAQ、News 线索、待验证列表 |
| 注意事项 | 适合作为“发现线索”，不适合作为单一事实来源 |

### 自己实测 / 游戏内截图

| 项目 | 说明 |
|---|---|
| 适合采集 | 配方材料、资源点、Boss 掉落、UI 文案、数值、截图 |
| 不适合采集 | 单次随机掉落推断固定概率 |
| 可信度 | `verified` |
| 用途 | 所有正式数据文件 |
| 注意事项 | 记录游戏版本、日期、截图路径、是否可复现 |

## 按数据类型推荐来源

| 数据类型 | 首选来源 | 辅助来源 | 备注 |
|---|---|---|---|
| 游戏基础信息 | Steam 商店页 | 官网 | 用于首页、Download、Schema |
| Dedicated Server | 官方 server guide | Steam 讨论区 | 命令和 app id 必须用官方来源 |
| 新闻/补丁 | Steam 新闻 | 官网、社区 | 写原创摘要，不复制全文 |
| Boss 列表 | Wiki/攻略站/视频 | 玩家讨论、实测 | 先做 tracker，不确定不建详情页 |
| Boss 机制 | 视频攻略、实测 | 攻略站 | 时间戳和截图很重要 |
| Boss 掉落 | 实测 | Wiki/攻略站 | 未验证掉落标 `unconfirmed` |
| 配方 | 实测 | Wiki/攻略站 | 最适合进入 `data/recipes.json` |
| 资源位置 | 实测、视频 | Wiki/Reddit | 位置类信息版本风险高 |
| 船只 | Steam/官网概述、实测 | 攻略站 | 当前适合先做定位和选择器 |
| 武器装备 | 实测 | Wiki/攻略站 | Tier List 必须标版本 |
| Build | 实测、视频 | Reddit/攻略站 | Build 是建议，不应写成唯一答案 |
| FAQ | Reddit/Steam 讨论区 | 站内搜索词、用户反馈 | 适合持续更新 |

## 本轮采集记录：2026-05-12

| 模块 | 已更新文件 | 主要来源 | 结果 |
|---|---|---|---|
| Boss | `data/bosses.json` | game.wiki、The Games Wiki | 从迁移快照扩展为 5 条：Thomas Richards、Israel Hands、High Priestess、Ghost Captain、Charon's Obols Legacy Page |
| Recipes | `data/recipes.json` | game.wiki Workbench、Mobalytics、GameSpot | 清洗为 37 条结构化配方，补充 Workbench comfort / Sawhorse / Toolbox 机制 |
| Resources | `data/resources.json` | PC Gamer、Windrose Wiki、Mobalytics | 扩展为 6 条：Clay、Gunpowder、Sulfur、Ash、Copper Ore、Foothills Iron Ore |
| Sources | `data/sources.json` | 本轮所有来源 | 扩展为 8 条来源记录 |

本轮重要发现：

- Boss 数据存在命名/分类冲突，尤其是 `Charon's Obols`。现阶段应保留为 `needs_verification` 的 legacy page，不应继续强化为已确认 Boss。
- `game.wiki/windrose/workbench` 适合作为 Workbench recipe 第一版结构化数据源。
- PC Gamer 对 Gunpowder 和 Clay 的实用路线价值较高，适合补资源页和 FAQ。
- Boss 掉落、推荐等级、optional boss 分类必须后续实测或找视频交叉验证。

## 采集记录格式建议

每次采集新来源，建议在对应 `data/*.json` 的 `sources` 字段记录：

```json
{
  "title": "Windrose Dedicated Server Guide",
  "url": "https://playwindrose.com/dedicated-server-guide/",
  "type": "official",
  "accessed": "2026-05-12"
}
```

如果来源只提供线索，建议在 `notes` 写明：

```text
Only one community source found. Needs in-game verification before creating a detail page.
```

## 当前经验结论

- 第一阶段可以用官方 Steam、官网、服务器文档、已有项目资料搭起可信框架。
- 第二阶段需要按模块多次采集，不要一次性追求完整。
- Boss、掉落、配方、资源点是最需要实测或多来源交叉验证的数据。
- 资料不足时，优先做 Tracker 和 Notes，不要创建低质量详情页。
- 所有采集经验都应持续补充到本文档，避免下一轮重复踩坑。

## 第二轮采集经验（2026-05-12）

### 关键修正

| 修正项 | 原始错误 | 正确数据 | 来源 |
|---|---|---|---|
| Tier 1 船名 | Sloop | **Ketch** | Fextralife Wiki, community `verified` |
| 船只变体系统 | 无（只有单一船型） | 每种船 3 个变体：Stock / Brethren / Blackbeard | Fextralife Wiki `community` |
| Co-op 最大人数 | 8 | **10**（推荐 2-4） | 官方 FAQ, Steam `official` |
| Respec 费用 | 未知 | **免费** | 多个社区来源 `community` |
| 食物 buff 叠加 | 未提及 | **最多同时 2 个** | YouTube 攻略, Reddit `community` |
| Parry 机制名称 | Parry | **Perfect Block** | 社区 Wiki `community` |

### 新发现的有价值数据源

- **patchbot.io**: 追踪 Windrose 所有补丁的时间线和 changelog 链接，适合 News 页面更新
- **steamdb.info**: 可查看精确的版本号、更新时间线、下载量趋势
- **windrose.support**: 官方 bug tracker 和反馈平台，适合追踪已知问题

### 船只数据注意事项

- 船只 HP/速度数据来自 Fextralife Wiki，标记为 `community`
- 蓝图解锁条件（Reputation Level、Piastre 价格）来自多个社区来源交叉验证
- Wharf 系统（码头造船）来自 YouTube 演示视频
- 变体之间的 cannon capacity / cargo capacity 差异需要实测确认

### Ashlands 路线图

- 来源：开发者 YouTube 采访 + TechPowerUp 报道
- 开发者明确表示：至少 6 个月后推出首个大型内容更新
- 开发者确认：不计划进行 save/server wipe
- 可信度：`official`（基于开发者直接陈述）

### 补丁数据采集流程

1. 优先查 patchbot.io 或 steamdb.info 获取版本号和发布时间
2. 在 Steam Community News 查看完整 changelog
3. 交叉验证 YouTube 内容创作者的补丁解读视频
4. 只在 News 页面写「Guide Impact」摘要，不复制完整 patch notes
