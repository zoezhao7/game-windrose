# Promo Scripts — 推广自动化脚本

这一组脚本对应 `docs/PROMOTION_DAILY_PLAYBOOK.md` 里所有标 🤖 / 🤝 的动作。
全部脚本都把日志输出到 stderr、把生成的报告路径写到 stdout，便于 pipeline 串联。

## 现有脚本

| 脚本 | 频次 | 输出 | 说明 |
|---|---|---|---|
| `reddit_watch.py` | 每天早上 | `reports/daily/YYYY-MM-DD-reddit.md` | 多 sub Windrose 关键词新帖，标记疑似问答 |
| `steam_watch.py` | 每天中午 | `reports/daily/YYYY-MM-DD-steam.md` | Steam Discussions 新帖，标记低回复待答 |
| `gsc_daily.py` | 每天 23 点 | `reports/daily/YYYY-MM-DD-gsc.md` | GSC 7 天搜索表现 + 高曝光 0 点击词 |

## 安装

```powershell
# Python 3.11+
# 当前所有脚本只用标准库，未来加 Cloudflare/Playwright 时再补依赖
```

## 凭证配置

复制示例文件并填入真实值：

```powershell
copy scripts\promo\.secrets.example.json scripts\promo\.secrets.json
```

`.secrets.json` 已在 `.gitignore` 中，不会进 git。

也可以全部用环境变量代替（变量名与 json key 同名）。

### GSC 凭证获取（一次性人工）

1. 在 Google Cloud Console 创建 OAuth Desktop 客户端，记下 client_id / secret
2. 打开 https://developers.google.com/oauthplayground
3. 右上齿轮 → 勾"Use your own OAuth credentials"，填入上一步的 client_id / secret
4. 左侧 scope 列表 → 找 `Google Search Console API` → 选 `webmasters.readonly`
5. Authorize → 同意 → Exchange authorization code for tokens
6. 把 `refresh_token` 复制到 `.secrets.json`

`GSC_SITE_URL` 用 Domain property 形式：`sc-domain:windrosewiki.games`

## 用法示例

```powershell
# Reddit 监控（默认过去 24 小时，6 个 sub）
python scripts\promo\reddit_watch.py
python scripts\promo\reddit_watch.py --hours 48 --subs WindroseGame,pcgaming

# Steam 论坛
python scripts\promo\steam_watch.py
python scripts\promo\steam_watch.py --pages 2 --max-replies 5

# GSC 日报（近 7 天）
python scripts\promo\gsc_daily.py
python scripts\promo\gsc_daily.py --days 14
```

每次运行都会在 stdout 打出生成的报告文件路径，比如：

```
F:\aicode\gamedoc\reports\daily\2026-05-23-reddit.md
```

## 一键跑全部（建议）

```powershell
python scripts\promo\reddit_watch.py
python scripts\promo\steam_watch.py
python scripts\promo\gsc_daily.py
```

可以做成 Windows 计划任务，每天早 8:00 / 12:00 / 23:00 各跑一次。

## 待开发（按 PROMOTION_DAILY_PLAYBOOK 优先级）

- P1 `cf_analytics.py` — Cloudflare Analytics 拉取（UV / 引荐来源）
- P1 `to_steam_bbcode.py` — 站内 HTML → Steam Guide BBCode
- P1 `reddit_draft.py` — Reddit 长帖草稿生成器
- P2 `patch_watch.py` — Steam News / SteamDB 补丁监控
- P2 `backlink_watch.py` — 外链监控
- P3 `seo_rewrite.py` — 0 点击高曝光页 title/meta 改写器
- P3 `charts.py` — 数据可视化图生成

## 设计约定

- **不发帖、不评论、不点赞、不私聊**：所有社交动作必须真人执行（Reddit/Steam/Discord 反 bot 极强，自动化 = 封号 + 域名拉黑）
- 脚本只做：抓取、分析、生成草稿、改写、监控、出报告
- 所有报告统一进 `reports/{daily,weekly,monthly}/` 便于回看和 git 追踪
