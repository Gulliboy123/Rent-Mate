document.querySelector("form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent form submission if validation fails

    let isValid = true;
    let username = document.getElementById("username");
    let password = document.getElementById("password");

    // Clear previous errors
    document.querySelectorAll(".error-message").forEach(el => el.textContent = "");
    document.querySelectorAll(".input-group input").forEach(el => el.classList.remove("error"));

    // Validate Username
    if (username.value.trim() === "") {
        showError(username, "Username is required.");
        isValid = false;
    }

    // Validate Password
    if (password.value.trim() === "") {
        showError(password, "Password is required.");
        isValid = false;
    }

    // If username and password are provided, check credentials
    if (isValid) {
        let loginValid = await checkUserCredentials(username.value, password.value);
        if (loginValid === "user_not_found") {
            showError(username, "Username does not exist.");
            isValid = false;
        } else if (loginValid === "password_incorrect") {
            showError(password, "Password is incorrect.");
            isValid = false;
        }
    }

    // If validation passes, submit the form
    if (isValid) {
    }
});

async function checkUserCredentials(username, password) {
    try {
        let response = await fetch(`/check-credentials/?username=${username}&password=${password}`);
        let data = await response.json();
        return data.status;  // Should return 'user_not_found', 'password_incorrect', or 'success'
    } catch (error) {
        console.error("Error checking credentials:", error);
        return "error";  // Error case
    }
}

// Function to show error messages
function showError(input, message) {
    let errorSpan = document.getElementById(input.id + "-error");
    errorSpan.textContent = message;
    input.classList.add("error");
}

// Function to toggle password visibility
function togglePassword() {
    var passwordField = document.getElementById("password");
    var passwordIcon = document.getElementById("password-icon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        passwordIcon.classList.remove("fa-eye");
        passwordIcon.classList.add("fa-eye-slash");
    } else {
        passwordField.type = "password";
        passwordIcon.classList.remove("fa-eye-slash");
        passwordIcon.classList.add("fa-eye");
    }
}

