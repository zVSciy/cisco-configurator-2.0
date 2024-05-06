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




// OSPF

function addOspfIp() {
  let Ip = document.getElementById('ospf_ip').value;
  let wildcardMask = document.getElementById('ospf_wm').value;
  let area = document.getElementById('ospf_area').value

  let networksInfo = "IP Address: " + Ip + "<br>Wildcard Mask: " + wildcardMask + '<br>Area:'+ area +'<br><br>';

  document.getElementById('ospf_info').innerHTML += networksInfo;
  document.getElementById('ospf_info_for_transfer').value += Ip + ',' + wildcardMask + ',' + area + ';';
}

function ValidateAreaOSPF(area){
  if(area >=0 && area <= 4294967294 ){
    return true;
  }
}

function ValidateOspfNetworks(info) {
  let message = document.getElementById(info);
  let TButton = document.getElementById("add_ospf_ip_button");
  if (isValidIpAddress(document.getElementById('ospf_wm').value) && isValidIpAddress(document.getElementById('ospf_ip').value) && ValidateAreaOSPF(document.getElementById('ospf_area').value)) {
    message.textContent = "";
    TButton.disabled = false;
    return true;
  }else if(document.getElementById('ospf_wm').value == '' && document.getElementById('ospf_ip').value == '' && document.getElementById('ospf_area').value == ''){
    message.textContent = "";
    TButton.disabled = false;
  }else {
    message.textContent = "Please fill out all fields correctly!";
    TButton.disabled = true;
  }
}

function checkOspfRouterID(){
  let TButton = document.getElementById("transferButton");
  let ospf_router_id = document.getElementById('ospf_router_id').value
  let message = document.getElementById('router_id_info')

  if (isValidIpAddress(ospf_router_id) ) {
    message.textContent = "";
    TButton.disabled = false;
    return true;
  }else if(ospf_router_id == ''){
    message.textContent = "";
    TButton.disabled = false;
  }else {
    message.textContent = "Invalid Router-ID";
    TButton.disabled = true;
  }
}

function checkOspfProcess(){
  let TButton = document.getElementById("transferButton");
  let ospf_process_id = document.getElementById('ospf_process').value
  let message = document.getElementById('process_id_info')

  if (ospf_process_id >=0 && ospf_process_id <= 10000) {
    message.textContent = "";
    TButton.disabled = false;
    return true;
  }else if(ospf_process_id == ''){
    message.textContent = "";
    TButton.disabled = false;
  }else {
    message.textContent = "Invalid Process";
    TButton.disabled = true;
  }
}

// Basic ACLs

let basic_acl_ids = []

function checkBasicAclId(){
  let id = document.getElementById('basic_acl_id').value;
  let message = document.getElementById('basic_acl_id_info');

  if (basic_acl_ids.includes(id)){
    message.textContent = "ID already set!";
    return false;
  }else {
    message.textContent = "";
    return true;
  }

}

function addBasicAclIp() {
  let Ip = document.getElementById('basic_acl_ip').value;
  let wildcardMask = document.getElementById('basic_acl_wm').value;
  let id = document.getElementById('basic_acl_id').value
  let pOrD = document.getElementById('basic_acl_pOrD').value

  basic_acl_ids.push(id);

  let networksInfo = "<b>ID: </b>" + id +  "<b> Option: </b>" + pOrD + " <b>IP-Address: </b>" + Ip + "<b> Wildcard Mask: </b>" + wildcardMask +'<br><br>';

  document.getElementById('basic_acl_info').innerHTML += networksInfo;
  document.getElementById('basic_acl_info_for_transfer').value += id + ',' + pOrD + ',' + Ip + ',' + wildcardMask + ';';

  document.getElementById("add_basic_acl_button").disabled = true;
}

function ValidateBasicAclNetwork(info) {
  let message = document.getElementById(info);
  let TButton = document.getElementById("add_basic_acl_button");
  if (isValidIpAddress(document.getElementById('basic_acl_wm').value) && isValidIpAddress(document.getElementById('basic_acl_ip').value) && checkBasicAclId()) {
    message.textContent = "";
    TButton.disabled = false;
    return true;
  }else if(document.getElementById('basic_acl_wm').value == '' && document.getElementById('basic_acl_ip').value == ''){
    message.textContent = "";
    TButton.disabled = true;
  }else {
    message.textContent = "Please fill out all fields correctly!";
    TButton.disabled = true;
  }
}

// Extended ACLs

let extended_acl_ids = []

function checkExtendedAclId(){
  let id = document.getElementById('extended_acl_id').value;
  let message = document.getElementById('extended_acl_id_info');

  if (extended_acl_ids.includes(id)){
    message.textContent = "ID already set!";
    return false;
  }else {
    message.textContent = "";
    return true;
  }

}

function addExtendedAclIp() {
  let srcIp = document.getElementById('extended_acl_src_ip').value;
  let srcWildcardMask = document.getElementById('extended_acl_src_wm').value;
  let destIp = document.getElementById('extended_acl_dest_ip').value;
  let destWildcardMask = document.getElementById('extended_acl_dest_wm').value;
  let id = document.getElementById('extended_acl_id').value
  let pOrD = document.getElementById('extended_acl_pOrD').value
  let port = document.getElementById('extended_acl_port').value

  extended_acl_ids.push(id);

  let networksInfo = "<b>ID: </b>" + id +  "<b> Option: </b>" + pOrD + " <b> Source IP-Address: </b>" + srcIp + "<b>Source Wildcard Mask: </b>" + srcWildcardMask + "<b> Destination IP-Adress: </b>" + destIp + "<b> Destination Wildcard Mask: </b>" + destWildcardMask + "<b> Port: </b>"+ port +'<br><br>';

  document.getElementById('extended_acl_info').innerHTML += networksInfo;
  document.getElementById('extended_acl_info_for_transfer').value += id + ',' + pOrD + ',' + srcIp + ',' + srcWildcardMask + ',' + destIp + ',' + destWildcardMask + ',' + port + ';';

  console.log(document.getElementById('extended_acl_info_for_transfer').value);

  document.getElementById("add_extended_acl_button").disabled = true;
}

function ValidateExtendedAclNetwork(info) {
  let message = document.getElementById(info);
  let TButton = document.getElementById("add_extended_acl_button");
  if (isValidIpAddress(document.getElementById('extended_acl_src_ip').value) && isValidIpAddress(document.getElementById('extended_acl_src_wm').value) && isValidIpAddress(document.getElementById('extended_acl_dest_ip').value) && isValidIpAddress(document.getElementById('extended_acl_dest_wm').value) && checkExtendedAclId()) {
    message.textContent = "";
    TButton.disabled = false;
    return true;
  }else if(document.getElementById('extended_acl_src_ip').value == '' && document.getElementById('extended_acl_src_wm').value == '' && document.getElementById('extended_acl_dest_ip').value == '' && document.getElementById('extended_acl_dest_wm').value == ''){
    message.textContent = "";
    TButton.disabled = true;
  }else {
    message.textContent = "Please fill out all fields correctly!";
    TButton.disabled = true;
  }
}



// add to Config for backend
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

  if (page == "ospf"){
    let ospf_process_to_set = document.getElementById('ospf_process').value 
    let ospf_router_id_to_set = document.getElementById('ospf_router_id').value 
    let ospf_info_for_transfer_to_set = document.getElementById('ospf_info_for_transfer').value 


    document.getElementById('hidden_ospf_process').value = ospf_process_to_set; //true = on | false = off
    document.getElementById('hidden_ospf_router_id').value = ospf_router_id_to_set;
    document.getElementById('hidden_ospf_info_for_transfer').value = ospf_info_for_transfer_to_set;
  }

  if (page == "acl_basic"){
    let basic_acl_info_for_transfer_to_set = document.getElementById('basic_acl_info_for_transfer').value 

    document.getElementById('hidden_basic_acl_info_for_transfer').value = basic_acl_info_for_transfer_to_set;
  }

  if (page == "acl_extended"){
    let extended_acl_info_for_transfer_to_set = document.getElementById('extended_acl_info_for_transfer').value 

    document.getElementById('hidden_extended_acl_info_for_transfer').value = extended_acl_info_for_transfer_to_set;
  }
}



//Index Site Checks

function ValidateIndexInput(){
  ip = document.getElementById('loadFromIpAddress')
  if (isValidIpAddress(ip.value)) {
      document.getElementById("IndexSubmitButton").disabled = false;
      document.getElementById("IndexErrorMessage").textContent = '';

  }else if(ip.value == ''){
    document.getElementById("IndexErrorMessage").textContent = '';
    document.getElementById("IndexSubmitButton").disabled = true;
  }else{
      document.getElementById("IndexSubmitButton").disabled = true;
      document.getElementById("IndexErrorMessage").textContent = 'You have entered an invalid IP address!';
  }
}