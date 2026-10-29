from .pdf_funtionality import file_text_extraction
from .model_prediction import extract_titles, extract_skills_loop
from .job_title_analyze import compare_skills


def extract_information(pdf):
    extracted_text = file_text_extraction(pdf)

    matched_titles = extract_titles(extracted_text)
    job_title = matched_titles[0] if matched_titles else None
    skills = extract_skills_loop(extracted_text, job_title)
    model_input = " ".join(([job_title] if job_title else []) + skills)

    return {
        "job_title": job_title,
        "skills": skills,
        "model_input": model_input,
    }

# resume_detail = extract_information(r"D:\resume\Yashash_Ravi_AI_Eng_Resume.pdf")
# # print(resume_detail)


# results = compare_skills(resume_detail["skills"])

# for role, details in results:
#     print(f"\n{role}: {details['score']}%")
#     print("Matched:", details["matched_skills"])
#     print("Missing:", details["missing_skills"])
    
    
def multiple_job_analysis(user_skills: list[str]) -> list[dict[str, object]]:
    return [
        {
            "role": role,
            "score": details["score"],
            "matched_skills": details["matched_skills"],
            "missing_skills": details["missing_skills"],
        }
        for role, details in compare_skills(user_skills)
    ]