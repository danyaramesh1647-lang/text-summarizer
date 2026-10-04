const $ = (id) => document.getElementById(id);
const textBox = $("text");
const genBtn = $("generate");
let lastSummary = "";

textBox.addEventListener("input", updateCounts);
genBtn.addEventListener("click", summarize);
$("clear").addEventListener("click", clearAll);
$("copy").addEventListener("click", copySummary);

function updateCounts() {
  const t = textBox.value.trim();
  const words = t ? t.split(/\s+/).length : 0;
  const sents = t ? (t.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || []).length : 0;
  $("c-words").textContent = `${words} words`;
  $("c-sent").textContent = `${sents} sentences`;
  $("c-chars").textContent = `${t.length} characters`;
}

async function summarize() {
  $("error").hidden = true;
  genBtn.disabled = true;
  genBtn.textContent = "Summarizing...";
  try {
    const res = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: textBox.value,
        length: document.querySelector('input[name="length"]:checked').value,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    render(data);
  } catch (err) {
    $("result").hidden = true;
    $("error").textContent = err.message;
    $("error").hidden = false;
  } finally {
    genBtn.disabled = false;
    genBtn.textContent = "Generate summary";
  }
}

function render(d) {
  lastSummary = d.summary;
  $("summary").textContent = d.summary;
  const s = d.stats;
  $("stats").textContent =
    `${s.words} words in ${s.sentences} sentences, reduced to ${s.summary_words} words in ${s.summary_sentences} sentences (${s.reduction}% shorter).`;
  $("keywords").textContent = d.keywords.length ? `Top keywords: ${d.keywords.join(", ")}` : "";

  const src = $("source");
  src.innerHTML = "";
  d.sentences.forEach((sent, i) => {
    const node = d.selected.includes(i) ? document.createElement("mark") : document.createElement("span");
    node.textContent = sent + " ";
    src.appendChild(node);
  });
  $("copy").textContent = "Copy summary";
  $("result").hidden = false;
}

async function copySummary() {
  try {
    await navigator.clipboard.writeText(lastSummary);
    $("copy").textContent = "Copied";
  } catch {
    $("copy").textContent = "Copy failed";
  }
  setTimeout(() => ($("copy").textContent = "Copy summary"), 1800);
}

function clearAll() {
  textBox.value = "";
  lastSummary = "";
  $("result").hidden = true;
  $("error").hidden = true;
  updateCounts();
  textBox.focus();
}