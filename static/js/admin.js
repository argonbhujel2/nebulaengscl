document.addEventListener('DOMContentLoaded', function() {
  // Sidebar toggle
  const toggle = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.admin-sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', () => sidebar.classList.toggle('open'));
  }

  // Delete confirmation
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', function(e) {
      if (!confirm(this.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });

  // Image preview
  document.querySelectorAll('input[type="file"][data-preview]').forEach(input => {
    input.addEventListener('change', function() {
      const preview = document.querySelector(this.dataset.preview);
      if (preview && this.files[0]) {
        const reader = new FileReader();
        reader.onload = e => { preview.src = e.target.result; preview.style.display = 'block'; };
        reader.readAsDataURL(this.files[0]);
      }
    });
  });

  // Flash auto-dismiss
  document.querySelectorAll('.flash').forEach(f => {
    setTimeout(() => { f.style.opacity = '0'; setTimeout(() => f.remove(), 300); }, 4000);
  });
});
