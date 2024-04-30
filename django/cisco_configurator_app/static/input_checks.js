const ipRegex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

function isValidIpAddress(ip) {
  return ipRegex.test(ip);
}

function disableNavigation() {
  let buttons = document.getElementsByClassName("menu-button");
  for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = true;
  }
}

function enableNavigation() {
  let buttons = document.getElementsByClassName("menu-button");
  for (let i = 0; i < buttons.length; i++) {
      buttons[i].disabled = false;
  }
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
    enableNavigation()
    return true;
  } else if (ip.value == "" && option == 'download') {
    TButton.disabled = false;
    message.textContent = "";
    TButton.disabled = false;
    TButton.style.backgroundColor = background_color;
    enableNavigation()
    return true;
  } else if (ip.value == "" && option == 'transfer') {
    TButton.disabled = true;
    message.textContent = "Please enter an IP Address";
    TButton.style.backgroundColor = "#f44336";
    disableNavigation();
  } else if (isValidIpAddress(ip.value) && TButton.disabled === true) {
    TButton.disabled = false;
    message.textContent = "";
    TButton.style.backgroundColor = background_color;
    disableNavigation();
  } else if (isValidIpAddress(ip.value) == false && option == 'download') {
    TButton.disabled = false;
    message.textContent = "";
    TButton.disabled = false;
    TButton.style.backgroundColor = background_color;
    enableNavigation()
    return true;
  } else {
    message.textContent = "You have entered an invalid IP address!";
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
    disableNavigation();
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


function checkIpAddress(Int_ip, Int_sm, Int_result) {
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
    enableNavigation();
  } else if (ip.value === "dhcp" && sm.value !== "") {
    resultElement.textContent = "Leave Subnet Mask field empty if IP is dhcp!";
    //disable the buttons
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
    disableNavigation();
  } else {
    resultElement.style.color = "#f44336";
    resultElement.textContent = "Invalid IP and/or Subnet Mask.";
    //disable the buttons
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
    disableNavigation();
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
    disableNavigation();
  } else {
    resultElement.textContent = "";
    Button.disabled = false;
    Button.style.backgroundColor = "#4CAF50";
    enableNavigation();
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
    enableNavigation();
  } else if (Network == "" && Dg == "" && Dns == "" && pool_name == "") {
    resultElement.textContent = "";
    Button.disabled = false;
    Button.style.backgroundColor = "#4CAF50";
    enableNavigation();
  } else {
    resultElement.textContent = "Please fill out all fields correctly";
    Button.disabled = true;
    Button.style.backgroundColor = "#f44336";
    disableNavigation();
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
    enableNavigation();
  } else {
    message.textContent = "You have entered an invalid IP address!";
    TButton.disabled = true;
    TButton.style.backgroundColor = "#f44336";
    disableNavigation();
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

function handleDropdownChange() {
  let dropdown = document.getElementById('dropdown_rip_version');
  let checkbox = document.getElementById('sum_state');

  if (dropdown.value === 'version1') {
    checkbox.disabled = true;
    document.getElementById('sum_state_description').innerText = ' (off)';
    checkbox.checked = false;
  } else {
    checkbox.disabled = false;
  }
}



// Static Routing

function addRoute() {
  let targetIP = document.getElementById('target_ip').value;
  let subnetMask = document.getElementById('static_routing_subnet_mask').value;
  let nextHopIP = document.getElementById('next_hop_ip').value;

  let routeInfo = "Target IP: " + targetIP + "<br>Subnet Mask: " +
    subnetMask + "<br>Next hop IP: " + nextHopIP + "<br><br>";

  document.getElementById('staticRouting_info').innerHTML += routeInfo;
  document.getElementById('staticRouting_info_for_transfer').value += targetIP + ',' + subnetMask + ',' + nextHopIP + ';';
}

function ValidateIPaddressStaticRouting(ipaddress, info) {
  let message = document.getElementById(info);
  let ip = document.getElementById(ipaddress);
  let TButton = document.getElementById("add_StaticRoute_button");
  if (isValidIpAddress(document.getElementById('target_ip').value) && isValidIpAddress(document.getElementById('static_routing_subnet_mask').value) && isValidIpAddress(document.getElementById('next_hop_ip').value)) {
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
  }
}

function extractInterfaceNames(inputString) {
   const regex = /(?:<Router_Interfaces:\s)(\w+\/\d+)(?=>)/g;
   const interfaceNames = [];
   let match;
   while ((match = regex.exec(inputString)) !== null) {
     interfaceNames.push(match[1]);
   }
   return interfaceNames;
}


function add_to_config(page) {

  if (page == "basic_config"){
    //get the inputs
    let hostname_to_set = document.getElementById('hostname').value 
    let banner_to_set = document.getElementById('banner').value

    // enter the values into the hidden fields
    document.getElementById('hidden_hostname').value = hostname_to_set;
    document.getElementById('hidden_banner').value = banner_to_set;
  }

  if (page == "interface"){
    // get the interfaces
      let interfaces = extractInterfaceNames(document.getElementById('interfaces_for_get_inputs').value);
    
      //get the inputs from all Interfaces and store them into the hidden input fields 

      for (let i = 0; i < interfaces.length; i++){
        document.getElementById('hidden_'+interfaces[i]+'_shutdown').value = document.getElementById(interfaces[i]+'_shutdown').checked;
        document.getElementById('hidden_'+interfaces[i]+'_description').value = document.getElementById(interfaces[i]+'_description').value;
        document.getElementById('hidden_'+interfaces[i]+'_ip').value = document.getElementById(interfaces[i]+'_ip').value;
        document.getElementById('hidden_'+interfaces[i]+'_sm').value = document.getElementById(interfaces[i]+'_sm').value;
      }


      // let FastEthernet00_shutdown_to_set = document.getElementById('FastEthernet0/0_shutdown').checked 
      // let FastEthernet00_description_to_set = document.getElementById('FastEthernet0/0_description').value;
      // let FastEthernet00_ip_to_set = document.getElementById('FastEthernet0/0_ip').value 
      // let FastEthernet00_sm_to_set = document.getElementById('FastEthernet0/0_sm').value 

      // let FastEthernet01_shutdown_to_set = document.getElementById('FastEthernet0/1_shutdown').checked 
      // let FastEthernet01_description_to_set = document.getElementById('FastEthernet0/1_description').value;
      // let FastEthernet01_ip_to_set = document.getElementById('FastEthernet0/1_ip').value 
      // let FastEthernet01_sm_to_set = document.getElementById('FastEthernet0/1_sm').value 

      // ! enter the values into the hidden fields
      // document.getElementById('hidden_FastEthernet0/0_shutdown').value = FastEthernet00_shutdown_to_set;
      // document.getElementById('hidden_FastEthernet0/0_description').value = FastEthernet00_description_to_set;
      // document.getElementById('hidden_FastEthernet0/0_ip').value = FastEthernet00_ip_to_set;
      // document.getElementById('hidden_FastEthernet0/0_sm').value = FastEthernet00_sm_to_set;

      // document.getElementById('hidden_FastEthernet0/1_shutdown').value = FastEthernet01_shutdown_to_set;
      // document.getElementById('hidden_FastEthernet0/1_description').value = FastEthernet01_description_to_set;
      // document.getElementById('hidden_FastEthernet0/1_ip').value = FastEthernet01_ip_to_set;
      // document.getElementById('hidden_FastEthernet0/1_sm').value = FastEthernet01_sm_to_set;

  }
  if (page == "nat"){
      let nat_status_to_set = document.getElementById('nat_status').checked 
      let nat_ingoing_to_set = document.getElementById('nat_ingoing').value 
      let nat_outgoing_to_set = document.getElementById('nat_outgoing').value 
      let nat_info_for_transfer_to_set = document.getElementById('nat_info_for_transfer').value 


      document.getElementById('hidden_nat_status').value = nat_status_to_set; //true = on | false = off
      document.getElementById('hidden_nat_ingoing').value = nat_ingoing_to_set;
      document.getElementById('hidden_nat_outgoing').value = nat_outgoing_to_set;
      document.getElementById('hidden_nat_info_for_transfer').value = nat_info_for_transfer_to_set;

  }

  if (page == "dhcp"){
    let dhcp_status_to_set = document.getElementById('dhcp_status').checked 
    let dhcp_poolName_to_set = document.getElementById('dhcp_poolName').value 
    let dhcp_Network_to_set = document.getElementById('dhcp_Network').value 
    let dhcp_dG_to_set = document.getElementById('dhcp_dG').value 
    let dhcp_dnsServer_to_set = document.getElementById('dhcp_dnsServer').value 
    let dhcp_info_for_transfer_to_set = document.getElementById('dhcp_info_for_transfer').value


    document.getElementById('hidden_dhcp_status').value = dhcp_status_to_set; //true = on | false = off
    document.getElementById('hidden_dhcp_poolName').value = dhcp_poolName_to_set;
    document.getElementById('hidden_dhcp_Network').value = dhcp_Network_to_set;
    document.getElementById('hidden_dhcp_dG').value = dhcp_dG_to_set;
    document.getElementById('hidden_dhcp_dnsServer').value = dhcp_dnsServer_to_set;
    document.getElementById('hidden_dhcp_info_for_transfer').value = dhcp_info_for_transfer_to_set;

  }

  if (page == "rip"){
    let rip_state_to_set = document.getElementById('rip_state').checked
    let networks_input_routing_to_set = document.getElementById('networks_input_routing').value
    let dropdown_rip_version_to_set = document.getElementById('dropdown_rip_version').value
    let sum_state_to_set = document.getElementById('sum_state').checked
    let originate_state_to_set = document.getElementById('originate_state').checked

    document.getElementById('hidden_rip_state').value = rip_state_to_set; //true = on | false = off
    document.getElementById('hidden_networks_input_routing').value = networks_input_routing_to_set;
    document.getElementById('hidden_dropdown_rip_version').value = dropdown_rip_version_to_set;
    document.getElementById('hidden_sum_state').value = sum_state_to_set;
    document.getElementById('hidden_originate_state').value = originate_state_to_set;

  }

  if (page == "static_routing"){
    let staticRouting_info_for_transfer_to_set = document.getElementById('staticRouting_info_for_transfer').value

    document.getElementById('hidden_staticRouting_info_for_transfer').value = staticRouting_info_for_transfer_to_set;
  }



}