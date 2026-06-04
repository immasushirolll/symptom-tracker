// ── Mobile menu ────────────────────────────────────────────────────────────────
function toggleMenu() {
  document.getElementById("mobileMenu").classList.toggle("open");
}

// ── Format seconds → M:SS ─────────────────────────────────────────────────────
function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

// ── Simple fade-in on load ─────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  document.body.style.opacity = "0";
  document.body.style.transition = "opacity 0.35s ease";
  requestAnimationFrame(() => { document.body.style.opacity = "1"; });
});
