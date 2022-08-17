#!/usr/bin/env python3
# required pip modules: simple-term-menu

import subprocess
import argparse
import time
from threading import Timer
from simple_term_menu import TerminalMenu

verbose = True
normal_output = subprocess.DEVNULL
error_output = subprocess.STDOUT

main_menu_title = " Proxmox Kubernetes Cluster Manager\n"
main_menu_exit = False
main_menu_items = [
    "Provision Cluster",
    "Provision Just Proxmox",
    "Provision Just Ansible",
    "Destory Cluster", 
    "Exit"
]
main_menu_cursor = "> "
main_menu_cursor_style = ("fg_red", "bold")
main_menu_style = ("bg_red", "fg_yellow")



def terraform_create():
    if verbose:
        return subprocess.run(['terraform apply -auto-approve'], shell=True)
    else:
        return subprocess.run(['terraform apply -auto-approve'], shell=True, stdout=normal_output, stderr=error_output)


def terraform_destroy():
    if verbose:
        return subprocess.run(['terraform apply -destroy -auto-approve'], shell=True)
    else:
        return subprocess.run(['terraform apply -destroy -auto-approve'], shell=True, stdout=normal_output,
                              stderr=error_output)


def ansible_provision():
    if verbose:
        return subprocess.run(['ansible-playbook -i ansible/inventory/getInventory.sh  ansible/site.yml'],
                              shell=True)
    else:
        return subprocess.run(['ansible-playbook -i ansible/inventory/getInventory.sh  ansible/site.yml'],
                              shell=True,
                              stdout=normal_output, stderr=error_output)


# Destroy menu option
def menu_destroy(exit_text):
    validate_destroy = input("ARE YOU SURE?!?!?!?! Y to continue: ")

    if validate_destroy != "Y":
        return

    start_time = time.perf_counter()
    print(exit_text)
    terraform_destroy()
    cluster_destroyed = (time.perf_counter() - start_time ) / 60
    print(f"Clean up complete in { cluster_destroyed } \n")
    input("Press enter to continue")


# Create Menu Option
def menu_create_resources():

    proxmox_timer = time.perf_counter()

    print(f"Creating the Kubernetes Cluster\n")

    # Run Terraform and provision resources
    print(f"Creating Proxmox Resources")

    print(f"--------------------------")
    create_resource = terraform_create()
    print(f"--------------------------")


    if create_resource.returncode == 0:
        resource_created = ( time.perf_counter() - proxmox_timer ) / 60
        print(f"Created Successfully in { resource_created } \n")
    else:
        print(f"Creating Proxmox Resources Failed")
        print(f"--------------------------")
        print(f"Cleaning up partially deployed resources")
        print(f"--------------------------")
        terraform_destroy()
        print(f"--------------------------")
        provision_failed = ( time.perf_counter() - proxmox_timer ) / 60
        print(f"Clean up complete in { provision_failed } \n")
        exit(-1)

def menu_provision_resources():
    ansible_timer = time.perf_counter()
    # Run ansible and provision resources
    print(f"Provisioning Kubernetes")

    print(f"--------------------------")
    provision_resource = ansible_provision()
    print(f"--------------------------")

    if provision_resource.returncode == 0:
        provision_completed = ( time.perf_counter() - ansible_timer ) / 60
        print(f"Provisioning Kubernetes Successful in { provision_completed }")
    else:
        print(f"Provision Kubernetes Failed")
        exit(-1)


# Exit Menu Option
def menu_exit():
    print(f"Nice")


# CLI Menu 
def cli_menu():

    main_menu = TerminalMenu(
        menu_entries=main_menu_items,
        title=main_menu_title,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )
    start_time = 0


    while not main_menu_exit:
        menu_entry_index = main_menu.show()

        if menu_entry_index == 0:
            start_time = time.perf_counter()
            menu_create_resources()
            menu_provision_resources()
            end_time = (time.perf_counter() - start_time ) / 60
            print(f"Provisioning completed in { end_time } \n")
            input("Press enter to continue")
        elif menu_entry_index == 1:
            start_time = time.perf_counter()
            menu_create_resources()
            end_time = (time.perf_counter() - start_time ) / 60
            print(f"Proxmox completed in { end_time } \n")
            input("Press enter to continue")
        elif menu_entry_index == 2:
            start_time = time.perf_counter()
            menu_provision_resources()
            end_time = (time.perf_counter() - start_time ) / 60
            print(f"Ansible completed in { end_time } \n")
            input("Press enter to continue")
        elif menu_entry_index == 3:
            menu_destroy("Destroying the Kubernetes Cluster")
        else:
            menu_exit()
            break


def main():
    parser = argparse.ArgumentParser(description="This tool is used to create a Kubernetes cluster on Proxmox")
    parser.add_argument('-s', '--silent', help="Hides all the output of the commands to console",
                        action='store_true')

    args = parser.parse_args()

    global verbose

    if args.silent:
        verbose = True

    cli_menu()


if __name__ == "__main__":
    main()
