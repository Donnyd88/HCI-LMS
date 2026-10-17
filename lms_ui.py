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
import dashboard
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
def main_page(course: int = None):  
    if course is not None:
        state["course_id"] = course
    courses = api_get("/courses")
    if courses and state["course_id"] is None:
        state["course_id"] = courses[0]["id"]

    with ui.row().classes("w-full no-wrap"):
        with ui.column().classes("w-1/5 p-2"):
            ui.link("Dashboard", "/dashboard")
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

    course = api_get(f"/courses/{course_id}")
    ui.label(f'{course.get("code", "")} - {course.get("name", "")}').classes("text-2xl")
    ui.label(f'{course.get("instructor", "")} | {course.get("term", "")}').classes("text-2xl")

    with ui.tabs().classes("w-full") as tabs:
        assignments_tab = ui.tab("Assignments")
        announcements_tab = ui.tab("Announcements")
        grades_tab = ui.tab("Grades")

    with ui.tab_panels(tabs, value=assignments_tab).classes("w-full"):
        with ui.tab_panel(assignments_tab):
            render_assignments(course_id)
        with ui.tab_panel(announcements_tab):
            render_announcements(course_id)
        with ui.tab_panel(grades_tab):
            render_grades(course_id)

def render_assignments(course_id: int):
    assignments = api_get(f"/courses/{course_id}/assignments")
    for a in assignments:
        label = f'{a["title"]} - due {a["due"][:10]} - {a["points"]} pts'
        if a["submitted"]:
            label += " (submitted)"
        ui.label(label)

def render_announcements(course_id: int):
    announcements = api_get(f"/courses/{course_id}/announcements")
    for ann in announcements:
        ui.label(ann["title"])
        ui.label(ann["body"])
        ui.separator()

def render_grades(course_id: int):
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

ui.run(port=8080, title="Mock Canvas")