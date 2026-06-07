## 🤖 AI 前沿新闻日报系统

自动化收集并发送 AI 领域最新新闻，每天 09:00 发送至您的邮箱。

### 📋 功能特性

- ✅ 每天自动收集 20 条 AI 前沿新闻
- ✅ 按类别分类（大模型、场景动态等）
- ✅ 每日 09:00 自动发送至指定邮箱
- ✅ 精美的 HTML 邮件格式
- ✅ 支持多个新闻源（Hacker News、RSS Feeds 等）

### 📰 新闻类别

1. **大模型** - 语言模型、LLM、GPT、Claude 等相关动态
2. **场景动态** - 应用案例、产品发布、融资新闻、行业动态等

### 🚀 快速开始

#### 1. 配置 Gmail 应用密码

由于 Gmail 安全限制，需要使用应用密码而不是账户密码：

1. 访问 [Google 账户安全页面](https://myaccount.google.com/security)
2. 启用两步验证（如果未启用）
3. 在安全页面找到"应用密码"
4. 为"邮件"应用和"Windows 电脑"生成应用密码
5. 复制生成的 16 位密码

#### 2. 配置 GitHub Secrets

在仓库的 **Settings → Secrets and variables → Actions** 中添加以下密钥：

| 密钥名称 | 说明 | 示例 |
|---------|------|------|
| `SENDER_EMAIL` | 你的 Gmail 地址 | `your-email@gmail.com` |
| `SENDER_PASSWORD` | Gmail 应用密码（16 位） | `xxxx xxxx xxxx xxxx` |
| `RECIPIENT_EMAIL` | 接收邮件的地址 | `chenxw823@gmail.com` |

**添加方法：**
```
Settings → Secrets and variables → Actions → New repository secret
```

#### 3. 验证配置

访问仓库的 **Actions** 标签，可以看到工作流：
- 每天 UTC 01:00（北京时间 09:00）自动运行
- 点击 **"Run workflow"** 可手动测试

### 📁 项目结构

```
News/
├── news_collector.py          # 新闻收集脚本
├── email_sender.py            # 邮件发送脚本
├── requirements.txt           # Python 依赖
├── .github/workflows/
│   └── daily-news.yml         # GitHub Actions 工作流
├── news_data.json             # 当天收集的新闻数据
└── README.md                  # 本文件
```

### 🔧 工作流程

1. **news_collector.py** - 从多个源收集新闻
   - 爬取 Hacker News 热点
   - 解析 RSS 源
   - 自动分类和去重

2. **email_sender.py** - 格式化并发送邮件
   - 按类别组织内容
   - 生成精美的 HTML 邮件
   - 通过 Gmail 发送

3. **.github/workflows/daily-news.yml** - 自动化工作流
   - 每天 09:00 触发
   - 执行收集和发送
   - 保存数据到仓库

### 📊 邮件格式示例

```
🤖 AI 前沿新闻日报 - 2026-06-07

📌 大模型 (10 条)
  1. ChatGPT 新功能发布...
  2. Claude 3.5 性能提升...
  ...

📌 场景动态 (10 条)
  1. OpenAI 获得新融资...
  2. AI 创业公司 A 轮融资...
  ...
```

### 🔍 新闻来源

- **Hacker News** - 技术社区热点
- **RSS Feeds** - Bloomberg、TechCrunch、Ars Technica
- **其他** - 可自行扩展

### ⚙️ 自定义配置

修改 `news_collector.py` 中的配置：

```python
self.categories = {
    '大模型': ['GPT', 'Claude', 'LLaMA', ...],
    '场景动态': ['应用', '产品', '融资', ...],
    # 可添加更多类别
}
```

### 🐛 故障排查

**邮件未收到？**
1. 检查 GitHub Actions 的工作流日志
2. 确认应用密码正确（16 位，空格不计）
3. 确保启用了 Gmail 两步验证
4. 查看垃圾邮件文件夹

**新闻数量少于 20 条？**
- 可能是网络问题或数据源暂时无法访问
- 检查仓库的 artifacts 中是否有 news_data.json

### 📝 更新日志

**v1.0** (2026-06-07)
- ✅ 初始版本发布
- ✅ 支持大模型和场景动态分类
- ✅ 自动化每日 09:00 发送

### 📄 许可证

MIT License

### 💡 建议

- 定期检查邮件接收情况
- 可以通过调整代码添加更多新闻源
- 支持修改发送时间和接收邮箱
- 欢迎提交 Issue 和 PR

---

**有问题？** 查看 GitHub Issues 或提交反馈！
