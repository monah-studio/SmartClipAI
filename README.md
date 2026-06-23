

<div align="center">

# ClipAI 🤖

**AI-powered clipboard assistant for macOS — translate, rewrite, summarize, explain code, all from your menu bar.**

*ClipAI 是一款 AI 增强的 macOS 剪贴板助手，菜单栏即可完成翻译、润色、总结和代码解释。*

[![GitHub stars](https://img.shields.io/github/stars/timwynter/ClipAI?style=social)](https://github.com/timwynter/ClipAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![macOS](https://img.shields.io/badge/platform-macOS-blue.svg)](https://github.com/timwynter/ClipAI)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)

</div>

https://github.com/user-attachments/assets/banner.png

---

## ✨ Features

| Action | What it does |
|--------|-------------|
| 🌍 **Translate** | Translate any text to Chinese instantly |
| ✍️ **Rewrite** | Polish rough text to be professional and fluent |
| 📝 **Summarize** | Get a concise summary of long articles |
| 💻 **Explain Code** | Paste any code and get a clear explanation |
| 🤖 **Ask Anything** | Free-form questions about your clipboard content |

## 🚀 Quick Start

### 1. Install

```bash
# Clone the repo
git clone https://github.com/timwynter/ClipAI.git
cd ClipAI

# Install dependencies
pip install -r requirements.txt

# Run ClipAI
python src/clipai.py
```

### 2. Add your API key

Click the 📋 icon in your menu bar → **Settings** → paste your DeepSeek API key.

> 💡 Get a DeepSeek API key at [platform.deepseek.com](https://platform.deepseek.com) — it's very cheap (~¥1/1M input tokens).

### 3. Use it

1. **Copy any text** (Cmd+C) from any app
2. **Click the 📋 icon** in your menu bar
3. **Choose an action**: Translate, Rewrite, Summarize, Explain Code, or Ask
4. **Get your result** in a popup window — click "Copy" to save it

---

## 📸 Demo

| Action | Preview |
|--------|---------|
| 🌍 Translate | English → Chinese in one click |
| ✍️ Rewrite | Messy notes → professional text |
| 📝 Summarize | Long article → TL;DR |
| 💻 Explain Code | Any code → clear explanation |

---

## 🔧 How It Works

ClipAI is a lightweight macOS menu bar app built with:

- **[rumps](https://github.com/jaredks/rumps)** — Python framework for macOS menu bar apps
- **[pyperclip](https://github.com/asweigart/pyperclip)** — Cross-platform clipboard access
- **[DeepSeek V4 Flash API](https://platform.deepseek.com)** — Fast, affordable AI processing (~¥1/1M tokens)
- **[pyobjc](https://github.com/ronaldoussoren/pyobjc)** — macOS native API bindings

Your API key is stored securely in **macOS Keychain** — never in plain text.

### Architecture

```
┌─────────────────────────────────────┐
│           Menu Bar Icon 📋          │
├─────────────────────────────────────┤
│  User copies text (Cmd+C) anywhere  │
│         ↓                           │
│  Clicks icon → selects action       │
│         ↓                           │
│  pyperclip reads clipboard          │
│         ↓                           │
│  DeepSeek API processes text        │
│         ↓                           │
│  Result shown in popup window       │
│  One more click → copy to clipboard │
└─────────────────────────────────────┘
```

---

## 🎯 Use Cases

- **Students** — Translate research papers, summarize articles
- **Developers** — Explain code snippets, format docs
- **Writers** — Polish drafts, translate content
- **Everyone** — Quick AI assistance without leaving your workflow

---

## 📦 Package as .app

```bash
make build
```

Then drag `dist/ClipAI.app` to your Applications folder. Requires rumps + pyobjc installed.

---

## 🧠 Part of "30 macOS Apps in 30 Days"

This is Day 1 of the **30 macOS Apps in 30 Days** challenge. Follow the journey:

- GitHub: [@timwynter](https://github.com/timwynter)
- Stay tuned for Day 2!

---

## 🤝 Contributing

PRs welcome! Ideas for new actions:

- 🎨 Format JSON/XML/code
- 🔍 Grammar check
- 🌐 Translate to multiple languages
- 📧 Write email replies
- 🖼️ OCR image text

---

## 📄 License

MIT

---

<div align="center">
  
**⭐ If you find this useful, give it a star!**

</div>
