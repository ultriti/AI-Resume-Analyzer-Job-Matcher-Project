
from collections import Counter
import re


def normalize(skill):
    skill = skill.lower().strip()
    aliases = {
        "sklearn": "scikit-learn",
        "scikit learn": "scikit-learn",
        "reactjs": "react",
        "nodejs": "node.js",
        "postgres": "postgresql",
    }
    return aliases.get(skill, skill)


def parse_skills(value):
    return [
        normalize(s)
        for s in re.split(r"[,;|\n]+", str(value))
        if s.strip()
    ]


def select_top_skills(
    resume_skills,
    job_rows,
    top_n=15,
):
    # Deduplicate resume skills.
    resume_skills = list(dict.fromkeys(
        normalize(s) for s in resume_skills
    ))

    # Count how often each skill occurs across job postings.
    job_skill_counts = Counter()

    for row in job_rows:
        job_skill_counts.update(
            set(parse_skills(row["required_skills"]))
        )

    total = max(len(job_rows), 1)

    # Skill prevalence across job postings.
    # Rare skills get more weight for distinguishing roles.
    scores = {}

    for skill in resume_skills:
        prevalence = job_skill_counts[skill] / total

        # Smoothed inverse prevalence:
        # avoids giving unseen skills an infinite score.
        relevance = 1.0 / (1.0 + prevalence)

        scores[skill] = relevance

    return sorted(
        resume_skills,
        key=lambda skill: scores[skill],
        reverse=True,
    )[:top_n]


# Example:
resume_skills = extract_skills(resume_text)
job_rows = combined_dataframe.to_dict("records")
major_skills = select_top_skills(resume_skills, job_rows)
print(major_skills)
