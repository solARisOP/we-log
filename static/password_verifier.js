function setAction() {
    let pass1 = document.getElementById('respass1').value;
    let pass2 = document.getElementById('respass2').value;
    if (pass1 === pass2) {
        let specialChars = /[`!@#$%^&*()_\-+=\[\]{};':"\\|,.<>\/?~]/;
        if (specialChars.test(pass1) && !pass1.includes(" ") && (/\d/.test(pass1)) && (/[a-z]/.test(pass1)) && (/[A-Z]/.test(pass1))) {
            document.getElementById('PrForm').submit();
            currpass.style.display = "none";
        }
        else {
            alert("invalid password format");
        }
    }
    else {
        alert("passwords doesnot match");
    }
}

const passreset = document.getElementById('userpassreset');
passreset.addEventListener('click', () => {
    currpass.style.display = "block";
});