Name: rdma-core
Version: 22.4
Release: 5%{?dist}
Summary: RDMA core userspace libraries and daemons

%ifnarch %{arm}
%define dma_coherent 1
%endif
# Almost everything is licensed under the OFA dual GPLv2, 2 Clause BSD license
#  providers/ipathverbs/ Dual licensed using a BSD license with an extra patent clause
#  providers/rxe/ Incorporates code from ipathverbs and contains the patent clause
#  providers/hfi1verbs Uses the 3 Clause BSD license
License: GPLv2 or BSD
Url: https://github.com/linux-rdma/rdma-core
Source: https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Red Hat patches
Patch1: 0001-redhat-kernel-init-ocrdma-is-tech-preview-too.patch
Patch2: 0002-redhat-kernel-init-libi40iw-no-longer-tech-preview.patch
Patch3: 0003-rdma-hw-modules.rules-i40iw-autoload-breaks-suspend.patch
Patch4: 0004-Revert-redhat-remove-files-that-we-no-longer-use.patch
Patch5: 0005-fix_mtu_limiting_for_ipoib.patch
Patch6: 0006-srp_daemon-Remove-unsupported-systemd-configurations.patch
Patch7: 0007-srp_daemon-srp_daemon.service-should-be-started-afte.patch
Patch8: rdma-core-unclamp-ipoib-mtu.patch
# Additional upstream patches from branch v23
Patch11: 0101-Update-kernel-headers.patch
Patch12: 0102-bnxt_re-lib-Enable-Broadcom-s-57500-RoCE-adapter.patch
Patch13: 0103-mlx5-Add-new-device-IDs.patch
# Additional upstream patches from stable-vX/master branch
Patch101: 0001-srp_daemon-fix-a-double-free-segment-fault-for-ibsrp.patch
Patch102: 0002-cxgb4-free-appropriate-pointer-in-error-case.patch
Patch103: 0003-man-Fix-return-value-for-ibv_reg_dm_mr.patch
# Patches backported from master branch
Patch104: 0004-Update-kernel-headers.patch
Patch105: 0005-mlx5-Support-scatter-to-CQE-over-DCT-QP.patch
Patch106: 0001-ibacm-Do-not-open-non-InfiniBand-device.patch
# Patches backported from stable-v27
Patch107: 0001-bnxt_re-lib-Add-remaining-pci-ids-for-gen-P5-devices.patch
Patch108: 0002-bnxt_re-lib-Recognize-additional-5750x-device-ID-s.patch

Patch109: 0001-libibverbs-Fix-ABI_placeholder1-and-ABI_placeholder2.patch
# Do not build static libs by default.
%define with_static %{?_with_static: 1} %{?!_with_static: 0}

BuildRequires: binutils
BuildRequires: cmake >= 2.8.11
BuildRequires: gcc
BuildRequires: libudev-devel
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
%ifnarch s390
BuildRequires: valgrind-devel
%endif
BuildRequires: systemd
BuildRequires: python
BuildRequires: sed

Requires: dracut, kmod, initscripts, systemd
%if 0%{?fedora} >= 24
Requires: systemd-udev
%endif
# Red Hat/Fedora previously shipped redhat/ as a stand-alone
# package called 'rdma', which we're supplanting here.
Provides: rdma = %{version}-%{release}
Obsoletes: rdma < %{version}-%{release}
Provides: rdma-ndd = %{version}-%{release}
Obsoletes: rdma-ndd < %{version}-%{release}
# libibcm was deprecated and removed
Provides: libibcm = %{version}-%{release}
Obsoletes: libibcm < %{version}-%{release}
# the ndd utility moved from infiniband-diags to rdma-core
Conflicts: infiniband-diags <= 1.6.5
Requires: pciutils

# Since we recommend developers use Ninja, so should packagers, for consistency.
%define CMAKE_FLAGS %{nil}
%if 0%{?fedora} >= 23
# Ninja was introduced in FC23
BuildRequires: ninja-build
%define CMAKE_FLAGS -GNinja
%define make_jobs ninja-build -v %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} ninja-build install
%else
# Fallback to make otherwise
BuildRequires: make
%define make_jobs make -v %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} make install
%endif

%description
RDMA core userspace infrastructure and documentation, including initscripts,
kernel driver-specific modprobe override configs, IPoIB network scripts,
dracut rules, and the rdma-ndd utility.

%package devel
Summary: RDMA core development libraries and headers
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libibverbs = %{version}-%{release}
Provides: libibverbs-devel = %{version}-%{release}
Obsoletes: libibverbs-devel < %{version}-%{release}
Provides: libibverbs-devel-static = %{version}-%{release}
Obsoletes: libibverbs-devel-static < %{version}-%{release}
Requires: libibumad = %{version}-%{release}
Provides: libibumad-devel = %{version}-%{release}
Obsoletes: libibumad-devel < %{version}-%{release}
Provides: libibumad-static = %{version}-%{release}
Obsoletes: libibumad-static < %{version}-%{release}
Requires: librdmacm = %{version}-%{release}
Provides: librdmacm-devel = %{version}-%{release}
Obsoletes: librdmacm-devel < %{version}-%{release}
Provides: librdmacm-static = %{version}-%{release}
Obsoletes: librdmacm-static < %{version}-%{release}
Requires: ibacm = %{version}-%{release}
Provides: ibacm-devel = %{version}-%{release}
Obsoletes: ibacm-devel < %{version}-%{release}
Provides: libcxgb3-static = %{version}-%{release}
Obsoletes: libcxgb3-static < %{version}-%{release}
Provides: libcxgb4-static = %{version}-%{release}
Obsoletes: libcxgb4-static < %{version}-%{release}
Provides: libhfi1-static = %{version}-%{release}
Obsoletes: libhfi1-static < %{version}-%{release}
Provides: libipathverbs-static = %{version}-%{release}
Obsoletes: libipathverbs-static < %{version}-%{release}
%if 0%{?dma_coherent}
Provides: libmlx4-static = %{version}-%{release}
Obsoletes: libmlx4-static < %{version}-%{release}
Provides: libmlx5-static = %{version}-%{release}
Obsoletes: libmlx5-static < %{version}-%{release}
%endif
Provides: libnes-static = %{version}-%{release}
Obsoletes: libnes-static < %{version}-%{release}
Provides: libocrdma-static = %{version}-%{release}
Obsoletes: libocrdma-static < %{version}-%{release}
Provides: libi40iw-devel-static = %{version}-%{release}
Obsoletes: libi40iw-devel-static < %{version}-%{release}
Provides: libmthca-static = %{version}-%{release}
Obsoletes: libmthca-static < %{version}-%{release}
Provides: libehca-devel = %{version}-%{release}
Obsoletes: libehca-devel < %{version}-%{release}
Provides: libehca-static = %{version}-%{release}
Obsoletes: libehca-static < %{version}-%{release}

%description devel
RDMA core development libraries and headers.

%package -n libibverbs
Summary: A library and drivers for direct userspace use of RDMA (InfiniBand/iWARP/RoCE) hardware
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: libcxgb3 = %{version}-%{release}
Obsoletes: libcxgb3 < %{version}-%{release}
Provides: libcxgb4 = %{version}-%{release}
Obsoletes: libcxgb4 < %{version}-%{release}
Provides: libhfi1 = %{version}-%{release}
Obsoletes: libhfi1 < %{version}-%{release}
Provides: libi40iw = %{version}-%{release}
Obsoletes: libi40iw < %{version}-%{release}
Provides: libipathverbs = %{version}-%{release}
Obsoletes: libipathverbs < %{version}-%{release}
%if 0%{?dma_coherent}
Provides: libmlx4 = %{version}-%{release}
Obsoletes: libmlx4 < %{version}-%{release}
%ifnarch s390
Provides: libmlx5 = %{version}-%{release}
Obsoletes: libmlx5 < %{version}-%{release}
%endif
%endif
Provides: libmthca = %{version}-%{release}
Obsoletes: libmthca < %{version}-%{release}
Provides: libnes = %{version}-%{release}
Obsoletes: libnes < %{version}-%{release}
Provides: libocrdma = %{version}-%{release}
Obsoletes: libocrdma < %{version}-%{release}
Provides: librxe = %{version}-%{release}
Obsoletes: librxe < %{version}-%{release}
Provides: libusnic_verbs = %{version}-%{release}
Obsoletes: libusnic_verbs < %{version}-%{release}
Provides: libehca = %{version}-%{release}
Obsoletes: libehca < %{version}-%{release}

%description -n libibverbs
libibverbs is a library that allows userspace processes to use RDMA
"verbs" as described in the InfiniBand Architecture Specification and
the RDMA Protocol Verbs Specification.  This includes direct hardware
access from userspace to InfiniBand/iWARP adapters (kernel bypass) for
fast path operations.

Device-specific plug-in ibverbs userspace drivers are included:

- libbxnt_re: Broadcom NetXtreme-E RoCE HCA
- libcxgb3: Chelsio T3 iWARP HCA
- libcxgb4: Chelsio T4 iWARP HCA
- libhfi1: Intel Omni-Path HFI
- libhns: HiSilicon Hip06 SoC
- libi40iw: Intel Ethernet Connection X722 RDMA
- libipathverbs: QLogic InfiniPath HCA
- libmlx4: Mellanox ConnectX-3 InfiniBand HCA
- libmlx5: Mellanox Connect-IB/X-4+ InfiniBand HCA
- libmthca: Mellanox InfiniBand HCA
- libnes: NetEffect RNIC
- libocrdma: Emulex OneConnect RDMA/RoCE Device
- libqedr: QLogic QL4xxx RoCE HCA
- librxe: A software implementation of the RoCE protocol
- libvmw_pvrdma: VMware paravirtual RDMA device

%package -n libibverbs-utils
Summary: Examples for the libibverbs library
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n libibverbs-utils
Useful libibverbs example programs such as ibv_devinfo, which
displays information about RDMA devices.

%package -n ibacm
Summary: InfiniBand Communication Manager Assistant
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libibumad%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n ibacm
The ibacm daemon helps reduce the load of managing path record lookups on
large InfiniBand fabrics by providing a user space implementation of what
is functionally similar to an ARP cache.  The use of ibacm, when properly
configured, can reduce the SA packet load of a large IB cluster from O(n^2)
to O(n).  The ibacm daemon is started and normally runs in the background,
user applications need not know about this daemon as long as their app
uses librdmacm to handle connection bring up/tear down.  The librdmacm
library knows how to talk directly to the ibacm daemon to retrieve data.

%package -n iwpmd
Summary: iWarp Port Mapper userspace daemon
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n iwpmd
iwpmd provides a userspace service for iWarp drivers to claim
tcp ports through the standard socket interface.

%package -n libibumad
Summary: OpenFabrics Alliance InfiniBand umad (userspace management datagram) library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n libibumad
libibumad provides the userspace management datagram (umad) library
functions, which sit on top of the umad modules in the kernel. These
are used by the IB diagnostic and management tools, including OpenSM.

%package -n librdmacm
Summary: Userspace RDMA Connection Manager
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n librdmacm
librdmacm provides a userspace RDMA Communication Managment API.

%package -n librdmacm-utils
Summary: Examples for the librdmacm library
Requires: librdmacm%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n librdmacm-utils
Example test programs for the librdmacm library.

%package -n srp_daemon
Summary: Tools for using the InfiniBand SRP protocol devices
Obsoletes: srptools <= 1.0.3
Provides: srptools = %{version}-%{release}
Obsoletes: openib-srptools <= 0.0.6
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libibumad%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n srp_daemon
In conjunction with the kernel ib_srp driver, srp_daemon allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%prep
%setup
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1

%build

# New RPM defines _rundir, usually as /run
%if 0%{?_rundir:1}
%else
%define _rundir /var/run
%endif

%{!?EXTRA_CMAKE_FLAGS: %define EXTRA_CMAKE_FLAGS %{nil}}

# Pass all of the rpm paths directly to GNUInstallDirs and our other defines.
%cmake %{CMAKE_FLAGS} \
         -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
         -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
         -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
         -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
         -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
         -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
         -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
         -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
         -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
         -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
         -DCMAKE_INSTALL_SYSTEMD_SERVICEDIR:PATH=%{_unitdir} \
         -DCMAKE_INSTALL_INITDDIR:PATH=%{_initrddir} \
         -DCMAKE_INSTALL_RUNDIR:PATH=%{_rundir} \
         -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name}-%{version} \
         -DCMAKE_INSTALL_UDEV_RULESDIR:PATH=%{_udevrulesdir} \
%if %{with_static}
         -DENABLE_STATIC=1 \
%endif
         %{EXTRA_CMAKE_FLAGS}
%make_jobs

%install
%cmake_install

mkdir -p %{buildroot}/%{_sysconfdir}/rdma

# Red Hat specific glue
%global dracutlibdir %{_prefix}/lib/dracut
%global sysmodprobedir %{_prefix}/lib/modprobe.d
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/05rdma
mkdir -p %{buildroot}%{sysmodprobedir}
install -D -m0644 redhat/rdma.conf %{buildroot}/%{_sysconfdir}/rdma/rdma.conf
install -D -m0644 redhat/rdma.sriov-vfs %{buildroot}/%{_sysconfdir}/rdma/sriov-vfs
%if 0%{?dma_coherent}
install -D -m0644 redhat/rdma.mlx4.conf %{buildroot}/%{_sysconfdir}/rdma/mlx4.conf
%endif
install -D -m0755 redhat/rdma.ifup-ib %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts/ifup-ib
install -D -m0755 redhat/rdma.ifdown-ib %{buildroot}/%{_sysconfdir}/sysconfig/network-scripts/ifdown-ib
install -D -m0644 redhat/rdma.service %{buildroot}%{_unitdir}/rdma.service
install -D -m0755 redhat/rdma.modules-setup.sh %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh
install -D -m0644 redhat/rdma.udev-rules %{buildroot}%{_udevrulesdir}/98-rdma.rules
%if 0%{?dma_coherent}
install -D -m0644 redhat/rdma.mlx4.sys.modprobe %{buildroot}%{sysmodprobedir}/libmlx4.conf
%endif
install -D -m0755 redhat/rdma.kernel-init %{buildroot}%{_libexecdir}/rdma-init-kernel
install -D -m0755 redhat/rdma.sriov-init %{buildroot}%{_libexecdir}/rdma-set-sriov-vf
%if 0%{?dma_coherent}
install -D -m0755 redhat/rdma.mlx4-setup.sh %{buildroot}%{_libexecdir}/mlx4-setup.sh
%endif

# ibacm
bin/ib_acme -D . -O
# multi-lib conflict resolution hacks (bug 1429362)
sed -i -e 's|%{_libdir}|/usr/lib|' %{buildroot}%{_mandir}/man7/ibacm_prov.7
sed -i -e 's|%{_libdir}|/usr/lib|' ibacm_opts.cfg
install -D -m0644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/

# Delete the package's init.d scripts
rm -rf %{buildroot}/%{_initrddir}/

%post -n libibverbs -p /sbin/ldconfig
%postun -n libibverbs -p /sbin/ldconfig

%post -n libibumad -p /sbin/ldconfig
%postun -n libibumad -p /sbin/ldconfig

%post -n librdmacm -p /sbin/ldconfig
%postun -n librdmacm -p /sbin/ldconfig

%post -n ibacm
%systemd_post ibacm.service
%preun -n ibacm
%systemd_preun ibacm.service
%postun -n ibacm
%systemd_postun_with_restart ibacm.service

%post -n srp_daemon
%systemd_post srp_daemon.service
%preun -n srp_daemon
%systemd_preun srp_daemon.service
%postun -n srp_daemon
%systemd_postun_with_restart srp_daemon.service

%post -n iwpmd
%systemd_post iwpmd.service
%preun -n iwpmd
%systemd_preun iwpmd.service
%postun -n iwpmd
%systemd_postun_with_restart iwpmd.service

%files
%dir %{_sysconfdir}/rdma
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README.md
%doc %{_docdir}/%{name}-%{version}/udev.md
%config(noreplace) %{_sysconfdir}/rdma/*
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%if 0%{?dma_coherent}
%ifnarch s390
%config(noreplace) %{_sysconfdir}/modprobe.d/mlx4.conf
%endif
%endif
%config(noreplace) %{_sysconfdir}/modprobe.d/truescale.conf
%{_sysconfdir}/sysconfig/network-scripts/*
%{_unitdir}/rdma-hw.target
%{_unitdir}/rdma-load-modules@.service
%{_unitdir}/rdma.service
%dir %{dracutlibdir}/modules.d/05rdma
%{dracutlibdir}/modules.d/05rdma/module-setup.sh
%{_udevrulesdir}/*
%if 0%{?dma_coherent}
%{sysmodprobedir}/libmlx4.conf
%endif
%{_libexecdir}/rdma-init-kernel
%{_libexecdir}/rdma-set-sriov-vf
%if 0%{?dma_coherent}
%{_libexecdir}/mlx4-setup.sh
%endif
%{_libexecdir}/truescale-serdes.cmds
%{_sbindir}/rdma-ndd
%{_unitdir}/rdma-ndd.service
%{_mandir}/man8/rdma-ndd.*
%license COPYING.*

%files devel
%doc %{_docdir}/%{name}-%{version}/MAINTAINERS
%dir %{_includedir}/infiniband
%dir %{_includedir}/rdma
%{_includedir}/infiniband/*
%{_includedir}/rdma/*
%if %{with_static}
%{_libdir}/lib*.a
%endif
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/ibv_*
%{_mandir}/man3/rdma*
%{_mandir}/man3/umad*
%{_mandir}/man3/*_to_ibv_rate.*
%if 0%{?dma_coherent}
%ifnarch s390
%{_mandir}/man3/mlx4dv*
%{_mandir}/man3/mlx5dv*
%{_mandir}/man7/mlx5dv*
%endif
%endif
%{_mandir}/man7/rdma_cm.*

%files -n libibverbs
%dir %{_sysconfdir}/libibverbs.d
%dir %{_libdir}/libibverbs
%{_libdir}/libibverbs*.so.*
%{_libdir}/libibverbs/*.so
%if 0%{?dma_coherent}
%ifnarch s390
%{_libdir}/libmlx4.so.*
%{_libdir}/libmlx5.so.*
%endif
%endif
%config(noreplace) %{_sysconfdir}/libibverbs.d/*.driver
%doc %{_docdir}/%{name}-%{version}/libibverbs.md
%doc %{_docdir}/%{name}-%{version}/rxe.md
%doc %{_docdir}/%{name}-%{version}/tag_matching.md
%{_bindir}/rxe_cfg
%{_mandir}/man7/rxe*
%if 0%{?dma_coherent}
%ifnarch s390
%{_mandir}/man7/mlx4dv*
%{_mandir}/man7/mlx5dv*
%endif
%endif
%{_mandir}/man8/rxe*

%files -n libibverbs-utils
%{_bindir}/ibv_*
%{_mandir}/man1/ibv_*

%files -n ibacm
%config(noreplace) %{_sysconfdir}/rdma/ibacm_opts.cfg
%{_bindir}/ib_acme
%{_sbindir}/ibacm
%{_mandir}/man1/ibacm.*
%{_mandir}/man1/ib_acme.*
%{_mandir}/man7/ibacm.*
%{_mandir}/man7/ibacm_prov.*
%{_unitdir}/ibacm.service
%{_unitdir}/ibacm.socket
%dir %{_libdir}/ibacm
%{_libdir}/ibacm/*
%doc %{_docdir}/%{name}-%{version}/ibacm.md

%files -n iwpmd
%{_sbindir}/iwpmd
%{_unitdir}/iwpmd.service
%config(noreplace) %{_sysconfdir}/iwpmd.conf
%{_mandir}/man8/iwpmd.*
%{_mandir}/man5/iwpmd.*

%files -n libibumad
%{_libdir}/libibumad*.so.*

%files -n librdmacm
%{_libdir}/librdmacm*.so.*
%dir %{_libdir}/rsocket
%{_libdir}/rsocket/librspreload.so*
%doc %{_docdir}/%{name}-%{version}/librdmacm.md
%{_mandir}/man7/rsocket.*

%files -n librdmacm-utils
%{_bindir}/cmtime
%{_bindir}/mckey
%{_bindir}/rcopy
%{_bindir}/rdma_client
%{_bindir}/rdma_server
%{_bindir}/rdma_xclient
%{_bindir}/rdma_xserver
%{_bindir}/riostream
%{_bindir}/rping
%{_bindir}/rstream
%{_bindir}/ucmatose
%{_bindir}/udaddy
%{_bindir}/udpong
%{_mandir}/man1/cmtime.*
%{_mandir}/man1/mckey.*
%{_mandir}/man1/rcopy.*
%{_mandir}/man1/rdma_client.*
%{_mandir}/man1/rdma_server.*
%{_mandir}/man1/rdma_xclient.*
%{_mandir}/man1/rdma_xserver.*
%{_mandir}/man1/riostream.*
%{_mandir}/man1/rping.*
%{_mandir}/man1/rstream.*
%{_mandir}/man1/ucmatose.*
%{_mandir}/man1/udaddy.*
%{_mandir}/man1/udpong.*

%files -n srp_daemon
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%{_libexecdir}/srp_daemon/start_on_all_ports
%{_unitdir}/srp_daemon.service
%{_unitdir}/srp_daemon_port@.service
%{_sbindir}/ibsrpdm
%{_sbindir}/srp_daemon
%{_sbindir}/srp_daemon.sh
%{_sbindir}/run_srp_daemon
%{_mandir}/man1/ibsrpdm.1*
%{_mandir}/man1/srp_daemon.1*
%{_mandir}/man5/srp_daemon.service.5*
%{_mandir}/man5/srp_daemon_port@.service.5*
%doc %{_docdir}/%{name}-%{version}/ibsrpdm.md

%changelog
* Sat Jun 06 2020 Honggang Li <honli@redhat.com> - 22.4-5
- libibverbs: Fix ABI_placeholder1 and ABI_placeholder2 assignment
- Resolves: rhbz#1843221

* Tue Apr 28 2020 Honggang Li <honli@redhat.com> - 22.4-4
- libbnxt_re support for some new device ids and generation id
- Resolves: rhbz#1828482

* Mon Mar 30 2020 Honggang Li <honli@redhat.com> - 22.4-3
- Restore three patches
- Resolves: rhbz#1817412

* Wed Feb 19 2020 Honggang Li <honli@redhat.com> - 22.4-2
- Fix ibacm segfault for dual port HCA support IB and Ethernet
- Resolves: rhbz#1793585

* Thu Nov 21 2019 Jarod Wilson <jarod@redhat.com> 22.4-1
- Update to v22.4 stable release
- Support mlx5 scatter to CQE over DCT QP
- Fix ibacm segfault on non-IB hardware
- Resolves: rhbz#1715489
- Resolves: rhbz#1712296

* Tue Aug 27 2019 Jarod Wilson <jarod@redhat.com> 22.3-1
- Update to v22.3 stable release
- Unclamp IPoIP MTUs
- Resolves: rhbz#1647541

* Thu May 30 2019 Jarod Wilson <jarod@redhat.com> 22.1-3
- Actually apply ConnectX-6 DX device ID patch
- Related: rhbz#1687426

* Thu May 02 2019 Jarod Wilson <jarod@redhat.com> 22.1-2
- Refresh stable-v22 branch fixes
- Add ConnectX-6 DX device IDs
- Resolves: rhbz#1687426

* Wed Mar 27 2019 Jarod Wilson <jarod@redhat.com> 22.1-1
- Update to upstream v22.1 release with stable-v22 branch fixes
- Add support for Broadcom 57500 RoCE adapter
- Resolves: rhbz#1678274

* Wed Jan 23 2019 Jarod Wilson <jarod@redhat.com> 22-1
- Rebase to upstream rdma-core v22
- Resolves: rhbz#1641921
- Add mlx5 IB Device Memory support (MEMIC)
- Resolves: rhbz#1644697
- Add mlx5 Tunnel protocol RX decap/encap offload
- Resolves: rhbz#1644709
- Add mlx5 Tunnel protocol TX decap/encap offload
- Resolves: rhbz#1644778
- Add support for mlx5 infiniband flow counters
- Resolves: rhbz#1644714
- Add mlx5 DEVX interface
- Resolves: rhbz#1644722
- Add libbnxt_re support for SRQ
- Resolves: rhbz#1570393

* Tue Jun 26 2018 Jarod Wilson <jarod@redhat.com> 17.2-3
- Restore RHEL7 systemd compat patches for srp_daemon
- Resolves: rhbz#1595019

* Wed Jun 20 2018 Jarod Wilson <jarod@redhat.com> 17.2-2
- Restore SysV Initscripts ib ifup and ifdown helpers
- Adjust MTU limit for IPoIB in datagram mode via ifup-ib
- Resolves: rhbz#1593426
- Resolves: rhbz#1593334

* Fri Jun 15 2018 Jarod Wilson <jarod@redhat.com> 17.2-1
- Rebase to upstream rdma-core v17.2 stable release

* Wed Jun 13 2018 Jarod Wilson <jarod@redhat.com> 17.1-3
- Grab latest stable-v17 fixes from upstream
- Fix Provides/Obsoletes on removed libibcm
- Fix Provides/Obsoletes on removed libehca
- Straighten out SW parsing feature support for DPDK
- Fix mlx5 rate-limiting support
- Resolves: rhbz#1588096
- Resovles: rhbz#1534856
- Resolves: rhbz#1589525

* Thu May 03 2018 Jarod Wilson <jarod@redhat.com> 17.1-2
- Match kernel ABI with kernel v4.17 for 32-on-64bit compatibility
- Resolves: rhbz#1573884

* Mon Apr 16 2018 Jarod Wilson <jarod@redhat.com> 17.1-1
- Rebase to upstream rdma-core v17.1 stable release
- No more libibcm or ib sysv initscripts
- Resolves: rhbz#1515647
- Resolves: rhbz#1517208
- Resolves: rhbz#1523201
- Resolves: rhbz#1541751

* Tue Feb 27 2018 Jarod Wilson <jarod@redhat.com> 15-7
- i40iw: revoke systemd udev rules auto-load on i40e hardware, due to
  causing problems with suspend and resume, and fall back to load via
  systemd rdma initscript.
- Resolves: rhbz#1561566

* Mon Feb 19 2018 Jarod Wilson <jarod@redhat.com> 15-6
- libbnxt_re: fix lat test failure in event mode
- Resolves: rhbz#1545248

* Tue Feb 06 2018 Jarod Wilson <jarod@redhat.com> 15-5
- libmlx4: report RSS caps for improved DPDK support
- Fix double mutex unlock in iwpmd
- Resolves: rhbz#1527350
- Resolves: rhbz#1542362

* Mon Jan 15 2018 Jarod Wilson <jarod@redhat.com> 15-4
- Add support for extended join multicast API in librdmacm
- Add support for striding RQ on mlx5
- Resolves: rhbz#1515487, rhbz#1516571

* Tue Dec 26 2017 Honggang Li <honli@redhat.com> 15-3
- srp_daemon: Don't create async_ev_thread if only run once
- srp_daemon: Remove unsupported systemd configurations
- srp_daemon: Start srp_daemon service after network target
- Resolves: bz1525193
- Resolves: bz1528671

* Mon Nov 13 2017 Jarod Wilson <jarod@redhat.com> 15-2
- Fix ibacm segfault and improper multicast handling
- Resolves: rhbz#1502745
- Resolves: rhbz#1502759

* Fri Sep 22 2017 Jarod Wilson <jarod@redhat.com> 15-1
- Update to upstream v15 release
- Resolves: rhbz#1494607

* Tue May 30 2017 Jarod Wilson <jarod@redhat.com> 13-7
- Add support for mlx5 Expand raw packet capabilities
- Resolves: rhbz#1456561

* Mon May 22 2017 Jarod Wilson <jarod@redhat.com> 13-6
- Clean up htonll/ntohll handling for opa-ff/infiniband-diags compile
- Add necessary Provides/Obsoletes for old -static packages
- Remove ibverbs providers that we aren't currently able to support
- Resolves: rhbz#1453096, rhbz#1451607

* Wed Apr 26 2017 Honggang Li <honli@redhat.com> 13-5
- rdma-ndd: Fix a busy loop for aarch64 platform
- Resolves: bz1442789

* Thu Apr 13 2017 Honggang Li <honli@redhat.com> 13-4
- srp_daemon: Don't rely on attribute offset in get_shared_pkeys
- Resolves: bz1432964

* Mon Apr 03 2017 Jarod Wilson <jarod@redhat.com> - 13-3
- Add necessary Provides/Obsoletes for rdma-ndd (rhbz 1437804)

* Mon Mar 27 2017 Jarod Wilson <jarod@redhat.com> - 13-2
- Build what we can on s390, don't exclude it entirely (rhbz 1434029)

* Tue Mar 21 2017 Jarod Wilson <jarod@redhat.com> - 13-1
- Update to rdma-core v13 release (rhbz 1404035)
- Mellanox mlx5 Direct Verbs support (rhbz 1426430)
- Get build working on s390x, less mlx5 (rhbz 1434029)

* Mon Mar 20 2017 Jarod Wilson <jarod@redhat.com> - 12-5
- Fix up multi-lib conflicts in ibacm files (rhbz 1429362)

* Mon Mar 13 2017 Jarod Wilson <jarod@redhat.com> - 12-4
- Clean up devel files list
- Fix up a few dependencies rpmdiff complained about (rhbz 1404035)
- Add Requires: pciutils for dracut to behave in minimalist cases (rhbz 1429046)
- Adjust Conflicts: on infiniband-diags to match RHEL packaging (rhbz 1428785)

* Mon Mar 06 2017 Jarod Wilson <jarod@redhat.com> - 12-3
- Take libi40iw out of tech-preview state (rhbz 1428930)
- Add ibv_*_pingpong man pages (rhbz 1416541)

* Thu Feb 09 2017 Jarod Wilson <jarod@redhat.com> - 12-2
- Make sure ocrdma module is classified as tech-preview (rhbz 1418224)

* Fri Jan 27 2017 Jarod Wilson <jarod@redhat.com> - 12-1
- Update to upstream final v12 release

* Wed Jan 25 2017 Jarod Wilson <jarod@redhat.com> - 12-0.1.rc3.1
- Initial import to Fedora package database via post-v12-rc3 git snapshot
