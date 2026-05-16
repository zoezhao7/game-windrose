# Windrose Guides

Windrose 非官方攻略站项目。当前项目采用 **纯静态 HTML/CSS** 架构，不依赖 React/Vue、后端服务或构建工具，适合部署到 Cloudflare Pages、GitHub Pages、Vercel 等静态托管平台。

## 给 Codex / 代理模型的说明

开始处理本项目任务前，请先阅读根目录：

```text
AGENTS.md
```

`AGENTS.md` 记录了本项目的数据驱动流程、数据可信度规则、脚本职责、采集经验维护要求和验证清单。

## 本地预览

在项目根目录执行：

```powershell
python -m http.server 4173 -d F:\aicode\gamedoc
```

然后浏览器打开：

```text
http://localhost:4173/
```

## 数据驱动流程

后续项目按以下流程维护：

```text
1. 搭建网站框架
2. 在 data/schema-template.json 约定数据对象格式
3. 把采集到的数据保存到 data/*.json
4. 使用 scripts/build_site.py 读取 data 并更新 HTML / sitemap / llms
```

当前已提供数据格式模板：

```text
data/schema-template.json
```

当前已拆分出第一版正式数据文件：

```text
data/pages.json
data/bosses.json
data/recipes.json
data/resources.json
data/ships.json
data/weapons.json
data/builds.json
data/tools.json
data/news.json
data/sources.json
```

同时保留了一份从现有 HTML 抽取出来的内容快照：

```text
data/html-content-snapshot.json
```

这份快照用于迁移保护，避免后续数据化改造时丢失已经写进 HTML 的内容。后续业务维护应优先更新分类型 JSON 文件，而不是直接维护快照。

## 构建脚本

长期推荐使用：

```text
scripts/build_site.py
```

运行方式：

```powershell
python scripts\build_site.py
```

当前 `build_site.py` 会：

- 校验 `data/*.json`
- 兼容调用第一阶段临时脚本 `scripts/seo_iteration.py`
- 刷新 `sitemap.xml`
- 输出构建结果

## 数据拆分脚本

如果需要重新从现有 HTML 抽取并拆分数据，可以依次执行：

```powershell
python scripts\extract_html_data.py
python scripts\split_snapshot_data.py
```

说明：

- `extract_html_data.py` 会生成 `data/html-content-snapshot.json`
- `split_snapshot_data.py` 会把快照拆成 `data/pages.json`、`data/bosses.json`、`data/recipes.json` 等分类型数据文件
- 这两个脚本主要用于迁移期，后续稳定后应直接维护分类型 JSON 文件

## SEO 迭代脚本

当前主要辅助脚本是：

```text
scripts/seo_iteration.py
```

这个脚本用于批量生成和刷新 SEO 页面，并同步更新站点基础文件。

注意：`seo_iteration.py` 是第一阶段临时脚本。后续内容更新应逐步迁移到 `data/*.json` + `scripts/build_site.py`。

## 脚本会更新哪些内容

运行 `scripts/seo_iteration.py` 后，会生成或刷新以下内容：

- `/tools/` 工具中心页面
- `/tools/recipe-finder/` 配方查询页
- `/tools/progression-checklist/` 进度清单页
- `/tools/resource-planner/` 资源规划页
- `/tools/ship-selector/` 船只选择页
- `/server-guide/` 专用服务器指南
- `/download/` 下载与游戏信息页
- `/sources/` 数据来源与更新策略页
- `/crafting/alchemy/`
- `/crafting/cooking/`
- `/crafting/building/`
- `/bosses/`
- `/news/`
- 首页导航和首页工具入口
- `llms.txt`
- `sitemap.xml`
- `docs/ITERATION_TODO_PROMOTION.md`
- `css/style.css` 中少量通用样式补充

## 如何运行脚本

推荐在项目根目录执行：

```powershell
python scripts\build_site.py
```

如需单独运行第一阶段临时 SEO 脚本，也可以执行：

```powershell
python scripts\seo_iteration.py
```

正常情况下会看到类似输出：

```text
Generated 13 SEO pages and refreshed site files.
```

## 内容来源说明

当前脚本 **不会在运行时联网抓取内容**。脚本里的页面内容是静态写入的，主要来源包括：

- Windrose 的 Steam 官方商店页信息
- Windrose 官方 dedicated server guide 信息
- 项目已有规划文档，例如 `docs/windrose-dev-plan.md`、`docs/GAME_GUIDE_SITE_SPEC.md`
- 对竞品 `heartopia.gg` 的 SEO 结构分析

也就是说，脚本现在是一个“静态页面生成器”，不是自动爬虫。

## 重要注意事项

`scripts/seo_iteration.py` 会覆盖它负责生成的页面。

如果你手动修改了以下页面，再次运行脚本时，手动改动可能会被覆盖：

- `/tools/`
- `/server-guide/`
- `/download/`
- `/sources/`
- `/crafting/alchemy/`
- `/crafting/cooking/`
- `/crafting/building/`
- `/bosses/`
- `/news/`

如果后续要长期维护，建议把内容从脚本里拆出来，改成：

```text
data/*.json
content/*.md
templates/*.html
```

然后让 Python 脚本只负责读取数据并渲染 HTML。

## 推荐验证流程

运行脚本后，先启动本地服务：

```powershell
python -m http.server 4173 -d F:\aicode\gamedoc
```

然后检查以下页面是否正常返回：

- `http://localhost:4173/`
- `http://localhost:4173/tools/`
- `http://localhost:4173/tools/recipe-finder/`
- `http://localhost:4173/server-guide/`
- `http://localhost:4173/download/`
- `http://localhost:4173/crafting/alchemy/`
- `http://localhost:4173/bosses/`
- `http://localhost:4173/news/`

## 当前上线前重点

- 补充真实截图或 WebP 图片资源
- 给主要页面配置更准确的 `og:image`
- 部署后使用 Google Rich Results Test 检查结构化数据
- 接入 Google Search Console 并提交 `sitemap.xml`
- AdSense 账号通过后替换正式 `ads.txt`

## 竞品参考与数据来源 (Competitors)
- windrose.tools
- gaming.tools
- windrosegame.net
- windrosewiki.org
