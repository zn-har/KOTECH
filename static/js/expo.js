    document.getElementById('registration-form').addEventListener('submit', function(e) {
      e.preventDefault();
      // Form submission logic would go here
      alert('Registration submitted successfully!');
    });

    // Display file name when selected
    document.getElementById('abstract').addEventListener('change', function() {
      if (this.files && this.files.length > 0) {
        const fileName = this.files[0].name;
        const fileLabel = this.closest('.file-input').querySelector('.file-input-label');
        fileLabel.textContent = fileName;
      }
    });

    // Check viewport width and adjust spacing on resize
    function adjustLayoutForViewport() {
      const viewportWidth = window.innerWidth;
      const root = document.documentElement;

      if (viewportWidth < 360) {
        root.style.setProperty('--border-radius', '6px');
      } else {
        root.style.setProperty('--border-radius', '12px');
      }
    }

    // Initialize and add event listener for resize
    window.addEventListener('resize', adjustLayoutForViewport);
    adjustLayoutForViewport();