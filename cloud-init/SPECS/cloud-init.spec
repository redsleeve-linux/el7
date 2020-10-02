%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?license: %global license %%doc}

# The only reason we are archful is because dmidecode is ExclusiveArch
# https://bugzilla.redhat.com/show_bug.cgi?id=1067089
%global debug_package %{nil}

Name:           cloud-init
Version:        18.5
Release:        6%{?dist}.5.redsleeve
Summary:        Cloud instance init scripts

Group:          System Environment/Base
License:        GPLv3
URL:            http://launchpad.net/cloud-init
Source0:        https://launchpad.net/cloud-init/trunk/%{version}/+download/%{name}-%{version}.tar.gz
Source1:        cloud-init-tmpfiles.conf

Patch0001: 0001-Add-initial-redhat-setup.patch
Patch0002: 0002-Do-not-write-NM_CONTROLLED-no-in-generated-interface.patch
Patch0003: 0003-limit-permissions-on-def_log_file.patch
Patch0004: 0004-remove-tee-command-from-logging-configuration.patch
Patch0005: 0005-azure-ensure-that-networkmanager-hook-script-runs.patch
Patch0006: 0006-sysconfig-Don-t-write-BOOTPROTO-dhcp-for-ipv6-dhcp.patch
Patch0007: 0007-DataSourceAzure.py-use-hostnamectl-to-set-hostname.patch
Patch0008: 0008-sysconfig-Don-t-disable-IPV6_AUTOCONF.patch
Patch0009: 0009-net-Wait-for-dhclient-to-daemonize-before-reading-le.patch
Patch0010: 0010-cloud-init-per-don-t-use-dashes-in-sem-names.patch
Patch0011: 0011-azure-Filter-list-of-ssh-keys-pulled-from-fabric.patch
Patch0012: 0012-include-NOZEROCONF-yes-in-etc-sysconfig-network.patch
# For bz#1687565 - cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 7]
Patch13: ci-Azure-Ensure-platform-random_seed-is-always-serializ.patch
# For bz#1687565 - cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 7]
Patch14: ci-DatasourceAzure-add-additional-logging-for-azure-dat.patch
# For bz#1687565 - cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 7]
Patch15: ci-Azure-Changes-to-the-Hyper-V-KVP-Reporter.patch
# For bz#1687565 - cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 7]
Patch16: ci-DataSourceAzure-Adjust-timeout-for-polling-IMDS.patch
# For bz#1687565 - cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 7]
Patch17: ci-cc_mounts-check-if-mount-a-on-no-change-fstab-path.patch
# For bz#1707725 - [WALA][cloud] cloud-init dhclient-hook script has some unexpected side-effects on Azure
Patch18: ci-Revert-azure-ensure-that-networkmanager-hook-script-.patch
# For bz#1726701 - [Azure] [RHEL 7.8] Cloud-init fixes to support fast provisioning for Azure
Patch19: ci-Azure-Return-static-fallback-address-as-if-failed-to.patch
# For bz#1593010 - [cloud-init][RHVM]cloud-init network configuration does not persist reboot [RHEL 7.8]
Patch20: ci-Fix-for-network-configuration-not-persisting-after-r.patch
# For bz#1744526 - [cloud-init][OpenStack] cloud-init can't persist instance-data.json
Patch21: ci-util-json.dumps-on-python-2.7-will-handle-UnicodeDec.patch
# For bz#1810064 - cloud-init Azure byte swap (hyperV Gen2 Only) [rhel-7.8.z]
Patch22: ci-azure-avoid.patch
# For bz#1802173 - [cloud-init][rhel-7.8.z]cloud-init cloud-final.service fail with KeyError: 'modules-init' after upgrade to version 18.2-1.el7_6.1 in RHV
Patch23: ci-cmd-main.py-Fix-missing-modules-init-key-in-modes-di.patch
# For bz#1801094 - [RHEL7] swapon fails with "swapfile has holes" when created on a xfs filesystem by cloud-init [rhel-7.8.z]
Patch24: ci-Do-not-use-fallocate-in-swap-file-creation-on-xfs.-7.patch
# For bz#1801094 - [RHEL7] swapon fails with "swapfile has holes" when created on a xfs filesystem by cloud-init [rhel-7.8.z]
Patch25: ci-swap-file-size-being-used-before-checked-if-str-315.patch
# For bz#1801094 - [RHEL7] swapon fails with "swapfile has holes" when created on a xfs filesystem by cloud-init [rhel-7.8.z]
Patch26: ci-cc_mounts-fix-incorrect-format-specifiers-316.patch
# For bz#1827207 - Support for AWS IMDS v2 (available in cloud-init 19.4) [rhel-7.8.z]
Patch27: ci-New-data-source-for-the-Exoscale.com-cloud-platform.patch
# For bz#1827207 - Support for AWS IMDS v2 (available in cloud-init 19.4) [rhel-7.8.z]
Patch28: ci-Add-support-for-publishing-host-keys-to-GCE-guest-at.patch
# For bz#1827207 - Support for AWS IMDS v2 (available in cloud-init 19.4) [rhel-7.8.z]
Patch29: ci-exoscale-fix-sysconfig-cloud_config_modules-override.patch
# For bz#1827207 - Support for AWS IMDS v2 (available in cloud-init 19.4) [rhel-7.8.z]
Patch30: ci-exoscale-Increase-url_max_wait-to-120s.patch
# For bz#1827207 - Support for AWS IMDS v2 (available in cloud-init 19.4) [rhel-7.8.z]
Patch31: ci-ec2-Add-support-for-AWS-IMDS-v2-session-oriented-55.patch
# For bz#1832177 - [Azure] cloud-init provisioning failed in Azure [rhel-7.8.z]
Patch32: ci-url_helper-read_file_or_url-should-pass-headers-para.patch

Patch9999: cloud-init-redsleeve-user.patch


# Deal with noarch -> arch
# https://bugzilla.redhat.com/show_bug.cgi?id=1067089
Obsoletes:      cloud-init < 0.7.5-3

BuildRequires:  python-devel
BuildRequires:  python-requests
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-yaml
BuildRequires:  systemd-units
BuildRequires:  git

%ifarch %{?ix86} x86_64 ia64
Requires:       dmidecode
%endif
Requires:       e2fsprogs
Requires:       iproute
Requires:       libselinux-python
Requires:       net-tools
Requires:       policycoreutils-python
Requires:       procps
Requires:       python-configobj
Requires:       python-jinja2
Requires:       python-jsonpatch
Requires:       python-prettytable
Requires:       python-requests
Requires:       python-setuptools
Requires:       python-six
Requires:       PyYAML
Requires:       pyserial
Requires:       shadow-utils
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description
Cloud-init is a set of init scripts for cloud instances.  Cloud instances
need special scripts to run during initialization to retrieve and install
ssh keys and to let the user run various scripts.


%prep
# on el7, autosetup -S git was failing with patches that
# # create new files.  rpm 4.11.3 and later has -S git_am, but
# # el7 only has 4.11.1.
%autosetup -p1 -n %{name}-%{version} -S git

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Don't ship the tests
#rm -r $RPM_BUILD_ROOT%{python_sitelib}/tests

mkdir -p $RPM_BUILD_ROOT/var/lib/cloud

# /run/cloud-init needs a tmpfiles.d entry
mkdir -p $RPM_BUILD_ROOT/run/cloud-init
mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
cp -p rhel/cloud-init-tmpfiles.conf $RPM_BUILD_ROOT/%{_tmpfilesdir}/%{name}.conf

# We supply our own config file since our software differs from Ubuntu's.
cp -p rhel/cloud.cfg $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d
cp -p tools/21-cloudinit.conf $RPM_BUILD_ROOT/%{_sysconfdir}/rsyslog.d/21-cloudinit.conf

# Make installed NetworkManager hook name less generic
mv $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d/hook-network-manager \
   $RPM_BUILD_ROOT/etc/NetworkManager/dispatcher.d/cloud-init-azure-hook

# Install our own systemd units (rhbz#1440831)
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
cp rhel/systemd/* $RPM_BUILD_ROOT%{_unitdir}/

[ ! -d $RPM_BUILD_ROOT/usr/lib/systemd/system-generators ] && mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system-generators
cp -p systemd/cloud-init-generator $RPM_BUILD_ROOT/usr/lib/systemd/system-generators

[ ! -d $RPM_BUILD_ROOT/usr/lib/%{name} ] && mkdir -p $RPM_BUILD_ROOT/usr/lib/%{name}
cp -p tools/ds-identify $RPM_BUILD_ROOT/usr/lib/%{name}/ds-identify


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    # Enabled by default per "runs once then goes away" exception
    /bin/systemctl enable cloud-config.service     >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-final.service      >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-init.service       >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-init-local.service >/dev/null 2>&1 || :
    /bin/systemctl enable cloud-init.target        >/dev/null 2>&1 || :
elif [ $1 -eq 2 ]; then
    # Upgrade. If the upgrade is from a version older than 0.7.9-8,
    # there will be stale systemd config
    /bin/systemctl is-enabled cloud-config.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-config.service >/dev/null 2>&1 || :

    /bin/systemctl is-enabled cloud-final.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-final.service >/dev/null 2>&1 || :

    /bin/systemctl is-enabled cloud-init.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-init.service >/dev/null 2>&1 || :

    /bin/systemctl is-enabled cloud-init-local.service >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-init-local.service >/dev/null 2>&1 || :

    /bin/systemctl is-enabled cloud-init.target >/dev/null 2>&1 &&
      /bin/systemctl reenable cloud-init.target >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable cloud-config.service >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-final.service  >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-init.service   >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-init-local.service >/dev/null 2>&1 || :
    /bin/systemctl --no-reload disable cloud-init.target     >/dev/null 2>&1 || :
    # One-shot services -> no need to stop
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
# One-shot services -> no need to restart


%files
%license LICENSE
%doc ChangeLog rhel/README.rhel
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg
%dir               %{_sysconfdir}/cloud/cloud.cfg.d
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/*.cfg
%doc               %{_sysconfdir}/cloud/cloud.cfg.d/README
%dir               %{_sysconfdir}/cloud/templates
%config(noreplace) %{_sysconfdir}/cloud/templates/*
%{_unitdir}/cloud-config.service
%{_unitdir}/cloud-config.target
%{_unitdir}/cloud-final.service
%{_unitdir}/cloud-init-local.service
%{_unitdir}/cloud-init.service
%{_unitdir}/cloud-init.target
%{_tmpfilesdir}/%{name}.conf
%{python_sitelib}/*
%{_libexecdir}/%{name}
%{_bindir}/cloud-init*
%doc %{_datadir}/doc/%{name}
%dir /run/cloud-init
%dir /var/lib/cloud
/etc/NetworkManager/dispatcher.d/cloud-init-azure-hook
%{_udevrulesdir}/66-azure-ephemeral.rules
%{_sysconfdir}/bash_completion.d/cloud-init
%{_bindir}/cloud-id
/usr/lib/%{name}/ds-identify
/usr/lib/systemd/system-generators/cloud-init-generator


%dir %{_sysconfdir}/rsyslog.d
%config(noreplace) %{_sysconfdir}/rsyslog.d/21-cloudinit.conf

%changelog
* Thu Jul 16 2020 Jacco Ligthart <jacco@redsleeve.org 18.5-6.el7.5.redsleeve
- rebrand for redsleeve

* Wed May 20 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-6.el7_8.5
- ci-url_helper-read_file_or_url-should-pass-headers-para.patch [bz#1832177]
- Resolves: bz#1832177
  ([Azure] cloud-init provisioning failed in Azure [rhel-7.8.z])

* Tue May 05 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-6.el7_8.4
- ci-New-data-source-for-the-Exoscale.com-cloud-platform.patch [bz#1827207]
- ci-Add-support-for-publishing-host-keys-to-GCE-guest-at.patch [bz#1827207]
- ci-exoscale-fix-sysconfig-cloud_config_modules-override.patch [bz#1827207]
- ci-exoscale-Increase-url_max_wait-to-120s.patch [bz#1827207]
- ci-ec2-Add-support-for-AWS-IMDS-v2-session-oriented-55.patch [bz#1827207]
- Resolves: bz#1827207
  (Support for AWS IMDS v2 (available in cloud-init 19.4) [rhel-7.8.z])

* Tue Apr 28 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-6.el7_8.3
- ci-Do-not-use-fallocate-in-swap-file-creation-on-xfs.-7.patch [bz#1801094]
- ci-swap-file-size-being-used-before-checked-if-str-315.patch [bz#1801094]
- ci-cc_mounts-fix-incorrect-format-specifiers-316.patch [bz#1801094]
- Resolves: bz#1801094
  ([RHEL7] swapon fails with "swapfile has holes" when created on a xfs filesystem by cloud-init [rhel-7.8.z])

* Tue Apr 14 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-6.el7_8.2
- ci-cmd-main.py-Fix-missing-modules-init-key-in-modes-di.patch [bz#1802173]
- Resolves: bz#1802173
  ([cloud-init][rhel-7.8.z]cloud-init cloud-final.service fail with KeyError: 'modules-init' after upgrade to version 18.2-1.el7_6.1 in RHV)

* Mon Mar 30 2020 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-6.el7_8.1
- ci-azure-avoid.patch [bz#1810064]
- Resolves: bz#1810064
  (cloud-init Azure byte swap (hyperV Gen2 Only) [rhel-7.8.z])

* Thu Oct 24 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-6.el7
- ci-util-json.dumps-on-python-2.7-will-handle-UnicodeDec.patch [bz#1744526]
- Resolves: bz#1744526
  ([cloud-init][OpenStack] cloud-init can't persist instance-data.json)

* Tue Sep 10 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-5.el7
- ci-Fix-for-network-configuration-not-persisting-after-r.patch [bz#1593010]
- Resolves: bz#1593010
  ([cloud-init][RHVM]cloud-init network configuration does not persist reboot [RHEL 7.8])

* Tue Aug 20 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-4.el7
- ci-Azure-Return-static-fallback-address-as-if-failed-to.patch [bz#1726701]
- Resolves: bz#1726701
  ([Azure] [RHEL 7.8] Cloud-init fixes to support fast provisioning for Azure)

* Tue May 28 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-3.el7
- ci-Revert-azure-ensure-that-networkmanager-hook-script-.patch [bz#1707725]
- Resolves: bz#1707725
  ([WALA][cloud] cloud-init dhclient-hook script has some unexpected side-effects on Azure)

* Fri May 17 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-2.el7
- ci-Azure-Ensure-platform-random_seed-is-always-serializ.patch [bz#1687565]
- ci-DatasourceAzure-add-additional-logging-for-azure-dat.patch [bz#1687565]
- ci-Azure-Changes-to-the-Hyper-V-KVP-Reporter.patch [bz#1687565]
- ci-DataSourceAzure-Adjust-timeout-for-polling-IMDS.patch [bz#1687565]
- ci-cc_mounts-check-if-mount-a-on-no-change-fstab-path.patch [bz#1687565]
- Resolves: bz#1687565
  (cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 7])

* Thu Mar 28 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.5-1.el7
- Rebase to 18.5 [bz#1687565]
- Resolves: bz#1687565
  (cloud-init 18.5 rebase for fast provisioning on Azure [RHEL 7])

* Mon Mar 25 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-5.el7
- ci-include-NOZEROCONF-yes-in-etc-sysconfig-network.patch [bz#1653131]
- Resolves: bz#1653131
  (cloud-init remove 'NOZEROCONF=yes' from /etc/sysconfig/network)

* Tue Mar 19 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-4.el7
- ci-azure-Filter-list-of-ssh-keys-pulled-from-fabric.patch [bz#1684040]
- Resolves: bz#1684040
  (CVE-2019-0816 cloud-init: extra ssh keys added to authorized_keys [rhel-7.7])

* Tue Mar 05 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-3.el7
- ci-cloud-init-per-don-t-use-dashes-in-sem-names.patch [bz#1664876]
- ci-Enable-cloud-init-by-default-on-vmware.patch [bz#1623281]
- Resolves: bz#1623281
  ([ESXi][RHEL7.6]Enable cloud-init by default on VMware)
- Resolves: bz#1664876
  (cloud-init Storage-Management Functionality Is Erasing Filesystems)

* Thu Jan 31 2019 Miroslav Rezanina <mrezanin@redhat.com> - 18.2-2.el7
- ci-net-Wait-for-dhclient-to-daemonize-before-reading-le.patch [bz#1632967]
- Resolves: bz#1632967
  ([Azure] cloud-init dhcp.py dhcp_discovery() race with dhclient with preprovisioned VM in Azure)

* Thu Jun 21 2018 Miroslav Rezanina <mrezanin@redhat.com>
- Rebase to 18.2
  Resolves: rhbz#1525267

* Tue Feb 13 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-24
- Set DHCP_HOSTNAME on Azure to allow for the hostname to be
  published correctly when bouncing the network.
  Resolves: rhbz#1434109

* Mon Jan 15 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-23
- Fix a bug tha caused cloud-init to fail as a result of trying
  to rename bonds.
  Resolves: rhbz#1512247

* Mon Jan 15 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-22
- Apply patch from -21
  Resolves: rhbz#1489270

* Mon Jan 15 2018 Ryan McCabe <rmccabe@redhat.com> 0.7.9-21
- sysconfig: Fix a potential traceback introduced in the
  0.7.9-17 build
  Resolves: rhbz#1489270

* Sun Dec 17 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-20
- sysconfig: Correct rendering for dhcp on ipv6
  Resolves: rhbz#1519271

* Thu Nov 30 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-19
- sysconfig: Fix rendering of default gateway for ipv6
  Resolves: rhbz#1492726

* Fri Nov 24 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-18
- Start the cloud-init init local service after the dbus socket is created
  so that the hostnamectl command works.
  Resolves: rhbz#1450521

* Tue Nov 21 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-17
- Correctly render DNS and DOMAIN for sysconfig
  Resolves: rhbz#1489270

* Mon Nov 20 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-16
- Disable NetworkManager management of resolv.conf if nameservers
  are specified by configuration.
  Resolves: rhbz#1454491

* Mon Nov 13 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-15
- Fix a null reference error in the rh_subscription module
  Resolves: rhbz#1498974

* Mon Nov 13 2017 Ryan McCabe <rmccabe@redhat.com> 0-7.9-14
- Include gateway if it's included in subnet configration
  Resolves: rhbz#1492726

* Sun Nov 12 2017 Ryan McCabe <rmccabe@redhat.com> 0-7.9-13
- Do proper cleanup of systemd units when upgrading from versions
  0.7.9-3 through 0.7.9-8.
  Resolves: rhbz#1465730

* Thu Nov 09 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-12
- Prevent Azure NM and dhclient hooks from running when cloud-init is
  disabled (rhbz#1474226)

* Tue Oct 31 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-11
- Fix rendering of multiple static IPs per interface file
  Resolves: rhbz#bz1497954

* Tue Sep 26 2017 Ryan McCabe <rmccabe@redhat.com> 0.7.9-10
- AliCloud: Add support for the Alibaba Cloud datasource (rhbz#1482547)

* Thu Jun 22 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-9
- RHEL/CentOS: Fix default routes for IPv4/IPv6 configuration. (rhbz#1438082)
- azure: ensure that networkmanager hook script runs (rhbz#1440831 rhbz#1460206)
- Fix ipv6 subnet detection (rhbz#1438082)

* Tue May 23 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-8
- Update patches

* Mon May 22 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-7
- Add missing sysconfig unit test data (rhbz#1438082)
- Fix dual stack IPv4/IPv6 configuration for RHEL (rhbz#1438082)
- sysconfig: Raise ValueError when multiple default gateways are present. (rhbz#1438082)
- Bounce network interface for Azure when using the built-in path. (rhbz#1434109)
- Do not write NM_CONTROLLED=no in generated interface config files (rhbz#1385172)

* Wed May 10 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-6
- add power-state-change module to cloud_final_modules (rhbz#1252477)
- remove 'tee' command from logging configuration (rhbz#1424612)
- limit permissions on def_log_file (rhbz#1424612)
- Bounce network interface for Azure when using the built-in path. (rhbz#1434109)
- OpenStack: add 'dvs' to the list of physical link types. (rhbz#1442783)

* Wed May 10 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-5
- systemd: replace generator with unit conditionals (rhbz#1440831)

* Thu Apr 13 2017 Charalampos Stratakis <cstratak@redhat.com> 0.7.9-4
- Import to RHEL 7
Resolves: rhbz#1427280

* Tue Mar 07 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-3
- fixes for network config generation
- avoid dependency cycle at boot (rhbz#1420946)

* Tue Jan 17 2017 Lars Kellogg-Stedman <lars@redhat.com> 0.7.9-2
- use timeout from datasource config in openstack get_data (rhbz#1408589)

* Thu Dec 01 2016 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.9-1
- Rebased on upstream 0.7.9.
- Remove dependency on run-parts

* Wed Jan 06 2016 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-8
- make rh_subscription plugin do nothing in the absence of a valid
  configuration [RH:1295953]
- move rh_subscription module to cloud_config stage

* Wed Jan 06 2016 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-7
- correct permissions on /etc/ssh/sshd_config [RH:1296191]

* Thu Sep 03 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-6
- rebuild for ppc64le

* Tue Jul 07 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-5
- bump revision for new build

* Tue Jul 07 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-4
- ensure rh_subscription plugin is enabled by default

* Wed Apr 29 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-3
- added dependency on python-jinja2 [RH:1215913]
- added rhn_subscription plugin [RH:1227393]
- require pyserial to support smartos data source [RH:1226187]

* Fri Jan 16 2015 Lars Kellogg-Stedman <lars@redhat.com> - 0.7.6-2
- Rebased RHEL version to Fedora rawhide
- Backported fix for https://bugs.launchpad.net/cloud-init/+bug/1246485
- Backported fix for https://bugs.launchpad.net/cloud-init/+bug/1411829

* Fri Nov 14 2014 Colin Walters <walters@redhat.com> - 0.7.6-1
- New upstream version [RH:974327]
- Drop python-cheetah dependency (same as above bug)
