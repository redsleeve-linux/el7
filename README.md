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
| bolt | bolt-0.7-1.el7.src.rpm | does no longer build on arm, keeping at version 0.4-3
| corosync | corosync-2.4.3-6.el7.src.rpm | make SRPM from git in stead of from the vault 
| devhelp | devhelp-3.28.1-1.el7.src.rpm | needs libatomic.so.1.2.0 from gcc7 to build
| dnssec-trigger | dnssec-trigger-0.11-22.el7.src.rpm | needs NetworkManager to be installed by hand for successful build
| elfutils | elfutils-0.176-2.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| evolution | evolution-3.28.5-5.el7.src.rpm |needs libatomic.so.1.2.0 from gcc7 to build
| evolution-data-server | evolution-data-server-3.28.5-3.el7.src.rpm |needs libatomic.so.1.2.0 from gcc7 to build
| gawk | gawk-4.0.2-4.el7_3.1.src.rpm | needs 'util-linux' to be installed by hand for successful build
| gc | gc-7.2d-7.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| gcc | gcc-4.8.5-39.el7.src.rpm | make SRPM from git in stead of from the vault, use the commit before last
| gcc-libraries | gcc-libraries-8.3.1-2.1.1.el7.src.rpm | make SRPM from git in stead of from the vault
| glassfish-fastinfoset | glassfish-fastinfoset-1.2.12-9.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| gnome-documents | gnome-documents-3.28.2-2.el7.src.rpm |needs libatomic.so.1.2.0 from gcc7 to build
| gnome-initial-setup | gnome-initial-setup-3.28.0-2.el7.src.rpm |needs libatomic.so.1.2.0 from gcc7 to build
| gsl | gsl-1.15-13.el7.src.rpm | needs to be build with '-D "check exit 0"'
| gstreamer-plugins-bad-free | gstreamer-plugins-bad-free-0.10.23-23.el7.src.rpm | needs to be build with redsleeve 7.3
| gstreamer-plugins-good | gstreamer-plugins-good-0.10.31-13.el7.src.rpm | needs to be build with redsleeve 7.3
| gutenprint | gutenprint-5.2.9-18.el7.src.rpm | needs to be build with '-D "check exit 0"'
| hawtjni | hawtjni-1.6-10.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel
| ipa | ipa-4.6.5-11.el7.centos.src.rpm | needs to be build with '-D "centos 7"'
| jflex | jflex-1.4.3-20.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| keepalived | keepalived-1.3.5-16.el7.src.rpm | needs to be build ipset-devel from RSEL 7.6
| libcmis | libcmis-0.5.1-2.el7.src.rpm | needs to be build with '-D "check exit 0"'
| libepoxy | libepoxy-1.5.2-1.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| libglvnd | libglvnd-1.0.1-0.8.git5baa1e5.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| log4j | log4j-1.2.17-16.el7_4.src.rpm | needs to be build without java-1.8.0-openjdk
| m2crypto | m2crypto-0.21.1-17.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| maven | maven-3.0.5-17.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| mesa-private-llvm | mesa-private-llvm-3.9.1-3.el7.src.rpm | version to new for armv5, downgraded to 3.7.1 
| msv | msv-2013.5.1-7.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| pacemaker | pacemaker-1.1.20-5.el7.src.rpm | needs to be build with '-D "check exit 0"'
| prelink | prelink-0.5.0-9.el7.src.rpm | needs to be build with older versions of: binutils, cpp, gcc*, glibc*, libgcc, libgomp, libstdc* (the 7.2 versions). Not sure what is wrong with the 7.3 versions
| uom-lib | uom-lib-1.0.1-5.el7.src.rpm | needs to be build without java-1.8.0-openjdk
| velocity | velocity-1.7-10.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| valgrind | valgrind-3.14.0-16.el7.src.rpm | version to new for armv5, keeping at version 3.10.0
| webkitgtk4 | webkitgtk4-2.22.7-2.el7.redsleeve.src.rpm | needs libatomic.so.1.2.0 from gcc7 to build
| xmvn | xmvn-1.3.0-6.el7_3.src.rpm | needs to be build without java-1.8.0-openjdk
| yelp | yelp-3.28.1-1.el7.src.rpm | needs libatomic.so.1.2.0 from gcc7 to build



## Packages not included in RedSleeve

Some packages that are present upstream are not in Redsleeve for a variety of reasons.


### not included for branding reasons

| Package | SRPM | reason
|---|---|---
| anaconda | anaconda-21.48.22.156-1.el7.centos.src.rpm | branding issue / removed because it was not used
| anaconda-user-help | anaconda-user-help-7.5.3-1.el7.src.rpm | branding issue / removed because it was not used
| centos-bookmarks | centos-bookmarks-7-1.el7.src.rpm | replaced with redsleeve-bookmarks
| centos-indexhtml | centos-indexhtml-7-9.el7.centos.src.rpm | replaced with redsleeve-indexhtml
| centos-logos | centos-logos-70.0.6-3.el7.centos.src.rpm | replaced with redsleeve-logos
| centos-release | centos-release-7-7.1908.0.el7.centos.src.rpm | replaced with redsleeve-release
| initial-setup | initial-setup-0.3.9.44-1.el7.centos.src.rpm | branding issue / removed because it was not used
| kabi-yum-plugins | kabi-yum-plugins-1.0-3.el7.centos.src.rpm | branding issue / removed because it was not used
| oscap-anaconda-addon | oscap-anaconda-addon-0.9-3.el7.centos.src.rpm | branding issue / removed because it was not used
| redhat-support-lib-python | redhat-support-lib-python-0.9.7-6.el7.src.rpm | branding issue / removed because it was not used
| redhat-support-tool | redhat-support-tool-0.9.11-1.el7.src.rpm | branding issue / removed because it was not used
| subscription-manager | subscription-manager-1.24.13-3.el7.centos.src.rpm | branding issue / removed because it was not used


### not included due to incompatibel architectures

| Package | SRPM
|---|---
| acpid | acpid-2.0.19-9.el7.src.rpm
| biosdevname | biosdevname-0.7.3-2.el7.src.rpm
| booth | booth-1.0-8.ef769ef.git.el7.src.rpm
| clufter | clufter-0.77.1-1.el7.src.rpm
| cpuid | cpuid-20170122-6.el7.src.rpm
| crash-gcore-command | crash-gcore-command-1.3.1-0.el7.src.rpm
| crash-ptdump-command | crash-ptdump-command-1.0.3-2.el7.src.rpm
| crash-trace-command | crash-trace-command-2.0-14.el7.src.rpm
| dbxtool | dbxtool-7-1.el7.src.rpm
| dlm | dlm-4.0.7-1.el7.src.rpm
| dmidecode | dmidecode-3.2-3.el7.src.rpm
| dyninst | dyninst-9.3.1-3.el7.src.rpm
| efibootmgr | efibootmgr-17-2.el7.src.rpm
| efivar | efivar-36-12.el7.src.rpm
| fence-virt | fence-virt-0.3.2-14.el7.src.rpm
| fwupdate | fwupdate-12-5.el7.centos.src.rpm
| gfs2-utils | gfs2-utils-3.1.10-9.el7.src.rpm
| gnome-boxes | gnome-boxes-3.28.5-2.el7.src.rpm
| gnu-efi | gnu-efi-3.0.8-2.el7.src.rpm
| grub2 | grub2-2.02-0.80.el7.centos.src.rpm
| hsakmt | hsakmt-1.0.0-7.el7.src.rpm
| hyperv-daemons | hyperv-daemons-0-0.34.20180415git.el7.src.rpm
| infinipath-psm | infinipath-psm-3.3-26_g604758e_open.2.el7.src.rpm
| intel-cmt-cat | intel-cmt-cat-3.0.1-1.el7.src.rpm
| ixpdimm_sw | ixpdimm_sw-01.00.00.2111-1.el7.src.rpm
| kmod-kvdo | kmod-kvdo-6.1.1.125-5.el7.src.rpm
| libguestfs | libguestfs-1.40.2-5.el7_7.1.src.rpm
| libguestfs-winsupport | libguestfs-winsupport-7.2-3.el7.src.rpm
| libinvm-cim | libinvm-cim-1.0.0.1041-3.el7.src.rpm
| libinvm-cli | libinvm-cli-1.0.0.1096-3.el7.src.rpm
| libinvm-i18n | libinvm-i18n-1.0.0.1016-3.el7.src.rpm
| libpsm2 | libpsm2-10.3.58-1.el7.src.rpm
| libsmbios | libsmbios-2.3.3-8.el7.src.rpm
| libvma | libvma-8.7.5-1.el7.src.rpm
| mcelog | mcelog-144-10.94d853b2ea81.el7.src.rpm
| memkind | memkind-1.7.0-1.el7.src.rpm
| memtest86+ | memtest86+-5.01-2.el7.src.rpm
| microcode_ctl | microcode_ctl-2.1-53.el7.src.rpm
| mkbootdisk | mkbootdisk-1.5.5-11.el7.src.rpm
| nbdkit | nbdkit-1.2.6-1.el7_6.2.src.rpm
| numad | numad-0.5-18.20150602git.el7.src.rpm
| nvml | nvml-1.4-3.el7.src.rpm
| opa-ff | opa-ff-10.7.0.0.133-1.el7.src.rpm
| opa-fm | opa-fm-10.7.0.0.141-1.el7.src.rpm
| opal-prd | opal-prd-6.2-3.el7.src.rpm
| open-vm-tools | open-vm-tools-10.3.0-2.el7.src.rpm
| oracleasm | oracleasm-2.0.8-22.1.el7_6.src.rpm
| ovmf | ovmf-20180508-6.gitee3198e672e2.el7.src.rpm
| pesign | pesign-0.109-10.el7.src.rpm
| powerpc-utils | powerpc-utils-1.3.4-10.el7.src.rpm
| qemu-kvm-ma | qemu-kvm-ma-2.12.0-33.el7.src.rpm
| rasdaemon | rasdaemon-0.4.1-35.el7.src.rpm
| ras-utils | ras-utils-7.0-6.el7.src.rpm
| sanlock | sanlock-3.7.3-1.el7.src.rpm
| sbd | sbd-1.4.0-4.el7.src.rpm
| seabios | seabios-1.11.0-2.el7.src.rpm
| sgabios | sgabios-0.20110622svn-4.el7.src.rpm
| shim | shim-15-2.el7.centos.src.rpm
| shim-signed | shim-signed-15-2.el7.centos.src.rpm
| spice | spice-0.14.0-6.el7_6.1.src.rpm
| spice-streaming-agent | spice-streaming-agent-0.2-3.el7.src.rpm
| spice-xpi | spice-xpi-2.8-8.el7.src.rpm
| syslinux | syslinux-4.05-15.el7.src.rpm
| tboot | tboot-1.9.6-3.el7.src.rpm
| tpm2-abrmd | tpm2-abrmd-1.1.0-11.el7.src.rpm
| tpm2-tools | tpm2-tools-3.0.4-3.el7.src.rpm
| tpm2-tss | tpm2-tss-1.4.0-3.el7.src.rpm
| ucx | ucx-1.4.0-1.el7.src.rpm
| vdo | vdo-6.1.1.125-3.el7.src.rpm
| x86info | x86info-1.30-6.el7.src.rpm
| xorg-x11-drv-intel | xorg-x11-drv-intel-2.99.917-28.20180530.el7.src.rpm
| xorg-x11-drv-openchrome | xorg-x11-drv-openchrome-0.5.0-3.el7.1.src.rpm
| xorg-x11-drv-vesa | xorg-x11-drv-vesa-2.4.0-3.el7.src.rpm
| xorg-x11-drv-vmmouse | xorg-x11-drv-vmmouse-13.1.0-1.el7.1.src.rpm
| xorg-x11-drv-vmware | xorg-x11-drv-vmware-13.2.1-1.el7.1.src.rpm


### not included due to build or install errors

| Package | SRPM | error
|---|---|---
| bcc | bcc-0.6.1-2.el7.src.rpm | depends on llvm-private-devel which doesnt build on arm
| ceph-common | ceph-common-10.2.5-4.el7.src.rpm | #error You must enable NEON instructions (e.g. -mfloat-abi=softfp -mfpu=neon) to use arm_neon.h
| cockpit | cockpit-195.1-1.el7.centos.src.rpm | cannot be installed due to missing deps
| compat-dapl | compat-dapl-1.2.19-4.el7.src.rpm | depends on dapl which is not available for arm
| compat-gcc-32 | compat-gcc-32-3.2.3-72.el7.src.rpm | Error: selected processor does not support ARM mode
| compat-gcc-34 | compat-gcc-34-3.4.6-32.el7.src.rpm | Error: selected processor does not support ARM mode
| compat-gcc-44 | compat-gcc-44-4.4.7-8.el7.src.rpm | Error: unrecognized symbol type ""
| compat-glibc | compat-glibc-2.12-4.el7.centos.src.rpm | configure: error: The armv5tel is not supported.
| dapl | dapl-2.1.5-2.el7.src.rpm | error: #error UNDEFINED ARCH
| fio | fio-3.1-2.el7.src.rpm | depends on librbd1-devel (part of ceph) which doesnt build on arm
| firefox | firefox-60.3.0-1.el7.centos.src.rpm | depends on modern llvm which is not available for armv5
| ksc | ksc-0.9.22-1.el7.src.rpm | cannot be installed due to missing deps
| llvm-private | llvm-private-6.0.1-2.el7.src.rpm | stl_deque.h:539:65: error: invalid application of 'sizeof' to incomplete type 'std::packaged_task<void()>'
| mpitests | mpitests-5.4.2-1.el7.src.rpm | depends on mvapich2-devel which doesnt build on arm   
| mstflint | mstflint-4.9.0-3.el7.src.rpm | error Unknown CPU architecture using the linux OS   
| mvapich2 | mvapich2-2.2-4.el7.src.rpm | fatal error: asm/timex.h: No such file or directory   
| openssl098e | openssl098e-0.9.8e-29.el7.centos.3.src.rpm | linux-arm not on the supported compiler list
| pcs | pcs-0.9.167-3.el7.centos.1.src.rpm | cannot be installed due to missing deps
| perftest | perftest-4.2-2.el7.src.rpm | fatal error: asm/timex.h: No such file or directory   
| redfish-finder | redfish-finder-0.3-3.el7.src.rpm | cannot be installed due to missing deps
| SLOF | SLOF-20171214-3.gitfa98132.el7.src.rpm | cannot be installed due to missing deps
| tbb | tbb-4.1-9.20130314.el7.src.rpm | error: #error Threading Building Blocks ARM port requires an ARMv7-a architecture.
| thunderbird | thunderbird-60.3.0-1.el7.centos.src.rpm | depends on modern llvm which is not available for armv5
| tuned | tuned-2.11.0-5.el7_7.1.src.rpm | cannot be installed due to missing deps
| usbguard | usbguard-0.7.4-2.el7.src.rpm | tuple:1090:70: error: using invalid field 'std::pair<_T1, _T2>::second'
| virt-who | virt-who-0.24.7-1.el7.src.rpm | cannot be installed due to missing deps
| xorg-x11-drivers | xorg-x11-drivers-7.7-6.el7.src.rpm | cannot be installed due to missing deps
| xorg-x11-drv-nouveau | xorg-x11-drv-nouveau-1.0.15-1.el7.src.rpm | cannot be installed due to missing deps
