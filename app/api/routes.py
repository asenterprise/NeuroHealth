import html
import asyncpg
from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.utils.parser import parse_lecture
from app.db.queries import get_db_connection, add_lecture, add_sections
from app.services.json_services import process_lecture_json

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
    
@router.post("/lectures-ui/add")
async def add_lecture_ui(
    request: Request,
    title: str = Form(...),
    content: str = Form(...)
):
    try:
        conn = await get_db_connection()
        lecture_id = await add_lecture(conn, title, content)
        await conn.close()

        return JSONResponse(content={"lecture_id": lecture_id})  # Return JSON response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/lectures-ui/parse", response_class=HTMLResponse)
async def parse_lecture_ui(
    request: Request,
    lecture_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):
    """Parse lecture into sections and display them before saving."""
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


@router.post("/sections/save")
async def save_sections(json_data: dict, conn=Depends(get_db_connection)):
    """Save lecture sections to database."""
    try:
        # Process input data
        processed_data = await process_lecture_json(json_data)
        lecture_id, sections = processed_data["lecture_id"], processed_data["sections"]

        # Save to database
        await add_sections(conn, lecture_id, sections)

        return {"message": "Sections saved successfully"}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving sections: {str(e)}")