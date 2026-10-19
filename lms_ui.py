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
from nicegui import ui, app

API_BASE = "http://localhost:8001"

state = {"course_id": None}

app.add_static_files(url_path="/Book_Images", local_directory="./Book_Images/")


def api_get(path: str):
    try:
        resp = requests.get(f"{API_BASE}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        ui.notify(f"Could not reach API: {e}", type="negative")
        return []


def create_sidebar():
    """Navigation sidebar."""
    with ui.column().classes(
        "fixed left-0 top-0 h-screen w-32 bg-gray-800 p-2 gap-2 z-50"
    ):
        ui.label("Canvas").classes("text-white font-bold text-lg mb-2 px-2")
        with ui.grid(columns=1).classes("w-full gap-2"):
            ui.button("Account", on_click=lambda: ui.notify("Account")).classes(
                "w-full"
            )
            ui.button("Courses", on_click=lambda: ui.navigate.to("/")).classes("w-full")
            ui.button("Grades", on_click=lambda: ui.notify("Grades")).classes("w-full")
            ui.button(
                "Materials", on_click=lambda: ui.navigate.to("/materials")
            ).classes("w-full")


@ui.page("/materials")
def materials_page():
    """Materials page"""

    create_sidebar()

    with ui.column().classes("ml-32 p-6 w-[calc(100%-8rem)]"):
        ui.label("Course Materials").classes("text-2xl font-bold mb-4")

        materials_data = api_get("/Materials")
        if not materials_data:
            ui.label("No materials uploaded yet.")
            return

        for course in materials_data:
            with ui.card().classes("w-full mb-6 p-4 shadow-md border"):
                ui.label(
                    f"{course.get('code', '')} - {course.get('course_name', '')}"
                ).classes("text-2xl font-bold mb-4")

                with ui.row().classes("w-full flex-nowrap overflow-x-auto gap-6 pb-4"):
                    for book in course.get("class_materials", []):
                        book_name = book.get("Book name", "Unknown Title")
                        book_isbn = book.get("Isbn") or book.get("ISBN", "N/A")
                        book_author = book.get("Author", "Unknown")
                        book_edition = book.get("Edition", "N/A")
                        book_link = book.get("Link", "")
                        book_image = book.get("Image", "")

                        is_required = str(book.get("Required", "")).lower() == "true"

                        if not book_image:
                            book_image = (
                                "https://via.placeholder.com/120x160?text=No+Cover"
                            )

                        with ui.row().classes(
                            "min-w-[400px] border rounded-lg p-4 bg-gray-50"
                        ):
                            with ui.column().classes("w-32 items-center gap-2"):
                                ui.image(book_image).classes(
                                    "w-full h-48 rounded shadow-sm object-cover"
                                )

                                if book_link:
                                    ui.button(
                                        "Buy",
                                        on_click=lambda l=book_link: ui.navigate.to(
                                            l, new_tab=True
                                        ),
                                    ).classes("w-full")
                                else:
                                    ui.button("Buy").classes("w-full").disable()

                            # right side info
                            with ui.column().classes("flex-1 pl-4 gap-1"):
                                ui.label(book_name).classes(
                                    "text-lg font-bold leading-tight"
                                )
                                ui.label(f"Author: {book_author}").classes(
                                    "text-gray-700"
                                )
                                ui.label(f"Edition: {book_edition}").classes(
                                    "text-gray-700 text-sm"
                                )
                                ui.label(f"ISBN: {book_isbn}").classes(
                                    "text-gray-700 text-sm"
                                )

                                if is_required:
                                    ui.badge("Required", color="red").classes("mt-2")
                                else:
                                    ui.badge("Optional", color="blue").classes("mt-2")


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
                ui.link(c["code"], "#").on("click", lambda c=c: select_course(c["id"]))

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
    ui.label(f"{course.get('code', '')} - {course.get('name', '')}").classes("text-2xl")
    ui.label(f"{course.get('instructor', '')} | {course.get('term', '')}").classes(
        "text-2xl"
    )

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
        label = f"{a['title']} - due {a['due'][:10]} - {a['points']} pts"
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
