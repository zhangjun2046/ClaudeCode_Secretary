# MCP 服务器配置指南

本文档说明如何为 ClaudeCode_Secretary 项目配置必需的 MCP (Model Context Protocol) 服务器。

## 什么是 MCP？

MCP (Model Context Protocol) 是一种让 AI 助手能够访问外部工具和数据源的协议。通过 MCP 服务器，Claude 可以执行文件操作、网络搜索、API调用等功能。

## 必需的 MCP 服务器

### 1. MCP Filesystem ⭐ 必需

**用途**: 所有 Agent 读写文件和文件夹

**功能**:
- 创建和读取文件
- 创建日期文件夹
- 更新上下文文件
- 生成每日记录

**配置步骤**:

1. 打开 Claude Desktop 配置文件：
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. 添加 Filesystem 服务器配置：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:/coding/ClaudeCode_Secretary"
      ]
    }
  }
}
```

3. 重启 Claude Desktop

**验证**: 在 Claude Code 中运行 `/mcp list` 查看是否加载成功

---

### 2. MCP Fetch ⭐ 必需

**用途**: 新闻张搜索网络新闻

**功能**:
- HTTP 请求
- 网页抓取
- API 调用

**配置步骤**:

在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ]
    }
  }
}
```

**注意**: Fetch 服务器有一些安全限制，只能访问允许的域名。

---

### 3. MCP Brave Search 🔸 推荐

**用途**: 新闻张的新闻搜索（比通用 fetch 更准确）

**功能**:
- 结构化搜索结果
- 新闻聚合
- 实时资讯

**配置步骤**:

1. 获取 Brave Search API 密钥：
   - 访问 https://brave.com/search/api/
   - 注册并获取 API 密钥（免费版每月 2000 次查询）

2. 配置 MCP 服务器：

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY_HERE"
      }
    }
  }
}
```

3. 或者在 `.env` 文件中配置：

```bash
BRAVE_SEARCH_API_KEY=your_brave_api_key_here
```

---

### 4. MCP Memory 🔸 推荐

**用途**: 保持对话状态，特别是反思张的多轮对话

**功能**:
- 会话记忆
- 上下文保持
- 对话历史追踪

**配置步骤**:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    }
  }
}
```

---

### 5. 自定义 Feishu MCP ⭐ 必需（需开发）

**用途**: 发送飞书消息

**功能**:
- 调用飞书开放平台 API
- 发送新闻简报
- 发送健康提醒

**实现方式**:

#### 选项 A: 使用飞书 Webhook（简单）

1. 在飞书群组中创建自定义机器人
2. 获取 Webhook URL
3. 在 `config/feishu_config.json` 中配置

```json
{
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
}
```

#### 选项 B: 开发自定义 MCP 服务器（完整功能）

1. 创建 `mcp-servers/feishu/` 目录
2. 实现飞书 API 调用逻辑
3. 在配置中引用

参考文档：
- 飞书开放平台: https://open.feishu.cn/
- MCP 开发指南: https://docs.anthropic.com/mcp

---

### 6. MCP Time 🔹 可选

**用途**: 准确的日期时间处理

**功能**:
- 获取当前时间
- 日期格式化
- 时区转换

**配置步骤**:

```json
{
  "mcpServers": {
    "time": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-time"
      ]
    }
  }
}
```

---

## 完整配置示例

将所有 MCP 服务器整合到 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:/coding/ClaudeCode_Secretary"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "your_brave_api_key_here"
      }
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "time": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-time"
      ]
    }
  }
}
```

---

## 验证配置

配置完成后，验证 MCP 服务器是否正常工作：

1. **重启 Claude Desktop**

2. **检查 MCP 服务器列表**:
   在 Claude Code 中运行：
   ```
   列出所有可用的 MCP 工具
   ```

3. **测试文件操作**:
   ```
   读取 context/about_me.md 文件
   ```

4. **测试网络搜索**:
   ```
   搜索最新的 AI 新闻
   ```

---

## 故障排查

### 问题 1: MCP 服务器未加载

**症状**: 运行 Agent 命令时提示无法访问文件或网络

**解决方法**:
1. 检查 `claude_desktop_config.json` 语法是否正确（JSON格式）
2. 确认路径使用正斜杠 `/` 或双反斜杠 `\\`
3. 重启 Claude Desktop
4. 查看 Claude Desktop 日志（Help → View Logs）

### 问题 2: Brave Search API 配额用完

**症状**: 新闻搜索失败

**解决方法**:
1. 检查 API 使用量：https://brave.com/search/api/dashboard
2. 升级到付费计划或等待下月配额重置
3. 临时使用通用 WebFetch 工具

### 问题 3: 飞书推送失败

**症状**: 文件生成成功，但未收到飞书通知

**解决方法**:
1. 检查 `config/feishu_config.json` 中的 `enabled` 是否为 `true`
2. 验证 Webhook URL 是否有效
3. 检查飞书机器人是否被禁用
4. 查看错误日志

### 问题 4: Windows 路径问题

**症状**: 文件操作失败，提示路径不存在

**解决方法**:
在配置中使用：
- 正斜杠: `"D:/coding/ClaudeCode_Secretary"`
- 或双反斜杠: `"D:\\coding\\ClaudeCode_Secretary"`

不要使用单反斜杠 `\`，它在 JSON 中是转义字符。

---

## 安全注意事项

1. **API 密钥保护**:
   - 不要将 API 密钥提交到 Git
   - 使用 `.env` 文件存储敏感信息
   - `.env` 已在 `.gitignore` 中排除

2. **文件系统权限**:
   - MCP Filesystem 只能访问配置的目录
   - 不要给予过大的权限范围

3. **网络请求限制**:
   - 注意 API 调用频率限制
   - 避免泄露个人数据到公共 API

---

## 下一步

配置完成后，可以开始测试 Agent：

1. **测试新闻张**: 输入 `/早上好`
2. **测试教练张**: 输入 `/自律`
3. **测试反思张**: 输入 `/今工作结束了`

详细使用说明请参考 `docs/USER_GUIDE.md`

---

**最后更新**: 2025-10-17
**维护者**: ClaudeCode_Secretary 项目组
