#!/usr/bin/env python3
"""ClipAI - AI-powered clipboard assistant for macOS menu bar."""

import rumps
import pyperclip
import threading
import json
import urllib.request
import urllib.error
import subprocess
import os
import tempfile
import base64
import io
from PIL import Image, ImageDraw, ImageFont
from Foundation import NSBlockOperation, NSOperationQueue

# ── Configuration ────────────────────────────────────────────────────────────

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"  # V4 Flash

KEYCHAIN_ACCOUNT = "ClipAI"
KEYCHAIN_SERVICE = "com.clipai.apikey"


# ── Keychain helpers ─────────────────────────────────────────────────────────

def get_api_key():
    r = subprocess.run(
        ["security", "find-generic-password", "-a", KEYCHAIN_ACCOUNT,
         "-s", KEYCHAIN_SERVICE, "-w"],
        capture_output=True, text=True, timeout=5,
    )
    return r.stdout.strip() if r.returncode == 0 else None


def store_api_key(key):
    subprocess.run(
        ["security", "delete-generic-password", "-a", KEYCHAIN_ACCOUNT,
         "-s", KEYCHAIN_SERVICE],
        capture_output=True, text=True, timeout=5,
    )
    r = subprocess.run(
        ["security", "add-generic-password", "-a", KEYCHAIN_ACCOUNT,
         "-s", KEYCHAIN_SERVICE, "-w", key, "-U"],
        capture_output=True, text=True, timeout=5,
    )
    return r.returncode == 0


def delete_api_key():
    subprocess.run(
        ["security", "delete-generic-password", "-a", KEYCHAIN_ACCOUNT,
         "-s", KEYCHAIN_SERVICE],
        capture_output=True, text=True, timeout=5,
    )


# ── Icon generation ──────────────────────────────────────────────────────────

def _create_icon_path():
    """Generate a simple clipboard icon as PNG, return its path."""
    size = 32
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a simple clipboard shape
    # Outer rectangle (clipboard body)
    draw.rectangle([4, 6, 27, 29], fill=(100, 140, 255, 255),
                   outline=(60, 100, 220, 255), width=2)
    # Top bar (clip)
    draw.rectangle([10, 2, 21, 8], fill=(100, 140, 255, 255))
    # Inner lines (text on clipboard)
    for y in [14, 18, 22]:
        draw.rectangle([8, y, 23, y + 1], fill=(220, 230, 255, 255))
    # Letter "A" icon
    draw.text((11, 12), "AI", fill=(255, 255, 255, 255))

    path = os.path.join(tempfile.gettempdir(), "clipai_icon.png")
    img.save(path, "PNG")
    return path


def _generate_banner_icon():
    """Generate a larger 1024x1024 banner icon for the repo."""
    size = 1024
    img = Image.new("RGBA", (size, size), (30, 40, 80, 255))
    draw = ImageDraw.Draw(img)

    # Clipboard body
    margin = 200
    draw.rounded_rectangle(
        [margin, margin + 80, size - margin, size - margin],
        radius=60, fill=(60, 100, 220, 255), outline=(100, 140, 255, 255), width=8
    )
    # Clip at top
    clip_top = margin - 30
    draw.rounded_rectangle(
        [margin + 100, clip_top, size - margin - 100, margin + 80],
        radius=30, fill=(60, 100, 220, 255)
    )

    # Text lines
    line_y_start = margin + 180
    for i in range(4):
        y = line_y_start + i * 80
        w = 80 + (3 - i) * 60
        draw.rectangle([margin + 100, y, size - margin - 100 - w, y + 12],
                       fill=(180, 210, 255, 255))

    # AI badge
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except (OSError, IOError):
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((margin + 60, margin + 120), "AI", fill=(255, 255, 255, 255),
              font=font_large)

    # Bottom text
    draw.text((margin, size - margin - 180), "ClipAI",
              fill=(200, 220, 255, 255), font=font_small)

    path = os.path.join(tempfile.gettempdir(), "clipai_banner.png")
    img.save(path, "PNG")
    return path


# ── Thread-safe UI helper ────────────────────────────────────────────────────

def main_thread(fn):
    op = NSBlockOperation.alloc().init()
    op.addExecutionBlock_(fn)
    NSOperationQueue.mainQueue().addOperation_(op)


# ── Main App ─────────────────────────────────────────────────────────────────

class ClipAI(rumps.App):
    def __init__(self):
        self.icon_path = _create_icon_path()
        super().__init__("📋", icon=self.icon_path, template=False)
        self.build_menu()

    def build_menu(self):
        self.menu.clear()
        self.menu.add(rumps.MenuItem("🌍 翻译为中文", callback=self.action_translate))
        self.menu.add(rumps.MenuItem("✍️ 润色文本", callback=self.action_rewrite))
        self.menu.add(rumps.MenuItem("📝 总结要点", callback=self.action_summarize))
        self.menu.add(rumps.MenuItem("💻 解释代码", callback=self.action_explain))
        self.menu.add(rumps.MenuItem("🤖 自由提问", callback=self.action_ask))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("⚙️ 设置 API Key", callback=self.action_settings))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("❌ 退出", callback=rumps.quit_application))

    # ── Actions ──────────────────────────────────────────────────────────

    def action_translate(self, _):
        text = pyperclip.paste()
        if not text.strip():
            rumps.notification("ClipAI", "⚠️ 剪贴板为空", "请先复制文本 (Cmd+C)")
            return
        threading.Thread(target=self._translate, args=(text,), daemon=True).start()

    def action_rewrite(self, _):
        text = pyperclip.paste()
        if not text.strip():
            rumps.notification("ClipAI", "⚠️ 剪贴板为空", "请先复制文本 (Cmd+C)")
            return
        threading.Thread(target=self._rewrite, args=(text,), daemon=True).start()

    def action_summarize(self, _):
        text = pyperclip.paste()
        if not text.strip():
            rumps.notification("ClipAI", "⚠️ 剪贴板为空", "请先复制文本 (Cmd+C)")
            return
        threading.Thread(target=self._summarize, args=(text,), daemon=True).start()

    def action_explain(self, _):
        text = pyperclip.paste()
        if not text.strip():
            rumps.notification("ClipAI", "⚠️ 剪贴板为空", "请先复制代码 (Cmd+C)")
            return
        threading.Thread(target=self._explain, args=(text,), daemon=True).start()

    def action_ask(self, _):
        """Free-form question about clipboard content."""
        text = pyperclip.paste()
        if not text.strip():
            rumps.notification("ClipAI", "⚠️ 剪贴板为空", "请先复制文本 (Cmd+C)")
            return
        win = rumps.Window(
            title="🤖 自由提问",
            message=f"基于以下内容提问：\n\n{text[:200]}{'...' if len(text) > 200 else ''}",
            default_text="",
            ok="发送",
            cancel="取消",
        )
        r = win.run()
        if r.clicked == 1 and r.text.strip():
            threading.Thread(target=self._ask, args=(text, r.text.strip()),
                             daemon=True).start()

    def action_settings(self, _):
        """Open settings dialog to set/change API key."""
        current_key = get_api_key()
        if current_key:
            masked = current_key[:10] + "..." + current_key[-4:]
            msg = f"当前 Key: {masked}\n\n输入新 Key 替换，或留空删除："
        else:
            msg = "未设置 API Key\n\n请输入 DeepSeek API Key："

        win = rumps.Window(
            title="⚙️ ClipAI 设置",
            message=msg,
            default_text="",
            ok="保存",
            cancel="取消",
        )
        r = win.run()
        if r.clicked == 1:
            if r.text.strip():
                store_api_key(r.text.strip())
                rumps.notification("ClipAI", "✅ Key 已保存",
                                   "API Key 已安全存储在 macOS Keychain")
            elif current_key:
                delete_api_key()
                rumps.notification("ClipAI", "🗑️ Key 已删除", "")
            else:
                rumps.notification("ClipAI", "ℹ️ 未更改", "")

    # ── AI helpers ───────────────────────────────────────────────────────

    def _call_deepseek(self, prompt, system_msg="You are a helpful assistant."):
        api_key = get_api_key()
        if not api_key:
            main_thread(lambda: rumps.notification(
                "ClipAI", "⚠️ 未设置 API Key",
                "请点击菜单 → 设置 API Key，然后输入你的 DeepSeek API Key"))
            return None

        data = json.dumps({
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 4096,
        }).encode()

        req = urllib.request.Request(
            DEEPSEEK_API_URL,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            return f"⚠️ API 错误 ({e.code}): {body[:300]}"
        except json.JSONDecodeError:
            return "⚠️ API 返回格式错误"
        except Exception as e:
            return f"⚠️ 网络错误: {str(e)[:200]}"

    def _show_result(self, title, content):
        main_thread(lambda: self._do_show_result(title, content))

    def _do_show_result(self, title, content):
        win = rumps.Window(
            title=title,
            message=content[:8000],
            default_text="",
            ok="📋 复制结果",
            cancel="关闭",
        )
        r = win.run()
        if r.clicked == 1:
            pyperclip.copy(content)
            rumps.notification("ClipAI", "✅ 已复制到剪贴板", "")

    # ── Workers ──────────────────────────────────────────────────────────

    def _translate(self, text):
        main_thread(lambda: rumps.notification("ClipAI", "🌍 翻译中...", text[:60]))
        result = self._call_deepseek(
            f"请将以下文本翻译成中文。直接返回翻译结果，不要附加解释：\n\n{text}",
            "You are a professional translator. Translate text to Chinese accurately and naturally."
        )
        if result:
            self._show_result("🌍 翻译结果", result)

    def _rewrite(self, text):
        main_thread(lambda: rumps.notification("ClipAI", "✍️ 润色中...", text[:60]))
        result = self._call_deepseek(
            f"请润色以下文本，使其更通顺、专业，保持原意。直接返回润色结果：\n\n{text}",
            "You are a professional editor. Polish text to be more fluent and professional."
        )
        if result:
            self._show_result("✍️ 润色结果", result)

    def _summarize(self, text):
        main_thread(lambda: rumps.notification("ClipAI", "📝 总结中...", text[:60]))
        result = self._call_deepseek(
            f"请用中文总结以下内容的核 心要点，要求简洁扼要：\n\n{text}",
            "You are a professional summarizer. Provide concise key points in Chinese."
        )
        if result:
            self._show_result("📝 总结结果", result)

    def _explain(self, text):
        main_thread(lambda: rumps.notification("ClipAI", "💻 分析代码中...", text[:60]))
        result = self._call_deepseek(
            f"请解释以下代码的功能、原理和关键逻辑：\n\n{text}",
            "You are an expert programmer. Explain code clearly with key concepts and logic."
        )
        if result:
            self._show_result("💻 代码解释", result)

    def _ask(self, context, question):
        main_thread(lambda: rumps.notification("ClipAI", "🤖 思考中...", question[:60]))
        result = self._call_deepseek(
            f"以下是我的参考内容：\n{context}\n\n我的问题是：{question}\n\n请基于参考内容回答。",
            "You are a helpful AI assistant. Answer based on the provided context."
        )
        if result:
            self._show_result("🤖 AI 回答", result)


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = ClipAI()
    app.run()
