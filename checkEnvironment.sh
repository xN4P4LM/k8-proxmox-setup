#!/bin/bash

# check to see if python3 is installed
if ! which python3 > /dev/null; then
   echo "python3 is not installed" 1>&2
   exit 1
fi

# check to see if terraform is installed 
if ! which terraform > /dev/null; then
   echo "terraform is not installed" 1>&2
   exit 1
fi

# check to see if ansible is installed
if ! which ansible-playbook > /dev/null; then
   echo "ansible is not installed" 1>&2
   exit 1
fi

# check to see if file ansible/inventory/proxmox.py exists
if [ ! -f ansible/inventory/proxmox.py ]; then
   # run ansible/inventory/setupDynamicInventory.sh in directory ansible/inventory
    cd ansible/inventory
    ./setupDynamicInventory.sh
    cd ../..
   exit 1
fi

# check to see if the pip package simple-term-menu is installed
if ! pip3 list | grep -q simple-term-menu; then
   echo "simple-term-menu is not installed" 1>&2
   exit 1
fi

# advise all check completed successfully
echo "All checks completed successfully"