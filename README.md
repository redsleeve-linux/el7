# Redsleeve / EL7

**RedSleeve Linux** is a 3rd party [ARM](http://en.wikipedia.org/wiki/ARM_architecture) port of a Linux distribution of a Prominent North American Enterprise Linux Vendor (PNAELV). They object to being referred to by name in the context of clones and ports of their distribution, but if you are aware of [CentOS](http://en.wikipedia.org/wiki/CentOS) and [Scientific Linux](http://en.wikipedia.org/wiki/Scientific_Linux), you can probably guess what [RedSleeve](http://wiki.redsleeve.org) is based on. 


## What is in this repository

Since version EL7 of PNAELV, they no longer distribute their source themselves. However all sources are now distributed via CentOS:
* [The Vault](http://vault.centos.org/)
* [git repositories](https://git.centos.org/)

This repository contains all patches to build RedSleeve. The patches are all to the CentOS git tree of sources. They are either needed to support the armv5 cpu or to rebrand to RedSleeve.


## How to use this repository

**Details to follow**


## Extra build instructions

Some packages needed some manual love and care to build, but not really a patch:

| Package | SRPM | instruction
|---|---|---
| base64coder | base64coder-20101219-10.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| dnssec-trigger | dnssec-trigger-0.11-22.el7.src.rpm | needs NetworkManager to be installed by hand for successful build
| file-roller | file-roller-3.14.2-10.el7.src.rpm | needs to be build with glib2-devel-2.42.2-5.el7.armv5tel.rpm
| gc | gc-7.2d-7.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| gedit | gedit-3.14.3-18.el7.src.rpm | needs to be build with glib2-devel-2.42.2-5.el7.armv5tel.rpm
| glassfish-fastinfoset | glassfish-fastinfoset-1.2.12-9.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| gnome-clocks | gnome-clocks-3.14.1-2.el7.src.rpm | needs to be build with glib2-devel-2.42.2-5.el7.armv5tel.rpm
| gnome-dictionary | gnome-dictionary-3.14.2-2.el7.src.rpm | needs to be build with glib2-devel-2.42.2-5.el7.armv5tel.rpm
| golang | golang-1.6.3-2.el7.redsleeve.src.rpm | needs to be build with tzdata-2016f
| gsl | gsl-1.15-13.el7.src.rpm | needs to be build with '-D "check exit 0"'
| gutenprint | gutenprint-5.2.9-18.el7.src.rpm | needs to be build with '-D "check exit 0"'
| irqbalance | irqbalance-1.0.7-6.el7.src.rpm | needs systemd-devel to be installed by hand for successful build
| jflex | jflex-1.4.3-20.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| libcmis | libcmis-0.5.1-2.el7.src.rpm | needs to be build with '-D "check exit 0"'
| m2crypto | m2crypto-0.21.1-17.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| maven | maven-3.0.5-17.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| mesa-private-llvm | mesa-private-llvm-3.8.x | version to new for armv5, downgraded to 3.7.1 
| msv | msv-2013.5.1-7.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| nss | nss-3.21.3-2.el7_3.src.rpm | clock needs to be set before 2016-12-16 for the tests to succeed
| prelink | prelink-0.5.0-9.el7.src.rpm | needs to be build with older versions of: binutils, cpp, gcc*, glibc*, libgcc, libgomp, libstdc* (the 7.2 versions). Not sure what is wrong with the 7.3 versions
| ruby | ruby-2.0.0.648-29.el7.src.rpm | needs to be build with openssl*-1.0.1e-51.el7.5.armv5tel
| tigervnc | tigervnc-1.3.1-9.el7.src.rpm | needs to be build with xorg-x11-server-source-1.17.2-10.el7.noarch.rpm
| velocity | velocity-1.7-10.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51


## Packages not included in RedSleeve

Some packages that are present upstream are not in Redsleeve for a variety of reasons.


### not included for branding reasons

| Package | SRPM | reason
|---|---|---
| anaconda | anaconda-21.48.22.93-1.el7.centos.1.src.rpm | branding issue / removed because it was not used
| centos-bookmarks | centos-bookmarks-7-1.el7.src.rpm | replaced with redsleeve-bookmarks
| centos-indexhtml | centos-indexhtml-7-9.el7.centos.src.rpm | replaced with redsleeve-indexhtml
| centos-logos | centos-logos-70.0.6-3.el7.centos.src.rpm | replaced with redsleeve-logos
| centos-release | centos-release-7-0.1406.el7.centos.2.5.src.rpm | replaced with redsleeve-release
| initial-setup | initial-setup-0.3.9.36-1.el7.src.rpm | branding issue / removed because it was not used
| kabi-yum-plugins | kabi-yum-plugins-1.0-3.el7.centos.src.rpm | branding issue / removed because it was not used
| redhat-support-lib-python | redhat-support-lib-python-0.9.7-6.el7.src.rpm | branding issue / removed because it was not used
| redhat-support-tool | redhat-support-tool-0.9.8-6.el7.src.rpm | branding issue / removed because it was not used
| subscription-manager | subscription-manager-1.17.15-1.el7.src.rpm | branding issue / removed because it was not used


### not included due to incompatibel architectures

| Package | SRPM
|---|---
| acpid | acpid-2.0.19-6.el7.src.rpm
| biosdevname | biosdevname-0.7.2-1.el7.src.rpm
| booth | booth-1.0-6.ef769ef.git.el7.src.rpm
| ceph-common | ceph-common-0.94.5-1.el7.src.rpm
| clufter | clufter-0.59.5-2.el7.src.rpm
| cpuid | cpuid-20151017-4.el7.src.rpm
| crash-gcore-command | crash-gcore-command-1.3.1-0.el7.src.rpm
| crash-ptdump-command | crash-ptdump-command-1.0.3-1.el7.src.rpm
| crash-trace-command | crash-trace-command-2.0-10.el7.src.rpm
| criu | criu-2.3-2.el7.src.rpm
| dlm | dlm-4.0.6-1.el7.src.rpm
| dmidecode | dmidecode-3.0-2.el7.src.rpm
| dyninst | dyninst-8.2.0-2.el7.src.rpm
| efibootmgr | efibootmgr-0.8.0-10.el7.src.rpm
| efivar | efivar-0.11-1.el7.src.rpm
| fence-virt | fence-virt-0.3.2-5.el7.src.rpm
| gcc-libraries | gcc-libraries-5.3.1-3.1.el7.src.rpm
| gfs2-utils | gfs2-utils-3.1.9-3.el7.src.rpm
| glusterfs | glusterfs-3.7.9-12.el7.centos.src.rpm
| gnome-boxes | gnome-boxes-3.14.3.1-10.el7.src.rpm
| gnu-efi | gnu-efi-3.0.2-2.el7.src.rpm
| golang-github-cpuguy83-go-md2man | golang-github-cpuguy83-go-md2man-1.0.4-2.el7_2.src.rpm
| grub2 | grub2-2.02-0.44.el7.centos.src.rpm
| hsakmt | hsakmt-1.0.0-7.el7.src.rpm
| hyperv-daemons | hyperv-daemons-0-0.29.20160216git.el7.src.rpm
| infinipath-psm | infinipath-psm-3.3-22_g4abbc60_open.2.el7.src.rpm
| ixpdimm_sw | ixpdimm_sw-01.00.00.2111-1.el7.src.rpm
| libguestfs | libguestfs-1.32.7-3.el7.centos.src.rpm
| libguestfs-winsupport | libguestfs-winsupport-7.2-1.el7.src.rpm
| libhfi1 | libhfi1-0.5-23.el7.src.rpm
| libinvm-cim | libinvm-cim-1.0.0.1041-3.el7.src.rpm
| libinvm-cli | libinvm-cli-1.0.0.1096-3.el7.src.rpm
| libinvm-i18n | libinvm-i18n-1.0.0.1016-3.el7.src.rpm
| libipathverbs | libipathverbs-1.3-2.el7.src.rpm
| libmspack | libmspack-0.5-0.4.alpha.el7.src.rpm
| libpsm2 | libpsm2-10.2.33-1.el7.src.rpm
| libvma | libvma-8.1.4-1.el7.src.rpm
| mcelog | mcelog-136-2.e4aca63.el7_3.src.rpm
| memkind | memkind-1.1.0-1.el7.src.rpm
| memtest86+ | memtest86+-5.01-2.el7.src.rpm
| microcode_ctl | microcode_ctl-2.1-16.el7.src.rpm
| mkbootdisk | mkbootdisk-1.5.5-11.el7.src.rpm
| numad | numad-0.5-17.20150602git.el7.src.rpm
| nvml | nvml-1.1-4.el7.src.rpm
| opa-ff | opa-ff-10.1.0.0-127.el7.src.rpm
| opa-fm | opa-fm-10.1.0.0-145.el7.src.rpm
| open-vm-tools | open-vm-tools-10.0.5-2.el7.src.rpm
| oracleasm | oracleasm-2.0.8-17.el7.centos.src.rpm
| pacemaker | pacemaker-1.1.15-11.el7_3.2.src.rpm
| pesign | pesign-0.109-10.el7.src.rpm
| rasdaemon | rasdaemon-0.4.1-24.el7.src.rpm
| ras-utils | ras-utils-7.0-6.el7.src.rpm
| sanlock | sanlock-3.4.0-1.el7.src.rpm
| sbd | sbd-1.2.1-21.el7.src.rpm
| seabios | seabios-1.9.1-5.el7.src.rpm
| sgabios | sgabios-0.20110622svn-4.el7.src.rpm
| shim | shim-0.9-1.el7.centos.src.rpm
| shim-signed | shim-signed-0.9-2.el7.src.rpm
| spice | spice-0.12.4-19.el7.src.rpm
| spice-xpi | spice-xpi-2.8-8.el7.src.rpm
| supermin | supermin-5.1.16-4.el7.src.rpm
| syslinux | syslinux-4.05-13.el7.src.rpm
| tboot | tboot-1.9.4-2.el7.src.rpm
| x86info | x86info-1.30-6.el7.src.rpm
| xorg-x11-drv-intel | xorg-x11-drv-intel-2.99.917-22.20151206.el7.src.rpm
| xorg-x11-drv-openchrome | xorg-x11-drv-openchrome-0.3.3-14.el7.src.rpm
| xorg-x11-drv-vesa | xorg-x11-drv-vesa-2.3.2-20.el7.src.rpm
| xorg-x11-drv-vmmouse | xorg-x11-drv-vmmouse-13.0.0-12.el7.src.rpm
| xorg-x11-drv-vmware | xorg-x11-drv-vmware-13.0.2-7.20150211git8f0cf7c.el7.src.rpm



### not included due to build or install errors

| Package | SRPM | error
|---|---|---
| compat-dapl | compat-dapl-1.2.19-4.el7.src.rpm | depends on dapl which is not available for arm
| compat-gcc-32 | compat-gcc-32-3.2.3-72.el7.src.rpm | Error: selected processor does not support ARM mode
| compat-gcc-34 | compat-gcc-34-3.4.6-32.el7.src.rpm | Error: selected processor does not support ARM mode
| compat-gcc-44 | compat-gcc-44-4.4.7-8.el7.src.rpm | Error: unrecognized symbol type ""
| compat-glibc | compat-glibc-2.12-4.el7.centos.src.rpm | configure: error: The armv5tel is not supported.
| dapl | dapl-2.1.5-2.el7.src.rpm | error: #error UNDEFINED ARCH
| ksc | ksc-0.9.18-1.el7.src.rpm | cannot be installed due to missing deps
| mpitests | mpitests-4.1-1.el7.src.rpm | depends on mvapich2-devel which doesnt build on arm
| mstflint | mstflint-4.3.0-1.49.g9b9af70.1.el7.src.rpm | error Unknown CPU architecture using the linux OS
| mvapich2 | mvapich2-2.2-0.3.rc1.el7.src.rpm | fatal error: asm/timex.h: No such file or directory
| openssl098e | openssl098e-0.9.8e-29.el7.centos.3.src.rpm | linux-arm not on the supported compiler list
| perftest | perftest-3.0-7.el7.src.rpm | fatal error: asm/timex.h: No such file or directory
| tbb | tbb-4.1-9.20130314.el7.src.rpm | error: #error Threading Building Blocks ARM port requires an ARMv7-a architecture.
| tuned | tuned-2.7.1-3.el7_3.1.src.rpm | cannot be installed due to missing deps
| pcs | pcs-0.9.152-10.el7.centos.src.rpm | depends on pacemaker which doesnt build on arm
| xorg-x11-drivers | xorg-x11-drivers-7.7-6.el7.src.rpm | cannot be installed due to missing deps
| xorg-x11-drv-nouveau | xorg-x11-drv-nouveau-1.0.11-4.el7.src.rpm | cannot be installed due to missing deps
