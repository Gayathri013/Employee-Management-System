const form = document.getElementById('my-Form');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phone');
const messageInput = document.getElementById('message');
const nameError = document.getElementById('name-error');
const emailError = document.getElementById('email-error');
const phoneError = document.getElementById('phone-error');
const messageError = document.getElementById('message-error');

form.addEventListener('submit', (event) => {
  if (validateName() && validateEmail() && validatePhone() && validateMessage()) {
    form.submit();
  }
});

function validateName() {
  const nameValue = nameInput.value.trim();
  if (nameValue === '') {
    nameError.innerText = 'Please enter your name.';
    console.log("enter name properly");
    return false;
  } else if (!/^[a-zA-Z ]+$/.test(nameValue)) {
    nameError.innerText = 'Please enter a valid name.';
    return false;
  } else {
    nameError.innerText = '';
    return true;
  }
}

function validateEmail() {
  const emailValue = emailInput.value.trim();
  if (emailValue === '') {
    emailError.innerText = 'Please enter your email address.';
    return false;
  } else if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(emailValue)) {
    emailError.innerText = 'Please enter a valid email address.';
    return false;
  } else {
    emailError.innerText = '';
    return true;
  }
}

function validatePhone() {
    const phoneValue = phoneInput.value.trim();
    if (phoneValue === '') {
      phoneError.innerText = 'Please enter your phone number.';
      return false;
    } else if (!/^[0-9]+$/.test(phoneValue) || phoneValue.length !== 10) {
      phoneError.innerText = 'Please enter a valid 10-digit phone number.';
      return false;
    } else {
      phoneError.innerText = 'hadjfasdif';
      return true;
    }
  }

function validateMessage() {
  const messageValue = messageInput.value.trim();
  if (messageValue === '') {
    messageError.innerText = 'Please enter a message.';
    return false;
  } else {
    messageError.innerText = '';
    return true;
  }
}
