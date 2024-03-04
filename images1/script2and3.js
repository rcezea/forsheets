function showSignUpModal() {
    document.getElementById('signUpModal').style.display = 'block';
    document.body.classList.add('blur-background');
    document.body.style.overflow = 'hidden'; // Disable scrolling
}

function showSignInModal() {
    document.getElementById('signInModal').style.display = 'block';
    document.body.classList.add('blur-background');
    document.body.style.overflow = 'hidden'; // Disable scrolling
}

function closeModal() {
    document.getElementById('signUpModal').style.display = 'none';
    document.getElementById('signInModal').style.display = 'none';
    document.body.classList.remove('blur-background');
    document.body.style.overflow = 'auto'; // Enable scrolling
}


// Sign-up Validation
    function validateSignUp() {
        var email = document.getElementById("signupEmail").value; 
        var password = document.getElementById("signupPassword").value;
        var confirmPassword = document.getElementById("signupConfirmPassword").value; 

    // Check if email ends with '.babcock.edu.ng'
    if (!email.endsWith('.babcock.edu.ng')) {
        alert("Email must end with '.babcock.edu.ng'");
        return false;
    }

    if (password.length < 8) {
        alert("Password must be at least 8 characters long");
        return false;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return false;
    }

    return true;
}

    
// Sign-in Validation
function validateSignIn() {
    var email = document.getElementById("signinEmail").value;

    // Check if email ends with '.babcock.edu.ng'
    if (!email.endsWith('.babcock.edu.ng')) {
        alert("Email must end with '.babcock.edu.ng'");
        return false;
    }

    return true;
}



