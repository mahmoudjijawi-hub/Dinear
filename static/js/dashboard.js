/**
 * dashboard.js — تحديث حالة الطلبات
 */

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
                        'X-CSRFToken': CSRF_TOKEN,
                    },
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
