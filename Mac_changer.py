import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="To enter the interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="To enter the new mac address")
    return parser.parse_args()


def change_mac(interface, new_mac):
    commands = [
        f"ifconfig {interface} down",
        f"ifconfig {interface} hw ether {new_mac}",
        f"ifconfig {interface} up"
    ]
    print(f"Changing mac address for {interface} to {new_mac}")

    for command in commands:
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        except subprocess.CalledProcessError as e:
            print("Error Changing the Mac Address")


    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        new_mac_address = mac_address_search_result.group(0)
        if new_mac_address.lower() == new_mac.lower():
            print(f"[+] MAC address was successfully changed to {new_mac_address}")
        else:
            print(f"[!] MAC address was not changed. Current MAC address is {new_mac_address}")
    else:
        print("[.] Could not find the MAC address")



options, arguments = get_arguments()
change_mac(options.interface, options.new_mac)
