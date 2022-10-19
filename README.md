# Xilinx Board Upgrade script

used for upgrading batch of targets with system files
current version are for MAPS borad but can support FCA
creating one thread per target to run an upgrade script found in the target_sd image


### Editable parameters
* **maps_list** - this list of list is used for target parmeters.<br />
  one list per target<br />
  [targetip | target_port | target_accout | target_password | target_new_ip]<br />
  e.g:<br />
  [['172.16.0.10', 22, 'root', 'root', '172.16.1.20'],<br />
   ['172.16.0.11', 22, 'root', 'root', '172.16.1.21']]<br />


### Requirements python lib
paramiko.<br />
ntpath.<br />

## How to used
1. open script for editing
2. update target parmaters under maps_list
3. make sure all targets are on the same LAN as host
4. make sure the boot switchs are in sd card mode
4. run application
5. when done (see log file) change borad switch to boot from intrernal emmc
5. boot the board

### Extra 
* **log file** - the script generate a .log file called log.upgrade.log at the same folder as the script.<br />
* **documentation** - script's documentation at [Xilinx SCS Pages](https://insightec.lightning.force.com/lightning/page/home). [**TDB**]

## Authors
Israel Yesha'ayahu (israely@insightec.com)

## copyright
Copyright © 2002 by InSightec
