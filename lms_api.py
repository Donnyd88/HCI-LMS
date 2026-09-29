"""
lms_api.py

A mock backend that serves Canvas-like LMS data over HTTP.
Built with FastAPI so it's easy to run standalone and easy for a
NiceGUI (or any) frontend to consume with simple HTTP requests.

Run with:
    pip install fastapi uvicorn
    python lms_api.py

API is available at http://localhost:8001

Endpoints:
    GET /courses
    GET /courses/{course_id}
    GET /courses/{course_id}/assignments
    GET /courses/{course_id}/announcements
    GET /courses/{course_id}/grades
"""

from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mock LMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

NOW = datetime(2026, 8, 23, 9, 0, 0)

def _iso(days_offset: int) -> str:
    return (NOW + timedelta(days=days_offset)).isoformat()

# ---------------------------------------------------------------------
# In-memory "database"
# ---------------------------------------------------------------------

COURSES = [
    {
        "id": 1,
        "code": "CS 340",
        "name": "Human-Computer Interaction",
        "instructor": "Prof. Parton",
        "term": "Fall 2026",
        "color": "#5b8def",
    },
    {
        "id": 2,
        "code": "CS 212",
        "name": "Data Structures & Algorithms",
        "instructor": "Prof. Presley",
        "term": "Fall 2026",
        "color": "#e07a5f",
    },
    {
        "id": 3,
        "code": "ENGL 150",
        "name": "Technical Writing",
        "instructor": "Prof. Cash",
        "term": "Fall 2026",
        "color": "#81b29a",
    },
]

ASSIGNMENTS = {
    1: [
        {"id": 101, "title": "Heuristic Evaluation Writeup", "due": _iso(2), "points": 50, "submitted": False},
        {"id": 102, "title": "Low-Fidelity Prototype", "due": _iso(-1), "points": 30, "submitted": True},
        {"id": 103, "title": "Fitts' Law Problem Set", "due": _iso(9), "points": 20, "submitted": False},
        {"id": 104, "title": "Reading Response 3", "due": _iso(-5), "points": 10, "submitted": True},
    ],
    2: [
        {"id": 201, "title": "Binary Search Tree Lab", "due": _iso(1), "points": 40, "submitted": False},
        {"id": 202, "title": "Heap Sort Implementation", "due": _iso(6), "points": 40, "submitted": False},
        {"id": 203, "title": "Midterm Review Set", "due": _iso(-3), "points": 15, "submitted": True},
    ],
    3: [
        {"id": 301, "title": "Draft: Formal Report", "due": _iso(4), "points": 60, "submitted": False},
        {"id": 302, "title": "Peer Review Checklist", "due": _iso(-2), "points": 10, "submitted": True},
    ],
}

ANNOUNCEMENTS = {
    1: [
        {"id": 1001, "title": "Office hours moved this week", "posted": _iso(-1),
         "body": "My Thursday office hours will be 2-4pm instead of the usual time, same room."},
        {"id": 1002, "title": "Prototype rubric posted", "posted": _iso(-4),
         "body": "The rubric for the low-fidelity prototype assignment is now up in the assignment details."},
    ],
    2: [
        {"id": 2001, "title": "Midterm grades released", "posted": _iso(-2),
         "body": "Grades are posted. Regrade requests are due within one week."},
    ],
    3: [
        {"id": 3001, "title": "No class Friday", "posted": _iso(-6),
         "body": "Class is cancelled Friday for a department event. Draft is still due as scheduled."},
    ],
}

GRADES = {
    1: [
        {"assignment": "Low-Fidelity Prototype", "score": 27, "points": 30},
        {"assignment": "Reading Response 3", "score": 9, "points": 10},
    ],
    2: [
        {"assignment": "Midterm Review Set", "score": 14, "points": 15},
    ],
    3: [
        {"assignment": "Peer Review Checklist", "score": 10, "points": 10},
    ],
}


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------

def _get_course_or_404(course_id: int) -> dict:
    for c in COURSES:
        if c["id"] == course_id:
            return c
    raise HTTPException(status_code=404, detail="Course not found")


@app.get("/courses")
def list_courses():
    return COURSES


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return _get_course_or_404(course_id)


@app.get("/courses/{course_id}/assignments")
def get_assignments(course_id: int):
    _get_course_or_404(course_id)
    return ASSIGNMENTS.get(course_id, [])


@app.get("/courses/{course_id}/announcements")
def get_announcements(course_id: int):
    _get_course_or_404(course_id)
    return ANNOUNCEMENTS.get(course_id, [])


@app.get("/courses/{course_id}/grades")
def get_grades(course_id: int):
    _get_course_or_404(course_id)
    return GRADES.get(course_id, [])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)