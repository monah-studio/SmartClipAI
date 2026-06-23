

<div align="center">

# SmartClipAI 🤖

**AI 增强的 macOS 剪贴板助手 — 菜单栏一键翻译、润色、总结、解释代码。**

*SmartClipAI is an AI-powered clipboard assistant for macOS — translate, rewrite, summarize, explain code, all from your menu bar.*

[![GitHub stars](https://img.shields.io/github/stars/Monah-Limited/SmartClipAI?style=social)](https://github.com/Monah-Limited/SmartClipAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![macOS](https://img.shields.io/badge/platform-macOS-blue.svg)](https://github.com/Monah-Limited/SmartClipAI)

</div>

https://github.com/user-attachments/assets/banner.png

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 🌍 **翻译** | 选中文本一键翻译为中文 |
| ✍️ **润色** | 让粗糙的文字变得通顺专业 |
| 📝 **总结** | 长文章秒变核心要点 |
| 💻 **解释代码** | 粘贴任何代码，获得清晰解释 |
| 🤖 **自由提问** | 基于剪贴板内容任意提问 |

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/Monah-Limited/SmartClipAI.git
cd SmartClipAI

# 安装依赖
pip install -r requirements.txt

# 运行 SmartClipAI
python src/smartclipai.py
```

### 2. 添加 API Key

点击菜单栏 📋 图标 → **设置** → 粘贴你的 DeepSeek API Key。

> 💡 在 [platform.deepseek.com](https://platform.deepseek.com) 获取 API Key，价格极低（约 ¥1/百万 tokens）。

### 3. 使用

1. **复制文本**（Cmd+C）— 从任何应用中复制
2. **点击菜单栏 📋 图标**
3. **选择操作**：翻译、润色、总结、解释代码或自由提问
4. **获取结果** — 弹出窗口显示，点击"复制"保存

---

## 📸 演示效果

| 操作 | 效果 |
|------|------|
| 🌍 翻译 | 英文 → 中文，一键完成 |
| ✍️ 润色 | 零碎笔记 → 专业文案 |
| 📝 总结 | 长文 → 核心要点 |
| 💻 解释代码 | 任何代码 → 清晰解释 |

---

## 🔧 工作原理

SmartClipAI 是一个轻量级的 macOS 菜单栏应用，基于：

- **[rumps](https://github.com/jaredks/rumps)** — macOS 菜单栏应用 Python 框架
- **[pyperclip](https://github.com/asweigart/pyperclip)** — 跨平台剪贴板访问
- **[DeepSeek V4 Flash API](https://platform.deepseek.com)** — 快速、便宜的 AI 处理（约 ¥1/百万 tokens）
- **[pyobjc](https://github.com/ronaldoussoren/pyobjc)** — macOS 原生 API 绑定

API Key 安全存储在 **macOS Keychain** 中，不会明文保存。

---

## 🎯 适用场景

- **学生** — 翻译论文、总结文章
- **开发者** — 解释代码片段、格式化文档
- **写作者** — 润色草稿、翻译内容
- **所有人** — 不离开当前工作流，快速获得 AI 帮助

---

## 🧠 "30 天 30 个 macOS 应用" Day 1

这是 **30 macOS Apps in 30 Days** 挑战的第一天。关注旅程：

- GitHub: [@timwynter](https://github.com/timwynter)
- 明天见 Day 2！

---

## 🤝 贡献指南

欢迎 PR！可以添加的新功能：

- 🎨 格式化 JSON/XML/代码
- 🔍 语法检查
- 🌐 多语言翻译
- 📧 写邮件回复
- 🖼️ OCR 图片文字识别

---

## 📄 许可证

MIT

---

<div align="center">
  
**⭐ 如果对你有帮助，点个 Star！**

</div>
