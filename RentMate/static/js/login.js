document.addEventListener("DOMContentLoaded", function () {
    // Attach event listener for form submission
    document.querySelector("form").addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent form submission if validation fails

        const username = document.getElementById("username");
        const password = document.getElementById("password");

        // Clear previous errors
        clearErrors();

        let isValid = true;

        // Validate inputs
        isValid &= validateUsername(username);
        isValid &= validatePassword(password);

        // If valid, check credentials
        if (isValid) {
            const loginValid = await checkUserCredentials(username.value, password.value);
            isValid &= handleLoginResponse(loginValid, username, password);
        }

        // If everything is valid, submit the form
        if (isValid) {
            document.querySelector("form").submit();
        }
    });

    // Function to clear previous error messages
    function clearErrors() {
        document.querySelectorAll(".error-message").forEach(el => el.textContent = "");
        document.querySelectorAll(".input-group input").forEach(el => el.classList.remove("error"));
    }

    // Validate username field
    function validateUsername(username) {
        if (username.value.trim() === "") {
            showError(username, "Username is required.");
            return false;
        }
        return true;
    }

    // Validate password field
    function validatePassword(password) {
        if (password.value.trim() === "") {
            showError(password, "Password is required.");
            return false;
        }
        return true;
    }

    // Check if the credentials are correct
    async function checkUserCredentials(username, password) {
        try {
            const response = await fetch(`/check-credentials/?username=${username}&password=${password}`);
            const data = await response.json();
            return data.status; // Should return 'user_not_found', 'password_incorrect', or 'success'
        } catch (error) {
            console.error("Error checking credentials:", error);
            return "error"; // Error case
        }
    }

    // Handle the login response
    function handleLoginResponse(status, username, password) {
        switch (status) {
            case "user_not_found":
                showError(username, "Username does not exist.");
                return false;
            case "password_incorrect":
                showError(password, "Password is incorrect.");
                return false;
            case "success":
                return true;
            default:
                showError(username, "An error occurred. Please try again.");
                return false;
        }
    }

    // Function to show error messages
    function showError(input, message) {
        const errorSpan = document.getElementById(input.id + "-error");
        errorSpan.textContent = message;
        input.classList.add("error");
    }

    // Function to toggle password visibility
    function togglePassword() {
        const passwordField = document.getElementById("password");
        const passwordIcon = document.getElementById("password-icon");

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

    // Ensure the password toggle works when clicking the button
    document.getElementById("pass-toggle").addEventListener("click", togglePassword);
});
