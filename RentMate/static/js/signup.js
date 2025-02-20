// Function to toggle password visibility
function togglePassword(fieldId) {
    var passwordField = document.getElementById(fieldId);
    var passwordIcon = document.getElementById(fieldId + "-icon");

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
