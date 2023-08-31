from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from scrapper import *
from parse import *
from fastapi.middleware.cors import CORSMiddleware
from schemas import ExamMarks
from deps import login_required

app = FastAPI()


#origins = ["http://localhost:5173/", #"http://localhost:5173", #"localhost:5137","https://khwopafrontend.vercel.app/," #"https://khwopafrontend.vercel.app"]

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



@app.get("/login/{username}/{password}")
async def checkLogin(username: str, password: str):
    data = {
        "LoginForm[username]": username,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0",
        "yt0": "Login",
    }

    success: bool = login(data)

    json_response = JSONResponse(
        content={"status": "Login successful." if success else "Login failed."}
    )

    #there is bug in login function
    if  success:
        json_response.set_cookie(key="username", value=username, httponly=True)
        json_response.set_cookie(key="password", value=password, httponly=True)

    return json_response


@app.get("/grades/{semester}")
async def get_grades_semester(semester: int, user = Depends(login_required)):
    scraped_data = scrape_all_site(user.username, user.password, semester)
    if type(scraped_data) == str:
        return {"message": f"{scraped_data}"}

    first_assessment_data = convert_to_dict(scraped_data["firstAssessment"])        #type:ignore
    final_assessment_data = convert_to_dict(scraped_data["finalAssessment"])        #type:ignore
    internal_marks_data = convert_to_dict_internal(scraped_data["internalMarks"])   #type:ignore

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


@app.get("/dueAmount")
async def fees(user=Depends(login_required)):
    return scrape_dueAmount(user.username, user.password)

