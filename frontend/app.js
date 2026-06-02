const API_BASE = "http://localhost:8000/api";

// ─── Upload Logic ───────────────────────────────────────────

const fileInput = document.getElementById("file-input");
const dropZone = document.getElementById("drop-zone");
const uploadStatus = document.getElementById("upload-status");

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) uploadFile(fileInput.files[0]);
});

// Drag and drop
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  if (file) uploadFile(file);
});

async function uploadFile(file) {
  showStatus("info", `⏳ Uploading "${file.name}"...`);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Upload failed");

    showStatus(
      "success",
      `✅ "${data.filename}" uploaded! ${data.chunks_indexed} chunks indexed.`
    );
  } catch (err) {
    showStatus("error", `❌ Error: ${err.message}`);
  }
}

function showStatus(type, message) {
  uploadStatus.className = `status-box ${type}`;
  uploadStatus.textContent = message;
  uploadStatus.classList.remove("hidden");
}

// ─── Query Logic ────────────────────────────────────────────

const queryInput = document.getElementById("query-input");
const answerSection = document.getElementById("answer-section");
const answerText = document.getElementById("answer-text");
const sourcesSection = document.getElementById("sources-section");
const sourcesList = document.getElementById("sources-list");
const loading = document.getElementById("loading");
const askBtn = document.getElementById("ask-btn");

queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") askQuestion();
});

function setQuery(chip) {
  queryInput.value = chip.textContent;
  queryInput.focus();
}

async function askQuestion() {
  const question = queryInput.value.trim();
  if (!question) return;

  // UI state
  askBtn.disabled = true;
  answerSection.classList.add("hidden");
  loading.classList.remove("hidden");

  try {
    const res = await fetch(`${API_BASE}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Query failed");

    // Show answer
    answerText.textContent = data.answer;
    answerSection.classList.remove("hidden");

    // Show sources
    if (data.sources && data.sources.length > 0) {
      sourcesList.innerHTML = data.sources
        .map(
          (s) => `
          <div class="source-item">
            <div class="source-meta">📄 ${s.file} — Page ${s.page}</div>
            <div class="source-snippet">${s.snippet}</div>
          </div>`
        )
        .join("");
      sourcesSection.classList.remove("hidden");
    } else {
      sourcesSection.classList.add("hidden");
    }
  } catch (err) {
    answerText.textContent = `❌ Error: ${err.message}`;
    answerSection.classList.remove("hidden");
    sourcesSection.classList.add("hidden");
  } finally {
    loading.classList.add("hidden");
    askBtn.disabled = false;
  }
}