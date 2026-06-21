// ── API Helpers ──────────────────────────────────────────────────────────────

async function api(url, method = 'GET', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function apiRaw(url, method = 'GET', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) opts.body = JSON.stringify(body);
  return fetch(url, opts);
}

// ── Modal ────────────────────────────────────────────────────────────────────

function openModal(title, html) {
  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalBody').innerHTML = html;
  document.getElementById('modal').classList.add('open');
  document.getElementById('modalOverlay').classList.add('open');
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
  document.getElementById('modalOverlay').classList.remove('open');
}

// Close on Escape
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ── Toast ────────────────────────────────────────────────────────────────────

let toastTimer;
function showToast(msg, type = 'success') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = `toast show ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 3200);
}
