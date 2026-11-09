# plugins-marketplace

Sesame Hut 的插件索引。各插件的工具支持范围和安装方式以其说明为准。

## 使用（Claude Code）

```bash
/plugin marketplace add sesamehut/plugins-marketplace
/plugin install <plugin-name>@sesamehut-plugins
```

当前插件：

| 插件 | 版本 | 描述 |
|------|------|------|
| `sonara` | 0.1.0 | SONARA 音频库工作流 skill 集合 |
| `agent-config-bridge` | 0.1.0 | Claude Code / Codex 项目级 agent 配置桥：只读漂移哨兵，以及计划确认后才落盘的同步；覆盖项目 skill、入口指令、规则分片与 hook 意图 |
| `casement` | 0.1.2 | Claude Code / Codex 的 AWS 入门、Lightsail 开通、节点部署运维及伪装域名选型与私有决策记录 skill |

## 新增插件

1. 在源码仓库的 `plugin/` 中生成可安装产物，或使用独立分发仓库；按实际支持的工具提供 manifest 与使用说明
2. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组中登记，发布条目固定版本 `ref` 与对应 commit `sha`
3. 提交并推送 marketplace 仓库
4. 用户执行 `/plugin marketplace update` 即可发现新插件

## Codex / Gemini 用户

Codex 也支持 marketplace，可从插件目录安装支持 Codex 的插件；具体命令见该插件的安装说明。Gemini 用户按各插件说明使用，不假定所有插件均支持 Gemini。
