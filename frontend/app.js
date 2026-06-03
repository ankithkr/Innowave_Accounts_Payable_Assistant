const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const filePreview = document.getElementById("filePreview");
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

    uploadBtn.disabled = false;
}


// Upload button

uploadBtn.addEventListener("click", () => {

    if (!selectedFile) {
        return;
    }

    const formData = new FormData();
    formData.append('invoice', selectedFile);

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';

    fetch('/upload', {
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
        filePreview.innerHTML = `Uploaded: <strong>${data.filename}</strong> (${data.size} bytes)`;
        alert('Upload successful: ' + data.path);
    }).catch((err) => {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload Invoice';
        alert('Upload error: ' + err.message);
    });

});