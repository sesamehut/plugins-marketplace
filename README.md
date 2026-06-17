# plugins-marketplace

Sesame Hut 的 Claude Code 插件索引。所有插件均设计为跨 Claude Code / Codex CLI / Gemini CLI 三家工具通用（具体安装命令见各 plugin 仓库 README）。

## 使用（Claude Code）

```bash
/plugin marketplace add sesamehut/plugins-marketplace
/plugin install <plugin-name>@sesamehut-plugins
```

当前插件：

| 插件 | 版本 | 描述 |
|------|------|------|
| `sonara` | 0.1.0 | SONARA 音频库工作流 skill 集合 |

## 新增插件

1. 独立 plugin 仓库按跨工具分发约定组织（同时兼容 Claude Code / Codex CLI / Gemini CLI）
2. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组中登记
3. 提交并推送 marketplace 仓库
4. 用户执行 `/plugin marketplace update` 即可发现新插件

## Codex / Gemini 用户

marketplace 是 Claude 独占概念。Codex / Gemini 用户请直接到对应 plugin 仓库按其 README 安装。
