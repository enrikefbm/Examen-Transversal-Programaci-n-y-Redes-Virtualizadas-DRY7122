# Script para clasificar número de VLAN

# Solicitar al usuario que ingrese el número de VLAN
try:
    vlan = int(input("Ingrese el número de VLAN: "))

    if 1 <= vlan <= 1005:
        print(f"La VLAN {vlan} pertenece al rango NORMAL.")
    elif 1006 <= vlan <= 4094:
        print(f"La VLAN {vlan} pertenece al rango EXTENDIDO.")
    else:
        print("Número de VLAN inválido. Debe estar entre 1 y 4094.")
except ValueError:
    print("Entrada inválida. Por favor ingrese un número entero.")
