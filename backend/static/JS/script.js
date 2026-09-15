// Error function 
function addErrorClass($element) {
    $element.closest(".rs-form-group").addClass("error").removeClass("success");
}

// COMMON INPUTS (Email, First Name, Last Name)
$("#email, #first-name, #last-name").on("keyup input", function() {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z-]+\.[a-zA-Z]{2,}$/;
    const nameRegex = /^[A-Za-z]+(?:[ '-][A-Za-z]+)*$/;
    
    const inputValue = $(this).val(); 
    // FIXED: Swapped parent().next() out to safely look within the local form group
    const $errorText = $(this).closest(".rs-form-group").find(".error-message");

    if (inputValue === "") {
        addErrorClass($(this)); 
        $errorText.removeClass("d-none text-success").addClass("d-block text-danger");

        if ($(this).is("#email")) {
            $errorText.text("Enter your email");
        } else if ($(this).is("#first-name")) {
            $errorText.text("Enter your first name");
        } else if ($(this).is("#last-name")) {
            $errorText.text("Enter your last name");
        }
    }
    // Email Validation Check
    else if ($(this).is("#email") && !emailRegex.test(inputValue)) {
        addErrorClass($(this)); 
        $errorText.removeClass("d-none text-success").addClass("d-block text-danger").text("Enter valid email address.");
    }
    // First Name Validation Check
    else if ($(this).is("#first-name") && !nameRegex.test(inputValue)) {
        addErrorClass($(this)); 
        $errorText.removeClass("d-none text-success").addClass("d-block text-danger").text("Enter a valid name (letters only).");
    }
    // Last Name Validation Check
    else if ($(this).is("#last-name") && !nameRegex.test(inputValue)) {
        addErrorClass($(this)); 
        $errorText.removeClass("d-none text-success").addClass("d-block text-danger").text("Enter a valid name (letters only).");
    }
    // Success State Pass
    else {
        $(this).closest(".rs-form-group").removeClass("error").addClass("success");
        $errorText.removeClass("d-block text-danger").addClass("d-none").text("");
    }
});


// 2. PASSWORD INPUTS (Password, Re-Type Password)
$("#password, #re-password").on("keyup input", function () {
    const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;

    const $passwordGroup = $("#password").closest(".rs-form-group");
    const strengthBars = $passwordGroup.find(".password-strength .bar");

    function updateStrengthBars(activeBars) {
        strengthBars.each(function (index) {
            if (index < activeBars) {
                $(this).addClass("active");
            } else {
                $(this).removeClass("active");
            }
        });
    }

    const inputValue = $(this).val();
    const passwordValue = $("#password").val();
    const $errorMessage = $(this).closest(".rs-form-group").find(".error-message");

    let score = 0;

    if (passwordValue.length >= 8) score++;
    if (/[A-Z]/.test(passwordValue)) score++;
    if (/[a-z]/.test(passwordValue)) score++;
    if (/\d/.test(passwordValue)) score++;
    if (/[!@#$%^&*]/.test(passwordValue)) score++;

    // Password and strength bar
    if ($(this).is("#password")) {
        if (passwordValue === "") {
            addErrorClass($(this));
            $errorMessage
                .removeClass("d-none text-success")
                .addClass("d-block text-danger")
                .text("Enter your password");

            updateStrengthBars(0);
            return false;
        }

        if (score <= 2) {
            updateStrengthBars(1);
        } else if (score === 3) {
            updateStrengthBars(2);
        } else if (score === 4) {
            updateStrengthBars(3);
        } else {
            updateStrengthBars(4);
        }

        if (!passwordRegex.test(passwordValue)) {
            addErrorClass($(this));
            $errorMessage
                .removeClass("d-none text-success")
                .addClass("d-block text-danger")
                .text("Enter valid Password.");
            return false;
        }

        $(this).closest(".rs-form-group").removeClass("error").addClass("success");
        $errorMessage
            .removeClass("d-none text-danger")
            .addClass("d-block text-success")
            .text("Strong");

        updateStrengthBars(4);
        return true;
    }

    // Re-Typed password 
    if ($(this).is("#re-password")) {
        if (inputValue === "") {
            addErrorClass($(this));
            $errorMessage
                .removeClass("d-none text-success")
                .addClass("d-block text-danger")
                .text("Re-Type your password");
            return false;
        }

        if (inputValue !== passwordValue) {
            addErrorClass($(this));
            $errorMessage
                .removeClass("d-none text-success")
                .addClass("d-block text-danger")
                .text("Passwords do not match.");
            return false;
        }

        $(this).closest(".rs-form-group").removeClass("error").addClass("success");
        $errorMessage
            .removeClass("d-block text-danger text-success")
            .addClass("d-none")
            .text("");

        return true;
    }
});

const eyeButton = document.querySelectorAll(".eye-btn");

eyeButton.forEach(function (button) {
    button.addEventListener("click", function() {
        const inputBox = button.parentElement;
        const input = inputBox.querySelector("input");
        const icon = button.querySelector("i");

        if (input.type === "password") {
            input.type = "text";

            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        }
        else{
            input.type = "password";

            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
    });
});

