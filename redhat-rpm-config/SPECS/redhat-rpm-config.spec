Summary: CentOS specific rpm configuration files
Name: redhat-rpm-config
Version: 9.1.0
Release: 72%{?dist}
# No version specified.
License: GPL+
Group: Development/System
URL: http://git.fedorahosted.org/git/redhat-rpm-config
Source: redhat-rpm-config-%{version}.tar.bz2

# gcc specs files for hardened builds
Source1: redhat-hardened-cc1
Source2: redhat-hardened-ld

# up-to-date copies of config.guess and config.sub (from automake 1.13.1)
Source10: config.guess
Source11: config.sub

# kabi provides generator
Source20: kabi.attr
Source21: kabi.sh

# Script to handle ppc64le in libtool and associated configure files.
Source30: libtool-handle-ppc64le.sh

Patch0: redhat-rpm-config-9.1.0-strict-python-bytecompile.patch
Patch1: redhat-rpm-config-9.1.0-fix-requires.patch
Patch2: redhat-rpm-config-9.1.0-no-strip-note.patch
Patch3: redhat-rpm-config-9.1.0-pkgconfig-private.patch
# the macros defined by this patch are for things that need to be defined
# at srpm creation time when it is not feasable to require the base packages
# that would otherwise be providing the macros. other language/arch specific
# macros should not be defined here but instead in the base packages that can
# be pulled in at rpm build time, this is specific for srpm creation.
Patch4: redhat-rpm-config-9.1.0-arches-macros.patch
Patch5: redhat-rpm-config-9.1.0-arm.patch
Patch6: redhat-rpm-config-9.1.0-relro.patch
Patch7: redhat-rpm-config-9.1.0-hardened.patch
Patch8: redhat-rpm-config-9.1.0-ppc-no-minimal-toc.patch
Patch9: redhat-rpm-config-9.1.0-dwz.patch
Patch10: redhat-rpm-config-9.1.0-minidebuginfo.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=783433
Patch11: redhat-rpm-config-9.1.0-python-hardlink-spaces-in-filenames.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=853216
Patch12:redhat-rpm-config-9.1.0-use-prefix-macro.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=648996
Patch13: redhat-rpm-config-9.1.0-kernel-source.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=465664
Patch14: redhat-rpm-config-9.1.0-java-repack-order.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=741089
Patch15: 0001-Drop-un-setting-LANG-and-DISPLAY-in-various-build-st.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=783932
Patch16: redhat-rpm-config-9.1.0-filtering-spaces-in-filename.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=872737
Patch17: redhat-rpm-config-9.1.0-java-repack-spaces-in-filenames.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=951669
Patch18: redhat-rpm-config-9.1.0-record-switches.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=951442
Patch19: redhat-rpm-config-9.1.0-configfoo.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=909788
Patch20: redhat-rpm-config-9.1.0-aarch64.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=914831
Patch21: redhat-rpm-config-9.1.0-fcflags.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=669638
Patch22: redhat-rpm-config-9.1.0-ncpus-max.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=905573
Patch23: redhat-rpm-config-9.1.0-jar-repack-perms.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=805266
Patch24: redhat-rpm-config-9.1.0-rhel7-arch-optflags.patch
# forward-port of various kABI-fixes from rhel-6
Patch25: redhat-rpm-config-9.1.0-kmod-kabi.patch
# allow kmod building against z-stream kernels
Patch26: redhat-rpm-config-9.1.0-kmod-brew-build.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=833747
Patch27: redhat-rpm-config-9.1.0-fix-find-provides-modalias-permissions.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1002618
Patch28: redhat-rpm-config-9.1.0-fix-depmod-path.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1040025
Patch29: redhat-rpm-config-9.1.0-stackprotector-strong.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1051558
Patch30: redhat-rpm-config-9.1.0-perfbuild.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1049175
Patch31: redhat-rpm-config-9.1.0-use-kverrel-for-kmodtool.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1126086
Patch32: redhat-rpm-config-9.1.0-fix-kabi-path.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1179523
Patch33: redhat-rpm-config-9.0.3-shebang.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1250015
Patch34: redhat-rpm-config-9.1.0-Fix-stripping-of-binaries.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1061619
Patch35: redhat-rpm-config-9.1.0-find-provides.libtool.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1270053
Patch36: redhat-rpm-config-9.1.0-repack-jars.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1323087
Patch37: redhat-rpm-config-9.0.3-latest-kernel.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1057327
Patch38: redhat-rpm-config-9.1.0-Add-_pkgdocdir.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1324003
Patch39: redhat-rpm-config-9.1.0-find-requires-fix-detection.patch
# ppc64 little endian support
Patch99: redhat-rpm-config-9.1.0-ppc64le.patch
Patch100: redhat-rpm-config-9.1.0-centos.dist.patch

BuildArch: noarch
Requires: coreutils
Requires: perl-srpm-macros
Requires: rpm >= 4.9.0
Requires: dwz >= 0.4
Requires: zip
Provides: system-rpm-config = %{version}-%{release}

%description
CentOS specific rpm configuration files.

%prep
%setup -q
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
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1

%patch99 -p2
%patch100 -p1

%build

%install
make DESTDIR=${RPM_BUILD_ROOT} install
install -m 0444 %{SOURCE1} %{SOURCE2} ${RPM_BUILD_ROOT}/usr/lib/rpm/redhat
install -m 0755 %{SOURCE10} %{SOURCE11} ${RPM_BUILD_ROOT}/usr/lib/rpm/redhat
install -m 0755 %{SOURCE30} ${RPM_BUILD_ROOT}/usr/lib/rpm/redhat

install -D -m 0644 %{SOURCE20} ${RPM_BUILD_ROOT}/usr/lib/rpm/fileattrs/kabi.attr
install -m 0755 %{SOURCE21} ${RPM_BUILD_ROOT}/usr/lib/rpm/kabi.sh

find ${RPM_BUILD_ROOT} -name \*.orig -delete
# buggy makefile in 9.1.0 leaves changelog in wrong place
find ${RPM_BUILD_ROOT} -name ChangeLog -delete

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc ChangeLog
%{_prefix}/lib/rpm/redhat
%{_prefix}/lib/rpm/fileattrs/kabi.attr
%{_prefix}/lib/rpm//kabi.sh
%{_sysconfdir}/rpm/*

%changelog
* Thu Nov 03 2016 CentOS Sources <bugs@centos.org> - 9.1.0-72.el7.centos
- update check_rhl function in dist.sh

* Mon Aug 29 2016 Florian Festi <ffesti@redhat.com> - 9.1.0-72
- Rebuild for fixed _docdir_fmt

* Thu Jul 28 2016 Florian Festi <ffesti@redhat.com> - 9.1.0-71
- Set _docdir_fmt macro to old default (#1057327)

* Tue Jul 26 2016 Florian Festi <ffesti@redhat.com> - 9.1.0-70
- Be stricter with she bang lines in find-requires (#1179523)
- Use --with-cpu=power8 for ppc64le (#1213268)
- Fix stripping of binaries for changed file output (#1250015)
- Fix find-provides.libtool for new libtool style (#1061619)
- Restore UID/ GID on jar files (#1270053)
- Fix latest_kernel macro (#1323087)
- Add _pkgdocdir and _docdir_fmt macro (#1057327)
- Fix detection for perl files in old depencency generator (#1324003)

* Tue Dec 08 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 9.1.0-69
- Add aarch64 and ppc64le to ghc, ocaml, and GNAT arches (#1193178)

* Wed Nov 12 2014 Weiping Pan <wpan@redhat.com> - 9.1.0-68
- fix kabi path (#1126086)

* Tue Aug 12 2014 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-67
- Enable stack protector on aarch64 (#1073677)

* Fri Aug 01 2014 Florian Festi <ffesti@redhat.com> - 9.1.0-66
- use -mtune=power8 for ppc64le (#1123485)

* Fri Jul 25 2014 Florian Festi <ffesti@redhat.com> - 9.1.0-65
- Fix fix for ppc64le libtool issues (#1113618)
- As this package is noarch we need to have a runtime solution

* Thu Jul 24 2014 Florian Festi <ffesti@redhat.com> - 9.1.0-64
- Fix ppc64le libtool issues (#1113618)

* Tue Feb 18 2014 Weiping Pan <wpan@redhat.com> - 9.1.0-61
- use kverrel as the parameter for kmodtool (#1049175)

* Fri Feb 07 2014 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-62
- config.guess/sub don't need to be group-writable (#1061762)

* Tue Jan 21 2014 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-61
- Bump s390(x) up to -march=z196 (#805266)

* Fri Jan 10 2014 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-60
- Add %%_performance_build macro for enabling extra optimizations (#1051558)

* Tue Jan 07 2014 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-59
- Update config.{sub,guess} for ppc64p7 support (#1048751)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 9.1.0-58
- Mass rebuild 2013-12-27

* Thu Dec 19 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-57
- Switch from -fstack-protector to -fstack-protector-strong (#1040025)

* Thu Oct 03 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-56
- Drop accidentally added second -m32 switch from i686 build flags
- Use -mcpu=power7 for ppc and ppc64 builds (#789116)

* Thu Oct 03 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-55
- Add dependency generator for kABI provides (#1004930)
- Explicitly require rpm >= 4.9.0 for the above

* Sun Sep 22 2013 Weiping Pan <wpan@redhat.com> - 9.1.0-54
- Fix depmod path

* Fri Sep 13 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-53
- adjust ppc(64), s390(x) and i686 arch optflags as per #805266 and #789116

* Tue Aug 06 2013 Weiping Pan <wpan@redhat.com> - 9.1.0-52
- Fix permissions on /usr/lib/rpm/redhat/find-provides.d/modalias.prov

* Tue Jul 09 2013 Dan Horák <dhorak@redhat.com> - 9.1.0-51
- disable the s390 architecture build options (patch24) until new hardware is installed

* Tue Jul 09 2013 Dan Horák <dhorak@redhat.com> - 9.1.0-50
- fix s390 architecture build options as per #805266

* Tue Jul 09 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-49
- Re-add various kABI-related bits (Jon Masters)
- Allow kmod building against z-stream kernels (Jiri Benc)

* Mon Jul 08 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-48
- update s390 architecture build options as per #805266

* Fri Jul 05 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-47
- fix brp-java-repack-jars failing on strange permissions (#905573)

* Thu Jun 27 2013 Panu Matilainen <pmatilai@redhat.com> - - 9.1.0-46
- make cpu limit for building configurable through _smp_ncpus_max macro

* Tue May 21 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 9.1.0-45
- add nodejs_arches macro for ExclusiveArch for Node.js packages

* Mon May 13 2013 Adam Jackson <ajax@redhat.com> 9.1.0-44
- redhat-config-*: Use + to append rather than %%rename, to protect against
  multiple -specs= ending up in the command line. (#892837)

* Tue Apr 23 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-43
- Add optflags stack protector override for AArch64 (#909788)
- Also set FCFLAGS from %%configure (#914831)

* Mon Apr 22 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-42
- Switch back to manual config.guess/sub copies for reproducability
- Replace config.guess/sub from %%configure again (#951442)

* Mon Apr 22 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-41
- Add -grecord-gcc-switches to global CFLAGS (#951669)

* Mon Mar 25 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-40
- Add virtual system-rpm-config provide

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.0-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 9.1.0-38
- add ARM to ghc_arches_with_ghci for ghc-7.4.2 ghci support
  (NB this change should not be backported before ghc-7.4.2)

* Fri Nov  9 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 9.1.0-37
- Patch to fix spaces in java jar files
  https://bugzilla.redhat.com/show_bug.cgi?id=872737

* Fri Nov  9 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 9.1.0-36
- Patch to fix spaces in files used in filtering macros
  https://bugzilla.redhat.com/show_bug.cgi?id=783932

* Wed Oct  3 2012 Ville Skyttä <ville.skytta@iki.fi> - 9.1.0-35
- Drop (un)setting LANG and DISPLAY in build stages, require rpm >= 4.8.0.

* Wed Oct  3 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 9.1.0-34
- Add patch from https://bugzilla.redhat.com/show_bug.cgi?id=783433
  to fix spaces in files and directories that are fed to the
  brp-python-hardlink script
- Require zip since java repack jars requires it
  https://bugzilla.redhat.com/show_bug.cgi?id=857479
- Java jars need the MANIFEST.MF file to be first in the archive
  https://bugzilla.redhat.com/show_bug.cgi?id=465664
- Fix kernel_source macro to match the directory that kernel sources are installed in
  https://bugzilla.redhat.com/show_bug.cgi?id=648996
- Patch _mandir, _infodir, and _defaultocdir to use _prefix
  https://bugzilla.redhat.com/show_bug.cgi?id=853216

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-32
- enable minidebuginfo generation (#834073)

* Mon Jun 25 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-31
- revert back to plain -g, -g3 seems to cancel dwz size improvements

* Mon Jun 25 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-30
- require dwz, enable dwarf compression for debuginfo packages (#833311)

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 9.1.0-29
- Pull in dependency with macros specific for building Perl source packages

* Sat Mar  3 2012 Jens Petersen <petersen@redhat.com> - 9.1.0-28
- add s390 and s390x to ghc_arches

* Wed Feb 22 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-27
- add GNAT arch definitions

* Sun Jan 15 2012 Dennis Gilmore <dennis@ausil.us> - 9.1.0-26
- per ppc team request drop -mminimal-toc on ppc64

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-24
- add ghc_arches_with_ghci

* Wed Nov 09 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-23
- remove patch that forces --disable-silent-rules to configure 
- it breaks anything set to not ignore unknown configure options

* Tue Oct 18 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-22
- add armv5tel to ghc_arches

* Wed Sep 28 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-21
- build armv5tel on armv7l since they are the same abi armv7hl is 
- a incompatable ABI

* Wed Sep 28 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-20
- add armv7hl to ghc_arches

* Sun Sep 25 2011 Ville Skyttä <ville.skytta@iki.fi> - 9.1.0-19
- Fix URL.

* Thu Sep 22 2011 Adam Jackson <ajax@redhat.com> 9.1.0-18
- redhat-hardened-cc1: Inject -fPIE, not -fPIC.
  cf. http://lists.fedoraproject.org/pipermail/devel/2011-September/157365.html

* Fri Sep 16 2011 Adam Jackson <ajax@redhat.com> 9.1.0-17
- Expose %%_hardening_{c,ld}flags independently to make it easier for
  packages to apply them to selected components

* Wed Aug 10 2011 Colin Walters <walters@verbum.org> - 9.1.0-16
- Globally disable silent rules

* Wed Aug 03 2011 Adam Jackson <ajax@redhat.com> 9.1.0-15
- redhat-hardened-{cc1,ld}: Move some of the rewrite magic to gcc specs so
  we don't end up with both -fPIC and -fPIE on the command line

* Mon Aug 01 2011 Adam Jackson <ajax@redhat.com> 9.1.0-14
- redhat-rpm-config-9.1.0-hardened.patch: Add macro magic for %%_hardened_build

* Thu Jul 07 2011 Adam Jackson <ajax@redhat.com> 9.1.0-13
- redhat-rpm-config-9.1.0-relro.patch: LDFLAGS, not CFLAGS.

* Sat Jul 02 2011 Jon Masters <jcm@jonmasters.org> - 9.1.0-12
- redhat-rpm-config-9.1.0-arm.patch: Make armv7hl default on all v7 ARM

* Mon Jun 27 2011 Adam Jackson <ajax@redhat.com> - 9.1.0-11
- redhat-rpm-config-9.1.0-relro.patch: Add -Wl,-z,relro to __global_cflags

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-10
- revert last build since releng prefers exclusivearch here

* Sat Jun 18 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-9
- replace ghc_archs with ghc_excluded_archs

* Mon Jun 13 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-8
- add arm hardware float macros, fix up armv7l

* Mon May 30 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-7
- add -srpm to the arches files so that the base language macros can
  be parallel installable with these

* Fri May 27 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-6
- add some specific macros needed at srpm creation time

* Thu May 27 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-5
- adjust to new pkg-config behavior wrt private dependencies (#596433)

* Mon Mar 01 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-4
- avoid unnecessarily running brp-strip-comment-note (#568924)

* Mon Feb 15 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-3
- unbreak find-requires again, doh (#564527)

* Wed Feb 3 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-2
- python byte-compilation errors abort the build by default

* Tue Feb 2 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-1
- new version, lose merged patches (fixes #521141, #455279, #496522, #458648)
- require rpm for parent dir, version >= 4.6.0 for sane keyserver behavior
- buildrequire libtool to grab copies of config.guess and config.sub
- add URL to the git repo and upstream changelog as documentation

* Mon Nov 23 2009 Orion Poplawski <orion@cora.nwra.com> - 9.0.3-19
- Change configure macro to use _configure to allow override (bug #489942)

* Mon Sep 28 2009 Bill Nottingham <notting@redhat.com>
- Drop xz compression level to 2

* Thu Sep 03 2009 Adam Jackson <ajax@redhat.com>
- Delete *.orig in %%install

* Thu Sep 03 2009 Paul Howarth <paul@city-fan.org> 9.0.3-17
- redhat-rpm-config-9.0.3-filtering-macros.patch: Rediff so we don't ship a .orig file
- add (empty) %%build section
- fix unescaped macros in changelog

* Tue Aug 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 9.0.3-16
- add the filtering framework approved by the FPC/FESCo. (#516240)

* Thu Aug 13 2009 Adam Jackson <ajax@redhat.com> 9.0.3-15
- redhat-rpm-config-9.0.4-brpssa-speedup.patch: When looking for static
  archives, only run file(1) on files named *.a. (#517101)

* Wed Aug 12 2009 Adam Jackson <ajax@redhat.com> 9.0.3-14
- redhat-rpm-config-9.0.3-jars-with-spaces.patch: Handle repacking jars
  whose filenames contain spaces. (#461854)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Bill Nottingham <notting@redhat.com> 9.0.3-12
- use XZ payload compression for binary packages

* Tue Jul 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 9.0.3-10
- always delete %%buildroot as first step of %%install (as long as %%buildroot is not /)

* Fri Jul 17 2009 Bill Nottingham <notting@redhat.com> 9.0.3-10
- apply fedora 12 default buildflags

* Wed Jun 03 2009 Adam Jackson <ajax@redhat.com> 9.0.3-9
- limit-smp-16-threads.patch: Rediff so we don't ship a .orig file (#500316)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Jon Masters <jcm@redhat.com> - 9.0.3-7
- Change default hashing algorithm in file digests to SHA-256
- Resolves: #485826.

* Tue Feb 17 2009 Dennis Gilmore <dennis@ausil.us> - 9.0.3-6
- add missing armv7l arch  
- set the default build arch to match fedora arm build target

* Mon Feb 16 2009 Dennis Gilmore <dennis@ausil.us> - 9.0.3-5
- apply fedora 11 default buildflags
- set 32 bit intel build arch to i586 on compatiable hardware
- set 32 bit sparc build arch to sparcv9 on compatiable hardware

* Mon Feb 16 2009 Dennis Gilmore <dennis@ausil.us> - 9.0.3-4
- limit _smp_flags to -j16

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9.0.3-3
- fix license tag
- nuke ancient conflicts

* Mon Aug 11 2008 Panu Matilainen <pmatilai@redhat.com> - 9.0.3-2
- Unbreak find-requires (#443015)

* Tue May 06 2008 Jon Masters <jcm@redhat.com> - 9.0.3-1
- Ensure Java Jar files have readable files within.
- Remove overwritten config.guess|sub files (testing).
- Fix Fortran flags for building using _fmoddir.
- Pull in objdump fix to upstream find-requires.

* Thu Apr 03 2008 Jon Masters <jcm@redhat.com> - 9.0.2-1
- Remove smp dependencies
- Update config.guess|sub files
- Don't call find-requires.ksyms for kmod packages (kernel kABI scripts).

* Thu Jul 05 2007 Jesse Keating <jkeating@redhat.com> - 9.0.1-1
- Remove dist defines, fedora-release does that now
- Enable post-build buildroot checking by default

* Tue Jun 19 2007 Jeremy Katz <katzj@redhat.com> - 9.0.0-1
- use stock find-lang.sh (#213041)
- arm fixes (Lennert Buytenhek, #243523)
- allow jar repacking to be disabled (#219731)
- fix running dist.sh --fc (#223651)
- hardlink identical .pyc and .pyo files to save space (Ville Skyttä)
- fix TMPDIR usage (Matthew Miller, #235614)

* Tue Jun 19 2007 Jeremy Katz <katzj@redhat.com> - 8.1.0-1
- add modalias tags to kmod packages and other kmod changes (jcm)
- recompress jars to avoid multilib conflicts (bkonrath)

* Fri May 18 2007 Jesse Keating <jkeating@redhat.com> 8.0.45-16
- Update macros for F8
- hardcode dist in release string, as we provide it.  chicken/egg.

* Wed Apr 11 2007 Jon Masters <jcm@redhat.com> 8.0.45-15
- Add modalias tags to kernel module packages (kmods) for tracking.
- Further information is available at http://www.kerneldrivers.org/.

* Tue Apr 03 2007 Jon Masters <jcm@redhat.com> 8.0.45-14
- Rebased all previous patches (since java fix introduced offset).
- Added Fedora per-release macros to platforms section of macros.
  Further debate may see these move elsewhere in the ordering.

* Tue Mar 13 2007 Ben Konrath <bkonrath@redhat.com> 8.0.45-13
- Update brp-java-repack-jars to fix issue with tomcat. 

* Wed Oct 18 2006 Jon Masters <jcm@redhat.com> 8.0.45-12
- Synced kernel_module_package semantics with SuSE.
- Updated kmodtool.

* Tue Oct 17 2006 Jon Masters <jcm@redhat.com> 8.0.45-10
- Updated kernel_module_package.

* Mon Oct 16 2006 Jon Masters <jcm@redhat.com> 8.0.45-9
- Added kernel_module_package macro. Working on unified packaging.

* Thu Oct 12 2006 Jon Masters <jcm@redhat.com> 8.0.45-8
- Added patch for find-requires. Waiting on write access to public CVS.

* Tue Sep 12 2006 Deepak Bhole <dbhole@redhat.com> 8.0.45-6
- Fix brp-java-repack-jars to work with builddirs that aren't %%name-%%version

* Mon Sep 11 2006 Fernando Nasser <fnasser@redhat.com> - 8.0.45-5
- Fix order of tokens in find command (thanks mikeb@redhat.com)

* Thu Sep  7 2006 Ben Konrath <bkonrath@redhat.com> - 8.0.45-4
- Fix bug in repack jars script. 

* Wed Sep  6 2006 Jeremy Katz <katzj@redhat.com> - 8.0.45-3
- path fix

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 8.0.45-2
- Add script from Ben Konrath <bkonrath@redhat.com> to repack jars to 
  avoid multilib conflicts

* Sun Jul 30 2006 Jon Masters <jcm@redhat.com> - 8.0.45-1
- Fix inverted kernel test.

* Sun Jul 30 2006 Jon Masters <jcm@redhat.com> - 8.0.44-1
- Add a better check for a kernel vs. kmod.

* Thu Jun 15 2006 Jon Masters <jcm@redhat.com> - 8.0.43-1
- Workaround bug in find-requires/find-provides for kmods.

* Thu Jun 15 2006 Jon Masters <jcm@redhat.com> - 8.0.42-1
- Fix a typo in KMP find-requires.

* Tue Jun 13 2006 Jon Masters <jcm@redhat.com> - 8.0.41-1
- Add support for KMP Fedora Extras packaging.

* Fri Feb  3 2006 Jeremy Katz <katzj@redhat.com> - 8.0.40-1
- use -mtune=generic for x86 and x86_64

* Tue Aug 16 2005 Elliot Lee <sopwith@redhat.com> - 8.0.39-1
- Fix #165416

* Mon Aug 01 2005 Elliot Lee <sopwith@redhat.com> - 8.0.38-1
- Add -Wall into cflags

* Mon Aug 01 2005 Elliot Lee <sopwith@redhat.com> - 8.0.37-1
- Patch from Uli: enable stack protector, fix sparc & ppc cflags

* Thu Jun 16 2005 Elliot Lee <sopwith@redhat.com> - 8.0.36-1
- Fix the fix

* Wed Apr  6 2005 Elliot Lee <sopwith@redhat.com> - 8.0.35-1
- Fix #129025 (enable python byte compilation)

* Wed Mar 23 2005 Elliot Lee <sopwith@redhat.com> 8.0.34-1
- Bug fixes
- Cflags change by drepper

* Wed Feb 9 2005 Elliot Lee <sopwith@redhat.com> 8.0.33-1
- Change -D to -Wp,-D to make java happy
- Add -D_FORTIFY_SOURCE=2 to global cflags (as per Jakub & Arjan's request)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 8.0.32-1
- allow all symbol versioning in find_requires - matches RPM internal
  behavior

* Mon Jun 28 2004 Elliot Lee <sopwith@redhat.com> 8.0.31-1
- Add ppc8[25]60 to rpmrc optflags

* Fri Jun 25 2004 Elliot Lee <sopwith@redhat.com> 8.0.29-1
- rpmrc patch from jakub to change optflags.

* Wed Sep 17 2003 Elliot Lee <sopwith@redhat.com> 8.0.28-1
- Change brp-compress to pass -n flag to gzip (per msw's request)

* Tue Jul 15 2003 Elliot Lee <sopwith@redhat.com> 8.0.27-1
- Fix broken configure macro find for config.guess/config.sub
- Put host/target/build back for now

* Mon Jul  7 2003 Jens Petersen <petersen@redhat.com> - 8.0.26-1
- preserve the vendor field when VENDOR not set
- put VENDOR in the final i386-libc line, not the tentative one

* Mon Jul  7 2003 Jens Petersen <petersen@redhat.com> - 8.0.25-1
- update config.{guess,sub} to 2003-06-17
- define VENDOR to be redhat only when /etc/redhat-release present
  [suggested by jbj]
- put VENDOR in vendor field in our config.guess file for
  ia64, ppc, ppc64, s390, s390x, x86_64 and elf32-i386 Linux
- drop the --host, --build, --target and --program-prefix configure options
  from %%configure, since this causes far too many problems

* Fri May  2 2003 Jens Petersen <petersen@redhat.com> - 8.0.24-3
- make config.{guess,sub} executable

* Thu May  1 2003 Jens Petersen <petersen@redhat.com> - 8.0.22-2
- add config.guess and config.sub (2003-02-22) with s390 patch on config.sub
- make %%configure use them

* Mon Mar 03 2003 Elliot Lee <sopwith@redhat.com>
- Unset $DISPLAY in macros

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com> 8.0.21-1
- Just turn on -g unconditionally for now

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 8.0.20-1
- Reorganize rpmrc/macros to set cflags in a nicer manner.

* Wed Jan 22 2003 Elliot Lee <sopwith@redhat.com> 8.0.19-1
- Disable brp-implant-ident-static until it works everywhere

* Thu Jan 16 2003 Nalin Dahyabhai <nalin@redhat.com> 8.0.18-1
- add brp-implant-ident-static, which requires mktemp

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 8.0.17-1
- add brp-strip-static-archive from rpm-4.2-0.54

* Tue Dec 17 2002 Bill Nottingham <notting@redhat.com> 8.0.16-1
- make -g in rpmrc conditional on debug_package

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 8.0.15-1
- Rename -debug subpackages to -debuginfo

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 8.0.14-1
- tweak debug package stuff so that we are overloading %%install
  instead of %%post

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 8.0.13-1
- turn on internal rpm dep generation by default

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 8.0.12-1
- New release with debug packages on

* Tue Dec  3 2002 Bill Nottingham <notting@redhat.com> 8.0.8-1
- turn debug packages off
- override optflags with no -g

* Fri Nov 22 2002 Elliot Lee <sopwith@redhat.com> 8.0.7-1
- turn on debug packages

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 8.0.6-1
- Pass __strip and __objdump macros

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 8.0.5-1
- Update macros to specify find-provides/find-requires

* Thu Oct 31 2002 Elliot Lee <sopwith@redhat.com> 8.0.4-1
- Remove tracking dependency

* Wed Oct 16 2002 Phil Knirsch <pknirsch@redhat.com> 8.0.3-2
- Added fix for outdated config.[sub|guess] files in %%configure section

* Wed Oct 16 2002 Elliot Lee <sopwith@redhat.com> 8.0.3-1
- New release that blows up on unpackaged files and missing doc files.

* Thu Oct  3 2002 Jeremy Katz <katzj@redhat.com> 8.0.2
- don't redefine everything in macros, just what we need to

* Mon Sep 16 2002 Alexander Larsson <alexl@redhat.com> 8.0.1
- Add debug package support to %%__spec_install_post

* Tue Sep  3 2002 Bill Nottingham <notting@redhat.com> 8.0-1
- bump version

* Wed Aug 28 2002 Elliot Lee <sopwith@redhat.com> 7.3.94-1
- Update macrofiles

* Wed Jul 31 2002 Elliot Lee <sopwith@redhat.com> 7.3.93-1
- Add _unpackaged_files_terminate_build and 
_missing_doc_files_terminate_build to macros

* Thu Jul 11 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-6
- find-lang.sh fix from 67368
- find-requires fix from 67325

* Thu Jul 11 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-5
- Add /etc/rpm/macros back to make #67951 go away

* Wed Jun 26 2002 Jens Petersen <petersen@redhat.com> 7.3.92-4
- fix %%configure targeting for autoconf-2.5x (#58468)
- include ~/.rpmmacros in macrofiles file path again

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 7.3.92-3
- automated rebuild

* Fri Jun 21 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-2
- Don't define _arch

* Thu Jun 20 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-1
- find-lang error detection from Havoc

* Wed Jun 12 2002 Elliot Lee <sopwith@redhat.com> 7.3.91-1
- Update

* Sun Jun  9 2002 Jeff Johnson <jbj@redhat.com>
- create.
