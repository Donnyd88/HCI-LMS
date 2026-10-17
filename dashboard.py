from nicegui import ui

@ui.page("/dashboard") 

def dashboard_page():
    ui.link("Back to courses", "/")
    ui.label("Dashboard").classes("text-2x1")
    