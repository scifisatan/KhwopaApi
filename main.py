from fastapi import FastAPI
from scrapper import *
from parse import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "How to use this api is in the readme.md file"}


@app.get("/{username}/{password}/{semester}")
async def get_grades_semester(username: str, password: str, semester: int):
    scraped_data = scrape_all_site(username, password, semester)

    first_assessment_data = convert_to_dict(scraped_data["first_assessment"])
    final_assessment_data = convert_to_dict(scraped_data["final_assessment"])
    internal_marks_data = convert_to_dict_internal(scraped_data["internalMarks"])

    response_json = {
        "firstAssessment": first_assessment_data,
        "finalAssessment": final_assessment_data,
        "internalMarks": internal_marks_data,
    }

    return response_json


@app.get("/{username}/{password}/{semester}/{exam}")
async def get_grades_exam(username: str, password: str, semester: int, exam: str):
    scraped_data = scrape_one_site(username, password, semester, exam)
    if exam == "internalMarks":
        exam_data = convert_to_dict_internal(scraped_data)
    else:
        exam_data = convert_to_dict(scraped_data)
    return exam_data


@app.get("/dueAmount/{username}/{password}/")
async def fees(username, password):
    return scrape_dueAmount(username, password)
