%global have_usbredir 1
%global have_spice    1
%global have_fdt      0
%global have_gluster  1
%global have_numa 1
%global have_librdma 1
%global have_seccomp 1
%global have_tcmalloc 1

%ifnarch %{ix86} x86_64 aarch64
    %global have_seccomp 0
%endif

%ifnarch %{ix86} x86_64
    %global have_usbredir 0
%endif

%ifarch s390 s390x %{arm}
    %global have_librdma 0
    %global have_numa 0
    %global have_tcmalloc 0
%endif

%ifarch %{ix86}
    %global kvm_target    i386
%endif
%ifarch x86_64
    %global kvm_target    x86_64
%else
    %global have_spice   0
    %global have_gluster 0
%endif
%ifarch %{power64}
    %global kvm_target    ppc64
    %global have_fdt     1
%endif
%ifarch s390
    %global kvm_target    s390
%endif
%ifarch s390x
    %global kvm_target    s390x
%endif
%ifarch ppc
    %global kvm_target    ppc
    %global have_fdt     1
%endif
%ifarch aarch64
    %global kvm_target    aarch64
    %global have_fdt     1
%endif
%ifarch %{arm}
    %global kvm_target    arm
    %global have_fdt     1
%endif

#Versions of various parts:

%define pkgname qemu-kvm

Summary: QEMU guest agent
Name: qemu-guest-agent
Version: 2.12.0
Release: 3%{?dist}
# Epoch because we pushed a qemu-1.0 package. AIUI this can't ever be dropped
Epoch: 10
License: GPLv2
Group: System Environment/Daemons
URL: http://www.qemu.org/
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
    %define _smp_mflags %{nil}
%endif

Source0: http://wiki.qemu.org/download/qemu-2.12.0.tar.xz

Source1: qemu-guest-agent.service
Source2: 99-qemu-guest-agent.rules
Source3: qemu-ga.sysconfig
Source4: build_configure.sh

# For bz#1567041 - qemu-guest-agent does not parse PCI bridge links in "build_guest_fsinfo_for_real_device" (q35)
Patch1: qemuga-qemu-ga-make-get-fsinfo-work-over-pci-bridges.patch
# For bz#1567041 - qemu-guest-agent does not parse PCI bridge links in "build_guest_fsinfo_for_real_device" (q35)
Patch2: qemuga-qga-fix-driver-leak-in-guest-get-fsinfo.patch
# For bz#1611062 - "virsh vcpucount --guest" fails after hotunplug a vcpu with intermediate order by "setvcpu"
Patch3: qemuga-qga-ignore-non-present-cpus-when-handling-qmp_guest_.patch
# For bz#1635571 - [RFE] Report disk device name and serial number (qemu-guest-agent on Linux)
Patch5: qemuga-configure-add-test-for-libudev.patch
# For bz#1635571 - [RFE] Report disk device name and serial number (qemu-guest-agent on Linux)
Patch6: qemuga-qga-linux-report-disk-serial-number.patch
# For bz#1635571 - [RFE] Report disk device name and serial number (qemu-guest-agent on Linux)
Patch7: qemuga-qga-linux-return-disk-device-in-guest-get-fsinfo.patch

BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: systemd
BuildRequires: systemd-devel
BuildRequires: python
BuildRequires: systemtap-sdt-devel
BuildRequires: perl-podlators
BuildRequires: texinfo
%if 0%{have_tcmalloc}
BuildRequires: gperftools-devel
%endif

%define qemudocdir %{_docdir}/%{pkgname}

%description
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%post
%systemd_post qemu-guest-agent.service

%preun
%systemd_preun qemu-guest-agent.service

%postun
%systemd_postun_with_restart qemu-guest-agent.service

%prep
%setup -q -n qemu-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# if patch fuzzy patch applying will be forbidden
%define with_fuzzy_patches 0
%if %{with_fuzzy_patches}
    patch_command='patch -p1 -s'
%else
    patch_command='patch -p1 -F1 -s'
%endif

ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

# don't apply patch if it's empty or does not exist
ApplyOptionalPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    return 0
  fi
  local C=$(wc -l $RPM_SOURCE_DIR/$patch | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch $patch ${1+"$@"}
  fi
}



ApplyOptionalPatch qemu-kvm-test.patch

%build
buildarch="%{kvm_target}-softmmu"

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# QEMU already knows how to set _FORTIFY_SOURCE
%global optflags %(echo %{optflags} | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')

%ifarch s390
    # drop -g flag to prevent memory exhaustion by linker
    %global optflags %(echo %{optflags} | sed 's/-g//')
    sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif

cp %{SOURCE4} build_configure.sh
./build_configure.sh  \
  "%{_prefix}" \
  "%{_libdir}" \
  "%{_sysconfdir}" \
  "%{_localstatedir}" \
  "%{_libexecdir}" \
  "qemu-ga" \
  "%{kvm_target}" \
  "%{name}-%{version}-%{release}" \
  "%{optflags}" \
%if 0%{have_fdt}
  enable \
%else
  disable \
%endif
%if 0%{have_tcmalloc}
  enable \
%else
  disable \
%endif
  --target-list= \
  --cpu="%{kvm_target}"

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make qemu-ga %{?_smp_mflags} $buildldflags
make qemu-ga.8

%install
%define _udevdir %(pkg-config --variable=udevdir udev)/rules.d


# For the qemu-guest-agent subpackage, install:
# - the systemd service file and the udev rules:
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_udevdir}
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_udevdir}

# - the environment file for the systemd service:
install -D -p -m 0644 %{SOURCE3} \
 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/qemu-ga

# - the fsfreeze hook script:
install -D --preserve-timestamps \
  scripts/qemu-guest-agent/fsfreeze-hook \
  $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook

# - the directory for user scripts:
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook.d

# - and the fsfreeze script samples:
mkdir --parents $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/qemu-ga/fsfreeze-hook.d/
install --preserve-timestamps --mode=0644 \
  scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample \
  $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/qemu-ga/fsfreeze-hook.d/

# - Install dedicated log directory:
mkdir -p -v $RPM_BUILD_ROOT%{_localstatedir}/log/qemu-ga/

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -c -m 0755  qemu-ga ${RPM_BUILD_ROOT}%{_bindir}/qemu-ga

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m 0644  qemu-ga.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/

%files
    %defattr(-,root,root,-)
    %doc COPYING README
    %{_bindir}/qemu-ga
    %{_unitdir}/qemu-guest-agent.service
    %{_udevdir}/99-qemu-guest-agent.rules
    %config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
    %{_sysconfdir}/qemu-ga
    %{_datadir}/%{pkgname}/qemu-ga
    %{_mandir}/man8/qemu-ga.8*
    %dir %{_localstatedir}/log/qemu-ga


%changelog
* Wed Dec 12 2018 Miroslav Rezanina <mrezanin@redhat.com> - 2.12.0-3.el7
- qemuga-qga-ignore-non-present-cpus-when-handling-qmp_guest_.patch [bz#1611062]
- qemuga-qemu-guest-agent.spec-add-systemd-devel-dependency.patch [bz#1635571]
- qemuga-configure-add-test-for-libudev.patch [bz#1635571]
- qemuga-qga-linux-report-disk-serial-number.patch [bz#1635571]
- qemuga-qga-linux-return-disk-device-in-guest-get-fsinfo.patch [bz#1635571]
- Resolves: bz#1611062
  ("virsh vcpucount --guest" fails after hotunplug a vcpu with intermediate order by "setvcpu")
- Resolves: bz#1635571
  ([RFE] Report disk device name and serial number (qemu-guest-agent on Linux))

* Tue Jul 24 2018 Miroslav Rezanina <mrezanin@redhat.com> - 2.12.0-2.el7
- qemuga-qemu-ga-make-get-fsinfo-work-over-pci-bridges.patch [bz#1567041]
- qemuga-qga-fix-driver-leak-in-guest-get-fsinfo.patch [bz#1567041]
- Resolves: bz#1567041
  (qemu-guest-agent does not parse PCI bridge links in "build_guest_fsinfo_for_real_device" (q35))

* Wed May 02 2018 Miroslav Rezanina <mrezanin@redhat.com> - 2.12.0-1.el7
- Rebase to 2.12.0 base [bz#1562218]
- Resolves: bz#1562218
  (Rebase qemu-guest-agent for RHEL-7.6)

* Fri May 19 2017 Miroslav Rezanina <mrezanin@redhat.com> - 2.8.0-2.el7
- qemuga-Remove-unnecessary-dependencies.patch [bz#1441999]
- Resolves: bz#1441999
  (Clean qemu-ga dependencies)

* Tue Feb 07 2017 Miroslav Rezanina <mrezanin@redhat.com> - 2.8.0-1.el7
- Rebase to 2.8.0 base [bz#1414676]
- Resolves: bz#1414676
  (Rebase qemu-guest-agent to 2.8.0 base)

* Thu Sep 01 2016 Miroslav Rezanina <mrezanin@redhat.com> - 2.5.0-3.el7
- qemuga-spec-add-qemu-ga-man-page.patch [bz#1101556]
- Resolves: bz#1101556
  ([RFE] qemu-ga should have a config file)

* Wed Jun 15 2016 Miroslav Rezanina <mrezanin@redhat.com> - 2.5.0-2.el7
- qemuga-redhat-blacklist-guest-exec-commands.patch [bz#1340346]
- Resolves: bz#1340346
  (blacklist guest-exec in newer version of qemu-guest-agent)

* Tue Jan 12 2016 Miroslav Rezanina <mrezanin@redhat.com> - 2.5.0-1.el7
- Rebase to QEMU 2.5.0 [bz#1297673]
- Resolves: bz#1297673
  (Rebase to QEMU 2.5)
* Tue Aug 25 2015 Miroslav Rezanina <mrezanin@redhat.com> - 2.3.0-3.el7
- qemuga-Do-not-stop-qemu-guest-agent-service-on-target-switc.patch [bz#1160930]
- Resolves: bz#1160930
  (The guest agent service in rhel7 guest will be stopped after run the init command)

* Mon Jul 13 2015 Miroslav Rezanina <mrezanin@redhat.com> - 2.3.0-2.el7
- synchronized with qemu-kvm-rhev-2.3.0-9.el7
- qemuga-Change-fsreeze-hook-default-location.patch [bz#1210707]
- qemuga-qga-commands-posix-Fix-bug-in-guest-fstrim.patch [bz#1211973]
- Resolves: bz#1210707
  (The default path '/etc/qemu/fsfreeze-hook' for 'fsfreeze-hook' script doesn't exist)
- Resolves: bz#1211973
  ('guest-fstrim' failed for guest with os on spapr-vscsi disk)

* Tue Apr 28 2015 Miroslav Rezanina <mrezanin@redhat.com> - 2.3.0-1.el7
- Rebase to 2.3.0 [bz#1194152]
- Resolves: bz#1194152
  (Rebase to 2.3.0)

* Tue Oct 21 2014 Miroslav Rezanina <mrezanin@redhat.com> - 2.1.0-4.el7
- kvm-Mark-etc-sysconfig-qemu-ga-as-config-noreplace.patch [bz#1150924]
- Resolves: bz#1150924
  (/etc/sysconfig/qemu-ga is replaced when updated)

* Thu Aug 28 2014 Miroslav Rezanina <mrezanin@redhat.com> - 2.1.0-3.el7
- Allow building qemu-guest-agent on ppc64le
- Synchronize with qemu-kvm-rhev-2.1.0-3.el7
- Resolves: bz#1132718
  (qemu-guest-agent fails to build for ppc64le)

* Sat Aug 02 2014 Miroslav Rezanina <mrezanin@redhat.com> - 2.1.0-2.el7
- Create separate qemu-guest-agent package based on qemu-kvm-rhev-2.1.0-1.el7 [bz#1117096]
- Resolves: #bz1117096

* Sat Aug 02 2014 Miroslav Rezanina <mrezanin@redhat.com> - 2.1.0-1.el7
- Rebase to 2.1.0 [bz#1121609]
- Resolves: bz#1121609
 (Rebase qemu-kvm-rhev to qemu 2.1)

