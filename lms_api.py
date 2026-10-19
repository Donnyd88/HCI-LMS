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
    GET /materials/{course_id}
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
        {
            "id": 101,
            "title": "Heuristic Evaluation Writeup",
            "due": _iso(2),
            "points": 50,
            "submitted": False,
        },
        {
            "id": 102,
            "title": "Low-Fidelity Prototype",
            "due": _iso(-1),
            "points": 30,
            "submitted": True,
        },
        {
            "id": 103,
            "title": "Fitts' Law Problem Set",
            "due": _iso(9),
            "points": 20,
            "submitted": False,
        },
        {
            "id": 104,
            "title": "Reading Response 3",
            "due": _iso(-5),
            "points": 10,
            "submitted": True,
        },
    ],
    2: [
        {
            "id": 201,
            "title": "Binary Search Tree Lab",
            "due": _iso(1),
            "points": 40,
            "submitted": False,
        },
        {
            "id": 202,
            "title": "Heap Sort Implementation",
            "due": _iso(6),
            "points": 40,
            "submitted": False,
        },
        {
            "id": 203,
            "title": "Midterm Review Set",
            "due": _iso(-3),
            "points": 15,
            "submitted": True,
        },
    ],
    3: [
        {
            "id": 301,
            "title": "Draft: Formal Report",
            "due": _iso(4),
            "points": 60,
            "submitted": False,
        },
        {
            "id": 302,
            "title": "Peer Review Checklist",
            "due": _iso(-2),
            "points": 10,
            "submitted": True,
        },
    ],
}

ANNOUNCEMENTS = {
    1: [
        {
            "id": 1001,
            "title": "Office hours moved this week",
            "posted": _iso(-1),
            "body": "My Thursday office hours will be 2-4pm instead of the usual time, same room.",
        },
        {
            "id": 1002,
            "title": "Prototype rubric posted",
            "posted": _iso(-4),
            "body": "The rubric for the low-fidelity prototype assignment is now up in the assignment details.",
        },
    ],
    2: [
        {
            "id": 2001,
            "title": "Midterm grades released",
            "posted": _iso(-2),
            "body": "Grades are posted. Regrade requests are due within one week.",
        },
    ],
    3: [
        {
            "id": 3001,
            "title": "No class Friday",
            "posted": _iso(-6),
            "body": "Class is cancelled Friday for a department event. Draft is still due as scheduled.",
        },
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

MATERIALS = [
    {
        "code": "CS761",
        "course_name": "Human-Computer Interaction",
        "class_materials": [
            {
                "Book name": "Interaction Design",
                "Isbn": 9781119020752,
                "Author": "Yvonne Rogers et al.",
                "Edition": "4th",
                "Required": True,
                "Purchased": False,
                "Link": "https://www.amazon.com/dp/0470665769?lv=shuf&channelId=500&plpRedirect=mhFallback",
                "Image": "/Book_Images/Interaction_Design.jpeg",
            },
            {
                "Book name": "The Design of Everyday Things",
                "ISBN": 9780465050659,
                "Author": "Don Norman",
                "Edition": "Any",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.com/dp/B00ES27KW2?lv=shuf&channelId=500&plpRedirect=mhFallback",
                "Image": "/Book_Images/The_Design_of_EveryDay_Things.jpeg",
            },
            {
                "Book name": "About Face: The Essentials of Interaction Design",
                "Isbn": 9781118766576,
                "Author": "Alan Cooper et al.",
                "Edition": "4th",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.com/dp/1118766571?lv=shuf&channelId=500&plpRedirect=mhFallback",
                "Image": "/Book_Images/About_Face.jpeg",
            },
        ],
    },
    {
        "code": "CS725",
        "course_name": "Networking",
        "class_materials": [
            {
                "Book name": "Computer Networking",
                "ISBN": 9780135928790,
                "Author": "James F. Kurose",
                "Edition": "8th",
                "Required": True,
                "Purchased": False,
                "Link": "https://www.amazon.com/Computer-Networking-Top-Down-Approach-Kurose/dp/0135429331/ref=pd_lpo_d_sccl_1/136-9451899-5630339?pd_rd_w=9UIPB&content-id=amzn1.sym.4c8c52db-06f8-4e42-8e56-912796f2ea6c&pf_rd_p=4c8c52db-06f8-4e42-8e56-912796f2ea6c&pf_rd_r=PC7YBK8ZA2XJ7CSMTNKQ&pd_rd_wg=aoxbW&pd_rd_r=61b73e98-6607-4d13-b0aa-4d3b08721e03&pd_rd_i=0135429331&psc=1",
                "Image": "/Book_Images/Computer_Networking.webp",
            }
        ],
    },
    {
        "code": "CS720",
        "course_name": "Systems Programming",
        "class_materials": [
            {
                "Book name": "Learning Linux Binary Analysis ",
                "ISBN": 9781782167105,
                "Author": "Ryan O'Neill",
                "Edition": "8th",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.com/dp/1782167102?lv=shuf&language=he&channelId=500&plpRedirect=mhFallback",
                "Image": "/Book_Images/Learning_Linux_Binary_Analysis.jpg",
            },
            {
                "Book name": "Linkers and Loaders  ",
                "ISBN": 781558604964,
                "Author": "John Levine",
                "Edition": "8th",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.ca/Linkers-Loaders-John-R-Levine/dp/1558604960",
                "Image": "/Book_Images/Linkers_&_Loaders.webp",
            },
            {
                "Book name": "Computer Systems: A Programmer's Perspective",
                "ISBN": 9780134092669,
                "Author": "Bryant and O'Hallaron",
                "Edition": "8th",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.com/Computer-Systems-Programmers-Perspective-3/dp/9332573905",
                "Image": "/Book_Images/Computer_Systems.webp",
            },
            {
                "Book name": "Computer Organization and Design - A Hardware/Software Interface",
                "ISBN": 9780128201091,
                "Author": "David Patterson and John Hennessey",
                "Edition": "8th",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.com/dp/B006ZMGCVS?lv=shuf&channelId=500&plpRedirect=mhFallback",
                "Image": "/Book_Images/Computer_Organization.webp",
            },
            {
                "Book name": "Systems Programming",
                "ISBN": 9780070176034,
                "Author": "John Donovan",
                "Edition": "8th",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.com/Systems-Programming-McGraw-Hill-computer-science/dp/0070176035",
                "Image": "/Book_Images/Systems Programming.jpg",
            },
            {
                "Book name": "Operating Systems Internals and Design Principles",
                "ISBN": 9780133805918,
                "Author": "William Stallings",
                "Edition": "8th",
                "Required": False,
                "Purchased": False,
                "Link": "https://www.amazon.com/Operating-Systems-Internals-Design-Principles/dp/9352866711",
                "Image": "/Book_Images/Operating_Systems_Internals_and_design_Principles.webp",
            },
        ],
    },
]


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


@app.get("/Materials")
def get_materials():
    return MATERIALS


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
