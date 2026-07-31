/**
 * dashboard.js — تحديث حالة الطلبات
 */

/** قراءة CSRF token من الكوكي */
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

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.status-select').forEach(select => {
        select.addEventListener('change', async () => {
            const orderId = select.dataset.orderId;
            const newStatus = select.value;
            const card = select.closest('.order-card');
            const badge = card.querySelector('.badge');

            try {
                const response = await fetch(`/dashboard/orders/${orderId}/status/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify({ status: newStatus }),
                });

                const data = await response.json();

                if (!response.ok || !data.success) {
                    throw new Error(data.error || 'فشل تحديث الحالة');
                }

                // تحديث الشارة
                badge.className = `badge badge-${data.status}`;
                badge.textContent = data.status_display;
            } catch (error) {
                alert(error.message);
            }
        });
    });
});
