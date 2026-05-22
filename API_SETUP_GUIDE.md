# API 密钥获取指南

本指南教你如何获取各平台的 API 密钥。详细的图文说明请参考 [使用说明书.md](./使用说明书.md)。

---

## 1. Twitter/X

### 需要的密钥
| 密钥名称 | 说明 |
|----------|------|
| `TWITTER_API_KEY` | API 密钥（Consumer Key） |
| `TWITTER_API_SECRET` | API 密钥密码（Consumer Secret） |
| `TWITTER_ACCESS_TOKEN` | 访问令牌 |
| `TWITTER_ACCESS_SECRET` | 访问令牌密码 |

### 申请步骤
1. 打开 [Twitter 开发者平台](https://developer.twitter.com/en/portal/dashboard)
2. 创建新的 **Project**（项目）和 **App**（应用）
3. 在应用设置中，进入 **Keys and Tokens**（密钥和令牌）
4. 生成 **API Key and Secret**（Consumer Keys）
5. 生成 **Access Token and Secret**（访问令牌）
6. 确保应用有 **读写权限**：
   - 进入 App Settings → User authentication settings → Set up
   - App permissions 选择 **Read and Write**
7. 把 4 个值添加到 GitHub 仓库的 Secrets

> ⚠️ 免费版每月 1,500 条推文。Basic 版（$100/月）3,000 条。本系统每天最多 6 条，足够用。

---

## 2. Facebook

### 需要的密钥
| 密钥名称 | 说明 |
|----------|------|
| `FACEBOOK_PAGE_ID` | Facebook 主页 ID |
| `FACEBOOK_ACCESS_TOKEN` | 主页访问令牌（永久有效） |

### 申请步骤
1. 打开 [Meta 开发者平台](https://developers.facebook.com/)
2. 创建新应用（类型选 Business / 商家）
3. 添加 **Facebook Login**（Facebook 登录）产品
4. 打开 [Graph API 探索工具](https://developers.facebook.com/tools/explorer/)
5. 选择你的应用，点击 **Get User Access Token**（获取用户访问令牌）
6. 勾选权限：`pages_manage_posts`、`pages_read_engagement`
7. 点击 **Generate Access Token** 并授权
8. 把短期令牌换成长期令牌：
   ```
   GET https://graph.facebook.com/v19.0/oauth/access_token?
     grant_type=fb_exchange_token&
     client_id={应用ID}&
     client_secret={应用密钥}&
     fb_exchange_token={短期令牌}
   ```
9. 获取主页令牌：
   ```
   GET https://graph.facebook.com/v19.0/me/accounts?access_token={长期用户令牌}
   ```
10. 在返回结果中找到你的主页：
    - `access_token` = 永久主页令牌 → `FACEBOOK_ACCESS_TOKEN`
    - `id` = 主页 ID → `FACEBOOK_PAGE_ID`

---

## 3. LinkedIn

### 需要的密钥
| 密钥名称 | 说明 |
|----------|------|
| `LINKEDIN_ACCESS_TOKEN` | OAuth 2.0 访问令牌 |
| `LINKEDIN_ORG_ID` | （可选）公司主页 ID |

### 申请步骤
1. 打开 [LinkedIn 开发者平台](https://www.linkedin.com/developers/)
2. 创建新应用
3. 申请 **Share on LinkedIn** 和 **Sign In with LinkedIn using OpenID Connect** 权限
4. 在 **Auth** 标签中获取 **Client ID** 和 **Client Secret**
5. 通过 OAuth 2.0 流程获取访问令牌：
   - 授权地址：`https://www.linkedin.com/oauth/v2/authorization`
   - 令牌地址：`https://www.linkedin.com/oauth/v2/accessToken`
   - 权限范围：`openid profile w_member_social`
   - 发到公司主页还需要：`w_organization_social`
6. 获取的访问令牌就是 `LINKEDIN_ACCESS_TOKEN`

> ⚠️ LinkedIn 令牌 **60 天后过期**！需要定期重新获取。建议设日历提醒。

---

## 4. Medium

### 需要的密钥
| 密钥名称 | 说明 |
|----------|------|
| `MEDIUM_TOKEN` | 集成令牌（Integration Token） |

### 申请步骤（最简单！）
1. 打开 [Medium 设置页面](https://medium.com/me/settings)
2. 找到 **Security and apps**（安全和应用）
3. 点击 **Integration tokens**（集成令牌）
4. 输入描述（如 `dibi8-auto-publisher`），点击 **Get token**
5. 复制令牌 → `MEDIUM_TOKEN`

> 30 秒搞定！

---

## 5. Reddit

### 需要的密钥
| 密钥名称 | 说明 |
|----------|------|
| `REDDIT_CLIENT_ID` | 应用 Client ID |
| `REDDIT_CLIENT_SECRET` | 应用 Client Secret |
| `REDDIT_USERNAME` | Reddit 用户名 |
| `REDDIT_PASSWORD` | Reddit 密码 |
| `REDDIT_SUBREDDITS` | 目标 subreddit 列表（逗号分隔，默认 `artificial`） |

### 申请步骤
1. 打开 [Reddit 应用管理页面](https://www.reddit.com/prefs/apps)
2. 点击 **Create App** 或 **Create Another App**
3. 填写信息：
   - **Name**（名称）：`dibi8-auto-publisher`
   - **Type**（类型）：选择 **script**（脚本）
   - **Redirect URI**：`http://localhost:8080`
4. 点击 **Create App**
5. 应用名下方的字符串 = `REDDIT_CLIENT_ID`
6. **secret** 一行 = `REDDIT_CLIENT_SECRET`
7. `REDDIT_USERNAME` 和 `REDDIT_PASSWORD` 就是你的 Reddit 登录账号密码

> ⚠️ Reddit 封号风险最高，请先手动积累 karma 再启用自动发帖。

---

## 添加密钥到 GitHub

1. 打开你的 GitHub 仓库
2. 点击 **Settings**（设置）→ **Secrets and variables** → **Actions**
3. 点击 **New repository secret**（新建仓库密钥）
4. 按上面的表格逐一添加密钥

**只需要配置你想用的平台**，没有配置的平台会自动跳过。

---

## 测试运行

手动触发测试：
1. 打开仓库的 **Actions** 标签
2. 选择 **Auto Publish dibi8 Articles**
3. 点击 **Run workflow** → **Run workflow**

本地测试：
```bash
# 设置环境变量
export TWITTER_API_KEY="你的密钥"
# ... 设置所有要测试的平台变量

# 禁用延迟方便测试
export STARTUP_JITTER_MAX=0
export INTER_PLATFORM_DELAY_MIN=0
export INTER_PLATFORM_DELAY_MAX=0
export RANDOM_SKIP_PROBABILITY=0

# 运行
python run.py
```
