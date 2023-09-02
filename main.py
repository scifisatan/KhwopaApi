from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from scrapper import *
from parse import *
from fastapi.middleware.cors import CORSMiddleware
from schemas import ExamMarks
from deps import login_required

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "How to use this api is in the readme.md file"}



@app.get("/login/{username}/{password}/")
async def checkLogin(username, password):
    data = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0",
        "yt0": "Login",
    }

    return {"status":"Incorrect Login Details" if login(data) else "Login Successful"}


@app.get("/{username}/{password}/{semester}/")
async def get_grades_semester(username: str, password: str, semester: int):
    scraped_data = scrape_all_site(username, password, semester)
    if type(scraped_data) == str:   
        return {"message": f"{scraped_data}"}   
    
    first_assessment_data = convert_to_dict(scraped_data["firstAssessment"])
    final_assessment_data = convert_to_dict(scraped_data["finalAssessment"])
    internal_marks_data = convert_to_dict_internal(scraped_data["internalMarks"])

    response_json = {
        "firstAssessment": first_assessment_data,
        "finalAssessment": final_assessment_data,
        "internalMarks": internal_marks_data,
    }

    return response_json


@app.get("/grades/{semester}/{exam}")
async def get_grades_exam(semester: int, exam: ExamMarks, user=Depends(login_required)):
    scraped_data = scrape_one_site(user.username, user.password, semester, exam.value)
    if exam == ExamMarks.INTERNAL:
        exam_data = convert_to_dict_internal(scraped_data)
    else: # bug: AssessmentMarks is not actual field in website.
        exam_data = convert_to_dict(scraped_data)
    return exam_data


@app.get("/dueAmount/{username}/{password}/")
async def fees(username, password):
 

 