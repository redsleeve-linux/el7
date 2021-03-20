# RPM conditionals so as to be able to dynamically produce
# slowdebug/release builds. See:
# http://rpm.org/user_doc/conditional_builds.html
#
# Examples:
#
# Produce release *and* slowdebug builds on x86_64 (default):
# $ rpmbuild -ba java-1.8.0-openjdk.spec
#
# Produce only release builds (no slowdebug builds) on x86_64:
# $ rpmbuild -ba java-1.8.0-openjdk.spec --without slowdebug
#
# Only produce a release build on x86_64:
# $ fedpkg mockbuild --without slowdebug
#
# Only produce a debug build on x86_64:
# $ fedpkg local --without release
#
# Enable slowdebug builds by default on relevant arches.
%bcond_without slowdebug
# Enable release builds by default on relevant arches.
%bcond_without release

# Workaround for stripping of debug symbols from static libraries
# RHEL 7 doesn't have __brp_strip_static_archive so need to redefine
# the entire os_install_post macro
%define __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    %{!?__debug_package:\
    /usr/lib/rpm/redhat/brp-strip %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
    } \
    %{!?__jar_repack:/usr/lib/rpm/redhat/brp-java-repack-jars} \
%{nil}

# The -g flag says to use strip -g instead of full strip on DSOs or EXEs.
# This fixes detailed NMT and other tools which need minimal debug info.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1520879
%global _find_debuginfo_opts -g

# note: parametrized macros are order-sensitive (unlike not-parametrized) even with normal macros
# also necessary when passing it as parameter to other macros. If not macro, then it is considered a switch
# see the difference between global and define:
# See https://github.com/rpm-software-management/rpm/issues/127 to comments at  "pmatilai commented on Aug 18, 2017"
# (initiated in https://bugzilla.redhat.com/show_bug.cgi?id=1482192)
%global debug_suffix_unquoted -debug
# quoted one for shell operations
%global debug_suffix "%{debug_suffix_unquoted}"
%global normal_suffix ""

# if you want only debug build but providing java build only normal build but set normalbuild_parameter
%global debug_warning This package is unoptimised with full debugging. Install only as needed and remove ASAP.
%global debug_on with full debugging on
%global for_debug for packages with debugging on

%if %{with release}
%global include_normal_build 1
%else
%global include_normal_build 0
%endif

%if %{include_normal_build}
%global build_loop1 %{normal_suffix}
%else
%global build_loop1 %{nil}
%endif

%global aarch64         aarch64 arm64 armv8
# we need to distinguish between big and little endian PPC64
%global ppc64le         ppc64le
%global ppc64be         ppc64 ppc64p7
# Set of architectures which support multiple ABIs
%global multilib_arches %{power64} sparc64 x86_64
# Set of architectures for which we build slowdebug builds
%global debug_arches    %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64} s390x
# Set of architectures with a Just-In-Time (JIT) compiler
%global jit_arches      %{debug_arches} %{arm}
# Set of architectures which run a full bootstrap cycle
%global bootstrap_arches %{jit_arches}
# Set of architectures which support SystemTap tapsets
%global systemtap_arches %{jit_arches}
# Set of architectures with a Ahead-Of-Time (AOT) compiler
%global aot_arches      x86_64 %{aarch64}
# Set of architectures which support the serviceability agent
%global sa_arches       %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64} %{arm}
# Set of architectures which support class data sharing
# As of JDK-8005165 in OpenJDK 10, class sharing is not arch-specific
# However, it does segfault on the Zero assembler port, so currently JIT only
%global share_arches    %{jit_arches}
# Set of architectures for which we build the Shenandoah garbage collector
%global shenandoah_arches x86_64 %{aarch64}
# Set of architectures for which we build the Z garbage collector
%global zgc_arches x86_64
# Set of architectures for which alt-java has SSB mitigation
%global ssbd_arches x86_64

# By default, we build a debug build during main build on JIT architectures
%if %{with slowdebug}
%ifarch %{debug_arches}
%global include_debug_build 1
%else
%global include_debug_build 0
%endif
%else
%global include_debug_build 0
%endif

# On certain architectures, we compile the Shenandoah GC
%ifarch %{shenandoah_arches}
%global use_shenandoah_hotspot 1
%global shenandoah_feature shenandoahgc
%else
%global use_shenandoah_hotspot 0
%global shenandoah_feature -shenandoahgc
%endif

# On certain architectures, we compile the ZGC
%ifarch %{zgc_arches}
%global use_zgc_hotspot 1
%global zgc_feature zgc
%else
%global use_zgc_hotspot 0
%global zgc_feature -zgc
%endif

%if %{include_debug_build}
%global build_loop2 %{debug_suffix}
%else
%global build_loop2 %{nil}
%endif

# if you disable both builds, then the build fails
# Note that the debug build requires the normal build for docs
%global build_loop  %{build_loop1} %{build_loop2}
# note: that order: normal_suffix debug_suffix, in case of both enabled
# is expected in one single case at the end of the build
%global rev_build_loop  %{build_loop2} %{build_loop1}

%ifarch %{bootstrap_arches}
%global bootstrap_build 1
%else
%global bootstrap_build 1
%endif

%if %{bootstrap_build}
%global release_targets bootcycle-images static-libs-image docs-zip
%else
%global release_targets images docs-zip static-libs-image
%endif
# No docs nor bootcycle for debug builds
%global debug_targets images static-libs-image


# Filter out flags from the optflags macro that cause problems with the OpenJDK build
# We filter out -O flags so that the optimization of HotSpot is not lowered from O3 to O2
# We filter out -Wall which will otherwise cause HotSpot to produce hundreds of thousands of warnings (100+mb logs)
# We replace it with -Wformat (required by -Werror=format-security) and -Wno-cpp to avoid FORTIFY_SOURCE warnings
# We filter out -fexceptions as the HotSpot build explicitly does -fno-exceptions and it's otherwise the default for C++
%global ourflags %(echo %optflags | sed -e 's|-Wall|-Wformat -Wno-cpp|' | sed -r -e 's|-O[0-9]*||')
%global ourcppflags %(echo %ourflags | sed -e 's|-fexceptions||')
%global ourldflags %{__global_ldflags}

# With disabled nss is NSS deactivated, so NSS_LIBDIR can contain the wrong path
# the initialization must be here. Later the pkg-config have buggy behavior
# looks like openjdk RPM specific bug
# Always set this so the nss.cfg file is not broken
%global NSS_LIBDIR %(pkg-config --variable=libdir nss)

# fix for https://bugzilla.redhat.com/show_bug.cgi?id=1111349
%global _privatelibs libsplashscreen[.]so.*|libawt_xawt[.]so.*|libjli[.]so.*|libattach[.]so.*|libawt[.]so.*|libextnet[.]so.*|libawt_headless[.]so.*|libdt_socket[.]so.*|libfontmanager[.]so.*|libharfbuzz[.]so.*|libinstrument[.]so.*|libj2gss[.]so.*|libj2pcsc[.]so.*|libj2pkcs11[.]so.*|libjaas[.]so.*|libjavajpeg[.]so.*|libjdwp[.]so.*|libjimage[.]so.*|libjsound[.]so.*|liblcms[.]so.*|libmanagement[.]so.*|libmanagement_agent[.]so.*|libmanagement_ext[.]so.*|libmlib_image[.]so.*|libnet[.]so.*|libnio[.]so.*|libprefs[.]so.*|librmi[.]so.*|libsaproc[.]so.*|libsctp[.]so.*|libsunec[.]so.*|libunpack[.]so.*|libzip[.]so.*

%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

# In some cases, the arch used by the JDK does
# not match _arch.
# Also, in some cases, the machine name used by SystemTap
# does not match that given by _target_cpu
%ifarch x86_64
%global archinstall amd64
%global stapinstall x86_64
%endif
%ifarch ppc
%global archinstall ppc
%global stapinstall powerpc
%endif
%ifarch %{ppc64be}
%global archinstall ppc64
%global stapinstall powerpc
%endif
%ifarch %{ppc64le}
%global archinstall ppc64le
%global stapinstall powerpc
%endif
%ifarch %{ix86}
%global archinstall i686
%global stapinstall i386
%endif
%ifarch ia64
%global archinstall ia64
%global stapinstall ia64
%endif
%ifarch s390
%global archinstall s390
%global stapinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%global stapinstall s390
%endif
%ifarch %{arm}
%global archinstall arm
%global stapinstall arm
%endif
%ifarch %{aarch64}
%global archinstall aarch64
%global stapinstall arm64
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%global stapinstall %{_target_cpu}
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%global stapinstall %{_target_cpu}
%endif
# Need to support noarch for srpm build
%ifarch noarch
%global archinstall %{nil}
%global stapinstall %{nil}
%endif

%ifarch %{systemtap_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# New Version-String scheme-style defines
%global featurever 11
%global interimver 0
%global updatever 10
%global patchver 0
# If you bump featurever, you must bump also vendor_version_string
# Used via new version scheme. JDK 11 was
# GA'ed in September 2018 => 18.9
%global vendor_version_string 18.9
# buildjdkver is usually same as %%{featurever},
# but in time of bootstrap of next jdk, it is featurever-1,
# and this it is better to change it here, on single place
%global buildjdkver %{featurever}
# Add LTS designator for RHEL builds
%if 0%{?rhel}
  %global lts_designator "LTS"
  %global lts_designator_zip -%{lts_designator}
%else
  %global lts_designator ""
  %global lts_designator_zip ""
%endif

# Define vendor information used by OpenJDK
%global oj_vendor Red Hat, Inc.
%global oj_vendor_url "https://www.redhat.com/"
# Define what url should JVM offer in case of a crash report
# order may be important, epel may have rhel declared
%if 0%{?epel}
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora%20EPEL&component=%{name}&version=epel%{epel}
%else
%if 0%{?fedora}
# Does not work for rawhide, keeps the version field empty
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora&component=%{name}&version=%{fedora}
%else
%if 0%{?rhel}
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Red%20Hat%20Enterprise%20Linux%20%{rhel}&component=%{name}
%else
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi
%endif
%endif
%endif

# Define IcedTea version used for SystemTap tapsets and desktop file
%global icedteaver      3.15.0

# Standard JPackage naming and versioning defines
%global origin          openjdk
%global origin_nice     OpenJDK
%global top_level_dir_name   %{origin}
%global buildver        9
%global rpmrelease      1
#%%global tagsuffix      %%{nil}
# priority must be 7 digits in total
# setting to 1, so debug ones can have 0
%global priority        00000%{interimver}1
%global newjavaver      %{featurever}.%{interimver}.%{updatever}.%{patchver}

# Omit trailing 0 in filenames when the patch version is 0
%if 0%{?patchver} > 0
%global filever %{newjavaver}
%else
%global filever %{featurever}.%{interimver}.%{updatever}
%endif

%global javaver         %{featurever}

# Define milestone (EA for pre-releases, GA for releases)
# Release will be (where N is usually a number starting at 1):
# - 0.N%%{?extraver}%%{?dist} for EA releases,
# - N%%{?extraver}{?dist} for GA releases
%global is_ga           1
%if %{is_ga}
%global ea_designator ""
%global ea_designator_zip ""
%global extraver %{nil}
%global eaprefix %{nil}
%else
%global ea_designator ea
%global ea_designator_zip -%{ea_designator}
%global extraver .%{ea_designator}
%global eaprefix 0.
%endif

# parametrized macros are order-sensitive
%global compatiblename  java-%{featurever}-%{origin}
%global fullversion     %{compatiblename}-%{version}-%{release}
# images directories from upstream build
%global jdkimage                jdk
%global static_libs_image       static-libs
# output dir stub
%global buildoutputdir() %{expand:openjdk/build%1}
# we can copy the javadoc to not arched dir, or make it not noarch
# javadoc is no longer noarch, as it have aot on only some arches
%global uniquejavadocdir()    %{expand:%{fullversion}.%{_arch}%1}
# main id and dir of this jdk
%global uniquesuffix()        %{expand:%{fullversion}.%{_arch}%1}

# Standard JPackage directories and symbolic links.
%global sdkdir()        %{expand:%{uniquesuffix %%1}}
%global jrelnk()        %{expand:jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}%1}

%global sdkbindir()     %{expand:%{_jvmdir}/%{sdkdir %%1}/bin}
%global jrebindir()     %{expand:%{_jvmdir}/%{sdkdir %%1}/bin}

%global alt_java_name     alt-java

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/

%if %{with_systemtap}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific sub-dir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinguish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka target_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdirttapset %{tapsetroot}/tapset/
%global tapsetdir %{tapsetdirttapset}/%{stapinstall}
%endif

# not-duplicated scriptlets for normal/debug packages
%global update_desktop_icons /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%define post_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0
}


%define post_headless() %{expand:
%ifarch %{share_arches}
%{jrebindir %%1}/java -Xshare:dump >/dev/null 2>/dev/null
%endif

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

ext=.gz
alternatives \\
  --install %{_bindir}/java java %{jrebindir %%1}/java $PRIORITY  --family %{name}.%{_arch} \\
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{sdkdir %%1} \\
  --slave %{_bindir}/%{alt_java_name} %{alt_java_name} %{jrebindir %%1}/%{alt_java_name} \\
  --slave %{_bindir}/jjs jjs %{jrebindir %%1}/jjs \\
  --slave %{_bindir}/keytool keytool %{jrebindir %%1}/keytool \\
  --slave %{_bindir}/pack200 pack200 %{jrebindir %%1}/pack200 \\
  --slave %{_bindir}/rmid rmid %{jrebindir %%1}/rmid \\
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir %%1}/rmiregistry \\
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir %%1}/unpack200 \\
  --slave %{_mandir}/man1/java.1$ext java.1$ext \\
  %{_mandir}/man1/java-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/%{alt_java_name}.1$ext %{alt_java_name}.1$ext \\
  %{_mandir}/man1/%{alt_java_name}-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jjs.1$ext jjs.1$ext \\
  %{_mandir}/man1/jjs-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \\
  %{_mandir}/man1/keytool-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \\
  %{_mandir}/man1/pack200-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \\
  %{_mandir}/man1/rmid-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \\
  %{_mandir}/man1/rmiregistry-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \\
  %{_mandir}/man1/unpack200-%{uniquesuffix %%1}.1$ext

for X in %{origin} %{javaver} ; do
  alternatives --install %{_jvmdir}/jre-"$X" jre_"$X" %{_jvmdir}/%{sdkdir %%1} $PRIORITY --family %{name}.%{_arch}
done

update-alternatives --install %{_jvmdir}/jre-%{javaver}-%{origin} jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk %%1} $PRIORITY  --family %{name}.%{_arch}


update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

# see pretrans where this file is declared
# also see that pretrans is only for non-debug
if [ ! "%1" == %{debug_suffix} ]; then
  if [ -f %{_libexecdir}/copy_jdk_configs_fixFiles.sh ] ; then
    sh  %{_libexecdir}/copy_jdk_configs_fixFiles.sh %{rpm_state_dir}/%{name}.%{_arch}  %{_jvmdir}/%{sdkdir %%1}
  fi
fi

exit 0
}

%global postun_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}


%global postun_headless() %{expand:
  alternatives --remove java %{jrebindir %%1}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk %%1}
}

%global posttrans_script() %{expand:
%{update_desktop_icons}
}

%global post_devel() %{expand:

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

ext=.gz
alternatives \\
  --install %{_bindir}/javac javac %{sdkbindir %%1}/javac $PRIORITY  --family %{name}.%{_arch} \\
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir %%1} \\
%ifarch %{aot_arches}
  --slave %{_bindir}/jaotc jaotc %{sdkbindir %%1}/jaotc \\
%endif
  --slave %{_bindir}/jlink jlink %{sdkbindir %%1}/jlink \\
  --slave %{_bindir}/jmod jmod %{sdkbindir %%1}/jmod \\
%ifarch %{sa_arches}
  --slave %{_bindir}/jhsdb jhsdb %{sdkbindir %%1}/jhsdb \\
%endif
  --slave %{_bindir}/jar jar %{sdkbindir %%1}/jar \\
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir %%1}/jarsigner \\
  --slave %{_bindir}/javadoc javadoc %{sdkbindir %%1}/javadoc \\
  --slave %{_bindir}/javap javap %{sdkbindir %%1}/javap \\
  --slave %{_bindir}/jcmd jcmd %{sdkbindir %%1}/jcmd \\
  --slave %{_bindir}/jconsole jconsole %{sdkbindir %%1}/jconsole \\
  --slave %{_bindir}/jdb jdb %{sdkbindir %%1}/jdb \\
  --slave %{_bindir}/jdeps jdeps %{sdkbindir %%1}/jdeps \\
  --slave %{_bindir}/jdeprscan jdeprscan %{sdkbindir %%1}/jdeprscan \\
  --slave %{_bindir}/jfr jfr %{sdkbindir %%1}/jfr \\
  --slave %{_bindir}/jimage jimage %{sdkbindir %%1}/jimage \\
  --slave %{_bindir}/jinfo jinfo %{sdkbindir %%1}/jinfo \\
  --slave %{_bindir}/jmap jmap %{sdkbindir %%1}/jmap \\
  --slave %{_bindir}/jps jps %{sdkbindir %%1}/jps \\
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir %%1}/jrunscript \\
  --slave %{_bindir}/jshell jshell %{sdkbindir %%1}/jshell \\
  --slave %{_bindir}/jstack jstack %{sdkbindir %%1}/jstack \\
  --slave %{_bindir}/jstat jstat %{sdkbindir %%1}/jstat \\
  --slave %{_bindir}/jstatd jstatd %{sdkbindir %%1}/jstatd \\
  --slave %{_bindir}/rmic rmic %{sdkbindir %%1}/rmic \\
  --slave %{_bindir}/serialver serialver %{sdkbindir %%1}/serialver \\
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \\
  %{_mandir}/man1/jar-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \\
  %{_mandir}/man1/jarsigner-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \\
  %{_mandir}/man1/javac-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \\
  %{_mandir}/man1/javadoc-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \\
  %{_mandir}/man1/javap-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jcmd.1$ext jcmd.1$ext \\
  %{_mandir}/man1/jcmd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \\
  %{_mandir}/man1/jconsole-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \\
  %{_mandir}/man1/jdb-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jdeps.1$ext jdeps.1$ext \\
  %{_mandir}/man1/jdeps-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \\
  %{_mandir}/man1/jinfo-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \\
  %{_mandir}/man1/jmap-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \\
  %{_mandir}/man1/jps-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \\
  %{_mandir}/man1/jrunscript-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \\
  %{_mandir}/man1/jstack-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \\
  %{_mandir}/man1/jstat-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \\
  %{_mandir}/man1/jstatd-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \\
  %{_mandir}/man1/rmic-%{uniquesuffix %%1}.1$ext \\
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \\
  %{_mandir}/man1/serialver-%{uniquesuffix %%1}.1$ext \\

for X in %{origin} %{javaver} ; do
  alternatives \\
    --install %{_jvmdir}/java-"$X" java_sdk_"$X" %{_jvmdir}/%{sdkdir %%1} $PRIORITY  --family %{name}.%{_arch}
done

update-alternatives --install %{_jvmdir}/java-%{javaver}-%{origin} java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir %%1} $PRIORITY  --family %{name}.%{_arch}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0
}

%global postun_devel() %{expand:
  alternatives --remove javac %{sdkbindir %%1}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdkdir %%1}
  alternatives --remove java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir %%1}

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
exit 0
}

%global posttrans_devel() %{expand:
%{update_desktop_icons}
}

%global post_javadoc() %{expand:

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

alternatives \\
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{uniquejavadocdir %%1}/api \\
  $PRIORITY  --family %{name}
exit 0
}

%global postun_javadoc() %{expand:
  alternatives --remove javadocdir %{_javadocdir}/%{uniquejavadocdir %%1}/api
exit 0
}

%global post_javadoc_zip() %{expand:

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

alternatives \\
  --install %{_javadocdir}/java-zip javadoczip %{_javadocdir}/%{uniquejavadocdir %%1}.zip \\
  $PRIORITY  --family %{name}
exit 0
}

%global postun_javadoc_zip() %{expand:
  alternatives --remove javadoczip %{_javadocdir}/%{uniquejavadocdir %%1}.zip
exit 0
}

%define files_jre() %{expand:
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}-%{origin}.png
%{_jvmdir}/%{sdkdir %%1}/lib/libsplashscreen.so
%{_jvmdir}/%{sdkdir %%1}/lib/libawt_xawt.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjawt.so
}


%define files_jre_headless() %{expand:
%license %{_jvmdir}/%{sdkdir %%1}/legal
%doc %{_defaultdocdir}/%{uniquejavadocdir %%1}/NEWS
%dir %{_sysconfdir}/.java/.systemPrefs
%dir %{_sysconfdir}/.java
%dir %{_jvmdir}/%{sdkdir %%1}
%{_jvmdir}/%{sdkdir %%1}/release
%{_jvmdir}/%{jrelnk %%1}
%dir %{_jvmdir}/%{sdkdir %%1}/bin
%{_jvmdir}/%{sdkdir %%1}/bin/java
%{_jvmdir}/%{sdkdir %%1}/bin/%{alt_java_name}
%{_jvmdir}/%{sdkdir %%1}/bin/jjs
%{_jvmdir}/%{sdkdir %%1}/bin/keytool
%{_jvmdir}/%{sdkdir %%1}/bin/pack200
%{_jvmdir}/%{sdkdir %%1}/bin/rmid
%{_jvmdir}/%{sdkdir %%1}/bin/rmiregistry
%{_jvmdir}/%{sdkdir %%1}/bin/unpack200
%dir %{_jvmdir}/%{sdkdir %%1}/lib
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir %%1}/lib/classlist
%endif
%{_jvmdir}/%{sdkdir %%1}/lib/jexec
%{_jvmdir}/%{sdkdir %%1}/lib/jspawnhelper
%{_jvmdir}/%{sdkdir %%1}/lib/jrt-fs.jar
%{_jvmdir}/%{sdkdir %%1}/lib/modules
%{_jvmdir}/%{sdkdir %%1}/lib/psfont.properties.ja
%{_jvmdir}/%{sdkdir %%1}/lib/psfontj2d.properties
%{_jvmdir}/%{sdkdir %%1}/lib/tzdb.dat
%dir %{_jvmdir}/%{sdkdir %%1}/lib/jli
%{_jvmdir}/%{sdkdir %%1}/lib/jli/libjli.so
%{_jvmdir}/%{sdkdir %%1}/lib/jvm.cfg
%{_jvmdir}/%{sdkdir %%1}/lib/libattach.so
%{_jvmdir}/%{sdkdir %%1}/lib/libawt.so
%{_jvmdir}/%{sdkdir %%1}/lib/libextnet.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjsig.so
%{_jvmdir}/%{sdkdir %%1}/lib/libawt_headless.so
%{_jvmdir}/%{sdkdir %%1}/lib/libdt_socket.so
%{_jvmdir}/%{sdkdir %%1}/lib/libfontmanager.so
%{_jvmdir}/%{sdkdir %%1}/lib/libharfbuzz.so
%{_jvmdir}/%{sdkdir %%1}/lib/libinstrument.so
%{_jvmdir}/%{sdkdir %%1}/lib/libj2gss.so
%{_jvmdir}/%{sdkdir %%1}/lib/libj2pcsc.so
%{_jvmdir}/%{sdkdir %%1}/lib/libj2pkcs11.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjaas.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjava.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjavajpeg.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjdwp.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjimage.so
%{_jvmdir}/%{sdkdir %%1}/lib/libjsound.so
%{_jvmdir}/%{sdkdir %%1}/lib/liblcms.so
%{_jvmdir}/%{sdkdir %%1}/lib/libmanagement.so
%{_jvmdir}/%{sdkdir %%1}/lib/libmanagement_agent.so
%{_jvmdir}/%{sdkdir %%1}/lib/libmanagement_ext.so
%{_jvmdir}/%{sdkdir %%1}/lib/libmlib_image.so
%{_jvmdir}/%{sdkdir %%1}/lib/libnet.so
%{_jvmdir}/%{sdkdir %%1}/lib/libnio.so
%{_jvmdir}/%{sdkdir %%1}/lib/libprefs.so
%{_jvmdir}/%{sdkdir %%1}/lib/librmi.so
# Some architectures don't have the serviceability agent
%ifarch %{sa_arches}
%{_jvmdir}/%{sdkdir %%1}/lib/libsaproc.so
%endif
%{_jvmdir}/%{sdkdir %%1}/lib/libsctp.so
%{_jvmdir}/%{sdkdir %%1}/lib/libsunec.so
%{_jvmdir}/%{sdkdir %%1}/lib/libunpack.so
%{_jvmdir}/%{sdkdir %%1}/lib/libverify.so
%{_jvmdir}/%{sdkdir %%1}/lib/libzip.so
%dir %{_jvmdir}/%{sdkdir %%1}/lib/jfr
%{_jvmdir}/%{sdkdir %%1}/lib/jfr/default.jfc
%{_jvmdir}/%{sdkdir %%1}/lib/jfr/profile.jfc
%{_mandir}/man1/java-%{uniquesuffix %%1}.1*
%{_mandir}/man1/%{alt_java_name}-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jjs-%{uniquesuffix %%1}.1*
%{_mandir}/man1/keytool-%{uniquesuffix %%1}.1*
%{_mandir}/man1/pack200-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmid-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix %%1}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix %%1}.1*
%{_jvmdir}/%{sdkdir %%1}/lib/server/
%{_jvmdir}/%{sdkdir %%1}/lib/client/
%ifarch %{share_arches}
%attr(444, root, root) %ghost %{_jvmdir}/%{sdkdir %%1}/lib/server/classes.jsa
%attr(444, root, root) %ghost %{_jvmdir}/%{sdkdir %%1}/lib/client/classes.jsa
%endif
%dir %{_jvmdir}/%{sdkdir %%1}/lib/security
%{_jvmdir}/%{sdkdir %%1}/lib/security/cacerts
%dir %{_jvmdir}/%{sdkdir %%1}/conf
%dir %{_jvmdir}/%{sdkdir %%1}/conf/management
%dir %{_jvmdir}/%{sdkdir %%1}/conf/security
%dir %{_jvmdir}/%{sdkdir %%1}/conf/security/policy
%dir %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/limited
%dir %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/unlimited
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/lib/security/default.policy
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/lib/security/blacklisted.certs
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/lib/security/public_suffix_list.dat
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/limited/exempt_local.policy
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/limited/default_local.policy
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/limited/default_US_export.policy
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/unlimited/default_local.policy
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/unlimited/default_US_export.policy
 %{_jvmdir}/%{sdkdir %%1}/conf/security/policy/README.txt
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/java.policy
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/java.security
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/logging.properties
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/security/nss.cfg
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/management/jmxremote.access
# this is conifg template, thus not config-noreplace
%config  %{_jvmdir}/%{sdkdir %%1}/conf/management/jmxremote.password.template
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/management/management.properties
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/net.properties
%config(noreplace) %{_jvmdir}/%{sdkdir %%1}/conf/sound.properties
}

%global files_devel() %{expand:
%dir %{_jvmdir}/%{sdkdir %%1}/bin
%{_jvmdir}/%{sdkdir %%1}/bin/jar
%{_jvmdir}/%{sdkdir %%1}/bin/jarsigner
%{_jvmdir}/%{sdkdir %%1}/bin/javac
%{_jvmdir}/%{sdkdir %%1}/bin/javadoc
%{_jvmdir}/%{sdkdir %%1}/bin/javap
%{_jvmdir}/%{sdkdir %%1}/bin/jconsole
%{_jvmdir}/%{sdkdir %%1}/bin/jcmd
%{_jvmdir}/%{sdkdir %%1}/bin/jdb
%{_jvmdir}/%{sdkdir %%1}/bin/jdeps
%{_jvmdir}/%{sdkdir %%1}/bin/jdeprscan
%{_jvmdir}/%{sdkdir %%1}/bin/jfr
%{_jvmdir}/%{sdkdir %%1}/bin/jimage
# Some architectures don't have the serviceability agent
%ifarch %{sa_arches}
%{_jvmdir}/%{sdkdir %%1}/bin/jhsdb
%endif
%{_jvmdir}/%{sdkdir %%1}/bin/jinfo
%{_jvmdir}/%{sdkdir %%1}/bin/jlink
%{_jvmdir}/%{sdkdir %%1}/bin/jmap
%{_jvmdir}/%{sdkdir %%1}/bin/jmod
%{_jvmdir}/%{sdkdir %%1}/bin/jps
%{_jvmdir}/%{sdkdir %%1}/bin/jrunscript
%{_jvmdir}/%{sdkdir %%1}/bin/jshell
%{_jvmdir}/%{sdkdir %%1}/bin/jstack
%{_jvmdir}/%{sdkdir %%1}/bin/jstat
%{_jvmdir}/%{sdkdir %%1}/bin/jstatd
%{_jvmdir}/%{sdkdir %%1}/bin/rmic
%{_jvmdir}/%{sdkdir %%1}/bin/serialver
%ifarch %{aot_arches}
%{_jvmdir}/%{sdkdir %%1}/bin/jaotc
%endif
%{_jvmdir}/%{sdkdir %%1}/include
%{_jvmdir}/%{sdkdir %%1}/lib/ct.sym
%if %{with_systemtap}
%{_jvmdir}/%{sdkdir %%1}/tapset
%endif
%{_datadir}/applications/*jconsole%1.desktop
%{_mandir}/man1/jar-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jarsigner-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javac-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javadoc-%{uniquesuffix %%1}.1*
%{_mandir}/man1/javap-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jconsole-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jcmd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jdb-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jdeps-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jinfo-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jmap-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jps-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstack-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstat-%{uniquesuffix %%1}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmic-%{uniquesuffix %%1}.1*
%{_mandir}/man1/serialver-%{uniquesuffix %%1}.1*
%if %{with_systemtap}
%dir %{tapsetroot}
%dir %{tapsetdirttapset}
%dir %{tapsetdir}
%{tapsetdir}/*%{_arch}%1.stp
%endif
}

%define files_jmods() %{expand:
%{_jvmdir}/%{sdkdir %%1}/jmods
}

%define files_demo() %{expand:
%license %{_jvmdir}/%{sdkdir %%1}/legal
%{_jvmdir}/%{sdkdir %%1}/demo
%{_jvmdir}/%{sdkdir %%1}/sample
}

%define files_src() %{expand:
%license %{_jvmdir}/%{sdkdir %%1}/legal
%{_jvmdir}/%{sdkdir %%1}/lib/src.zip
}

%define files_static_libs() %{expand:
%dir %{_jvmdir}/%{sdkdir %%1}/lib/static
%dir %{_jvmdir}/%{sdkdir %%1}/lib/static/linux-%{archinstall}
%dir %{_jvmdir}/%{sdkdir %%1}/lib/static/linux-%{archinstall}/glibc
%{_jvmdir}/%{sdkdir %%1}/lib/static/linux-%{archinstall}/glibc/lib*.a
}

%define files_javadoc() %{expand:
%doc %{_javadocdir}/%{uniquejavadocdir %%1}
%license %{_jvmdir}/%{sdkdir %%1}/legal
}

%define files_javadoc_zip() %{expand:
%doc %{_javadocdir}/%{uniquejavadocdir %%1}.zip
%license %{_jvmdir}/%{sdkdir %%1}/legal
}

# not-duplicated requires/provides/obsolate for normal/debug packages
%global java_rpo() %{expand:
Requires: fontconfig%{?_isa}
Requires: xorg-x11-fonts-Type1
# Requires rest of java
Requires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
# for java-X-openjdk package's desktop binding
#Recommends: gtk2%{?_isa}
# rhel7 do not have week depndencies

Provides: java-%{javaver}-%{origin}%1 = %{epoch}:%{version}-%{release}

# Standard JPackage base provides
#Provides: jre = %{javaver}%1
#Provides: jre-%{origin}%1 = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}%1 = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-%{origin}%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}%1 = %{epoch}:%{version}-%{release}
#Provides: java-%{origin}%1 = %{epoch}:%{version}-%{release}
#Provides: java%1 = %{epoch}:%{javaver}
}

%global java_headless_rpo() %{expand:
# Require /etc/pki/java/cacerts
Requires: ca-certificates
# Require jpackage-utils for ownership of /usr/lib/jvm/ and macros
Requires: javapackages-tools
# Require zone-info data provided by tzdata-java sub-package
# 2020b required as of JDK-8254177 in October CPU
Requires: tzdata-java >= 2020b
# for support of kernel stream control
# libsctp.so.1 is being `dlopen`ed on demand
Requires: lksctp-tools%{?_isa}
# For smartcard support
# libpcsclite.so & libpcsclite.so.1 are both tried for dlopen
# and this package provides the latter (see RH910107)
Requires: pcsc-lite-libs%{?_isa}
# tool to copy jdk's configs - should be Recommends only, but then only dnf/yum enforce it,
# not rpm transaction and so no configs are persisted when pure rpm -u is run. It may be
# considered as regression
Requires: copy-jdk-configs >= 3.3
OrderWithRequires: copy-jdk-configs
# for printing support
Requires: cups-libs%{?_isa}
# Post requires alternatives to install tool alternatives
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

# rhel7 do not have weak depndencies

# Standard JPackage base provides
#Provides: jre-headless%1 = %{epoch}:%{javaver}
Provides: jre-%{javaver}-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: jre-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-headless%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: java-%{origin}-headless%1 = %{epoch}:%{version}-%{release}
#Provides: java-headless%1 = %{epoch}:%{javaver}

# https://bugzilla.redhat.com/show_bug.cgi?id=1312019
Provides: /usr/bin/jjs

}

%global java_devel_rpo() %{expand:
# Require base package
Requires:         %{name}%1%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

# Standard JPackage devel provides
Provides: java-sdk-%{javaver}-%{origin}%1 = %{epoch}:%{version}
Provides: java-sdk-%{javaver}%1 = %{epoch}:%{version}
#Provides: java-sdk-%{origin}%1 = %{epoch}:%{version}
#Provides: java-sdk%1 = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel%1 = %{epoch}:%{version}
Provides: java-%{javaver}-%{origin}-devel%1 = %{epoch}:%{version}
#Provides: java-devel-%{origin}%1 = %{epoch}:%{version}
#Provides: java-devel%1 = %{epoch}:%{javaver}

}

%define java_static_libs_rpo() %{expand:
Requires:         %{name}-devel%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
}

%define java_jmods_rpo() %{expand:
# Requires devel package
# as jmods are bytecode, they should be OK without any _isa
Requires:         %{name}-devel%1 = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1 = %{epoch}:%{version}-%{release}

Provides: java-jmods%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-jmods%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-jmods%1 = %{epoch}:%{version}-%{release}

}

%global java_demo_rpo() %{expand:
Requires: %{name}%1%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}

Provides: java-demo%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-demo%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-demo%1 = %{epoch}:%{version}-%{release}

}

%global java_javadoc_rpo() %{expand:
OrderWithRequires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install javadoc alternative
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall javadoc alternative
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

# Standard JPackage javadoc provides.
Provides: java-javadoc%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-javadoc%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-javadoc%1 = %{epoch}:%{version}-%{release}
}

%global java_src_rpo() %{expand:
Requires: %{name}-headless%1%{?_isa} = %{epoch}:%{version}-%{release}

# Standard JPackage sources provides.
Provides: java-src%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-src%1 = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-src%1 = %{epoch}:%{version}-%{release}
}

# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{newjavaver}.%{buildver}
Release: %{?eaprefix}%{rpmrelease}%{?extraver}%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons
# and this change was brought into RHEL-4. java-1.5.0-ibm packages
# also included the epoch in their virtual provides. This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0". In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0. So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages. Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".

Epoch:   1
Summary: %{origin_nice} %{featurever} Runtime Environment
Group:   Development/Languages

# HotSpot code is licensed under GPLv2
# JDK library code is licensed under GPLv2 with the Classpath exception
# The Apache license is used in code taken from Apache projects (primarily xalan & xerces)
# DOM levels 2 & 3 and the XML digital signature schemas are licensed under the W3C Software License
# The JSR166 concurrency code is in the public domain
# The BSD and MIT licenses are used for a number of third-party libraries (see ADDITIONAL_LICENSE_INFO)
# The OpenJDK source tree includes:
# - JPEG library (IJG), zlib & libpng (zlib), giflib (MIT), harfbuzz (ISC),
# - freetype (FTL), jline (BSD) and LCMS (MIT)
# - jquery (MIT), jdk.crypto.cryptoki PKCS 11 wrapper (RSA)
# - public_suffix_list.dat from publicsuffix.org (MPLv2.0)
# The test code includes copies of NSS under the Mozilla Public License v2.0
# The PCSClite headers are under a BSD with advertising license
# The elliptic curve cryptography (ECC) source code is licensed under the LGPLv2.1 or any later version
License:  ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib and ISC and FTL and RSA
URL:      http://openjdk.java.net/


# to regenerate source0 (jdk) run update_package.sh
# update_package.sh contains hard-coded repos, revisions, tags, and projects to regenerate the source archives
Source0: jdk-updates-jdk%{featurever}u-jdk-%{filever}+%{buildver}%{?tagsuffix:-%{tagsuffix}}-4curve.tar.xz

# Use 'icedtea_sync.sh' to update the following
# They are based on code contained in the IcedTea project (3.x).
# Systemtap tapsets. Zipped up to keep it small.
Source8: tapsets-icedtea-%{icedteaver}.tar.xz

# Desktop files. Adapted from IcedTea
Source9: jconsole.desktop.in

# Release notes
Source10: NEWS

# nss configuration file
Source11: nss.cfg.in

# Removed libraries that we link instead
Source12: remove-intree-libraries.sh

# Ensure we aren't using the limited crypto policy
Source13: TestCryptoLevel.java

# Ensure ECDSA is working
Source14: TestECDSA.java

# Ensure vendor settings are correct
Source15: CheckVendor.java

############################################
#
# RPM/distribution specific patches
#
############################################

# NSS via SunPKCS11 Provider (disabled comment
# due to memory leak).
Patch1000: rh1648249-add_commented_out_nss_cfg_provider_to_java_security.patch

# Ignore AWTError when assistive technologies are loaded
Patch1:    rh1648242-accessible_toolkit_crash_do_not_break_jvm.patch
# Restrict access to java-atk-wrapper classes
Patch2:    rh1648644-java_access_bridge_privileged_security.patch
Patch3:    rh649512-remove_uses_of_far_in_jpeg_libjpeg_turbo_1_4_compat_for_jdk10_and_up.patch
# Follow system wide crypto policy RHBZ#1249083
Patch4:    pr3183-rh1340845-support_fedora_rhel_system_crypto_policy.patch
# RH1750419: Enable build of speculative store bypass hardened alt-java (CVE-2018-3639)
Patch600: rh1750419-redhat_alt_java.patch

#############################################
#
# Shenandoah specific patches
#
#############################################

#############################################
#
# OpenJDK specific patches
#
#############################################

# JDK-8009550, RH910107: Search for libpcsclite.so.1 if libpcsclite.so fails
Patch7: jdk8009550-rh910107-search_for_versioned_libpcsclite.patch

#############################################
#
# JDK 9+ only patches
#
#############################################

#############################################
#
# Patches appearing in 11.0.11
#
# This section includes patches which are present
# in the listed OpenJDK 8u release and should be
# able to be removed once that release is out
# and used by this RPM.
#############################################
Patch8: jdk8258836-jni_local_refs_exceed_capacity.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: binutils
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
# elfutils only are OK for build without AOT
BuildRequires: elfutils-devel
BuildRequires: fontconfig
BuildRequires: freetype-devel
BuildRequires: giflib-devel
BuildRequires: gcc-c++
BuildRequires: gdb
%ifarch %{arm}
BuildRequires: devtoolset-7-build
BuildRequires: devtoolset-7-binutils
BuildRequires: devtoolset-7-gcc
BuildRequires: devtoolset-7-gcc-c++
BuildRequires: devtoolset-7-gdb
%endif
BuildRequires: gtk2-devel
# LCMS on rhel7 is older then LCMS in intree JDK
BuildRequires: lcms2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxslt
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
# Requirements for setting up the nss.cfg
BuildRequires: nss-devel
BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: zip
BuildRequires: javapackages-tools
BuildRequires: java-%{buildjdkver}-openjdk-devel
# Zero-assembler build requirement
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif
# 2020b required as of JDK-8254177 in October CPU
BuildRequires: tzdata-java >= 2020b
# Earlier versions have a bug in tree vectorization on PPC
BuildRequires: gcc >= 4.8.3-8

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif

# this is always built, also during debug-only build
# when it is built in debug-only this package is just placeholder
%{java_rpo %{nil}}

%description
The %{origin_nice} %{featurever} runtime environment.

%if %{include_debug_build}
%package debug
Summary: %{origin_nice} %{featurever} Runtime Environment %{debug_on}
Group:   Development/Languages

%{java_rpo -- %{debug_suffix_unquoted}}
%description debug
The %{origin_nice} %{featurever} runtime environment.
%{debug_warning}
%endif

%if %{include_normal_build}
%package headless
Summary: %{origin_nice} %{featurever} Headless Runtime Environment
Group:   Development/Languages

%{java_headless_rpo %{nil}}

%description headless
The %{origin_nice} %{featurever} runtime environment without audio and video support.
%endif

%if %{include_debug_build}
%package headless-debug
Summary: %{origin_nice} %{featurever} Runtime Environment %{debug_on}
Group:   Development/Languages

%{java_headless_rpo -- %{debug_suffix_unquoted}}

%description headless-debug
The %{origin_nice} %{featurever} runtime environment without audio and video support.
%{debug_warning}
%endif

%if %{include_normal_build}
%package devel
Summary: %{origin_nice} %{featurever} Development Environment
Group:   Development/Tools

%{java_devel_rpo %{nil}}

%description devel
The %{origin_nice} %{featurever} development tools.
%endif

%if %{include_debug_build}
%package devel-debug
Summary: %{origin_nice} %{featurever} Development Environment %{debug_on}
Group:   Development/Tools

%{java_devel_rpo -- %{debug_suffix_unquoted}}

%description devel-debug
The %{origin_nice} %{featurever} development tools.
%{debug_warning}
%endif

%if %{include_normal_build}
%package static-libs
Summary: %{origin_nice} %{featurever} libraries for static linking

%{java_static_libs_rpo %{nil}}

%description static-libs
The %{origin_nice} %{featurever} libraries for static linking.
%endif

%if %{include_debug_build}
%package static-libs-debug
Summary: %{origin_nice} %{featurever} libraries for static linking %{debug_on}

%{java_static_libs_rpo -- %{debug_suffix_unquoted}}

%description static-libs-debug
The %{origin_nice} %{featurever} libraries for static linking.
%{debug_warning}
%endif

%if %{include_normal_build}
%package jmods
Summary: JMods for %{origin_nice} %{featurever}
Group:   Development/Tools

%{java_jmods_rpo %{nil}}

%description jmods
The JMods for %{origin_nice} %{featurever}.
%endif

%if %{include_debug_build}
%package jmods-debug
Summary: JMods for %{origin_nice} %{featurever} %{debug_on}
Group:   Development/Tools

%{java_jmods_rpo -- %{debug_suffix_unquoted}}

%description jmods-debug
The JMods for %{origin_nice} %{featurever}.
%{debug_warning}
%endif

%if %{include_normal_build}
%package demo
Summary: %{origin_nice} %{featurever} Demos
Group:   Development/Languages

%{java_demo_rpo %{nil}}

%description demo
The %{origin_nice} %{featurever} demos.
%endif

%if %{include_debug_build}
%package demo-debug
Summary: %{origin_nice} %{featurever} Demos %{debug_on}
Group:   Development/Languages

%{java_demo_rpo -- %{debug_suffix_unquoted}}

%description demo-debug
The %{origin_nice} %{featurever} demos.
%{debug_warning}
%endif

%if %{include_normal_build}
%package src
Summary: %{origin_nice} %{featurever} Source Bundle
Group:   Development/Languages

%{java_src_rpo %{nil}}

%description src
The %{compatiblename}-src sub-package contains the complete %{origin_nice} %{featurever}
 class library source code for use by IDE indexers and debuggers.
%endif

%if %{include_debug_build}
%package src-debug
Summary: %{origin_nice} %{featurever} Source Bundle %{for_debug}
Group:   Development/Languages

%{java_src_rpo -- %{debug_suffix_unquoted}}

%description src-debug
The %{compatiblename}-src-debug sub-package contains the complete %{origin_nice} %{featurever}
 class library source code for use by IDE indexers and debuggers, %{for_debug}.
%endif

%if %{include_normal_build}
%package javadoc
Summary: %{origin_nice} %{featurever} API documentation
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo %{nil}}

%description javadoc
The %{origin_nice} %{featurever} API documentation.
%endif

%if %{include_normal_build}
%package javadoc-zip
Summary: %{origin_nice} %{featurever} API documentation compressed in a single archive
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo %{nil}}

%description javadoc-zip
The %{origin_nice} %{featurever} API documentation compressed in a single archive.
%endif

%if %{include_debug_build}
%package javadoc-debug
Summary: %{origin_nice} %{featurever} API documentation %{for_debug}
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo -- %{debug_suffix_unquoted}}

%description javadoc-debug
The %{origin_nice} %{featurever} API documentation %{for_debug}.
%endif

%if %{include_debug_build}
%package javadoc-zip-debug
Summary: %{origin_nice} %{featurever} API documentation compressed in a single archive %{for_debug}
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo -- %{debug_suffix_unquoted}}

%description javadoc-zip-debug
The %{origin_nice} %{featurever} API documentation compressed in a single archive %{for_debug}.
%endif

%prep

# Using the echo macro breaks rpmdev-bumpspec, as it parses the first line of stdout :-(
%if 0%{?stapinstall:1}
  echo "CPU: %{_target_cpu}, arch install directory: %{archinstall}, SystemTap install directory: %{stapinstall}"
%else
  %{error:Unrecognised architecture %{_target_cpu}}
%endif

if [ %{include_normal_build} -eq 0 -o  %{include_normal_build} -eq 1 ] ; then
  echo "include_normal_build is %{include_normal_build}"
else
  echo "include_normal_build is %{include_normal_build}, thats invalid. Use 1 for yes or 0 for no"
  exit 11
fi
if [ %{include_debug_build} -eq 0 -o  %{include_debug_build} -eq 1 ] ; then
  echo "include_debug_build is %{include_debug_build}"
else
  echo "include_debug_build is %{include_debug_build}, thats invalid. Use 1 for yes or 0 for no"
  exit 12
fi
if [ %{include_debug_build} -eq 0 -a  %{include_normal_build} -eq 0 ] ; then
  echo "You have disabled both include_debug_build and include_normal_build. That is a no go."
  exit 13
fi
if [ %{include_normal_build} -eq 0 ] ; then
  echo "You have disabled the normal build, but this is required to provide docs for the debug build."
  exit 14
fi
%setup -q -c -n %{uniquesuffix ""} -T -a 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 7 ] ; then
 echo "priority must be 7 digits in total, violated"
 exit 14
fi

# OpenJDK patches

# Remove libraries that are linked
sh %{SOURCE12}
pushd %{top_level_dir_name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch7 -p1
%patch8 -p1
popd # openjdk

%patch1000
%patch600

# Extract systemtap tapsets
%if %{with_systemtap}
tar --strip-components=1 -x -I xz -f %{SOURCE8}
%if %{include_debug_build}
cp -r tapset tapset%{debug_suffix}
%endif


for suffix in %{build_loop} ; do
  for file in "tapset"$suffix/*.in; do
    OUTPUT_FILE=`echo $file | sed -e "s:\.stp\.in$:-%{version}-%{release}.%{_arch}.stp:g"`
    sed -e "s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir $suffix}/lib/server/libjvm.so:g" $file > $file.1
# TODO find out which architectures other than i686 have a client vm
%ifarch %{ix86}
    sed -e "s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir $suffix}/lib/client/libjvm.so:g" $file.1 > $OUTPUT_FILE
%else
    sed -e "/@ABS_CLIENT_LIBJVM_SO@/d" $file.1 > $OUTPUT_FILE
%endif
    sed -i -e "s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir $suffix}:g" $OUTPUT_FILE
    sed -i -e "s:@INSTALL_ARCH_DIR@:%{archinstall}:g" $OUTPUT_FILE
    sed -i -e "s:@prefix@:%{_jvmdir}/%{sdkdir $suffix}/:g" $OUTPUT_FILE
  done
done
# systemtap tapsets ends
%endif

# Prepare desktop files
# The _X_ syntax indicates variables that are replaced by make upstream
# The @X@ syntax indicates variables that are replaced by configure upstream
for suffix in %{build_loop} ; do
for file in %{SOURCE9}; do
    FILE=`basename $file | sed -e s:\.in$::g`
    EXT="${FILE##*.}"
    NAME="${FILE%.*}"
    OUTPUT_FILE=$NAME$suffix.$EXT
    sed    -e  "s:_SDKBINDIR_:%{sdkbindir $suffix}:g" $file > $OUTPUT_FILE
    sed -i -e  "s:@target_cpu@:%{_arch}:g" $OUTPUT_FILE
    sed -i -e  "s:@OPENJDK_VER@:%{version}-%{release}.%{_arch}$suffix:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VER@:%{javaver}:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VENDOR@:%{origin}:g" $OUTPUT_FILE
done
done

# Setup nss.cfg
sed -e "s:@NSS_LIBDIR@:%{NSS_LIBDIR}:g" %{SOURCE11} > nss.cfg


%build
%ifarch %{arm}
%{?enable_devtoolset7:%{enable_devtoolset7}}
%endif

# How many CPU's do we have?
export NUM_PROC=%(/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :)
export NUM_PROC=${NUM_PROC:-1}
%if 0%{?_smp_ncpus_max}
# Honor %%_smp_ncpus_max
[ ${NUM_PROC} -gt %{?_smp_ncpus_max} ] && export NUM_PROC=%{?_smp_ncpus_max}
%endif

%ifarch s390x sparc64 alpha %{power64} %{aarch64}
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

# We use ourcppflags because the OpenJDK build seems to
# pass EXTRA_CFLAGS to the HotSpot C++ compiler...
# Explicitly set the C++ standard as the default has changed on GCC >= 6
EXTRA_CFLAGS="%ourcppflags -std=gnu++98 -Wno-error -fno-delete-null-pointer-checks"
EXTRA_CPP_FLAGS="%ourcppflags -std=gnu++98 -fno-delete-null-pointer-checks"
%ifarch %{ix86}
EXTRA_CFLAGS="${EXTRA_CFLAGS} -mstackrealign"
EXTRA_CPP_FLAGS="${EXTRA_CPP_FLAGS} -mstackrealign"
%endif

%ifarch %{power64} ppc
# fix rpmlint warnings
EXTRA_CFLAGS="$EXTRA_CFLAGS -fno-strict-aliasing"
%endif
EXTRA_ASFLAGS="${EXTRA_CFLAGS}"
export EXTRA_CFLAGS EXTRA_ASFLAGS

for suffix in %{build_loop} ; do
if [ "x$suffix" = "x" ] ; then
  debugbuild=release
else
  # change --something to something and rpeffix as slow
  debugbuild=`echo slow$suffix  | sed "s/-//g"`
fi

# Variable used in hs_err hook on build failures
top_dir_abs_path=$(pwd)/%{top_level_dir_name}

mkdir -p %{buildoutputdir $suffix}
pushd %{buildoutputdir $suffix}

bash ../configure \
%ifnarch %{jit_arches}
    --with-jvm-variants=zero \
%endif
%ifarch %{ppc64le}
    --with-jobs=1 \
%endif
    --with-version-build=%{buildver} \
    --with-version-pre="%{ea_designator}" \
    --with-version-opt=%{lts_designator} \
    --with-vendor-version-string="%{vendor_version_string}" \
    --with-vendor-name="%{oj_vendor}" \
    --with-vendor-url="%{oj_vendor_url}" \
    --with-vendor-bug-url="%{oj_vendor_bug_url}" \
    --with-vendor-vm-bug-url="%{oj_vendor_bug_url}" \
    --with-boot-jdk=/usr/lib/jvm/java-%{buildjdkver}-openjdk \
    --with-debug-level=$debugbuild \
    --with-native-debug-symbols=internal \
    --enable-unlimited-crypto \
    --with-zlib=system \
    --with-libjpeg=system \
    --with-giflib=system \
    --with-libpng=system \
    --with-lcms=bundled \
    --with-harfbuzz=bundled \
    --with-stdc++lib=dynamic \
    --with-extra-cxxflags="$EXTRA_CPP_FLAGS" \
    --with-extra-cflags="$EXTRA_CFLAGS" \
    --with-extra-asflags="$EXTRA_ASFLAGS" \
    --with-extra-ldflags="%{ourldflags}" \
    --with-num-cores="$NUM_PROC" \
    --disable-javac-server \
    --with-jvm-features="%{shenandoah_feature},%{zgc_feature}" \
    --disable-warnings-as-errors

# Debug builds don't need same targets as release for
# build speed-up
maketargets="%{release_targets}"
if echo $debugbuild | grep -q "debug" ; then
  maketargets="%{debug_targets}"
fi
make \
    JAVAC_FLAGS=-g \
    LOG=trace \
    WARNINGS_ARE_ERRORS="-Wno-error" \
    CFLAGS_WARNINGS_ARE_ERRORS="-Wno-error" \
    $maketargets || ( pwd; find $top_dir_abs_path -name "hs_err_pid*.log" | xargs cat && false )

# the build (erroneously) removes read permissions from some jars
# this is a regression in OpenJDK 7 (our compiler):
# http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
find images/%{jdkimage} -iname '*.jar' -exec chmod ugo+r {} \;

# Build screws up permissions on binaries
# https://bugs.openjdk.java.net/browse/JDK-8173610
find images/%{jdkimage} -iname '*.so' -exec chmod +x {} \;
find images/%{jdkimage}/bin/ -exec chmod +x {} \;

popd >& /dev/null

# Install nss.cfg right away as we will be using the JRE above
export JAVA_HOME=$(pwd)/%{buildoutputdir $suffix}/images/%{jdkimage}

# Install nss.cfg right away as we will be using the JRE above
install -m 644 nss.cfg $JAVA_HOME/conf/security/

# Use system-wide tzdata
rm $JAVA_HOME/lib/tzdb.dat
ln -s %{_datadir}/javazi-1.8/tzdb.dat $JAVA_HOME/lib/tzdb.dat

# Create fake alt-java as a placeholder for future alt-java
pushd ${JAVA_HOME}
# add alt-java man page
echo "Hardened java binary recommended for launching untrusted code from the Web e.g. javaws" > man/man1/%{alt_java_name}.1
cat man/man1/java.1 >> man/man1/%{alt_java_name}.1
popd

# build cycles
done

%check

# We test debug first as it will give better diagnostics on a crash
for suffix in %{rev_build_loop} ; do

export JAVA_HOME=$(pwd)/%{buildoutputdir $suffix}/images/%{jdkimage}

#check Shenandoah is enabled
%if %{use_shenandoah_hotspot}
$JAVA_HOME//bin/java -XX:+UseShenandoahGC -version
%endif

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java --add-opens java.base/javax.crypto=ALL-UNNAMED TestCryptoLevel

# Check ECC is working
$JAVA_HOME/bin/javac -d . %{SOURCE14}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE14})|sed "s|\.java||")

# Check correct vendor values have been set
$JAVA_HOME/bin/javac -d . %{SOURCE15}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE15})|sed "s|\.java||") "%{oj_vendor}" %{oj_vendor_url} %{oj_vendor_bug_url}

# Check java launcher has no SSB mitigation
if ! nm $JAVA_HOME/bin/java | grep set_speculation ; then true ; else false; fi

# Check alt-java launcher has SSB mitigation on supported architectures
%ifarch %{ssbd_arches}
nm $JAVA_HOME/bin/%{alt_java_name} | grep set_speculation
%else
if ! nm $JAVA_HOME/bin/%{alt_java_name} | grep set_speculation ; then true ; else false; fi
%endif

# Check debug symbols in static libraries (smoke test)
export STATIC_LIBS_HOME=$(pwd)/%{buildoutputdir $suffix}/images/%{static_libs_image}
readelf --debug-dump $STATIC_LIBS_HOME/lib/libfdlibm.a | grep w_remainder.c
readelf --debug-dump $STATIC_LIBS_HOME/lib/libfdlibm.a | grep e_remainder.c

# Check debug symbols are present and can identify code
find "$JAVA_HOME" -iname '*.so' -print0 | while read -d $'\0' lib
do
  if [ -f "$lib" ] ; then
    echo "Testing $lib for debug symbols"
    # All these tests rely on RPM failing the build if the exit code of any set
    # of piped commands is non-zero.

    # Test for .debug_* sections in the shared object. This is the main test
    # Stripped objects will not contain these
    eu-readelf -S "$lib" | grep "] .debug_"
    test $(eu-readelf -S "$lib" | grep -E "\]\ .debug_(info|abbrev)" | wc --lines) == 2

    # Test FILE symbols. These will most likely be removed by anything that
    # manipulates symbol tables because it's generally useless. So a nice test
    # that nothing has messed with symbols
    old_IFS="$IFS"
    IFS=$'\n'
    for line in $(eu-readelf -s "$lib" | grep "00000000      0 FILE    LOCAL  DEFAULT")
    do
     # We expect to see .cpp files, except for architectures like aarch64 and
     # s390 where we expect .o and .oS files
      echo "$line" | grep -E "ABS ((.*/)?[-_a-zA-Z0-9]+\.(c|cc|cpp|cxx|o|oS))?$"
    done
    IFS="$old_IFS"

    # If this is the JVM, look for javaCalls.(cpp|o) in FILEs, for extra sanity checking
    if [ "`basename $lib`" = "libjvm.so" ]; then
      eu-readelf -s "$lib" | \
        grep -E "00000000      0 FILE    LOCAL  DEFAULT      ABS javaCalls.(cpp|o)$"
    fi

    # Test that there are no .gnu_debuglink sections pointing to another
    # debuginfo file. There shouldn't be any debuginfo files, so the link makes
    # no sense either
    eu-readelf -S "$lib" | grep 'gnu'
    if eu-readelf -S "$lib" | grep '] .gnu_debuglink' | grep PROGBITS; then
      echo "bad .gnu_debuglink section."
      eu-readelf -x .gnu_debuglink "$lib"
      false
    fi
  fi
done

# Make sure gdb can do a backtrace based on line numbers on libjvm.so
# javaCalls.cpp:58 should map to:
# http://hg.openjdk.java.net/jdk8u/jdk8u/hotspot/file/ff3b27e6bcc2/src/share/vm/runtime/javaCalls.cpp#l58 
# Using line number 1 might cause build problems. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1539664
# https://bugzilla.redhat.com/show_bug.cgi?id=1538767
# Temporarily disabled on s390x as it sporadically crashes with SIGFPE, Arithmetic exception.
%ifnarch s390x
gdb -q "$JAVA_HOME/bin/java" <<EOF | tee gdb.out
handle SIGSEGV pass nostop noprint
handle SIGILL pass nostop noprint
set breakpoint pending on
break javaCalls.cpp:1
commands 1
backtrace
quit
end
run -version
EOF
grep 'JavaCallWrapper::JavaCallWrapper' gdb.out
%endif

# Check src.zip has all sources. See RHBZ#1130490
jar -tf $JAVA_HOME/lib/src.zip | grep 'sun.misc.Unsafe'

# Check class files include useful debugging information
$JAVA_HOME/bin/javap -l java.lang.Object | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.lang.Object | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.lang.Object | grep LocalVariableTable

# Check generated class files include useful debugging information
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep "Compiled from"
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep LineNumberTable
$JAVA_HOME/bin/javap -l java.nio.ByteBuffer | grep LocalVariableTable

# build cycles check
done

%install
STRIP_KEEP_SYMTAB=libjvm*

for suffix in %{build_loop} ; do

# Install the jdk
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}
cp -a %{buildoutputdir $suffix}/images/%{jdkimage} \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}

# Install jsa directories so we can owe them
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/%{archinstall}/server/
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/%{archinstall}/client/
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/client/ || true  ; # sometimes is here, sometimes not, ifout it or || true it out

pushd %{buildoutputdir $suffix}/images/%{jdkimage}

%if %{with_systemtap}
  # Install systemtap support files
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset
  # note, that uniquesuffix  is in BUILD dir in this case
  cp -a $RPM_BUILD_DIR/%{uniquesuffix ""}/tapset$suffix/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset/
  pushd  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/tapset/
   tapsetFiles=`ls *.stp`
  popd
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  for name in $tapsetFiles ; do
    targetName=`echo $name | sed "s/.stp/$suffix.stp/"`
    ln -sf %{_jvmdir}/%{sdkdir $suffix}/tapset/$name $RPM_BUILD_ROOT%{tapsetdir}/$targetName
  done
%endif

  # Remove empty cacerts database
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/security/cacerts
  # Install cacerts symlink needed by some apps which hard-code the path
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/security
      ln -sf /etc/pki/java/cacerts .
  popd

  # Install version-ed symlinks
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{sdkdir $suffix} %{jrelnk $suffix}
  popd

  # Install man pages
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{uniquesuffix $suffix}.1
  done
  # Remove man pages from jdk image
  rm -rf $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/man

popd
# Install static libs artefacts
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/static/linux-%{archinstall}/glibc
cp -a %{buildoutputdir $suffix}/images/%{static_libs_image}/lib/*.a \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir $suffix}/lib/static/linux-%{archinstall}/glibc


# Install Javadoc documentation
# Always take docs from normal build to avoid building them twice
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir $normal_suffix}/images/docs $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir $suffix}
built_doc_archive=jdk-%{filever}%{ea_designator_zip}+%{buildver}%{lts_designator_zip}-docs.zip
cp -a %{buildoutputdir $normal_suffix}/bundles/${built_doc_archive} \
     $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir $suffix}.zip || ls -l %{buildoutputdir $normal_suffix}/bundles/

# Install release notes
commondocdir=${RPM_BUILD_ROOT}%{_defaultdocdir}/%{uniquejavadocdir $suffix}
install -d -m 755 ${commondocdir}
cp -a %{SOURCE10} ${commondocdir}

# Install icons and menu entries
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    %{top_level_dir_name}/src/java.desktop/unix/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}-%{origin}.png
done

# Install desktop files
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole$suffix ; do
    desktop-file-install --vendor=%{uniquesuffix $suffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# copy samples next to demos; samples are mostly js files
cp -r %{top_level_dir_name}/src/sample  $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/


# stabilize permissions
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/ -name "*.so" -exec chmod 755 {} \; ; 
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/ -type d -exec chmod 755 {} \; ; 
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir $suffix}/legal -type f -exec chmod 644 {} \; ; 

# end, dual install
done

%if %{include_normal_build}
# intentionally only for non-debug
%pretrans headless -p <lua>
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1290388 for pretrans over pre
-- if copy-jdk-configs is in transaction, it installs in pretrans to temp
-- if copy_jdk_configs is in temp, then it means that copy-jdk-configs is in transaction  and so is
-- preferred over one in %%{_libexecdir}. If it is not in transaction, then depends
-- whether copy-jdk-configs is installed or not. If so, then configs are copied
-- (copy_jdk_configs from %%{_libexecdir} used) or not copied at all
local posix = require "posix"
local debug = false

SOURCE1 = "%{rpm_state_dir}/copy_jdk_configs.lua"
SOURCE2 = "%{_libexecdir}/copy_jdk_configs.lua"

local stat1 = posix.stat(SOURCE1, "type");
local stat2 = posix.stat(SOURCE2, "type");

  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE1 .." exists - copy-jdk-configs in transaction, using this one.")
  end;
  package.path = package.path .. ";" .. SOURCE1
else
  if (stat2 ~= nil) then
  if (debug) then
    print(SOURCE2 .." exists - copy-jdk-configs already installed and NOT in transaction. Using.")
  end;
  package.path = package.path .. ";" .. SOURCE2
  else
    if (debug) then
      print(SOURCE1 .." does NOT exists")
      print(SOURCE2 .." does NOT exists")
      print("No config files will be copied")
    end
  return
  end
end
-- run content of included file with fake args
arg = {"--currentjvm", "%{uniquesuffix %{nil}}", "--jvmdir", "%{_jvmdir %{nil}}", "--origname", "%{name}", "--origjavaver", "%{javaver}", "--arch", "%{_arch}", "--temp", "%{rpm_state_dir}/%{name}.%{_arch}"}
require "copy_jdk_configs.lua"

%post
%{post_script %{nil}}

%post headless
%{post_headless %{nil}}

%postun
%{postun_script %{nil}}

%postun headless
%{postun_headless %{nil}}

%posttrans
%{posttrans_script %{nil}}

%post devel
%{post_devel %{nil}}

%postun devel
%{postun_devel %{nil}}

%posttrans  devel
%{posttrans_devel %{nil}}

%post javadoc
%{post_javadoc %{nil}}

%postun javadoc
%{postun_javadoc %{nil}}

%post javadoc-zip
%{post_javadoc_zip %{nil}}

%postun javadoc-zip
%{postun_javadoc_zip %{nil}}
%endif

%if %{include_debug_build}
%post debug
%{post_script -- %{debug_suffix_unquoted}}

%post headless-debug
%{post_headless -- %{debug_suffix_unquoted}}

%postun debug
%{postun_script -- %{debug_suffix_unquoted}}

%postun headless-debug
%{postun_headless -- %{debug_suffix_unquoted}}

%posttrans debug
%{posttrans_script -- %{debug_suffix_unquoted}}

%post devel-debug
%{post_devel -- %{debug_suffix_unquoted}}

%postun devel-debug
%{postun_devel -- %{debug_suffix_unquoted}}

%posttrans  devel-debug
%{posttrans_devel -- %{debug_suffix_unquoted}}

%post javadoc-debug
%{post_javadoc -- %{debug_suffix_unquoted}}

%postun javadoc-debug
%{postun_javadoc -- %{debug_suffix_unquoted}}

%post javadoc-zip-debug
%{post_javadoc_zip -- %{debug_suffix_unquoted}}

%postun javadoc-zip-debug
%{postun_javadoc_zip -- %{debug_suffix_unquoted}}

%endif

%if %{include_normal_build}
%files
# main package builds always
%{files_jre %{nil}}
%else
%files
# placeholder
%endif


%if %{include_normal_build}
%files headless
# important note, see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
# all config/noreplace files (and more) have to be declared in pretrans. See pretrans
%{files_jre_headless %{nil}}

%files devel
%{files_devel %{nil}}

%files static-libs
%{files_static_libs %{nil}}

%files jmods
%{files_jmods %{nil}}

%files demo
%{files_demo %{nil}}

%files src
%{files_src %{nil}}

%files javadoc
%{files_javadoc %{nil}}

# this puts huge file to /usr/share
# unluckily ti is really a documentation file
# and unluckily it really is architecture-dependent, as eg. aot and grail are now x86_64 only
# same for debug variant
%files javadoc-zip
%{files_javadoc_zip %{nil}}
%endif

%if %{include_debug_build}
%files debug
%{files_jre -- %{debug_suffix_unquoted}}

%files headless-debug
%{files_jre_headless -- %{debug_suffix_unquoted}}

%files devel-debug
%{files_devel -- %{debug_suffix_unquoted}}

%files static-libs-debug
%{files_static_libs -- %{debug_suffix_unquoted}}

%files jmods-debug
%{files_jmods -- %{debug_suffix_unquoted}}

%files demo-debug
%{files_demo -- %{debug_suffix_unquoted}}

%files src-debug
%{files_src -- %{debug_suffix_unquoted}}

%files javadoc-debug
%{files_javadoc -- %{debug_suffix_unquoted}}

%files javadoc-zip-debug
%{files_javadoc_zip -- %{debug_suffix_unquoted}}
%endif

%changelog
* Tue Mar 02 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.9-1
- Add backport of JDK-8258836 to fix -Xcheck:jni warnings
- Resolves: rhbz#1897602

* Fri Jan 15 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.9-0
- Update to jdk-11.0.10.0+9
- Update release notes to 11.0.10.0+9
- Switch to GA mode for final release.
- This tarball is embargoed until 2021-01-19 @ 1pm PT.
- Resolves: rhbz#1908970

* Thu Jan 14 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.8-0.0.ea
- Update to jdk-11.0.10.0+8
- Update release notes to 11.0.10.0+8 and add missing JDK-8245051 from b04.
- Resolves: rhbz#1903907

* Thu Jan 14 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.5-0.0.ea
- Update to jdk-11.0.10.0+5
- Update release notes to 11.0.10.0+5
- Drop JDK-8222527 as applied upstream.
- Resolves: rhbz#1903907

* Wed Jan 13 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.4-0.0.ea
- Update to jdk-11.0.10.0+4
- Update release notes to 11.0.10.0+4
- Resolves: rhbz#1903907

* Tue Jan 12 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.3-0.0.ea
- Update to jdk-11.0.10.0+3
- Update release notes to 11.0.10.0+3
- Resolves: rhbz#1903907

* Tue Jan 12 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.2-0.0.ea
- Completely revert hacks from previous release, using buildver in configure and tzdata 2020b
- Resolves: rhbz#1903907

* Mon Jan 11 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.2-0.0.ea
- Update to jdk-11.0.10.0+2
- Update release notes to 11.0.10.0+2
- Update tarball generation script to use PR3818 which handles JDK-8171279 changes
- Drop JDK-8250861 as applied upstream.
- Resolves: rhbz#1903907

* Mon Jan 04 2021 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.1-0.0.ea
- Add new Harfbuzz library to package listing and _privatelibs
- Resolves: rhbz#1903907

* Sun Jan 03 2021 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.10.0.1-0.0.ea
- Update to jdk-11.0.10.0+1
- Update release notes to 11.0.10.0+1
- Use JEP-322 Time-Based Versioning so we can handle a future 11.0.9.1-like release correctly.
- Still use 11.0.x rather than 11.0.x.0 for file naming, as the trailing zero is omitted from tags.
- Revert configure and built_doc_archive hacks to build 11.0.9.1 from 11.0.9.0 sources, and synced with Fedora version.
- Cleanup debug package descriptions and version number placement.
- Switch to EA mode for 11.0.10 pre-release builds.
- Drop JDK-8222286 & JDK-8254177 as applied upstream
- Explicitly request bundled Harfbuzz (too risky to change this so late in the RHEL 7 lifecycle)
- Resolves: rhbz#1903907

* Tue Dec 29 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.11-5
- Introduced ssbd_arches to denote architectures with SSBD mitigation (currently only x86_64)
- Introduced nm-based check to verify alt-java on ssbd_arches is patched, and no other alt-java or java binaries are patched
- RH1750419 patch amended to emit a warning on architectures where alt-java is the same as java
- Resolves: rhbz#1901695

* Tue Dec 29 2020 Jiri Vanek <jvanek@redhat.com> - 1:11.0.9.11-5
- Redefined linux -> __linux__ and __x86_64 -> __x86_64__ in RH1750419 patch
- Resolves: rhbz#1901695

* Tue Dec 29 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.11-4
- Update release notes for 11.0.9.1 release.
- Resolves: rhbz#1895275

* Tue Dec 01 2020 Jiri Vanek <jvanek@redhat.com> - 1:11.0.9.11-3
- Removed patch6: rh1566890-CVE_2018_3639-speculative_store_bypass.patch, surpassed by new patch
- Added patch600: rh1750419-redhat_alt_java.patch, surpassing removed patch
- No longer copy java->alt-java as it is created by patch600
- Resolves: rhbz#1901695

* Thu Nov 12 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.11-2
- Add backport of JDK-8222537 so the Host header is sent when using proxies.
- Resolves: rhbz#1869530

* Wed Nov 04 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.9.11-1
- Update to jdk-11.0.9.1+1
- RPM version stays at 11.0.9.11 so as to not break upgrade path.
- Adds a single patch for JDK-8250861.
- Resolves: rhbz#1895275

* Thu Oct 29 2020 Jiri Vanek <jvanek@redhat.com> - 1:11.0.9.11-1
- Move all license files to NVR-specific JVM directory.
- This bad placement was killing parallel installability and thus having a bad impact on leapp, if used.
- Resolves: rhbz#1896609

* Mon Oct 19 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.9.11-1
- Fix directory ownership of static-libs package
- Resolves: rhbz#1896610

* Thu Oct 15 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.11-0
- Delay tzdata 2020b dependency until tzdata update has shipped.
- Resolves: rhbz#1876665

* Thu Oct 15 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.11-0
- Update to jdk-11.0.9+11
- Update release notes for 11.0.9 release.
- Add backport of JDK-8254177 to update to tzdata 2020b
- Require tzdata 2020b due to resource changes in JDK-8254177
- This tarball is embargoed until 2020-10-20 @ 1pm PT.
- Resolves: rhbz#1876665

* Thu Oct 15 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.10-0.1.ea
- Improve quoting of vendor name
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Jiri Vanek <jvanek@redhat.com> - 1:11.0.9.10-0.1.ea
- Set vendor property and vendor URLs
- Made URLs to be preconfigured by OS
- Moved vendor_version_string to a better place
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.10-0.0.ea
- Update to jdk-11.0.9+10 (EA)
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.9-0.0.ea
- Update to jdk-11.0.9+9 (EA)
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.8-0.0.ea
- Update to jdk-11.0.9+8 (EA)
- Remove JDK-8252258/RH1868406 now applied upstream.
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.7-0.0.ea
- Update to jdk-11.0.9+7 (EA)
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.9.6-0.1.ea
- Update static-libs packaging to new layout
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.6-0.0.ea
- Update to jdk-11.0.9+6 (EA)
- Update tarball generation script to use PR3802, handling JDK-8233228 & JDK-8177334
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.5-0.0.ea
- Update to jdk-11.0.9+5 (EA)
- Resolves: rhbz#1876665

* Wed Oct 14 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.4-0.0.ea
- Update to jdk-11.0.9+4 (EA)
- Resolves: rhbz#1876665

* Sun Oct 11 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.3-0.0.ea
- Update to jdk-11.0.9+3 (EA)
- Resolves: rhbz#1876665

* Sat Oct 10 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.2-0.1.ea
- Following JDK-8005165, class data sharing can be enabled on all JIT architectures
- Resolves: rhbz#1876665

* Thu Oct 08 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.2-0.0.ea
- Update to jdk-11.0.9+2 (EA)
- With Shenandoah now upstream in OpenJDK 11, we can use jdk-updates/jdk11 directly
- Resolves: rhbz#1876665

* Mon Oct 05 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.1-0.0.ea
- JDK-8245832 increases the set of static libraries, so try and include them all with a wildcard.
- Resolves: rhbz#1876665

* Mon Oct 05 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.1-0.0.ea
- Cleanup architecture and JVM feature handling in preparation for using upstreamed Shenandoah.
- Resolves: rhbz#1876665

* Mon Oct 05 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.9.1-0.0.ea
- Update to shenandoah-jdk-11.0.9+1 (EA)
- Switch to EA mode for 11.0.9 pre-release builds.
- Drop JDK-8227269, JDK-8241750 & JDK-8245714 backports now applied upstream.
- Resolves: rhbz#1876665

* Tue Aug 25 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.10-2
- Add JDK-8252258 to return default vendor to the original value of 'Oracle Corporation'
- Include a test in the RPM to check the build has the correct vendor information.
- Use 'oj_' prefix on new vendor globals to avoid a conflict with RPM's vendor value.
- Resolves: rhbz#1876665

* Sat Jul 11 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.10-1
- Update to shenandoah-jdk-11.0.8+10 (GA)
- Switch to GA mode for final release.
- Update release notes with last minute fix (JDK-8248505).
- This tarball is embargoed until 2020-07-14 @ 1pm PT.
- Resolves: rhbz#1838811

* Fri Jul 10 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.9-0.1.ea
- Update to shenandoah-jdk-11.0.8+9 (EA)
- Update release notes for 11.0.8 release.
- This tarball is embargoed until 2020-07-14 @ 1pm PT.
- Resolves: rhbz#1838811

* Sun Jul 05 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.8-0.1.ea
- Update to shenandoah-jdk-11.0.8+8 (EA)
- Resolves: rhbz#1838811

* Sat Jul 04 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.7-0.2.ea
- java-11-openjdk doesn't have a JRE tree, so don't try and copy alt-java there...
- Resolves: rhbz#1838811

* Sat Jul 04 2020 Jiri Vanek <jvanek@redhat.com> - 1:11.0.8.7-0.2.ea
- Create a copy of java as alt-java with alternatives and man pages
- Resolves: rhbz#1838811

* Fri Jul 03 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.7-0.1.ea
- Update to shenandoah-jdk-11.0.8+7 (EA)
- Resolves: rhbz#1838811

* Thu Jul 02 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.6-0.1.ea
- Update to shenandoah-jdk-11.0.8+6 (EA)
- Resolves: rhbz#1838811

* Tue Jun 30 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.8.5-0.2.ea
- Disable stripping of debug symbols for static libraries part of
  the -static-libs sub-package.
- Resolves: rhbz#1838811

* Thu Jun 25 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.5-0.1.ea
- Update to shenandoah-jdk-11.0.8+5 (EA)
- Resolves: rhbz#1838811

* Tue Jun 23 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.4-0.1.ea
- Update to shenandoah-jdk-11.0.8+4 (EA)
- Require tzdata 2020a due to resource changes in JDK-8243541
- Resolves: rhbz#1838811

* Fri Jun 19 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.3-0.1.ea
- Update to shenandoah-jdk-11.0.8+3 (EA)
- Resolves: rhbz#1838811

* Mon Jun 08 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.2-0.3.ea
- Add backport of JDK-8245714 to fix crash in build_loop_late_post(Node*)
- Resolves: rhbz#1828845

* Thu Jun 04 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.2-0.2.ea
- Use RHEL 7 format for handling the debug argument to the files_static_libs macro.
- Fix warning about macro in comment.
- Resolves: rhbz#1839091

* Wed Jun 03 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.8.2-0.2.ea
- Build static-libs-image and add resulting files via -static-libs sub-package.
- Resolves: rhbz#1839091

* Tue Jun 02 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.2-0.1.ea
- Update to shenandoah-jdk-11.0.8+2 (EA)
- Resolves: rhbz#1838811

* Mon May 25 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.8.1-0.1.ea
- Update to shenandoah-jdk-11.0.8+1 (EA)
- Switch to EA mode for 11.0.8 pre-release builds.
- Drop JDK-8237396 & JDK-8228407 backports now applied upstream.
- Resolves: rhbz#1838811

* Sat May 23 2020 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-7
- Add backports of JDK-8227269 & JDK-8241750 to resolve slow class loading with JDWP enabled.
- Resolves: rhbz#1826915

* Mon Apr 20 2020 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-6
- Introduce stapinstall variable to set SystemTap arch directory correctly (e.g. arm64 on aarch64)
- Need to support noarch for creating source RPMs for non-scratch builds.
- Resolves: rhbz#1737114

* Mon Apr 20 2020 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-6
- Sync SystemTap & desktop files with upstream IcedTea release 3.15.0
- Resolves: rhbz#1737114

* Mon Apr 20 2020 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-6
- Sync SystemTap & desktop files with upstream IcedTea release 3.11.0 using new script
- Resolves: rhbz#1737114

* Thu Apr 16 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-5
- Add JDK-8228407 backport to resolve crashes during verification.
- Resolves: rhbz#1810557

* Thu Apr 16 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-5
- Amend release notes, removing issue actually fixed in 11.0.6.
- Resolves: rhbz#1810557

* Thu Apr 16 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-5
- Add release notes.
- Resolves: rhbz#1810557

* Thu Apr 16 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.10-5
- Update to shenandoah-jdk-11.0.7+10 (GA)
- Switch to GA mode for final release.
- Resolves: rhbz#1810557

* Mon Apr 13 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.9-0.2.ea
- Make use of --with-extra-asflags introduced in jdk-11.0.6+1.
- Resolves: rhbz#1810557

* Sat Mar 28 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.9-0.1.ea
- Update to shenandoah-jdk-11.0.7+9 (EA)
- Resolves: rhbz#1810557

* Sat Mar 28 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.8-0.1.ea
- Update to shenandoah-jdk-11.0.7+8 (EA)
- Resolves: rhbz#1810557

* Sat Mar 28 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.7-0.1.ea
- Update to shenandoah-jdk-11.0.7+7 (EA)
- Resolves: rhbz#1810557

* Thu Mar 19 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.6-0.1.ea
- Update to shenandoah-jdk-11.0.7+6 (EA)
- Resolves: rhbz#1810557

* Thu Mar 19 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.5-0.1.ea
- Update to shenandoah-jdk-11.0.7+5 (EA)
- Resolves: rhbz#1810557

* Thu Mar 19 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.4-0.1.ea
- Update to shenandoah-jdk-11.0.7+4 (EA)
- Resolves: rhbz#1810557

* Thu Mar 19 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.3-0.1.ea
- Update to shenandoah-jdk-11.0.7+3 (EA)
- Resolves: rhbz#1810557

* Thu Mar 19 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.2-0.1.ea
- Update to shenandoah-jdk-11.0.7+2 (EA)
- Resolves: rhbz#1810557

* Thu Mar 19 2020 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.7.1-0.1.ea
- Bump release for y-stream branch.
- Resolves: rhbz#1810557

* Sun Feb 16 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.7.1-0.0.ea
- Update to shenandoah-jdk-11.0.7+1 (EA)
- Switch to EA mode for 11.0.7 pre-release builds.
- Drop JDK-8236039 backport now applied upstream.
- Resolves: rhbz#1810557

* Sun Feb 16 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.10-3
- Add JDK-8237396 backport to resolve Shenandoah TCK breakage in traversal mode.
- Resolves: rhbz#1785753

* Sat Jan 11 2020 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.6.10-2
- Add JDK-8236039 backport to resolve OpenShift blocker
- Resolves: rhbz#1785753

* Thu Jan 09 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.10-1
- Update to shenandoah-jdk-11.0.6+10 (GA)
- Switch to GA mode for final release.
- Resolves: rhbz#1785753

* Thu Jan 09 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.9-0.1.ea
- Update to shenandoah-jdk-11.0.6+9 (EA)
- Resolves: rhbz#1785753

* Wed Jan 08 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.8-0.1.ea
- Update to shenandoah-jdk-11.0.6+8 (EA)
- Resolves: rhbz#1785753

* Wed Jan 08 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.7-0.1.ea
- Update to shenandoah-jdk-11.0.6+7 (EA)
- Resolves: rhbz#1785753

* Wed Jan 08 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.6-0.1.ea
- Update to shenandoah-jdk-11.0.6+6 (EA)
- Resolves: rhbz#1785753

* Tue Jan 07 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.5-0.1.ea
- Update to shenandoah-jdk-11.0.6+5 (EA)
- Resolves: rhbz#1785753

* Mon Jan 06 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.4-0.1.ea
- Update to shenandoah-jdk-11.0.6+4 (EA)
- Resolves: rhbz#1785753

* Fri Jan 03 2020 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.3-0.1.ea
- Update to shenandoah-jdk-11.0.6+3 (EA)
- Resolves: rhbz#1785753

* Mon Dec 30 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.2-0.1.ea
- Update to shenandoah-jdk-11.0.6+2 (EA)
- Resolves: rhbz#1785753

* Thu Dec 19 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.6.1-0.1.ea
- Update to shenandoah-jdk-11.0.6+1 (EA)
- Switch to EA mode for 11.0.6 pre-release builds.
- Add support for jfr binary.
- Resolves: rhbz#1785753

* Wed Oct 09 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.10-1
- Update to shenandoah-jdk-11.0.5+10 (GA)
- Switch to GA mode for final release.
- Resolves: rhbz#1753423

* Mon Oct 07 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.9-0.1.ea
- Update to shenandoah-jdk-11.0.5+9 (EA)
- Resolves: rhbz#1737117

* Sun Oct 06 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.8-0.1.ea
- Update to shenandoah-jdk-11.0.5+8 (EA)
- Resolves: rhbz#1737117

* Fri Oct 04 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.7-0.1.ea
- Update to shenandoah-jdk-11.0.5+7 (EA)
- Resolves: rhbz#1737117

* Wed Oct 02 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.6-0.1.ea
- Update to shenandoah-jdk-11.0.5+6 (EA)
- Resolves: rhbz#1737117

* Tue Sep 17 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.5-0.1.ea
- Update to shenandoah-jdk-11.0.5+5 (EA)
- Resolves: rhbz#1737117

* Wed Sep 11 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.4-0.1.ea
- Revert rpmdev-bumpspec workaround as it has consequences for RPM installation.
- Resolves: rhbz#1737117

* Mon Sep 09 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.4-0.1.ea
- Update to shenandoah-jdk-11.0.5+4 (EA)
- Resolves: rhbz#1737117

* Thu Sep 05 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.3-0.1.ea
- Use 'release' rather than 'rpmrelease' for the release variable so rpmdev-bumpspec works again.
- Resolves: rhbz#1737117

* Thu Sep 05 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.3-0.1.ea
- Update to shenandoah-jdk-11.0.5+3 (EA)
- Resolves: rhbz#1737117

* Tue Aug 27 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.2-0.2.ea
- Update generate_source_tarball.sh script to use the PR3751 patch and retain the secp256k1 curve.
- Regenerate source tarball using the updated script and add the -'4curve' suffix.
- PR3751 includes the changes in the PR1834/RH1022017 patch which is removed.
- Resolves: rhbz#1699068

* Sat Aug 24 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.2-0.1.ea
- Update to shenandoah-jdk-11.0.5+2 (EA)
- Resolves: rhbz#1737117

* Mon Aug 12 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.5.1-0.1.ea
- Update to shenandoah-jdk-11.0.5+1 (EA)
- Switch to EA mode for 11.0.5 pre-release builds.
- Resolves: rhbz#1737117

* Tue Jul 09 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.11-1
- Update to shenandoah-jdk-11.0.4+11 (GA)
- Switch to GA mode for final release.
- Resolves: rhbz#1724452

* Mon Jul 08 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.10-0.1.ea
- Update to shenandoah-jdk-11.0.4+10 (EA)
- Resolves: rhbz#1724452

* Mon Jul 08 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.9-0.1.ea
- Update to shenandoah-jdk-11.0.4+9 (EA)
- Resolves: rhbz#1724452

* Mon Jul 08 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.8-0.1.ea
- Update to shenandoah-jdk-11.0.4+8 (EA)
- Resolves: rhbz#1724452

* Sun Jul 07 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.7-0.1.ea
- Update to shenandoah-jdk-11.0.4+7 (EA)
- Resolves: rhbz#1724452

* Wed Jul 03 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.6-0.1.ea
- Provide Javadoc debug subpackages for now, but populate them from the normal build.
- Resolves: rhbz#1724452

* Wed Jul 03 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.6-0.1.ea
- Update to shenandoah-jdk-11.0.4+6 (EA)
- Resolves: rhbz#1724452

* Wed Jul 03 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.5-0.1.ea
- Update to shenandoah-jdk-11.0.4+5 (EA)
- Resolves: rhbz#1724452

* Tue Jul 02 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.4-0.1.ea
- Update to shenandoah-jdk-11.0.4+4 (EA)
- Resolves: rhbz#1724452

* Mon Jul 01 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.3-0.1.ea
- Update to shenandoah-jdk-11.0.4+3 (EA)
- Resolves: rhbz#1724452

* Sun Jun 30 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.4.2-0.1.ea
- Use RHEL 7 format for jspawnhelper addition.
- Resolves: rhbz#1724452

* Sun Jun 30 2019 Andrew John Hughes <gnu.andrew@redhat.com> - 1:11.0.4.2-0.1.ea
- Update to shenandoah-jdk-11.0.4+2 (EA)
- Resolves: rhbz#1724452

* Fri Jun 21 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.4.2-0.1.ea
- Package jspawnhelper (see JDK-8220360).
- Resolves: rhbz#1724452

* Fri Jun 21 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.3.7-3
- Include 'ea' designator in Release when appropriate.
- Resolves: rhbz#1724452

* Wed May 22 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.3.7-3
- Handle milestone as variables so we can alter it easily and set the docs zip filename appropriately.
- Resolves: rhbz#1724452

* Thu Apr 25 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.3.7-2
- Don't build the test images needlessly.
- Don't produce javadoc/javadoc-zip sub packages for the debug variant build.
- Don't perform a bootcycle build for the debug variant build.
- Resolves: rhbz#1724452

* Thu Apr 04 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.3.7-1
- Update to shenandoah-jdk-11.0.3+7 (April 2019 GA)
- Resolves: rhbz#1693468

* Thu Apr 04 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.3.6-1
- Add -mstackrealign workaround to build flags to avoid SSE issues on x86
- Resolves: rhbz#1677516

* Thu Apr 04 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.3.6-1
- Fix macro which doesn't expand.
- Related: rhbz#1684617

* Thu Apr 04 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.3.6-1
- Add cast to resolve s390 ambiguity in call to log2_intptr
- Resolves: rhbz#1677516

* Thu Apr 04 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.3.6-1
- Update to shenandoah-jdk-11.0.3+6 (April 2019 EA)
- Drop JDK-8210416/RH1632174 applied upstream.
- Drop JDK-8210425/RH1632174 applied upstream.
- Drop JDK-8210647/RH1632174 applied upstream.
- Drop JDK-8210761/RH1632174 applied upstream.
- Drop JDK-8210703/RH1632174 applied upstream.
- Resolves: rhbz#1677516

* Wed Apr 03 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.2.7-4
- Replace pcsc-lite-devel with pcsc-lite-libs so deps can be resolved without optional repository
- Add JDK-8009550/RH910107 patch so OpenJDK checks for libpcsclite.so.1 (in pcsc-lite-libs)
- Add missing ISA to cups-libs requirement
- Remove duplicate lksctp-tools requirement
- Resolves: rhbz#1684617

* Wed Apr 03 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.2.7-4
- Disable gdb check on s390 as it sporadically fails with SIGFPE
- Resolves: rhbz#1693468

* Tue Apr 02 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.2.7-3
- Drop NSS runtime dependencies and patches to link against it.
- Resolves: rhbz#1656677

* Thu Mar 21 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.2.7-2
- Add patch for RH1566890
- Resolves: rhbz#1693468

* Tue Jan 15 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.2.7-1
- Update to shenandoah-jdk-11.0.2+7 (January 2019 CPU)
- Make tagsuffix optional and comment it out while unused.
- Drop JDK-8211105/RH1628612/RH1630996 applied upstream.
- Drop JDK-8209639/RH1640127 applied upstream.
- Re-generate JDK-8210416/RH1632174 following JDK-8209786
- Resolves: rhbz#1661577

* Mon Jan 14 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.1.13-8
- Fix remove-intree-libraries.sh to not exit early and skip SunEC handling.
- Fix PR1983 SunEC patch so that ecc_impl.h is patched rather than added
- Resolves: rhbz#1661577

* Fri Jan 11 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.1.13-8
- Update to shenandoah-jdk-11.0.1+13-20190101
- Update tarball generation script in preparation for PR3681/RH1656677 SunEC changes.
- Use remove-intree-libraries.sh to remove the remaining SunEC code for now.
- Add missing RH1022017 patch to reduce curves reported by SSL to those we support.
- Drop upstream Shenandoah patch RH1648995.
- Resolves: rhbz#1661577

* Fri Dec 07 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.1.13-7
- Added %%global _find_debuginfo_opts -g
- Resolves: rhbz#1656997

* Mon Nov 12 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.1.13-6
- fixed tck failures of arraycopy and process exec with shenandoah on
- added patch585 rh1648995-shenandoah_array_copy_broken_by_not_always_copy_forward_for_disjoint_arrays.patch

* Wed Nov 07 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.1.13-5
- headless' suggests of cups, replaced by Requires of cups-libs

* Thu Nov 01 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.1.13-3
- added Patch584 jdk8209639-rh1640127-02-coalesce_attempted_spill_non_spillable.patch

* Mon Oct 29 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.1.13-3
- Use upstream's version of Aarch64 intrinsics disable patch:
  - Removed:
    RHBZ-1628612-JDK-8210461-workaround-disable-aarch64-intrinsic.patch
    RHBZ-1630996-JDK-8210858-workaround-disable-aarch64-intrinsic-log.patch
  - Superceded by:
    jdk8211105-aarch64-disable_cos_sin_and_log_intrinsics.patch

* Thu Oct 18 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.1.13-2
- Use LTS designator in version output for RHEL.

* Thu Oct 18 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.1.13-1
- Update to October 2018 CPU release, 11.0.1+13.

* Wed Oct 17 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.0.28-2
- Use --with-vendor-version-string=18.9 so as to show original
  GA date for the JDK.

* Fri Sep 28 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.0.28-1
- Identify as GA version and no longer as early access (EA).
- JDK 11 has been released for GA on 2018-09-25.

* Fri Sep 28 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.ea.28-9
- Rework changes from 1:11.0.ea.22-6. RHBZ#1632174 supercedes
  RHBZ-1624122.
- Add patch, jdk8210416-rh1632174-compile_fdlibm_with_o2_ffp_contract_off_on_gcc_clang_arches.patch, so as to
  optimize compilation of fdlibm library.
- Add patch, jdk8210425-rh1632174-sharedRuntimeTrig_sharedRuntimeTrans_compiled_without_optimization.patch, so
  as to optimize compilation of sharedRuntime{Trig,Trans}.cpp
- Add patch, jdk8210647-rh1632174-libsaproc_is_being_compiled_without_optimization.patch, so as to
  optimize compilation of libsaproc (extra c flags won't override
  optimization).
- Add patch, jdk8210761-rh1632174-libjsig_is_being_compiled_without_optimization.patch, so as to
  optimize compilation of libjsig.
- Add patch, jdk8210703-rh1632174-vmStructs_cpp_no_longer_compiled_with_o0, so as to
  optimize compilation of vmStructs.cpp (part of libjvm.so).
- Reinstate filtering of opt flags coming from redhat-rpm-config.

* Thu Sep 27 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.28-8
- removed version less provides
- javadocdir moved to arched dir as it is no longer noarch
- Resolves: rhbz#1570856

* Thu Sep 20 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.ea.28-6
- Add patch, RHBZ-1630996-JDK-8210858-workaround-disable-aarch64-intrinsic-log.patch,
  so as to disable log math intrinsic on aarch64. Work-around for
  JDK-8210858
- Resolves: rhbz#1570856

* Thu Sep 13 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.ea.28-5
- Add patch, RHBZ-1628612-JDK-8210461-workaround-disable-aarch64-intrinsic.patch,
  so as to disable dsin/dcos math intrinsics on aarch64. Work-around for
  JDK-8210461.
- Resolves: rhbz#1570856

* Wed Sep 12 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.ea.22-6
- Add patch, JDK-8210416-RHBZ-1624122-fdlibm-opt-fix.patch, so as to
  optimize compilation of fdlibm library.
- Add patch, JDK-8210425-RHBZ-1624122-sharedRuntimeTrig-opt-fix.patch, so
  as to optimize compilation of sharedRuntime{Trig,Trans}.cpp
- Add patch, JDK-8210647-RHBZ-1624122-libsaproc-opt-fix.patch, so as to
  optimize compilation of libsaproc (extra c flags won't override
  optimization).
- Add patch, JDK-8210703-RHBZ-1624122-vmStructs-opt-fix.patch, so as to
  optimize compilation of vmStructs.cpp (part of libjvm.so).
- No longer filter -O flags from C flags coming from
  redhat-rpm-config.
- Resolves: RHBZ#1570856

* Mon Sep 10 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.28-4
- link to jhsdb followed its file to ifarch jit_arches ifnarch s390x
- Resolves: rhbz#1570856

* Fri Sep 7 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.28-4
- modified to build by itself
- Resolves: rhbz#1570856

* Fri Sep 7 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.ea.28-3
- Enable ZGC on x86_64.
- Resolves: RHBZ#1570856

* Wed Sep 5 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.28-2
- jfr/*jfc files listed for all arches
- lib/classlist do not exists s390, ifarch-ed via jit_arches out
- specfile slightly improved to allow srpm rebuild on rhel8/fedoras
- Resolves: rhbz#1570856

* Fri Aug 31 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.ea.28-1
- Update to latest upstream build jdk11+28, the first release
  candidate.
- Resolves: rhbz#1570856

* Wed Aug 29 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:11.0.ea.22-8
- Adjust system NSS patch, pr1983-rh1565658-support_using_the_system_installation_of_nss_with_the_sunec_provider_jdk11.patch, so
  as to filter -Wl,--as-needed from linker flags. Fixes FTBFS issue.
- Resolves: rhbz#1570856

* Tue Aug 28 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.22-6
- dissabled accessibility, fixed provides for main package's debug variant
- Resolves: RHBZ#1570856

* Mon Aug 27 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.22-8
- jfr/*jfc files listed for all arches
- Resolves: rhbz#1570856

* Mon Aug 27 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.22-7
- added space behind jmd slave
- Resolves: rhbz#1570856

* Mon Aug 27 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.22-6
- jfr/*jfc files listed also for ppc
- Resolves: rhbz#1570856

* Thu Aug 23 2018 Jiri Vanek <jvanek@redhat.com> - 1:11.0.ea.22-5
- Initial Load
- removed -fno-lifetime-dse; rhel7 gcc to old (4.8.5)
- lib/classlist do not exists s390, ifarch-ed via jit_arches out
- Resolves: rhbz#1570856
