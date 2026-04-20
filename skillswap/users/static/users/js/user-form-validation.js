document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const phoneInput = document.getElementById("phone");

    const streetNumber = document.getElementById("street_number");
    const postalCode = document.getElementById("postal_code");


    // محدود کردن ورودی کیبورد برای شماره تلفن
    phoneInput.addEventListener("keypress", function (e) {
        const char = String.fromCharCode(e.which);
        if (!/[0-9\+]/.test(char)) {
            e.preventDefault();
        }
    });


    streetNumber.addEventListener("keypress", function (e) {
        const char = String.fromCharCode(e.which);
        if (!/[0-9\+]/.test(char)) {
            e.preventDefault();
        }
    });


    postalCode.addEventListener("keypress", function (e) {
        const char = String.fromCharCode(e.which);
        if (!/[0-9\+]/.test(char)) {
            e.preventDefault();
        }
    });




    // جلوگیری از پیست کردن متن غیرمجاز در تلفن
    phoneInput.addEventListener("paste", function (e) {
        const paste = (e.clipboardData || window.clipboardData).getData("text");
        if (!/^\+?\d*$/.test(paste)) {
            e.preventDefault();
        }
    });

    form.addEventListener("submit", function (e) {
        clearErrors();

        let have_error = false;

        const username = document.getElementById("user_name");
        const email = document.getElementById("email");
        const phone = document.getElementById("phone");
        const fileInput = document.getElementById("profile_image_url");

        if (!username.value.trim()) {
            showError(username, "Benutzername ist erforderlich.");
            have_error = true;
        }

        if (!email.value.trim()) {
            showError(email, "Email ist erforderlich.");
            have_error = true;
        } else if (!validateEmail(email.value.trim())) {
            showError(email, "Ungültige Email-Adresse.");
            have_error = true;
        }

        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const fileName = file.name.toLowerCase();
            const allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;

            if (file.type === "application/pdf" || file.type === "application/svg" || fileName.endsWith('.pdf') || fileName.endsWith('.svg')) {
                showError(fileInput, "PDF-Dateien sind nicht erlaubt! Bitte wählen Sie ein Bild.");
                have_error = true;
            } else if (!allowedExtensions.exec(fileName)) {
                showError(fileInput, "Nur Bilddateien (JPG, PNG, GIF) sind erlaubt.");
                have_error = true;
            } else if (file.size > 5 * 1024 * 1024) { // مثال: محدودیت ۵ مگابایت
                showError(fileInput, "Die Datei ist zu groß (Max. 5MB).");
                have_error = true;
            }
        }

        // اگر خطایی وجود داشت، فرم ارسال نشود
        if (have_error) {
            e.preventDefault();
            // اسکرول به اولین خطا برای تجربه کاربری بهتر
            const firstError = document.querySelector(".is-invalid");
            if (firstError) firstError.scrollIntoView({behavior: "smooth", block: "center"});
        }
    });

    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // تابع نمایش خطا زیر هر فیلد
    function showError(inputElement, message) {
        inputElement.classList.add("is-invalid"); // قرمز کردن کادر اینپوت

        // ایجاد یا پیدا کردن المان نمایش متن خطا
        let errorDiv = inputElement.parentElement.querySelector(".invalid-feedback");

        // اگر فیلد عکس است (چون input مخفی است)، خطا را در نگهدارنده والد نشان بده
        if (inputElement.id === "profile_image_url") {
            errorDiv = inputElement.closest(".d-flex").querySelector(".invalid-feedback");
        }

        if (errorDiv) {
            errorDiv.innerText = message;
            errorDiv.style.display = "block";
        }
    }

    // تابع پاکسازی خطاها
    function clearErrors() {
        const inputs = form.querySelectorAll(".form-control, .form-select");
        inputs.forEach(input => {
            input.classList.remove("is-invalid");
        });
        const errorMessages = form.querySelectorAll(".invalid-feedback");
        errorMessages.forEach(msg => {
            msg.innerText = "";
            msg.style.display = "none";
        });
    }
});