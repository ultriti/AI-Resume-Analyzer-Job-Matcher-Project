const textInput = document.getElementById("textInput");
const analyzeBtn = document.getElementById("analyzeBtn");

const resultSection = document.getElementById("resultSection");

const errorBox = document.getElementById("errorBox");
const errorMessage = document.getElementById("errorMessage");

const categoryLabel = document.getElementById("categoryLabel");
const confidenceValue = document.getElementById("confidenceValue");

const probabilityList = document.getElementById("probabilityList");

const charCount = document.getElementById("charCount");

// ---------------------------------------
// Character counter
// ---------------------------------------

textInput.addEventListener("input", () => {


charCount.textContent =
    `${textInput.value.length} / 2000`;


});

// ---------------------------------------
// Predict
// ---------------------------------------

analyzeBtn.addEventListener("click", predictJob);

async function predictJob() {


const text = textInput.value.trim();


// -----------------------------------
// Empty input
// -----------------------------------

if (!text) {

    showError("Please enter some job information.");

    resultSection.classList.add("hidden");

    return;
}


// -----------------------------------
// Reset UI
// -----------------------------------

hideError();

resultSection.classList.add("hidden");

analyzeBtn.disabled = true;

analyzeBtn.innerHTML =
    "Predicting...";


try {

    // --------------------------------
    // Send request to FastAPI
    // --------------------------------

    const response = await fetch("/predict", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            text: text

        })

    });


    // --------------------------------
    // Read backend response
    // --------------------------------

    const data = await response.json();


    // --------------------------------
    // Backend error
    // --------------------------------

    if (!response.ok) {

        throw new Error(
            data.detail || "Prediction failed."
        );

    }


    // --------------------------------
    // Display predicted category
    // --------------------------------

    categoryLabel.textContent =
        data.prediction_emotion;


    // --------------------------------
    // Display confidence
    // --------------------------------

    confidenceValue.textContent =
        `${(data.confidence * 100).toFixed(2)}%`;


    // --------------------------------
    // Clear previous probabilities
    // --------------------------------

    probabilityList.innerHTML = "";


    // --------------------------------
    // Display all probabilities
    // --------------------------------

    for (
        const [label, probability]
        of Object.entries(data.all_probabilities)
    ) {

        const percentage =
            probability * 100;


        const row =
            document.createElement("div");

        row.className =
            "probability-row";


        row.innerHTML = `

            <div class="probability-label">
                ${label}
            </div>

            <div class="progress-container">

                <div
                    class="progress-bar"
                    style="width: ${percentage}%"
                ></div>

            </div>

            <div class="probability-value">
                ${percentage.toFixed(2)}%
            </div>

        `;


        probabilityList.appendChild(row);

    }


    // --------------------------------
    // Show result
    // --------------------------------

    resultSection.classList.remove("hidden");


} catch (error) {

    console.error(error);

    showError(
        error.message ||
        "Something went wrong while predicting."
    );


} finally {

    analyzeBtn.disabled = false;

    analyzeBtn.innerHTML =
        `Predict Category <span>→</span>`;

}


}

// ---------------------------------------
// Show error
// ---------------------------------------

function showError(message) {


errorMessage.textContent = message;

errorBox.classList.remove("hidden");


}

// ---------------------------------------
// Hide error
// ---------------------------------------

function hideError() {


errorBox.classList.add("hidden");

errorMessage.textContent = "";


}
