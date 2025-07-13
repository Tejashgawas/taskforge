let sessionId = null;

function showMsg(message, targetId = "sessionResult") {
  const el = document.getElementById(targetId);
  if (el) {
    el.innerText = message;
  }
}

// 🔐 Login
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (data.success) {
      sessionId = data.data.session_id;
      showMsg("✅ Logged in successfully!", "sessionResult");
    } else {
      showMsg("❌ Login failed: " + data.message, "sessionResult");
    }
  } catch (err) {
    showMsg("❌ Error logging in.", "sessionResult");
  }
});

// 🔐 Check Session
async function checkSession() {
  try {
    const res = await fetch(`/me?session_id=${sessionId}`);
    const data = await res.json();
    showMsg(data.success ? "✅ Session Active" : "⚠️ Session Invalid", "sessionResult");
  } catch {
    showMsg("❌ Error checking session", "sessionResult");
  }
}

// 🔐 Logout
async function logout() {
  try {
    const res = await fetch(`/logout?session_id=${sessionId}`);
    const data = await res.json();
    showMsg(data.message, "sessionResult");
  } catch {
    showMsg("❌ Error logging out", "sessionResult");
  }
}
//otp
async function sendOTP() {
  const email = document.getElementById("otpEmail").value;

  try {
    const res = await fetch("/send-otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });
    const data = await res.json();

    if (data.success) {
      const otp = data.data?.otp || "(hidden)";
      showMsg(`📩 OTP sent successfully!\n🔐 OTP for demo: ${otp}`, "otpResult");
    } else {
      showMsg(`❌ ${data.message}`, "otpResult");
    }

  } catch {
    showMsg("❌ Failed to send OTP", "otpResult");
  }
}
// 📩 Verify OTP
async function verifyOTP() {
  const email = document.getElementById("otpEmail").value;
  const otp = document.getElementById("otpCode").value;

  try {
    const res = await fetch("/verify-otp", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ email, otp })
    });
    const data = await res.json();
    showMsg(data.message || "OTP check done", "otpResult");
  } catch {
    showMsg("❌ OTP verification failed", "otpResult");
  }
}

// 📄 Fetch Article
async function fetchArticle() {
  const id = document.getElementById("articleId").value;

  try {
    const res = await fetch(`/articles/${id}`);
    const data = await res.json();

    if (data.success) {
      const article = data.data;
      const source = data.message || "Source unknown";

      showMsg(`📰 [${source}]\n\n📌 ${article.title}\n${article.content}`, "articleResult");
    } else {
      showMsg("❌ Article not found", "articleResult");
    }

  } catch {
    showMsg("❌ Failed to fetch article", "articleResult");
  }
}
async function clearArticleCache() {
  const id = document.getElementById("articleId").value;
  if (!id) return showMsg("❌ Enter article ID", "articleResult");

  try {
    const res = await fetch(`/articles/${id}/clear-cache`, {
      method: "POST"
    });
    const data = await res.json();
    showMsg(`🧹 ${data.message}`, "articleResult");
  } catch {
    showMsg("❌ Failed to clear cache", "articleResult");
  }
}
async function getArticleTTL() {
  const id = document.getElementById("articleId").value;
  if (!id) return showMsg("❌ Enter article ID", "articleResult");

  try {
    const res = await fetch(`/articles/${id}/ttl`);
    const data = await res.json();

    if (data.success) {
      showMsg(`⏱️ ${data.message}`, "articleResult");
    } else {
      showMsg(`❌ ${data.message}`, "articleResult");
    }
  } catch {
    showMsg("❌ Failed to get TTL", "articleResult");
  }
}

async function hitLimited() {
  try {
    const res = await fetch("/limited-endpoint");
    const data = await res.json();
    console.log("🔥 Response data:", data); // <== TEMP LOG

    if (!res.ok) {
      showMsg(`❌ ${data?.message  || "Rate limit error"}`, "rateLimitResult");
    } else {
      showMsg(`✅ ${data?.message || "Success!"}`, "rateLimitResult");
    }

  } catch (err) {
    showMsg("❌ Failed to hit endpoint or invalid JSON", "rateLimitResult");
  }
}

