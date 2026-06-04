const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const filePreview = document.getElementById("filePreview");
const resultPanel = document.getElementById("resultPanel");
const uploadBtn = document.getElementById("uploadBtn");

let selectedFile = null;


// Open file explorer

dropZone.addEventListener("click", () => {
    fileInput.click();
});


// File selection

fileInput.addEventListener("change", (event) => {

    if (event.target.files.length > 0) {

        selectedFile = event.target.files[0];

        showSelectedFile();
    }
});


// Drag over

dropZone.addEventListener("dragover", (event) => {

    event.preventDefault();

    dropZone.classList.add("drag-over");
});


// Drag leave

dropZone.addEventListener("dragleave", () => {

    dropZone.classList.remove("drag-over");
});


// Drop file

dropZone.addEventListener("drop", (event) => {

    event.preventDefault();

    dropZone.classList.remove("drag-over");

    if (event.dataTransfer.files.length > 0) {

        selectedFile = event.dataTransfer.files[0];

        showSelectedFile();
    }
});


function showSelectedFile() {

    filePreview.innerHTML =
        `Selected: <strong>${selectedFile.name}</strong>`;

    resultPanel.innerHTML = '<h2>Workflow result will appear here.</h2>';
    uploadBtn.disabled = false;
}

function renderResult(result) {
    if (!result || Object.keys(result).length === 0) {
        resultPanel.innerHTML = '<h2>No workflow result returned.</h2>';
        return;
    }

    const fields = [
        ['Invoice ID', result.invoice_id],
        ['Invoice Number', result.invoice_number],
        ['Invoice Status', result.invoice_status],
        ['Current Step', result.current_step],
        ['Extraction Status', result.extraction_status],
        ['Validation Status', result.validation_status],
        ['Approval Status', result.approval_status],
        ['Recommended Approver', result.recommended_approver],
        ['Risk Score', result.risk_score],
        ['Risk Assessment', result.risk_assessment],
        ['Final Recommendation', result.final_recommendation],
        ['Error Message', result.error_message],
    ];

    const summaryHtml = fields.map(([label, value]) => {
        if (value === undefined || value === null || value === '') {
            return '';
        }
        return `<div class="result-row"><span>${label}</span><strong>${value}</strong></div>`;
    }).join('');

    const actionItems = result.recommendations && result.recommendations.length > 0
        ? `<div class="result-section"><h3>Action Items</h3><ul>${result.recommendations.map(item => `<li>${item}</li>`).join('')}</ul></div>`
        : '';

    const exceptions = result.exceptions && result.exceptions.length > 0
        ? `<div class="result-section"><h3>Exceptions</h3><pre>${JSON.stringify(result.exceptions, null, 2)}</pre></div>`
        : '';

    const extracted = result.extracted_data && Object.keys(result.extracted_data).length > 0
        ? `<div class="result-section"><h3>Extracted Data</h3><pre>${JSON.stringify(result.extracted_data, null, 2)}</pre></div>`
        : '';

    resultPanel.innerHTML = `
        <h2>Workflow Result</h2>
        <div class="result-summary">${summaryHtml}</div>
        ${actionItems}
        ${extracted}
        ${exceptions}
    `;
}


// Upload button

uploadBtn.addEventListener("click", () => {

    if (!selectedFile) {
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';

    fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData
    }).then(async (res) => {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload Invoice';
        if (!res.ok) {
            const text = await res.text();
            alert('Upload failed: ' + res.status + '\n' + text);
            return;
        }
        const data = await res.json();
        const result = data.result || {};

        filePreview.innerHTML = `Uploaded: <strong>${selectedFile.name}</strong> (${selectedFile.size} bytes)`;
        renderResult(result);
    }).catch((err) => {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload Invoice';
        alert('Upload error: ' + err.message);
    });

});