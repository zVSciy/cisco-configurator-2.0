const ipRegex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

function isValidIpAddress(ip) {
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

//interfaces
function updateInterfaceDescription(checkbox_value, checkbox_description) {
  let checkbox = document.getElementById(checkbox_value);
  let interfaceDescription = document.getElementById(checkbox_description);

  if (checkbox.checked) {
    interfaceDescription.innerHTML = "<span class='text-accent'> (on)</span>";
  } else {
    interfaceDescription.innerText = ' (shutdown)';
  }
}


function checkIpAddress(Int_ip, Int_sm, Int_result, transferButton) {
  let ip = document.getElementById(Int_ip);
  let sm = document.getElementById(Int_sm);
  let resultElement = document.getElementById(Int_result);
  let TButton = document.getElementById("transferButton");
  let background_color = '#4CAF50';

  if (isValidIpAddress(ip.value) && isValidIpAddress(sm.value) || ip.value === "" && sm.value === "" || ip.value === "dhcp" && sm.value === "") {
    resultElement.textContent = "";
    //re-able the buttons if they got disabled
    TButton.disabled = false;
    TButton.style.backgroundColor = background_color;
  } else if (ip.value === "dhcp" && sm.value !== "") {
    resultElement.textContent = "Leave Subnet Mask field empty if IP is dhcp!";
    //disable the buttons
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
  } else {
    resultElement.style.color = "#f44336";
    resultElement.textContent = "Invalid IP and/or Subnet Mask.";
    //disable the buttons
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
  }
}

//function to update the state descriptions 
function updateStateDescription(checkbox_value, checkbox_description) {
  let checkbox = document.getElementById(checkbox_value);
  let interfaceDescription = document.getElementById(checkbox_description);

  if (checkbox.checked) {
    interfaceDescription.innerHTML = "<span class='text-accent'> (on)</span>";
  } else {
    interfaceDescription.innerText = ' (off)';
  }
}


//NAT
function addNatIp() {
  let Ip = document.getElementById('nat_ip').value;
  let wildcardMask = document.getElementById('nat_wm').value;

  let routeInfo = "IP Address: " + Ip + "<br>Wildcard Mask: " + wildcardMask + '<br><br>';

  document.getElementById('nat_info').innerHTML += routeInfo;
  document.getElementById('nat_info_for_transfer').value += Ip + ',' + wildcardMask + ';';
}

function ValidateIPaddressNat(ipaddress, info) {
  let message = document.getElementById(info);
  let ip = document.getElementById(ipaddress);
  let TButton = document.getElementById("add_nat_ip_button");
  if (isValidIpAddress(document.getElementById('nat_wm').value) && isValidIpAddress(document.getElementById('nat_ip').value)) {
    message.textContent = "";
    TButton.disabled = false;
    return true;
  } else if (isValidIpAddress(ip.value)) {
    message.textContent = "";
    return true;
  } else if (ip.value == "") {
    message.textContent = "";
    TButton.disabled = true;
    return true;
  } else {
    message.textContent = "You have entered an invalid IP address!";
    TButton.disabled = true;
    // TButton.style.backgroundColor = "#f44336";
  }
}

function checkInterfacesNat() {
  let ingoing = document.getElementById('nat_ingoing').value
  let outgoing = document.getElementById('nat_outgoing').value
  let Button = document.getElementById("transferButton")
  let resultElement = document.getElementById('nat_interface_info')
  let status = document.getElementById('nat_status').checked

  if (ingoing == outgoing && status == true) {
    resultElement.textContent = "Ingoing and Outgoing Interfaces must be a different one.";
    Button.disabled = true;
    Button.style.backgroundColor = "#f44336";
  } else {
    resultElement.textContent = "";
    Button.disabled = false;
    Button.style.backgroundColor = "#4CAF50";
  }
}

//DHCP
function checkDhcpInput(Network_Input, Dg_input, dns_input, result) {
  let Network = document.getElementById(Network_Input).value.split(' ');
  let Dg = document.getElementById(Dg_input).value;
  let Dns = document.getElementById(dns_input).value;
  let resultElement = document.getElementById(result);
  let Button = document.getElementById("transferButton")
  let pool_name = document.getElementById("dhcp_poolName").value

  let Network_IP = Network[0].replace(/[\s,]+/g, '');
  let Network_SM = Network[1];

  if (isValidIpAddress(Network_IP) && isValidIpAddress(Network_SM) && isValidIpAddress(Dg) && isValidIpAddress(Dns) && pool_name != "") {
    resultElement.textContent = "";
    Button.disabled = false;
    Button.style.backgroundColor = "#4CAF50";
  } else if (Network == "" && Dg == "" && Dns == "" && pool_name == "") {
    resultElement.textContent = "";
    Button.disabled = false;
    Button.style.backgroundColor = "#4CAF50";
  } else {
    resultElement.textContent = "Please fill out all fields correctly";
    Button.disabled = true;
    Button.style.backgroundColor = "#f44336";
  }
}

function ValidateIPaddressDhcp(Ip_from, Ip_to, info) {
  let From = document.getElementById(Ip_from).value
  let To = document.getElementById(Ip_to).value;
  let Info = document.getElementById(info);
  let Button = document.getElementById("add_dhcp_button")


  if (isValidIpAddress(From) && isValidIpAddress(To)) {
    Info.textContent = "";
    Button.disabled = false;
  } else if (isValidIpAddress(From) && To == "") {
    Info.textContent = "";
    Button.disabled = false;
  } else if (From == "" && To == "") {
    Info.textContent = "";
    Button.disabled = false;
  } else {
    Info.textContent = "Please check your Input";
    Button.disabled = true;
  }
}

function addDhcpIp() {
  let From = document.getElementById('dhcp_pool_from').value;
  let To = document.getElementById('dhcp_pool_to').value;

  let routeInfo = "From: " + From + "<br>To: " + To + '<br><br>';

  document.getElementById('dhcp_pool_result').innerHTML += routeInfo;
  document.getElementById('dhcp_info_for_transfer').value += From + ',' + To + ';';
}

// RIP

function ValidateIPaddressesDynamicRouting(ipaddresses, info) {
  let message = document.getElementById(info);
  let ip = document.getElementById(ipaddresses);
  let containsIPs = checkmultipleIPs(ip.value)
  let TButton = document.getElementById("transferButton");

  if (containsIPs == true || ip.value == '') {
    message.textContent = "";
    TButton.disabled = false;
    TButton.style.backgroundColor = "#4CAF50";
  } else {
    message.textContent = "You have entered an invalid IP address!";
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
  }
}

function checkmultipleIPs(string) {
  const ipAdressen = string.split(',');

  for (const ipAdresse of ipAdressen) {

    if (!ipRegex.test(ipAdresse.trim())) {
      return false;
    }
  }
  return true;
}