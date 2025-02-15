async function validateForm(event) {
    event.preventDefault(); // Prevent form submission if validation fails

    let isValid = true;

    // Get input values
    let firstname = document.getElementById("firstname");
    let lastname = document.getElementById("lastname");
    let email = document.getElementById("email");
    let username = document.getElementById("username");
    let password = document.getElementById("password");
    let confirmpassword = document.getElementById("confirmpassword");

    // Clear previous errors
    document.querySelectorAll(".error-message").forEach(el => el.textContent = "");
    document.querySelectorAll(".input-container input").forEach(el => el.classList.remove("error"));

    // Validate First Name
    if (firstname.value.trim() === "") {
        showError(firstname, "First Name is required.");
        isValid = false;
    }

    // Validate Last Name
    if (lastname.value.trim() === "") {
        showError(lastname, "Last Name is required.");
        isValid = false;
    }

    // Validate Email
    if (!email.value.includes("@gmail.com")) {
        showError(email, "Email must be a valid Gmail address.");
        isValid = false;
    } else {
        let emailExists = await checkEmailExists(email.value);
        if (emailExists) {
            showError(email, "Email already exists. Please choose another.");
            isValid = false;
        }
    }
    
    if (username.value.trim() === "") {
        showError(username, "Username is required.");
        isValid = false;
    } else if (username.value.trim().length < 4) {
        showError(username, "Username must be at least 4 characters.");
        isValid = false;
    }
    

    // Validate Password Complexity
    let passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordPattern.test(password.value)) {
        showError(password, "Password must contain at least 8 characters, one uppercase, one lowercase, one number, and one special character.");
        isValid = false;
    }
    // Validate Last Name
    if (confirmpassword.value.trim() === "") {
        showError(confirmpassword, "Confirm password is required.");
        isValid = false;
    }
    // Validate Confirm Password
    if (password.value !== confirmpassword.value) {
        showError(confirmpassword, "Passwords do not match.");
        isValid = false;
    }

    // If the form is valid, submit it
    if (isValid) {
        document.querySelector("form").submit();
    }
}

// Function to check if username exists (AJAX request)
async function checkEmailExists(email) {
    try {
        let response = await fetch(`/check-email/?email=${email}`);
        let data = await response.json();
        return data.exists; // Returns true if username exists, false otherwise
    } catch (error) {
        console.error("Error checking username:", error);
        return false;
    }
}

// Function to show error messages
function showError(input, message) {
    let errorSpan = document.getElementById(input.id + "-error");
    errorSpan.textContent = message;
    input.classList.add("error");
}
