Name:           nfs4-acl-tools
Version:        0.3.3
Release:        20%{?dist}
Summary:        The nfs4 ACL tools
Group:          Applications/System
License:        BSD
URL:            http://www.citi.umich.edu/projects/nfsv4/linux/

BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Source0:        http://www.citi.umich.edu/projects/nfsv4/linux/nfs4-acl-tools/%{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: libattr-devel

Patch001: nfs4acl-0.3.3-ace.patch
Patch002: nfs4acl-0.3.3-memleak.patch
Patch003: nfs4acl-0.3.3-infile-segfault.patch
Patch004: nfs4-acl-tools-0.3.3-DENY-ace-for-DELETE-WRITE_OWNE.patch
#
# RHEL 7.3
#
Patch005: nfs4-acl-tools-0.3.3-spaceinname.patch
Patch006: nfs4-acl-tools-0.3.3-fd-leak.patch
#
# RHEL 7.4
#
Patch007: nfs4-acl-tools-0.3.3-manpage-acls.patch
#
# RHEL 7.6
#
Patch008: nfs4-acl-tools-0.3.3-more-paths.patch
Patch009: nfs4-acl-tools-0.3.3-R-flag.patch
#
# RHEL 7.7
#
Patch010: nfs4-acl-tools-0.3.3-skip-comment-field.patch

Patch100: nfs4acl-0.2.0-compile.patch

%description
This package contains commandline and GUI ACL utilities for the Linux
NFSv4 client.

%prep
%setup -q

%patch001 -p1
%patch002 -p1
%patch003 -p1
# 1160463 - nfs4_setfacl, nfs4_getfacl ignores DENY ace for DELETE
%patch004 -p1
# Bug 1284597 - nfs4_setfacl command fails when NFSv4 group...
%patch005 -p1
# 1284608 - nfs4-acl-tools: FD leak in edit_ACL() 
%patch006 -p1
# 1493905 - Need to add the method used for inheritance-only flag...
%patch007 -p1
# 1412181 - nfs4_getfacl should accept more paths
%patch008 -p1
# 1416685 - nfs4_setfacl -R should not bail out on error 
%patch009 -p1
# 1666850 - nfs4_setfacl error applying nfs4_getfacl output 
%patch010 -p1

%patch100 -p1

%build
%ifarch s390 s390x sparc
PIE="-fPIE"
%else
PIE="-fpie"
%endif

RELRO="-Wl,-z,relro,-z,now"

CFLAGS="`echo $RPM_OPT_FLAGS $PIE $RELRO`"
export LDFLAGS="`echo $PIE $RELRO`"

%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING INSTALL README TODO VERSION
%{_bindir}/nfs4_editfacl
%{_bindir}/nfs4_getfacl
%{_bindir}/nfs4_setfacl
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Apr 10 2019 Steve Dickson <steved@redhat.com> 0.3.3-20
- nfs4_setfacl: Skip comment field while reading ACE(s) (bz 1666850)

* Mon Jul  9 2018 Steve Dickson <steved@redhat.com> 0.3.3-19
- Add support for recursive nfs4_getfacl option (bz 1416685)

* Tue Jun 26 2018 Steve Dickson <steved@redhat.com> 0.3.3-18
-  nfs4_getfacl: Add support to accept more paths (bz 1412181)

* Tue Dec 12 2016 Steve Dickson <steved@redhat.com> 0.3.3-17
- Describe how the Linux server handles inheritable acls (bz 1493905)

* Tue Jun  7 2016 Steve Dickson <steved@redhat.com> 0.3.3-16
- Fixed the RELRO check (bz 1092556)

* Tue Apr  5 2016 Steve Dickson <steved@redhat.com> 0.3.3-15
- Allow spaces in group principal names (bz 1284597)
- Fixed FD leak in edit_ACL() (bz 1284608)
- Added the RELRO check (bz 1092556)

* Thu Jul 30 2015 Steve Dickson <steved@redhat.com> 0.3.3-14
- Handle the setting of DENY ace for DELETE, WRITE_OWNER (bz 1160463)

* Sat Feb 22 2014 Steve Dickson <steved@redhat.com> 0.3.3-13
- Fixed segfault when inputting a file (bz 882068)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.3.3-12
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.3.3-11
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 16 2009 Steve Dickson <steved@redhat.com> - 0.3.3-6
- Fix a memory leak in nfs4_getfacl

* Mon Nov 16 2009 Steve Dickson <steved@redhat.com> - 0.3.3-5
- Fixes segfaulting issues with ACEs that have empty mask fields

* Thu Jul 30 2009 Steve Dickson <steved@redhat.com> - 0.3.3-4
- Change Group in spec file (bz 512580)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Steve Dickson <steved@redhat.com> - 0.3.3-1
- Updated to latest upstream version: 0.3.3

* Wed Oct 29 2008 Steve Dickson <steved@redhat.com> - 0.3.2-3
- Removed fuzzness from the compile.patch (bz 321745)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.2-2
- Autorebuild for GCC 4.3

* Fri Oct 26 2007 Steve Dickson <steved@redhat.com> - 0.3.2-1
- Updated to latest upstream version 0.3.2

* Tue Mar 27 2007 Steve Dickson <steved@redhat.com> - 0.3.1-1.2
- Checked in to Fedora CVS 

* Thu Mar  8 2007  Steve Dickson <steved@redhat.com> - 0.3.1-1.1
- Updated to latest upstream version 0.3.1 which eliminated the 
  need for the patches introduced in the previous commit.

* Tue Mar  6 2007  Tom "spot" Callaway <tcallawa@redhat.com> 0.3.0-1.1
- lose the BR for autotools
- Patch in support for destdir
- use %%configure macro, make DESTDIR= install
- add sparc to -fPIE (trivial, but correct)
- destdir revealed missing/poorly created symlink, patch fixes it, add nfs4_editfacl to files
- LDFLAGS passed to configure/exported were being blindly overwritten, patch fixes

* Fri Mar  2 2007  Steve Dickson <steved@redhat.com> - 0.3.0-1
- Updated to latest upstream version 0.3.0
- Fixed minor issues in spec file from the package review

* Fri Feb 16 2007 Steve Dickson <steved@redhat.com> - 0.2.0-1
- Initial commit
