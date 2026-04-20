document.getElementById('profile_image_url').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('preview-img');
    const errorDiv = document.getElementById('error-profile_image_url');

    if (file) {
        const fileName = file.name.toLowerCase();
        if (fileName.endsWith('.pdf') || fileName.endsWith('.svg')) {
            alert("PDF und SVG sind nicht erlaubt!");
            this.value = "";
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
        };
        reader.readAsDataURL(file);

        errorDiv.innerText = "";
        this.classList.remove('is-invalid');
    }
});