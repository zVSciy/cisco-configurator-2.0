function isValidIpAddress(ip) {
  const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$/;
  return ipRegex.test(ip);
}


function ValidateFooter(ipaddress, info, transfer_button, option_button) {
  let message = document.getElementById(info);
  let ip = document.getElementById(ipaddress);
  let TButton = document.getElementById(transfer_button);
  let option = document.getElementById(option_button).value; //download or transfer config button
  let background_color = '#4CAF50';

  if (isValidIpAddress(ip.value)) {
    document.getElementById("transferButton").disabled = false;
    message.textContent = "";
    TButton.disabled = false;
    TButton.style.backgroundColor = background_color;
    return true;
  } else if (ip.value == "" && option == 'download') {
    TButton.disabled = false;
    message.textContent = "";
    TButton.disabled = false;
    TButton.style.backgroundColor = background_color;
    return true;
  } else if (ip.value == "" && option == 'transfer') {
    TButton.disabled = true;
    message.textContent = "Please enter an IP Address";
    TButton.style.backgroundColor = "#f44336";
  } else if (isValidIpAddress(ip.value) && TButton.disabled === true) {
    TButton.disabled = false;
    message.textContent = "";
    TButton.style.backgroundColor = background_color;
  } else if (isValidIpAddress(ip.value) == false && option == 'download') {
    TButton.disabled = false;
    message.textContent = "";
    TButton.disabled = false;
    TButton.style.backgroundColor = background_color;
    return true;
  } else {
    message.textContent = "You have entered an invalid IP address!";
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
  }
}

