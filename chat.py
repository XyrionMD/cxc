import requests, os, base64, sys, io
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer, Center
from textual.widgets import Header, Footer, Input, Static, Markdown, LoadingIndicator
from textual.binding import Binding
from textual.screen import ModalScreen

from config_loader import load_config, set_conf, debug_mode
from contextlib import redirect_stdout

CVT = load_config()
style = CVT.LOADING_STYLES

API_KEY = f"{CVT.API}"
MODEL_AI = f"{CVT.MODEL}"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_AI}:generateContent"

history = []

class HelpScreen(ModalScreen):
    BINDINGS = [
        ("escape", "dismiss", "Close"),
    ]

    def compose(self):
        yield Static(
            """[ HELP ]

quit         : Go out 
/file        : Send Media To Ai

Example

- /file <path> <prompt>

- /file ~/photo.png Look at this.

Press ESC to close
""",
            id="help",
            )

    def action_dismiss(self):
        self.dismiss()


class ChatBubble(Markdown):
    pass

class CodeX(App):
                                            
    CSS = """
    Screen {
        background: #1a1a1a;
    }
    Header {
        background: #333333;
        color: #cccccc;
    }
    Footer {
        background: #333333;
        color: #999999;
    }
    #chat-area {
        background: #1a1a1a;
        padding: 1;
    }
    Input {
        background: #2a2a2a;
        color: #cccccc;
        border: none;
        dock: bottom;
        margin: 0 1 1 1;
    }
    Input:focus {
        border: none;
    }
    .user-row {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    .ai-row {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    .user-bubble {
        background: #3a3a3a;
        color: #cccccc;
        padding: 1 2;
        max-width: 70%;
        width: auto;
    }
    .ai-bubble {
        background: #2e2e2e;
        color: #dddddd;
        padding: 1 2;
        max-width: 70%;
        width: auto;
    }

    HelpScreen {
        align: center middle;
    }

    #help {
        width: 60;
        border: round green;
        padding: 1 2;
        background: $surface;
    }
    

    #esc {
        width: 100%;
        text-align: center;
    }

    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+H", "help", "Help", priority=True),
    ]

    def _handle_exception(self, error: Exception) -> None:
        if (CVT.DEBUG) == True:
            buf = io.StringIO()
            with redirect_stdout(buf):
                debug_mode(type(error), ":", error)
            self.exit(message=buf.getvalue().strip())
        else:
            self.exit(message="Debug mode is disabled. Enable it in the config file if needed.")

    def compose(self):
        yield Header(name="CodeX Core", classes="header")
        with ScrollableContainer(id="chat-area"):
            pass
        yield Input(placeholder="Type a message ...", id="input-box")
        yield Footer()

    def on_mount(self) -> None:
        self.theme = getattr(CVT, "THEME", "catppuccin-mocha")
        self.query_one("#input-box", Input).focus()

    def watch_theme(self, new_theme: str) -> None:
        set_conf("THEME", new_theme)

    def show_typing(self):
        chat = self.query_one("#chat-area", ScrollableContainer)
        col = Vertical(id="typing-indicator")
        col.styles.height = 2
        col.styles.width = "100%"
        lbl = Static(f"{CVT.AI_NAME} is typing...")
        lbl.styles.color = "#777777"
        loader = Static("•")
        loader.styles.color = "#888888"
        dots = [f"[{style}___]", f"[{style}{style}__]", f"[{style}{style}{style}_]", f"[{style}{style}{style}{style}]"]
        loader.set_interval(0.3, lambda: loader.update(dots[int(__import__("time").time() * 3) % 4]))
        chat.mount(col)
        col.mount(lbl)
        col.mount(loader)
                                                                                                        

    def hide_typing(self):
        try:
            self.query_one("#typing-indicator").remove()
        except Exception:
            pass

    def on_input_submitted(self, event: Input.Submitted):
        msg = event.value.strip()
        if not msg:
            return
        if msg.lower() == "quit":
            self.exit()
            return


        elif msg.lower() == "help":
            self.push_screen(HelpScreen())
            event.input.value = ""
            event.input.focus()
            return

        elif msg.lower().startswith("/file "):
            parts = msg.split(" ", 2)
            file_path = os.path.expanduser(parts[1]) if len(parts) > 1 else ""
            prompt = parts[2] if len(parts) > 2 else "Analyze this file."

            if not os.path.isfile(file_path):
                self.add_ai_msg(f"File not found: `{file_path}`")
                self.query_one("#input-box", Input).value = ""
                return

            ext = os.path.splitext(file_path)[1].lower()
            mime_types = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
            }

            if ext in mime_types:
                with open(file_path, "rb") as f:
                    b64_data = base64.b64encode(f.read()).decode("utf-8")
                ai_parts = [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_types[ext],
                            "data": b64_data
                        }
                    }
                ]
                self.add_user_msg(f"🖼️ **{file_path}**\n\n{prompt}")
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                full_msg = f"{prompt}\n\n--- File: {file_path} ---\n{file_content}"
                ai_parts = [{"text": full_msg}]
                self.add_user_msg(f"📄 **{file_path}**\n\n{prompt}")

            self.query_one("#input-box", Input).value = ""
            self.run_worker(lambda: self.get_ai_response(ai_parts), name="ai_request", thread=True)
            return

        self.add_user_msg(msg)
        self.query_one("#input-box", Input).value = ""
        self.show_typing()
        self.run_worker(lambda: self.get_ai_response([{"text": msg}]), name="ai_request", thread=True)
                                
        

    def add_user_msg(self, text):
        chat = self.query_one("#chat-area", ScrollableContainer)
        row = Horizontal(classes="user-row")
        row.styles.width = "100%"
        row.styles.height = "auto"
        row.styles.align_horizontal = "right"
        chat.mount(row)
        bubble = ChatBubble(text, classes="user-bubble")
        bubble.styles.margin = (0, 0, 0, 1)
        row.mount(bubble)
        chat.scroll_end()

    def add_ai_msg(self, text):
        self.hide_typing()
        chat = self.query_one("#chat-area", ScrollableContainer)
        col = Vertical(classes="ai-row")
        col.styles.width = "100%"
        col.styles.height = "auto"
        chat.mount(col)
        name_label = Static(CVT.AI_NAME)
        name_label.styles.margin = (0, 0, 0, 0)
        name_label.styles.color = "#777777"
        col.mount(name_label)
        bubble = ChatBubble(text, classes="ai-bubble")
        bubble.styles.margin = (0, 1, 0, 0)
        col.mount(bubble)
        chat.scroll_end()

    def get_ai_response(self, parts):
        history.append({
            "role": "user",
            "parts": parts
        })
        SYS_PROMPT = f"{CVT.AI_PROMPT}"
        payload = {
            "system_instruction": {
                "parts": [{"text": SYS_PROMPT}]
            },
            "contents": history
        }
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        }
        try:
            response = requests.post(URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            ai_response = data['candidates'][0]['content']['parts'][0]['text']
            self.call_from_thread(self.add_ai_msg, ai_response)
            history.append({
                "role": "model",
                "parts": [{"text": ai_response}]
            })
        except requests.exceptions.RequestException as e:
            self.call_from_thread(self.add_ai_msg, f"[Error]: {e}")

def askAI():
    app = CodeX()
    app.run()
