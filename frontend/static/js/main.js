/* ============================================================
   Task Manager — Main JavaScript
   ============================================================ */

// Auto-dismiss flash messages after 4s
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => el.remove(), 4000);
  });

  // Highlight overdue tasks
  highlightOverdue();
});

function highlightOverdue() {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  document.querySelectorAll('.due-date').forEach(el => {
    const text = el.textContent.trim().replace('📅', '').trim();
    const d = new Date(text);
    if (!isNaN(d) && d < today) el.classList.add('overdue');
  });
}

// Quick status update (tasks list page)
async function updateTaskStatus(select) {
  const taskId = select.dataset.taskId;
  const status = select.value;
  try {
    const res = await fetch(`/tasks/${taskId}/status`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    if (res.ok) {
      const card = document.getElementById(`task-${taskId}`);
      if (card) {
        card.style.transition = 'opacity .3s';
        card.style.opacity = '0.5';
        setTimeout(() => location.reload(), 400);
      }
    }
  } catch (err) {
    console.error('Status update failed:', err);
  }
}
