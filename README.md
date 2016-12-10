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
| cogl | cogl-1.18.2-12.el7.src.rpm | needs to be build with gtk3-devel-3.8.8-10.el7.armv5tel.rpm **to check**
| gc | gc-7.2d-7.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| glassfish-fastinfoset | glassfish-fastinfoset-1.2.12-9.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| gsl | gsl-1.15-13.el7.src.rpm | needs to be build with '-D "check exit 0"'
| gutenprint | gutenprint-5.2.9-18.el7.src.rpm | needs to be build with '-D "check exit 0"'
| irqbalance | irqbalance-1.0.7-6.el7.src.rpm | needs systemd-devel to be installed by hand for successful build
| jflex | jflex-1.4.3-20.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51
| libcmis | libcmis-0.5.1-2.el7.src.rpm | needs to be build with '-D "check exit 0"' **to check**
| libqb | libqb-1.0-1.el7.src.rpm | needs to be build with '-D "check exit 0"' **to check**
| m2crypto | m2crypto-0.21.1-17.el7.src.rpm | needs to be build with '-D "check exit 0" -D "debug_package %{nil}"'
| pki-core | pki-core-10.3.3-10.el7.src.rpm | needs to be build with java-1.8.0-openjdk-1.8.0.65-2.b17.el7.armv5tel **to check**
| qdox | qdox-1.12.1-10.el7.src.rpm | needs to be build with java-1.7.0-openjdk-devel-1.7.0.51 **to check**
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
|


### not included due to build errors

| Package | SRPM | error
|---|---|---
|
