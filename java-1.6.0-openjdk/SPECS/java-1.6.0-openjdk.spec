# If gcjbootstrap is 1 IcedTea is bootstrapped against
# java-1.5.0-gcj-devel.  If gcjbootstrap is 0 IcedTea is built against
# java-1.6.0-openjdk-devel.
%define gcjbootstrap 0

# If debug is 1, IcedTea is built with all debug info present.
%define debug 0


%define icedteaver 1.13.12
%define icedteasnapshot %{nil}
%define openjdkver 40
%define openjdkdate 22_aug_2016

%define genurl http://cvs.fedoraproject.org/viewcvs/devel/java-1.6.0-openjdk/

%define icedteaurl http://icedtea.classpath.org/

%define accessmajorver 1.23
%define accessminorver 0
%define accessver %{accessmajorver}.%{accessminorver}
%define accessurl http://ftp.gnome.org/pub/GNOME/sources/java-access-bridge/

%define openjdkurl https://java.net/downloads/openjdk6/
%define rhelzip  openjdk-6-src-b%{openjdkver}-%{openjdkdate}-rhel.tar.xz

%define multilib_arches ppc64 sparc64 x86_64

%define jit_arches %{ix86} x86_64 sparcv9 sparc64

%ifarch x86_64
%define archbuild amd64
%define archinstall amd64
%endif
%ifarch ppc
%define archbuild ppc
%define archinstall ppc
%endif
%ifarch ppc64
%define archbuild ppc64
%define archinstall ppc64
%endif
%ifarch i386
%define archbuild i586
%define archinstall i386
%endif
%ifarch i686
%define archbuild i586
%define archinstall i386
%endif
%ifarch ia64
%define archbuild ia64
%define archinstall ia64
%endif
%ifarch s390
%define archbuild s390x
%define archinstall s390x
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%define archbuild sparc
%define archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%define archbuild sparcv9
%define archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%define archbuild %{_arch}
%define archinstall %{_arch}
%endif

%if %{debug}
%define debugbuild icedtea-debug-against-icedtea
%else
%define debugbuild %{nil}
%endif

%if %{debug}
%define buildoutputdir openjdk.build-debug
%else
%define buildoutputdir openjdk.build
%endif

%if %{gcjbootstrap}
%define icedteaopt %{nil}
%else
%define icedteaopt --with-jdk-home=/usr/lib/jvm/%{sdklnk}
%endif

%ifarch %{jit_arches}
%define stapopt --enable-systemtap
%define bootstrapopt %{nil}
%else
%define stapopt %{nil}
%define bootstrapopt --disable-bootstrap
%endif

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%define script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%define abs2rel %{__perl} -e %{script}

# Hard-code libdir on 64-bit architectures to make the 64-bit JDK
# simply be another alternative.
%ifarch %{multilib_arches}
%define syslibdir       %{_prefix}/lib64
%define _libdir         %{_prefix}/lib
%define archname        %{name}.%{_arch}
%else
%define syslibdir       %{_libdir}
%define archname        %{name}
%endif

# Standard JPackage naming and versioning defines.
%define origin          openjdk
%define priority        16000
%define javaver         1.6.0
%define buildver        %{openjdkver}

# Standard JPackage directories and symbolic links.
# Make 64-bit JDKs just another alternative on 64-bit architectures.
%ifarch %{multilib_arches}
%define sdklnk          java-%{javaver}-%{origin}.%{_arch}
%define jrelnk          jre-%{javaver}-%{origin}.%{_arch}
%define sdkdir          %{name}-%{version}.%{_arch}
%else
%define sdklnk          java-%{javaver}-%{origin}
%define jrelnk          jre-%{javaver}-%{origin}
%define sdkdir          %{name}-%{version}
%endif
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%ifarch %{multilib_arches}
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}.%{_arch}
%else
%define jvmjardir       %{_jvmjardir}/%{name}-%{version}
%endif

%ifarch %{jit_arches}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
#%define tapsetdir	/usr/share/systemtap/tapset/%{sdkdir}
%define tapsetdir	/usr/share/systemtap/tapset/%{_build_cpu}
%endif

# Prevent brp-java-repack-jars from being run.
%define __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{buildver}
Release: %{icedteaver}.9%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons,
# and this change was brought into RHEL-4.  java-1.5.0-ibm packages
# also included the epoch in their virtual provides.  This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0".  In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0.  So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages.  Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".
Epoch:   1
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

License:  ASL 1.1, ASL 2.0, GPL+, GPLv2, GPLv2 with exceptions, LGPL+, LGPLv2, MPLv1.0, MPLv1.1, Public Domain, W3C
URL:      http://icedtea.classpath.org/
Source0:  %{icedteaurl}download/source/icedtea6-%{icedteaver}%{icedteasnapshot}.tar.xz
# To generate, download OpenJDK tarball from %{openjdkurl},
# and run %{SOURCE3} on the tarball.
Source1:  %{rhelzip}
Source2:  %{accessurl}%{accessmajorver}/java-access-bridge-%{accessver}.tar.bz2
Source3:  %{genurl}generate-rhel-zip.sh
Source4:  README.src

# Pre-2009 changelog, retained to ensure contributions are not lost
SOURCE900: pre-2009-spec-changelog

# FIXME: This patch needs to be fixed. optflags argument
# -mtune=generic is being ignored because it breaks several graphical
# applications.
Patch0:   java-1.6.0-openjdk-optflags.patch
Patch1:   java-1.6.0-openjdk-java-access-bridge-tck.patch
Patch2:   java-1.6.0-openjdk-java-access-bridge-idlj.patch
Patch3:	  java-1.6.0-openjdk-java-access-bridge-security.patch
Patch4:   java-1.6.0-openjdk-accessible-toolkit.patch
Patch5:   java-1.6.0-openjdk-debugdocs.patch
Patch6:   %{name}-debuginfo.patch
# This turns off the application of PR2125 by fsg.sh as
# we do it ourselves ahead of time via generate-rhel-zip.sh
Patch7:  no_pr2125.patch
# This is a RHEL-specific patch to embed RHEL-specific paths
Patch10:  add-final-location-rpaths.patch
# PR2808, RH1302383: Backport "8076221: Disable RC4 cipher suites"
Patch12: pr2808.patch
# PR2849: wget not required when downloading is disabled
Patch13: pr2849.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: giflib-devel
BuildRequires: libcap-devel
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXp-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: ant
BuildRequires: libXinerama-devel
BuildRequires: rhino
# Provides lsb_release for generating identification
BuildRequires: redhat-lsb-core
%if %{gcjbootstrap}
BuildRequires: java-1.5.0-gcj-devel
BuildRequires: libxslt
%else
BuildRequires: java-1.6.0-openjdk-devel >= 1.6.0.40
%endif
# Java Access Bridge for GNOME build requirements.
BuildRequires: at-spi-devel
BuildRequires: gawk
BuildRequires: libbonobo-devel
BuildRequires: pkgconfig >= 0.9.0
BuildRequires: xorg-x11-utils
# PulseAudio build requirements.
BuildRequires: pulseaudio-libs-devel >= 0.9.11
BuildRequires: pulseaudio >= 0.9.11
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif

# cacerts build requirement.
BuildRequires: openssl
# execstack build requirement.
BuildRequires: prelink
%ifarch %{jit_arches}
#systemtap build requirement.
BuildRequires: systemtap-sdt-devel
%endif
# configure looks for /etc/mime.types
# to provide the JDK symlink
BuildRequires: mailcap

Requires: fontconfig
Requires: libjpeg = 6b
# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require /etc/mime.types
Requires: mailcap
# Require jpackage-utils for ant.
Requires: jpackage-utils >= 1.7.3-1jpp.2
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage base provides.
Provides: jre6-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre6-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre6-%{javaver} = %{epoch}:%{version}-%{release}
Provides: java6-%{javaver} = %{epoch}:%{version}-%{release}
Provides: jre6 = %{javaver}
Provides: java6-%{origin} = %{epoch}:%{version}-%{release}
Provides: java6 = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: jndi6 = %{epoch}:%{version}
Provides: jndi6-ldap = %{epoch}:%{version}
Provides: jndi6-cos = %{epoch}:%{version}
Provides: jndi6-rmi = %{epoch}:%{version}
Provides: jndi6-dns = %{epoch}:%{version}
Provides: jaas6 = %{epoch}:%{version}
Provides: jsse6 = %{epoch}:%{version}
Provides: jce6 = %{epoch}:%{version}
Provides: jdbc6-stdext = 3.0
Provides: java6-sasl = %{epoch}:%{version}
Provides: java6-fonts = %{epoch}:%{version}

# No means to bootstrap these architectures
ExcludeArch: aarch64 ppc64le

%description
The OpenJDK runtime environment.

%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

# Require base package.
Requires:         %{name} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage devel provides.
Provides: java6-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides: java6-sdk-%{javaver} = %{epoch}:%{version}
Provides: java6-sdk-%{origin} = %{epoch}:%{version}
Provides: java6-sdk = %{epoch}:%{javaver}
Provides: java6-%{javaver}-devel = %{epoch}:%{version}
Provides: java6-devel-%{origin} = %{epoch}:%{version}
Provides: java6-devel = %{epoch}:%{javaver}


%description devel
The OpenJDK development tools.

%package demo
Summary: OpenJDK Demos
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description demo
The OpenJDK demos.

%package src
Summary: OpenJDK Source Bundle
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description src
The OpenJDK source bundle.

%package javadoc
Summary: OpenJDK API Documentation
Group:   Documentation

# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# Postun requires alternatives to uninstall javadoc alternative.
Requires(postun): %{_sbindir}/alternatives

# Standard JPackage javadoc provides.
Provides: java6-javadoc = %{epoch}:%{version}-%{release}
Provides: java6-%{javaver}-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
The OpenJDK API documentation.

%prep
%setup -q -n icedtea6-%{icedteaver}%{icedteasnapshot}
%setup -q -n icedtea6-%{icedteaver}%{icedteasnapshot} -T -D -a 2
%patch0
%patch7 -p1
%patch10 -p1
%patch12 -p1
%patch13 -p1

cp %{SOURCE4} .

%build
# How many cpu's do we have?
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}


# Build IcedTea and OpenJDK.
%ifarch sparc64 alpha
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif
./autogen.sh
%configure %{bootstrapopt} --prefix=%{_jvmdir}/%{sdkdir} --exec-prefix=%{_jvmdir}/%{sdkdir} \
  --bindir=%{_jvmdir}/%{sdkdir}/bin --includedir=%{_jvmdir}/%{sdkdir}/include \
  --docdir=%{_defaultdocdir}/%{name} --mandir=%{_jvmdir}/%{sdkdir}/man \
  --htmldir=%{_javadocdir}/%{name} %{icedteaopt} %{stapopt} --with-openjdk-src-zip=%{SOURCE1} \
  --with-pkgversion=rhel-%{release}-%{_arch} --enable-pulse-java \
  --with-abs-install-dir=%{_jvmdir}/%{sdkdir} --disable-downloading \
  --with-rhino --with-parallel-jobs=$NUM_PROC --disable-lcms2 \
  --disable-tests --disable-systemtap-tests

make DISTRIBUTION_PATCHES="patches/add-final-location-rpaths.patch patches/openjdk/8076221-pr2808-disable_rc4_cipher_suites.patch patches/openjdk/8078823-disabledalgorithms_fails_intermittently.patch patches/pr2808-fix_disabled_algorithms_test.patch" patch

patch -l -p0 < %{PATCH3}
patch -l -p0 < %{PATCH4}

%if %{debug}
patch -l -p0 < %{PATCH5}
patch -l -p0 < %{PATCH6}
%endif

make %{debugbuild} INSTALL_LOCATION="%{_jvmdir}/%{sdkdir}"

%ifarch %{jit_arches}
chmod 644 $(pwd)/%{buildoutputdir}/j2sdk-image/lib/sa-jdi.jar
%endif

export JAVA_HOME=$(pwd)/%{buildoutputdir}/j2sdk-image

# Build Java Access Bridge for GNOME.
pushd java-access-bridge-%{accessver}
  patch -l -p1 < %{PATCH1}
  patch -l -p1 < %{PATCH2}
  OLD_PATH=$PATH
  export PATH=$JAVA_HOME/bin:$OLD_PATH
  ./configure
  make
  export PATH=$OLD_PATH
  cp -a bridge/accessibility.properties $JAVA_HOME/jre/lib
  chmod 644 gnome-java-bridge.jar
  cp -a gnome-java-bridge.jar $JAVA_HOME/jre/lib/ext
popd

%check

# Should be 'make check' but IcedTea 1.13.x doesn't support disabling SystemTap tests
# Enable when we switch to 1.14.x
#make check
make check-mimetype
make check-java-debug
make check-java-src

%install
rm -rf $RPM_BUILD_ROOT
STRIP_KEEP_SYMTAB=libjvm*

pushd %{buildoutputdir}/j2sdk-image

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  cp -a bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}

%ifarch %{jit_arches}
  # Install systemtap support files.
  cp -a tapset $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir}/tapset %{tapsetdir})
    ln -sf $RELATIVE/*.stp .
  popd
%endif

  # Install cacerts symlink.
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/cacerts
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{jredir}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
  pushd $RPM_BUILD_ROOT%{jvmjardir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir}/lib %{jvmjardir})
    ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
    ln -sf $RELATIVE/jce.jar jce-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
    ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
    ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
    ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
    for jar in *-%{version}.jar
    do
      if [ x%{version} != x%{javaver} ]
      then
        ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
  popd

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{archname}/jce/vanilla

  # Install versionless symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir} %{jrelnk}
    ln -sf %{sdkdir} %{sdklnk}
  popd

  # Remove javaws man page
  rm -f man/man1/javaws*

  # Install man pages.
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding.
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{name}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  mkdir -p sample/rmi
  mv bin/java-rmi.cgi sample/rmi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

  # Run execstack on libjvm.so.
  %ifarch i386 i686
    execstack -c $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/libjvm.so
  %endif
  execstack -c $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/libjvm.so

popd

# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole policytool ; do
    desktop-file-install --vendor=%{name} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}.files
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}-demo.files

# FIXME: remove SONAME entries from demo DSOs.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files

%clean
rm -rf $RPM_BUILD_ROOT

# FIXME: identical binaries are copied, not linked. This needs to be
# fixed upstream.
%post
ext=.gz
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} \
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jrelnk} \
  --slave %{_jvmjardir}/jre jre_exports %{_jvmjardir}/%{jrelnk} \
  --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \
  --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \
  --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \
  --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200 \
  --slave %{_mandir}/man1/java.1$ext java.1$ext \
  %{_mandir}/man1/java-%{name}.1$ext \
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \
  %{_mandir}/man1/keytool-%{name}.1$ext \
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \
  %{_mandir}/man1/orbd-%{name}.1$ext \
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \
  %{_mandir}/man1/pack200-%{name}.1$ext \
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \
  %{_mandir}/man1/rmid-%{name}.1$ext \
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \
  %{_mandir}/man1/rmiregistry-%{name}.1$ext \
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \
  %{_mandir}/man1/servertool-%{name}.1$ext \
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \
  %{_mandir}/man1/tnameserv-%{name}.1$ext \
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \
  %{_mandir}/man1/unpack200-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/jre-%{origin} \
  jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{origin} \
  jre_%{origin}_exports %{_jvmjardir}/%{jrelnk}

alternatives \
  --install %{_jvmdir}/jre-%{javaver} \
  jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
  --slave %{_jvmjardir}/jre-%{javaver} \
  jre_%{javaver}_exports %{_jvmjardir}/%{jrelnk}

# Update for jnlp handling.
update-desktop-database %{_datadir}/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

exit 0

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jrelnk}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jrelnk}
fi

# Update for jnlp handling.
update-desktop-database %{_datadir}/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

exit 0

%post devel
ext=.gz
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdklnk} \
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdklnk} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
  --slave %{_bindir}/apt apt %{sdkbindir}/apt \
  --slave %{_bindir}/extcheck extcheck %{sdkbindir}/extcheck \
  --slave %{_bindir}/jar jar %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir}/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah javah %{sdkbindir}/javah \
  --slave %{_bindir}/javap javap %{sdkbindir}/javap \
  --slave %{_bindir}/jconsole jconsole %{sdkbindir}/jconsole \
  --slave %{_bindir}/jdb jdb %{sdkbindir}/jdb \
  --slave %{_bindir}/jhat jhat %{sdkbindir}/jhat \
  --slave %{_bindir}/jinfo jinfo %{sdkbindir}/jinfo \
  --slave %{_bindir}/jmap jmap %{sdkbindir}/jmap \
  --slave %{_bindir}/jps jps %{sdkbindir}/jps \
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir}/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir}/jsadebugd \
  --slave %{_bindir}/jstack jstack %{sdkbindir}/jstack \
  --slave %{_bindir}/jstat jstat %{sdkbindir}/jstat \
  --slave %{_bindir}/jstatd jstatd %{sdkbindir}/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir}/native2ascii \
  --slave %{_bindir}/policytool policytool %{sdkbindir}/policytool \
  --slave %{_bindir}/rmic rmic %{sdkbindir}/rmic \
  --slave %{_bindir}/schemagen schemagen %{sdkbindir}/schemagen \
  --slave %{_bindir}/serialver serialver %{sdkbindir}/serialver \
  --slave %{_bindir}/wsgen wsgen %{sdkbindir}/wsgen \
  --slave %{_bindir}/wsimport wsimport %{sdkbindir}/wsimport \
  --slave %{_bindir}/xjc xjc %{sdkbindir}/xjc \
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \
  %{_mandir}/man1/appletviewer-%{name}.1$ext \
  --slave %{_mandir}/man1/apt.1$ext apt.1$ext \
  %{_mandir}/man1/apt-%{name}.1$ext \
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \
  %{_mandir}/man1/extcheck-%{name}.1$ext \
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \
  %{_mandir}/man1/jar-%{name}.1$ext \
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \
  %{_mandir}/man1/jarsigner-%{name}.1$ext \
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \
  %{_mandir}/man1/javac-%{name}.1$ext \
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \
  %{_mandir}/man1/javadoc-%{name}.1$ext \
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \
  %{_mandir}/man1/javah-%{name}.1$ext \
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \
  %{_mandir}/man1/javap-%{name}.1$ext \
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \
  %{_mandir}/man1/jconsole-%{name}.1$ext \
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \
  %{_mandir}/man1/jdb-%{name}.1$ext \
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \
  %{_mandir}/man1/jhat-%{name}.1$ext \
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \
  %{_mandir}/man1/jinfo-%{name}.1$ext \
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \
  %{_mandir}/man1/jmap-%{name}.1$ext \
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \
  %{_mandir}/man1/jps-%{name}.1$ext \
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \
  %{_mandir}/man1/jrunscript-%{name}.1$ext \
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \
  %{_mandir}/man1/jsadebugd-%{name}.1$ext \
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \
  %{_mandir}/man1/jstack-%{name}.1$ext \
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \
  %{_mandir}/man1/jstat-%{name}.1$ext \
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \
  %{_mandir}/man1/jstatd-%{name}.1$ext \
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \
  %{_mandir}/man1/native2ascii-%{name}.1$ext \
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \
  %{_mandir}/man1/policytool-%{name}.1$ext \
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \
  %{_mandir}/man1/rmic-%{name}.1$ext \
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \
  %{_mandir}/man1/schemagen-%{name}.1$ext \
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \
  %{_mandir}/man1/serialver-%{name}.1$ext \
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \
  %{_mandir}/man1/wsgen-%{name}.1$ext \
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \
  %{_mandir}/man1/wsimport-%{name}.1$ext \
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \
  %{_mandir}/man1/xjc-%{name}.1$ext

alternatives \
  --install %{_jvmdir}/java-%{origin} \
  java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{origin} \
  java_sdk_%{origin}_exports %{_jvmjardir}/%{sdklnk}

alternatives \
  --install %{_jvmdir}/java-%{javaver} \
  java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
  --slave %{_jvmjardir}/java-%{javaver} \
  java_sdk_%{javaver}_exports %{_jvmjardir}/%{sdklnk}

exit 0

%postun devel
if [ $1 -eq 0 ]
then
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdklnk}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

exit 0

%post javadoc
alternatives \
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{name}/api \
  %{priority}

exit 0

%postun javadoc
if [ $1 -eq 0 ]
then
  alternatives --remove javadocdir %{_javadocdir}/%{name}/api
fi

exit 0


%files -f %{name}.files
%defattr(-,root,root,-)
%doc %{buildoutputdir}/j2sdk-image/jre/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE
%doc %{buildoutputdir}/j2sdk-image/jre/THIRD_PARTY_README
# FIXME: The TRADEMARK file should be in j2sdk-image.
%doc openjdk/TRADEMARK
%doc AUTHORS
%doc COPYING
%doc ChangeLog
%doc NEWS
%doc README
%dir %{_jvmdir}/%{sdkdir}
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/local_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security.old
%{_datadir}/icons/hicolor/*x*/apps/java.png
%{_mandir}/man1/java-%{name}.1*
%{_mandir}/man1/keytool-%{name}.1*
%{_mandir}/man1/orbd-%{name}.1*
%{_mandir}/man1/pack200-%{name}.1*
%{_mandir}/man1/rmid-%{name}.1*
%{_mandir}/man1/rmiregistry-%{name}.1*
%{_mandir}/man1/servertool-%{name}.1*
%{_mandir}/man1/tnameserv-%{name}.1*
%{_mandir}/man1/unpack200-%{name}.1*
%{_jvmdir}/%{jredir}/lib/security/nss.cfg

%files devel
%defattr(-,root,root,-)
%doc %{buildoutputdir}/j2sdk-image/ASSEMBLY_EXCEPTION
%doc %{buildoutputdir}/j2sdk-image/LICENSE
#%doc %{buildoutputdir}/j2sdk-image/README.html
%doc %{buildoutputdir}/j2sdk-image/THIRD_PARTY_README
# FIXME: The TRADEMARK file should be in j2sdk-image.
%doc openjdk/TRADEMARK
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%ifarch %{jit_arches}
%dir %{_jvmdir}/%{sdkdir}/tapset
%endif
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir}/tapset/*.stp
%endif
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
%{_datadir}/applications/*jconsole.desktop
%{_datadir}/applications/*policytool.desktop
%{_mandir}/man1/appletviewer-%{name}.1*
%{_mandir}/man1/apt-%{name}.1*
%{_mandir}/man1/extcheck-%{name}.1*
%{_mandir}/man1/idlj-%{name}.1*
%{_mandir}/man1/jar-%{name}.1*
%{_mandir}/man1/jarsigner-%{name}.1*
%{_mandir}/man1/javac-%{name}.1*
%{_mandir}/man1/javadoc-%{name}.1*
%{_mandir}/man1/javah-%{name}.1*
%{_mandir}/man1/javap-%{name}.1*
%{_mandir}/man1/jconsole-%{name}.1*
%{_mandir}/man1/jdb-%{name}.1*
%{_mandir}/man1/jhat-%{name}.1*
%{_mandir}/man1/jinfo-%{name}.1*
%{_mandir}/man1/jmap-%{name}.1*
%{_mandir}/man1/jps-%{name}.1*
%{_mandir}/man1/jrunscript-%{name}.1*
%{_mandir}/man1/jsadebugd-%{name}.1*
%{_mandir}/man1/jstack-%{name}.1*
%{_mandir}/man1/jstat-%{name}.1*
%{_mandir}/man1/jstatd-%{name}.1*
%{_mandir}/man1/native2ascii-%{name}.1*
%{_mandir}/man1/policytool-%{name}.1*
%{_mandir}/man1/rmic-%{name}.1*
%{_mandir}/man1/schemagen-%{name}.1*
%{_mandir}/man1/serialver-%{name}.1*
%{_mandir}/man1/wsgen-%{name}.1*
%{_mandir}/man1/wsimport-%{name}.1*
%{_mandir}/man1/xjc-%{name}.1*
%ifarch %{jit_arches}
%{tapsetdir}/*.stp
%endif

%files demo -f %{name}-demo.files
%defattr(-,root,root,-)

%files src
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir}/src.zip

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}

%changelog
* Mon Sep 05 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.9
- Require a JDK with RH1334465/PR2956 fixed and turn off bootstrapping for Zero architectures.
- Resolves: rhbz#1350047

* Thu Sep 01 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.8
- Set install directories in configure so that @prefix@ is substituted correctly in tapset
- Resolves: rhbz#1350047

* Mon Aug 22 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.7
- Bump source tarballs to try and really fix TCK failures this time.
- Resolves: rhbz#1350047

* Mon Aug 22 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.6
- Bump source tarballs to missing -DNDEBUG on JDK native code.
- Resolves: rhbz#1350047

* Fri Aug 19 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.5
- Non-JIT architectures have not been bootstrapping, due to RPM reading commented macros
- Resolves: rhbz#1350047

* Fri Aug 19 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.4
- Bump source tarballs to fix TCK failures.
- Resolves: rhbz#1350047

* Thu Aug 18 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.3
- Separate bootstrap option as it should not be tied to the JDK used.
- Enable bootstrapping on JIT architectures going forward.
- Temporarily enable bootstrapping on all architectures to work around RH1334465/PR2956.
- Resolves: rhbz#1350047

* Wed Aug 17 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.2
- Require mailcap at build time as well, so configure finds /etc/mime.types
- Resolves: rhbz#1350047

* Wed Aug 17 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.1
- Add RHEL version of b40 tarball.
- Resolves: rhbz#1350047

* Wed Aug 17 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.40-1.13.12.1
- Update to IcedTea 1.13.12 & OpenJDK 6 b40.
- Separate SystemTap option from bootstrap options.
- Depend on mailcap for /etc/mime.types (PR2800)
- Use configure macro and disable long-running JTreg & SystemTap tests from make check
- Remove redundant patch-ecj target invocation for bootstrap build.
- Add check section to run the new tests introduced in 1.13.12.
- Fix context for rpath patch following PR3140.
- Resolves: rhbz#1350047

* Wed May 04 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.39-1.13.11.1
- Update to IcedTea 1.13.11 & OpenJDK 6 b39.
- Resolves: rhbz#1325433

* Mon Feb 15 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.38-1.13.10.3
- Remove dependencies no longer needed by modern IcedTea 1.x and current RPM build.
- Explicitly disable downloading, removing the need for wget.
- Resolves: rhbz#1308687

* Mon Jan 25 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.38-1.13.10.2
- Disable RC4 by default.
- Resolves: rhbz#1302383

* Thu Jan 21 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.38-1.13.10.1
- Update to IcedTea 1.13.10 & OpenJDK 6 b38.
- Resolves: rhbz#1295776

* Wed Nov 11 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.37-1.13.9.5
- Update with new IcedTea & b37 tarballs, including fix for appletviewer regression.
- Resolves: rhbz#1271931

* Tue Nov 10 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.37-1.13.9.4
- Update with new IcedTea & b37 tarballs, including more Kerberos fixes for TCK regression.
- Resolves: rhbz#1271931

* Wed Nov 04 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.37-1.13.9.3
- Update with new IcedTea & b37 tarballs, including Kerberos fixes for TCK regression.
- Resolves: rhbz#1271931

* Mon Nov 02 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.37-1.13.9.2
- Update with newer tarball, including 6763122 fix for TCK regression.
- Use release + 1 to avoid having a lower version than the 6.7 version.
- Resolves: rhbz#1271931

* Tue Oct 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.37-1.13.9.0
- Update to IcedTea 1.13.9
- Resolves: rhbz#1271931

* Tue Jul 28 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.36-1.13.8.1
- Update tarball to fix TCK regression (PR2565)
- Resolves: rhbz#1235154

* Wed Jul 22 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.36-1.13.8.0
- Update to IcedTea 1.13.8
- Update no_pr2125.patch to work against new version.
- Resolves: rhbz#1235154

* Fri Apr 10 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.35-1.13.7.1
- Repackaged source files
- Resolves: rhbz#1209068

* Thu Apr 09 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.35-1.13.7.0
- Update to IcedTea 1.13.7
- Regenerate add-final-location-rpaths patch so as to be less disruptive.
- Add ExcludeArch directive for RH1209326
- Resolves: rhbz#1209068

* Thu Jan 22 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.34-1.13.6.1
- Update to latest 1.13.6 release candidate tarball
- Fixes a number of issues found with b34:
- * OJ51, PR2187: Sync patch for 4873188 with 7 version
- * OJ52, PR2185: Application of 6786276 introduces compatibility issue
- * OJ53, PR2181: strict-aliasing warnings issued on PPC32
- * OJ54, PR2182: 6911104 reintroduces test fragment removed in existing 6964018 backport
- * S6730740, PR2186: Fix for 6729881 has apparently broken several 64 bit tests: "Bad address"
- * S7031830, PR2183: bad_record_mac failure on TLSv1.2 enabled connection with SSLEngine
- Regenerate add-final-location-rpaths patch against new release.
- Resolves: rhbz#1180293

* Tue Jan 20 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.34-1.13.6.0
- Update to IcedTea 1.13.6
- Remove upstream patch type_hsx23_patch4.patch.
- Regenerate add-final-location-rpaths patch against new release.
- Apply pr2125.patch in generate_rhel_zip.sh to remove unwanted elliptic curves.
- Add no_pr2125.patch to avoid repeating the procedure during the IcedTea build.
- Avoid duplicating the OpenJDK build version by making more use of %%{openjdkver}.
- Add US_export_policy.jar and local_policy.jar to packages.
- Resolves: rhbz#1180293

* Thu Oct 09 2014 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.6.0.33-1.13.5.0
- Update to IcedTea 1.13.5
- Remove upstreamed patches.
- Regenerate add-final-location-rpaths patch against new release.
- Change versioning to match java-1.7.0-openjdk so revisions work.
- Use xz for tarballs to reduce file size.
- No need to explicitly disable system LCMS any more (bug fixed upstream).
- Add icedteasnapshot to setup lines so they work with pre-release tarballs.
- Resolves: rhbz#1148902

* Mon Jul 14 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.1-6.1.13.4
- moved to  icedteaver 1.13.4
- moved to openjdkver b32 and openjdkdate 15_jul_2014
- added upstreamed patch patch9 rh1115580-unsyncHashMap.patch
- Resolves: rhbz#1115870
- forwardported from rhel 6.6, patch10, add-final-location-rpaths.patch (rh1059925)
 - Work when capabilities are set on the binary
 - Include hardcoded install path as well as $ORIGIN in RPATH
 - Don't Expect LD_LIBRARY_PATH to be set in the launcher

* Tue May 20 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.1-6.1.13.3
- updated to icedtea 1.13.3
- updated to openjdk-6-src-b31-15_apr_2014
- renmoved upstreamed patch7, 1.13_fixes.patch
- renmoved upstreamed patch9, 1051245.patch
- Resolves: rhbz#1099563

* Thu Mar 13 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.1-7.1.13.1
- added and applied patch9 1051245.patch
- Resolves: rhbz#1070816

* Fri Feb 21 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.1-5.1.13.1
- removed redundant (we have in tree copy) rhino requires
- Resolves: rhbz#1066873

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:1.6.0.0-4.1.13.1
- Mass rebuild 2014-01-24

* Thu Jan 23 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.1-3.1.13.0
- updated to icedtea 1.13.1
 - http://blog.fuseyism.com/index.php/2014/01/23/security-icedtea-1-12-8-1-13-1-for-openjdk-6-released/
- updated to jdk6, b30,  21_jan_2014
 - https://openjdk6.java.net/OpenJDK6-B30-Changes.html
- adapted patch7 1.13_fixes.patch
- pre 2011 changelog moved to (till now  wrong) pre-2009-spec-changelog (rh1043611)
- added --disable-system-lcms to configure options to pass build
- adapted patch3 java-1.6.0-openjdk-java-access-bridge-security.patch
- removed upstreamed  patch103 type_hsx23_patch3.patch
- Resolves: rhbz#1053279

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:1.6.0.0-2.1.13.0
- Mass rebuild 2013-12-27

* Wed Oct 30 2013 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.1-1.66.1.13.0
- updated to icedtea 1.13
- updated to openjdk-6-src-b28-04_oct_2013
- added --disable-lcms2 configure switch to fix tck
- removed upstreamed patch7,java-1.6.0-openjdk-jstack.patch
- removed patch100: 8000791-regression-fix.patch
- added patch7 1.13_fixes.patch to fix 1.13 build issues
- adapted patch0 java-1.6.0-openjdk-optflags.patch
- adapted patch3 java-1.6.0-openjdk-java-access-bridge-security.patch
- removed useless runtests parts
- included also java.security.old files
- added:
   - Patch103 type_hsx23_patch3.patch
   - Patch104 type_hsx23_patch4.patch
 -to fix zero type error
 -aplied everywhere, as should go upstream
- Resolves: rhbz#1018679

* Thu Aug 22 2013 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.64.1.11.12
- Removed the temporary libffi-compat-5 requirement
- Updated BR to java6-1.6.0-devel
- Build with OpenJDK6 specifically

* Fri Aug 16 2013 Deepak Bhole <dbhole@redhat.com> - 1:1.6.0.0-1.63.1.11.12
- Merged with latest version from 6.5 branch

* Tue Nov 01 2011 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.0-60.1.10.4
- omajid have added Patch6 as (probably temporally) solution for S7103224 for buildability on newest glibc libraries.

* Thu Oct 13 2011 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.0-60.1.10.4
- updated to icedtea6 1.10.4
- Security fixes
  - S7000600, CVE-2011-3547: InputStream skip() information leak
  - S7019773, CVE-2011-3548: mutable static AWTKeyStroke.ctor
  - S7023640, CVE-2011-3551: Java2D TransformHelper integer overflow
  - S7032417, CVE-2011-3552: excessive default UDP socket limit under SecurityManager
  - S7046823, CVE-2011-3544: missing SecurityManager checks in scripting engine
  - S7055902, CVE-2011-3521: IIOP deserialization code execution
  - S7057857, CVE-2011-3554: insufficient pack200 JAR files uncompress error checks
  - S7064341, CVE-2011-3389: HTTPS: block-wise chosen-plaintext attack against SSL/TLS (BEAST)
  - S7070134, CVE-2011-3558: HotSpot crashes with sigsegv from PorterStemmer
  - S7077466, CVE-2011-3556: RMI DGC server remote code execution
  - S7083012, CVE-2011-3557: RMI registry privileged code execution
  - S7096936, CVE-2011-3560: missing checkSetFactory calls in HttpsURLConnection
- Bug fixes
  - RH727195 : Japanese font mappings are broken
- Backports
  - S6826104, RH730015: Getting a NullPointer exception when clicked on Application & Toolkit Modal dialog
- Zero/Shark
  - PR690: Shark fails to JIT using hs20.
  - PR696: Zero fails to handle fast_aldc and fast_aldc_w in hs20.

* Fri Jul 22 2011 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.0-59.1.10.3
- updated to icedtea6 1.10.3
- http://blog.fuseyism.com/index.php/2011/07/21/icedtea6-1103-released/

* Fri Jun 10 2011 Jiri Vanek <jvanek@redhat.com> - 1:1.6.0.0-58.1.10.2
- added requires: fontconfig
- resolves: rhbz#708201
