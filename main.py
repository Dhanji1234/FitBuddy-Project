from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai
import os
from dotenv import load_dotenv

from database import conn, cursor

# 1. Load environment variables from the .env file
load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# 2. Fetch the API key securely from the environment
api_key = os.getenv("GEMINI_API_KEY")

# 3. Safety check: Prevent the app from crashing silently if the key is missing
if not api_key:
    raise ValueError("API key not found! Please ensure you have a .env file with GEMINI_API_KEY set.")

# 4. Initialize the client securely
client = genai.Client(api_key=api_key)

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
    # Generate the content using the secure client
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    plan = response.text

    # Save the user data to the database
    cursor.execute(
        "INSERT INTO users(name,age,weight,goal,intensity) VALUES(?,?,?,?,?)",
        (name, age, weight, goal, intensity)
    )

    conn.commit()

    # Return the generated plan to the results page
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "plan": plan}
    )