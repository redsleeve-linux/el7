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
%global debug_warning This package has full debug on. Install only in need and remove asap.
%global debug_on with full debug on
%global for_debug for packages with debug on

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
%global multilib_arches %{power64} sparc64 x86_64
%global jit_arches      %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64} s390x
%global aot_arches      x86_64 %{aarch64}

# By default, we build a debug build during main build on JIT architectures
%if %{with slowdebug}
%ifarch %{jit_arches}
%ifnarch %{arm}
%global include_debug_build 1
%else
%global include_debug_build 0
%endif
%else
%global include_debug_build 0
%endif
%else
%global include_debug_build 0
%endif

# On x86_64 and AArch64, we use the Shenandoah HotSpot
%ifarch x86_64 %{aarch64}
%global use_shenandoah_hotspot 1
%else
%global use_shenandoah_hotspot 0
%endif

%if %{include_debug_build}
%global build_loop2 %{debug_suffix}
%else
%global build_loop2 %{nil}
%endif

# if you disable both builds, then the build fails
%global build_loop  %{build_loop1} %{build_loop2}
# note: that order: normal_suffix debug_suffix, in case of both enabled
# is expected in one single case at the end of the build
%global rev_build_loop  %{build_loop2} %{build_loop1}

%ifarch %{jit_arches}
%global bootstrap_build 1
%else
%global bootstrap_build 1
%endif

%if %{bootstrap_build}
%global targets bootcycle-images all docs
%else
%global targets all docs
%endif


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
%global NSS_LIBS %(pkg-config --libs nss)
%global NSS_CFLAGS %(pkg-config --cflags nss-softokn)
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332456
%global NSSSOFTOKN_BUILDTIME_NUMBER %(pkg-config --modversion nss-softokn || : )
%global NSS_BUILDTIME_NUMBER %(pkg-config --modversion nss || : )
# this is workaround for processing of requires during srpm creation
%global NSSSOFTOKN_BUILDTIME_VERSION %(if [ "x%{NSSSOFTOKN_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSSSOFTOKN_BUILDTIME_NUMBER}" ;fi)
%global NSS_BUILDTIME_VERSION %(if [ "x%{NSS_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSS_BUILDTIME_NUMBER}" ;fi)


# fix for https://bugzilla.redhat.com/show_bug.cgi?id=1111349
%global _privatelibs libsplashscreen[.]so.*|libawt_xawt[.]so.*|libjli[.]so.*|libattach[.]so.*|libawt[.]so.*|libextnet[.]so.*|libawt_headless[.]so.*|libdt_socket[.]so.*|libfontmanager[.]so.*|libinstrument[.]so.*|libj2gss[.]so.*|libj2pcsc[.]so.*|libj2pkcs11[.]so.*|libjaas[.]so.*|libjavajpeg[.]so.*|libjdwp[.]so.*|libjimage[.]so.*|libjsound[.]so.*|liblcms[.]so.*|libmanagement[.]so.*|libmanagement_agent[.]so.*|libmanagement_ext[.]so.*|libmlib_image[.]so.*|libnet[.]so.*|libnio[.]so.*|libprefs[.]so.*|librmi[.]so.*|libsaproc[.]so.*|libsctp[.]so.*|libsunec[.]so.*|libunpack[.]so.*|libzip[.]so.*

%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

# In some cases, the arch used by the JDK does
# not match _arch.
# Also, in some cases, the machine name used by SystemTap
# does not match that given by _build_cpu
%ifarch x86_64
%global archinstall amd64
%endif
%ifarch ppc
%global archinstall ppc
%endif
%ifarch %{ppc64be}
%global archinstall ppc64
%endif
%ifarch %{ppc64le}
%global archinstall ppc64le
%endif
%ifarch %{ix86}
%global archinstall i686
%endif
%ifarch ia64
%global archinstall ia64
%endif
%ifarch s390
%global archinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%endif
%ifarch %{arm}
%global archinstall arm
%endif
%ifarch %{aarch64}
%global archinstall aarch64
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%endif
%ifnarch %{jit_arches}
%global archinstall %{_arch}
%endif



%ifarch %{jit_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# New Version-String scheme-style defines
%global majorver 11
%global securityver 2
# Used via new version scheme. JDK 11 was
# GA'ed in September 2018 => 18.9
%global vendor_version_string 18.9
# Add LTS designator for RHEL builds
%if 0%{?rhel}
  %global lts_designator "LTS"
  %global lts_designator_zip -%{lts_designator}
%else
  %global lts_designator ""
  %global lts_designator_zip ""
%endif

# Standard JPackage naming and versioning defines
%global origin          openjdk
%global origin_nice     OpenJDK
%global top_level_dir_name   %{origin}
%global minorver        0
%global buildver        7
#%%global tagsuffix      %{nil}
# priority must be 7 digits in total
# setting to 1, so debug ones can have 0
%global priority        00000%{minorver}1
%global newjavaver      %{majorver}.%{minorver}.%{securityver}

%global javaver         %{majorver}

# parametrized macros are order-sensitive
%global compatiblename  java-%{majorver}-%{origin}
%global fullversion     %{compatiblename}-%{version}-%{release}
# images stub
%global jdkimage       jdk
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

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/

%if %{with_systemtap}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific sub-dir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinguish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdirttapset %{tapsetroot}/tapset/
%global tapsetdir %{tapsetdirttapset}/%{_build_cpu}
%endif

# not-duplicated scriptlets for normal/debug packages
%global update_desktop_icons /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%define post_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0
}


%define post_headless() %{expand:
%ifarch %{jit_arches}
# MetaspaceShared::generate_vtable_methods not implemented for PPC JIT
%ifnarch %{ppc64le}
# see https://bugzilla.redhat.com/show_bug.cgi?id=513605
%{jrebindir %%1}/java -Xshare:dump >/dev/null 2>/dev/null
%endif
%endif

PRIORITY=%{priority}
if [ "%1" == %{debug_suffix} ]; then
  let PRIORITY=PRIORITY-1
fi

ext=.gz
alternatives \\
  --install %{_bindir}/java java %{jrebindir %%1}/java $PRIORITY  --family %{name}.%{_arch} \\
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{sdkdir %%1} \\
  --slave %{_bindir}/jjs jjs %{jrebindir %%1}/jjs \\
  --slave %{_bindir}/keytool keytool %{jrebindir %%1}/keytool \\
  --slave %{_bindir}/pack200 pack200 %{jrebindir %%1}/pack200 \\
  --slave %{_bindir}/rmid rmid %{jrebindir %%1}/rmid \\
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir %%1}/rmiregistry \\
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir %%1}/unpack200 \\
  --slave %{_mandir}/man1/java.1$ext java.1$ext \\
  %{_mandir}/man1/java-%{uniquesuffix %%1}.1$ext \\
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
%ifarch %{jit_arches}
%ifnarch s390x
  --slave %{_bindir}/jhsdb jhsdb %{sdkbindir %%1}/jhsdb \\
%endif
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
%dir %{_sysconfdir}/.java/.systemPrefs
%dir %{_sysconfdir}/.java
%dir %{_jvmdir}/%{sdkdir %%1}
%{_jvmdir}/%{sdkdir %%1}/release
%{_jvmdir}/%{jrelnk %%1}
%dir %{_jvmdir}/%{sdkdir %%1}/bin
%{_jvmdir}/%{sdkdir %%1}/bin/java
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
# Zero and S390x don't have SA
%ifarch %{jit_arches}
%ifnarch s390x
%{_jvmdir}/%{sdkdir %%1}/lib/libsaproc.so
%endif
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
%{_mandir}/man1/jjs-%{uniquesuffix %%1}.1*
%{_mandir}/man1/keytool-%{uniquesuffix %%1}.1*
%{_mandir}/man1/pack200-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmid-%{uniquesuffix %%1}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix %%1}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix %%1}.1*
%{_jvmdir}/%{sdkdir %%1}/lib/server/
%{_jvmdir}/%{sdkdir %%1}/lib/client/
%ifarch %{jit_arches}
%ifnarch %{power64}
%attr(444, root, root) %ghost %{_jvmdir}/%{sdkdir %%1}/lib/server/classes.jsa
%attr(444, root, root) %ghost %{_jvmdir}/%{sdkdir %%1}/lib/client/classes.jsa
%endif
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
%{_jvmdir}/%{sdkdir %%1}/bin/jimage
# Zero and S390x don't have SA
%ifarch %{jit_arches}
%ifnarch s390x
%{_jvmdir}/%{sdkdir %%1}/bin/jhsdb
%endif
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

%define files_javadoc() %{expand:
%doc %{_javadocdir}/%{uniquejavadocdir %%1}
%license %{buildoutputdir %%1}/images/%{jdkimage}/legal
}

%define files_javadoc_zip() %{expand:
%doc %{_javadocdir}/%{uniquejavadocdir %%1}.zip
%license %{buildoutputdir %%1}/images/%{jdkimage}/legal
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
Requires: tzdata-java >= 2015d
# libsctp.so.1 is being `dlopen`ed on demand
Requires: lksctp-tools%{?_isa}
# there is a need to depend on the exact version of NSS
Requires: nss%{?_isa} %{NSS_BUILDTIME_VERSION}
Requires: nss-softokn%{?_isa} %{NSSSOFTOKN_BUILDTIME_VERSION}
# tool to copy jdk's configs - should be Recommends only, but then only dnf/yum enforce it,
# not rpm transaction and so no configs are persisted when pure rpm -u is run. It may be
# considered as regression
Requires: copy-jdk-configs >= 3.3
OrderWithRequires: copy-jdk-configs
# Post requires alternatives to install tool alternatives
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7
# for optional support of kernel stream control, card reader and printing bindings
#Suggests: lksctp-tools%{?_isa}, pcsc-lite-devel%{?_isa}, cups
# rhel7 do not have week depndencies

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
Release: 0%{?dist}.redsleeve
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
Summary: %{origin_nice} Runtime Environment %{majorver}
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


# to regenerate source0 (jdk) and source8 (jdk's taspets) run update_package.sh
# update_package.sh contains hard-coded repos, revisions, tags, and projects to regenerate the source archives
Source0: shenandoah-jdk%{majorver}-shenandoah-jdk-%{newjavaver}+%{buildver}%{?tagsuffix:-%{tagsuffix}}.tar.xz
Source8: systemtap_3.2_tapsets_hg-icedtea8-9d464368e06d.tar.xz

# Desktop files. Adapted from IcedTea
Source9: jconsole.desktop.in

# nss configuration file
Source11: nss.cfg.in

# Removed libraries that we link instead
Source12: remove-intree-libraries.sh

# Ensure we aren't using the limited crypto policy
Source13: TestCryptoLevel.java

# Ensure ECDSA is working
Source14: TestECDSA.java

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
# PR1834, RH1022017: Reduce curves reported by SSL to those in NSS
# Not currently suitable to go upstream as it disables curves
# for all providers unconditionally
Patch525: rh1022017-reduce_ssl_curves.patch
Patch3:    rh649512-remove_uses_of_far_in_jpeg_libjpeg_turbo_1_4_compat_for_jdk10_and_up.patch
# Follow system wide crypto policy RHBZ#1249083
Patch4:    pr3183-rh1340845-support_fedora_rhel_system_crypto_policy.patch
# System NSS via SunEC Provider
Patch5:    pr1983-rh1565658-support_using_the_system_installation_of_nss_with_the_sunec_provider_jdk11.patch

#############################################
#
# Shenandaoh specific patches
#
#############################################

#############################################
#
# OpenJDK specific patches
#
#############################################

# 8210416, RHBZ#1632174: [linux] Poor StrictMath performance due to non-optimized compilation
Patch8:    jdk8210416-rh1632174-compile_fdlibm_with_o2_ffp_contract_off_on_gcc_clang_arches.patch
# 8210425, RHBZ#1632174: [x86] sharedRuntimeTrig/sharedRuntimeTrans compiled without optimization
Patch9:    jdk8210425-rh1632174-sharedRuntimeTrig_sharedRuntimeTrans_compiled_without_optimization.patch

#############################################
#
# JDK 9+ only patches
#
#############################################

# 8210647, RHBZ#1632174: libsaproc is being compiled without optimization
Patch10:    jdk8210647-rh1632174-libsaproc_is_being_compiled_without_optimization.patch
# 8210761, RHBZ#1632174: libjsig is being compiled without optimization
Patch11:    jdk8210761-rh1632174-libjsig_is_being_compiled_without_optimization.patch
# 8210703, RHBZ#1632174: vmStructs.cpp compiled with -O0
Patch12:    jdk8210703-rh1632174-vmStructs_cpp_no_longer_compiled_with_o0

#############################################
#
# Patches appearing in 11.0.2
#
#############################################

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
BuildRequires: java-11-openjdk-devel
# Zero-assembler build requirement
%ifnarch %{jit_arches}
BuildRequires: libffi-devel
%endif
BuildRequires: tzdata-java >= 2015d
# Earlier versions have a bug in tree vectorization on PPC
BuildRequires: gcc >= 4.8.3-8
# Build requirements for SunEC system NSS support
BuildRequires: nss-softokn-freebl-devel >= 3.16.1

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif

# this is always built, also during debug-only build
# when it is built in debug-only this package is just placeholder
%{java_rpo %{nil}}

%description
The %{origin_nice} runtime environment.

%if %{include_debug_build}
%package debug
Summary: %{origin_nice} Runtime Environment %{majorver} %{debug_on}
Group:   Development/Languages

%{java_rpo -- %{debug_suffix_unquoted}}
%description debug
The %{origin_nice} runtime environment.
%{debug_warning}
%endif

%if %{include_normal_build}
%package headless
Summary: %{origin_nice} Headless Runtime Environment %{majorver}
Group:   Development/Languages

%{java_headless_rpo %{nil}}

%description headless
The %{origin_nice} runtime environment %{majorver} without audio and video support.
%endif

%if %{include_debug_build}
%package headless-debug
Summary: %{origin_nice} Runtime Environment %{debug_on}
Group:   Development/Languages

%{java_headless_rpo -- %{debug_suffix_unquoted}}

%description headless-debug
The %{origin_nice} runtime environment %{majorver} without audio and video support.
%{debug_warning}
%endif

%if %{include_normal_build}
%package devel
Summary: %{origin_nice} Development Environment %{majorver}
Group:   Development/Tools

%{java_devel_rpo %{nil}}

%description devel
The %{origin_nice} development tools %{majorver}.
%endif

%if %{include_debug_build}
%package devel-debug
Summary: %{origin_nice} Development Environment %{majorver} %{debug_on}
Group:   Development/Tools

%{java_devel_rpo -- %{debug_suffix_unquoted}}

%description devel-debug
The %{origin_nice} development tools %{majorver}.
%{debug_warning}
%endif

%if %{include_normal_build}
%package jmods
Summary: JMods for %{origin_nice} %{majorver}
Group:   Development/Tools

%{java_jmods_rpo %{nil}}

%description jmods
The JMods for %{origin_nice}.
%endif

%if %{include_debug_build}
%package jmods-debug
Summary: JMods for %{origin_nice} %{majorver} %{debug_on}
Group:   Development/Tools

%{java_jmods_rpo -- %{debug_suffix_unquoted}}

%description jmods-debug
The JMods for %{origin_nice} %{majorver}.
%{debug_warning}
%endif

%if %{include_normal_build}
%package demo
Summary: %{origin_nice} Demos %{majorver}
Group:   Development/Languages

%{java_demo_rpo %{nil}}

%description demo
The %{origin_nice} demos %{majorver}.
%endif

%if %{include_debug_build}
%package demo-debug
Summary: %{origin_nice} Demos %{majorver} %{debug_on}
Group:   Development/Languages

%{java_demo_rpo -- %{debug_suffix_unquoted}}

%description demo-debug
The %{origin_nice} demos %{majorver}.
%{debug_warning}
%endif

%if %{include_normal_build}
%package src
Summary: %{origin_nice} Source Bundle %{majorver}
Group:   Development/Languages

%{java_src_rpo %{nil}}

%description src
The java-%{origin}-src sub-package contains the complete %{origin_nice} %{majorver}
class library source code for use by IDE indexers and debuggers.
%endif

%if %{include_debug_build}
%package src-debug
Summary: %{origin_nice} Source Bundle %{majorver} %{for_debug}
Group:   Development/Languages

%{java_src_rpo -- %{debug_suffix_unquoted}}

%description src-debug
The java-%{origin}-src-slowdebug sub-package contains the complete %{origin_nice} %{majorver}
 class library source code for use by IDE indexers and debuggers. Debugging %{for_debug}.
%endif

%if %{include_normal_build}
%package javadoc
Summary: %{origin_nice} %{majorver} API documentation
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo %{nil}}

%description javadoc
The %{origin_nice} %{majorver} API documentation.
%endif

%if %{include_normal_build}
%package javadoc-zip
Summary: %{origin_nice} %{majorver} API documentation compressed in single archive
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo %{nil}}

%description javadoc-zip
The %{origin_nice} %{majorver} API documentation compressed in single archive.
%endif

%if %{include_debug_build}
%package javadoc-debug
Summary: %{origin_nice} %{majorver} API documentation %{for_debug}
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo -- %{debug_suffix_unquoted}}

%description javadoc-debug
The %{origin_nice} %{majorver} API documentation %{for_debug}.
%endif

%if %{include_debug_build}
%package javadoc-zip-debug
Summary: %{origin_nice} %{majorver} API documentation compressed in single archive %{for_debug}
Group:   Documentation
Requires: javapackages-tools

%{java_javadoc_rpo -- %{debug_suffix_unquoted}}

%description javadoc-zip-debug
The %{origin_nice} %{majorver} API documentation compressed in single archive %{for_debug}.
%endif


%prep
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
%patch5 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch525 -p1
popd # openjdk

%patch1000

# Extract systemtap tapsets
%if %{with_systemtap}
tar --strip-components=1 -x -I xz -f %{SOURCE8}
%if %{include_debug_build}
cp -r tapset tapset%{debug_suffix}
%endif


for suffix in %{build_loop} ; do
  for file in "tapset"$suffix/*.in; do
    OUTPUT_FILE=`echo $file | sed -e "s:\.stp\.in$:%{version}-%{release}.%{_arch}.stp:g"`
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
for suffix in %{build_loop} ; do
for file in %{SOURCE9}; do
    FILE=`basename $file | sed -e s:\.in$::g`
    EXT="${FILE##*.}"
    NAME="${FILE%.*}"
    OUTPUT_FILE=$NAME$suffix.$EXT
    sed    -e  "s:@JAVA_HOME@:%{sdkbindir $suffix}:g" $file > $OUTPUT_FILE
    sed -i -e  "s:@JRE_HOME@:%{jrebindir $suffix}:g" $OUTPUT_FILE
    sed -i -e  "s:@ARCH@:%{version}-%{release}.%{_arch}$suffix:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_MAJOR_VERSION@:%{majorver}:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VENDOR@:%{origin}:g" $OUTPUT_FILE
done
done

# Setup nss.cfg
sed -e "s:@NSS_LIBDIR@:%{NSS_LIBDIR}:g" %{SOURCE11} > nss.cfg


%build
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

%ifarch %{power64} ppc
# fix rpmlint warnings
EXTRA_CFLAGS="$EXTRA_CFLAGS -fno-strict-aliasing"
%endif
export EXTRA_CFLAGS

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
    --with-version-pre="" \
    --with-version-opt=%{lts_designator} \
    --with-vendor-version-string="%{vendor_version_string}" \
    --with-boot-jdk=/usr/lib/jvm/java-11-openjdk \
    --with-debug-level=$debugbuild \
    --with-native-debug-symbols=internal \
    --enable-unlimited-crypto \
    --enable-system-nss \
    --with-zlib=system \
    --with-libjpeg=system \
    --with-giflib=system \
    --with-libpng=system \
    --with-lcms=bundled \
    --with-stdc++lib=dynamic \
    --with-extra-cxxflags="$EXTRA_CPP_FLAGS" \
    --with-extra-cflags="$EXTRA_CFLAGS" \
    --with-extra-ldflags="%{ourldflags}" \
    --with-num-cores="$NUM_PROC" \
    --disable-javac-server \
%ifarch x86_64
    --with-jvm-features=zgc \
%endif
    --disable-warnings-as-errors

make \
    JAVAC_FLAGS=-g \
    LOG=trace \
    WARNINGS_ARE_ERRORS="-Wno-error" \
    CFLAGS_WARNINGS_ARE_ERRORS="-Wno-error" \
    %{targets} || ( pwd; find $top_dir_abs_path -name "hs_err_pid*.log" | xargs cat && false )

make docs-zip

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

# build cycles
done

%check

# We test debug first as it will give better diagnostics on a crash
for suffix in %{rev_build_loop} ; do

export JAVA_HOME=$(pwd)/%{buildoutputdir $suffix}/images/%{jdkimage}

#check sheandoah is enabled
%if %{use_shenandoah_hotspot}
$JAVA_HOME//bin/java -XX:+UseShenandoahGC -version
%endif

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java --add-opens java.base/javax.crypto=ALL-UNNAMED TestCryptoLevel

# Check ECC is working
$JAVA_HOME/bin/javac -d . %{SOURCE14}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE14})|sed "s|\.java||")

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
#gdb -q "$JAVA_HOME/bin/java" <<EOF | tee gdb.out
#handle SIGSEGV pass nostop noprint
#handle SIGILL pass nostop noprint
#set breakpoint pending on
#break javaCalls.cpp:1
#commands 1
#backtrace
#quit
#end
#run -version
#EOF
#grep 'JavaCallWrapper::JavaCallWrapper' gdb.out

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


# Install Javadoc documentation
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir $suffix}/images/docs $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir $suffix}
cp -a %{buildoutputdir $suffix}/bundles/jdk-%{newjavaver}+%{buildver}%{lts_designator_zip}-docs.zip  $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir $suffix}.zip

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
* Wed Mar 06 2019 Jacco Ligthart <jacco@redsleeve.org> - 1:11.0.2.7-0.redsleeve
- removed arm from jit_arches
- removed the gdb section of the SPEC file

* Tue Jan 15 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.2.7-0
- Update to shenandoah-jdk-11.0.2+7 (January 2019 CPU)
- Make tagsuffix optional and comment it out while unused.
- Drop JDK-8211105/RH1628612/RH1630996 applied upstream.
- Drop JDK-8209639/RH1640127 applied upstream.
- Re-generate JDK-8210416/RH1632174 following JDK-8209786
- Resolves: rhbz#1661577

* Mon Jan 14 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:11.0.1.13-4
- Update to shenandoah-jdk-11.0.1+13-20190101
- Update tarball generation script in preparation for PR3681/RH1656677 SunEC changes.
- Use remove-intree-libraries.sh to remove the remaining SunEC code for now.
- Fix remove-intree-libraries.sh to not exit early and skip SunEC handling.
- Fix PR1983 SunEC patch so that ecc_impl.h is patched rather than added
- Add missing RH1022017 patch to reduce curves reported by SSL to those we support.
- Resolves: rhbz#1661577

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