from fastapi import FastAPI
from scrapper import *
from parse import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends

app = FastAPI()


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

def get_login_data(username: str, password: str):
    return {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0",
        "yt0": "Login",
    }

@app.get("/login/{username}/{password}/")
async def checkLogin(login_data: dict = Depends(get_login_data)):
    return {"status":"Login Successful" if login(login_data) else "Incorrect Login Details"}

@app.get("/dueAmount/{username}/{password}/")
async def fees(username, password):
    return scrape_dueAmount(username, password)


@app.get("/grades/{username}/{password}/{semester}/")
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
