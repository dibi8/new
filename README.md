# dibi8 自动发布系统

自动从 [dibi8.com](https://dibi8.com) 抓取文章，定时发布到多个社交平台 — 内置防封号保护。

## 防封号安全机制

| 功能 | 说明 |
|------|------|
| **启动随机延迟** | 每次运行随机等待 0-50 分钟，发帖时间在每小时窗口内完全随机 |
| **随机跳过** | 15% 概率跳过本次运行，发帖不规律更像真人 |
| **每日发帖上限** | Twitter: 6条/天, Facebook: 4条/天, LinkedIn: 2条/天, Medium: 1篇/天, Reddit: 2帖/天 |
| **最小发帖间隔** | 同平台强制冷却（Twitter 2小时, LinkedIn 6小时, Medium 24小时, Reddit 8小时） |
| **平台间延迟** | 发完一个平台后等 1-5 分钟再发下一个 |
| **内容变体** | 每个平台用不同的格式/模板/话题标签，避免被检测为模板化发帖 |
| **平台顺序随机** | 每次运行打乱平台发布顺序 |
| **Token 验证** | 发布前检查凭证是否有效，过期会记录日志告警 |
| **指数退避重试** | 遇到限流会自动等待并重试，不是盲目重试 |
| **Reddit 专项保护** | Subreddit 轮换、重复链接检测、标题前缀随机变化 |
| **User-Agent 轮换** | 抓取网页时随机使用不同浏览器标识 |
| **加权文章选择** | 越新的文章被选中概率越高 |

## 功能特点

- **RSS 抓取** — 从 dibi8.com 的 RSS 订阅源获取文章（257+ 篇）
- **多平台发布** — 支持 Twitter/X、Facebook、LinkedIn、Medium、Reddit
- **智能调度** — 亚洲和美国工作时间每小时运行一次
- **防重复** — 按平台跟踪已发布文章，不会重复发
- **自动循环** — 所有文章发完后自动重置，重新开始
- **优雅降级** — 没有配置的平台自动跳过

## 运行时间

| 地区 | 本地时间 | UTC 时间 |
|------|---------|----------|
| 亚洲（UTC+8） | 09:00 – 17:00 | 01:00 – 09:00 |
| 美国（UTC-5） | 09:00 – 17:00 | 14:00 – 22:00 |

每天共 **18 次触发**，加上随机跳过（~15%）和发帖上限，实际每个平台发帖量很低。

## 快速开始

1. **Fork/克隆** 本仓库
2. **申请 API 密钥** — 按照 [使用说明书.md](./使用说明书.md) 操作
3. **添加密钥** 到 GitHub 仓库的 Settings → Secrets
4. GitHub Action 会按计划自动运行

### 手动测试

```bash
pip install -r requirements.txt

# 禁用延迟，方便本地测试
export STARTUP_JITTER_MAX=0
export INTER_PLATFORM_DELAY_MIN=0
export INTER_PLATFORM_DELAY_MAX=0
export RANDOM_SKIP_PROBABILITY=0

# 设置平台密钥
export TWITTER_API_KEY="..."
# ...（完整变量列表见使用说明书）

python run.py
```

## 项目结构

```
├── .github/workflows/
│   └── auto-publish.yml     # GitHub Actions 定时工作流
├── src/
│   ├── config.py            # 配置和环境变量
│   ├── scraper.py           # RSS 解析和文章元数据抓取
│   ├── scheduler.py         # 主调度器（含安全控制）
│   ├── safety.py            # 速率限制、每日上限、冷却时间、随机延迟
│   ├── content.py           # 内容变体引擎（每平台不同格式）
│   └── publishers/
│       ├── twitter.py       # Twitter/X（Tweepy + 重试 + 限流处理）
│       ├── facebook.py      # Facebook 主页（Graph API + Token过期检测）
│       ├── linkedin.py      # LinkedIn（REST API v2 + Token过期检测）
│       ├── medium.py        # Medium（集成令牌 + 重试）
│       └── reddit.py        # Reddit（PRAW + 重复检测 + Subreddit轮换）
├── data/
│   ├── published.json       # 已发布文章记录（按平台）
│   └── rate_limits.json     # 每日发帖计数和最后发帖时间
├── requirements.txt
├── 使用说明书.md             # 详细中文使用说明（含API申请教程）
└── README.md
```

## 配置说明

所有配置通过环境变量（或 GitHub Secrets）设置。

### 防封号参数

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `STARTUP_JITTER_MAX` | `3000` | 最大随机启动延迟（秒），0-50分钟覆盖整个小时 |
| `INTER_PLATFORM_DELAY_MIN` | `60` | 平台间最小延迟（秒） |
| `INTER_PLATFORM_DELAY_MAX` | `300` | 平台间最大延迟（秒） |
| `RANDOM_SKIP_PROBABILITY` | `0.15` | 随机跳过概率（0-1），0.15 = 15% |

### 平台密钥

| 平台 | 需要的密钥 |
|------|-----------|
| Twitter/X | `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET` |
| Facebook | `FACEBOOK_PAGE_ID`, `FACEBOOK_ACCESS_TOKEN` |
| LinkedIn | `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_ORG_ID`（可选） |
| Medium | `MEDIUM_TOKEN` |
| Reddit | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD`, `REDDIT_SUBREDDITS` |

### Reddit 多 Subreddit 配置

设置 `REDDIT_SUBREDDITS` 为逗号分隔的列表，系统会随机轮换发帖：

```
REDDIT_SUBREDDITS=artificial,MachineLearning,OpenSource,selfhosted
```

## 防封号注意事项

1. **循序渐进** — 不要一次开启所有平台，先启用 1-2 个，运行几周后再添加
2. **手动互动** — 特别是 Reddit，确保账号有正常的评论、点赞等互动
3. **查看日志** — 定期检查 GitHub Actions 日志，关注限流和 Token 过期告警
4. **LinkedIn Token 会过期** — 每 60 天需要重新获取，建议设日历提醒
5. **Facebook 用主页令牌** — 主页令牌不会过期，不要用用户令牌（60天过期）
6. **Reddit 先攒 karma** — 低 karma 账号更容易被标记，先手动积累再开自动发帖
7. **考虑周末不运行** — LinkedIn 可以考虑只在工作日运行

## 许可证

MIT
