from ncclient import manager

# Parámetros de conexión NETCONF
router = {
    "host": "192.168.1.10",
    "port": 830,
    "username": "cisco",
    "password": "cisco123!",
    "hostkey_verify": False
}

# Apellidos del grupo
nuevo_hostname = "Acosta-Salazar-Gonzalez-Villalobos"

config_xml = f"""
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>{nuevo_hostname}</hostname>
  </native>
</config>
"""

with manager.connect(**router) as m:
    response = m.edit_config(target="running", config=config_xml)
    print("✅ Hostname cambiado a:", nuevo_hostname)
    print(response)
