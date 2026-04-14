import flet as ft
import requests
import threading
import time
import multiprocessing
from neuro_symbolic import run_neuro_symbolic_pipeline

MAX_LOGS = 50  # Rolling window limit to prevent memory leaks

def get_ollama_models():
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        resp.raise_for_status()
        return [m["name"] for m in resp.json().get("models", [])]
    except Exception:
        return []

def main(page: ft.Page):
    page.title = "Math-OS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 800
    page.bgcolor = "#F8F9FA"
    page.padding = 0

    # --- STATE ---
    models = get_ollama_models()
    if not models:
        models = ["deepseek-r1:8b"]
    
    state = {
        "current_model": models[0],
        "is_thinking": False
    }

    # --- UI COMPONENTS ---
    
    # Header Area
    model_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(m) for m in models],
        value=state["current_model"],
        width=250,
        height=40,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=0),
        bgcolor="#FFFFFF",
        border_radius=8,
        border_color="#DEE2E6"
    )
    model_dropdown.on_change = lambda e: state.update({"current_model": e.control.value})

    header = ft.Container(
        content=ft.Row([
            ft.Text("Math-OS", size=24, weight="bold", color="#212529"),
            ft.Text("Neuro-Symbolic Solver", size=14, color="#6C757D"),
            ft.Container(expand=True),  # Spacer
            ft.Text("Model:", size=14, color="#495057", weight="bold"),
            model_dropdown
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
        bgcolor="#FFFFFF"
    )
    
    header_divider = ft.Container(height=1, bgcolor="#E9ECEF")

    # Chat Area
    chat_list = ft.ListView(
        expand=True,
        spacing=15,
        padding=20,
        auto_scroll=True
    )

    def manage_memory():
        """Ensures the chat_list does not exceed MAX_LOGS to prevent memory leaks."""
        while len(chat_list.controls) > MAX_LOGS:
            oldest_control = chat_list.controls.pop(0)
            # Flet objects should just be dereferenced, in old flet clean() might not exist on controls. 
            # If it throws, we can safely ignore it or just pop it.
            if hasattr(oldest_control, 'clean'):
                try:
                    oldest_control.clean() 
                except Exception:
                    pass

    def add_message(role: str, text: str, is_log: bool = False):
        bg_color = "#FFFFFF" if role == "user" else "#E9ECEF" if is_log else "#E3F2FD"
        text_color = "#212529" if role == "user" else "#6C757D" if is_log else "#084298"
        border_col = "#DEE2E6" if role == "user" else "transparent" if is_log else "#B6D4FE"
        align = ft.MainAxisAlignment.END if role == "user" else ft.MainAxisAlignment.START
        
        msg_container = ft.Container(
            content=ft.Text(text, color=text_color, size=13 if is_log else 15, selectable=True),
            bgcolor=bg_color,
            padding=15,
            border_radius=10,
            border=ft.Border.all(1, border_col) if border_col != "transparent" else None,
            width=600 if not is_log else 700, # Constrain width for chat bubbles
        )
        
        row = ft.Row([msg_container], alignment=align)
        chat_list.controls.append(row)
        manage_memory()
        page.update()

    # Input Area
    problem_input = ft.TextField(
        hint_text="Type your mathematical problem here...",
        multiline=True,
        min_lines=1,
        max_lines=5,
        bgcolor="#FFFFFF",
        border_radius=20,
        border_color="#DEE2E6",
        content_padding=ft.padding.all(15),
        expand=True,
        shift_enter=True,
        text_style=ft.TextStyle(color="#212529")
    )

    solve_btn = ft.ElevatedButton(
        content="Send",
        color="#FFFFFF",
        bgcolor="#0D6EFD",
        width=100,
        height=50,
        tooltip="Send Problem"
    )

    input_container = ft.Container(
        content=ft.Row([
            problem_input,
            solve_btn
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.END),
        padding=20,
        bgcolor="#FFFFFF"
    )
    
    input_divider = ft.Container(height=1, bgcolor="#E9ECEF")

    # --- LOGIC ---
    def solve_click(e):
        problem = problem_input.value.strip()
        if not problem or state["is_thinking"]:
            return
        
        state["is_thinking"] = True
        problem_input.value = ""
        solve_btn.disabled = True
        problem_input.disabled = True
        
        add_message("user", problem)
        page.update()

        def run_task():
            start_time = time.time()
            try:
                result = run_neuro_symbolic_pipeline(
                    problem, 
                    model=state['current_model'],
                    ui_callback=lambda m: add_message("system", m, is_log=True)
                )
                duration = round(time.time() - start_time, 1)
                add_message("assistant", f"**Result:**\n{result}\n\n_Done in {duration}s_")
            except Exception as ex:
                add_message("assistant", f"**Error:** {str(ex)}")
            finally:
                state["is_thinking"] = False
                solve_btn.disabled = False
                problem_input.disabled = False
                page.update()

        threading.Thread(target=run_task, daemon=True).start()

    solve_btn.on_click = solve_click

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Enter" and not e.shift and not state["is_thinking"]:
            solve_click(None)
            
    page.on_keyboard_event = on_keyboard

    # Add welcome message
    add_message("assistant", "Welcome to Math-OS Premium. How can I help you solve a math problem today?")

    # --- MAIN LAYOUT ---
    main_column = ft.Column([
        header,
        header_divider,
        ft.Container(content=chat_list, expand=True, bgcolor="#F8F9FA"),
        input_divider,
        input_container
    ], expand=True, spacing=0)

    page.add(main_column)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    ft.run(main)
