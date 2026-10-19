"""
lms_ui.py

A simple NiceGUI frontend that pulls data from lms_api.py
and renders a Learning Management System (LMS) course dashboard.

Run with:
    pip install nicegui requests
    python lms_api.py        # in one terminal
    python lms_ui.py              # in another terminal

Then http://localhost:8080 will open automatically.
"""

import requests
from nicegui import ui

API_BASE = "http://localhost:8001"

state = {"course_id": None}

def api_get(path: str):
    try:
        resp = requests.get(f"{API_BASE}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        ui.notify(f"Could not reach API: {e}", type="negative")
        return []

@ui.page("/")
def main_page():
    ui.add_css(f'''
        .titles {{
            font-size: 24px;
            line-height: 32px;
            color: {'black'}
        }}

        .tabs {{
            width: 100%;
            color: {'black'}
        }}
    ''')

    courses = api_get("/courses")
    if courses and state["course_id"] is None:
        state["course_id"] = courses[0]["id"]

    with ui.row().classes("w-full no-wrap"):
        with ui.column().classes("w-1/5 p-2"):
            ui.label("Courses").classes("text-lg")
            for c in courses:
                ui.link(c["code"], "#").on(
                    "click", lambda c=c: select_course(c["id"])
                )

        with ui.column().classes("w-4/5 p-4"):
            render_main_content()

def select_course(course_id: int):
    state["course_id"] = course_id
    render_main_content.refresh()

@ui.refreshable
def render_main_content():
    course_id = state["course_id"]
    if course_id is None:
        ui.label("No course selected")
        return

    with ui.tabs().classes("tabs") as tabs:
        assignments_tab = ui.tab("Assignments")
        announcements_tab = ui.tab("Announcements")
        grades_tab = ui.tab("Grades")
        settings_tab = ui.tab("Settings")

    with ui.tab_panels(tabs, value=assignments_tab).classes("tabs"):
        with ui.tab_panel(assignments_tab):
            render_assignments(course_id)
        with ui.tab_panel(announcements_tab):
            render_announcements(course_id)
        with ui.tab_panel(grades_tab):
            render_grades(course_id)
        with ui.tab_panel(settings_tab):
            render_settings()

def render_assignments(course_id: int):
    course = api_get(f"/courses/{course_id}")
    ui.label(f'{course.get("code", "")} - {course.get("name", "")}').classes("titles")
    ui.label(f'{course.get("instructor", "")} | {course.get("term", "")}').classes("titles")

    assignments = api_get(f"/courses/{course_id}/assignments")
    for a in assignments:
        label = f'{a["title"]} - due {a["due"][:10]} - {a["points"]} pts'
        if a["submitted"]:
            label += " (submitted)"
        ui.label(label)
    ui.update()

def render_announcements(course_id: int):
    course = api_get(f"/courses/{course_id}")
    ui.label(f'{course.get("code", "")} - {course.get("name", "")}').classes("titles")
    ui.label(f'{course.get("instructor", "")} | {course.get("term", "")}').classes("titles")

    announcements = api_get(f"/courses/{course_id}/announcements")
    for ann in announcements:
        ui.label(ann["title"])
        ui.label(ann["body"])
        ui.separator()

    ui.update()

def render_grades(course_id: int):
    course = api_get(f"/courses/{course_id}")
    ui.label(f'{course.get("code", "")} - {course.get("name", "")}').classes("titles")
    ui.label(f'{course.get("instructor", "")} | {course.get("term", "")}').classes("titles")

    grades = api_get(f"/courses/{course_id}/grades")
    if not grades:
        ui.label("No grades posted yet.")
        return
    columns = [
        {"name": "assignment", "label": "Assignment", "field": "assignment"},
        {"name": "score", "label": "Score", "field": "score"},
        {"name": "points", "label": "Points", "field": "points"},
    ]
    ui.table(columns=columns, rows=grades, row_key="assignment")

    ui.update()

def render_settings():
    ui.label("Customize Canvas").classes("titles")

    ui.label("Color theme:")
    with ui.row():
        redbutton = ui.button(on_click=lambda: update_theme("lightcoral", "maroon"), color='red').style("width: 10px; height: 10px;")
        bluebutton = ui.button(on_click=lambda: update_theme("lightblue", "darkblue"), color='blue').style("width: 10px; height: 10px;")
        yellowbutton = ui.button(on_click=lambda: update_theme("lightyellow", "goldenrod"), color='yellow').style("width: 10px; height: 10px;")
        greenbutton = ui.button(on_click=lambda: update_theme("palegreen", "darkgreen"), color='green').style("width: 10px; height: 10px;")
        pinkbutton = ui.button(on_click=lambda: update_theme("lightpink", "darkmagenta"), color='pink').style("width: 10px; height: 10px;")
        blackbutton = ui.button(on_click=lambda: update_theme("white", "black"), color='black').style("width: 10px; height: 10px;")

def update_theme(color, auxcolor):
    ui.add_css(f'''
        .titles {{
            font-size: 24px;
            line-height: 32px;
            color: {auxcolor}
        }}

        .tabs {{
            width: 100%;
            color: {auxcolor}
        }}
    ''')

    ui.query('body').style(f'background-color: {color}')

    ui.update()

ui.run(port=8080, title="Mock Canvas")