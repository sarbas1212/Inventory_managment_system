/* ============================================================
   InventoryPro — Application JavaScript
   Sidebar toggle, dark mode, toasts, table search
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
    initDarkMode();
    initDjangoToasts();
    initTableSearch();
    initPublicNavScroll();
});

/* ─── Sidebar Toggle ────────────────────────────────────────── */
function initSidebar() {
    const body = document.body;
    const toggleBtn = document.getElementById('sidebar-toggle');
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    // Restore saved state
    if (localStorage.getItem('sidebar-collapsed') === 'true') {
        body.classList.add('sidebar-collapsed');
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            body.classList.toggle('sidebar-collapsed');
            localStorage.setItem('sidebar-collapsed', body.classList.contains('sidebar-collapsed'));
        });
    }

    // Mobile sidebar
    if (mobileBtn && sidebar) {
        mobileBtn.addEventListener('click', () => {
            sidebar.classList.toggle('mobile-open');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', () => {
            sidebar?.classList.remove('mobile-open');
        });
    }
}

/* ─── Dark / Light Mode ─────────────────────────────────────── */
function initDarkMode() {
    const toggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    const saved = localStorage.getItem('theme');

    if (saved) {
        html.setAttribute('data-theme', saved);
    }

    if (toggle) {
        updateThemeIcon(toggle, html.getAttribute('data-theme'));
        toggle.addEventListener('click', () => {
            const current = html.getAttribute('data-theme');
            const next = current === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            updateThemeIcon(toggle, next);
        });
    }
}

function updateThemeIcon(btn, theme) {
    const icon = btn.querySelector('i');
    if (icon) {
        icon.className = theme === 'light' ? 'bi bi-moon-stars-fill' : 'bi bi-sun-fill';
    }
}

/* ─── Toast Notifications ───────────────────────────────────── */
function initDjangoToasts() {
    // Convert Django messages into toasts
    const djangoMessages = document.querySelectorAll('[data-django-message]');
    djangoMessages.forEach(el => {
        const msg = el.getAttribute('data-django-message');
        const tag = el.getAttribute('data-django-tag') || 'info';
        showToast(msg, tag);
        el.remove();
    });
}

function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-exclamation-triangle-fill',
        warning: 'bi-exclamation-circle-fill',
        info: 'bi-info-circle-fill'
    };

    const toast = document.createElement('div');
    toast.className = `toast-item toast-${type}`;
    toast.innerHTML = `
        <i class="bi ${icons[type] || icons.info}"></i>
        <span>${message}</span>
        <button class="toast-dismiss" onclick="dismissToast(this)">&times;</button>
    `;

    container.appendChild(toast);

    // Auto-dismiss after 5s
    setTimeout(() => dismissToast(toast.querySelector('.toast-dismiss')), 5000);
}

function dismissToast(btnOrEl) {
    const toast = btnOrEl.closest ? btnOrEl.closest('.toast-item') : btnOrEl;
    if (toast) {
        toast.classList.add('toast-fade-out');
        setTimeout(() => toast.remove(), 300);
    }
}

/* ─── Table Search ──────────────────────────────────────────── */
function initTableSearch() {
    document.querySelectorAll('[data-table-search]').forEach(input => {
        const targetId = input.getAttribute('data-table-search');
        const table = document.getElementById(targetId);
        if (!table) return;

        input.addEventListener('input', () => {
            const query = input.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    });
}

/* ─── Public Nav Scroll Effect ──────────────────────────────── */
function initPublicNavScroll() {
    const nav = document.querySelector('.public-nav');
    if (!nav) return;

    const check = () => {
        nav.classList.toggle('scrolled', window.scrollY > 20);
    };

    window.addEventListener('scroll', check, { passive: true });
    check();
}
