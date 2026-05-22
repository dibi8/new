# API Setup Guide / API 密钥获取指南

This guide walks you through getting API credentials for each platform.

---

## 1. Twitter/X

### Required Secrets
| Secret Name | Description |
|---|---|
| `TWITTER_API_KEY` | API Key (Consumer Key) |
| `TWITTER_API_SECRET` | API Secret (Consumer Secret) |
| `TWITTER_ACCESS_TOKEN` | Access Token |
| `TWITTER_ACCESS_SECRET` | Access Token Secret |

### Steps
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new **Project** and **App**
3. In the App settings, go to **Keys and Tokens**
4. Generate **API Key and Secret** (Consumer Keys)
5. Generate **Access Token and Secret**
6. Make sure the App has **Read and Write** permissions:
   - Go to App Settings → User authentication settings → Set up
   - Select **Read and Write** under App permissions
7. Add all 4 values as GitHub repository secrets

> ⚠️ Twitter Free tier allows 1,500 tweets/month. Basic ($100/mo) allows 3,000.

---

## 2. Facebook

### Required Secrets
| Secret Name | Description |
|---|---|
| `FACEBOOK_PAGE_ID` | Your Facebook Page ID |
| `FACEBOOK_ACCESS_TOKEN` | Page Access Token (long-lived) |

### Steps
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new App (type: Business)
3. Add the **Facebook Login** product
4. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
5. Select your App, then click **Get User Access Token**
6. Select permissions: `pages_manage_posts`, `pages_read_engagement`
7. Click **Generate Access Token** and authorize
8. Exchange for a **long-lived token**:
   ```
   GET https://graph.facebook.com/v19.0/oauth/access_token?
     grant_type=fb_exchange_token&
     client_id={APP_ID}&
     client_secret={APP_SECRET}&
     fb_exchange_token={SHORT_LIVED_TOKEN}
   ```
9. Get the **Page Access Token**:
   ```
   GET https://graph.facebook.com/v19.0/me/accounts?access_token={LONG_LIVED_USER_TOKEN}
   ```
10. Find your Page in the response — the `access_token` is your permanent Page Access Token
11. The `id` field is your `FACEBOOK_PAGE_ID`

---

## 3. LinkedIn

### Required Secrets
| Secret Name | Description |
|---|---|
| `LINKEDIN_ACCESS_TOKEN` | OAuth 2.0 Access Token |
| `LINKEDIN_ORG_ID` | (Optional) Organization/Company Page ID |

### Steps
1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/)
2. Create a new App
3. Request access to **Share on LinkedIn** and **Sign In with LinkedIn using OpenID Connect**
4. In the **Auth** tab, note the **Client ID** and **Client Secret**
5. Generate an access token via OAuth 2.0 flow:
   - Authorization URL: `https://www.linkedin.com/oauth/v2/authorization`
   - Token URL: `https://www.linkedin.com/oauth/v2/accessToken`
   - Scopes: `openid profile w_member_social`
   - For organization posting, also request: `w_organization_social`
6. Use the access token as `LINKEDIN_ACCESS_TOKEN`

> 💡 LinkedIn tokens expire in 60 days. Set a reminder to refresh.

---

## 4. Medium

### Required Secrets
| Secret Name | Description |
|---|---|
| `MEDIUM_TOKEN` | Integration Token |

### Steps
1. Go to [Medium Settings](https://medium.com/me/settings)
2. Scroll to **Security and apps**
3. Click **Integration tokens**
4. Enter a description (e.g., "dibi8-auto-publisher") and click **Get token**
5. Copy the token as `MEDIUM_TOKEN`

> This is the simplest API to set up!

---

## 5. Reddit

### Required Secrets
| Secret Name | Description |
|---|---|
| `REDDIT_CLIENT_ID` | App Client ID |
| `REDDIT_CLIENT_SECRET` | App Client Secret |
| `REDDIT_USERNAME` | Reddit username |
| `REDDIT_PASSWORD` | Reddit password |
| `REDDIT_SUBREDDIT` | Target subreddit (default: `artificial`) |

### Steps
1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click **Create App** or **Create Another App**
3. Fill in:
   - **Name**: dibi8-auto-publisher
   - **Type**: Select **script**
   - **Redirect URI**: `http://localhost:8080`
4. Click **Create App**
5. Note the **Client ID** (under the app name) and **Client Secret**
6. Use your Reddit login credentials for `REDDIT_USERNAME` and `REDDIT_PASSWORD`

> ⚠️ Be mindful of subreddit rules. Many subreddits have self-promotion limits.

---

## Adding Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the exact name from the tables above

You only need to configure the platforms you want to use. Unconfigured platforms are automatically skipped.

---

## Testing

Run manually to test:

```bash
# Set environment variables
export TWITTER_API_KEY="your-key"
# ... set all variables for platforms you want to test

# Run the publisher
python run.py
```

Or trigger the workflow manually:
1. Go to **Actions** tab in your GitHub repo
2. Select **Auto Publish dibi8 Articles**
3. Click **Run workflow**
