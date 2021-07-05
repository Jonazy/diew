const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector(".invalid_feedback");
const emailFieldId = document.querySelector('#emailFieldId');
const emailFeedBackArea = document.querySelector(".email-invalid-feedback");


usernameField.addEventListener('keyup', (e)=> {
    const usernameValue = e.target.value;
    if (usernameValue.length > 0){
    fetch("/authentication/validate-username/", {
        body: JSON.stringify({ username: usernameValue }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            if ( data.username_valid) {
                usernameField.classList.remove('is-invalid');
                feedBackArea.style.display = 'none';
            };
            if ( data.username_error) {
                usernameField.classList.add('is-invalid');
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
            }
        });
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
            };
            if (data.email_error) {
                emailFieldId.classList.add('is-invalid');
                emailFeedBackArea.style.display = 'block';
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
            }
        });
    }
});
