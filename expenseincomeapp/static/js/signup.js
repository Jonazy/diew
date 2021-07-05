const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector(".invalid_feedback");
const emailFieldId = document.querySelector('#emailFieldId');
const emailFeedBackArea = document.querySelector(".email-invalid-feedback");
const usernameSuccess = document.querySelector(".usernameSuccess");
const passwordField = document.querySelector('#passwordField');
const confirmPasswordField = document.querySelector('#confirmPasswordField');
const missMatchPassword = document.querySelector(".miss-match-password");
const showHidePasswordToggle = document.querySelector(".showHidePasswordToggle");
const submitButton = document.querySelector(".submit-button");
submitButton.disabled = false;

const handleToggle = (e) => {
    if (showHidePasswordToggle.textContent === 'show'){
        showHidePasswordToggle.textContent = 'hide';
        passwordField.setAttribute("type", "text");
        confirmPasswordField.setAttribute("type", "text");
    } else {
        showHidePasswordToggle.textContent = 'show';
        passwordField.setAttribute("type", "password");
        confirmPasswordField.setAttribute("type", "password");
    }
};
showHidePasswordToggle.addEventListener('click', handleToggle);

usernameField.addEventListener('keyup', (e)=> {
    const usernameValue = e.target.value;
    usernameSuccess.style.display = "block";
    usernameSuccess.textContent = `Checking, ${usernameValue}...`;

    if (usernameValue.length > 0){
    fetch("/authentication/validate-username/", {
        body: JSON.stringify({ username: usernameValue }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            usernameSuccess.style.display = "none";
            if ( data.username_valid) {
                usernameField.classList.remove('is-invalid');
                feedBackArea.style.display = 'none';
                submitButton.disabled = false;
            };
            if ( data.username_error) {
                usernameField.classList.add('is-invalid');
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                submitButton.disabled = true;
            }
        });
    } else{
        usernameField.classList.remove('is-invalid');
        feedBackArea.style.display = 'none';
        submitButton.disabled = true;
    }
});

emailFieldId.addEventListener('keyup', (e)=> {
    const emailValue = e.target.value;
    if ( emailValue.length > 0){
    fetch("/authentication/validate-email/", {
        body: JSON.stringify({ email: emailValue }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.email_valid) {
                emailFieldId.classList.remove('is-invalid');
                emailFeedBackArea.style.display = 'none';
                submitButton.disabled = false;
            };
            if (data.email_error) {
                emailFieldId.classList.add('is-invalid');
                emailFeedBackArea.style.display = 'block';
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                submitButton.disabled = true;
            }
        });
    } else {
        emailFieldId.classList.remove('is-invalid');
        emailFeedBackArea.style.display = 'none';
        submitButton.disabled = true;
    }

});

confirmPasswordField.addEventListener('keyup', (e) => {
    confirmPasswordFieldValue = e.target.value;
    passwordFieldValue = passwordField.value;

    if (confirmPasswordFieldValue != passwordFieldValue){
        confirmPasswordField.classList.add('is-invalid');
        passwordField.classList.add('is-invalid');
        missMatchPassword.style.display = 'block';
        missMatchPassword.innerHTML = "Passwords does not match. Please enter same password!";
        submitButton.disabled = true;
    } else {
        confirmPasswordField.classList.remove('is-invalid');
        passwordField.classList.remove('is-invalid');
        missMatchPassword.style.display = 'none';
        submitButton.disabled = false;
    }
})