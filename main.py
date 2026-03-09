from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai
import os

from database import conn, cursor

app = FastAPI()

templates = Jinja2Templates(directory="templates")

client=genai.Client(api_key="AIzaSyB3VDZiDRnOvTFc2_A8ZVHbeCOamkKaYpY")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: int = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    prompt = f"""
Create a 7 day fitness workout plan.

Rules:
- Do NOT use symbols like *, #, or ---
- Use simple plain text
- Separate each day clearly
- Keep formatting clean

Age: {age}
Weight: {weight}
Goal: {goal}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    plan = response.text

    cursor.execute(
        "INSERT INTO users(name,age,weight,goal,intensity) VALUES(?,?,?,?,?)",
        (name,age,weight,goal,intensity)
    )

    conn.commit()

    return templates.TemplateResponse(
        "results.html",
        {"request": request, "plan": plan}
    )