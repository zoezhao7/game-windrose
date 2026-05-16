# AGENTS.md

本文件是 Codex / 代理模型进入游戏攻略站项目后的通用工作规则。每次开始处理本仓库任务时，必须先阅读本文件，再阅读相关项目文档。

## 必读文件

进入项目后优先阅读：

1. `AGENTS.md`
2. `README.md`
3. `docs/GAME_GUIDE_SITE_SPEC.md`（通用攻略站规范）
4. `docs/windrose-dev-plan.md`（Windrose 项目专属开发方案）
5. `docs/experience.md`

如果任务涉及 SEO 页面生成，还需要阅读：

5. `scripts/build_site.py`
6. 当前项目仍在使用的临时生成脚本，例如 `scripts/seo_iteration.py`

如果任务涉及新增或修改数据对象，再阅读：

7. `data/schema-template.json`

## 数据驱动流程

后续内容维护必须遵守以下流程：

```text
1. 搭建或维护网站框架
2. 在 data/schema-template.json 中确认对象 JSON 格式
3. 将采集到的数据写入 data/*.json
4. 使用 scripts/build_site.py 根据 data 更新 HTML / sitemap / llms
5. 验证 HTML、JSON-LD、内链、sitemap
```

原则：

- `data/` 是长期内容源。
- HTML 是渲染结果，不应成为唯一数据源。
- 新数据必须有 `sources`、`confidence`、`status`、`last_verified`。
- 数据不足时标记 `needs_verification` 或 `unconfirmed`。
- 不确定内容先进入 tracker，不创建低质量详情页。

## 数据源经验记录

采集过程中如果发现：

- 某个数据源适合采集某类数据
- 某个数据源不可靠
- 某个来源字段经常变化
- 某类数据需要特殊验证方式

必须更新：

```text
docs/experience.md
```

该文档用于沉淀数据采集经验，避免后续重复踩坑。

## 脚本职责

长期推荐入口：

```powershell
python scripts\build_site.py
```

当前状态：

- `scripts/build_site.py` 是目标构建入口。
- `scripts/seo_iteration.py` 等脚本可能是第一阶段临时脚本，具体以当前项目 README 和脚本内容为准。
- `scripts/extract_html_data.py` 用于从现有 HTML 抽取内容快照到 `data/html-content-snapshot.json`。

注意：

- `seo_iteration.py` 会覆盖它负责生成的页面。
- 如果页面已经进入人工精修阶段，不要随意重跑会覆盖内容的脚本。
- 第二阶段应逐步把硬编码页面内容迁移到 `data/*.json`。

## 内容可信度规则

统一使用以下可信度：

| 值 | 含义 |
|---|---|
| `official` | Steam、官网、官方公告、官方服务器文档 |
| `verified` | 自己实测或可重复验证的游戏内数据 |
| `community` | Wiki、攻略站、视频、Reddit、Discord 等社区资料 |
| `unconfirmed` | 单一来源、版本不明、无法复现 |
| `outdated` | 旧版本数据，可能已失效 |

页面文案规则：

- 不确定内容写 `Needs verification` 或 `Verify after latest patch`。
- 不要用 `Complete`、`All`、`Every` 等绝对词，除非数据确实完整且已验证。
- Boss、资源、配方页面优先使用 `Known`、`Early Access Tracker`、`Verified` 等表达。
- 不为资料不足的条目创建薄详情页。

## 修改规范

- 修改数据前，先看 `data/schema-template.json`。
- 修改内容来源经验，更新 `docs/experience.md`。
- 修改通用规范（SEO/AdSense/性能/多语言），更新 `docs/GAME_GUIDE_SITE_SPEC.md`。
- 修改 Windrose 项目方案（阶段/脚本/数据文件/验证基线），更新 `docs/windrose-dev-plan.md`。
- 修改脚本使用方式，更新 `README.md`。
- 新增页面后，同步 `sitemap.xml` 和 `llms.txt`。
- 运行脚本后，检查是否覆盖了人工精修页面。

## 验证清单

完成内容或脚本改动后，至少检查：

```powershell
python scripts\build_site.py
```

并确认：

- JSON 可以解析
- 关键页面本地返回 200
- JSON-LD 无解析错误
- sitemap 不包含 404
- 站内链接无坏链
- 页面没有明显 `coming soon`、`TBD`、空白主内容

## 关于 AGENTS.md 的读取

Codex 通常会自动读取仓库根目录或当前目录链路上的 `AGENTS.md` 作为项目指令。为了保险，后续新会话开始时也可以明确要求：

```text
请先阅读 AGENTS.md、README.md、docs/GAME_GUIDE_SITE_SPEC.md、docs/windrose-dev-plan.md 和 docs/experience.md，再继续任务。
```

如果代理环境没有自动读取 `AGENTS.md`，必须手动打开本文件后再执行项目任务。
