from netmiko_csr_script import ConnectHandler

# Parámetros del router
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.10',     
    'username': 'cisco',         
    'password': 'cisco123!',     
    'secret': 'cisco123!',       
    'port': 22,
}

# AS para EIGRP nombrado
eigrp_as = 100

# Interfaces que usarás para EIGRP (pasa las que tienes en tu router)
eigrp_interfaces = ['GigabitEthernet1', 'GigabitEthernet2']

try:
    net_connect = ConnectHandler(**router)
    net_connect.enable()

    # Configurar EIGRP nombrado IPv4
    config_commands = [
        'router eigrp {}'.format(eigrp_as),
        'address-family ipv4 autonomous-system {}'.format(eigrp_as),
    ]
    # Configurar interfaces activas y pasivas para IPv4
    for iface in eigrp_interfaces:
        config_commands.append('interface {}'.format(iface))
        # Hacemos passiva solo si no queremos enviar EIGRP por esa interfaz (ajusta según necesidad)
        # Si quieres que alguna sea pasiva, por ejemplo:
        if iface == 'GigabitEthernet2':
            config_commands.append('ip passive-interface')
        else:
            config_commands.append('no ip passive-interface')

    config_commands.append('exit-address-family')

    # Configurar EIGRP nombrado IPv6
    config_commands.extend([
        'router eigrp {}'.format(eigrp_as),
        'address-family ipv6 autonomous-system {}'.format(eigrp_as),
    ])

    # Interfaces para IPv6
    for iface in eigrp_interfaces:
        config_commands.append('interface {}'.format(iface))
        if iface == 'GigabitEthernet2':
            config_commands.append('ipv6 passive-interface')
        else:
            config_commands.append('no ipv6 passive-interface')

    config_commands.append('exit-address-family')

    # Enviar configuración
    output = net_connect.send_config_set(config_commands)
    print("Configuración enviada:\n", output)

    # Mostrar resultado del running-config sección eigrp
    eigrp_config = net_connect.send_command('show running-config | section eigrp')
    print("\n=== Sección EIGRP en Running-config ===\n", eigrp_config)

    # Mostrar IPs y estado interfaces IPv4
    ip_int_brief = net_connect.send_command('show ip interface brief')
    print("\n=== Estado y IP interfaces IPv4 ===\n", ip_int_brief)

    # Mostrar IPs y estado interfaces IPv6
    ipv6_int_brief = net_connect.send_command('show ipv6 interface brief')
    print("\n=== Estado y IP interfaces IPv6 ===\n", ipv6_int_brief)

    # Mostrar running-config completo
    running_config = net_connect.send_command('show running-config')
    print("\n=== Running-config completo ===\n", running_config)

    # Mostrar show version
    version_info = net_connect.send_command('show version')
    print("\n=== Show Version ===\n", version_info)

    net_connect.disconnect()

except Exception as e:
    print(f"Error: {e}")