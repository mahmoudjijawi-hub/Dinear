/**
 * dashboard.js — تحديث حالة الطلبات
 */

function getCsrfToken() {
    const name = 'csrftoken';
    if (document.cookie) {
        for (const cookie of document.cookie.split(';')) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                return decodeURIComponent(trimmed.substring(name.length + 1));
            }
        }
    }
    return typeof CSRF_TOKEN !== 'undefined' ? CSRF_TOKEN : '';
}

function buildApiUrl(path) {
    const params = new URLSearchParams();
    if (typeof AUTH_TOKEN !== 'undefined' && AUTH_TOKEN) {
        params.set('auth_token', AUTH_TOKEN);
    }
    if (typeof INGRESS_TOKEN !== 'undefined' && INGRESS_TOKEN) {
        params.set('_ingress_token', INGRESS_TOKEN);
    }
    const qs = params.toString();
    return qs ? `${path}?${qs}` : path;
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.status-select').forEach(select => {
        select.addEventListener('change', async () => {
            const orderId = select.dataset.orderId;
            const newStatus = select.value;
            const card = select.closest('.order-card');
            const badge = card.querySelector('.badge');

            try {
                const response = await fetch(buildApiUrl(`/dashboard/orders/${orderId}/status/`), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    credentials: 'include',
                    body: JSON.stringify({ status: newStatus }),
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || 'فشل تحديث الحالة');
                }

                badge.className = `badge badge-${data.status}`;
                badge.textContent = data.status_display;
            } catch (error) {
                alert(error.message);
            }
        });
    });
});
