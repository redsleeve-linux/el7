
# FIXME: HAVE TO USE SYSTEM NSS IN FINAL RELEASE!!!
%define system_nss              1
%global nspr_version            4.11.0
%global nss_version             3.21.0
%define system_sqlite           0
%define sqlite_version          3.8.4.2
%define system_ffi              1
%define ffi_version             3.0.9
%define use_bundled_yasm        1
%define use_bundled_python      0
%define python_version          2.7.8
%define use_bundled_gcc         0
%define gcc_version             4.8.2-16
%define enable_gstreamer        0
%define system_cairo            0
%define cairo_version           1.10.2
%define freetype_version        2.1.9
%define system_jpeg             1
%define system_gio              1
%define system_hunspell         1
%define system_libatomic        0
%define use_baselinejit         1
%define official_branding       1
%define libnotify_version       0.4
%define debug_build             0
# This is for local builds or builds in mock with --no-clean
# It skips building of gcc, binutils and yasm rpms when they exists, it just installs
# them and doesn't delete them to allow recycling them in next build.
# SHOULD ALWAYS BE 0 WHEN BUILDING IN BREW
%define do_not_clean_rpms       0


# Configure and override build options for various platforms and RHEL versions
# ============================================================================

# RHEL7
%if 0%{?rhel} == 7
%ifarch s390x
%define use_bundled_gcc         1
%endif
%endif

# RHEL6
%if 0%{?rhel} == 6
%define use_bundled_python      1
%define use_bundled_gcc         1
%define use_bundled_yasm        1
%define system_ffi              0
%define enable_gstreamer        0
%define use_bundled_binutils    1
%endif

# RHEL5
%if 0%{?rhel} == 5
%define use_bundled_python      1
%define use_bundled_gcc         1
%define use_bundled_yasm        1
%define system_ffi              0
%define enable_gstreamer        0
%define use_bundled_binutils    1
%define system_jpeg             0
%define system_gio              0
%define system_hunspell         0
%define enable_gnomevfs         1
# ppc and ia64 no longer supported (rhbz#1214863, rhbz#1214865)
ExcludeArch: ppc ia64
%define system_libatomic        1
%endif

# Require libatomic for ppc
%ifarch ppc
%define system_libatomic        1
%endif

# ============================================================================

# Avoid patch failures
%define _default_patch_fuzz 2

%define thunderbird_app_id      \{3550f703-e582-4d05-9a08-453d09bdfdc6\} 
%define build_langpacks         1

%define langpackdir             %{mozappdir}/langpacks
%if %{?system_sqlite}
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif


%define mozappdir    %{_libdir}/%{name}

Summary:        Mozilla Thunderbird mail/newsgroup client
Name:           thunderbird
Version:        45.6.0
Release:        1%{?dist}
URL:            http://www.mozilla.org/projects/thunderbird/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
%if 0%{?rhel} == 5
ExcludeArch:    ppc ppc64 ia64 s390 s390x
%endif

%define         tarballdir              thunderbird-45.6.0
%define         objdir                  objdir

# From ftp://archive.mozilla.org/pub/thunderbird/releases/%{version}%{?ext_version}/source
Source0:        https://archive.mozilla.org/pub/thunderbird/releases/%{version}%{?pre_version}/source/thunderbird-%{version}%{?pre_version}.source.tar.xz
%if %{build_langpacks}
Source1:        thunderbird-langpacks-%{version}%{?ext_version}-20161216.tar.xz
%endif
# Locales for lightning
Source2:        l10n-lightning-%{version}.tar.xz
Source3:        mklangsource.sh

Source10:       thunderbird-mozconfig
Source11:       thunderbird-mozconfig-branded
Source20:       thunderbird.desktop
Source21:       thunderbird.sh.in
Source30:       thunderbird-open-browser.sh
Source100:      find-external-requires
Source200:      https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz
Source300:      gcc48-%{gcc_version}.el5.src.rpm
Source301:      yasm-1.2.0-3.el5.src.rpm
Source302:      devtoolset-2-binutils-2.23.52.0.1-10.el5.src.rpm
Source500:      thunderbird.sh.in.rhel5
Source501:      thunderbird-redhat-default-prefs.js.el5
Source600:      thunderbird.sh.in.rhel6
Source601:      thunderbird-redhat-default-prefs.js.el6
Source700:      thunderbird.sh.in.rhel7
Source701:      thunderbird-redhat-default-prefs.js.el7

# Mozilla (XULRunner) patches
Patch0:         firefox-install-dir.patch

# Build patches
Patch5:         xulrunner-24.0-jemalloc-ppc.patch
Patch6:         webrtc-arch-cpu.patch
Patch8:         firefox-ppc64le.patch
Patch16:        mozilla-1253216-disable-ion.patch
Patch17:        build-nss.patch

# RHEL patches
Patch103:       rhbz-966424.patch
Patch109:       aarch64-fix-skia.patch
Patch110:       mozilla-1170092-etc-conf.patch
Patch111:       rhbz-1173156.patch
Patch112:       rhbz-1150082.patch

# Upstream patches
Patch201:       mozilla-1005535.patch
# Kaie's patch, we'll most likely need this one
Patch202:       mozilla-1152515.patch

# RHEL5 patches
Patch500:       build-el5-build-id.patch
Patch501:       build-el5-sandbox.patch
Patch502:       build-el5-gtk2-2.10.patch
Patch503:       build-el5-xlib-header.patch
Patch504:       build-el5-rt-tgsigqueueinfo.patch
Patch505:       build-el5-rapl.patch
Patch506:       build-el5-fontconfig.patch
Patch507:       build-el5-stdint.patch
Patch508:       build-el5-nss.patch
Patch509:       mozilla-694870-backout.patch
Patch510:       mozilla-1134537-delete-nsgnomevfsservice.patch
Patch511:       mozilla-1134537-only-support-gio-in-nsioservice.patch
Patch512:       mozilla-1134537-delete-gnomevfs-extension.patch

# Thunderbird patches
Patch1000:      thunderbird-objdir.patch
Patch1001:      lightning-bad-langs.patch
Patch1002:      thunderbird-enable-addons.patch

# ---------------------------------------------------
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  desktop-file-utils
BuildRequires:  mesa-libGL-devel
BuildRequires:  libnotify-devel >= %{libnotify_version}
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libnotify-devel
BuildRequires:  autoconf213
BuildRequires:  mesa-libGL-devel
BuildRequires:  autoconf213
BuildRequires:  xz
%if ! %{use_bundled_yasm}0
BuildRequires:  yasm
%endif
%if %{?system_sqlite}
BuildRequires:  sqlite-devel >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif
%if %{?system_nss}
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
Requires:       nspr >= %{nspr_version}
Requires:       nss >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
%if %{?system_sqlite}
BuildRequires:  sqlite-devel >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif
%if %{?system_ffi}
BuildRequires:  libffi-devel >= %{ffi_version}
Requires:       libffi >= %{ffi_version}
%endif
%if %{?enable_gstreamer}
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
%endif
BuildRequires:  libpng-devel
%if %{?system_jpeg}
BuildRequires:  libjpeg-devel
%endif
%if %{?system_hunspell}
BuildRequires:  hunspell-devel
%endif
%if %{system_libatomic}
BuildRequires:  libatomic
Requires:       libatomic
%endif

# RHEL7 requires
%if 0%{?rhel} == 7
BuildRequires:  pulseaudio-libs-devel
Requires:       mozilla-filesystem
Requires:       liberation-fonts-common
Requires:       liberation-sans-fonts
%endif

# RHEL6 requires
%if 0%{?rhel} == 6
BuildRequires:  desktop-file-utils
Requires:       mozilla-filesystem
Requires:       gtk2 >= 2.24
BuildRequires:  pulseaudio-libs-devel
Requires:       liberation-fonts-common
Requires:       liberation-sans-fonts
%endif

# RHEL5 requires
%if 0%{?rhel} == 5
BuildRequires:  libXcomposite-devel
BuildRequires:  libXdamage-devel
BuildRequires:  xorg-x11-proto-devel
%endif

Obsoletes:      thunderbird-lightning
Obsoletes:      thunderbird-lightning-gdata
%if %{use_bundled_python}
BuildRequires:  openssl-devel
%endif
# GCC 4.8 BuildRequires
# ==================================================================================
%if %{use_bundled_gcc}

%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%if 0%{?rhel} >= 6
%global multilib_32_arch i686
%else
%global multilib_32_arch i386
%endif
%endif

%global multilib_64_archs sparc64 ppc64 s390x x86_64

%if 0%{?rhel} >= 6
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.19.51.0.14-33
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
%else
# Don't have binutils which support --build-id >= 2.17.50.0.17-3
# Don't have binutils which support %gnu_unique_object >= 2.19.51.0.14
# Don't have binutils which  support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.17.50.0.2-8
%endif
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
BuildRequires: /usr/bin/pod2man
%if 0%{?rhel} >= 7
BuildRequires: texinfo-tex
%endif
#BuildRequires: systemtap-sdt-devel >= 1.3
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
%if 0%{?rhel} >= 6
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%else
BuildRequires: elfutils-devel >= 0.72
%endif
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
#%if 0%{?rhel} >= 6
## Need binutils which support --build-id >= 2.17.50.0.17-3
## Need binutils which support %gnu_unique_object >= 2.19.51.0.14
## Need binutils which support .cfi_sections >= 2.19.51.0.14-33
#Requires: binutils >= 2.19.51.0.14-33
#%else
## Don't have binutils which support --build-id >= 2.17.50.0.17-3
## Don't have binutils which support %gnu_unique_object >= 2.19.51.0.14
## Don't have binutils which  support .cfi_sections >= 2.19.51.0.14-33
#Requires: binutils >= 2.17.50.0.2-8
#%endif
## Make sure gdb will understand DW_FORM_strp
#Conflicts: gdb < 5.1-2
#Requires: glibc-devel >= 2.2.90-12
#%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
## Make sure glibc supports TFmode long double
#Requires: glibc >= 2.3.90-35
#%endif
#Requires: libgcc >= 4.1.2-43
#Requires: libgomp >= 4.4.4-13
#%if 0%{?rhel} == 6
#Requires: libstdc++ >= 4.4.4-13
#%else
#Requires: libstdc++ = 4.1.2
#%endif
##FIXME gcc version
#Requires: libstdc++-devel = %{version}-%{release}
BuildRequires: gmp-devel >= 4.1.2-8
%if 0%{?rhel} >= 6
BuildRequires: mpfr-devel >= 2.2.1
%endif
%if 0%{?rhel} >= 7
BuildRequires: libmpc-devel >= 0.8.1
%endif

%endif # bundled gcc BuildRequires
# ==================================================================================
# Override internal dependency generator to avoid showing libraries provided by this package
# in dependencies:
AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

%description
Mozilla Thunderbird is a standalone mail and newsgroup client.


%prep
%setup -q -c
cd %{tarballdir}

# Mozilla (XULRunner) patches
cd mozilla
# Build patches
# We have to keep original patch backup extension to go thru configure without problems with tests
%patch0 -p1 -b .orig
%patch5 -p2 -b .jemalloc-ppc.patch
%patch6 -p1 -b .webrtc-arch-cpu
%patch8 -p2 -b .ppc64le
%patch16 -p2 -b .moz-1253216-disable-ion
%patch17 -p1 -b .build-nss

# RPM specific patches
%patch103 -p1 -b .rhbz-966424
%patch109 -p1 -b .aarch64
%patch110 -p1 -b .moz-1170092-etc-conf
%patch111 -p2 -b .rhbz-1173156
%patch112 -p1 -b .rhbz-1150082

# Upstream patches
%patch201 -p1 -b .mozbz-1005535
# FIXME: will require this?: by kai
%patch202 -p1 -b .mozbz-1152515


# RHEL5 only patches
%if 0%{?rhel} == 5
%patch500 -p1 -b .gnu-build-id
%patch501 -p1 -b .build-sandbox
%patch502 -p1 -b .build-gtk2
%patch503 -p1 -b .build-xlib-swap
%patch504 -p1 -b .build-rt-tgsigqueueinfo
%patch505 -p1 -b .build-el5-rapl
%patch506 -p1 -b .build-el5-fontconfig
%patch507 -p1 -b .build-el5-stdint
%patch508 -p1 -b .build-el5-nss
%patch509 -p2 -b .moz-694870-backout
%patch510 -p2 -b .moz-1134537-delete-nsgnomevfsservice
%patch511 -p1 -R -b .moz-1134537-only-support-gio-in-nsioservice
%patch512 -p2 -b .moz-1134537-gnomevfsservice
%endif
cd ..

%patch1000 -p2 -b .objdir
%patch1001 -p1 -b .badlangs
%patch1002 -p1 -b .addons
#%patch301 -p1 -b .ppc64le-build # fixme?


%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
function add_to_mozconfig() {
  mozconfig_entry=$1
  echo "ac_add_options --$1" >> .mozconfig
}

# Modify mozconfig file
%if %{official_branding}
 add_to_mozconfig "enable-official-branding"
%endif

%if %{?system_sqlite}
 add_to_mozconfig "enable-system-sqlite"
%else
 add_to_mozconfig "disable-system-sqlite"
%endif

%if %{?system_cairo}
 add_to_mozconfig "enable-system-cairo"
%else
 add_to_mozconfig "disable-system-cairo"
%endif

%if %{?system_ffi}
 add_to_mozconfig "enable-system-ffi"
%endif

%if %{?system_nss}
 add_to_mozconfig "with-system-nspr"
 add_to_mozconfig "with-system-nss"
%else
 add_to_mozconfig "without-system-nspr"
 add_to_mozconfig "without-system-nss"
%endif

%if %{?enable_gstreamer}
 add_to_mozconfig "enable-gstreamer=1.0"
%else
 add_to_mozconfig "disable-gstreamer"
%endif

%if %{?system_jpeg}
 add_to_mozconfig "with-system-jpeg"
%else
 add_to_mozconfig "without-system-jpeg"
%endif
%if %{?system_hunspell}
 add_to_mozconfig "enable-system-hunspell"
%endif

# RHEL 7 mozconfig changes:
%if 0%{?rhel} >= 6
 add_to_mozconfig "enable-libnotify"
 add_to_mozconfig "enable-startup-notification"
 add_to_mozconfig "enable-jemalloc"
%endif

# RHEL 6
%if 0%{?rhel} == 6
 # Disable dbus, because we're unable to build with its support in brew
 add_to_mozconfig "disable-dbus"
%endif

%if 0%{?rhel} == 5
 add_to_mozconfig "disable-pulseaudio"
%endif

%ifarch aarch64
 add_to_mozconfig "disable-ion"
%endif

%if %{system_gio}
 add_to_mozconfig "enable-gio"
 add_to_mozconfig "disable-gnomevfs"
%else
 add_to_mozconfig "disable-gio"
 add_to_mozconfig "enable-gnomevfs"
%endif

# Debug build flags
%if %{?debug_build}
 add_to_mozconfig "enable-debug"
 add_to_mozconfig "disable-optimize"
%else
 add_to_mozconfig "disable-debug"
 add_to_mozconfig "enable-optimize"
%endif

#FIXME RTTI?? RHEL5/6
# ac_add_options --enable-cpp-rtti
# RHEL7: ac_add_options --with-system-bz2
# RHEL5: never been there, but is it usable --enable-gnomeui ????

%if %{use_bundled_python}
 # Prepare Python 2.7 sources
 tar xf %{SOURCE200}
%endif

# install lightning langpacks
cd ..
%{__xz} -dc %{SOURCE2} | %{__tar} xf -
cd -
#===============================================================================

%build

function build_bundled_package() {
  PACKAGE_RPM=$1
  PACKAGE_FILES=$2
  PACKAGE_SOURCE=$3
  PACKAGE_DIR="%{_topdir}/RPMS"

  PACKAGE_ALREADY_BUILD=0
  %if %{do_not_clean_rpms}
    if ls $PACKAGE_DIR/$PACKAGE_RPM; then
      PACKAGE_ALREADY_BUILD=1
    fi
    if ls $PACKAGE_DIR/%{_arch}/$PACKAGE_RPM; then
      PACKAGE_ALREADY_BUILD=1
    fi
  %endif
  if [ $PACKAGE_ALREADY_BUILD == 0 ]; then
    echo "Rebuilding $PACKAGE_RPM from $PACKAGE_SOURCE"; echo "==============================="
    rpmbuild --nodeps --rebuild $PACKAGE_SOURCE
  fi

  if [ ! -f $PACKAGE_DIR/$PACKAGE_RPM ]; then
    # Hack for tps tests
    ARCH_STR=%{_arch}
    %ifarch i386 i686
    ARCH_STR="i?86"
    %endif
    PACKAGE_DIR="$PACKAGE_DIR/$ARCH_STR"
  fi
  pushd $PACKAGE_DIR
  echo "Installing $PACKAGE_DIR/$PACKAGE_RPM"; echo "==============================="
  rpm2cpio $PACKAGE_DIR/$PACKAGE_RPM | cpio -iduv
  # Clean rpms to avoid including them to package
  %if ! %{do_not_clean_rpms}0
    rm -f $PACKAGE_FILES
  %endif

  PATH=$PACKAGE_DIR/usr/bin:$PATH
  export PATH
  LD_LIBRARY_PATH=$PACKAGE_DIR/usr/%{_lib}
  export LD_LIBRARY_PATH
  popd
}

# Build and install local yasm if needed
# ======================================
%if %{use_bundled_yasm}
  build_bundled_package 'yasm-1*.rpm' 'yasm-*.rpm' '%{SOURCE301}'
%endif

# Install local binutils if needed
# ======================================
%if 0%{?use_bundled_binutils}
  build_bundled_package 'binutils-2*.rpm' 'binutils*.rpm' '%{SOURCE302}'
%endif

# Install local GCC if needed
# ======================================
%if %{use_bundled_gcc}
  %if %{rhel} == 5
    %ifarch ppc64
      export STRIP="/bin/true"
    %endif
  %endif
  build_bundled_package 'gcc48-%{gcc_version}*.rpm' 'gcc48-*.rpm' '%{SOURCE300}'
  %if %{rhel} == 5
    %ifarch ppc64
      unset STRIP
    %endif
  %endif
  export CXX=g++
%endif


# Install local Python if needed
# ======================================
%if %{use_bundled_python}
    echo "Rebuilding Python"; echo "==============================="
  pushd %{tarballdir}

  # Build Python 2.7 and set environment
  BUILD_DIR=`pwd`/python_build
  cd Python-%{python_version}
  ./configure --prefix=$BUILD_DIR --exec-prefix=$BUILD_DIR
  make
  make install
  cd -

  PATH=$BUILD_DIR/bin:$PATH
  export PATH
  popd
%endif # bundled Python

%if %{?system_sqlite}
  # Do not proceed with build if the sqlite require would be broken:
  # make sure the minimum requirement is non-empty, ...
  sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
  # ... and that major number of the computed build-time version matches:
  case "%{sqlite_build_version}" in
    "$sqlite_version"*) ;;
    *) exit 1 ;;
  esac
%endif

echo "Building Thunderbird"; echo "==============================="
cd %{tarballdir}

# 1. Mozilla builds with -Wall with exception of a few warnings which show up
#    everywhere in the code; so, don't override that.
# 2. -Werror=format-security causes build failures when -Wno-format is explicitly given
#    for some sources
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive -Wformat-security -Wformat -Werror=format-security" | %{__sed} -e 's/-Wall//')

# TODO check if necessery
# Update the various config.guess to upstream release for aarch64 support
#find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'
# FIXME required? find ./ -name config.guess -exec cp ./mozilla/build/autoconf/config.guess {} ';'

%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
%endif

# Avoid failing builds because OOM killer on some arches
%ifarch s390 %{arm} ppc
MOZ_LINK_FLAGS="$MOZ_LINK_FLAGS -Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif

%if 0%{?rhel} == 6
  %if %{system_libatomic}
    MOZ_LINK_FLAGS="$MOZ_LINK_FLAGS -l:libatomic.so.1"
  %endif
%endif

%if 0%{?rhel} == 5
  %if %{system_libatomic}
    # Force to use ld.bfd linker instead of ld.gold
    MOZ_LINK_FLAGS="$MOZ_LINK_FLAGS -fuse-ld=bfd -l:libatomic.so.1"
  %endif
  %ifarch i386 i686
    MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-march=i386/-march=i586/')
  %endif
%endif

%if %{?debug_build}
  MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif

export CFLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-fpermissive//')
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS="-Wl,--verbose $MOZ_LINK_FLAGS"

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

# Hack for missing shell when building in brew on RHEL6 and RHEL5
%if 0%{?rhel} <= 6
export SHELL=/bin/sh
%endif

MOZ_SMP_FLAGS=-j1
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
#FIXME echo "test config.guess"
#./mozilla/build/autoconf/config.guess
#echo "test LDAP config.guess"
#sh -x ./ldap/sdks/c-sdk/config/autoconf/config.guess

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"

# Package l10n files
cd %{objdir}/calendar/lightning
grep -v 'osx' ../../../calendar/locales/shipped-locales | while read lang x
do
   make AB_CD=en-US L10N_XPI_NAME=lightning libs-$lang
done
# install l10n files
make tools
cd -

#===============================================================================

%install
cd %{tarballdir}
%{__rm} -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT make -C objdir install

%if 0%{?rhel} == 5
desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category Network \
  --add-category Email \
  %{SOURCE20}
%else
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE20}
%endif

# Set up the thunderbird start script, unfortunatelly it is different for each RHEL
rm -rf $RPM_BUILD_ROOT%{_bindir}/thunderbird
THUNDERBIRD_SH_SOURCE=%{SOURCE700}
THUNDERBIRD_PREF_SOURCE=%{SOURCE701}
%if 0%{?rhel} == 5
  THUNDERBIRD_SH_SOURCE=%{SOURCE500}
  THUNDERBIRD_PREF_SOURCE=%{SOURCE501}
%endif
%if 0%{?rhel} == 6
  THUNDERBIRD_SH_SOURCE=%{SOURCE600}
  THUNDERBIRD_PREF_SOURCE=%{SOURCE601}
%endif
cp $THUNDERBIRD_SH_SOURCE $RPM_BUILD_ROOT%{_bindir}/thunderbird
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/thunderbird

# Fill in THUNDERBIRD_RPM_VR and COMMAND into our rh-default-prefs
%{__cat} $THUNDERBIRD_PREF_SOURCE | %{__sed} -e 's,THUNDERBIRD_RPM_VR,%{version}-%{release},g' \
                                -e 's,COMMAND,%{mozappdir}/open-browser.sh,g' > \
        $RPM_BUILD_ROOT/rh-default-prefs
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/greprefs/all-redhat.js
%{__install} -D $RPM_BUILD_ROOT/rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-redhat.js
%{__rm} $RPM_BUILD_ROOT/rh-default-prefs

# Hyperlink opening script for rhel5
%if 0%{?rhel} == 5
  install -Dm755 %{SOURCE30} $RPM_BUILD_ROOT/%{mozappdir}/open-browser.sh
  %{__sed} -i -e 's|LIBDIR|%{_libdir}|g' $RPM_BUILD_ROOT/%{mozappdir}/open-browser.sh
%endif


# install icons
for s in 16 22 24 32 48 256; do
    %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p other-licenses/branding/%{name}/mailicon${s}.png \
               $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/thunderbird.png
done

%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/thunderbird-config

# own mozilla plugin dir (#135050)
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins

# own extension directories
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{thunderbird_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{thunderbird_app_id}

# Install langpacks
echo > ../%{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
%{__mkdir_p} $RPM_BUILD_ROOT%{langpackdir}
%{__xz} -dc %{SOURCE1} | %{__tar} xf -
for langpack in `ls thunderbird-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@thunderbird.mozilla.org
  %{__mkdir_p} $extensionID
  unzip $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -r9mX ../${extensionID}.xpi *
  cd -

  %{__install} -m 644 ${extensionID}.xpi $RPM_BUILD_ROOT%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> ../%{name}.lang
done
%{__rm} -rf thunderbird-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
  language_long=$1
  language_short=$2
  cd $RPM_BUILD_ROOT%{langpackdir}
  ln -s langpack-$language_long@thunderbird.mozilla.org.xpi langpack-$language_short@thunderbird.mozilla.org.xpi
  cd -
  echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@thunderbird.mozilla.org.xpi" >> ../%{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
# Because of bug 1341629 we can't do this:
#create_default_langpack "bn-BD" "bn"
#create_default_langpack "es-AR" "es"
#create_default_langpack "fy-NL" "fy"
#create_default_langpack "ga-IE" "ga"
#create_default_langpack "hy-AM" "hy"
#create_default_langpack "nb-NO" "nb"
#create_default_langpack "nn-NO" "nn"
#create_default_langpack "pa-IN" "pa"
#create_default_langpack "pt-PT" "pt"
#create_default_langpack "sv-SE" "sv"
#create_default_langpack "zh-TW" "zh"
%endif # build_langpacks

# Get rid of devel package and its debugsymbols
%{__rm} -rf $RPM_BUILD_ROOT%{_libdir}/%{name}-devel-%{version}

# Copy over the LICENSE
cd mozilla
install -c -m 644 LICENSE $RPM_BUILD_ROOT%{mozappdir}
cd -

# Use the system dictionaries for system hunspell
%if %{system_hunspell}
  %{__rm} -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
  ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
%endif

# ghost files
%{__mkdir_p} $RPM_BUILD_ROOT%{mozappdir}/components
touch $RPM_BUILD_ROOT%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{mozappdir}/components/xpti.dat

# Clean thunderbird-devel debuginfo
rm -rf %{_prefix}/lib/debug/lib/%{name}-devel-*
rm -rf %{_prefix}/lib/debug/lib64/%{name}-devel-*

#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

#===============================================================================
%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/thunderbird
%if 0%{?rhel} == 5
%attr(644,root,root) %{_datadir}/applications/mozilla-thunderbird.desktop
%else
%attr(644,root,root) %{_datadir}/applications/thunderbird.desktop
%endif
%dir %{_datadir}/mozilla/extensions/%{thunderbird_app_id}
%dir %{_libdir}/mozilla/extensions/%{thunderbird_app_id}
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/chrome
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/omni.ja
%{mozappdir}/plugin-container
%{mozappdir}/defaults
%{mozappdir}/dictionaries
%dir %{mozappdir}/extensions
%{mozappdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}.xpi
%dir %{mozappdir}/langpacks
%{mozappdir}/greprefs
%{mozappdir}/isp
%{mozappdir}/run-mozilla.sh
%{mozappdir}/thunderbird-bin
%{mozappdir}/thunderbird
%{mozappdir}/*.so
%{mozappdir}/platform.ini
%{mozappdir}/application.ini
%{mozappdir}/blocklist.xml
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/thunderbird.png
%{_datadir}/icons/hicolor/22x22/apps/thunderbird.png
%{_datadir}/icons/hicolor/24x24/apps/thunderbird.png
%{_datadir}/icons/hicolor/256x256/apps/thunderbird.png
%{_datadir}/icons/hicolor/32x32/apps/thunderbird.png
%{_datadir}/icons/hicolor/48x48/apps/thunderbird.png
%if !%{?system_nss}
%{mozappdir}/*.chk
%endif
%exclude %{_datadir}/idl/%{name}-%{version}
%exclude %{_includedir}/%{name}-%{version}
%{mozappdir}/dependentlibs.list
%{mozappdir}/distribution
%if 0%{?rhel} < 6
%{mozappdir}/open-browser.sh
%endif

#===============================================================================

%changelog
* Wed Dec 21 2016 Johnny Hughes <johnny@centos.org> - 45.6.0-1
- Manual CentOS Debranding
 
* Fri Dec 16 2016 Martin Stransky <stransky@redhat.com> - 45.6.0-1
- Update to the latest upstream (45.6.0)

* Thu Dec  1 2016 Jan Horak <jhorak@redhat.com> - 45.5.1-1
- Update to 45.5.1

* Fri Nov 18 2016 Jan Horak <jhorak@redhat.com> - 45.5.0-1
- Update to 45.5.0

* Thu Sep 29 2016 Jan Horak <jhorak@redhat.com> - 45.4.0-1
- Update to 45.4.0

* Fri Aug 26 2016 Jan Horak <jhorak@redhat.com> - 45.3.0-1
- Update to 45.3.0

* Wed Jun 29 2016 Jan Horak <jhorak@redhat.com> - 45.2-1
- Update to 45.2

* Mon Jun  6 2016 Jan Horak <jhorak@redhat.com> - 45.1.1-1
- Update to 45.1.1

* Mon Jun 06 2016 Jan Horak <jhorak@redhat.com> - 45.1.0-5
- Do not add symlinks to some langpacks

* Tue May 17 2016 Jan Horak <jhorak@redhat.com> - 45.1.0-4
- Update to 45.1.0

* Tue Apr 26 2016 Jan Horak <jhorak@redhat.com> - 45.0-5
- Update to 45.0

* Tue Sep 29 2015 Jan Horak <jhorak@redhat.com> - 38.3.0-1
- Update to 38.3.0

* Fri Aug 14 2015 Jan Horak <jhorak@redhat.com> - 38.2.0-1
- Update to 38.2.0

* Wed Jul 15 2015 Jan Horak <jhorak@redhat.com> - 38.1.0-2
- Rebase to 38.1.0

* Wed Jul 15 2015 Jan Horak <jhorak@redhat.com> - 31.8.0-1
- Update to 31.8.0

* Sun May 10 2015 Jan Horak <jhorak@redhat.com> - 31.7.0-1
- Update to 31.7.0

* Tue Mar 31 2015 Jan Horak <jhorak@redhat.com> - 31.6.0-1
- Update to 31.6.0

* Mon Feb 23 2015 Jan Horak <jhorak@redhat.com> - 31.5.0-2
- Update to 31.5.0

* Sat Jan 10 2015 Jan Horak <jhorak@redhat.com> - 31.4.0-1
- Update to 31.4.0

* Mon Dec 22 2014 Jan Horak <jhorak@redhat.com> - 31.3.0-2
- Fixed problems with dictionaries (mozbz#1097550)

* Fri Nov 28 2014 Jan Horak <jhorak@redhat.com> - 31.3.0-1
- Update to 31.3.0

* Thu Oct 30 2014 Jan Horak <jhorak@redhat.com> - 31.2.0-2
- Update to 31.2.0

* Wed Oct 1 2014 Martin Stransky <stransky@redhat.com> - 31.1.1-5
- Sync preferences with Firefox

* Thu Sep 18 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 31.1.1-4
- Fix dependency generation for internal libraries (#1140471)

* Fri Sep 12 2014 Jan Horak <jhorak@redhat.com> - 31.1.1-3
- Update to 31.1.1

* Tue Sep  9 2014 Jan Horak <jhorak@redhat.com> - 31.1.0-4
- Use  system libffi

* Wed Sep  3 2014 Jan Horak <jhorak@redhat.com> - 31.1.0-2
- Added fix for ppc64le

* Mon Sep  1 2014 Jan Horak <jhorak@redhat.com> - 31.1.0-1
- Update to 31.1.0

* Wed Jul 30 2014 Martin Stransky <stransky@redhat.com> - 31.0-2
- Added patch for mozbz#858919

* Tue Jul 29 2014 Martin Stransky <stransky@redhat.com> - 31.0-1
- Update to 31.0

* Tue Jul 22 2014 Jan Horak <jhorak@redhat.com> - 24.7.0-1
- Update to 24.7.0

* Mon Jun  9 2014 Jan Horak <jhorak@redhat.com> - 24.6.0-1
- Update to 24.6.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 24.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Brent Baude <baude@us.ibm.com> - 24.5.0-5
- Moving the ppc64 conditional up before the cd so it will
- apply cleanly

* Fri May 23 2014 Martin Stransky <stransky@redhat.com> - 24.5.0-4
- Added a build fix for ppc64 - rhbz#1100495

* Mon May  5 2014 Jan Horak <jhorak@redhat.com> - 24.5.0-3
- Fixed find requires

* Mon Apr 28 2014 Jan Horak <jhorak@redhat.com> - 24.5.0-1
- Update to 24.5.0

* Tue Apr 22 2014 Jan Horak <jhorak@redhat.com> - 24.4.0-2
- Added support for ppc64le

* Tue Mar 18 2014 Jan Horak <jhorak@redhat.com> - 24.4.0-1
- Update to 24.4.0

* Mon Feb  3 2014 Jan Horak <jhorak@redhat.com> - 24.3.0-1
- Update to 24.3.0

* Mon Dec 16 2013 Martin Stransky <stransky@redhat.com> - 24.2.0-4
- Fixed rhbz#1024232 - thunderbird: squiggly lines used 
  for spelling correction disappear randomly

* Fri Dec 13 2013 Martin Stransky <stransky@redhat.com> - 24.2.0-3
- Build with -Werror=format-security (rhbz#1037353)

* Wed Dec 11 2013 Martin Stransky <stransky@redhat.com> - 24.2.0-2
- rhbz#1001998 - added a workaround for system notifications

* Mon Dec  9 2013 Jan Horak <jhorak@redhat.com> - 24.2.0-1
- Update to 24.2.0

* Sat Nov 02 2013 Dennis Gilmore <dennis@ausil.us> - 24.1.0-2
- remove ExcludeArch: armv7hl

* Wed Oct 30 2013 Jan Horak <jhorak@redhat.com> - 24.1.0-1
- Update to 24.1.0

* Thu Oct 17 2013 Martin Stransky <stransky@redhat.com> - 24.0-4
- Fixed rhbz#1005611 - BEAST workaround not enabled in Firefox

* Wed Sep 25 2013 Jan Horak <jhorak@redhat.com> - 24.0-3
- Update to 24.0

* Mon Sep 23 2013 Jan Horak <jhorak@redhat.com> - 17.0.9-1
- Update to 17.0.9 ESR

* Mon Aug  5 2013 Jan Horak <jhorak@redhat.com> - 17.0.8-1
- Update to 17.0.8

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 25 2013 Jan Horak <jhorak@redhat.com> - 17.0.7-1
- Update to 17.0.7

* Wed Jun 12 2013 Jan Horak <jhorak@redhat.com> - 17.0.6-2
- Fixed rhbz#973371 - unable to install addons

* Tue May 14 2013 Jan Horak <jhorak@redhat.com> - 17.0.6-1
- Update to 17.0.6

* Tue Apr  2 2013 Jan Horak <jhorak@redhat.com> - 17.0.5-1
- Update to 17.0.5

* Mon Mar 11 2013 Jan Horak <jhorak@redhat.com> - 17.0.4-1
- Update to 17.0.4

* Tue Feb 19 2013 Jan Horak <jhorak@redhat.com> - 17.0.3-1
- Update to 17.0.3

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Martin Stransky <stransky@redhat.com> - 17.0.2-3
- Added fix for NM regression (mozbz#791626)

* Tue Jan 15 2013 Jan Horak <jhorak@redhat.com> - 17.0.2-2
- Added mozilla-746112 patch to fix crash on ppc(64)

* Thu Jan 10 2013 Jan Horak <jhorak@redhat.com> - 17.0.2-1
- Update to 17.0.2

* Mon Nov 19 2012 Jan Horak <jhorak@redhat.com> - 17.0-1
- Update to 17.0

* Mon Oct 29 2012 Jan Horak <jhorak@redhat.com> - 16.0.2-1
- Update to 16.0.2

* Tue Oct 16 2012 Jan Horak <jhorak@redhat.com> - 16.0.1-2
- Fixed nss and nspr versions

* Thu Oct 11 2012 Jan Horak <jhorak@redhat.com> - 16.0.1-1
- Update to 16.0.1

* Tue Oct  9 2012 Jan Horak <jhorak@redhat.com> - 16.0-1
- Update to 16.0

* Tue Sep 18 2012 Dan Horák <dan[at]danny.cz> - 15.0.1-3
- Added fix for rhbz#855923 - TB freezes on Fedora 18 for PPC64

* Fri Sep 14 2012 Martin Stransky <stransky@redhat.com> - 15.0.1-2
- Added build flags for second arches

* Tue Sep 11 2012 Jan Horak <jhorak@redhat.com> - 15.0.1-1
- Update to 15.0.1

* Fri Sep  7 2012 Jan Horak <jhorak@redhat.com> - 15.0-2
- Added workaround fix for PPC (rbhz#852698)

* Mon Aug 27 2012 Jan Horak <jhorak@redhat.com> - 15.0-1
- Update to 15.0

* Wed Aug 1 2012 Martin Stransky <stransky@redhat.com> - 14.0-4
- Removed StartupWMClass (rhbz#844863)
- Fixed -g parameter
- Removed thunderbird-devel before packing to avoid debugsymbols duplicities (rhbz#823940)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Jan Horak <jhorak@redhat.com> - 14.0-1
- Update to 14.0

* Fri Jun 15 2012 Jan Horak <jhorak@redhat.com> - 13.0.1-1
- Update to 13.0.1

* Tue Jun  5 2012 Jan Horak <jhorak@redhat.com> - 13.0-1
- Update to 13.0

* Mon May 7 2012 Martin Stransky <stransky@redhat.com> - 12.0.1-2
- Fixed #717245 - adhere Static Library Packaging Guidelines

* Mon Apr 30 2012 Jan Horak <jhorak@redhat.com> - 12.0.1-1
- Update to 12.0.1

* Tue Apr 24 2012 Jan Horak <jhorak@redhat.com> - 12.0-1
- Update to 12.0

* Mon Apr 16 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 11.0.1-2
- Add upstream patch to fix FTBFS on ARM

* Thu Mar 29 2012 Jan Horak <jhorak@redhat.com> - 11.0.1-1
- Update to 11.0.1

* Thu Mar 22 2012 Jan Horak <jhorak@redhat.com> - 11.0-6
- Added translations to thunderbird.desktop file

* Fri Mar 16 2012 Martin Stransky <stransky@redhat.com> - 11.0-5
- gcc 4.7 build fixes

* Wed Mar 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 11.0-4
- Add ARM configuration options

* Wed Mar 14 2012 Martin Stransky <stransky@redhat.com> - 11.0-3
- Build with system libvpx

* Tue Mar 13 2012 Martin Stransky <stransky@redhat.com> - 11.0-1
- Update to 11.0

* Thu Feb 23 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-3
- Added fix for proxy settings mozbz#682832

* Thu Feb 16 2012 Martin Stransky <stransky@redhat.com> - 10.0.1-2
- Added fix for mozbz#727401

* Thu Feb  9 2012 Jan Horak <jhorak@redhat.com> - 10.0.1-1
- Update to 10.0.1

* Mon Feb 6 2012 Martin Stransky <stransky@redhat.com> - 10.0-2
- gcc 4.7 build fixes

* Tue Jan 31 2012 Jan Horak <jhorak@redhat.com> - 10.0-1
- Update to 10.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jan 05 2012 Dan Horák <dan[at]danny.cz> - 9.0-6
- disable jemalloc on s390(x) (taken from xulrunner)

* Wed Jan 04 2012 Dan Horák <dan[at]danny.cz> - 9.0-5
- fix build on secondary arches (cherry-picked from 13afcd4c097c)

* Thu Dec 22 2011 Jan Horak <jhorak@redhat.com> - 9.0-4
- Update to 9.0

* Fri Dec 9 2011 Martin Stransky <stransky@redhat.com> - 8.0-4
- enabled gio support (#760644)

* Tue Nov 29 2011 Jan Horak <jhorak@redhat.com> - 8.0-3
- Fixed s390x issues

* Thu Nov 10 2011 Jan Horak <jhorak@redhat.com> - 8.0-2
- Enable Mozilla's crash reporter again for all archs
- Temporary workaround for langpacks
- Disabled addon check UI (#753551)

* Tue Nov  8 2011 Jan Horak <jhorak@redhat.com> - 8.0-1
- Update to 8.0

* Tue Oct 18 2011 Martin Stransky <stransky@redhat.com> - 7.0.1-3
- Added NM patches (mozbz#627672, mozbz#639959)

* Wed Oct 12 2011 Dan Horák <dan[at]danny.cz> - 7.0.1-2
- fix build on secondary arches (copied from xulrunner)

* Fri Sep 30 2011 Jan Horak <jhorak@redhat.com> - 7.0.1-1
- Update to 7.0.1

* Tue Sep 27 2011 Jan Horak <jhorak@redhat.com> - 7.0-1
- Update to 7.0

* Tue Sep  6 2011 Jan Horak <jhorak@redhat.com> - 6.0.2-1
- Update to 6.0.2

* Wed Aug 31 2011 Jan Horak <jhorak@redhat.com> - 6.0-3
- Distrust a specific Certificate Authority

* Wed Aug 31 2011 Dan Horák <dan[at]danny.cz> - 6.0-2
- add secondary-ipc patch from xulrunner

* Tue Aug 16 2011 Jan Horak <jhorak@redhat.com> - 6.0-1
- Update to 6.0

* Tue Aug 16 2011 Remi Collet <remi@fedoraproject.org> 5.0-4
- Don't unzip the langpacks

* Mon Aug 15 2011 Jan Horak <jhorak@redhat.com> - 5.0-3
- Rebuild due to rhbz#728707

* Wed Jul 20 2011 Dan Horák <dan[at]danny.cz> - 5.0-2
- add xulrunner patches for secondary arches

* Tue Jun 28 2011 Jan Horak <jhorak@redhat.com> - 5.0-1
- Update to 5.0

* Tue Jun 21 2011 Jan Horak <jhorak@redhat.com> - 3.1.11-1
- Update to 3.1.11

* Wed May 25 2011 Caolán McNamara <caolanm@redhat.com> - 3.1.10-2
- rebuild for new hunspell

* Thu Apr 28 2011 Jan Horak <jhorak@redhat.com> - 3.1.10-1
- Update to 3.1.10

* Thu Apr 21 2011 Christopher Aillon <caillon@redhat.com> - 3.1.9-7
- Make gvfs-open launch a compose window (salimma)
- Spec file cleanups (salimma, caillon)
- Split out mozilla crashreporter symbols to its own debuginfo package (caillon)

* Sat Apr  2 2011 Christopher Aillon <caillon@redhat.com> - 3.1.9-6
- Drop gio support: the code hooks don't exist yet for TB 3.1.x

* Fri Apr  1 2011 Orion Poplawski <orion@cora.nwra.com> - 3.1.9-5
- Enable startup notification

* Sun Mar 20 2011 Dan Horák <dan[at]danny.cz> - 3.1.9-4
- updated the s390 build patch

* Fri Mar 18 2011 Jan Horak <jhorak@redhat.com> - 3.1.9-3
- Removed gnome-vfs2, libgnomeui and libgnome from build requires

* Wed Mar  9 2011 Jan Horak <jhorak@redhat.com> - 3.1.9-2
- Disabled gnomevfs, enabled gio

* Mon Mar  7 2011 Jan Horak <jhorak@redhat.com> - 3.1.9-1
- Update to 3.1.9

* Tue Mar  1 2011 Jan Horak <jhorak@redhat.com> - 3.1.8-3
- Update to 3.1.8

* Wed Feb  9 2011 Christopher Aillon <caillon@redhat.com> - 3.1.7-6
- Drop the -lightning subpackage, it needs to be in its own SRPM

* Mon Feb  7 2011 Christopher Aillon <caillon@redhat.com> - 3.1.7-5
- Bring back the default mailer check but fix up the directory

* Wed Dec 15 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-4
- Mozilla crash reporter enabled

* Thu Dec  9 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-2
- Fixed useragent

* Thu Dec  9 2010 Jan Horak <jhorak@redhat.com> - 3.1.7-1
- Update to 3.1.7

* Sat Nov 27 2010 Remi Collet <fedora@famillecollet.com> - 3.1.6-8
- fix cairo + nspr required version
- lightning: fix thunderbird version required
- lightning: fix release (b3pre)
- lightning: clean install

* Mon Nov 22 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-7
- Added x-scheme-handler/mailto to thunderbird.desktop file

* Mon Nov  8 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-4
- Added libnotify patch
- Removed dependency on static libraries

* Fri Oct 29 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-2
- Move thunderbird-lightning extension from Sunbird package to Thunderbird

* Wed Oct 27 2010 Jan Horak <jhorak@redhat.com> - 3.1.6-1
- Update to 3.1.6

* Tue Oct 19 2010 Jan Horak <jhorak@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Thu Sep 16 2010 Dan Horák <dan[at]danny.cz> - 3.1.3-2
- fix build on s390

* Tue Sep  7 2010 Jan Horak <jhorak@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Fri Aug  6 2010 Jan Horak <jhorak@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Disable updater

* Tue Jul 20 2010 Jan Horak <jhorak@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Thu Jun 24 2010 Jan Horak <jhorak@redhat.com> - 3.1-1
- Thunderbird 3.1

* Fri Jun 11 2010 Jan Horak <jhorak@redhat.com> - 3.1-0.3.rc2
- TryExec added to desktop file

* Wed Jun  9 2010 Christopher Aillon <caillon@redhat.com> 3.1-0.2.rc2
- Thunderbird 3.1 RC2

* Tue May 25 2010 Christopher Aillon <caillon@redhat.com> 3.1-0.1.rc1
- Thunderbird 3.1 RC1

* Fri Apr 30 2010 Jan Horak <jhorak@redhat.com> - 3.0.4-3
- Fix for mozbz#550455

* Tue Apr 13 2010 Martin Stransky <stransky@redhat.com> - 3.0.4-2
- Fixed langpacks (#580444)

* Tue Mar 30 2010 Jan Horak <jhorak@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Sat Mar 06 2010 Kalev Lember <kalev@smartlink.ee> - 3.0.3-2
- Own extension directories (#532132)

* Mon Mar  1 2010 Jan Horak <jhorak@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Thu Feb 25 2010 Jan Horak <jhorak@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Wed Jan 20 2010 Martin Stransky <stransky@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Jan 18 2010 Martin Stransky <stransky@redhat.com> - 3.0-5
- Added fix for #480603 - thunderbird takes 
  unacceptably long time to start

* Wed Dec  9 2009 Jan Horak <jhorak@redhat.com> - 3.0-4
- Update to 3.0

* Thu Dec  3 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.13.rc2
- Update to RC2

* Wed Nov 25 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.12.rc1
- Sync with Mozilla latest RC1 build

* Thu Nov 19 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.11.rc1
- Update to RC1

* Thu Sep 17 2009 Christopher Aillon <caillon@redhat.com> - 3.0-3.9.b4
- Update to 3.0 b4

* Thu Aug  6 2009 Martin Stransky <stransky@redhat.com> - 3.0-3.8.beta3
- Added fix for #437596
- Removed unused patches

* Thu Aug  6 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.7.beta3
- Removed unused build requirements

* Mon Aug  3 2009 Jan Horak <jhorak@redhat.com> - 3.0-3.6.beta3
- Build with system hunspell

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3.5.b3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.5.beta3
- Use system hunspell

* Tue Jul 21 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.4.beta3
- Update to 3.0 beta3

* Mon Mar 30 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.2.beta2
- Fixed open-browser.sh to use xdg-open instead of gnome-open

* Mon Mar 23 2009 Christopher Aillon <caillon@redhat.com> - 3.0-2.1.beta2
- Disable the default app nag dialog

* Tue Mar 17 2009 Jan Horak <jhorak@redhat.com> - 3.0-2.beta2
- Fixed clicked link does not open in browser (#489120)
- Fixed missing help in thunderbird (#488885)

* Mon Mar  2 2009 Jan Horak <jhorak@redhat.com> - 3.0-1.beta2
- Update to 3.0 beta2
- Added Patch2 to build correctly when building with --enable-shared option 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Christopher Aillon <caillon@redhat.com> - 2.0.0.18-2
- Disable the crash dialog

* Wed Nov 19 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.18-1
- Update to 2.0.0.18

* Thu Oct  9 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.17-1
- Update to 2.0.0.17

* Wed Jul 23 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.16-1
- Update to 2.0.0.16

* Thu May  1 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.14-1
- Update to 2.0.0.14
- Use the system dictionaries

* Fri Apr 18 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-6
- Icon belongs in _datadir/pixmaps

* Fri Apr 18 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-5
- rebuilt

* Mon Apr  7 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-4
- Add %%lang attributes to langpacks

* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-3
- Avoid conflict between gecko debuginfos

* Mon Mar 03 2008 Martin Stransky <stransky@redhat.com> 2.0.0.12-2
- Updated starting script (#426331)

* Tue Feb 26 2008 Christopher Aillon <caillon@redhat.com> 2.0.0.12-1
- Update to 2.0.0.12
- Fix up icon location and some scriptlets

* Sun Dec  9 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-2
- Fix some rpmlint warnings
- Drop some old patches and obsoletes

* Thu Nov 15 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.9-1
- Update to 2.0.0.9

* Wed Sep 26 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-6
- Fixed #242657 - firefox -g doesn't work

* Tue Sep 25 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-5
- Removed hardcoded MAX_PATH, PATH_MAX and MAXPATHLEN macros

* Tue Sep 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-4
- Fix crashes when using GTK+ themes containing a gtkrc which specify 
  GtkOptionMenu::indicator_size and GtkOptionMenu::indicator_spacing

* Mon Sep 10 2007 Martin Stransky <stransky@redhat.com> 2.0.0.6-3
- added fix for #246248 - firefox crashes when searching for word "do"

* Mon Aug 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-2
- Update the license tag

* Wed Aug  8 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.6-1
- Update to 2.0.0.6
- Own the application directory (#244901)

* Tue Jul 31 2007 Martin Stransky <stransky@redhat.com> 2.0.0.0-3
- added pango ligature fix

* Thu Apr 19 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-1
- Update to 2.0.0.0 Final

* Fri Apr 13 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.5.rc1
- Fix the desktop file
- Clean up the files list
- Remove the default client stuff from the pref window

* Thu Apr 12 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.4.rc1
- Rebuild into Fedora

* Wed Apr 11 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.3.rc1
- Update langpacks

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.2.rc1
- Build option tweaks
- Bring the install section to parity with Firefox's

* Thu Apr  5 2007 Christopher Aillon <caillon@redhat.com> 2.0.0.0-0.1.rc1
- Update to 2.0.0.0 RC1

* Sun Mar 25 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.11-1
- Update to 1.5.0.11

* Fri Mar 2 2007 Martin Stransky <stransky@redhat.com> 1.5.0.10-1
- Update to 1.5.0.10

* Mon Feb 12 2007 Martin Stransky <stransky@redhat.com> 1.5.0.9-8
- added fix for #227406: garbage characters on some websites
  (when pango is disabled)
  
* Tue Jan 30 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.9-7
- Updated cursor position patch from tagoh to fix issue with "jumping"
  cursor when in a textfield with tabs.

* Tue Jan 30 2007 Christopher Aillon <caillon@redhat.com> 1.5.0.9-6
- Fix the DND implementation to not grab, so it works with new GTK+.

* Thu Dec 21 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-5
- Added firefox-1.5-pango-underline.patch

* Wed Dec 20 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-4
- Added firefox-1.5-pango-justified-range.patch

* Tue Dec 19 2006 Behdad Esfahbod <besfahbo@redhat.com> 1.5.0.9-3
- Added firefox-1.5-pango-cursor-position-more.patch

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> 1.5.0.9-2
- Add a Requires: launchmail  (#219884)

* Tue Dec 19 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.9-1
- Update to 1.5.0.9
- Take firefox's pango fixes
- Don't offer to import...nothing.

* Tue Nov  7 2006 Christopher Aillon <caillon@redhat.com> 1.5.0.8-1
- Update to 1.5.0.8
- Allow choosing of download directory
- Take the user to the correct directory from the Download Manager.
- Patch to add support for printing via pango from Behdad.

* Sun Oct  8 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-4
- Default to use of system colors

* Wed Oct  4 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-3
- Bring the invisible character to parity with GTK+

* Wed Sep 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-2
- Fix crash when changing gtk key theme
- Prevent UI freezes while changing GNOME theme
- Remove verbiage about pango; no longer required by upstream.

* Wed Sep 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.7-1
- Update to 1.5.0.7

* Thu Sep  7 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-8
- Shuffle order of the install phase around

* Thu Sep  7 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-7
- Let there be art for Alt+Tab again
- s/tbdir/mozappdir/g

* Wed Sep  6 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-6
- Fix for cursor position in editor widgets by tagoh and behdad (#198759)

* Tue Sep  5 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-5
- Update nopangoxft.patch
- Fix rendering of MathML thanks to Behdad Esfahbod.
- Update start page text to reflect the MathML fixes.
- Enable pango by default on all locales
- Build using -rpath
- Re-enable GCC visibility

* Thu Aug  3 2006 Kai Engert <kengert@redhat.com> - 1.5.0.5-4
- Fix a build failure in mailnews mime code.

* Tue Aug  1 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.0.5-3
- Rebuild

* Thu Jul 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.5-2
- Update to 1.5.0.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5.0.4-2.1
- rebuild

* Mon Jun 12 2006 Kai Engert <kengert@redhat.com> - 1.5.0.4-2
- Update to 1.5.0.4
- Fix desktop-file-utils requires

* Wed Apr 19 2006 Christopher Aillon <caillon@redhat.com> - 1.5.0.2-2
- Update to 1.5.0.2

* Thu Mar 16 2006 Christopher Aillon <caillon@redhat.com> - 1.5-7
- Bring the other arches back

* Mon Mar 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5.6
- Temporarily disable other arches that we don't ship FC5 with, for time

* Mon Mar 13 2006 Christopher Aillon <caillon@redhat.com> - 1.5-5
- Add a notice to the mail start page denoting this is a pango enabled build.

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 1.5-3
- Add dumpstack.patch
- Improve the langpack install stuff

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.5-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Christopher Aillon <caillon@redhat.com> - 1.5-2
- Add some langpacks back in
- Stop providing MozillaThunderbird

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 1.5-1
- Official 1.5 release is out

* Wed Jan 11 2006 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.6.rc1
- Fix crash when deleting highlighted text while composing mail within
  plaintext editor with spellcheck enabled.

* Tue Jan  3 2006 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.5.rc1
- Looks like we can build on ppc64 again.

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.4.rc1
- Rebuild

* Fri Dec 16 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.3.rc1
- Once again, disable ppc64 because of a new issue.
  See https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=175944

- Use the system NSS libraries
- Build on ppc64

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Christopher Aillon <caillon@redhat.com> - 1.5-0.5.1.rc1
- Fix issue with popup dialogs and other actions causing lockups

* Sat Nov  5 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.rc1
- Update to 1.5 rc1

* Sat Oct  8 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta2
- Update to 1.5 beta2

* Wed Sep 28 2005 Christopher Aillon <caillon@redhat.com> 1.5-0.5.0.beta1
- Update to 1.5 beta1
- Bring the install phase of the spec file up to speed

* Sun Aug 14 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-4
- Rebuild

* Sat Aug  6 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-3
- Add patch to make file chooser dialog modal

* Fri Jul 22 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-2
- Update to 1.0.6

* Mon Jul 18 2005 Christopher Aillon <caillon@redhat.com> 1.0.6-0.1.fc5
- 1.0.6 Release Candidate

* Fri Jul 15 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-8
- Use system NSPR
- Fix crash on 64bit platforms (#160330)

* Thu Jun 23 2005 Kristian Høgsberg <krh@redhat.com>  1.0.2-7
- Add firefox-1.0-pango-cairo.patch to get rid of the last few Xft
  references, fixing the "no fonts" problem.

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-6
- Change the Exec line in the desktop file to `thunderbird`

* Fri May 13 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-5
- Update pango patche, MOZ_DISABLE_PANGO now works as advertised.

* Mon May  9 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-4
- Add temporary workaround to not create files in the user's $HOME (#149664)

* Wed May  4 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-3
- Don't have downloads "disappear" when downloading to desktop (#139015)
- Fix for some more cursor issues in textareas (149991, 150002, 152089)
- Add upstream patch to fix bidi justification of pango
- Add patch to fix launching of helper applications
- Add patch to properly link against libgfxshared_s.a
- Fix multilib conflicts

* Wed Apr 27 2005 Warren Togami <wtogami@redhat.com>
- correct confusing PANGO vars in startup script

* Wed Mar 23 2005 Christopher Aillon <caillon@redhat.com> 1.0.2-1
- Thunderbird 1.0.2

* Tue Mar  8 2005 Christopher Aillon <caillon@redhat.com> 1.0-5
- Add patch to compile against new fortified glibc macros

* Sat Mar  5 2005 Christopher Aillon <caillon@redhat.com> 1.0-4
- Rebuild against GCC 4.0
- Add execshield patches
- Minor specfile cleanup

* Mon Dec 20 2004 Christopher Aillon <caillon@redhat.com> 1.0-3
- Rebuild

* Thu Dec 16 2004 Christopher Aillon <caillon@redhat.com> 1.0-2
- Add RPM version to useragent

* Thu Dec 16 2004 Christopher Blizzard <blizzard@redhat.com>
- Port over pango patches from firefox

* Wed Dec  8 2004 Christopher Aillon <caillon@redhat.com> 1.0-1
- Thunderbird 1.0

* Mon Dec  6 2004 Christopher Aillon <caillon@redhat.com> 1.0-0.rc1.1
- Fix advanced prefs

* Fri Dec  3 2004 Christopher Aillon <caillon@redhat.com>
- Make this run on s390(x) now for real

* Wed Dec  1 2004 Christopher Aillon <caillon@redhat.com> 1.0-0.rc1.0
- Update to 1.0 rc1

* Fri Nov 19 2004 Christopher Aillon <caillon@redhat.com>
- Add patches to build and run on s390(x)

* Thu Nov 11 2004 Christopher Aillon <caillon@redhat.com> 0.9.0-2
- Rebuild to fix file chooser

* Fri Nov  5 2004 Christopher Aillon <caillon@redhat.com> 0.9.0-1
- Update to 0.9

* Fri Oct 22 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-10
- Prevent inlining of stack direction detection (#135255)

* Tue Oct 19 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-9
- More file chooser fixes (same as in firefox)
- Fix for upstream 28327.

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-8
- Update the pango patch

* Mon Oct 18 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-8
- Pull over patches from firefox build:
  - disable default application dialog
  - don't include software update since it doesn't work
  - make external app support work

* Thu Oct 14 2004 Christopher Blizzard <blizzard@redhat.com> 0.8.0-7
- Use pango for rendering

* Tue Oct 12 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-6
- Fix for 64 bit crash at startup (b.m.o #256603)

* Sat Oct  9 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-5
- Add patches to fix xremote (#135036)

* Fri Oct  8 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-4
- Add patch to fix button focus issues (#133507)
- Add patch for fix IMAP race issues (bmo #246439)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 0.8.0-3
- filter out library Provides: and internal Requires:

* Tue Sep 28 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-2
- Backport the GTK+ File Chooser.
- Add fix for JS math on x86_64 systems
- Add pkgconfig patch

* Thu Sep 16 2004 Christopher Aillon <caillon@redhat.com> 0.8.0-1
- Update to 0.8.0
- Remove enigmail
- Update BuildRequires
- Remove gcc34 and extension manager patches -- they are upstreamed.
- Fix for gnome-vfs2 error at component registration

* Fri Sep 03 2004 Christopher Aillon <caillon@redhat.com> 0.7.3-5
- Build with --disable-xprint

* Wed Sep 01 2004 David Hill <djh[at]ii.net> 0.7.3-4
- remove all Xvfb-related hacks

* Wed Sep 01 2004 Warren Togami <wtogami@redhat.com> 
- actually apply psfonts
- add mozilla gnome-uriloader patch to prevent build failure

* Tue Aug 31 2004 Warren Togami <wtogami@redhat.com> 0.7.3-3
- rawhide import
- apply NetBSD's freetype 2.1.8 patch
- apply psfonts patch
- remove BR on /usr/bin/ex, breaks beehive

* Tue Aug 31 2004 David Hill <djh[at]ii.net> 0.7.3-0.fdr.2
- oops, fix %%install

* Thu Aug 26 2004 David Hill <djh[at]ii.net> 0.7.3-0.fdr.1
- update to Thunderbird 0.7.3 and Enigmail 0.85.0
- remove XUL.mfasl on startup, add Debian enigmail patches
- add Xvfb hack for -install-global-extension

* Wed Jul 14 2004 David Hill <djh[at]ii.net> 0.7.2-0.fdr.0
- update to 0.7.2, just because it's there
- update gcc-3.4 patch (Kaj Niemi)
- add EM registration patch and remove instdir hack

* Sun Jul 04 2004 David Hill <djh[at]ii.net> 0.7.1-0.fdr.1
- re-add Enigmime 1.0.7, omit Enigmail until the Mozilla EM problems are fixed

* Wed Jun 30 2004 David Hill <djh[at]ii.net> 0.7.1-0.fdr.0
- update to 0.7.1
- remove Enigmail

* Mon Jun 28 2004 David Hill <djh[at]ii.net> 0.7-0.fdr.1
- re-enable Enigmail 0.84.1
- add gcc-3.4 patch (Kaj Niemi)
- use official branding (with permission)

* Fri Jun 18 2004 David Hill <djh[at]ii.net> 0.7-0.fdr.0
- update to 0.7
- temporarily disable Enigmail 0.84.1, make ftp links work (#1634)
- specify libdir, change BR for apt (V. Skyttä, #1617)

* Tue May 18 2004 Warren Togami <wtogami@redhat.com> 0.6-0.fdr.5
- temporary workaround for enigmail skin "modern" bug

* Mon May 10 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.4
- update to Enigmail 0.84.0 
- update launch script

* Mon May 10 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.3
- installation directory now versioned
- allow root to run the program (for installing extensions)
- remove unnecessary %%pre and %%post
- remove separators, update mozconfig and launch script (M. Schwendt, #1460)

* Wed May 05 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.2
- include Enigmail, re-add release notes
- delete %%{_libdir}/thunderbird in %%pre

* Mon May 03 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.1
- update to Thunderbird 0.6

* Fri Apr 30 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.0.rc1
- update to Thunderbird 0.6 RC1
- add new icon, remove release notes

* Thu Apr 15 2004 David Hill <djh[at]ii.net> 0.6-0.fdr.0.20040415
- update to latest CVS, update mozconfig and %%build accordingly
- update to Enigmail 0.83.6
- remove x-remote and x86_64 patches
- build with -Os

* Thu Apr 15 2004 David Hill <djh[at]ii.net> 0.5-0.fdr.12
- update x-remote patch
- more startup script fixes

* Tue Apr 06 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.11
- startup script fixes, and a minor cleanup

* Sun Apr 04 2004 Warren Togami <wtogami@redhat.com> 0:0.5-0.fdr.10
- Minor cleanups

* Sun Apr 04 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.8
- minor improvements to open-browser.sh and startup script
- update to latest version of Blizzard's x-remote patch

* Thu Mar 25 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.7
- update open-browser.sh, startup script, and BuildRequires

* Sun Mar 14 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.6
- update open-browser script, modify BuildRequires (Warren)
- add Blizzard's x-remote patch
- initial attempt at x-remote-enabled startup script

* Sun Mar 07 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.5
- refuse to run with excessive privileges

* Fri Feb 27 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.4
- add Mozilla x86_64 patch (Oliver Sontag)
- Enigmail source filenames now include the version
- modify BuildRoot

* Thu Feb 26 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.3
- use the updated official tarball

* Wed Feb 18 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.2
- fix %%prep script

* Mon Feb 16 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.1
- update Enigmail to 0.83.3
- use official source tarball (after removing the CRLFs)
- package renamed to thunderbird

* Mon Feb 09 2004 David Hill <djh[at]ii.net> 0:0.5-0.fdr.0
- update to 0.5
- check for lockfile before launching

* Fri Feb 06 2004 David Hill <djh[at]ii.net>
- update to latest cvs
- update to Enigmail 0.83.2

* Thu Jan 29 2004 David Hill <djh[at]ii.net> 0:0.4-0.fdr.5
- update to Enigmail 0.83.1
- removed Mozilla/Firebird script patching

* Sat Jan 03 2004 David Hill <djh[at]ii.net> 0:0.4-0.fdr.4
- add startup notification to .desktop file

* Thu Dec 25 2003 Warren Togami <warren@togami.com> 0:0.4-0.fdr.3
- open-browser.sh release 3
- patch broken /usr/bin/mozilla script during install
- dir ownership
- XXX: Source fails build on x86_64... fix later

* Tue Dec 23 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.2
- update to Enigmail 0.82.5
- add Warren's open-browser.sh (#1113)

* Tue Dec 09 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.1
- use Thunderbird's mozilla-xremote-client to launch browser

* Sun Dec 07 2003 David Hill <djh[at]ii.net> 0:0.4-0.fdr.0
- update to 0.4
- make hyperlinks work (with recent versions of Firebird/Mozilla)

* Thu Dec 04 2003 David Hill <djh[at]ii.net>
- update to 0.4rc2

* Wed Dec 03 2003 David Hill <djh[at]ii.net>
- update to 0.4rc1 and Enigmail 0.82.4

* Thu Nov 27 2003 David Hill <djh[at]ii.net>
- update to latest CVS and Enigmail 0.82.3

* Sun Nov 16 2003 David Hill <djh[at]ii.net>
- update to latest CVS (0.4a)
- update Enigmail to 0.82.2
- alter mozconfig for new build requirements
- add missing BuildReq (#987)

* Thu Oct 16 2003 David Hill <djh[at]ii.net> 0:0.3-0.fdr.0
- update to 0.3

* Sun Oct 12 2003 David Hill <djh[at]ii.net> 0:0.3rc3-0.fdr.0
- update to 0.3rc3
- update Enigmail to 0.81.7

* Thu Oct 02 2003 David Hill <djh[at]ii.net> 0:0.3rc2-0.fdr.0
- update to 0.3rc2

* Wed Sep 17 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.2
- simplify startup script

* Wed Sep 10 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.1
- add GPG support (Enigmail 0.81.6)
- specfile fixes (#679)

* Thu Sep 04 2003 David Hill <djh[at]ii.net> 0:0.2-0.fdr.0
- update to 0.2

* Mon Sep 01 2003 David Hill <djh[at]ii.net>
- initial RPM
  (based on the fedora MozillaFirebird-0.6.1 specfile)
