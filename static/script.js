// Auto-refresh dashboard every 30 seconds
if (window.location.pathname === '/') {
    setInterval(() => {
        location.reload();
    }, 30000);
}

// Confirm before deleting
document.querySelectorAll('.btn-danger').forEach(btn => {
    btn.addEventListener('click', (e) => {
        if (!confirm('Are you sure you want to delete this switch?')) {
            e.preventDefault();
        }
    });
});
