var countdownDisplay2 = document.getElementById("countdown-2");
var userotp2 = document.getElementById('signup-otp')
var email = document.getElementById('email');
var fname = document.getElementById('fname');
var lname = document.getElementById('lname');
var desc = document.getElementById('desc');

var subbutton2 = document.getElementById("sub-signup-1");
function send_otp2() {
    subbutton2.disabled = true;
    const email_ = email.value
    const fname_ = fname.value
    const lname_ = lname.value
    const desc_ = desc.value

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch('/you/check', {
        method: 'POST',
        body: JSON.stringify({ email: email_, fname: fname_, lname: lname_, desc: desc_}),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data['message'] == true) {
                otp = data['otp'];
                otptimer();
            }
            else if (data['message'] == false) {
                alert("email already exists please select a different email");
                subbutton2.disabled = false;
            }
            else {
                alert(data['message']);
                subbutton2.disabled = false;
            }

        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


var otptimer = () => {
    document.getElementById('invalidtext-2').style.display = "none";
    countdownDisplay2.textContent = "";
    userotp2.value = "";
    const otpmodal2 = document.getElementById("selfclick-2");
    otpmodal2.click();
    let countdown = 30;
    countdownIntervalOtp = setInterval(() => {
        if (countdown <= 0) {
            subbutton2.disabled = false;
            clearInterval(countdownIntervalOtp); // Stop the countdownDisplay
            countdownDisplay2.textContent = "";
            userotp2.value = "";
            otp = 1000001;
            document.getElementById('signupmodaltrigger').click();
        }
        else {
            countdownDisplay2.textContent = `OTP valid till: ${countdown} seconds`;
        }
        countdown--;
    }, 1000);

}

var otp_verify = () => {
    if (userotp2.value == otp) {
        subbutton2.disabled = false;
        clearInterval(countdownIntervalOtp);
        countdownDisplay2.textContent = "";
        otp = 1000001;
        document.getElementById('invalidtext-2').style.display = "none";
        userotp2.value = "";
        document.getElementById('selfclick-3').click();
    }
    else {
        document.getElementById('invalidtext-2').style.display = "block";
    }
}

var submituser = () => {
    let pass1 = document.getElementById('createpass1').value;
    let pass2 = document.getElementById('createpass2').value;
    let username = document.getElementById('createusername').value;
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    fetch('/you/check', {
        method: 'POST',
        body: JSON.stringify({ username: username }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data['message'] == true) {
                if (pass1 === pass2) {
                    let specialChars = /[`!@#$%^&*()_\-+=\[\]{};':"\\|,.<>\/?~]/;
                    if (specialChars.test(pass1) && !pass1.includes(" ") && (/\d/.test(pass1)) && (/[a-z]/.test(pass1)) && (/[A-Z]/.test(pass1))) {
                        document.getElementById('myForm').submit();
                    }
                    else {
                        alert("invalid password format");
                    }
                }
                else {
                    alert("passwords do not match");
                }
            }
            else {
                alert('username already exists');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}