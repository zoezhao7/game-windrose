# Windrose Wiki 推广日常执行手册

> 站点：windrosewiki.games（已上线，6 语言，已接 IndexNow）
> 目标：把"推广方案"落到每天可勾的动作上，并明确哪些必须人工、哪些可以让 Claude Code + Playwright / API 自动或半自动完成。

## 图例

| 标记 | 含义 |
|---|---|
| 🧑 **人工** | 必须真人操作。涉及账号登录、平台反 bot、社区氛围判断、版规风险 |
| 🤖 **可自动** | Claude Code 通过本地脚本 / API / Playwright 可独立完成 |
| 🤝 **半自动** | Claude 生成内容 / 数据 / 草稿，人工最终发布 |

> 自动化红线：Reddit / Steam / Discord 用脚本发帖一旦被识别就是封号 + 域名拉黑级别风险。所以"发帖、评论、点赞"这类**社交动作一律 🧑**。Claude 的价值在**生产内容、抓数据、做监控、改稿、本地化**。

---

## 每日动作（合计 30–45 分钟）

### 早 15 分钟 — Reddit 巡查

| 子动作 | 标记 | 说明 |
|---|---|---|
| 抓取过去 24h 各 sub 内 "Windrose" 关键词新帖 | 🤖 | 用 Reddit JSON API（`https://www.reddit.com/r/<sub>/search.json?q=Windrose&sort=new&restrict_sr=1`），无需登录。Claude 每天早上跑一次脚本，按"含问号 / how to / where / stuck"过滤，输出候选清单 |
| 起草每个候选帖的回答 | 🤝 | Claude 读站内对应页面 → 给出 200–400 字回答 + 是否带链接的建议（遵守 10:1） |
| 实际登录 Reddit 发回答 | 🧑 | 必须真人。手动微调语气、避免被识别为 AI |
| 给优质讨论点赞、关注作者 | 🧑 | 养号必须真人 |

### 中午 10 分钟 — Steam 社区

| 子动作 | 标记 | 说明 |
|---|---|---|
| 抓取 Steam Community Hub General Discussions 最新 20 帖 | 🤖 | Playwright 打开 `https://steamcommunity.com/app/<APPID>/discussions/`，提取标题 / 链接 / 回复数 / 是否未解决，输出 markdown 清单 |
| 起草回答草稿 | 🤝 | Claude 基于站内内容生成草稿 |
| 登录 Steam 账号发回答 / 点赞 | 🧑 | Steam 对自动化极敏感，必须真人 |
| Guides 板块新攻略点赞 | 🧑 | 真人 |

### 晚 10 分钟 — 数据 + Discord

| 子动作 | 标记 | 说明 |
|---|---|---|
| 拉取 GSC 当日 Performance 数据 | 🤖 | Search Console API（OAuth 一次授权后免人工），输出当日曝光 / 点击 / Top 上升关键词 |
| 拉取 Cloudflare Analytics（UV / 引荐来源） | 🤖 | Cloudflare GraphQL API，token 配好后全自动 |
| 生成日报到 `reports/daily/YYYY-MM-DD.md` | 🤖 | Claude 跑脚本聚合上面两份数据 |
| Discord 答 1–2 题 | 🧑 | 必须真人。Discord 自动化 = 直接 ban |

---

## 每周固定动作

### 周一 — Steam Guide 发布日

| 子动作 | 标记 | 说明 |
|---|---|---|
| 选当周主题（轮换：Beginner / Boss / Crafting / Ships …） | 🤝 | Claude 根据上周 GSC 高曝光词推荐主题 |
| 把对应站内英文页改写成 Steam Guide 格式（BBCode、章节、图、结尾 CTA） | 🤖 | 全自动。输出 `drafts/steam/YYYY-WW-<topic>.bbcode` |
| 截图素材准备 | 🧑 | 游戏内截图必须真人玩游戏截。Claude 不能代劳 |
| 登录 Steam 发布 Guide | 🧑 | 真人 |
| 发布后 24h 内回复评论 | 🧑 | 真人 |

### 周三 — Reddit 长帖

| 子动作 | 标记 | 说明 |
|---|---|---|
| 选题（数据可视化 / 深度指南，参考站内统计） | 🤝 | Claude 从 `data/` 目录里挖反差大的对比（如 Frigate vs Brigantine 真实 DPS）当题材 |
| 写 Reddit 正文（Markdown，自带表格 / 截图占位） | 🤖 | Claude 起草，输出 `drafts/reddit/YYYY-WW-<topic>.md` |
| 配图（图表、对比表）生成 | 🤖 | Claude 跑脚本用站内 JSON 数据生成 PNG（matplotlib / chart.js + Playwright 截图） |
| 实际发帖、和评论互动 | 🧑 | 真人。Reddit 反 bot 极强 |
| crosspost 到 r/pcgaming / r/Survivalgaming | 🧑 | 真人 |

### 周五 — 外链建设

| 子动作 | 标记 | 说明 |
|---|---|---|
| 用 Ahrefs / GSC API 拉本周新增外链域名 | 🤖 | GSC Links Report API |
| GameFAQs 攻略文档撰写 | 🤖 | Claude 把站内合并成单文档 txt |
| GameFAQs 提交 / 更新 | 🧑 | 必须人工，平台需账号信誉 |
| Fandom Wiki External Links 添加 | 🧑 | 真人，避免被判 spam |
| 寻找新外链机会（搜 Windrose 相关博客 / 论坛） | 🤖 | Claude 用 WebSearch 找候选，输出"邮件 outreach 名单" |
| 发 outreach 邮件 | 🧑 | 真人发，Claude 可起草模板 |

### 周日 — 复盘 + 下周排期

| 子动作 | 标记 | 说明 |
|---|---|---|
| 拉 GSC 7 天 Top 20 关键词 + 0 点击高曝光词 | 🤖 | API 全自动 |
| 自动给"0 点击高曝光"页面改写 title / meta | 🤖 | Claude 改完直接 commit PR，由你 review |
| 分析 Cloudflare 引荐来源 Top 10 | 🤖 | 全自动 |
| 出周报 `reports/weekly/YYYY-WW.md` | 🤖 | 全自动 |
| 决定下周 Steam Guide / Reddit 主题 | 🧑 | 真人拍板 |

---

## 双周 / 每月动作

### 短视频（每两周 1 条，可选）

| 子动作 | 标记 |
|---|---|
| 选题、剧本草稿 | 🤝 Claude 起草，人工定稿 |
| 游戏内录屏 | 🧑 真人玩 |
| 剪辑 + 字幕（可用项目自带 youtube-clipper skill） | 🤖 |
| 双语字幕翻译、烧录 | 🤖 |
| 发 YouTube / TikTok | 🧑 真人发 |
| 描述区放站点链接 | 🤖 模板自动填 |

### 每月 Medium / Dev.to 技术文

| 子动作 | 标记 |
|---|---|
| 选题（技术向：6 语言静态站、AI 翻译流水线） | 🤝 |
| 全文撰写 | 🤖 |
| 配图、代码块 | 🤖 |
| 发布到 Medium / Dev.to | 🧑 真人贴号发 |

### 每月末复盘

| 子动作 | 标记 |
|---|---|
| 月度数据汇总（GSC / Cloudflare / 外链） | 🤖 |
| 关键词排名变化、新增收录页 | 🤖 |
| 决定下月内容方向、是否启动多语种推广 | 🧑 真人决策 |

---

## 触发式动作（按事件触发）

| 触发 | 动作 | 标记 |
|---|---|---|
| 游戏发补丁 | 监控 Steam News RSS / SteamDB API | 🤖 全自动监控，到点推送提醒 |
| 同上 | 更新 /news 页面 + 生成 Steam 论坛"Patch 总结"草稿 + Reddit 帖草稿 | 🤖 |
| 同上 | 实际发到 Steam / Reddit | 🧑 |
| 出现新 Boss / 新系统 | 站内建独立页 | 🤖 |
| 同上 | Reddit + Steam Guide 双发 | 🧑（内容由 🤖 准备） |
| GSC 出现新长尾词曝光 ≥50/天 | 为该词建独立页 | 🤖 |
| Reddit 出现 Windrose 热门讨论（>50 upvotes） | 推送提醒 | 🤖 |
| 同上 | 评论区补深度回答 | 🧑 |

---

## 可以现在搭起来的自动化任务清单

按优先级，给 Claude Code 的待开发脚本：

| 优先级 | 脚本 | 路径 | 状态 | 频率 |
|---|---|---|---|---|
| P0 | Reddit 监控器（多 sub + 关键词，输出候选清单） | `scripts/promo/reddit_watch.py` | ✅ 已实现 | 每天早上 8 点 cron |
| P0 | GSC 日报（曝光 / 点击 / 新长尾词） | `scripts/promo/gsc_daily.py` | ✅ 已实现 | 每天 23 点 cron |
| P0 | Steam Discussions 抓取 | `scripts/promo/steam_watch.py` | ✅ 已实现 | 每天中午 cron |
| P1 | Cloudflare Analytics 拉取 | `scripts/promo/cf_analytics.py` | ⏳ 待开发 | 每天 23 点 |
| P1 | Steam Guide 自动改写器（站内 HTML → BBCode） | `scripts/promo/to_steam_bbcode.py` | ⏳ 待开发 | 按需 |
| P1 | Reddit 长帖草稿生成器 | `scripts/promo/reddit_draft.py` | ⏳ 待开发 | 每周三上午 |
| P2 | Steam News / SteamDB 补丁监控 | `scripts/promo/patch_watch.py` | ⏳ 待开发 | 每小时 |
| P2 | 外链监控（GSC Links + Ahrefs API） | `scripts/promo/backlink_watch.py` | ⏳ 待开发 | 每周 |
| P3 | 0 点击高曝光页 title/meta 改写器 | `scripts/promo/seo_rewrite.py` | ⏳ 待开发 | 每周日 |
| P3 | 数据可视化图生成（船 / 武器 / Boss 对比） | `scripts/promo/charts.py` | ⏳ 待开发 | 按需 |

输出统一汇总到 `reports/` 目录，并由 Claude Code 生成日 / 周 / 月报。

---

## 已实现脚本的使用方式

> 所有脚本只用 Python 3.11+ 标准库，无需 pip install。
> 日志走 stderr、生成的报告路径写 stdout，方便 pipeline 串联。
> 报告统一进 `reports/daily/YYYY-MM-DD-<name>.md`。

### 一次性配置

复制凭证模板：

```powershell
copy scripts\promo\.secrets.example.json scripts\promo\.secrets.json
```

`.secrets.json` 已在 `.gitignore` 中，不会进 git。也可全部用同名环境变量代替。

#### GSC 凭证获取（5–10 分钟人工，只需做一次）

1. 打开 https://console.cloud.google.com/ → 创建项目（或用现有项目）
2. APIs & Services → Library → 搜 "Search Console API" → Enable
3. APIs & Services → Credentials → Create Credentials → OAuth client ID → 选 **Desktop app**
4. 记下 `client_id` 和 `client_secret`
5. 打开 https://developers.google.com/oauthplayground
6. 右上齿轮 → 勾 **Use your own OAuth credentials** → 填入上一步的 client_id / secret
7. 左侧 scope 列表 → 找 **Google Search Console API v1** → 勾 `https://www.googleapis.com/auth/webmasters.readonly`
8. **Authorize APIs** → 用拥有 GSC 权限的 Google 账号登录 → 同意
9. **Exchange authorization code for tokens** → 复制 `refresh_token`
10. 把 `client_id` / `client_secret` / `refresh_token` 填进 `.secrets.json`

`GSC_SITE_URL` 用 Domain property 形式：`sc-domain:windrosewiki.games`（如果你 GSC 加站时用的是 URL prefix，则填 `https://windrosewiki.games/`）

### 日常用法

```powershell
# Reddit 监控（默认过去 24 小时，6 个 sub）
python scripts\promo\reddit_watch.py
python scripts\promo\reddit_watch.py --hours 48
python scripts\promo\reddit_watch.py --subs WindroseGame,pcgaming --keywords windrose,pirate

# Steam 论坛（默认抓第 1 页，关注回复数 ≤3 的新问题）
python scripts\promo\steam_watch.py
python scripts\promo\steam_watch.py --pages 2 --max-replies 5

# GSC 日报（近 7 天，因 GSC 数据延迟 2 天，窗口为 T-8 → T-2）
python scripts\promo\gsc_daily.py
python scripts\promo\gsc_daily.py --days 14
```

每次运行都会在 stdout 打出生成的报告文件路径，例如：

```
F:\aicode\gamedoc\reports\daily\2026-05-23-reddit.md
```

### 一键全跑

```powershell
python scripts\promo\reddit_watch.py
python scripts\promo\steam_watch.py
python scripts\promo\gsc_daily.py
```

### 用 Windows 任务计划程序定时跑

打开"任务计划程序"→ 创建基本任务，三条分别配：

| 任务名 | 触发 | 操作 |
|---|---|---|
| Promo - Reddit Watch | 每天 08:00 | `python.exe`，参数 `F:\aicode\gamedoc\scripts\promo\reddit_watch.py` |
| Promo - Steam Watch | 每天 12:00 | `python.exe`，参数 `F:\aicode\gamedoc\scripts\promo\steam_watch.py` |
| Promo - GSC Daily | 每天 23:00 | `python.exe`，参数 `F:\aicode\gamedoc\scripts\promo\gsc_daily.py` |

"起始位置"统一填 `F:\aicode\gamedoc`。

### 常见问题

| 现象 | 原因 | 解决 |
|---|---|---|
| Reddit `HTTP 403 Blocked` | 当前 IP 被 Reddit 拉黑（云服务器/机房常见） | 换家用网络或挂代理后重跑 |
| Steam `SSL EOF` / 超时 | 网络出口问题 | 同上 |
| GSC `缺少 GSC_OAUTH_*` | 凭证未配置 | 按上文 GSC 凭证获取步骤填 `.secrets.json` |
| GSC 报告里数据全是 0 | GSC 数据本身延迟 1–2 天 | 等一天再看；脚本已自动用 T-2 作为 endDate |
| Reddit 报告显示"未发现问答帖" | 过去 24h 真没人发 | 加 `--hours 168` 看一周 |

### 现在跑出来的会是什么

每个脚本输出一份 markdown，结构大致：

- **总览**（命中数、覆盖范围、时间窗口）
- **🎯 优先回答清单**（按"最值得回答"排序的具体帖子）
- **其他相关讨论**（次优）
- **行动建议**（每个脚本针对场景的提醒，比如 10:1 自推规则、单帖 1 链接）

每天看完三份报告 → 直接照着挑 3–5 条去 Reddit / Steam 真人回答即可，不用再到处搜帖。

---

## 一句话总结

| 类别 | 谁来做 |
|---|---|
| 写内容、抓数据、改 SEO、生成草稿、做图表、监控补丁 | 🤖 Claude Code 全包 |
| 登录账号 / 发帖 / 评论 / 点赞 / 私聊 / 视频录制 | 🧑 必须真人 |
| 选题拍板、社区氛围判断、外链 outreach 策略 | 🤝 一起决定 |

**人工每天的真实负担：30–45 分钟操作 + 周末 1–2 小时录素材 / 拍板**，其余全部由 Claude Code 离线跑。
