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
| flatpak | flatpak-0.8.7-1.el7.src.rpm | needs to be build with redhat-rpm-config from 7.3
| gawk | gawk-4.0.2-4.el7_3.1.src.rpm | needs 'util-linux' to be installed by hand for successful build
| gc | gc-7.2d-7.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| glassfish-fastinfoset | glassfish-fastinfoset-1.2.12-9.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| gsl | gsl-1.15-13.el7.src.rpm | needs to be build with '-D "check exit 0"'
| gstreamer-plugins-bad-free | gstreamer-plugins-bad-free-0.10.23-23.el7.src.rpm | needs to be build with redsleeve 7.3
| gstreamer-plugins-good | gstreamer-plugins-good-0.10.31-13.el7.src.rpm | needs to be build with redsleeve 7.3
| gutenprint | gutenprint-5.2.9-18.el7.src.rpm | needs to be build with '-D "check exit 0"'
| irqbalance | irqbalance-1.0.7-9.el7.src.rpm | needs systemd-devel to be installed by hand for successful build
| jflex | jflex-1.4.3-20.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| libcmis | libcmis-0.5.1-2.el7.src.rpm | needs to be build with '-D "check exit 0"'
| libepoxy | libepoxy-1.3.1-1.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| libusnic_verbs | libusnic_verbs-2.0.1-5.el7.src.rpm | needs to be build with redsleeve 7.3
| log4j | log4j-1.2.17-16.el7_4.src.rpm | needs to be build without java-1.8.0-openjdk
| m2crypto | m2crypto-0.21.1-17.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| maven | maven-3.0.5-17.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| mesa-private-llvm | mesa-private-llvm-3.8.x | version to new for armv5, downgraded to 3.7.1 
| msv | msv-2013.5.1-7.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| prelink | prelink-0.5.0-9.el7.src.rpm | needs to be build with older versions of: binutils, cpp, gcc*, glibc*, libgcc, libgomp, libstdc* (the 7.2 versions). Not sure what is wrong with the 7.3 versions
| pykickstart | pykickstart-1.99.66.12-1.el7.src.rpm | needs to be build with '-D "check exit 0"'
| tog-pegasus | tog-pegasus-2.14.1-5.el7.src.rpm | needs to be build with redsleeve 7.3
| uom-lib | uom-lib-1.0.1-5.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| velocity | velocity-1.7-10.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| xmvn | xmvn-1.3.0-6.el7_3.src.rpm | needs to be build without java-1.8.0-openjdk
| xdg-desktop-portal | xdg-desktop-portal-0.5-2.el7.src.rpm | needs to be build with redhat-rpm-config from 7.3



## Packages not included in RedSleeve

Some packages that are present upstream are not in Redsleeve for a variety of reasons.


### not included for branding reasons

| Package | SRPM | reason
|---|---|---
| anaconda | anaconda-21.48.22.121-1.el7.centos.src.rpm | branding issue / removed because it was not used
| anaconda-user-help | anaconda-user-help-7.3.2-1.el7.src.rpm | branding issue / removed because it was not used
| centos-bookmarks | centos-bookmarks-7-1.el7.src.rpm | replaced with redsleeve-bookmarks
| centos-indexhtml | centos-indexhtml-7-9.el7.centos.src.rpm | replaced with redsleeve-indexhtml
| centos-logos | centos-logos-70.0.6-3.el7.centos.src.rpm | replaced with redsleeve-logos
| centos-release | centos-release-7-4.1708.el7.centos.src.rpm | replaced with redsleeve-release
| initial-setup | initial-setup-0.3.9.40-1.el7.centos.src.rpm | branding issue / removed because it was not used
| kabi-yum-plugins | kabi-yum-plugins-1.0-3.el7.centos.src.rpm | branding issue / removed because it was not used
| oscap-anaconda-addon | oscap-anaconda-addon-0.7-15.el7.centos.src.rpm | branding issue / removed because it was not used
| redhat-support-lib-python | redhat-support-lib-python-0.9.7-6.el7.src.rpm | branding issue / removed because it was not used
| redhat-support-tool | redhat-support-tool-0.9.9-3.el7.src.rpm | branding issue / removed because it was not used
| subscription-manager | subscription-manager-1.19.21-1.el7.centos.src.rpm | branding issue / removed because it was not used


### not included due to incompatibel architectures

| Package | SRPM
|---|---
| acpid | acpid-2.0.19-8.el7.src.rpm
| biosdevname | biosdevname-0.7.2-2.el7.src.rpm
| booth | booth-1.0-7.ef769ef.git.el7.src.rpm
| clufter | clufter-0.76.0-1.el7.src.rpm
| cpuid | cpuid-20170122-6.el7.src.rpm
| crash-gcore-command | crash-gcore-command-1.3.1-0.el7.src.rpm
| crash-ptdump-command | crash-ptdump-command-1.0.3-2.el7.src.rpm
| crash-trace-command | crash-trace-command-2.0-12.el7.src.rpm
| criu | criu-2.12-2.el7.src.rpm
| dbxtool | dbxtool-7-1.el7.src.rpm
| dlm | dlm-4.0.7-1.el7.src.rpm
| dmidecode | dmidecode-3.0-5.el7.src.rpm
| dyninst | dyninst-9.3.1-1.el7.src.rpm
| efibootmgr | efibootmgr-15-2.el7.src.rpm
| efivar | efivar-31-4.el7.src.rpm
| fence-virt | fence-virt-0.3.2-12.el7.src.rpm
| fwupdate | fwupdate-9-8.el7.src.rpm
| gcc-libraries | gcc-libraries-7.1.1-2.2.1.el7.src.rpm
| gfs2-utils | gfs2-utils-3.1.10-3.el7.src.rpm
| glusterfs | glusterfs-3.8.4-18.4.el7.centos.src.rpm
| gnome-boxes | gnome-boxes-3.22.4-4.el7.src.rpm
| gnu-efi | gnu-efi-3.0.5-9.el7.src.rpm
| golang-github-cpuguy83-go-md2man | golang-github-cpuguy83-go-md2man-1.0.4-4.el7.src.rpm
| golang-github-gorilla-context | golang-github-gorilla-context-0-0.24.gitb06ed15.el7.src.rpm
| grub2 | grub2-2.02-0.64.el7.centos.src.rpm
| hsakmt | hsakmt-1.0.0-7.el7.src.rpm
| hyperv-daemons | hyperv-daemons-0-0.30.20161211git.el7.src.rpm
| infinipath-psm | infinipath-psm-3.3-25_g326b95a_open.1.el7.src.rpm
| intel-cmt-cat | intel-cmt-cat-0.1.5-2.el7.src.rpm
| ixpdimm_sw | ixpdimm_sw-01.00.00.2111-1.el7.src.rpm
| libguestfs | libguestfs-1.36.3-6.el7_4.3.src.rpm
| libguestfs-winsupport | libguestfs-winsupport-7.2-2.el7.src.rpm
| libinvm-cim | libinvm-cim-1.0.0.1041-3.el7.src.rpm
| libinvm-cli | libinvm-cli-1.0.0.1096-3.el7.src.rpm
| libinvm-i18n | libinvm-i18n-1.0.0.1016-3.el7.src.rpm
| libpsm2 | libpsm2-10.2.63-2.el7.src.rpm
| libvma | libvma-8.1.4-1.el7.src.rpm
| mcelog | mcelog-144-3.94d853b2ea81.el7.src.rpm
| memkind | memkind-1.5.0-1.el7.src.rpm
| memtest86+ | memtest86+-5.01-2.el7.src.rpm
| microcode_ctl | microcode_ctl-2.1-22.el7.src.rpm
| mkbootdisk | mkbootdisk-1.5.5-11.el7.src.rpm
| numad | numad-0.5-17.20150602git.el7.src.rpm
| nvml | nvml-1.2.1-4.el7.src.rpm
| opa-ff | opa-ff-10.3.1.0-11.el7.src.rpm
| opa-fm | opa-fm-10.3.1.0-8.el7.src.rpm
| open-vm-tools | open-vm-tools-10.1.5-3.el7.src.rpm
| oracleasm | oracleasm-2.0.8-19.el7.src.rpm
| ovmf | ovmf-20170228-5.gitc325e41585e3.el7.src.rpm
| pacemaker | pacemaker-1.1.16-12.el7_4.2.src.rpm
| pcs | pcs-0.9.158-6.el7.centos.src.rpm
| pesign | pesign-0.109-10.el7.src.rpm
| rasdaemon | rasdaemon-0.4.1-28.el7.src.rpm
| ras-utils | ras-utils-7.0-6.el7.src.rpm
| sanlock | sanlock-3.5.0-1.el7.src.rpm
| sbd | sbd-1.3.0-3.el7.src.rpm
| seabios | seabios-1.10.2-3.el7_4.1.src.rpm
| sgabios | sgabios-0.20110622svn-4.el7.src.rpm
| shim | shim-12-1.el7.centos.src.rpm
| shim-signed | shim-signed-12-1.el7.centos.src.rpm
| spice | spice-0.12.8-2.el7.1.src.rpm
| spice-xpi | spice-xpi-2.8-8.el7.src.rpm
| supermin | supermin-5.1.16-4.el7.src.rpm
| syslinux | syslinux-4.05-13.el7.src.rpm
| tboot | tboot-1.9.5-1.el7.src.rpm
| tpm2-tools | tpm2-tools-1.1.0-7.el7.src.rpm
| tpm2-tss | tpm2-tss-1.0-5.el7.src.rpm
| x86info | x86info-1.30-6.el7.src.rpm
| xorg-x11-drv-intel | xorg-x11-drv-intel-2.99.917-26.20160929.el7.src.rpm
| xorg-x11-drv-openchrome | xorg-x11-drv-openchrome-0.5.0-3.el7.src.rpm
| xorg-x11-drv-vesa | xorg-x11-drv-vesa-2.3.2-25.1.el7.src.rpm
| xorg-x11-drv-vmmouse | xorg-x11-drv-vmmouse-13.1.0-1.el7.src.rpm
| xorg-x11-drv-vmware | xorg-x11-drv-vmware-13.2.1-1.el7.src.rpm



### not included due to build or install errors

| Package | SRPM | error
|---|---|---
| ceph-common | ceph-common-0.94.5-2.el7.src.rpm | #error You must enable NEON instructions (e.g. -mfloat-abi=softfp -mfpu=neon) to use arm_neon.h
| cockpit | cockpit-138-9.el7.src.rpm | cannot be installed due to missing deps
| compat-dapl | compat-dapl-1.2.19-4.el7.src.rpm | depends on dapl which is not available for arm
| compat-gcc-32 | compat-gcc-32-3.2.3-72.el7.src.rpm | Error: selected processor does not support ARM mode
| compat-gcc-34 | compat-gcc-34-3.4.6-32.el7.src.rpm | Error: selected processor does not support ARM mode
| compat-gcc-44 | compat-gcc-44-4.4.7-8.el7.src.rpm | Error: unrecognized symbol type ""
| compat-glibc | compat-glibc-2.12-4.el7.centos.src.rpm | configure: error: The armv5tel is not supported.
| dapl | dapl-2.1.5-2.el7.src.rpm | error: #error UNDEFINED ARCH
| ksc | ksc-0.9.18-1.el7.src.rpm | cannot be installed due to missing deps
| llvm-private | llvm-private-3.9.1-9.el7.src.rpm | stl_deque.h:539:65: error: invalid application of 'sizeof' to incomplete type 'std::packaged_task<void()>'
| mpitests | mpitests-4.1-1.el7.src.rpm | depends on mvapich2-devel which doesnt build on arm   
| mstflint | mstflint-4.6.0-2.el7.src.rpm | error Unknown CPU architecture using the linux OS   
| mvapich2 | mvapich2-2.2-1.el7.src.rpm | fatal error: asm/timex.h: No such file or directory   
| openssl098e | openssl098e-0.9.8e-29.el7.centos.3.src.rpm | linux-arm not on the supported compiler list
| perftest | perftest-3.4-1.el7.src.rpm | fatal error: asm/timex.h: No such file or directory   
| tbb | tbb-4.1-9.20130314.el7.src.rpm | error: #error Threading Building Blocks ARM port requires an ARMv7-a architecture.
| tuned | tuned-2.8.0-5.el7.src.rpm | cannot be installed due to missing deps
| usbguard | usbguard-0.7.0-3.el7.src.rpm | tuple:1090:70: error: using invalid field 'std::pair<_T1, _T2>::second'
| xorg-x11-drivers | xorg-x11-drivers-7.7-6.el7.src.rpm | cannot be installed due to missing deps
| xorg-x11-drv-nouveau | xorg-x11-drv-nouveau-1.0.13-3.el7.src.rpm | cannot be installed due to missing deps
