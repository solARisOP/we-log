var otp = 10000001;
const sendotpButton = document.getElementById('sendotp');
const submitButton = document.getElementById('subbutton');
const passmodal = document.getElementById("selfclick");
const invalidtext = document.getElementById("invalidtext");
const countdownDisplay = document.getElementById('countdown');
const otpdiv = document.getElementById('otpdiv');
const userInputOTP = document.getElementById('resotp');
const userInputEmail = document.getElementById('resemail');
const invalidEmail = document.getElementById('invalid-email');
const currpass = document.getElementById('curr-password');

function send_OTP() {
    otp = 10000001;
    clearall();
    sendotpButton.disabled = true;
    let email = userInputEmail.value;
    email = email.trim()
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    fetch('/you/otpverif', {
        method: 'POST',
        body: JSON.stringify({ message: email }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if ('message' in data) {
                const userMessageElement = document.createElement('div');
                userMessageElement.classList.add('my-1');
                userMessageElement.textContent = data['message'];
                invalidEmail.appendChild(userMessageElement);
            }
            else {
                sendotpButton.disabled = true;
                startTimer();
                otp = data['otp'];
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function startTimer() {
    let countdown = 100;
    otpdiv.style.display = "block";
    submitButton.style.display = "block";
    countdownDisplay.style.display = "block";
    countdownInterval = setInterval(() => {
        if (countdown <= 0) {
            clearInterval(countdownInterval); // Stop the countdownDisplay
            clearall();
            sendotpButton.disabled = false;
        }
        else {
            countdownDisplay.textContent = `OTP valid till: ${countdown} seconds`;
        }
        countdown--;
    }, 1000);
}

var clearall = () => {
    otpdiv.style.display = "none";
    submitButton.style.display = "none";
    countdownDisplay.style.display = "none";
    invalidtext.style.display = "none";
    while (invalidEmail.hasChildNodes()) {
        invalidEmail.removeChild(invalidEmail.firstChild)
    }
}

sendotpButton.addEventListener('click', send_OTP);
submitButton.addEventListener('click', function (e) {
    let userotp = userInputOTP.value;
    if (userotp === otp) {
        currpass.style.display = "none";
        passmodal.click();
        userInputEmail.value = "";
        userInputOTP.value = "";
        clearInterval(countdownInterval);
        sendotpButton.disabled = false;
        countdownDisplay.textContent = "";
        clearall();
    }
    else {
        invalidtext.style.display = "block";
    }
});