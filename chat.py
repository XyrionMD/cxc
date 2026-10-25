import requests
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer, Center
from textual.widgets import Header, Footer, Input, Static, Markdown
from textual.binding import Binding
from textual.screen import ModalScreen

from config_loader import load_config

CVT = load_config()
                            

API_KEY = f"{CVT.API}"
MODEL_AI = f"{CVT.MODEL}"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_AI}:generateContent?key={API_KEY}"

history = []

class HelpScreen(ModalScreen):
    BINDINGS = [
        ("escape", "dismiss", "Close"),
    ]

    def compose(self):
        yield Static(
            """[ HELP ]

quit         : Go out 

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


    def compose(self):
        yield Header(name="CodeX Core", classes="header")
        with ScrollableContainer(id="chat-area"):
            pass
        yield Input(placeholder="Type a message ...", id="input-box")
        yield Footer()

    def on_mount(self):
        self.query_one("#input-box", Input).focus()

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


        self.add_user_msg(msg)
        self.query_one("#input-box", Input).value = ""
        self.run_worker(lambda: self.get_ai_response(msg), name="ai_request", thread=True)

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

    def get_ai_response(self, msg):
        history.append({
            "role": "user",
            "parts": [{"text": msg}]
        })
        SYS_PROMPT = f"{CVT.AI_PROMPT}"
        payload = {
            "system_instruction": {
                "parts": [{"text": SYS_PROMPT}]
            },
            "contents": history
        }
        headers = {"Content-Type": "application/json"}
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
            self.call_from_thread(self.add_ai_msg, f"Connection Error: {e}")

def askAI():
    app = CodeX()
    app.run()
