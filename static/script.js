const textInput = document.getElementById("textInput");
const textInputArea = document.getElementById("textInputArea");
const resumeFile = document.getElementById("resumeFile");
const resumeModeNote = document.getElementById("resumeModeNote");
const predictBtn = document.getElementById("predictBtn");
const resumeBtn = document.getElementById("resumeBtn");

const resultSection = document.getElementById("resultSection");
const errorBox = document.getElementById("errorBox");
const errorMessage = document.getElementById("errorMessage");
const categoryLabel = document.getElementById("categoryLabel");
const confidenceValue = document.getElementById("confidenceValue");
const resultModeLabel = document.getElementById("resultModeLabel");
const probabilityList = document.getElementById("probabilityList");
const resumeDetails = document.getElementById("resumeDetails");
const jobTitle = document.getElementById("jobTitle");
const skillCount = document.getElementById("skillCount");
const skillList = document.getElementById("skillList");
const jobMatchList = document.getElementById("jobMatchList");
const charCount = document.getElementById("charCount");

textInput.addEventListener("input", () => {
    charCount.textContent = `${textInput.value.length} / 2000`;
});

resumeFile.addEventListener("change", () => {
    const hasResume = Boolean(resumeFile.files[0]);
    textInputArea.classList.toggle("hidden", hasResume);
    textInput.disabled = hasResume;
    resumeModeNote.classList.toggle("hidden", !hasResume);
    hideError();
});

predictBtn.addEventListener("click", predictText);
resumeBtn.addEventListener("click", analyzeResume);

async function predictText() {
    const text = textInput.value.trim();
    if (!text) {
        showError("Enter job or skills information to predict a category.");
        resultSection.classList.add("hidden");
        return;
    }

    await submitAnalysis({
        button: predictBtn,
        loadingLabel: "Predicting...",
        endpoint: "/predict",
        options: {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        },
        isResume: false
    });
}

async function analyzeResume() {
    const file = resumeFile.files[0];
    if (!file) {
        showError("Choose a PDF resume to analyze.");
        resultSection.classList.add("hidden");
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        showError("Please choose a PDF resume.");
        resultSection.classList.add("hidden");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    await submitAnalysis({
        button: resumeBtn,
        loadingLabel: "Analyzing resume...",
        endpoint: "/analyze-resume",
        options: { method: "POST", body: formData },
        isResume: true
    });
}

async function submitAnalysis({ button, loadingLabel, endpoint, options, isResume }) {
    hideError();
    resultSection.classList.add("hidden");
    resumeDetails.classList.add("hidden");
    button.disabled = true;
    predictBtn.disabled = true;
    resumeBtn.disabled = true;
    button.dataset.originalLabel = button.textContent.trim();
    button.textContent = loadingLabel;

    try {
        const response = await fetch(endpoint, options);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed.");
        }

        if (!data.all_probabilities || typeof data.all_probabilities !== "object") {
            throw new Error("The server returned an invalid prediction response.");
        }
        if (isResume && !Array.isArray(data.job_analysis)) {
            throw new Error("The resume response did not include role skill matches.");
        }

        renderPrediction(data, isResume);
        if (isResume) {
            renderResumeAnalysis(data);
        }
        resultSection.classList.remove("hidden");
        resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
        console.error(error);
        showError(error.message || "Something went wrong while analyzing.");
    } finally {
        button.disabled = false;
        predictBtn.disabled = false;
        resumeBtn.disabled = false;
        button.textContent = button.dataset.originalLabel;
    }
}

function renderPrediction(data, isResume) {
    categoryLabel.textContent = data.prediction_category || data.prediction_emotion;
    confidenceValue.textContent = `${(Number(data.confidence) * 100).toFixed(2)}%`;
    resultModeLabel.textContent = isResume ? "Resume analysis" : "Text prediction";

    probabilityList.replaceChildren();
    for (const [label, probabilityValue] of Object.entries(data.all_probabilities)) {
        const percentage = Number(probabilityValue) * 100;
        const row = document.createElement("div");
        row.className = "probability-row";

        const name = document.createElement("div");
        name.className = "probability-label";
        name.textContent = label;

        const progressContainer = document.createElement("div");
        progressContainer.className = "progress-container";
        const progressBar = document.createElement("div");
        progressBar.className = "progress-bar";
        progressBar.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
        progressContainer.appendChild(progressBar);

        const value = document.createElement("div");
        value.className = "probability-value";
        value.textContent = `${percentage.toFixed(2)}%`;

        row.append(name, progressContainer, value);
        probabilityList.appendChild(row);
    }
}

function renderResumeAnalysis(data) {
    jobTitle.textContent = data.job_title || "Not detected";
    skillList.replaceChildren();
    for (const skill of data.skills) {
        const item = document.createElement("li");
        item.textContent = skill;
        skillList.appendChild(item);
    }
    skillCount.textContent = String(data.skills.length);
    renderJobMatches(data.job_analysis);
    resumeDetails.classList.remove("hidden");
}

function renderJobMatches(matches) {
    jobMatchList.replaceChildren();

    if (matches.length === 0) {
        const emptyState = document.createElement("p");
        emptyState.className = "empty-match-state";
        emptyState.textContent = "No role comparisons were returned for this resume.";
        jobMatchList.appendChild(emptyState);
        return;
    }

    matches.forEach((match, index) => {
        const card = document.createElement("details");
        card.className = "job-match-card";
        card.open = index === 0;

        const summary = document.createElement("summary");
        const role = document.createElement("span");
        role.className = "match-role";
        role.textContent = match.role;
        const score = Number(match.score);
        const scoreLabel = document.createElement("span");
        scoreLabel.className = "match-score";
        scoreLabel.textContent = `${score.toFixed(2)}% match`;
        summary.append(role, scoreLabel);

        const meter = document.createElement("div");
        meter.className = "match-meter";
        const meterFill = document.createElement("span");
        meterFill.style.width = `${Math.max(0, Math.min(100, score))}%`;
        meter.appendChild(meterFill);

        const skillColumns = document.createElement("div");
        skillColumns.className = "match-skill-columns";
        skillColumns.append(
            createSkillGroup("Matched skills", match.matched_skills, "matched"),
            createSkillGroup("Skills to build", match.missing_skills, "missing")
        );

        card.append(summary, meter, skillColumns);
        jobMatchList.appendChild(card);
    });
}

function createSkillGroup(title, skills, kind) {
    const group = document.createElement("div");
    group.className = `match-skill-group ${kind}`;
    const heading = document.createElement("h5");
    heading.textContent = title;
    const list = document.createElement("ul");

    if (skills.length === 0) {
        const emptyItem = document.createElement("li");
        emptyItem.className = "no-skills";
        emptyItem.textContent = kind === "matched" ? "No matches yet" : "All listed skills matched";
        list.appendChild(emptyItem);
    } else {
        for (const skill of skills) {
            const item = document.createElement("li");
            item.textContent = skill;
            list.appendChild(item);
        }
    }

    group.append(heading, list);
    return group;
}

function showError(message) {
    errorMessage.textContent = message;
    errorBox.classList.remove("hidden");
}

function hideError() {
    errorBox.classList.add("hidden");
    errorMessage.textContent = "";
}
