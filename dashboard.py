import base64

import requests
from nicegui import ui

from file_upload import open_file

API_BASE = "http://localhost:8001"

course_images = {}


def get_courses():
    try:
        resp = requests.get(f"{API_BASE}/courses", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        ui.notify(f"Could not reach API: {e}", type="negative")
        return []


def change_image(course_id):
    def save_image(name, data):
        course_images[course_id] = "data:image/png;base64," + base64.b64encode(data).decode()
        ui.navigate.reload()

    open_file(save_image, accept="image/*")


@ui.page("/dashboard")
def dashboard_page():
    ui.link("Back to courses", "/")
    ui.label("Dashboard").classes("text-2xl")
    courses = get_courses()
    with ui.row().classes("gap-6"):
        for c in courses:
            with ui.column():
                with ui.card().tight().classes("w-64 cursor-pointer").on(
                    "click", lambda c=c: ui.navigate.to(f"/?course={c['id']}")
                ):
                    if c["id"] in course_images:
                        ui.image(course_images[c["id"]]).classes("w-full h-32")
                    else:
                        ui.element("div").classes("w-full h-32").style(f"background-color: {c['color']}")
                    with ui.column().classes("p-4 gap-1"):
                        ui.label(c["code"]).classes("font-bold").style(f"color: {c['color']}")
                        ui.label(c["name"])
                        ui.label(c["term"]).classes("text-sm text-gray-500")
                ui.button("Change image", on_click=lambda c=c: change_image(c["id"]))