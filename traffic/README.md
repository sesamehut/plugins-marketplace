# traffic/

GitHub 只保留最近 **14 天**的流量（clone / view）。这里用一个每天跑的
GitHub Action（[`../.github/workflows/traffic.yml`](../.github/workflows/traffic.yml)）
把数据快照下来，按日期合并进每仓库一个 CSV，于是 14 天滚动窗口就拼成了长期曲线。

## 文件

- `collect.py` —— 采集脚本，调用 `gh api .../traffic/clones` 与 `.../traffic/views`，
  按日期 upsert 进 CSV。要追踪更多仓库，在脚本顶部的 `REPOS` 里加 `owner/repo`。
- `<repo>.csv` —— 每个被追踪仓库一份，列为：
  `date, clones_total, clones_unique, views_total, views_unique`。

## 怎么读

- **看 `*_unique`（按 IP 去重）而不是 `*_total`。** 一次真实安装 ≈ 1 个独立 IP 的
  clone；`total` 会被重复 clone 灌水。
- **`clones` ≠ `installs`**：CI、镜像站、归档机器人（如 Software Heritage）也会
  clone。某一天 `clones_total` 远大于 `clones_unique`（高倍率）基本就是自动化/CI，
  不是安装。
- **本仓库（`plugins-marketplace`）没有 CI**，所以它的 `clones_unique` 是最干净的
  「有多少独立来源加了这个市场」信号。带 CI 的插件源仓库噪声更大，只信它的
  `unique` 列，并把高倍率的日子当作自动化剔除。

## 一次性配置：PAT secret

Action 用内置的 `GITHUB_TOKEN` **读不了** traffic API（该接口要求 push 权限，而内置
token 没有）。所以需要一个 PAT：

1. 建一个 PAT（classic：勾 `repo` scope；或 fine-grained：对被追踪的每个仓库给
   `Administration: Read-only`），账号需对这些仓库有 push 权限。
2. 存为本仓库的 Actions secret，名为 `TRAFFIC_PAT`：

   ```bash
   gh secret set TRAFFIC_PAT --repo sesamehut/plugins-marketplace
   ```

## 手动 / 本地运行

```bash
# 本地（gh 已登录、对相关仓库有 push 权限即可）
python3 traffic/collect.py

# 在 GitHub 上手动触发一次
gh workflow run "Archive repo traffic" --repo sesamehut/plugins-marketplace
```
