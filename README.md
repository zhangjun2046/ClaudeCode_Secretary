# ClaudeCode_Secretary

> 你的个人AI助理团队 - 新闻张、教练张、反思张

ClaudeCode_Secretary 是一个基于 Claude Code 的个人生活助理系统，包含三个专业AI分身，帮助你管理日常新闻、健康追踪和工作反思。

## 核心功能

### 🗞️ 新闻张 - 晨间新闻助理
- 自动搜集AI、金融、股市领域的最新资讯
- 生成个性化新闻简报
- 可选飞书推送通知

**触发**: `/早上好`

### 💪 教练张 - 健康教练
- 追踪体重变化趋势
- 提供个性化运动和饮食建议
- 激励和支持健康目标达成

**触发**: `/自律`

### 🌙 反思张 - 工作反思伙伴
- 引导式多轮深度对话
- 帮助梳理工作体验和情绪
- 识别长期模式，促进个人成长

**触发**: `/今工作结束了`

## 快速开始

### 1. 前置要求

- [Claude Desktop](https://claude.ai/download) 已安装
- Node.js 环境（用于 MCP 服务器）

### 2. 配置步骤

1. **克隆或下载项目**
   ```bash
   git clone <your-repo-url>
   cd ClaudeCode_Secretary
   ```

2. **配置 MCP 服务器**

   参考 [`docs/MCP_SETUP.md`](docs/MCP_SETUP.md) 配置必需的 MCP 服务器：
   - MCP Filesystem（必需）
   - MCP Fetch（必需）
   - MCP Brave Search（推荐）
   - MCP Memory（推荐）

3. **填写个人档案**

   编辑 `context/about_me.md`，填入：
   - 基本信息
   - 健康与健身目标
   - 新闻关注领域
   - 个人偏好

4. **配置API密钥（可选）**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入 API 密钥
   ```

5. **在 Claude Code 中打开项目**
   ```bash
   claude-code .
   ```

### 3. 开始使用

- 输入 `/早上好` - 获取今日新闻
- 输入 `/自律` - 记录体重，获取健康建议
- 输入 `/今工作结束了` - 进行工作反思

详细使用方法参考 [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)

## 项目结构

```
ClaudeCode_Secretary/
├── .claude/
│   └── commands/           # 触发命令定义
│       ├── 早上好.md
│       ├── 自律.md
│       └── 今工作结束了.md
├── agents/                 # Agent 提示词
│   ├── news_agent_prompt.md
│   ├── coach_agent_prompt.md
│   └── reflection_agent_prompt.md
├── config/                 # 配置文件
│   ├── agent_config.json
│   └── feishu_config.json
├── context/                # 个人数据（不提交到git）
│   ├── about_me.md
│   ├── health_history.md
│   ├── insights.md
│   └── preferences.md
├── daily_records/          # 每日记录（不提交到git）
│   └── YYYY-MM-DD/
│       ├── 今日新闻.md
│       ├── 健康.md
│       └── 反思.md
├── docs/                   # 文档
│   ├── MCP_SETUP.md       # MCP 配置指南
│   └── USER_GUIDE.md      # 使用手册
├── templates/              # 文档模板
│   ├── news_template.md
│   ├── health_template.md
│   └── reflection_template.md
├── .env.example            # 环境变量模板
├── .gitignore
├── CLAUDE.md               # Claude Code 项目说明
└── README.md
```

## 文档

- [MCP 配置指南](docs/MCP_SETUP.md) - 如何配置必需的 MCP 服务器
- [用户指南](docs/USER_GUIDE.md) - 详细使用说明和最佳实践
- [项目构想](构想.md) - 项目设计理念和实现细节

## 技术栈

- **AI 框架**: Claude Code + MCP (Model Context Protocol)
- **MCP 服务器**:
  - `@modelcontextprotocol/server-filesystem` - 文件操作
  - `@modelcontextprotocol/server-fetch` - 网络请求
  - `@modelcontextprotocol/server-brave-search` - 新闻搜索
  - `@modelcontextprotocol/server-memory` - 对话记忆
- **外部集成**: 飞书开放平台 API（可选）

## 特色功能

### 个性化定制
- 所有 Agent 根据你的个人档案提供定制化服务
- 可自定义关注领域、健康目标、对话模式

### 数据本地化
- 所有个人数据存储在本地
- 完全掌控自己的隐私数据
- 支持手动备份和迁移

### 持续记忆
- 体重变化趋势追踪
- 工作模式和洞察积累
- 长期行为模式识别

### 灵活扩展
- 基于 MCP 的模块化架构
- 易于添加新的 Agent 或功能
- 支持自定义提示词和配置

## 安全与隐私

- ✅ 所有个人数据本地存储
- ✅ `.gitignore` 排除敏感文件
- ✅ API 密钥环境变量管理
- ✅ 可选的外部服务集成
- ✅ 完全控制数据访问权限

## 常见问题

**Q: 需要付费吗？**
A: Claude Code 本身免费，但 Brave Search API 和飞书推送等可选功能可能需要 API 密钥。

**Q: 数据存在哪里？**
A: 所有数据存储在本地项目文件夹中，不上传云端。

**Q: 能在移动设备上使用吗？**
A: 目前需要在支持 Claude Desktop 的桌面设备上使用。

**Q: 可以添加新的 Agent 吗？**
A: 当然！参考现有 Agent 的结构，创建新的提示词和触发命令即可。

更多问题参考 [用户指南](docs/USER_GUIDE.md)

## 贡献

这是一个个人项目，但欢迎 Fork 和定制！

如果你有好的想法或改进建议，欢迎提交 Issue 或 Pull Request。

## 许可证

MIT License - 自由使用和修改

## 致谢

- 感谢 [Anthropic](https://anthropic.com) 提供的 Claude AI
- 感谢 [Model Context Protocol](https://modelcontextprotocol.io) 提供的扩展框架

---

**开始你的AI助理之旅吧！** 输入 `/早上好` 试试看 ☀️
