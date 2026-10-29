from fastapi import APIRouter, Depends, HTTPException, status, Response


from backend.dependencies.Funtions import extract_information
from backend.dependencies.job_title_analyze import compare_skills

router = APIRouter(prefix="/job_analysis")


# @router.post(
#     "/register",
#     response_model=UserResponse,
#     status_code=status.HTTP_201_CREATED,
# )
def multiple_job_analysis(pdf):
    
    resume_detail = extract_information(pdf=pdf)
    
    results = compare_skills(resume_detail["skills"])
    
    for role, details in results:
        print(f"\n{role}: {details['score']}%")
        print("Matched:", details["matched_skills"])
        print("Missing:", details["missing_skills"])
        
        