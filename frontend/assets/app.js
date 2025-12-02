const API = window.location.origin;
const ACTIVE_USER_KEY = "bitewise:active-user";

const state = {
  get userId() {
    const value = localStorage.getItem(ACTIVE_USER_KEY);
    return value ? Number(value) : null;
  },
  set userId(id) {
    if (id) {
      localStorage.setItem(ACTIVE_USER_KEY, String(id));
    } else {
      localStorage.removeItem(ACTIVE_USER_KEY);
    }
    updateUserBadge();
  },
};

const formatJSON = (payload) => JSON.stringify(payload, null, 2);

const toList = (value) =>
  value
    .split(/[\n,]/)
    .map((token) => token.trim())
    .filter(Boolean);

const requestJSON = async (path, options = {}) => {
  const response = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || `Request failed (${response.status})`);
  }
  return response.json();
};

const postJSON = (path, body) => requestJSON(path, { method: "POST", body: JSON.stringify(body) });

const escapeHTML = (str = "") =>
  String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");

const setOutput = (element, content, options = {}) => {
  if (!element) return;
  if (options.html) {
    element.innerHTML = content;
    return;
  }
  const text = typeof content === "string" ? content : formatJSON(content);
  element.innerHTML = `<pre>${escapeHTML(text)}</pre>`;
};

const formatDate = (value) => {
  if (!value) return "Unknown";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString();
};

const listOrEmpty = (items, fallback = "<p class=\"muted\">No data yet.</p>") =>
  items && items.length ? items.join("") : fallback;

const renderAnalysisSummary = (data) => {
  if (!data || data.error) {
    return `<p>${escapeHTML(data?.error || "No analysis yet.")}</p>`;
  }
  const reasons = listOrEmpty(
    (data.reasons || []).map((reason) => `<li>${escapeHTML(reason)}</li>`),
    "<li>Balanced macros detected.</li>"
  );
  const macros = Object.entries(data.macros || {}).map(
    ([key, value]) => `<li><span>${escapeHTML(key)}</span><strong>${escapeHTML(String(value))}</strong></li>`
  );
  return `
    <div class="result-card">
      <div class="rating-pill ${data.rating?.toLowerCase() || "mid"}">${escapeHTML(data.rating || "Score")}</div>
      <p>${escapeHTML(data.suggestion || "No suggestion yet.")}</p>
      <p class="muted">Detected: ${escapeHTML((data.detected_items || []).join(", ") || "Unknown items")}</p>
      <div class="result-grid">
        <div>
          <h4>Reasons</h4>
          <ul>${reasons}</ul>
        </div>
        <div>
          <h4>Macros snapshot</h4>
          <ul class="mini-grid">${macros.join("")}</ul>
        </div>
      </div>
    </div>
  `;
};

const renderPlan = (data) => {
  if (!data || data.error) {
    return `<p>${escapeHTML(data?.error || "Unable to build plan.")}</p>`;
  }
  const dayCards = listOrEmpty(
    (data.days || []).map(
      (day) => `
        <article class="day-card">
          <header>Day ${escapeHTML(String(day.day))}</header>
          <ul>
            ${day.meals
              .map(
                (meal) => `
                  <li>
                    <strong>${escapeHTML(meal.slot)}</strong>
                    <div>${escapeHTML(meal.item)}</div>
                    <small class="muted">$${escapeHTML(String(meal.price || 0))}</small>
                  </li>
                `
              )
              .join("")}
          </ul>
        </article>
      `
    )
  );
  return `
    <div class="result-card">
      <p>${escapeHTML(data.goal)} plan · Avg $${escapeHTML(String(data.average_cost_per_day))}/day</p>
      <p class="muted">Budget window: $${escapeHTML(String(data.budget?.min))} - $${escapeHTML(
    String(data.budget?.max)
  )}</p>
      <div class="result-list">${dayCards}</div>
    </div>
  `;
};

const renderSearchResults = (data, type = "text") => {
  if (!data) return "<p>No data.</p>";
  const cards = (data.results || []).map(
    (item) => `
      <article class="food-card">
        <div class="rating-pill ${item.rating?.toLowerCase() || "mid"}">${escapeHTML(item.rating || "Score")}</div>
        <h4>${escapeHTML(item.name)}</h4>
        <p>Health score: ${escapeHTML(String(item.health_score ?? "N/A"))}</p>
        <small class="muted">Tags: ${escapeHTML((item.tags || []).join(", ") || "none")}</small>
        ${
          item.alternatives && item.alternatives.length
            ? `<p class="muted">Alternatives: ${escapeHTML(item.alternatives.join(", "))}</p>`
            : ""
        }
      </article>
    `
  );
  const extra =
    type === "image"
      ? `<p class="muted">Labels: ${escapeHTML((data.labels || []).join(", ") || "none detected")}</p>`
      : "";
  return `
    <div class="result-card">
      ${extra}
      <div class="result-list">${cards.join("") || `<p>${escapeHTML(data.message || "No matches found.")}</p>`}</div>
    </div>
  `;
};

const renderHistory = (data) => {
  if (!data) return "<p>No history yet.</p>";
  const analyses = listOrEmpty(
    (data.analyses || []).map(
      (item) => `
        <li>
          <strong>${escapeHTML(item.rating)}</strong> · ${escapeHTML(item.detected_items.join(", ") || "Unknown")} 
          <small class="muted">${escapeHTML(new Date(item.created_at).toLocaleString())}</small>
        </li>
      `
    ),
    "<li>No analyses yet.</li>"
  );
  const plans = listOrEmpty(
    (data.meal_plans || []).map(
      (plan) => `
        <li>
          <strong>${escapeHTML(plan.goal)}</strong> · Budget ${escapeHTML(JSON.stringify(plan.budget || {}))}
          <small class="muted">${escapeHTML(new Date(plan.created_at).toLocaleString())}</small>
        </li>
      `
    ),
    "<li>No plans yet.</li>"
  );
  return `
    <div class="result-card">
      <h4>Analyses</h4>
      <ul>${analyses}</ul>
      <h4>Meal plans</h4>
      <ul>${plans}</ul>
    </div>
  `;
};

const renderNotificationsList = (data) => {
  if (!data) return "<p>No reminders yet.</p>";
  const cards = (data.notifications || []).map(
    (note) => `
      <article class="day-card">
        <header>${escapeHTML(note.category || "Reminder")}</header>
        <p>${escapeHTML(note.message)}</p>
        <small class="muted">Send at: ${escapeHTML(formatDate(note.send_at))}</small>
      </article>
    `
  );
  return `<div class="result-list">${cards.join("") || "<p>No reminders yet.</p>"}</div>`;
};

const renderNotificationAck = (data) =>
  `<p class="success">Reminder scheduled (ID ${escapeHTML(String(data.notification_id))}).</p>`;

const renderChatResponse = (data) => {
  if (!data) return "<p>No response yet.</p>";
  return `
    <div class="result-card">
      <p class="muted">You</p>
      <p>${escapeHTML(data.user || "")}</p>
      <p class="muted">BiteWise Coach</p>
      <p>${escapeHTML(data.bot || "🤖 No response from bot.")}</p>
    </div>
  `;
};

const renderFaqList = (faqs) => {
  const cards = (faqs || []).map(
    (item) => `
      <article class="day-card">
        <p><strong>Q:</strong> ${escapeHTML(item.question)}</p>
        <p><strong>A:</strong> ${escapeHTML(item.answer)}</p>
      </article>
    `
  );
  return `<div class="result-list">${cards.join("") || "<p>No FAQ available.</p>"}</div>`;
};

const updateUserBadge = () => {
  const badge = document.querySelector("#userBadge");
  if (!badge) return;
  const id = state.userId;
  badge.textContent = id ? `Active user #${id}` : "Guest session";
};

const highlightNav = (page) => {
  document.querySelectorAll("nav a[data-nav]").forEach((link) => {
    const isActive = link.dataset.nav === page;
    link.classList.toggle("active", isActive);
  });
};

const ensureUser = () => {
  if (!state.userId) {
    throw new Error("Create a profile first to personalize this action.");
  }
};

const initProfilePage = () => {
  const form = document.querySelector("#profileForm");
  const statusEl = document.querySelector("#profileStatus");
  const historyBtn = document.querySelector("#loadHistory");
  const historyOutput = document.querySelector("#historyOutput");

  const populateForm = (data) => {
    document.querySelector("#profileName").value = data.name;
    document.querySelector("#profileEmail").value = data.email;
    document.querySelector("#profileGoal").value = data.goal;
    document.querySelector("#profileLanguage").value = data.language;
    document.querySelector("#profileBudgetMin").value = data.budget.min;
    document.querySelector("#profileBudgetMax").value = data.budget.max;
    document.querySelector("#profilePreferences").value = (data.dietary_preferences || []).join(", ");
    document.querySelector("#profileAllergies").value = (data.allergies || []).join(", ");
  };

  const loadUser = async () => {
    if (!state.userId) return;
    try {
      const data = await requestJSON(`/users/${state.userId}`, { method: "GET" });
      populateForm(data);
      setOutput(statusEl, `Loaded user #${data.id}`);
    } catch (error) {
      setOutput(statusEl, `Unable to load user: ${error.message}`);
    }
  };

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      name: document.querySelector("#profileName").value,
      email: document.querySelector("#profileEmail").value,
      goal: document.querySelector("#profileGoal").value,
      language: document.querySelector("#profileLanguage").value,
      budget_min: Number(document.querySelector("#profileBudgetMin").value),
      budget_max: Number(document.querySelector("#profileBudgetMax").value),
      dietary_preferences: toList(document.querySelector("#profilePreferences").value),
      allergies: toList(document.querySelector("#profileAllergies").value),
    };
    const route = state.userId ? `/users/${state.userId}` : "/users";
    const method = state.userId ? "PATCH" : "POST";
    try {
      setOutput(statusEl, "Saving profile...");
      const data = await requestJSON(route, { method, body: JSON.stringify(payload) });
      state.userId = data.id;
      setOutput(statusEl, `Profile saved (#${data.id})`);
    } catch (error) {
      setOutput(statusEl, `Save failed: ${error.message}`);
    }
  });

  historyBtn?.addEventListener("click", async () => {
    try {
      ensureUser();
      setOutput(historyOutput, "Loading history...");
      const data = await requestJSON(`/users/${state.userId}/history`, { method: "GET" });
      setOutput(historyOutput, renderHistory(data), { html: true });
    } catch (error) {
      setOutput(historyOutput, error.message);
    }
  });

  loadUser();
};

const initAnalysisPage = () => {
  const imageButton = document.querySelector("#runImageAnalysis");
  const imageOutput = document.querySelector("#imageAnalysisOutput");
  const textButton = document.querySelector("#runTextAnalysis");
  const textOutput = document.querySelector("#textAnalysisOutput");

  imageButton?.addEventListener("click", async () => {
    const fileInput = document.querySelector("#analysisImageUpload");
    const file = fileInput?.files?.[0];
    if (!file) {
      alert("Select an image first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    if (state.userId) formData.append("user_id", state.userId);
    try {
      setOutput(imageOutput, "Analyzing image...");
      const response = await fetch(`${API}/upload`, { method: "POST", body: formData });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(detail.detail || "Upload failed");
      }
      const data = await response.json();
      setOutput(imageOutput, renderAnalysisSummary(data), { html: true });
    } catch (error) {
      setOutput(imageOutput, `Error: ${error.message}`);
    }
  });

  textButton?.addEventListener("click", async () => {
    const text = document.querySelector("#analysisIngredients").value;
    if (!text.trim()) {
      setOutput(textOutput, "Provide ingredients or a description first.");
      return;
    }
    const payload = {
      ingredients: toList(text),
      text_summary: text,
      goal: document.querySelector("#analysisGoal").value,
      budget_min: Number(document.querySelector("#analysisBudgetMin").value),
      budget_max: Number(document.querySelector("#analysisBudgetMax").value),
      user_id: state.userId,
    };
    try {
      setOutput(textOutput, "Scoring nutrition...");
      const data = await postJSON("/analyze", payload);
      setOutput(textOutput, renderAnalysisSummary(data), { html: true });
    } catch (error) {
      setOutput(textOutput, `Error: ${error.message}`);
    }
  });
};

const initPlansPage = () => {
  const button = document.querySelector("#generatePlan");
  const output = document.querySelector("#planOutput");
  button?.addEventListener("click", async () => {
    const payload = {
      user_id: state.userId,
      goal: document.querySelector("#planGoal").value,
      days: Number(document.querySelector("#planDays").value),
      budget_min: Number(document.querySelector("#planBudgetMin").value),
      budget_max: Number(document.querySelector("#planBudgetMax").value),
      preferences: toList(document.querySelector("#planPreferences").value),
      allergies: toList(document.querySelector("#planAllergies").value),
    };
    try {
      setOutput(output, "Generating plan...");
      const data = await postJSON("/meal-plans/generate", payload);
      setOutput(output, renderPlan(data), { html: true });
    } catch (error) {
      setOutput(output, `Error: ${error.message}`);
    }
  });
};

const initSearchPage = () => {
  const textOutput = document.querySelector("#searchOutput");
  document.querySelector("#runSearch")?.addEventListener("click", async () => {
    const query = document.querySelector("#searchQuery").value;
    if (!query.trim()) {
      setOutput(textOutput, "Type a query first.");
      return;
    }
    try {
      setOutput(textOutput, "Searching catalog...");
      const data = await postJSON("/search", { query });
      setOutput(textOutput, renderSearchResults(data), { html: true });
    } catch (error) {
      setOutput(textOutput, `Error: ${error.message}`);
    }
  });

  const imgOutput = document.querySelector("#imageSearchOutput");
  document.querySelector("#searchFromImage")?.addEventListener("click", async () => {
    const file = document.querySelector("#searchImageUpload")?.files?.[0];
    if (!file) {
      setOutput(imgOutput, "Select a photo first.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    try {
      setOutput(imgOutput, "Detecting foods...");
      const response = await fetch(`${API}/search/from-image`, { method: "POST", body: formData });
      if (!response.ok) {
        const detail = await response.json().catch(() => ({}));
        throw new Error(detail.detail || "Image search failed");
      }
      const data = await response.json();
      setOutput(imgOutput, renderSearchResults(data, "image"), { html: true });
    } catch (error) {
      setOutput(imgOutput, `Error: ${error.message}`);
    }
  });
};

const initSupportPage = () => {
  const notifOutput = document.querySelector("#notificationOutput");
  document.querySelector("#scheduleNotification")?.addEventListener("click", async () => {
    try {
      ensureUser();
      const payload = {
        user_id: state.userId,
        message: document.querySelector("#notificationMessage").value || "Hydrate & log your meal.",
        send_in_minutes: Number(document.querySelector("#notificationDelay").value) || 60,
      };
      setOutput(notifOutput, "Scheduling reminder...");
      const data = await postJSON("/notifications", payload);
      setOutput(notifOutput, renderNotificationAck(data), { html: true });
    } catch (error) {
      setOutput(notifOutput, error.message);
    }
  });

  document.querySelector("#loadNotifications")?.addEventListener("click", async () => {
    try {
      ensureUser();
      setOutput(notifOutput, "Fetching reminders...");
      const response = await fetch(
        `${API}/notifications${state.userId ? `?user_id=${state.userId}` : ""}`
      );
      if (!response.ok) throw new Error("Unable to load notifications");
      const data = await response.json();
      setOutput(notifOutput, renderNotificationsList(data), { html: true });
    } catch (error) {
      setOutput(notifOutput, error.message);
    }
  });

  const chatOutput = document.querySelector("#chatOutput");
  document.querySelector("#askCoach")?.addEventListener("click", async () => {
    const question = document.querySelector("#chatQuestion").value;
    if (!question.trim()) {
      setOutput(chatOutput, "Ask a question first.");
      return;
    }
    try {
      setOutput(chatOutput, "Connecting to support...");
      const data = await postJSON("/support/chat", { text: question });
      setOutput(chatOutput, renderChatResponse(data), { html: true });
    } catch (error) {
      setOutput(chatOutput, error.message);
    }
  });

  document.querySelector("#loadFaq")?.addEventListener("click", async () => {
    try {
      setOutput(chatOutput, "Loading FAQ...");
      const response = await fetch(`${API}/support/faq`);
      const data = await response.json();
      setOutput(chatOutput, renderFaqList(data), { html: true });
    } catch (error) {
      setOutput(chatOutput, error.message);
    }
  });
};

const initPage = (page) => {
  switch (page) {
    case "profile":
      initProfilePage();
      break;
    case "analysis":
      initAnalysisPage();
      break;
    case "plans":
      initPlansPage();
      break;
    case "search":
      initSearchPage();
      break;
    case "support":
      initSupportPage();
      break;
    default:
      break;
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page || "home";
  highlightNav(page);
  updateUserBadge();
  initPage(page);
});

