# Commands to get github work
login to pangeo jupyter lab : https://pangeo-eosc.vm.fedcloud.eu/jupyterhub/hub/user-redirect/git-pull?repo=https%3A//github.com/pangeo-data/escience-2022&urlpath=lab/tree/escience-2022/tutorial/pangeo101/&branch=main

#### open a terminal: 
cd to escience-2022 folder
git config --global user.name "username"
git config --global user.email email
gh auth login

#### get a code with 8 numbers/alphabet
open a webbrouser https://github.com/login/device, insert the code
Then it's connected with github.

#### Now you can clone the Group repository from Github:
git clone https://github.com/eScience-course/Tjaernoe2022-group2.git

#### Now you can add materials, commit and push to it.

# Useful examples:
Introduction to CMIP6:
/home/jovyan/escience-2022/tutorial/pangeo101/data_discovery.ipynb

Get data from pangeo and plot:
/home/jovyan/escience-2022/tutorial/examples/notebooks/CMIP6_example.ipynb

pre-industrial years: 1850-1900 (IPCC) 

# About CMIP6 data
What Amon/Emon etc means: https://clipc-services.ceda.ac.uk/dreq/index/miptable.html

Check volcanic forcing: CMIP6.CMIP.NCAR.CESM2.historical.r11i1p1f1.AERmon.abs550aer.gn (CMIP6.CMIP.NCAR.CESM2.historical.r11i1p1f1.AERmon.od550so4.gn)

# check system resource
open a terminal cd to the start folder, use "df -h", it will show:
Filesystem                                                                               Size  Used Avail Use% Mounted on
overlay                                                                                   78G  8.3G   70G  11% /
tmpfs                                                                                     64M     0   64M   0% /dev
kubeserver.localdomain:/pv/daskhub-claim-zzhuo-pvc-34342ab8-fc08-4703-a2e3-282c3b95fa00  1.8T   13G  1.7T   1% /home/jovyan
/dev/sda1                                                                                 78G  8.3G   70G  11% /etc/hosts
shm                                                                                       64M  8.0K   64M   1% /dev/shm
tmpfs                                                                                     32G     0   32G   0% /proc/acpi
tmpfs                                                                                     32G     0   32G   0% /proc/scsi
tmpfs                                                                                     32G     0   32G   0% /sys/firmware