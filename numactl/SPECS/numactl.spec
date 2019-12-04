Name:		numactl
Summary:	Library for tuning for Non Uniform Memory Access machines
Version:	2.0.12
Release:	3%{?dist}.1
# libnuma is LGPLv2 and GPLv2
# numactl binaries are GPLv2 only
License:	GPLv2
Group:		System Environment/Base
URL:            https://github.com/numactl/numactl
Source0:        https://github.com/numactl/numactl/releases/download/%{version}/numactl-%{version}.tar.gz
Buildroot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  libtool automake autoconf

ExcludeArch: s390 s390x %{arm}

Patch1: numactl-2.0.12-numastat-when-reading-no-exist-pid-return-EXIT_FAILU.patch
Patch2: numactl-2.0.12-Fix-crashes-when-using-the-touch-option.patch

%description
Simple NUMA policy support. It consists of a numactl program to run
other programs with a specific NUMA policy.

%package libs
Summary: libnuma libraries
# There is a tiny bit of GPLv2 code in libnuma.c
License: LGPLv2 and GPLv2
Group: System Environment/Libraries

%description libs
numactl-libs provides libnuma, a library to do allocations with
NUMA policy in applications.

%package devel
Summary: Development package for building Applications that use numa
Group: System Environment/Libraries
Requires: %{name}-libs = %{version}-%{release}
License: LGPLv2 and GPLv2

%description devel
Provides development headers for numa library calls

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1

%build
%configure --prefix=/usr --libdir=%{_libdir}
make clean
make CFLAGS="$RPM_OPT_FLAGS -I."

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

%post -p /sbin/ldconfig
%post libs -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%doc README.md
%{_bindir}/numactl
%{_bindir}/numademo
%{_bindir}/numastat
%{_bindir}/memhog
%{_bindir}/migspeed
%{_bindir}/migratepages
%{_mandir}/man8/*.8*
%exclude %{_mandir}/man2/*.2*

%files libs
%{_libdir}/libnuma.so.1.0.0
%{_libdir}/libnuma.so.1

%files devel
%{_libdir}/libnuma.so
%{_libdir}/pkgconfig/numa.pc
%exclude %{_libdir}/libnuma.a
%exclude %{_libdir}/libnuma.la
%{_includedir}/numa.h
%{_includedir}/numaif.h
%{_includedir}/numacompat1.h
%{_mandir}/man3/*.3*

%changelog
* Thu Oct 17 2019 Pingfan Liu <piliu@redhat.com> - 2.0.12-3.1
- Fix crashes when using the "--touch" option

* Sat Jun  1 2019 Pingfan Liu <piliu@redhat.com> - 2.0.12-3
- numastat: bail out if reading no-exist pid

* Fri May 31 2019 Pingfan Liu <piliu@redhat.com> - 2.0.12-2
- numastat: when reading no-exist pid, return EXIT_FAILURE
- Rebase to numactl-2.0.12

* Tue Aug 8 2017 Petr Oros <poros@redhat.com> - 2.0.9-7
- Segment fault when numa nodes not sequential or contiguous
- Resolves: #1219445

* Mon Dec 14 2015 Petr Holasek <pholasek@redhat.com> - 2.0.9-6
- confusing warning supressed (bz1270734)

* Wed Jul 01 2015 Petr Holasek <pholasek@redhat.com> - 2.0.9-5
- numa_node_to_cpu skips over non-existing nodes (bz1180415)

* Mon Nov 10 2014 Petr Holasek <pholasek@redhat.com> - 2.0.9-4
- Fixed missing question mark in dist macro

* Thu Jul 31 2014 Petr Holasek <pholasek@redhat.com> - 2.0.9-3
- Fixed hw detect segfault (bz1061874)
- Fixed printing of preferred node for MPOL_BIND (bz1119887)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0.9-2
- Mass rebuild 2013-12-27

* Fri Oct 25 2013 Petr Holasek <pholasek@redhat.com> - 2.0.9-1
- rebased to version 2.0.9 (bz1017053)

* Mon Aug 19 2013 Petr Holasek <pholasek@redhat.com> - 2.0.8-6
- localalloc manpage option is more verbose (bz881779)

* Tue Jul 30 2013 Petr Holasek <pholasek@redhat.com> - 2.0.8-5
- numastat minor bugfixes
- manpage and usage fixes (bz948377)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Petr Holasek <pholasek@redhat.com> - 2.0.8-3
- deleted empty numastat file

* Thu Nov  1 2012 Tom Callaway <spot@fedoraproject.org> - 2.0.8-2
- fix license issues

* Fri Oct 26 2012 Petr Holasek <pholasek@redhat.com> - 2.0.8-1
- Rebased to version 2.0.8

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Petr Holasek <pholasek@redhat.com> - 2.0.7-6
- numademo segfault fix (bz823125, bz823127)

* Sun Apr 15 2012 Petr Holasek <pholasek@redhat.com> - 2.0.7-5
- Library splitted out of numactl package to numactl-libs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 01 2012 Anton Arapov <anton@redhat.com> - 2.0.7-3
- Include missing manpages

* Sat Jun 18 2011 Peter Robinson <pbrobinson@gmail.com> - 2.0.7-2
- Exclude ARM platforms

* Fri Apr 15 2011 Anton Arapov <anton@redhat.com> - 2.0.7-1
- Update to latest upstream stable version (bz 696703)

* Tue Mar 22 2011 Anton Arapov <anton@redhat.com> - 2.0.6-2
- Better manpages (bz 673613)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Neil Horman <nhorman@redhat.com> - 2.0.6-1
- Update to latest upstream stable version (bz 666379)

* Mon Oct 18 2010 Neil Horman <nhorman@redhat.com> - 2.0.5-1
- Update to latest stable upstream source

* Mon Feb 15 2010 Neil Horman <nhorman@redhat.com> - 2.0.3-8
- Remove static libs from numactl (bz 556088)

* Mon Aug 10 2009 Neil Horman <nhorman@redhat.com> - 2.0.3-7
- Add destructor to libnuma.so to free allocated memory (bz 516227)

* Mon Aug 10 2009 Neil Horman <nhorman@redhat.com> - 2.0.3-6
- Fix obo in nodes_allowed_list strncpy (bz 516223)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Neil Horman <nhorman@redhat.com>
- Update to full 2.0.3 version (bz 506795)

* Wed Jun 17 2009 Neil Horman <nhorman@redhat.com>
- Fix silly libnuma warnings again (bz 499633)

* Fri May 08 2009 Neil Horman <nhorman@redhat.com>
- Update to 2.0.3-rc3 (bz 499633)

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2.0.2-4
- Remove warning from libnuma (bz 484552)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Neil Horman <nhorman@redhat.com> - 2.0.2-2
- Fix build break due to register selection in asm

* Mon Sep 29 2008 Neil Horman <nhorman@redhat.com> - 2.0.2-1
- Update rawhide to version 2.0.2 of numactl

* Fri Apr 25 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-6
- Fix buffer size passing and arg sanity check for physcpubind (bz 442521)

* Fri Mar 14 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-5
- Fixing spec file to actually apply alpha patch :)

* Fri Mar 14 2008 Neil Horman <nhorman@redhat.com> - 1.0.2-4
- Add alpha syscalls (bz 396361)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-3
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Neil Horman <nhorman@redhat.com> - 1.0.2-1
- Update numactl to fix get_mempolicy signature (bz 418551)

* Fri Dec 14 2007 Neil Horman <nhorman@redhat.com> - 1.0.2-1
- Update numactl to latest version (bz 425281)

* Tue Aug 07 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-4
- Fixing some remaining merge review issues (bz 226207)

* Fri Aug 03 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-3
- fixing up merge review (bz 226207)

* Fri Jan 12 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-2
- Properly fixed bz 221982
- Updated revision string to include %{dist}

* Thu Jan 11 2007 Neil Horman <nhorman@redhat.com> - 0.9.8-1.38
- Fixed -devel to depend on base package so libnuma.so resolves

* Thu Sep 21 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.36
- adding nodebind patch for bz 207404

* Fri Aug 25 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.35
- moving over libnuma.so to -devel package as well

* Fri Aug 25 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.34
- split out headers/devel man pages to a devel subpackage

* Tue Aug 15 2006 Neil Horman <nhorman@redhat.com> - 0.9.8-1.32
- add patch for broken cpu/nodebind output (bz 201906)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8-1.31
- rebuild

* Tue Jun 13 2006 Neil Horman <nhorman@redhat.com>
- Rebased numactl to version 0.9.8 for FC6/RHEL5

* Wed Apr 26 2006 Neil Horman <nhorman@redhat.com>
- Added patches for 64 bit overflows and cpu mask problem

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com>
- rebuild for ppc TLS issue (#184446)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.4-1.25.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jul  7 2005 Dave Jones <davej@redhat.com>
- numactl doesn't own the manpage dirs. (#161547)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- rebuild with -D_FORTIFY_SOURCE=2

* Wed Nov 10 2004 David Woodhouse <dwmw2@redhat.com>
- Fix build on x86_64

* Thu Oct 21 2004 David Woodhouse <dwmw2@redhat.com>
- Add PPC support

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jun 05 2004 Warren Togami <wtogami@redhat.com> 
- spec cleanup

* Sat Jun 05 2004 Arjan van de Ven <arjanv@redhat.com>
- initial packaging

