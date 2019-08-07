%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Summary: A set of tools to gather troubleshooting information from a system
Name: sos
Version: 3.6
Release: 19%{?dist}.redsleeve
Group: Applications/System
Source0: https://github.com/sosreport/sos/archive/%{version}.tar.gz
License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
Url: http://github.com/sosreport/sos
BuildRequires: python-devel
BuildRequires: gettext
Requires: libxml2-python
Requires: python-six
Requires: bzip2
Requires: xz
Requires: python2-futures
Obsoletes: sos-plugins-openstack
Patch0: skip-generating-doc.patch
Patch1: sos-bz1474976-regexp-sub.patch
Patch2: sos-bz1594327-archive-encryption.patch
Patch3: sos-bz1597532-stat-isblk.patch
Patch4: sos-bz1596494-cds-on-rhui3.patch
Patch5: sos-bz1609135-ceph-dont-collect-tmp-mnt.patch
Patch6: sos-bz1608384-archive-name-sanitize.patch
Patch7: sos-bz1613806-rhosp-lsof-optional.patch
Patch8: sos-bz1600158-rhv-log-collector-analyzer.patch
Patch9: sos-bz1616030-etcd-kube-osp-3-10.patch
Patch10: sos-bz1624043-symlinks-not-copied.patch
Patch11: sos-bz1626159-atomic-attribute-error.patch
Patch12: sos-bz1623070-pipe-returncode.patch
Patch13: sos-bz1636093-openstack-relax-enabling-plugins.patch
Patch14: sos-bz1637632-kernel-dont-collect-tracing-instance.patch
Patch15: sos-bz1656732-ovirt_node-plugin.patch
Patch16: sos-bz1658570-docker-podman-containers.patch
Patch17: sos-bz1658571-postgresql-collect-full-dump.patch
Patch18: sos-bz1669045-rhcos-policy-and-plugins.patch
Patch19: sos-bz1679238-crio-plugin.patch
Patch20: sos-bz1690999-docker-skip-system-df.patch
Patch21: sos-bz1715470-rhv-postgres-from-scl.patch
Patch22: sos-3.6-redsleeve-branding.patch

%description
Sos is a set of tools that gathers information about system
hardware and configuration. The information can then be used for
diagnostic purposes and debugging. Sos is commonly used to help
support technicians and developers.

%prep
%setup -qn %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1

%build
make

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
%find_lang %{name} || echo 0

%clean
rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_sbindir}/sosreport
%{_datadir}/%{name}
%{python_sitelib}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%doc AUTHORS README.md LICENSE 
%config(noreplace) %{_sysconfdir}/sos.conf

%changelog
* Fri Aug 02 2019 Jacco Ligthart <jacco@redsleeve.org> - 3.6-19.el7.redsleeve
- Roll in RedSleeve Branding

* Mon Jul 29 2019 CentOS Sources <bugs@centos.org> - 3.6-19.el7.centos
- Roll in CentOS Branding

* Thu May 30 2019 Pavel Moravec <pmoravec@redhat.com> = 3.6-19
- [postgresql] Use postgres 10 scl if installed
  Resolves: bz1715470

* Wed Mar 20 2019 Pavel Moravec <pmoravec@redhat.com> = 3.6-17
- [docker] do not collect 'system df' by default
  Resolves: bz1690999

* Mon Feb 25 2019 Pavel Moravec <pmoravec@redhat.com> = 3.6-16
- [crio] Add tagging classes
  Resolves: bz1679238

* Wed Feb 20 2019 Pavel Moravec <pmoravec@redhat.com> = 3.6-15
- [crio] Add new plugin
  Resolves: bz1679238

* Thu Jan 24 2019 Pavel Moravec <pmoravec@redhat.com> = 3.6-14
- [rhcos,rpmostree] Add RHCOS policy and 2 plugins
  Resolves: bz1669045

* Wed Dec 12 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-13
- [ovirt_node] New plugin for oVirt Node
  Resolves: bz1656732
- [podman] Add support for gathering information on podman
  Resolves: bz1658570
- [postgresql] Do not limit dump size
  Resolves: bz1658571

* Tue Oct 09 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-11
- [kernel] dont collect some tracing instance files
  Resolves: bz1637632

* Thu Oct 04 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-10
- [openstack_*] relax enabling of OSP RedHat plugins
  Resolves: bz1636093

* Fri Sep 14 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-9
- [archive] recursive symlink fix and simplify directory destination
  Resolves: bz1624043

* Thu Sep 13 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-8
- [plugin,archive] fix remaining add_link issues
  Resolves: bz1624043

* Tue Sep 11 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-7
- [archive] fix copy&paste error in link_path
  Resolves: bz1624043

* Mon Sep 10 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-6
- [archive] fix leading path creation
  Resolves: bz1624043
- [atomic] Define valid preset for RHEL Atomic
  Resolves: bz1626159
- [utilities] wait till AsyncReader p.poll() returns None
  Resolves: bz1623070

* Tue Aug 21 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-5
- [rhv-log-collector-analyzer] Add new plugin for RHV
  Resolves: bz1600158
- [kubernetes|etcd] Support OpenShift 3.10 deployments
  Resolves: bz1616030

* Fri Aug 10 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-4
- [apparmor,ceph] fix typo in add_forbidden_path
  Resolves: bz1609135
- [policies] sanitize report label
  Resolves: bz1608384
- [policies,process] make lsof execution optional, dont call on RHOSP
  Resolves: bz1613806

* Thu Jul 12 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-3
- [sosreport] Add mechanism to encrypt final archive
  Resolves: bz1594327
- [archive] fix stat typo
  Resolves: bz1597532
- [rhui] Fix detection of CDS for RHUI3
  Resolves: bz1596494

* Mon Jul 02 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-2
- [archive] fix add_string()/do_*_sub() regression
  Resolves: bz1474976
- [kernel] handle case when bpftool installed but not implemented
  Resolves: bz1559756

* Fri Jun 22 2018 Pavel Moravec <pmoravec@redhat.com> = 3.6-1
- New upstream release sos-3.6

* Thu May 31 2018 Pavel Moravec <pmoravec@redhat.com> = 3.5-9
- [logs] collect journalctl verbosed logs with --all-logs only
  Resolves: bz1183244

* Mon May 21 2018 Pavel Moravec <pmoravec@redhat.com> = 3.5-8
- [docker] backport three container related patches
  Resolves: bz1573907
- [ovn] add two OpenVSwitch plugins
  Resoles: bz1560845

* Wed Apr 18 2018 Pavel Moravec <pmoravec@redhat.com> = 3.5-7
- [kernel] Disable gathering /proc/timer* statistics
  Resolves: bz1566933
- [openstack_octavia] Add new plugin
  Resolves: bz1541100
- [ovirt-provider-ovn] A new plugin
  Resolves: bz1547544

* Tue Feb 13 2018 Pavel Moravec <pmoravec@redhat.com> = 3.5-6
- [ipa] set ipa_version variable before referencing it
  Resolves: bz1535390

* Tue Feb 13 2018 Pavel Moravec <pmoravec@redhat.com> = 3.5-5
- [rabbitmq] Log collection when run in containerized OSP
  Resolves: bz1525620
- [ipa] add KRA logs and correct PKI directories
  Resolves: bz1535390
- [opendaylight] Enable plugin by puppet-opendaylight package
  Resolves: bz1483414
- [etcd] Do not collect private etcd keys
  Resolves: bz1539038

* Tue Jan 16 2018 Pavel Moravec <pmoravec@redhat.com> = 3.5-4
- [pcp] really apply sizelimit to logs collected
  Resolves: bz1353873
- [opendaylight] collect more logs and puppet config
  Resolves: bz1483414
- [plugins] allow add_cmd_output to collect binary output
  Resolves: bz1494420
- [openstack_ironic] collect drivers, ports and much more
  Resolves: bz1517767
- [openstack_cinder] check for api service running
  Resolves: bz1506908

* Fri Dec 08 2017 Pavel Moravec <pmoravec@redhat.com> = 3.5-2
- [vdo] revise collected files
  Resolves: bz1509079
- further updates to OSP plugins in containerized environment
  Resolves: bz1506908
- [opendaylight] new plugin
  Resolves: bz1483414
- collect all keystone domains
  Resolves: bz1491042
- haproxy, etcd and docker tracebacks
  Resolves: bz1519267
- [origin] fix typo in oc adm diagnostics
  Resolves: bz1463509
- [postgresql] Call SCL pg_dump with proper path
  Resolves: bz1494420

* Thu Nov 02 2017 Pavel Moravec <pmoravec@redhat.com> = 3.5-1
- New upstream release sos-3.5

* Tue Oct 10 2017 Pavel Moravec <pmoravec@redhat.com> = 3.4-7
- [openstack plugins] Tripleo specific containerized services
  Resolves: bz1463635
- [jars] Scan only /usr/{share,lib}/java by default
  Resolves: bz1482574
- [gluster_block] Added new plugin gluster_block
  Resolves: bz1491964

* Wed Jul 12 2017 Pavel Moravec <pmoravec@redhat.com> = 3.4-6
- [tripleo] Add ui logs
  Resolves: bz1470573

* Tue May 30 2017 Pavel Moravec <pmoravec@redhat.com> = 3.4-5
- [samba] Fix dc-connect winbind logfile path
  Resolves: bz1400407

* Mon May 22 2017 Pavel Moravec <pmoravec@redhat.com> = 3.4-4
- [libvirt] fix per-process cgroup collection
  Resolves: bz1148381
- [ceph] exclude temporary mount locations from collection
  Resolves: bz1449904
- [policies/redhat] make missing 'filesystem' package non-fatal
  Resolves: bz1393961

* Wed May 10 2017 Pavel Moravec <pmoravec@redhat.com> = 3.4-3
- [ceph] fix list formatting
  Resolves: bz1438269
- [virsh] Handle properly cases when virsh commands fail
  Resolves: bz1444641
- [openstack_*] fix issue with --verify option, extend pkglist for instack
  Resolves: bz1250346
- [policies/redhat] accept 'oci' as a valid container type
  Resolves: bz1442078
- [pacemaker] Collect user-defined logfile
  Resolves: bz1416535

* Wed Apr 19 2017 Pavel Moravec <pmoravec@redhat.com> = 3.4-2
- [Pugin] revert 77eb4ab (do not return output from failed cmds)
  Resolves: bz1438257

* Tue Mar 28 2017 Pavel Moravec <pmoravec@redhat.com> = 3.4-1
- New upstream release sos-3.4

* Fri Nov 04 2016 Pavel Moravec <pmoravec@redhat.com> = 3.3-5
- [networking] plugin crash with quotemark in network name
  Resolves: bz1353992

* Fri Sep 09 2016 Pavel Moravec <pmoravec@redhat.com> = 3.3-4
- [networking][reporting] plugin tracebacks when net-tools missing
  Resolves: bz1374152

* Fri Sep 02 2016 Pavel Moravec <pmoravec@redhat.com> = 3.3-3
- [nodejs][nms]: new plugins
  Resolves: bz1368393
- [docker]: Gather more data and expand plugin options
  Resolves: bz1351647

* Fri Aug 19 2016 Pavel Moravec <pmoravec@redhat.com> = 3.3-2
- [grub2] grub2-mkconfig loads ext4 and brctl kernel
  Resolves: bz1116670
- [ceph] skip collecting of all keyring and bindpass files
  Resolves: bz1260607
- [omsa] add omreport storage controller
  Resolves: bz1299603
- [atomichost] fix collection of 'docker info' output
  Resolves: bz1302146
- [monit] fix add_copy_spec() arguments
  Resolves: bz1356945
- [virtwho] add new plugin for virt-who agent
  Resolves: bz1353552

* Thu Jun 30 2016 Pavel Moravec <pmoravec@redhat.com> = 3.3-1
- New upstream release sos-3.3

* Wed Jun 29 2016 Pavel Moravec <pmoravec@redhat.com> = 3.3-0
- New upstream release (beta version)

* Thu Jan 14 2016 Pavel Moravec <pmoravec@redhat.com> = 3.2-37
- [sosreport] prepare report in a private subdirectory (updated)
  Resolves: bz1290955

* Mon Dec 14 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-36
- [ceph] collect /var/lib/ceph and /var/run/ceph
  Resolves: bz1260607
- [sosreport] prepare report in a private subdirectory
  Resolves: bz1290955

* Wed Oct 07 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-35
- [docker] collect journald logs for docker unit
  Resolves: bz1245770

* Tue Oct 06 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-34
- [sosreport] fix command-line report defaults
  Resolves: bz1219720

* Thu Sep 10 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-33
- [openstack_neutron] obfuscate server_auth in restproxy.ini
  Resolves: bz1243092

* Fri Aug 28 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-32
- [memory] collect swapon --show output in bytes
  Resolves: bz1194159

* Mon Aug 24 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-31
- [sosreport] fix command-line report defaults (proper patch ordering)
  Resolves: bz1219720
 
* Tue Aug 04 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-30
- [sapnw] call self methods properly
  Resolves: bz1195608

* Tue Aug 04 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-29
- [openvswitch] capture the logs, db and OVS bridges details
  Resolves: bz1242507
- [logs] fix reference to missing 'rsyslog_conf' variable
  Resolves: bz1249705
- [sapnw] Add check if saphostctrl is not present, dont use Set
  Resolves: bz1195608
- [Plugin] fix handling of symlinks in non-sysroot environments
  Resolves: bz1248672

* Sat Jul 18 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-28
- [openstack] Ensure openstack passwords and secrets are obfuscated
  Resolves: bz1243092

* Wed Jul 15 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-27
- [plugin] pass stderr through _collect_cmd_output
- split dependencies of bz1185990 fix from bz1185990 patch
  Resolves: bz1185990

* Thu Jul 09 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-26
- [kubernetes,plugin] Support running sos inside a container
  Resolves: bz1185990

* Tue Jul 07 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-25
- [openstack] New Openstack Trove (DBaaS) plugin
  Resolves: bz1238349
- [services] Add more diagnostics to applications
  Resolves: bz1195087
- [openstack_neutron] Obscure passwords and secrets
  Resolves: bz1240666

* Sat Jul 04 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-23
- [ceph] add calamari and ragos logs and configs
  Resolves: bz1210527
- [iprconfig] enable plugin for ppc64* architectures
  Resolves: bz1238726

* Fri Jul 03 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-22
- [general] verify --profile contains valid plugins only
  Resolves: bz1184602
- [kernel,mpt,memory] additional kernel-related diagnostics
  Resolves: bz1194159

* Wed Jul 01 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-21
- [cluster] enable crm_report password scrubbing
  Resolves: bz1164864
- [sosreport] fix command-line report defaults
  Resolves: bz1219720
- [virsh] add new plugin, add listing of qemu
  Resolves: bz1195086
- [sap*,vhostmd] new plugins for SAP
  Resolves: bz1195608

* Tue Jun 30 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-20
- [cluster] crm_report fails to run because dir already exists
  Resolves: bz1200526
- [foreman] Skip collection of generic resources
  Resolves: bz1135317
- [apache] Added collection of conf.modules.d dir for httpd 2.4
  Resolves: bz1183265
- [pcp] collect /etc/pcp.conf
  Resolves: bz1183297
- [puppet] adding new plugin for puppet
  Resolves: bz1183768
- [block] Don't use parted human readable output
  Resolves: bz1183770
- [general] Better handling --name and --ticket-number in
  Resolves: bz1185093
- [networking] additional ip, firewall and traffic shaping
  Resolves: bz1194554
- [infiniband] add opensm and infiniband-diags support
  Resolves: bz1194556
- [plugins/rabbitmq] Added cluster_status command output
  Resolves: bz1197006
- [networking] re-add 'ip addr' with a root symlink
  Resolves: bz1209454
- [kimchi] add new plugin
  Resolves: bz1209840
- [iprconfig] add plugin for IBM Power RAID adapters
  Resolves: bz1221932
- [ovirt] Collect engine tunables and domain information.
  Resolves: bz1236101
- [activemq] Honour all_logs and get config on RHEL
  Resolves: bz1236111
- [cluster] Add luci to packages for standalone luci servers
  Resolves: bz1236124
- [hpasm] hpasmcli commands hang under timeout
  Resolves: bz1214209
- [mysql] Collect log file
  Resolves: bz1210906
- [chrony] add chrony plugin
  Resolves: bz1165418

* Mon Jun 15 2015 Shane Bradley <sbradley@redhat.com> = 3.2-19
- [openstack_sahara] redact secrets from sahara configuration
  Resolves: bz1211984

* Tue Jun 09 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-18
- [openstack_sahara] add new openstack_sahara plugin
  Resolves: bz1211984

* Tue Apr 21 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-17
- [openstack_neutron] neutron configuration and logs files not captured
  Resolves: bz1213315
- [ovirt] remove ovirt-engine setup answer file password leak
  Resolves: bz1162788
- [networking] network plugin fails if NetworkManager is disabled
  Resolves: bz1206633

* Fri Mar 13 2015 Pavel Moravec <pmoravec@redhat.com> = 3.2-16
- [cluster] crm_report fails to run because dir already exists
  Resolves: bz1200526

* Thu Jan 22 2015 Bryn M. Reeves <bmr@redhat.com> = 3.2-15
- [mysql] improve handling of dbuser, dbpass and MYSQL_PWD
  Resolves: bz1180919

* Tue Jan 20 2015 Bryn M. Reeves <bmr@redhat.com> = 3.2-14
- [mysql] test for boolean values in dbuser and dbpass
  Resolves: bz1180919

* Mon Jan 19 2015 Bryn M. Reeves <bmr@redhat.com> = 3.2-12
- [plugin] limit path names to PC_NAME_MAX
  Resolves: bz1026962
- [squid] collect files from /var/log/squid
  Resolves: bz1026962
- [sosreport] log plugin exceptions to a file
  Resolves: bz1026962
- [ctdb] fix collection of /etc/sysconfig/ctdb
  Resolves: bz1026962
- [sosreport] fix silent exception handling
  Resolves: bz1026962

* Tue Jan 13 2015 Bryn M. Reeves <bmr@redhat.com> = 3.2-11
- [sosreport] do not make logging calls after OSError
  Resolves: bz1087977
- [sosreport] catch OSError exceptions in SoSReport.execute()
  Resolves: bz1087977
- [anaconda] make useradd password regex tolerant of whitespace
  Resolves: bz1112175

* Tue Dec 23 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-10
- [mysql] fix handling of mysql.dbpass option
  Resolves: bz1126001

* Wed Dec 17 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-9
- [navicli] catch exceptions if stdin is unreadable
  Resolves: bz1166039
- [docs] update man page for new options
  Resolves: bz1171658
- [sosreport] make all utf-8 handling user errors=ignore
  Resolves: bz1164267

* Tue Dec 09 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-8
- [kpatch] do not attempt to collect data if kpatch is not installed
  Resolves: bz1110918
- [archive] drop support for Zip archives
  Resolves: bz1118152

* Thu Oct 30 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-7
- [sosreport] fix archive permissions regression
  Resolves: bz1158891

* Mon Oct 20 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-6
- [tomcat] add support for tomcat7 and default log size limits
  Resolves: bz1148375
- [mysql] obtain database password from the environment
  Resolves: bz1126001

* Wed Oct 15 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-5
- [corosync] add postprocessing for corosync-objctl output
  Resolves: bz1087515
- [ovirt_hosted_engine] fix exception when force-enabled
  Resolves: bz1148551

* Thu Oct 02 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-4
- [yum] call rhsm-debug with --no-subscriptions
  Resolves: bz1116349
- [powerpc] allow PowerPC plugin to run on ppc64le
  Resolves: bz1140427
- [package] add Obsoletes for sos-plugins-openstack
  Resolves: bz1140756

* Wed Oct 01 2014 Bryn M. Reeves <bmr@redhat.com> = 3.2-3
- [pam] add pam_tally2 and faillock support
  Resolves: bz1127631
- [postgresql] obtain db password from the environment
  Resolves: bz1126001
- [pcp] add Performance Co-Pilot plugin
  Resolves: bz1119833
- [nfsserver] collect /etc/exports.d
  Resolves: bz1118921
- [sosreport] handle --compression-type correctly
  Resolves: bz1118152
- [anaconda] redact passwords in kickstart configurations
  Resolves: bz1112175
- [haproxy] add new plugin
  Resolves: bz1107865
- [keepalived] add new plugin
  Resolves: bz1105247
- [lvm2] set locking_type=0 when calling lvm commands
  Resolves: bz1102285
- [tuned] add new plugin
  Resolves: bz1095447
- [cgroups] collect /etc/sysconfig/cgred
  Resolves: bz1083677
- [plugins] ensure doc text is always displayed for plugins
  Resolves: bz1065473
- [sosreport] fix the distribution version API call
  Resolves: bz1028111
- [docker] add new plugin
  Resolves: bz1084990
- [openstack_*] include broken-out openstack plugins
  Resolves: bz1140756
- [mysql] support MariaDB
  Resolves: bz1106600
- [openstack] do not collect /var/lib/nova
  Resolves: bz1106423
- [grub2] collect grub.cfg on UEFI systems
  Resolves: bz1086648
- [sosreport] handle out-of-space errors gracefully
  Resolves: bz1087977
- [firewalld] new plugin
  Resolves: bz1100505
- [networking] collect NetworkManager status
  Resolves: bz1100505
- [kpatch] new plugin
  Resolves: bz1110918
- [global] update to upstream 3.2 release
  Resolves: bz1026962

* Mon Sep 08 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-24
- [foreman] add new plugin
  Resolves: bz1130273

* Thu Mar 20 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-23
- Call rhsm-debug with the --sos switch
  Resolves: bz1039036

* Mon Mar 03 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-22
- Fix package check in anacron plugin
  Resolves: bz1067769

* Wed Feb 12 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-21
- Remove obsolete rhel_version() usage from yum plugin
  Resolves: bz916705

* Tue Feb 11 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-20
- Prevent unhandled exception during command output substitution
  Resolves: bz1030553

* Mon Feb 10 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-19
- Fix generation of volume names in gluster plugin
  Resolves: bz1036752
- Add distupgrade plugin
  Resolves: bz1059760

* Tue Feb 04 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-18
- Prevent file descriptor leaks when using Popen
  Resolves: bz1051009
- Disable zip archive creation when running rhsm-debug
  Resolves: bz1039036
- Include volume geo-replication status in gluster plugin
  Resolves: bz1036752

* Mon Feb 03 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-17
- Fix get_option use in cluster plugin
  Resolves: bz1030553
- Fix debug logging to file when given '-v'
  Resolves: bz1031126
- Always treat rhevm plugin's vdsmlogs option as a string
  Resolves: bz1030617
- Run the rhsm-debug script from yum plugin
  Resolves: bz1039036

* Fri Jan 31 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-16
- Add new plugin to collect OpenHPI configuration
  Resolves: bz1028121
- Fix cluster plugin crm_report support
  Resolves: bz1030553
- Fix file postprocessing in ldap plugin
  Resolves: bz1030602
- Remove collection of anaconda-ks.cfg from general plugin
  Resolves: bz1034865

* Fri Jan 24 2014 Bryn M. Reeves <bmr@redhat.com> = 3.0-15
- Remove debug statements from logs plugin
  Resolves: bz1030042
- Make ethernet interface detection more robust
  Resolves: bz1030824
- Fix specifying multiple plugin options on the command line
  Resolves: bz1031124
- Make log and message levels match previous versions
  Resolves: bz1031126
- Log a warning message when external commands time out
  Resolves: bz1034956
- Remove --upload command line option
  Resolves: bz1028484
- Update sos UI text to match upstream
  Resolves: bz1034970

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> = 3.0-14
- Mass rebuild 2013-12-27

* Thu Nov 14 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-13
- Fix regressions introduced with --build option
  Resolves: bz1015599

* Tue Nov 12 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-12
- Fix typo in yum plug-in add_forbidden_paths
  Resolves: bz829297
- Add krb5 plug-in and drop collection of krb5.keytab
  Resolves: bz1028150

* Fri Nov  8 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-10
- Add nfs client plug-in
  Resolves: bz1028072
- Fix traceback when sar module force-enabled
  Resolves: bz1028125

* Thu Nov  7 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-9
- Restore --build command line option
  Resolves: bz1015599
- Collect saved vmcore-dmesg.txt files
  Resolves: bz1026959
- Normalize temporary directory paths
  Resolves: bz829069

* Tue Nov  5 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-7
- Add domainname output to NIS plug-in
  Resolves: bz1026906
- Collect /var/log/squid in squid plug-in
  Resolves: bz1026829
- Collect mountstats and mountinfo in filesys plug-in
  Resolves: bz1026869
- Add PowerPC plug-in from upstream
  Resolves: bz1025236

* Thu Oct 31 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-6
- Remove version checks in gluster plug-in
  Resolves: bz1015606
- Check for usable temporary directory
  Resolves: bz1019517
- Fix --alloptions command line option
  Resolves: bz1019356
- Fix configuration fail regression
  Resolves: bz1019516

* Wed Oct 30 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-5
- Include /etc/yaboot.conf in boot plug-in
  Resolves: bz1001966
- Fix collection of brctl output in networking plug-in
  Resolves: bz1019235
- Verify limited set of RPM packages by default
  Resolves: bz1019863
- Do not strip newlines from command output
  Resolves: bz1019338
- Limit default sar data collection
  Resolves: bz1001599

* Thu Oct 3 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-4
- Do not attempt to read RPC pseudo files in networking plug-in
  Resolves: bz996992, bz996994
- Restrict wbinfo collection to the current domain
  Resolves: bz997101
- Add obfuscation of luci secrets to cluster plug-in
  Resolves: bz997090
- Add XFS plug-in
  Resolves: bz997094
- Fix policy class handling of --tmp-dir
  Resolves: bz997083
- Do not set batch mode if stdin is not a TTY
  Resolves: bz1002943
- Attempt to continue when reading bad input in interactive mode
  Resolves: bz1002943

* Wed Aug 14 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-3
- Add crm_report support to cluster plug-in
  Resolves: bz839342
- Fix rhel_version() usage in cluster and s390 plug-ins
  Resolves: bz916705
- Strip trailing newline from command output
  Resolves: bz971420

* Mon Jun 10 2013 Bryn M. Reeves <bmr@redhat.com> = 3.0-2
- Silence 'could not run' messages at default verbosity
- New upstream release

* Thu May 23 2013 Bryn M. Reeves <bmr@redhat.com> = 2.2-39
- Always invoke tar with '-f-' option

* Mon Jan 21 2013 Bryn M. Reeves <bmr@redhat.com> = 2.2-38
- Fix interactive mode regression when --ticket unspecified

* Fri Jan 18 2013 Bryn M. Reeves <bmr@redhat.com> = 2.2-37
- Fix propagation of --ticket parameter in interactive mode

* Thu Jan 17 2013 Bryn M. Reeves <bmr@redhat.com> = 2.2-36
- Revert OpenStack patch

* Wed Jan  9 2013 Bryn M. Reeves <bmr@redhat.com> = 2.2-35
- Report --name and --ticket values as defaults
- Fix device-mapper command execution logging
- Fix data collection and rename PostreSQL module to pgsql

* Fri Oct 19 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-34
- Add support for content delivery hosts to RHUI module

* Thu Oct 18 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-33
- Add Red Hat Update Infrastructure module
- Collect /proc/iomem in hardware module
- Collect subscription-manager output in general module
- Collect rhsm log files in general module
- Fix exception in gluster module on non-gluster systems
- Fix exception in psql module when dbname is not given

* Wed Oct 17 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-32
- Collect /proc/pagetypeinfo in memory module
- Strip trailing newline from command output
- Add sanlock module
- Do not collect archived accounting files in psacct module
- Call spacewalk-debug from rhn module to collect satellite data

* Mon Oct 15 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-31
- Avoid calling volume status when collecting gluster statedumps
- Use a default report name if --name is empty
- Quote tilde characters passed to shell in RPM module
- Collect KDC and named configuration in ipa module
- Sanitize hostname characters before using as report path
- Collect /etc/multipath in device-mapper module
- New plug-in for PostgreSQL
- Add OpenStack module
- Avoid deprecated sysctls in /proc/sys/net
- Fix error logging when calling external programs
- Use ip instead of ifconfig to generate network interface lists

* Wed May 23 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-29
- Collect the swift configuration directory in gluster module
- Update IPA module and related plug-ins

* Fri May 18 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-28
- Collect mcelog files in the hardware module

* Wed May 02 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-27
- Add nfs statedump collection to gluster module

* Tue May 01 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-26
- Use wildcard to match possible libvirt log paths

* Mon Apr 23 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-25
- Add forbidden paths for new location of gluster private keys

* Fri Mar  9 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-24
- Fix katello and aeolus command string syntax
- Remove stray hunk from gluster module patch

* Thu Mar  8 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-22
- Correct aeolus debug invocation in CloudForms module
- Update gluster module for gluster-3.3
- Add additional command output to gluster module
- Add support for collecting gluster configuration and logs

* Wed Mar  7 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-19
- Collect additional diagnostic information for realtime systems
- Improve sanitization of RHN user and case number in report name
- Fix verbose output and debug logging
- Add basic support for CloudForms data collection
- Add support for Subscription Asset Manager diagnostics

* Tue Mar  6 2012 Bryn M. Reeves <bmr@redhat.com> = 2.2-18
- Collect fence_virt.conf in cluster module
- Fix collection of /proc/net directory tree
- Gather output of cpufreq-info when present
- Fix brctl showstp output when bridges contain multiple interfaces
- Add /etc/modprobe.d to kernel module
- Ensure relative symlink targets are correctly handled when copying
- Fix satellite and proxy package detection in rhn plugin
- Collect stderr output from external commands
- Collect /proc/cgroups in the cgroups module
  Resolve: bz784874
- Collect /proc/irq in the kernel module
- Fix installed-rpms formatting for long package names
- Add symbolic links for truncated log files
- Collect non-standard syslog and rsyslog log files
- Use correct paths for tomcat6 in RHN module
- Obscure root password if present in anacond-ks.cfg
- Do not accept embedded forward slashes in RHN usernames
- Add new sunrpc module to collect rpcinfo for gluster systems

* Tue Nov  1 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-17
- Do not collect subscription manager keys in general plugin
 
* Fri Sep 23 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-16
- Fix execution of RHN hardware.py from hardware plugin
- Fix hardware plugin to support new lsusb path

* Fri Sep 09 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-15
- Fix brctl collection when a bridge contains no interfaces
- Fix up2dateclient path in hardware plugin

* Mon Aug 15 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-14
- Collect brctl show and showstp output
- Collect nslcd.conf in ldap plugin

* Sun Aug 14 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-11
- Truncate files that exceed specified size limit
- Add support for collecting Red Hat Subscrition Manager configuration
- Collect /etc/init on systems using upstart
- Don't strip whitespace from output of external programs
- Collect ipv6 neighbour table in network module
- Collect basic cgroups configuration data

* Sat Aug 13 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-10
- Fix collection of data from LVM2 reporting tools in devicemapper plugin
- Add /proc/vmmemctl collection to vmware plugin

* Fri Aug 12 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-9
- Collect yum repository list by default
- Add basic Infiniband plugin
- Add plugin for scsi-target-utils iSCSI target
- Fix autofs plugin LC_ALL usage
- Fix collection of lsusb and add collection of -t and -v outputs
- Extend data collection by qpidd plugin
- Add ethtool pause, coalesce and ring (-a, -c, -g) options to network plugin

* Thu Apr 07 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-8
- Use sha256 for report digest when operating in FIPS mode
 
* Tue Apr 05 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-7
- Fix parted and dumpe2fs output on s390

* Fri Feb 25 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-6
- Fix collection of chkconfig output in startup.py
- Collect /etc/dhcp in dhcp.py plugin
- Collect dmsetup ls --tree output in devicemapper.py
- Collect lsblk output in filesys.py

* Thu Feb 24 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-4
- Fix collection of logs and config files in sssd.py
- Add support for collecting entitlement certificates in rhn.py

* Thu Feb 03 2011 Bryn M. Reeves <bmr@redhat.com> = 2.2-3
- Fix cluster plugin dlm lockdump for el6
- Add sssd plugin to collect configuration and logs
- Collect /etc/anacrontab in system plugin
- Correct handling of redhat-release for el6

* Thu Jul 29 2010 Adam Stokes <ajs at redhat dot com> = 2.2-2

* Thu Jun 10 2010 Adam Stokes <ajs at redhat dot com> = 2.2-0

* Wed Apr 28 2010 Adam Stokes <ajs at redhat dot com> = 2.1-0

* Mon Apr 12 2010 Adam Stokes <ajs at redhat dot com> = 2.0-0

* Tue Mar 30 2010 Adam Stokes <ajs at redhat dot com> = 1.9-3
- fix setup.py to autocompile translations and man pages
- rebase 1.9

* Fri Mar 19 2010 Adam Stokes <ajs at redhat dot com> = 1.9-2
- updated translations

* Thu Mar 04 2010 Adam Stokes <ajs at redhat dot com> = 1.9-1
- version bump 1.9
- replaced compression utility with xz
- strip threading/multiprocessing
- simplified progress indicator
- pylint update
- put global vars in class container
- unittests
- simple profiling
- make use of xgettext as pygettext is deprecated

* Mon Jan 18 2010 Adam Stokes <ajs at redhat dot com> = 1.8-21
- more sanitizing options for log files
- rhbz fixes from RHEL version merged into trunk
- progressbar update

