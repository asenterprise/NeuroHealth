import html
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.utils.parser import parse_lecture

router = APIRouter()

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/lectures-ui/")
async def lectures_ui(request: Request):
    return templates.TemplateResponse("lectures.html", {"request": request, "lectures": []})


@router.post("/lectures-ui/parse", response_class=HTMLResponse)
async def parse_lecture_ui(
    request: Request,
    lecture_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):
    """Parses the lecture into sections and displays them before saving."""
    try:
        sections = parse_lecture(content)

        return templates.TemplateResponse(
            "sections_preview.html",
            {
                "request": request,
                "lecture_id": lecture_id,
                "title": title,
                "sections": sections
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))