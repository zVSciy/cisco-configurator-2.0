<div align="center">

# Cisco-Configurator 2.0

</div>

## Run the container

Open the CLI and enter this command to build the container
```docker
docker-compose build
```
Next step you need to run the container with the following command
```docker
docker-compose up
```

## Prepare your cisco device

Open the CLI and enter the follwing commands to access the cisco router/switch

- Interface setup:

```cisco
Router(config)# int f0/0
Router(config-if)# ip address dhcp
Router(config-if)# no shutdown
```

```cisco
Testrouter(config)# ip domain-name test.local
Testrouter(config)# crypto key generate rsa general-keys modulus 2048
Testrouter(config)# ip ssh version 2
Testrouter(config)# line vty 0 15
Testrouter(config-line)# transport input ssh
Testrouter(config-line)# login local
Testrouter(config)# username admin privilege 15 password admin
Testrouter(config)# ip scp server enable
```

> [!IMPORTANT]
> This application is only working for PNET Lab devices.
