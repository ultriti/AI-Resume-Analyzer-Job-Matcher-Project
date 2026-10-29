from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd
from pypdf import PdfReader


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"

DATASET_FILES = [
    "aiml pre.csv",
    "business pre.csv",
    "cloud_infrastructure pre.csv",
    "design pre.csv",
    "developer pre.csv",
    "marketing pre.csv",
    "product_management pre.csv",
]

# Only return job postings whose required-skill coverage reaches this value.
# Set to 0 to return every posting, including poor matches.
DEFAULT_MIN_MATCH_PERCENT = 60.0
DEFAULT_TOP_N = 10

REQUIRED_COLUMNS = {"job_title", "category", "required_skills"}


# ============================================================
# SKILL TAXONOMY
# Add skills here to improve resume skill extraction.
# ============================================================

SKILLS = {
    "Programming": {
        "python", "java", "javascript", "typescript", "c", "c++",
        "c#", "sql", "r", "go", "rust"
    },
    "Machine Learning": {
        "machine learning", "scikit-learn", "sklearn",
        "feature engineering", "classification", "regression",
        "random forest", "decision tree", "xgboost",
        "model evaluation", "model selection", "tf-idf",
        "cross validation", "hyperparameter tuning"
    },
    "Deep Learning": {
        "deep learning", "tensorflow", "keras", "pytorch",
        "neural networks", "cnn", "cnns", "rnn", "rnns",
        "lstm", "gru", "bigru", "transfer learning",
        "backpropagation", "dropout", "softmax",
        "cross entropy", "adam optimizer", "early stopping"
    },
    "Graph Machine Learning": {
        "graph neural network", "graph neural networks",
        "gnn", "graph convolutional network",
        "graph convolutional networks", "gcn",
        "pytorch geometric", "pyg", "node classification",
        "citation networks", "graph representation learning",
        "message passing", "networkx"
    },
    "Natural Language Processing": {
        "natural language processing", "nlp",
        "text classification", "tokenization",
        "word embeddings", "sequence modeling",
        "hugging face", "transformers", "spacy",
        "named entity recognition", "sentiment analysis",
        "text preprocessing", "language models"
    },
    "Generative AI and Agents": {
        "generative ai", "large language models", "llm", "llms",
        "retrieval augmented generation", "rag",
        "langchain", "langgraph", "vector databases",
        "embeddings", "chromadb", "chroma",
        "ai agents", "agentic ai", "prompt engineering",
        "information retrieval", "semantic search",
        "human in the loop", "tool calling"
    },
    "Computer Vision": {
        "computer vision", "opencv", "image classification",
        "image processing", "object detection",
        "facial emotion recognition", "emotion recognition",
        "image segmentation"
    },
    "Data Science and Analytics": {
        "pandas", "numpy", "scipy", "matplotlib", "seaborn",
        "statistical analysis", "data analysis",
        "data visualization", "exploratory data analysis",
        "data preprocessing", "probability", "prediction",
        "excel", "power bi", "tableau"
    },
    "Backend and APIs": {
        "fastapi", "flask", "django", "rest api", "rest apis",
        "restful api", "pydantic", "onnx", "onnx runtime",
        "model inference", "model deployment", "web scraping",
        "beautifulsoup", "beautifulsoup4", "api development"
    },
    "Frontend Development": {
        "react", "react.js", "reactjs", "next.js", "nextjs",
        "html", "css", "tailwind css", "vite",
        "responsive design", "frontend development", "redux"
    },
    "Backend Development": {
        "node.js", "nodejs", "express.js", "expressjs",
        "socket.io", "websockets", "backend development",
        "api gateway", "microservices"
    },
    "Full Stack Development": {
        "full stack development", "full stack",
        "software development", "application development",
        "electron"
    },
    "Databases": {
        "postgresql", "postgres", "mysql", "mongodb",
        "sqlite", "redis", "database design",
        "database management", "database optimization",
        "sqlalchemy", "vector database", "vector databases"
    },
    "Tools and DevOps": {
        "git", "github", "docker", "kubernetes",
        "jupyter notebook", "postman", "selenium",
        "ci/cd", "linux", "api deployment",
        "model serialization", "inference pipeline", "mlops"
    },
    "Authentication and Cloud": {
        "jwt", "oauth", "firebase", "cloudinary",
        "aws", "azure", "google cloud", "gcp",
        "cloud computing", "authentication", "authorization"
    },
    "Business and Product": {
        "business analysis", "product management",
        "product strategy", "market research",
        "stakeholder management", "project management",
        "requirements gathering", "agile", "scrum",
        "roadmap planning", "user stories", "kpi"
    },
    "Design": {
        "ui design", "ux design", "ui/ux", "figma",
        "wireframing", "prototyping", "user research",
        "visual design", "adobe photoshop", "adobe illustrator"
    },
    "Marketing": {
        "digital marketing", "seo", "sem",
        "content marketing", "social media marketing",
        "email marketing", "google analytics",
        "campaign management", "lead generation",
        "market segmentation", "copywriting"
    },
}

SKILL_ALIASES = {
    "sklearn": "scikit-learn",
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "expressjs": "express.js",
    "postgres": "postgresql",
    "pyg": "pytorch geometric",
    "gnn": "graph neural networks",
    "gcn": "graph convolutional networks",
    "llm": "large language models",
    "llms": "large language models",
    "rag": "retrieval augmented generation",
    "rest apis": "rest api",
    "restful api": "rest api",
    "beautifulsoup4": "beautifulsoup",
    "nextjs": "next.js",
    "vector database": "vector databases",
    "spacy": "spacy",
}

ALL_SKILLS = {
    skill.lower().strip()
    for group in SKILLS.values()
    for skill in group
}
ALL_SKILLS.update(SKILL_ALIASES.keys())


# ============================================================
# NORMALIZATION AND SKILL EXTRACTION
# ============================================================

def normalize_text(text: Any) -> str:
    """Normalize whitespace and case while retaining technical punctuation."""
    text = str(text).lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[\u2010-\u2015]", "-", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def canonicalize_skill(skill: str) -> str:
    skill = normalize_text(skill)
    return SKILL_ALIASES.get(skill, skill)


def contains_phrase(text: str, phrase: str) -> bool:
    """Find a phrase without matching it inside a longer alphanumeric word."""
    phrase = normalize_text(phrase)
    if not phrase:
        return False
    pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text: str) -> list[str]:
    """Extract skills known to the local SKILLS dictionary."""
    normalized = normalize_text(text)
    found = set()

    # Check longer terms first to recognize multiword technical skills.
    for skill in sorted(ALL_SKILLS, key=len, reverse=True):
        if contains_phrase(normalized, skill):
            found.add(canonicalize_skill(skill))

    return sorted(found)


def categorize_skills(resume_skills: list[str]) -> dict[str, list[str]]:
    resume_set = {canonicalize_skill(skill) for skill in resume_skills}
    categorized = {}

    for category, skills in SKILLS.items():
        canonical_group = {canonicalize_skill(skill) for skill in skills}
        matched = sorted(resume_set.intersection(canonical_group))
        if matched:
            categorized[category] = matched

    return categorized


# ============================================================
# PDF AND CONTACT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path: str | Path) -> str:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError("Please provide a PDF file.")

    reader = PdfReader(str(path))

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise ValueError(
                "The PDF is encrypted. Please provide an accessible PDF."
            ) from exc

    text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()

    if not text:
        raise ValueError(
            "No selectable text was found. If this is a scanned PDF, add OCR."
        )

    return text


def extract_email(text: str) -> str | None:
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    matches = re.findall(pattern, text)
    return matches[0] if matches else None


def extract_phone(text: str) -> str | None:
    pattern = r"(?<!\w)(?:\+\d{1,3}[\s().-]*)?(?:\d[\s().-]*){9,12}\d(?!\w)"

    for match in re.findall(pattern, text):
        digits = re.sub(r"\D", "", match)
        if 10 <= len(digits) <= 13:
            return match.strip()

    return None


# ============================================================
# DATASET LOADING
# ============================================================

def load_datasets() -> pd.DataFrame:
    frames = []
    missing_files = []

    for filename in DATASET_FILES:
        path = DATASET_DIR / filename

        if not path.exists():
            missing_files.append(filename)
            continue

        frame = pd.read_csv(path)
        frame.columns = frame.columns.str.strip().str.lower()

        missing_columns = REQUIRED_COLUMNS - set(frame.columns)
        if missing_columns:
            raise ValueError(
                f"{filename} is missing required columns: "
                f"{sorted(missing_columns)}"
            )

        frame["source_file"] = filename
        frames.append(frame)

    if not frames:
        raise FileNotFoundError(
            f"No dataset CSVs were found in: {DATASET_DIR}"
        )

    if missing_files:
        print("Warning: missing dataset files:")
        for filename in missing_files:
            print(f"  - {filename}")

    data = pd.concat(frames, ignore_index=True)

    for column in ("job_title", "category", "required_skills"):
        data[column] = data[column].fillna("").astype(str).str.strip()

    data = data[
        (data["job_title"] != "") &
        (data["required_skills"] != "")
    ].copy()

    # Retain an explicit row identifier for tracing results to source rows.
    data = data.reset_index(drop=True)
    data["job_id"] = data.index.map(lambda index: f"job_{index + 1}")

    return data


# ============================================================
# PARSE REQUIRED SKILLS
# ============================================================

def parse_required_skills(value: Any) -> list[str]:
    """
    Parse a CSV required_skills cell.

    This expects skills separated by commas, semicolons, pipes, or newlines.
    If the CSV stores skills in another format, adjust this parser.
    """
    if value is None or pd.isna(value):
        return []

    text = str(value).strip()
    if not text:
        return []

    pieces = re.split(r"[,;|\n\r]+", text)
    skills = {
        canonicalize_skill(piece)
        for piece in pieces
        if piece.strip()
    }

    return sorted(skills)


# ============================================================
# CREATE ONE PROFILE PER JOB POSTING
# ============================================================

def dataset_skill_profiles(
    data: pd.DataFrame,
) -> dict[str, dict[str, Any]]:
    """
    Every CSV row becomes an individual job profile.
    Do not group Senior, Junior, Intern, and other postings together.
    """
    profiles = {}

    for _, row in data.iterrows():
        required_skills = set(parse_required_skills(row["required_skills"]))
        if not required_skills:
            continue

        job_id = str(row["job_id"])

        profiles[job_id] = {
            "job_id": job_id,
            "job_title": str(row["job_title"]),
            "category": str(row["category"]),
            "experience_level": str(row.get("experience_level", "")).strip(),
            "min_experience_years": row.get("min_experience_years", None),
            "max_experience_years": row.get("max_experience_years", None),
            "skills": required_skills,
            "description": str(row.get("description", "")),
            "source_file": str(row.get("source_file", "")),
        }

    return profiles


# ============================================================
# OPTIONAL EXPERIENCE FILTER
# ============================================================

def normalize_experience_level(value: str) -> str:
    value = normalize_text(value)
    aliases = {
        "entry level": "entry",
        "entry-level": "entry",
        "early career": "entry",
        "mid level": "mid",
        "mid-level": "mid",
        "middle": "mid",
        "senior level": "senior",
        "senior-level": "senior",
        "leadership": "lead",
        "principal level": "principal",
    }
    return aliases.get(value, value)


def experience_level_matches(
    profile_level: str,
    requested_level: str | None,
) -> bool:
    if not requested_level:
        return True

    if not profile_level:
        # If the dataset does not specify the level, don't assume a match.
        return False

    return (
        normalize_experience_level(profile_level)
        == normalize_experience_level(requested_level)
    )


# ============================================================
# RANK JOB POSTINGS BY SKILL COVERAGE
# ============================================================

def rank_job_titles(
    resume_skills: list[str],
    profiles: dict[str, dict[str, Any]],
    top_n: int = DEFAULT_TOP_N,
    min_match_percent: float = DEFAULT_MIN_MATCH_PERCENT,
    experience_level: str | None = None,
) -> list[dict[str, Any]]:
    """
    Score each posting using exact normalized skill coverage:

        matched required skills / all required skills * 100

    This is a transparent skill-coverage percentage, not a hiring probability.
    """
    if not 0 <= min_match_percent <= 100:
        raise ValueError("min_match_percent must be between 0 and 100.")

    resume_set = {canonicalize_skill(skill) for skill in resume_skills}
    results = []

    for profile in profiles.values():
        required_skills = {
            canonicalize_skill(skill)
            for skill in profile.get("skills", set())
        }

        if not required_skills:
            continue

        if not experience_level_matches(
            str(profile.get("experience_level", "")),
            experience_level,
        ):
            continue

        matched = resume_set.intersection(required_skills)
        missing = required_skills - resume_set

        coverage = len(matched) / len(required_skills) * 100

        if coverage < min_match_percent:
            continue

        results.append({
            "job_id": profile["job_id"],
            "job_title": profile["job_title"],
            "category": profile["category"],
            "experience_level": profile["experience_level"] or "Not specified",
            "fit_score": round(coverage, 2),
            "skill_coverage": round(coverage, 2),
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "matched_skill_count": len(matched),
            "required_skill_count": len(required_skills),
            "min_experience_years": profile["min_experience_years"],
            "max_experience_years": profile["max_experience_years"],
            "source_file": profile["source_file"],
        })

    results.sort(
        key=lambda item: (
            item["fit_score"],
            item["matched_skill_count"],
            -len(item["missing_skills"]),
        ),
        reverse=True,
    )

    return results[:top_n]


# ============================================================
# CATEGORY MATCHING
# ============================================================

def rank_categories(
    resume_skills: list[str],
    data: pd.DataFrame,
    top_n: int = 7,
) -> list[dict[str, Any]]:
    """
    Rank broad dataset categories by skill coverage.
    This score describes overlap with the category's combined vocabulary;
    it is not the same as an individual job-posting match.
    """
    resume_set = {canonicalize_skill(skill) for skill in resume_skills}
    category_skills: dict[str, set[str]] = {}

    for _, row in data.iterrows():
        category = str(row["category"]).strip() or "Unknown"
        category_skills.setdefault(category, set()).update(
            parse_required_skills(row["required_skills"])
        )

    results = []

    for category, required in category_skills.items():
        if not required:
            continue

        matched = resume_set.intersection(required)
        coverage = len(matched) / len(required) * 100

        results.append({
            "category": category,
            "fit_score": round(coverage, 2),
            "skill_coverage": round(coverage, 2),
            "matched_skills": sorted(matched),
            "matched_skill_count": len(matched),
            "profile_skill_count": len(required),
        })

    results.sort(
        key=lambda item: (item["fit_score"], item["matched_skill_count"]),
        reverse=True,
    )

    return results[:top_n]


# ============================================================
# COMPLETE RESUME ANALYSIS
# ============================================================

def analyze_resume(
    pdf_path: str | Path,
    data: pd.DataFrame | None = None,
    top_n: int = DEFAULT_TOP_N,
    min_match_percent: float = DEFAULT_MIN_MATCH_PERCENT,
    experience_level: str | None = None,
) -> dict[str, Any]:
    if data is None:
        data = load_datasets()

    raw_text = extract_pdf_text(pdf_path)
    resume_skills = extract_skills(raw_text)
    profiles = dataset_skill_profiles(data)

    return {
        "file_name": Path(pdf_path).name,
        "email": extract_email(raw_text),
        "phone_number": extract_phone(raw_text),
        "extracted_skills": resume_skills,
        "categorized_skills": categorize_skills(resume_skills),
        "category_matches": rank_categories(resume_skills, data),
        "job_title_matches": rank_job_titles(
            resume_skills=resume_skills,
            profiles=profiles,
            top_n=top_n,
            min_match_percent=min_match_percent,
            experience_level=experience_level,
        ),
        "extracted_text_length": len(raw_text),
        "dataset_rows_loaded": len(data),
        "minimum_match_percent": min_match_percent,
        "experience_level_filter": experience_level,
    }


# ============================================================
# PRINT RESULTS
# ============================================================

def print_analysis(result: dict[str, Any]) -> None:
    print("\n" + "=" * 72)
    print("RESUME ANALYSIS")
    print("=" * 72)
    print(f"File: {result['file_name']}")
    print(f"Email: {result['email'] or 'Not found'}")
    print(f"Phone: {result['phone_number'] or 'Not found'}")
    print(f"Dataset rows loaded: {result['dataset_rows_loaded']}")
    print(f"Minimum match threshold: {result['minimum_match_percent']}%")
    print(f"Experience filter: {result['experience_level_filter'] or 'None'}")

    print("\nEXTRACTED SKILLS")
    print("-" * 72)
    print(", ".join(result["extracted_skills"]) or "No known skills found.")

    print("\nCATEGORIZED SKILLS")
    print("-" * 72)
    if result["categorized_skills"]:
        for category, skills in result["categorized_skills"].items():
            print(f"{category}: {', '.join(skills)}")
    else:
        print("No categorized skills found.")

    print("\nBEST-FIT CATEGORIES")
    print("-" * 72)
    for item in result["category_matches"]:
        print(
            f"{item['category']}: {item['fit_score']}% coverage "
            f"({item['matched_skill_count']}/{item['profile_skill_count']} skills)"
        )

    print("\nBEST-FIT JOB POSTINGS")
    print("-" * 72)

    matches = result["job_title_matches"]
    if not matches:
        print(
            "No postings met the threshold. Lower min_match_percent, "
            "check the required_skills parser, or expand the skill dictionary."
        )

    for index, item in enumerate(matches, start=1):
        print(f"\n{index}. {item['job_title']} ({item['category']})")
        print(f"   Job ID: {item['job_id']}")
        print(f"   Experience level: {item['experience_level']}")
        print(
            f"   Skill coverage: {item['fit_score']}% "
            f"({item['matched_skill_count']}/{item['required_skill_count']})"
        )
        print(
            "   Matched: "
            + (", ".join(item["matched_skills"]) or "None")
        )
        print(
            "   Missing: "
            + (", ".join(item["missing_skills"]) or "None")
        )
        print(f"   Dataset: {item['source_file']}")

    print("\nNote: skill coverage is not a probability of getting hired.")
    print("=" * 72)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":
    # Update this path to your PDF resume.
    RESUME_PATH = (
        r"E:\Personal Projects\deep learning"
        r"\Ai_Resume_Analyser_project"
        r"\AI-ML Intern Resume - 95%.pdf"
    )

    # Set this to None to include every experience level.
    # Examples: "Intern", "Junior", "Mid-level", "Senior"
    EXPERIENCE_LEVEL = None

    dataset = load_datasets()

    result = analyze_resume(
        pdf_path=RESUME_PATH,
        data=dataset,
        top_n=10,
        min_match_percent=60.0,
        experience_level=EXPERIENCE_LEVEL,
    )

    print_analysis(result)
