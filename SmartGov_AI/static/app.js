const $ = (id) => document.getElementById(id);

async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}
function showMessage(target, message, isError = false) {
  target.classList.remove("hidden");
  target.innerHTML = "";
  const p = document.createElement("p");
  p.textContent = message;
  if (isError) p.style.color = "#a12626";
  target.appendChild(p);
}
function addText(parent, tag, text, className = "") {
  const el = document.createElement(tag);
  el.textContent = text ?? "";
  if (className) el.className = className;
  parent.appendChild(el);
  return el;
}
function addLink(parent, label, url) {
  const a = document.createElement("a");
  a.textContent = label;
  a.href = url;
  a.target = "_blank";
  a.rel = "noopener noreferrer";
  parent.appendChild(a);
}
function renderResult(target, data) {
  target.classList.remove("hidden");
  target.innerHTML = "";
  Object.entries(data).forEach(([key, value]) => {
    if (value === null || value === undefined || value === "") return;
    const label = key.replaceAll("_", " ").replace(/\b\w/g, c => c.toUpperCase());
    addText(target, "p", `${label}: ${value}`);
  });
}
$("assistant-submit").addEventListener("click", async () => {
  const question = $("assistant-question").value.trim();
  if (!question) return showMessage($("assistant-result"), "Please enter a question.", true);
  const target = $("assistant-result");
  showMessage(target, "Searching the demo FAQ...");
  try {
    const data = await api("/api/assistant", {
      method: "POST",
      body: JSON.stringify({ question, language: $("assistant-language").value })
    });
    target.innerHTML = "";
    addText(target, "h3", "Assistant response");
    addText(target, "p", data.answer);
    addText(target, "p", data.disclaimer);
    addLink(target, "Open official resource", data.source_url);
  } catch (error) { showMessage(target, error.message, true); }
});

$("scheme-submit").addEventListener("click", async () => {
  const target = $("scheme-results");
  target.innerHTML = "Searching...";
  try {
    const data = await api("/api/schemes", {
      method: "POST",
      body: JSON.stringify({ query: $("scheme-query").value.trim(), audience: $("scheme-audience").value })
    });
    target.innerHTML = "";
    if (!data.results.length) return showMessage(target, "No matching demo schemes found. Try another keyword or choose All audiences.");
    data.results.forEach(item => {
      const card = document.createElement("article"); card.className = "scheme-result";
      addText(card, "h4", item.name);
      addText(card, "p", item.description);
      addText(card, "p", `Audience: ${item.audience}`);
      addText(card, "p", item.eligibility_note);
      addLink(card, "Visit official government portal ↗", item.official_url);
      target.appendChild(card);
    });
  } catch (error) { showMessage(target, error.message, true); }
});

$("tracker-submit").addEventListener("click", async () => {
  const id = $("application-id").value.trim();
  const target = $("tracker-result");
  if (!id) return showMessage(target, "Enter an application reference.", true);
  showMessage(target, "Looking up demo record...");
  try {
    const data = await api(`/api/applications/${encodeURIComponent(id)}`);
    renderResult(target, { application_id: data.application_id, service_name: data.service_name, status: data.status, last_updated: data.last_updated, next_step: data.next_step, notice: "Fictional demonstration record" });
  } catch (error) { showMessage(target, error.message, true); }
});

$("grievance-submit").addEventListener("click", async () => {
  const description = $("grievance-description").value.trim();
  const target = $("grievance-result");
  if (description.length < 8) return showMessage(target, "Please describe the issue in at least 8 characters.", true);
  showMessage(target, "Creating local demo ticket...");
  try {
    const data = await api("/api/grievances", {
      method: "POST",
      body: JSON.stringify({
        citizen_name: $("citizen-name").value.trim() || "Demo Citizen",
        locality: $("locality").value.trim(),
        description
      })
    });
    renderResult(target, {
      ticket_id: data.ticket_id, category: data.category, priority: data.priority,
      department: data.department, status: data.status,
      possible_duplicate: data.possible_duplicate || "No likely duplicate detected",
      notice: "Saved locally only; not sent to a government department."
    });
    $("grievance-description").value = "";
    await loadGrievances();
    await loadDashboard();
  } catch (error) { showMessage(target, error.message, true); }
});

async function loadGrievances() {
  const target = $("grievance-list");
  target.innerHTML = "Loading tickets...";
  try {
    const data = await api("/api/grievances");
    target.innerHTML = "";
    if (!data.grievances.length) return showMessage(target, "No demo grievances have been submitted yet.");
    data.grievances.slice(0, 8).forEach(item => {
      const card = document.createElement("article"); card.className = "ticket-item";
      addText(card, "h4", `${item.ticket_id} · ${item.category}`);
      addText(card, "p", `${item.priority} — ${item.status}`);
      addText(card, "p", item.description);
      if (item.possible_duplicate) addText(card, "p", `Possible duplicate of ${item.possible_duplicate}`);
      target.appendChild(card);
    });
  } catch (error) { showMessage(target, error.message, true); }
}
$("refresh-grievances").addEventListener("click", loadGrievances);

function renderBars(target, rows, labelKey) {
  target.innerHTML = "";
  if (!rows.length) return addText(target, "p", "No data available yet.");
  const max = Math.max(...rows.map(r => r.count), 1);
  rows.forEach(row => {
    const wrap = document.createElement("div");
    const label = document.createElement("div"); label.className = "bar-label";
    addText(label, "span", row[labelKey]); addText(label, "strong", String(row.count));
    wrap.appendChild(label);
    const track = document.createElement("div"); track.className = "bar-track";
    const fill = document.createElement("div"); fill.className = "bar-fill";
    fill.style.width = `${(row.count / max) * 100}%`;
    track.appendChild(fill); wrap.appendChild(track); target.appendChild(wrap);
  });
}
async function loadDashboard() {
  try {
    const data = await api("/api/dashboard");
    const kpis = $("dashboard-kpis"); kpis.innerHTML = "";
    [
      ["Total applications", data.kpis.total_applications],
      ["Pending applications", data.kpis.pending_applications],
      ["Grievances", data.kpis.total_grievances],
      ["High-priority flags", data.kpis.high_priority_recommendations]
    ].forEach(([label, value]) => {
      const card = document.createElement("div"); card.className = "kpi";
      addText(card, "span", label); addText(card, "strong", String(value)); kpis.appendChild(card);
    });
    renderBars($("application-status-chart"), data.application_statuses, "status");
    renderBars($("grievance-category-chart"), data.grievance_categories, "category");
    const tbody = $("dashboard-tickets"); tbody.innerHTML = "";
    if (!data.recent_grievances.length) {
      const tr = document.createElement("tr"); const td = document.createElement("td");
      td.colSpan = 5; td.textContent = "No grievance tickets yet."; tr.appendChild(td); tbody.appendChild(tr);
    }
    data.recent_grievances.forEach(ticket => {
      const tr = document.createElement("tr");
      [ticket.ticket_id, ticket.category, ticket.priority, ticket.status].forEach(value => {
        const td = document.createElement("td"); td.textContent = value; tr.appendChild(td);
      });
      const td = document.createElement("td");
      const select = document.createElement("select");
      ["Submitted", "In Progress", "Resolved", "Closed"].forEach(status => {
        const opt = document.createElement("option"); opt.value = status; opt.textContent = status;
        if (status === ticket.status) opt.selected = true;
        select.appendChild(opt);
      });
      const btn = document.createElement("button"); btn.className = "button secondary small"; btn.textContent = "Save";
      btn.addEventListener("click", async () => {
        try {
          await api(`/api/grievances/${encodeURIComponent(ticket.ticket_id)}`, {
            method: "PATCH", body: JSON.stringify({ status: select.value })
          });
          await loadDashboard(); await loadGrievances();
        } catch (error) { alert(error.message); }
      });
      td.append(select, btn); tr.appendChild(td); tbody.appendChild(tr);
    });
  } catch (error) {
    showMessage($("dashboard-kpis"), error.message, true);
  }
}
$("refresh-dashboard").addEventListener("click", loadDashboard);

loadGrievances();
loadDashboard();
