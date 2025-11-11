const API_BASE_URL = "http://127.0.0.1:8000";
const uploadBtn = document.getElementById("uploadBtn");
const cleanBtn = document.getElementById("cleanBtn");
const featureSelectionBtn = document.getElementById("featureSelection")
const generateChartBtn = document.getElementById("generateChartBtn");
let uploadedFile;
let cleanData; // will store cleaned data
let datasetColumns = [];

// Upload file
document.getElementById("fileInput").addEventListener("change", async () => {
    uploadedFile = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", uploadedFile);

    console.log("Uploading file:", uploadedFile);

    try {
        const response = await fetch(`${API_BASE_URL}/upload/`, {
            method: "POST",
            body: formData
        });
        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
            console.error(data.trace);
            return;
        }

        datasetColumns = data.columns;
        document.getElementById("datasetInfo").innerHTML = `
            <p>Filename: ${data.filename}</p>
            <p>Rows: ${data.num_rows}, Columns: ${data.num_columns}</p>
            <p>Columns: ${data.columns.join(", ")}</p>
            <p>Number of duplicaes: ${data.duplicates}</p>
            <p>Number of missing values in each colum: ${JSON.stringify(data.missing_values)}</p>
            <p>Number of outliers: ${JSON.stringify(data.outliers_detected)}</p>
        `;
    } catch (err) {
        console.error(err);
        alert("Failed to upload file.");
    }
});

// Clean data
const removeOutliersCheckbox = document.getElementById("removeOutliers");
const outlierMethodContainer = document.getElementById("outlierMethodContainer");

removeOutliersCheckbox.addEventListener("change", () => {
    if (removeOutliersCheckbox.checked) {
        outlierMethodContainer.style.display = "block"; // show dropdown
    } else {
        outlierMethodContainer.style.display = "none"; // hide dropdown
    }
});

cleanBtn.addEventListener("click", async () => {
    if (!uploadedFile) {
        alert("Upload a file first.");
        return;
    }

    // Capture User input from the HTML file
    const removeOutliers = document.getElementById("removeOutliers").checked;
    const outlierMethod = document.getElementById("outlierMethod").value;

    // assigns user input the FormData variable/container
    const formData = new FormData();
    formData.append("file", uploadedFile);
    formData.append("remove_outliers", removeOutliers);
    formData.append("outlier_method", outlierMethod);

    try {
        // Sends data in FormData to backend to perform necessary function in /clean/
        const response = await fetch(`${API_BASE_URL}/clean/`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Server error during cleaning");

        //awaits Json format response from backend
        const data = await response.json();
        // stores response in a variable and sends it to HTML file for output on user interface
        cleanDataReport = data.cleaned_report;
        cleanData = data.cleaned_data
        if (Array.isArray(cleanDataReport) && cleanDataReport.length > 0) {
            datasetColumns = Object.keys(cleanDataReport[0]);
        } else {
            datasetColumns = [];
        }
        document.getElementById("cleanReport").innerHTML = `
            ✅ Data cleaned successfully!<br><br>
            <strong>Report:</strong><pre>${JSON.stringify(data.cleaned_report, null, 2)}</pre>
        `;

    } 
    catch (err) {
        console.error(err);
        alert("❌ Failed to clean data. Check console for details.");
    }
});

featureSelectionBtn.addEventListener("click", async () =>{
    if (!cleanData) {
        alert("Clean your data first!");
        return;
    }
    const chartType = document.getElementById("chartType").value;
    try {
        const response = await fetch(`${API_BASE_URL}/analysis`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({cleaned_data: cleanData, chart_type: chartType})
        });
        if (!response.ok) throw new Error("Server error during cleaning");
        const data = await response.json();
        xAxisFeatures = data.X_axis || [];
        yAxisFeatures = data.Y_axis || [];
        groupFeatures = data.Group || [];
        document.getElementById("featuresSelected").innerHTML = `
            <label>Select X-axis:</label>
            <select id="xAxisSelect">
                ${xAxisFeatures.map(col => `<option value="${col}">${col}</option>`).join("")}
            </select>

            <label>Select Y-axis:</label>
            <select id="yAxisSelect">
                ${yAxisFeatures.map(col => `<option value="${col}">${col}</option>`).join("")}
            </select>

            <label>Select Group / Color (Optional):</label>
            <select id="groupSelect">
                <option value="">None</option>
                ${groupFeatures.map(col => `<option value="${col}">${col}</option>`).join("")}
            </select>
        `;
    }
    catch (err) {
        console.error(err);
        alert("❌ Failed to clean data. Check console for details.");
    }
})