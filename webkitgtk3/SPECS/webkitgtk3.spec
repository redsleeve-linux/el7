# Fix rebuild on non-Fedora
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global         add_to_doc_files()      \
        mkdir -p %{buildroot}%{_pkgdocdir} ||: ; \
        cp -p %1  %{buildroot}%{_pkgdocdir}/$(echo '%1' | sed -e 's!/!.!g')

# Enable higher compression for output rpms
# https://bugzilla.redhat.com/show_bug.cgi?id=1039590
%define _binary_payload w8.xzdio

Name:           webkitgtk3
Version:        2.4.9
Release:        6%{?dist}
Summary:        GTK+ Web content engine library

Group:          Development/Libraries
License:        LGPLv2+ and BSD
URL:            http://www.webkitgtk.org/

Source0:        http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz

Patch0:         webkit-1.1.14-nspluginwrapper.patch
Patch1:         webkitgtk-aarch64.patch
Patch2:         webkitgtk-2.4.1-cloop_fix.patch
Patch3:         webkitgtk-2.4.5-cloop_fix_32.patch
Patch4:         webkitgtk-2.4.1-ppc64_align.patch
Patch5:         webkitgtk-2.4.9-translations.patch
Patch6:         webkitgtk-2.4.9-disable_deprecated_get_set_id.patch
# http://trac.webkit.org/changeset/169665
Patch7:         webkitgtk-2.4.9-sql_initialize_string.patch

BuildRequires:  at-spi2-core-devel
BuildRequires:  bison
BuildRequires:  cairo-devel
BuildRequires:  chrpath
BuildRequires:  enchant-devel
BuildRequires:  flex
BuildRequires:  fontconfig-devel >= 2.5
BuildRequires:  freetype-devel
BuildRequires:  geoclue2-devel
BuildRequires:  gettext
BuildRequires:  gperf
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel >= 3.6
BuildRequires:  gtk-doc
BuildRequires:  glib2-devel >= 2.36.0
BuildRequires:  harfbuzz-devel
BuildRequires:  libsoup-devel >= 2.42.0
BuildRequires:  libicu-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libsecret-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxslt-devel
BuildRequires:  libXt-devel
BuildRequires:  pcre-devel
BuildRequires:  sqlite-devel
BuildRequires:  gobject-introspection-devel >= 1.32.0
BuildRequires:  perl-Switch
BuildRequires:  ruby
BuildRequires:  mesa-libGL-devel
%ifarch ppc
BuildRequires:  libatomic
%endif
Requires:       geoclue2

%description
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

This package contains WebKitGTK+ for GTK+ 3.

%package -n     libwebkit2gtk
Summary:        The libwebkit2gtk library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       geoclue2

%description -n libwebkit2gtk
The libwebkit2gtk package contains the libwebkit2gtk library
that is part of %{name}.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       gtk3-devel
Requires:       libwebkit2gtk%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains developer documentation for %{name}.

%prep
%setup -qn "webkitgtk-%{version}"
%patch0 -p1 -b .nspluginwrapper
%patch1 -p1 -b .aarch64
%patch2 -p1 -b .cloop_fix
%patch5 -p1 -b .translations
%patch6 -p1 -b .disable_deprecated_get_id
%patch7 -p1 -b .sql_initialize_string
%ifarch ppc s390
%patch3 -p1 -b .cloop_fix_32
%endif
%ifarch %{power64} aarch64 ppc
%patch4 -p1 -b .ppc64_align
%endif

# Fix the permissions
chmod 644 Source/WebCore/html/canvas/CanvasRenderingContext2D.cpp

%build
%global optflags %{optflags} -fno-strict-aliasing

# Use linker flags to reduce memory consumption
%global optflags %{optflags} -Wl,--no-keep-memory -Wl,--reduce-memory-overheads

%ifarch s390 %{arm}
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

%ifarch ppc
# Use linker flag -relax to get WebKit2 build under ppc(32) with JIT disabled
%global optflags %{optflags} -Wl,-relax -latomic
%endif

%ifarch s390 s390x ppc %{power64} aarch64
%global optflags %{optflags} -DENABLE_YARR_JIT=0
%endif

%configure                                      \
        --with-gtk=3.0                          \
%ifarch s390 s390x ppc %{power64} aarch64
        --disable-jit                           \
%else
        --enable-jit                            \
%endif
        --enable-introspection

mkdir -p DerivedSources/webkit
mkdir -p DerivedSources/WebCore
mkdir -p DerivedSources/ANGLE
mkdir -p DerivedSources/WebKit2
mkdir -p DerivedSources/webkitdom/
mkdir -p DerivedSources/InjectedBundle
mkdir -p DerivedSources/Platform

# Disable the parallel compilation as it fails to compile in brew.
# https://bugs.webkit.org/show_bug.cgi?id=34846
# make -j1 V=1
make %{_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}

install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -m 755 Programs/GtkLauncher %{buildroot}%{_libexecdir}/%{name}
install -m 755 Programs/MiniBrowser %{buildroot}%{_libexecdir}/%{name}

# Remove lib64 rpaths
chrpath --delete %{buildroot}%{_bindir}/jsc-3
chrpath --delete %{buildroot}%{_libdir}/libwebkitgtk-3.0.so
chrpath --delete %{buildroot}%{_libdir}/libwebkit2gtk-3.0.so
chrpath --delete %{buildroot}%{_libexecdir}/%{name}/GtkLauncher
chrpath --delete %{buildroot}%{_libexecdir}/%{name}/MiniBrowser
chrpath --delete %{buildroot}%{_libexecdir}/WebKitNetworkProcess
chrpath --delete %{buildroot}%{_libexecdir}/WebKitPluginProcess
chrpath --delete %{buildroot}%{_libexecdir}/WebKitWebProcess

# Remove .la files
find $RPM_BUILD_ROOT%{_libdir} -name "*.la" -delete

%find_lang WebKitGTK-3.0

## Finally, copy over and rename the various files for %%doc inclusion.
%add_to_doc_files Source/WebKit/LICENSE
%add_to_doc_files Source/WebKit/gtk/NEWS
%add_to_doc_files Source/WebCore/icu/LICENSE
%add_to_doc_files Source/WebCore/LICENSE-APPLE
%add_to_doc_files Source/WebCore/LICENSE-LGPL-2
%add_to_doc_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_doc_files Source/JavaScriptCore/COPYING.LIB
%add_to_doc_files Source/JavaScriptCore/THANKS
%add_to_doc_files Source/JavaScriptCore/AUTHORS
%add_to_doc_files Source/JavaScriptCore/icu/README
%add_to_doc_files Source/JavaScriptCore/icu/LICENSE

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n libwebkit2gtk -p /sbin/ldconfig
%postun -n libwebkit2gtk -p /sbin/ldconfig

%files -f WebKitGTK-3.0.lang
%doc %{_pkgdocdir}/
%{_libdir}/libwebkitgtk-3.0.so.*
%{_libdir}/libjavascriptcoregtk-3.0.so.*
%{_libdir}/girepository-1.0/WebKit-3.0.typelib
%{_libdir}/girepository-1.0/JavaScriptCore-3.0.typelib
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/GtkLauncher
%{_datadir}/webkitgtk-3.0

%files -n libwebkit2gtk
%{_libdir}/libwebkit2gtk-3.0.so.*
%{_libdir}/webkit2gtk-3.0/
%{_libdir}/girepository-1.0/WebKit2-3.0.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-3.0.typelib
%{_libexecdir}/%{name}/MiniBrowser
%{_libexecdir}/WebKitNetworkProcess
%{_libexecdir}/WebKitPluginProcess
%{_libexecdir}/WebKitWebProcess

%files  devel
%{_bindir}/jsc-3
%{_includedir}/webkitgtk-3.0
%{_libdir}/libwebkitgtk-3.0.so
%{_libdir}/libwebkit2gtk-3.0.so
%{_libdir}/libjavascriptcoregtk-3.0.so
%{_libdir}/pkgconfig/webkitgtk-3.0.pc
%{_libdir}/pkgconfig/webkit2gtk-3.0.pc
%{_libdir}/pkgconfig/webkit2gtk-web-extension-3.0.pc
%{_libdir}/pkgconfig/javascriptcoregtk-3.0.pc
%{_datadir}/gir-1.0/WebKit-3.0.gir
%{_datadir}/gir-1.0/WebKit2-3.0.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-3.0.gir
%{_datadir}/gir-1.0/JavaScriptCore-3.0.gir

%files doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/webkitgtk
%{_datadir}/gtk-doc/html/webkit2gtk
%{_datadir}/gtk-doc/html/webkitdomgtk

%changelog
* Thu Jun 23 2016 Tomas Popela <tpopela@redhat.com> - 2.4.9-6
- Update the translations
- Resolves: rhbz#1302692

* Mon Sep 14 2015 Tomas Popela <tpopela@redhat.com> - 2.4.9-5
- Initialize string in SQLiteStatement before using it
- Resolves: rhbz#1259283

* Mon Jun 22 2015 Tomas Popela <tpopela@redhat.com> - 2.4.9-4
- Remove deprecation from webkit_dom_html_element_get/set_id
- Resolves: rhbz#1174556

* Fri May 29 2015 Tomas Popela <tpopela@redhat.com> - 2.4.9-3
- Fix some of rpmdiff warnings
- Resolves: rhbz#1174556

* Thu May 21 2015 Tomas Popela <tpopela@redhat.com> - 2.4.9-2
- Compile with -fno-strict-aliasing
- Resolves: rhbz#1174556
- Update translations
- Resolves: rhbz#1223643

* Wed May 20 2015 Tomas Popela <tpopela@redhat.com> - 2.4.9-1
- Update to 2.4.9
- Resolves: rhbz#1174556

* Wed Aug 20 2014 Dan Horák <dhorak@redhat.com> - 2.0.4-9
- refresh ppc64le patch, use %%{power64} for conditions in spec
- Resolves: rhbz#1125710

* Mon Aug 04 2014 Tomas Popela <tpopela@redhat.com> - 2.0.4-8
- Add support for ppc64le
- Resolves: rhbz#1125710

* Mon May 12 2014 Tomas Popela <tpopela@redhat.com> - 2.0.4-7
- Fix memory align in JSC for ppc64
- Fix CLoop for ppc64 and s390x
- Resolves: rhbz#1019801

* Tue Jan 28 2014 Tomas Popela <tpopela@redhat.com> - 2.0.4-6
- Enable higher compression for output rpms
- Resolves: rhbz#1039590
- Avoid video player to set system volume to 100%
- Resolves: rhbz#1029783

* Tue Jan 28 2014 Tomas Popela <tpopela@redhat.com> - 2.0.4-5
- Update translations
- Resolves: rhbz#1030388

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.0.4-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0.4-3
- Mass rebuild 2013-12-27

* Tue Nov 5 2013 Tomas Popela <tpopela@redhat.com> - 2.0.4-2
- Let webkitgtk3 compile on aarch64
- Resolves: rhbz#1026479

* Wed Oct 2 2013 Tomas Popela <tpopela@redhat.com> - 2.0.4-1
- Update to 2.0.4
- Resolves: rhbz#1013726

* Tue Jun 11 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.3-1
- Update to 2.0.3

* Fri Jun 07 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.2-3
- Link with harfbuzz-icu (split into separate library in harfbuzz 0.9.18)

* Mon Jun 03 2013 Kalev Lember <kalevlember@gmail.com> - 2.0.2-2
- Remove glib-compile-schemas scriptlets: the schemas are no longer installed
- Add ldconfig calls to the libwebkit2gtk subpackage
- Remove rpath from MiniBrowser
- Re-enable full debuginfo (#861452)

* Mon May 13 2013 Tomas Popela <tpopela@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Mon May  6 2013 Matthias Clasen <mclasen@redhat.com> - 2.0.1-2
- Split libwebkit2gtk off into a subpackage to avoid
  pulling this 35M behemoth of a library onto the livecd
  needlessly

* Tue Apr 16 2013 Tomas Popela <tpopela@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Thu Apr 11 2013 Tomas Popela <tpopela@redhat.com> - 2.0.0-3
- Add fix for broken GObject casting

* Wed Apr 3 2013 Tomas Popela <tpopela@redhat.com> - 2.0.0-2
- Apply double2intsPPC32.patch also on s390

* Wed Mar 27 2013 Tomas Popela <tpopela@redhat.com> - 2.0.0-1
- Update to 2.0.0
- Update BR versions
- Drop unused patches

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.11.92-1
- Update to 1.11.92

* Fri Mar 08 2013 Tomas Popela <tpopela@redhat.com> 1.11.91-1
- Update to 1.11.91
- Fix for RH bug #915990 - Seed segfaults in JSC::LLInt::CLoop::execute()

* Mon Feb 25 2013 Tomas Popela <tpopela@redhat.com> 1.11.90-3
- Fix for not building on ppc32 with JIT disabled

* Sat Feb 23 2013 Kevin Fenzi <kevin@scrye.com> 1.11.90-2
- Add webkit2 MiniBrowser

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 1.11.90-1
- Update to 1.11.90

* Fri Feb 22 2013 Tomas Popela <tpopela@redhat.com> 1.11.5-5
- Fix for not building on ppc32 with JIT disabled
- BR libatomic (needs gcc >= 4.8.0) for ppc32

* Mon Feb 18 2013 Tomas Popela <tpopela@redhat.com> 1.11.5-4
- Backported fixes for not building with disabled JIT

* Sat Feb 16 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.11.5-3
- Re-enable JIT on ARM (hopefully the gmail crash is fixed)

* Thu Feb 14 2013 Tomas Popela <tpopela@redhat.com> 1.11.5-2
- Add upstream patch for RH bug #908143 - AccessibilityTableRow::parentTable crash

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 1.11.5-1
- Update to 1.11.5
- Drop upstreamed patches

* Wed Jan 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.4-5
- Rebuild against new icu again

* Sat Jan 26 2013 Kalev Lember <kalevlember@gmail.com> - 1.11.4-4
- Rebuilt for icu 50

* Fri Jan 25 2013 Kalev Lember <kalevlember@gmail.com> - 1.11.4-3
- Backport a fix for a crash in AccessibilityTableCell::parentTable()

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.11.4-2
- rebuild due to "jpeg8-ABI" feature drop

* Wed Jan 16 2013 Kalev Lember <kalevlember@gmail.com> - 1.11.4-1
- Update to 1.11.4
- Remove conditional pango deps; the build now uses harfbuzz directly
- BR libwebp-devel
- Drop upstreamed librt linking patch

* Tue Dec 18 2012 Dan Horák <dan[at]danny.cz> - 1.11.2-3
- fix 32-bit non-JIT arches

* Tue Dec 18 2012 Dan Horák <dan[at]danny.cz> - 1.11.2-2
- fix build for non-JIT arches

* Sat Nov 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.11.2-1
- Update to 1.11.2
- Add a patch to explicitly link with librt

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.1-1
- Update to 1.10.1
- Enable the parallel build
- Drop the upstreamed Geode-compatibility patch

* Fri Oct  5 2012 Daniel Drake <dsd@laptop.org> - 1.10.0-2
- Restore compatibility with AMD Geode processors

* Mon Sep 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.0-1
- Update to 1.10.0
- Adjust for webkit -> webkitgtk upstream tarball rename

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.92-2
- Build with gstreamer1

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.92-1
- Update to 1.9.92

* Wed Sep 05 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.91-1
- Update to 1.9.91

* Sun Sep  2 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.90-2
- Rebuild

* Wed Aug 29 2012 Daniel Drake <dsd@laptop.org> - 1.9.90-1
- Update to latest release (#850520)

* Thu Aug  9 2012 Daniel Drake <dsd@laptop.org> - 1.9.5-2
- Add upstream patch to fix build without JIT (#843428)
- Add upstream patch to fix build with latest gcc/bison

* Wed Jul 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.5-1
- Update to 1.9.5
- Build with -g1 to avoid running into 4 GB ar format limit

* Wed Jul 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.9.4-3
- Fix %%post scriptlet dependencies.

* Wed Jul 04 2012 Dan Horák <dan[at]danny.cz> - 1.9.4-2
- apply workaround for s390x until #835957 is resolved (static library archive > 4 GB)

* Thu Jun 28 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.4-1
- Update to 1.9.4

* Thu Jun 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.3-1
- Update to 1.9.3
- Build webkit2gtk and BR gtk2-devel for its plugin process

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 1.8.1-3
- disable JIT on PPC(64) as the autodetection enables it even if not supported

* Mon May 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.1-2
- Explicitly disable JIT on ARM as it's not currently stable with JS heavy pages

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.1-1
- Update to 1.8.1
- Dropped the backported patches
- Remove lib64 rpaths with chrpath
- Update gsettings rpm scriptlets

* Wed Apr 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.0-3
- Add upstream patch to fix crash when SSE2 isn't present
- Add upstream patch to flickering when some widgets are drawn

* Mon Apr 09 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.0-2
- Finish splitting out a -doc subpackage (#808917)

* Wed Mar 28 2012 Richard Hughes <rhughes@redhat.com> - 1.8.0-1
- Update to 1.8.0.

* Sat Mar 24 2012 Dan Horák <dan[at]danny.cz> - 1.7.92-2
- add ppc to low mem arches
- decrease debuginfo verbosity on s390 to save memory

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 1.7.92-1
- Update to 1.7.92
- Don't pass --enable-geolocation to configure; it's now enabled by default

* Thu Mar 15 2012 Karsten Hopp <karsten@redhat.com> 1.7.91-2
- disable jit on ppc(64)

* Thu Mar  8 2012 Matthias Clasen <mclasen@redhat.com> - 1.7.91-1
- Update to 1.7.91

* Tue Feb 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.5-3
- Add ARM to and optimise compile flags for low mem arches

* Mon Feb 20 2012 Dan Horák <dan[at]danny.cz> - 1.7.5-2
- don't enable jit on s390(x)

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 1.7.5-1
- Update to 1.7.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.3-1
- Update to 1.7.3

* Thu Nov 24 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Mon Nov 7 2011 Matthias Clasen <mclasen@redhat.com> 1.7.1-2
- Rebuild against new libpng

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> 1.7.1-1
- Update to 1.7.1

* Wed Oct 12 2011 Dan Horák <dan[at]danny.cz> 1.6.1-2
- fix build on s390(x)

* Wed Sep 28 2011 Ray Strode <rstrode@redhat.com> 1.6.1-1
- Update to 1.6.1

* Fri Sep 09 2011 Caolán McNamara <caolanm@redhat.com> - 1.5.1-2
- rebuild for icu 4.8.1

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Tue Jun 14 2011 Bastien Nocera <bnocera@redhat.com> 1.4.0-3
- Rebuild against newer GTK+

* Wed May 11 2011 Cosimo Cecchi <cosimoc@redhat.com> 1.4.0-2
- Add a doc package for gtk-doc documentation

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> 1.4.0-1
- Update to 1.4.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> 1.3.13-1
- Update to 1.3.13

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 1.3.10-3
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 1.3.11-1
- 1.3.11

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 1.3.10-2
- Rebuild against newer gtk

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 1.3.10-1
- Update to 1.3.10

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 1.3.9-1
- Update to 1.3.9

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 1.3.7-2
- Rebuild against new gtk

* Wed Dec  1 2010 Matthias Clasen <mclasen@redhat.com> 1.3.7-1
- Update to 1.3.7

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> 1.3.6-1
- Update to 1.3.6
- Disable the s390 patch again :-( Upstream it, maybe ?

* Thu Nov 11 2010 Dan Horák <dan[at]danny.cz> - 1.3.5-2
- Updated and re-enabled the s390 patch

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> 1.3.5-1
- Update to 1.3.5

* Wed Sep 29 2010 jkeating - 1.3.4-3
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Matthias Clasen <mclasen@redhat.com> 1.3.4-2
- Enable JIT/patch for execmem
- Move inspector to the main package

* Thu Sep 23 2010 Matthias Clasen <mclasen@redhat.com> 1.3.4-1
- Update to 1.3.4

* Wed Aug 25 2010 Dan Horák <dan[at]danny.cz> - 1.3.3-4
- Do not generate debug information to prevent linker memory exhaustion on s390 with its 2 GB address space

* Wed Jul 21 2010 Dan Horák <dan[at]danny.cz> - 1.3.3-3
- Fix build on s390(x)

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 1.3.3-2
- Rebuild with new gobject-introspection

* Fri Jul  9 2010 Matthias Clasen <mclasen@redhat.com> 1.3.2-2
- Fix conflicting gettext domain with webkitgtk
- Drop the -doc subpackage

* Thu Jul  1 2010 Matthias Clasen <mclasen@redhat.com> 1.3.2-1
- Initial packaging
