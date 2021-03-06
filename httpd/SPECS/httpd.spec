%define contentdir %{_datadir}/httpd
%define docroot /var/www
%define suexec_caller apache
%define mmn 20120211
%define oldmmnisa %{mmn}-%{__isa_name}-%{__isa_bits}
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}
%define vstring CentOS

# Drop automatic provides for module DSOs
%{?filter_setup:
%filter_provides_in %{_libdir}/httpd/modules/.*\.so$
%filter_setup
}

Summary: Apache HTTP Server
Name: httpd
Version: 2.4.6
Release: 97%{?dist}.redsleeve
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
Source1: index.html
Source2: httpd.logrotate
Source3: httpd.sysconf
Source4: httpd-ssl-pass-dialog
Source5: httpd.tmpfiles
Source6: httpd.service
Source7: action-graceful.sh
Source8: action-configtest.sh
Source10: httpd.conf
Source11: 00-base.conf
Source12: 00-mpm.conf
Source13: 00-lua.conf
Source14: 01-cgi.conf
Source15: 00-dav.conf
Source16: 00-proxy.conf
Source17: 00-ssl.conf
Source18: 01-ldap.conf
Source19: 00-proxyhtml.conf
Source20: userdir.conf
Source21: ssl.conf
Source22: welcome.conf
Source23: manual.conf
Source24: 00-systemd.conf
Source25: 01-session.conf
# Documentation
Source30: README.confd
Source40: htcacheclean.service
Source41: htcacheclean.sysconf
# build/scripts patches
Patch1: httpd-2.4.1-apctl.patch
Patch2: httpd-2.4.3-apxs.patch
Patch3: httpd-2.4.1-deplibs.patch
Patch5: httpd-2.4.3-layout.patch
Patch6: httpd-2.4.3-apctl-systemd.patch
# Features/functional changes
Patch21: httpd-2.4.6-full-release.patch
Patch23: httpd-2.4.4-export.patch
Patch24: httpd-2.4.1-corelimit.patch
Patch25: httpd-2.4.1-selinux.patch
Patch26: httpd-2.4.4-r1337344+.patch
Patch27: httpd-2.4.2-icons.patch
Patch28: httpd-2.4.6-r1332643+.patch
Patch29: httpd-2.4.3-mod_systemd.patch
Patch30: httpd-2.4.4-cachehardmax.patch
Patch31: httpd-2.4.6-sslmultiproxy.patch
Patch32: httpd-2.4.6-r1537535.patch
Patch33: httpd-2.4.6-r1542327.patch
Patch34: httpd-2.4.6-ssl-large-keys.patch
Patch35: httpd-2.4.6-pre_htaccess.patch
Patch36: httpd-2.4.6-r1573626.patch
Patch37: httpd-2.4.6-uds.patch
Patch38: httpd-2.4.6-upn.patch
Patch39: httpd-2.4.6-r1664565.patch
Patch40: httpd-2.4.6-r1861793+.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1715981
Patch41: httpd-2.4.6-session-expiry-updt-int.patch

# Bug fixes
Patch51: httpd-2.4.3-sslsninotreq.patch
Patch55: httpd-2.4.4-malformed-host.patch
Patch56: httpd-2.4.4-mod_unique_id.patch
Patch57: httpd-2.4.6-ldaprefer.patch
Patch58: httpd-2.4.6-r1507681+.patch
Patch59: httpd-2.4.6-r1556473.patch
Patch60: httpd-2.4.6-r1553540.patch
Patch61: httpd-2.4.6-rewrite-clientaddr.patch
Patch62: httpd-2.4.6-ab-overflow.patch
Patch63: httpd-2.4.6-sigint.patch
Patch64: httpd-2.4.6-ssl-ecdh-auto.patch
Patch65: httpd-2.4.6-r1556818.patch
Patch66: httpd-2.4.6-r1618851.patch
Patch67: httpd-2.4.6-r1526189.patch
Patch68: httpd-2.4.6-r1663647.patch
Patch69: httpd-2.4.6-r1569006.patch
Patch70: httpd-2.4.6-r1506474.patch
Patch71: httpd-2.4.6-bomb.patch
Patch72: httpd-2.4.6-r1604460.patch
Patch73: httpd-2.4.6-r1624349.patch
Patch74: httpd-2.4.6-ap-ipv6.patch
Patch75: httpd-2.4.6-r1530280.patch
Patch76: httpd-2.4.6-r1633085.patch
Patch78: httpd-2.4.6-ssl-error-free.patch
Patch79: httpd-2.4.6-r1528556.patch
Patch80: httpd-2.4.6-r1594625.patch
Patch81: httpd-2.4.6-r1674222.patch
Patch82: httpd-2.4.6-apachectl-httpd-env.patch
Patch83: httpd-2.4.6-rewrite-dir.patch
Patch84: httpd-2.4.6-r1420184.patch
Patch85: httpd-2.4.6-r1524368.patch
Patch86: httpd-2.4.6-r1528958.patch
Patch87: httpd-2.4.6-r1651083.patch
Patch88: httpd-2.4.6-r1688399.patch
Patch89: httpd-2.4.6-r1527509.patch
Patch90: httpd-2.4.6-apachectl-status.patch
Patch91: httpd-2.4.6-r1650655.patch
Patch92: httpd-2.4.6-r1533448.patch
Patch93: httpd-2.4.6-r1610013.patch
Patch94: httpd-2.4.6-r1705528.patch
Patch95: httpd-2.4.6-r1684462.patch
Patch96: httpd-2.4.6-r1650677.patch
Patch97: httpd-2.4.6-r1621601.patch
Patch98: httpd-2.4.6-r1610396.patch
Patch99: httpd-2.4.6-rotatelog-timezone.patch
Patch100: httpd-2.4.6-ab-ssl-error.patch
Patch101: httpd-2.4.6-r1723522.patch
Patch102: httpd-2.4.6-r1681107.patch
Patch103: httpd-2.4.6-dhparams-free.patch
Patch104: httpd-2.4.6-r1651658.patch
Patch105: httpd-2.4.6-r1560093.patch
Patch106: httpd-2.4.6-r1748212.patch
Patch107: httpd-2.4.6-r1570327.patch
Patch108: httpd-2.4.6-r1631119.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1406184
Patch109: httpd-2.4.6-r1593002.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1389535
Patch110: httpd-2.4.6-r1662640.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1348019
Patch111: httpd-2.4.6-r1348019.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1396197
Patch112: httpd-2.4.6-r1587053.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1376835
# https://bugzilla.redhat.com/show_bug.cgi?id=1527295
Patch113: httpd-2.4.6-mpm-segfault.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1372692
Patch114: httpd-2.4.6-r1681114.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1371876
Patch115: httpd-2.4.6-r1775832.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1353740
Patch116: httpd-2.4.6-r1726019.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1364604
Patch117: httpd-2.4.6-r1683112.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1378946
Patch118: httpd-2.4.6-r1651653.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1414258
Patch119: httpd-2.4.6-r1634529.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1397241
Patch120: httpd-2.4.6-r1738878.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1445885
Patch121: httpd-2.4.6-http-protocol-options-define.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1332242
Patch122: httpd-2.4.6-statements-comment.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1451333
Patch123: httpd-2.4.6-rotatelogs-zombie.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1368491
Patch124: httpd-2.4.6-mod_authz_dbd-missing-query.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1288395
Patch125: httpd-2.4.6-r1668532.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1499253
Patch126: httpd-2.4.6-r1681289.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1430640
Patch127: httpd-2.4.6-r1805099.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1448892
Patch128: httpd-2.4.6-r1811831.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1464406
Patch129: httpd-2.4.6-r1811746.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1440590
Patch130: httpd-2.4.6-r1811976.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1506392
Patch131: httpd-2.4.6-r1650310.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1557785
Patch132: httpd-2.4.6-r1530999.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1533793
Patch133: httpd-2.4.6-r1555539.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1523536
Patch134: httpd-2.4.6-r1737363.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1548501
Patch135: httpd-2.4.6-r1826995.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1556761
Patch136: httpd-2.4.6-default-port-worker.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1493181
Patch137: httpd-2.4.6-r1825120.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1458364
Patch138: httpd-2.4.6-r1515372.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1458364
Patch139: httpd-2.4.6-r1824872.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1583218
Patch140: httpd-2.4.6-r1833014.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1673457
Patch141: httpd-2.4.6-r1583175.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1649470
Patch142: httpd-2.4.6-r1862604.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1724879
Patch143: httpd-2.4.6-ssl-close-notify-client.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1852350
Patch144: httpd-2.4.6-r1879224.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1785100
Patch145: httpd-2.4.6-r1881459.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1862499
Patch146: httpd-2.4.6-r1872790.patch

# Security fixes
Patch200: httpd-2.4.6-CVE-2013-6438.patch
Patch201: httpd-2.4.6-CVE-2014-0098.patch
Patch202: httpd-2.4.6-CVE-2014-0231.patch
Patch203: httpd-2.4.6-CVE-2014-0117.patch
Patch204: httpd-2.4.6-CVE-2014-0118.patch
Patch205: httpd-2.4.6-CVE-2014-0226.patch
Patch206: httpd-2.4.6-CVE-2013-4352.patch
Patch207: httpd-2.4.6-CVE-2013-5704.patch
Patch208: httpd-2.4.6-CVE-2014-3581.patch
Patch209: httpd-2.4.6-CVE-2015-3185.patch
Patch210: httpd-2.4.6-CVE-2015-3183.patch
Patch211: httpd-2.4.6-CVE-2016-5387.patch
Patch212: httpd-2.4.6-CVE-2016-8743.patch
Patch213: httpd-2.4.6-CVE-2016-0736.patch
Patch214: httpd-2.4.6-CVE-2016-2161.patch
Patch215: httpd-2.4.6-CVE-2017-3167.patch
Patch216: httpd-2.4.6-CVE-2017-3169.patch
Patch217: httpd-2.4.6-CVE-2017-7668.patch
Patch218: httpd-2.4.6-CVE-2017-7679.patch
Patch219: httpd-2.4.6-CVE-2017-9788.patch
Patch220: httpd-2.4.6-CVE-2017-9798.patch
Patch221: httpd-2.4.6-CVE-2018-1312.patch
Patch222: httpd-2.4.6-CVE-2019-0217.patch
Patch223: httpd-2.4.6-CVE-2019-0220.patch
Patch224: httpd-2.4.6-CVE-2017-15710.patch
Patch225: httpd-2.4.6-CVE-2018-1301.patch
Patch226: httpd-2.4.6-CVE-2018-17199.patch
Patch227: httpd-2.4.6-CVE-2017-15715.patch
Patch228: httpd-2.4.6-CVE-2019-10098.patch
Patch229: httpd-2.4.6-CVE-2018-1303.patch
Patch230: httpd-2.4.6-CVE-2018-1283.patch
Patch240: httpd-2.4.6-CVE-2020-1934.patch

License: ASL 2.0
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, perl, pkgconfig, findutils, xmlto
BuildRequires: zlib-devel, libselinux-devel, lua-devel
BuildRequires: apr-devel >= 1.4.0, apr-util-devel >= 1.2.0, pcre-devel >= 5.0
BuildRequires: systemd-devel
Requires: /etc/mime.types, system-logos >= 7.92.1-1
Obsoletes: httpd-suexec
Provides: webserver
Provides: mod_dav = %{version}-%{release}, httpd-suexec = %{version}-%{release}
Provides: httpd-mmn = %{mmn}, httpd-mmn = %{mmnisa}, httpd-mmn = %{oldmmnisa}
Requires: httpd-tools = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires(pre): /usr/sbin/groupadd
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package devel
Group: Development/Libraries
Summary: Development interfaces for the Apache HTTP server
Obsoletes: secureweb-devel, apache-devel, stronghold-apache-devel
Requires: apr-devel, apr-util-devel, pkgconfig
Requires: httpd = %{version}-%{release}

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server
Requires: httpd = %{version}-%{release}
Obsoletes: secureweb-manual, apache-manual
BuildArch: noarch

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/2.2/.

%package tools
Group: System Environment/Daemons
Summary: Tools for use with the Apache HTTP Server

%description tools
The httpd-tools package contains tools which can be used with 
the Apache HTTP Server.

%package -n mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP Server
Epoch: 1
BuildRequires: openssl-devel >= 1:1.0.1e-37
Requires: openssl-libs >= 1:1.0.1e-37
Requires(post): openssl, /bin/cat, hostname
Requires(pre): httpd
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Obsoletes: stronghold-mod_ssl

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%package -n mod_proxy_html
Group: System Environment/Daemons
Summary: HTML and XML content filters for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
BuildRequires: libxml2-devel
Epoch: 1
Obsoletes: mod_proxy_html < 1:2.4.1-2

%description -n mod_proxy_html
The mod_proxy_html and mod_xml2enc modules provide filters which can
transform and modify HTML and XML content.

%package -n mod_ldap
Group: System Environment/Daemons
Summary: LDAP authentication modules for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Requires: apr-util-ldap

%description -n mod_ldap
The mod_ldap and mod_authnz_ldap modules add support for LDAP
authentication to the Apache HTTP Server.

%package -n mod_session
Group: System Environment/Daemons
Summary: Session interface for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Requires: apr-util-openssl

%description -n mod_session
The mod_session module and associated backends provide an abstract
interface for storing and accessing per-user session data.

%prep
%setup -q
%patch1 -p1 -b .apctl
%patch2 -p1 -b .apxs
%patch3 -p1 -b .deplibs
%patch5 -p1 -b .layout
%patch6 -p1 -b .apctlsystemd

%patch21 -p1 -b .fullrelease
%patch23 -p1 -b .export
%patch24 -p1 -b .corelimit
%patch25 -p1 -b .selinux
%patch26 -p1 -b .r1337344+
%patch27 -p1 -b .icons
%patch28 -p1 -b .r1332643+
%patch29 -p1 -b .systemd
%patch30 -p1 -b .cachehardmax
%patch31 -p1 -b .sslmultiproxy
%patch32 -p1 -b .r1537535
%patch33 -p1 -b .r1542327
rm modules/ssl/ssl_engine_dh.c
%patch34 -p1 -b .ssllargekeys
%patch35 -p1 -b .prehtaccess
%patch36 -p1 -b .r1573626
%patch37 -p1 -b .uds
%patch38 -p1 -b .upn
%patch39 -p1 -b .r1664565
%patch40 -p1 -b .r1861793+
%patch41 -p1 -b .session-expiry

%patch51 -p1 -b .sninotreq
%patch55 -p1 -b .malformedhost
%patch56 -p1 -b .uniqueid
%patch57 -p1 -b .ldaprefer
%patch58 -p1 -b .r1507681+
%patch59 -p1 -b .r1556473
%patch60 -p1 -b .r1553540
%patch61 -p1 -b .clientaddr
%patch62 -p1 -b .aboverflow
%patch63 -p1 -b .sigint
%patch64 -p1 -b .sslecdhauto
%patch65 -p1 -b .r1556818
%patch66 -p1 -b .r1618851
%patch67 -p1 -b .r1526189
%patch68 -p1 -b .r1663647
%patch69 -p1 -b .1569006
%patch70 -p1 -b .r1506474
%patch71 -p1 -b .bomb
%patch72 -p1 -b .r1604460
%patch73 -p1 -b .r1624349
%patch74 -p1 -b .abipv6
%patch75 -p1 -b .r1530280
%patch76 -p1 -b .r1633085
%patch78 -p1 -b .sslerrorfree
%patch79 -p1 -b .r1528556
%patch80 -p1 -b .r1594625
%patch81 -p1 -b .r1674222
%patch82 -p1 -b .envhttpd
%patch83 -p1 -b .rewritedir
%patch84 -p1 -b .r1420184
%patch85 -p1 -b .r1524368
%patch86 -p1 -b .r1528958
%patch87 -p1 -b .r1651083
%patch88 -p1 -b .r1688399
%patch89 -p1 -b .r1527509
%patch90 -p1 -b .apachectlstatus
%patch91 -p1 -b .r1650655
%patch92 -p1 -b .r1533448
%patch93 -p1 -b .r1610013
%patch94 -p1 -b .r1705528
%patch95 -p1 -b .r1684462
%patch96 -p1 -b .r1650677
%patch97 -p1 -b .r1621601
%patch98 -p1 -b .r1610396
%patch99 -p1 -b .rotatelogtimezone
%patch100 -p1 -b .absslerror
%patch101 -p1 -b .r1723522
%patch102 -p1 -b .r1681107
%patch103 -p1 -b .dhparamsfree
%patch104 -p1 -b .r1651658
%patch105 -p1 -b .r1560093
%patch106 -p1 -b .r1748212
%patch107 -p1 -b .r1570327
%patch108 -p1 -b .r1631119
%patch109 -p1 -b .r1593002
%patch110 -p1 -b .r1662640
%patch111 -p1 -b .r1348019
%patch112 -p1 -b .r1587053
%patch113 -p1 -b .mpmsegfault
%patch114 -p1 -b .r1681114
%patch115 -p1 -b .r1371876
%patch116 -p1 -b .r1726019
%patch117 -p1 -b .r1683112
%patch118 -p1 -b .r1651653
%patch119 -p1 -b .r1634529
%patch120 -p1 -b .r1738878
%patch121 -p1 -b .httpprotdefine
%patch122 -p1 -b .statement-comment
%patch123 -p1 -b .logrotate-zombie
%patch124 -p1 -b .modauthzdbd-segfault
%patch125 -p1 -b .r1668532
%patch126 -p1 -b .r1681289
%patch127 -p1 -b .r1805099
%patch128 -p1 -b .r1811831
%patch129 -p1 -b .r1811746
%patch130 -p1 -b .r1811976
%patch131 -p1 -b .r1650310
%patch132 -p1 -b .r1530999
%patch133 -p1 -b .r1555539
%patch134 -p1 -b .r1523536
%patch135 -p1 -b .r1826995
%patch136 -p1 -b .defaultport-proxy
%patch137 -p1 -b .r1825120
%patch138 -p1 -b .r1515372
%patch139 -p1 -b .r1824872
%patch140 -p1 -b .r1833014
%patch141 -p1 -b .r1583175
%patch142 -p1 -b .r1862604
%patch143 -p1 -b .ssl-close-notify-client
%patch144 -p1 -b .r1879224
%patch145 -p1 -b .r1881459
%patch146 -p1 -b .r1872790

%patch200 -p1 -b .cve6438
%patch201 -p1 -b .cve0098
%patch202 -p1 -b .cve0231
%patch203 -p1 -b .cve0117
%patch204 -p1 -b .cve0118
%patch205 -p1 -b .cve0226
%patch206 -p1 -b .cve4352
%patch207 -p1 -b .cve5704
%patch208 -p1 -b .cve3581
%patch209 -p1 -b .cve3185
%patch210 -p1 -b .cve3183
%patch211 -p1 -b .cve5387
%patch212 -p1 -b .cve8743
%patch213 -p1 -b .cve0736
%patch214 -p1 -b .cve2161
%patch215 -p1 -b .cve3167
%patch216 -p1 -b .cve3169
%patch217 -p1 -b .cve7668
%patch218 -p1 -b .cve7679
%patch219 -p1 -b .cve9788
%patch220 -p1 -b .cve9798
%patch221 -p1 -b .cve1312
%patch222 -p1 -b .cve0217
%patch223 -p1 -b .cve0220
%patch224 -p1 -b .cve15710
%patch225 -p1 -b .cve1301
%patch226 -p1 -b .cve17199
%patch227 -p1 -b .cve15715
%patch228 -p1 -b .cve10098
%patch229 -p1 -b .cve1303
%patch230 -p1 -b .cve1283
%patch240 -p1 -b .cve1934

# Patch in the vendor string and the release string
sed -i '/^#define PLATFORM/s/Unix/%{vstring}/' os/unix/os.h
sed -i 's/@RELEASE@/%{release}/' server/core.c

# Prevent use of setcap in "install-suexec-caps" target.
sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}
   : Update the mmn macro and rebuild.
   exit 1
fi

: Building with MMN %{mmn}, MMN-ISA %{mmnisa} and vendor string '%{vstring}'

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
	support/apxs.in

export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-Wl,-z,relro,-z,now"

%ifarch ppc64 ppc64le
%global _performance_build 1
%endif

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

# Build the daemon
%configure \
 	--prefix=%{_sysconfdir}/httpd \
 	--exec-prefix=%{_prefix} \
 	--bindir=%{_bindir} \
 	--sbindir=%{_sbindir} \
 	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir}/httpd/conf \
	--includedir=%{_includedir}/httpd \
	--libexecdir=%{_libdir}/httpd/modules \
	--datadir=%{contentdir} \
        --enable-layout=Fedora \
        --with-installbuilddir=%{_libdir}/httpd/build \
        --enable-mpms-shared=all \
        --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
	--enable-suexec --with-suexec \
        --enable-suexec-capabilities \
	--with-suexec-caller=%{suexec_caller} \
	--with-suexec-docroot=%{docroot} \
	--without-suexec-logfile \
        --with-suexec-syslog \
	--with-suexec-bin=%{_sbindir}/suexec \
	--with-suexec-uidmin=500 --with-suexec-gidmin=100 \
        --enable-pie \
        --with-pcre \
        --enable-mods-shared=all \
	--enable-ssl --with-ssl --disable-distcache \
	--enable-proxy \
        --enable-cache \
        --enable-disk-cache \
        --enable-ldap --enable-authnz-ldap \
        --enable-cgid --enable-cgi \
        --enable-authn-anon --enable-authn-alias \
        --disable-imagemap  \
	$*
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
for s in httpd htcacheclean; do
  install -p -m 644 $RPM_SOURCE_DIR/${s}.service \
                    $RPM_BUILD_ROOT%{_unitdir}/${s}.service
done

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d \
      $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README
for f in 00-base.conf 00-mpm.conf 00-lua.conf 01-cgi.conf 00-dav.conf \
         00-proxy.conf 00-ssl.conf 01-ldap.conf 00-proxyhtml.conf \
         01-ldap.conf 00-systemd.conf 01-session.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/$f
done

for f in welcome.conf ssl.conf manual.conf userdir.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
done

# Split-out extra config shipped as default in conf.d:
for f in autoindex; do
  mv docs/conf/extra/httpd-${f}.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/${f}.conf
done

# Extra config trimmed:
rm -v docs/conf/extra/httpd-{ssl,userdir}.conf

rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf
install -m 644 -p $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
for s in httpd htcacheclean; do
  install -m 644 -p $RPM_SOURCE_DIR/${s}.sysconf \
                    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/${s}
done

# tmpfiles.d configuration
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d 
install -m 644 -p $RPM_SOURCE_DIR/httpd.tmpfiles \
   $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/httpd.conf

# Other directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dav \
         $RPM_BUILD_ROOT/run/httpd/htcacheclean

# Create cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/proxy \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/ssl

# Make the MMN accessible to module packages
echo %{mmnisa} > $RPM_BUILD_ROOT%{_includedir}/httpd/.mmn
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat > $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.httpd <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %{_bindir}/apxs
%%_httpd_modconfdir %{_sysconfdir}/httpd/conf.modules.d
%%_httpd_confdir %{_sysconfdir}/httpd/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %{_libdir}/httpd/modules
EOF

# Handle contentdir
mkdir $RPM_BUILD_ROOT%{contentdir}/noindex
install -m 644 -p $RPM_SOURCE_DIR/index.html \
        $RPM_BUILD_ROOT%{contentdir}/noindex/index.html

rm -rf %{contentdir}/htdocs

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# Clean Document Root
rm -v $RPM_BUILD_ROOT%{docroot}/html/*.html \
      $RPM_BUILD_ROOT%{docroot}/cgi-bin/*

# Symlink for the powered-by-$DISTRO image:
ln -s ../../pixmaps/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

# symlinks for /etc/httpd
ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s /run/httpd $RPM_BUILD_ROOT/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

# install http-ssl-pass-dialog
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m755 $RPM_SOURCE_DIR/httpd-ssl-pass-dialog \
	$RPM_BUILD_ROOT%{_libexecdir}/httpd-ssl-pass-dialog

# Install action scripts
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd
for f in graceful configtest; do
    install -p -m 755 $RPM_SOURCE_DIR/action-${f}.sh \
            $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd/${f}
done

# Install logrotate config
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
	$RPM_BUILD_ROOT/etc/logrotate.d/httpd

# fix man page paths
sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/httpd/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/httpd/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|/var/log/httpd/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|/var/log/httpd/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|/run/httpd/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/httpd|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/special.mk

# Remove unpackaged files
rm -vf \
      $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/{ap?-config,dbmmanage} \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}

%pre
# Add the "apache" group and user
/usr/sbin/groupadd -g 48 -r apache 2> /dev/null || :
/usr/sbin/useradd -c "Apache" -u 48 -g apache \
	-s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :

%post
%systemd_post httpd.service htcacheclean.service

%preun
%systemd_preun httpd.service htcacheclean.service

%postun
%systemd_postun

# Trigger for conversion from SysV, per guidelines at:
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
%triggerun -- httpd < 2.2.21-5
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save httpd.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del httpd >/dev/null 2>&1 || :

%posttrans
test -f /etc/sysconfig/httpd-disable-posttrans || \
  /bin/systemctl try-restart httpd.service htcacheclean.service >/dev/null 2>&1 || :

%define sslcert %{_sysconfdir}/pki/tls/certs/localhost.crt
%define sslkey %{_sysconfdir}/pki/tls/private/localhost.key

%post -n mod_ssl
umask 077

if [ -f %{sslkey} -o -f %{sslcert} ]; then
   exit 0
fi

%{_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 2048 > %{sslkey} 2> /dev/null

FQDN=`hostname`
if [ "x${FQDN}" = "x" -o ${#FQDN} -gt 59 ]; then
   FQDN=localhost.localdomain
fi

cat << EOF | %{_bindir}/openssl req -new -key %{sslkey} \
         -x509 -sha256 -days 365 -set_serial $RANDOM -extensions v3_req \
         -out %{sslcert} 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF

%check
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc docs/conf/extra/*.conf

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic

%config(noreplace) %{_sysconfdir}/logrotate.d/httpd

%dir %{_sysconfdir}/httpd/conf.d
%{_sysconfdir}/httpd/conf.d/README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.d/ssl.conf
%exclude %{_sysconfdir}/httpd/conf.d/manual.conf

%dir %{_sysconfdir}/httpd/conf.modules.d
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%config(noreplace) %{_sysconfdir}/sysconfig/ht*
%{_prefix}/lib/tmpfiles.d/httpd.conf

%dir %{_libexecdir}/initscripts/legacy-actions/httpd
%{_libexecdir}/initscripts/legacy-actions/httpd/*

%{_sbindir}/ht*
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%caps(cap_setuid,cap_setgid+pe) %attr(510,root,%{suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod*.so
%exclude %{_libdir}/httpd/modules/mod_auth_form.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so
%exclude %{_libdir}/httpd/modules/mod_*ldap.so
%exclude %{_libdir}/httpd/modules/mod_proxy_html.so
%exclude %{_libdir}/httpd/modules/mod_xml2enc.so
%exclude %{_libdir}/httpd/modules/mod_session*.so

%dir %{contentdir}
%dir %{contentdir}/icons
%dir %{contentdir}/error
%dir %{contentdir}/error/include
%dir %{contentdir}/noindex
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/*.var
%{contentdir}/error/include/*.html
%{contentdir}/noindex/index.html

%dir %{docroot}
%dir %{docroot}/cgi-bin
%dir %{docroot}/html

%attr(0710,root,apache) %dir /run/httpd
%attr(0700,apache,apache) %dir /run/httpd/htcacheclean
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/dav
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/proxy

%{_mandir}/man8/*

%{_unitdir}/*.service

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%doc LICENSE NOTICE
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files manual
%defattr(-,root,root)
%{contentdir}/manual
%config(noreplace) %{_sysconfdir}/httpd/conf.d/manual.conf

%files -n mod_ssl
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/httpd/ssl
%{_libexecdir}/httpd-ssl-pass-dialog

%files -n mod_proxy_html
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_proxy_html.so
%{_libdir}/httpd/modules/mod_xml2enc.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf

%files -n mod_ldap
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_*ldap.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf

%files -n mod_session
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_session*.so
%{_libdir}/httpd/modules/mod_auth_form.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%files devel
%defattr(-,root,root)
%{_includedir}/httpd
%{_bindir}/apxs
%{_mandir}/man1/apxs.1*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh
%{_sysconfdir}/rpm/macros.httpd

%changelog
* Thu Nov 19 2020 Jacco Ligthart <jacco@redsleeve.org> - 2.4.6-97.el7.redsleeve
- roll in redsleeve branding, based on RHEL

* Tue Nov 10 2020 CentOS Sources <bugs@centos.org> - 2.4.6-97.el7.centos
- Remove index.html, add centos-noindex.tar.gz
- change vstring
- change symlink for poweredby.png
- update welcome.conf with proper aliases

* Wed Oct 07 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.6-97
- Resolves: #1852350 - httpd/mod_proxy_http/mod_ssl aborted when sending
  a client cert to backend server
- Resolves: #1785100 - mod_cgid takes CGIDScriptTimeout x 2 seconds for timeout
- Resolves: #1862499 - Intermittent Segfault in Apache httpd due to pool
  concurrency issues

* Fri Apr 17 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.6-95
- Resolves: #1823262 - CVE-2020-1934 httpd: mod_proxy_ftp use of uninitialized
  value

* Thu Mar 26 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.6-94
- Resolves: #1565491 - CVE-2017-15715 httpd: <FilesMatch> bypass with a trailing
  newline in the file name
- Resolves: #1747283 - CVE-2019-10098 httpd: mod_rewrite potential open redirect
- Resolves: #1724879 - httpd terminates all SSL connections using an abortive
  shutdown
- Resolves: #1715981 - Backport of SessionExpiryUpdateInterval directive
- Resolves: #1565457 - CVE-2018-1303 httpd: Out of bounds read in
  mod_cache_socache can allow a remote attacker to cause a denial of service
- Resolves: #1566531 - CVE-2018-1283 httpd: Improper handling of headers in 
  mod_session can allow a remote user to modify session data for CGI applications

* Tue Oct 08 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.6-93
- Resolves: #1677496 - CVE-2018-17199 httpd: mod_session_cookie does not respect
  expiry time

* Thu Aug 22 2019 Joe Orton <jorton@redhat.com> - 2.4.6-92
- htpasswd: add SHA-2 crypt() support (#1486889)

* Wed Jul 31 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.6-91
- Resolves: #1630886 - scriptlet can fail if hostname is not installed
- Resolves: #1565465 - CVE-2017-15710 httpd: Out of bound write in
  mod_authnz_ldap when using too small Accept-Language values
- Resolves: #1568298 - CVE-2018-1301 httpd: Out of bounds access after
  failure in reading the HTTP request
- Resolves: #1673457 - Apache child process crashes because ScriptAliasMatch
  directive
- Resolves: #1633152 - mod_session missing apr-util-openssl
- Resolves: #1649470 - httpd response contains garbage in Content-Type header
- Resolves: #1724034 - Unexpected OCSP in proxy SSL connection

* Sat Jun 08 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.6-90
- Resolves: #1566317 - CVE-2018-1312 httpd: Weak Digest auth nonce generation
  in mod_auth_digest
- Resolves: #1696141 - CVE-2019-0217 httpd: mod_auth_digest: access control
  bypass due to race condition
- Resolves: #1696096 - CVE-2019-0220 httpd: URL normalization inconsistency

* Fri Mar 15 2019 Joe Orton <jorton@redhat.com> - 2.4.6-89
- fix per-request leak of bucket brigade structure (#1583218)

* Thu Jun 21 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-88
- Resolves: #1527295 - httpd with worker/event mpm segfaults after multiple
  SIGUSR1

* Thu Jun 21 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-87
- Resolves: #1458364 - RMM list corruption in ldap module results in server hang

* Thu Jun 21 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-86
- Resolves: #1493181 - RFE: mod_ssl: allow sending multiple CA names which
  differ only in case

* Wed Jun 20 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-85
- Resolves: #1556761 - mod_proxy_wstunned config needs the default port number

* Mon Jun 18 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-84
- Resolves: #1548501 - Make OCSP more configurable (like CRL)

* Mon Jun 11 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-83
- Resolves: #1523536 - Backport Apache BZ#59230 mod_proxy_express uses db
  after close

* Mon Jun 11 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-82
- Resolves: #1533793 - Use Variable with mod_authnz_ldap

* Mon Mar 26 2018 Joe Orton <jorton@redhat.com> - 2.4.6-81
- don't terminate connections during graceful stop/restart (#1557785)

* Mon Jan 08 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-80
- Related: #1288395 - httpd segfault when logrotate invoked

* Wed Nov 01 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-79
- Resolves: #1274890 - mod_ssl config: tighten defaults

* Tue Oct 31 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-78
- Resolves: #1506392 - Backport: SSLSessionTickets directive support

* Mon Oct 16 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-77
- Resolves: #1440590 - Need an option to disable UTF8-conversion
  of certificate DN

* Thu Oct 12 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-76
- Resolves: #1464406 - Apache consumes too much memory for CGI output

* Thu Oct 12 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-75
- Resolves: #1448892 - Cannot override LD_LIBARY_PATH in Apache HTTPD
  using SetEnv or PassEnv. Needs documentation.

* Mon Oct 09 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-74
- Resolves: #1430640 - "ProxyAddHeaders Off" does not become effective
  when it's defined outside <Proxy> setting

* Fri Oct 06 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-73
- Resolves: #1499253 - ProxyRemote with HTTPS backend sends requests
  with absoluteURI instead of abs_path

* Tue Oct 03 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-72
- Resolves: #1288395 - httpd segfault when logrotate invoked

* Tue Oct 03 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-71
- Resolves: #1368491 - mod_authz_dbd segfaults when AuthzDBDQuery missing

* Mon Oct 02 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-70
- Resolves: #1467402 - rotatelogs: creation of zombie processes when -p is used

* Tue Sep 19 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-69
- Resolves: #1493065 - CVE-2017-9798 httpd: Use-after-free by limiting
  unregistered HTTP method

* Tue Jul 25 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-68
- Resolves: #1463194 - CVE-2017-3167 httpd: ap_get_basic_auth_pw()
  authentication bypass
- Resolves: #1463197 - CVE-2017-3169 httpd: mod_ssl NULL pointer dereference
- Resolves: #1463207 - CVE-2017-7679 httpd: mod_mime buffer overread
- Resolves: #1463205 - CVE-2017-7668 httpd: ap_find_token() buffer overread
- Resolves: #1470748 - CVE-2017-9788 httpd: Uninitialized memory reflection
  in mod_auth_digest

* Tue May 09 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-67
- Related: #1332242 - Explicitly disallow the '#' character in allow,deny
  directives

* Tue May 09 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-66
- Related: #1332242 - Explicitly disallow the '#' character in allow,deny
  directives

* Thu Apr 27 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-65
- Resolves: #1445885 - define _RH_HAS_HTTPPROTOCOLOPTIONS

* Tue Apr 18 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-64
- Resolves: #1442872 - apache user is not created during httpd installation
  when apache group already exist with GID other than 48

* Wed Mar 22 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-63
- Related: #1412976 - CVE-2016-0736 CVE-2016-2161 CVE-2016-8743
  httpd: various flaws

* Wed Mar 15 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-62
- Resolves: #1397241 - Backport Apache Bug 53098 - mod_proxy_ajp:
  patch to set worker secret passed to tomcat

* Wed Mar 15 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-61
- Related: #1414258 - Crash during restart or at startup in mod_ssl,
  in certinfo_free() function registered by ssl_stapling_ex_init()

* Tue Mar 14 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-60
- Resolves: #1414258 - Crash during restart or at startup in mod_ssl,
  in certinfo_free() function registered by ssl_stapling_ex_init()

* Mon Mar 13 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-59
- Resolves: #1378946 - Backport of apache bug 55910: Continuation lines
  are broken during buffer resize

* Fri Mar 10 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-58
- Resolves: #1364604 - Upstream Bug 56925 - ErrorDocument directive misbehaves
  with mod_proxy_http and mod_proxy_ajp

* Thu Mar 09 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-57
- Resolves: #1324416 - Error 404 when switching language in HTML manual
  more than once

* Wed Mar 08 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-56
- Resolves: #1353740 - Backport Apache PR58118 to fix mod_proxy_fcgi
  spamming non-errors: AH01075: Error dispatching request to : (passing
  brigade to output filters)

* Wed Mar 08 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-55
- Resolves: #1371876 - Apache httpd returns "200 OK" for a request
  exceeding LimitRequestBody when enabling mod_ext_filter

* Tue Mar 07 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-54
- Resolves: #1372692 - Apache httpd does not log status code "413" in
  access_log when exceeding LimitRequestBody

* Tue Mar 07 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-53
- Resolves: #1376835 - httpd with worker/event mpm segfaults after multiple
  successive graceful reloads

* Tue Mar 07 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-52
- Resolves: #1332242 - Explicitly disallow the '#' character in allow,deny
  directives

* Mon Mar 06 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-51
- Resolves: #1396197 - Backport: mod_proxy_wstunnel - AH02447: err/hup
  on backconn

* Mon Mar 06 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-50
- Resolves: #1348019 - mod_proxy: Fix a race condition that caused a failed
  worker to be retried before the retry period is over

* Mon Mar 06 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-49
- Resolves: #1389535 - Segmentation fault in SSL_renegotiate

* Mon Mar 06 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-48
- Resolves: #1406184 - stapling_renew_response: abort early
  (before apr_uri_parse) if ocspuri is empty

* Tue Feb  7 2017 Joe Orton <jorton@redhat.com> - 2.4.6-47
- prefork: fix delay completing graceful restart (#1327624)
- mod_ldap: fix authz regression, failing to rebind (#1415257)

* Thu Jan 26 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-46
- Resolves: #1412976 - CVE-2016-0736 CVE-2016-2161 CVE-2016-8743
  httpd: various flaws

* Wed Aug 03 2016 Luboš Uhliarik <luhliari@redhat.com> - 2.4.6-45
- RFE: run mod_rewrite external mapping program as non-root (#1316900)

* Tue Jul 12 2016 Joe Orton <jorton@redhat.com> - 2.4.6-44
- add security fix for CVE-2016-5387

* Tue Jul  5 2016 Joe Orton <jorton@redhat.com> - 2.4.6-43
- add 451 (Unavailable For Legal Reasons) response status-code (#1343582)

* Fri Jun 17 2016 Joe Orton <jorton@redhat.com> - 2.4.6-42
- mod_cache: treat cache as valid with changed Expires in 304 (#1331341)

* Wed Feb 24 2016 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-41
- mod_cache: merge r->err_headers_out into r->headers when the response
  is cached for the first time (#1264989)
- mod_ssl: Do not send SSL warning when SNI hostname is not found as per
  RFC 6066 (#1298148)
- mod_proxy_fcgi: Ignore body data from backend for 304 responses (#1263038)
- fix apache user creation when apache group already exists (#1299889)
- fix apache user creation when USERGROUPS_ENAB is set to 'no' (#1288757)
- mod_proxy: fix slow response time for reponses with error status code
  when using ProxyErrorOverride (#1283653)
- mod_ldap: Respect LDAPConnectionPoolTTL for authn connections (#1300149)
- mod_ssl: use "localhost" in the dummy SSL cert for long FQDNs (#1240495)
- rotatelogs: improve support for localtime (#1244545)
- ab: fix read failure when targeting SSL server (#1255331)
- mod_log_debug: fix LogMessage example in documentation (#1279465)
- mod_authz_dbd, mod_authn_dbd, mod_session_dbd, mod_rewrite: Fix lifetime
  of DB lookup entries independently of the selected DB engine (#1287844)
- mod_ssl: fix hardware crypto support with custom DH parms (#1291865)
- mod_proxy_fcgi: fix SCRIPT_FILENAME when a balancer is used (#1302797)

* Thu Sep 17 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-40
- mod_dav: follow up fix for previous commit (#1263975)

* Wed Aug 26 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-39
- mod_dav: treat dav_resource uri as escaped (#1255480)

* Wed Aug 19 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-38
- mod_ssl: add support for User Principal Name in SSLUserName  (#1242503)

* Mon Aug 10 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-37
- core: fix chunk header parsing defect (CVE-2015-3183)
- core: replace of ap_some_auth_required with ap_some_authn_required
  and ap_force_authn hook (CVE-2015-3185)

* Tue Jul 14 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-36
- Revert fix for #1162152, it is not needed in RHEL7
- mod_proxy_ajp: fix settings ProxyPass parameters for AJP backends (#1242416)

* Wed Jul 01 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-35
- mod_remoteip: correct the trusted proxy match test (#1179306)
- mod_dav: send complete response when resource is created (#1235383)
- apachectl: correct the apachectl status man page (#1231924)

* Wed Jun 03 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-34
- mod_proxy_fcgi: honor Timeout / ProxyTimeout (#1222328)
- do not show all vhosts twice in httpd -D DUMP_VHOSTS output (#1225820)
- fix -D[efined] or <Define>[d] variables lifetime accross restarts (#1227219)
- mod_ssl: do not send NPN extension with not configured (#1226015)

* Mon May 18 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-33
- mod_authz_dbm: fix crash when using "Require dbm-file-group" (#1221575)

* Wed Apr 15 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-32
- mod_authn_dbd: fix use-after-free bug with postgresql (#1188779)
- mod_remoteip: correct the trusted proxy match test (#1179306)
- mod_status: honor remote_ip as documented (#1169081)
- mod_deflate: fix decompression of files larger than 4GB (#1170214)
- core: improve error message for inaccessible DocumentRoot (#1170220)
- ab: try all addresses instead of failing on first one when not available (#1125276)
- mod_proxy_wstunnel: add support for SSL (#1180745)
- mod_proxy_wstunnel: load this module by default (#1180745)
- mod_rewrite: add support for WebSockets (#1180745)
- mod_rewrite: do not search for directory if a URL will be rewritten (#1210091)
- mod_ssl: Fix SSL_CLIENT_VERIFY value when optional_no_ca and SSLSessionCache
  are used and SSL session is resumed (#1170206)
- mod_ssl: fix memory leak on httpd reloads (#1181690)
- mod_ssl: use SSLCipherSuite HIGH:MEDIUM:!aNULL:!MD5:!SEED:!IDEA (#1118476)
- mod_cgi: return error code 408 on timeout (#1162152)
- mod_dav_fs: set default value of DAVLockDB (#1176449)
- add Documentation= to the httpd.service and htcacheclean.service (#1184118)
- do not display "bomb" icon for files ending with "core" (#1170215)
- add missing Reason-Phrase in HTTP response headers (#1162159)
- fix BuildRequires to require openssl-devel >= 1:1.0.1e-37 (#1160625)
- apachectl: ignore HTTPD variable from sysconfig (#1214401)
- apachectl: fix "graceful" documentation (#1214398)
- apachectl: fix "graceful" behaviour when httpd is not running (#1214430)

* Tue Dec 02 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-31
- mod_proxy_fcgi: determine if FCGI_CONN_CLOSE should be enabled
  instead of hardcoding it (#1168050)
- mod_proxy: support Unix Domain Sockets (#1168081)

* Tue Nov 25 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-30
- core: fix bypassing of mod_headers rules via chunked requests (CVE-2013-5704)
- mod_cache: fix NULL pointer dereference on empty Content-Type (CVE-2014-3581)

* Tue Nov 04 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-29
- rebuild against proper version of OpenSSL (#1080125)

* Wed Oct 22 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-28
- set vstring based on /etc/os-release (#1114123)

* Mon Oct 06 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-27
- fix the dependency on openssl-libs to match the fix for #1080125

* Mon Sep 22 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-26
- allow <Auth*ProviderAlias>'es to be seen under virtual hosts (#1131847)

* Fri Sep 19 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-25
- do not use hardcoded curve for ECDHE suites (#1080125)

* Wed Sep 03 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-24
- allow reverse-proxy to be set via SetHandler (#1136290)

* Thu Aug 21 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-23
- fix possible crash in SIGINT handling (#1131006)

* Mon Aug 18 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-22
- ab: fix integer overflow when printing stats with lot of requests (#1092420)

* Mon Aug 11 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-21
- add pre_htaccess so mpm-itk can be build as separate module (#1059143)

* Tue Aug 05 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-20
- mod_ssl: prefer larger keys and support up to 8192-bit keys (#1073078)

* Mon Aug 04 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-19
- fix build on ppc64le by using configure macro (#1125545)
- compile httpd with -O3 on ppc64le (#1123490)
- mod_rewrite: expose CONN_REMOTE_ADDR (#1060536)

* Thu Jul 17 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-18
- mod_cgid: add security fix for CVE-2014-0231 (#1120608)
- mod_proxy: add security fix for CVE-2014-0117 (#1120608)
- mod_deflate: add security fix for CVE-2014-0118 (#1120608)
- mod_status: add security fix for CVE-2014-0226 (#1120608)
- mod_cache: add secutiry fix for CVE-2013-4352 (#1120608)

* Thu Mar 20 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-17
- mod_dav: add security fix for CVE-2013-6438 (#1077907)
- mod_log_config: add security fix for CVE-2014-0098 (#1077907)

* Wed Mar  5 2014 Joe Orton <jorton@redhat.com> - 2.4.6-16
- mod_ssl: improve DH temp key handling (#1057687)

* Wed Mar  5 2014 Joe Orton <jorton@redhat.com> - 2.4.6-15
- mod_ssl: use 2048-bit RSA key with SHA-256 signature in dummy certificate (#1071276)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.4.6-14
- Mass rebuild 2014-01-24

* Mon Jan 13 2014 Joe Orton <jorton@redhat.com> - 2.4.6-13
- mod_ssl: sanity-check use of "SSLCompression" (#1036666)
- mod_proxy_http: fix brigade memory usage (#1040447)

* Fri Jan 10 2014 Joe Orton <jorton@redhat.com> - 2.4.6-12
- rebuild

* Thu Jan  9 2014 Joe Orton <jorton@redhat.com> - 2.4.6-11
- build with -O3 on ppc64 (#1051066)

* Tue Jan  7 2014 Joe Orton <jorton@redhat.com> - 2.4.6-10
- mod_dav: fix locktoken handling (#1004046)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.4.6-9
- Mass rebuild 2013-12-27

* Fri Dec 20 2013 Joe Orton <jorton@redhat.com> - 2.4.6-8
- use unambiguous httpd-mmn (#1029360)

* Fri Nov   1 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-7
- mod_ssl: allow SSLEngine to override Listen-based default (#1023168)

* Thu Oct  31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-6
- systemd: Use {MAINPID} notation in service file (#969972)

* Thu Oct 24 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-5
- systemd: send SIGWINCH signal without httpd -k in ExecStop (#969972)

* Thu Oct 03 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-4
- expand macros in macros.httpd (#1011393)

* Mon Aug 26 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-3
- fix "LDAPReferrals off" to really disable LDAP Referrals

* Wed Jul 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-2
- revert fix for dumping vhosts twice

* Mon Jul 22 2013 Joe Orton <jorton@redhat.com> - 2.4.6-1
- update to 2.4.6
- mod_ssl: use revised NPN API (r1487772)

* Thu Jul 11 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-12
- mod_unique_id: replace use of hostname + pid with PRNG output (#976666)
- apxs: mention -p option in manpage

* Tue Jul  2 2013 Joe Orton <jorton@redhat.com> - 2.4.4-11
- add patch for aarch64 (Dennis Gilmore, #925558)

* Mon Jul  1 2013 Joe Orton <jorton@redhat.com> - 2.4.4-10
- remove duplicate apxs man page from httpd-tools

* Mon Jun 17 2013 Joe Orton <jorton@redhat.com> - 2.4.4-9
- remove zombie dbmmanage script

* Fri May 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-8
- return 400 Bad Request on malformed Host header

* Mon May 20 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-6
- htpasswd/htdbm: fix hash generation bug (#956344)
- do not dump vhosts twice in httpd -S output (#928761)
- mod_cache: fix potential crash caused by uninitialized variable (#954109)

* Thu Apr 18 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-5
- execute systemctl reload as result of apachectl graceful
- mod_ssl: ignore SNI hints unless required by config
- mod_cache: forward-port CacheMaxExpire "hard" option
- mod_ssl: fall back on another module's proxy hook if mod_ssl proxy
  is not configured.

* Tue Apr 16 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-4
- fix service file to not send SIGTERM after ExecStop (#906321, #912288)

* Tue Mar 26 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-3
- protect MIMEMagicFile with IfModule (#893949)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-2
- really package mod_auth_form in mod_session (#915438)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-1
- update to 2.4.4
- fix duplicate ownership of mod_session config (#914901)

* Fri Feb 22 2013 Joe Orton <jorton@redhat.com> - 2.4.3-17
- add mod_session subpackage, move mod_auth_form there (#894500)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Joe Orton <jorton@redhat.com> - 2.4.3-15
- add systemd service for htcacheclean

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-14
- drop patch for r1344712

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-13
- filter mod_*.so auto-provides (thanks to rcollet)
- pull in syslog logging fix from upstream (r1344712)

* Fri Oct 26 2012 Joe Orton <jorton@redhat.com> - 2.4.3-12
- rebuild to pick up new apr-util-ldap

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 2.4.3-11
- rebuild

* Wed Oct  3 2012 Joe Orton <jorton@redhat.com> - 2.4.3-10
- pull upstream patch r1392850 in addition to r1387633

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9.1
- restore "ServerTokens Full-Release" support (#811714)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9
- define PLATFORM in os.h using vendor string

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-8
- use systemd script unconditionally (#850149)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-7
- use systemd scriptlets if available (#850149)
- don't run posttrans restart if /etc/sysconfig/httpd-disable-posttrans exists

* Mon Oct 01 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-6
- use systemctl from apachectl (#842736)

* Wed Sep 19 2012 Joe Orton <jorton@redhat.com> - 2.4.3-5
- fix some error log spam with graceful-stop (r1387633)
- minor mod_systemd tweaks

* Thu Sep 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-4
- use IncludeOptional for conf.d/*.conf inclusion

* Fri Sep 07 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-3
- adding mod_systemd to integrate with systemd better

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-2
- mod_ssl: add check for proxy keypair match (upstream r1374214)

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-1
- update to 2.4.3 (#849883)
- own the docroot (#848121)

* Mon Aug  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-23
- add mod_proxy fixes from upstream (r1366693, r1365604)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-21
- drop explicit version requirement on initscripts

* Thu Jul  5 2012 Joe Orton <jorton@redhat.com> - 2.4.2-20
- mod_ext_filter: fix error_log warnings

* Mon Jul  2 2012 Joe Orton <jorton@redhat.com> - 2.4.2-19
- support "configtest" and "graceful" as initscripts "legacy actions"

* Fri Jun  8 2012 Joe Orton <jorton@redhat.com> - 2.4.2-18
- avoid use of "core" GIF for a "core" directory (#168776)
- drop use of "syslog.target" in systemd unit file

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-17
- use _unitdir for systemd unit file
- use /run in unit file, ssl.conf

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-16
- mod_ssl: fix NPN patch merge

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-15
- move tmpfiles.d fragment into /usr/lib per new guidelines
- package /run/httpd not /var/run/httpd
- set runtimedir to /run/httpd likewise

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-14
- fix htdbm/htpasswd crash on crypt() failure (#818684)

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-13
- pull fix for NPN patch from upstream (r1345599)

* Thu May 31 2012 Joe Orton <jorton@redhat.com> - 2.4.2-12
- update suexec patch to use LOG_AUTHPRIV facility

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-11
- really fix autoindex.conf (thanks to remi@)

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-10
- fix autoindex.conf to allow symlink to poweredby.png

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-9
- suexec: use upstream version of patch for capability bit support

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-8
- suexec: use syslog rather than suexec.log, drop dac_override capability

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-7
- mod_ssl: add TLS NPN support (r1332643, #809599)

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-6
- add BR on APR >= 1.4.0

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-5
- use systemctl from logrotate (#221073)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-4
- pull from upstream:
  * use TLS close_notify alert for dummy_connection (r1326980+)
  * cleanup symbol exports (r1327036+)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3.2
- rebuild

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3
- really fix restart

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-2
- tweak default ssl.conf
- fix restart handling (#814645)
- use graceful restart by default

* Wed Apr 18 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.2-1
- update to 2.4.2

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-6
- fix macros

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-5
- add _httpd_moddir to macros

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-4
- fix symlink for poweredby.png
- fix manual.conf

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-3
- add mod_proxy_html subpackage (w/mod_proxy_html + mod_xml2enc)
- move mod_ldap, mod_authnz_ldap to mod_ldap subpackage

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-2
- clean docroot better
- ship proxy, ssl directories within /var/cache/httpd
- default config:
 * unrestricted access to (only) /var/www
 * remove (commented) Mutex, MaxRanges, ScriptSock
 * split autoindex config to conf.d/autoindex.conf
- ship additional example configs in docdir

* Tue Mar  6 2012 Joe Orton <jorton@redhat.com> - 2.4.1-1
- update to 2.4.1
- adopt upstream default httpd.conf (almost verbatim)
- split all LoadModules to conf.modules.d/*.conf
- include conf.d/*.conf at end of httpd.conf
- trim %%changelog

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-2
- fix build against PCRE 8.30

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-1
- update to 2.2.22

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.2.21-8
- Rebuild against PCRE 8.30

* Mon Jan 23 2012 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-7
- fix #783629 - start httpd after named

* Mon Jan 16 2012 Joe Orton <jorton@redhat.com> - 2.2.21-6
- complete conversion to systemd, drop init script (#770311)
- fix comments in /etc/sysconfig/httpd (#771024)
- enable PrivateTmp in service file (#781440)
- set LANG=C in /etc/sysconfig/httpd

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-4
- fix #751591 - start httpd after remote-fs

* Mon Oct 24 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-3
- allow change state of BalancerMember in mod_proxy_balancer web interface

* Thu Sep 22 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.2.21-2
- Make mmn available as %%{_httpd_mmn}.
- Add .svgz to AddEncoding x-gzip example in httpd.conf.

* Tue Sep 13 2011 Joe Orton <jorton@redhat.com> - 2.2.21-1
- update to 2.2.21

* Mon Sep  5 2011 Joe Orton <jorton@redhat.com> - 2.2.20-1
- update to 2.2.20
- fix MPM stub man page generation

* Wed Aug 10 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-5
- fix #707917 - add httpd-ssl-pass-dialog to ask for SSL password using systemd

* Fri Jul 22 2011 Iain Arnell <iarnell@gmail.com> 1:2.2.19-4
- rebuild while rpm-4.9.1 is untagged to remove trailing slash in provided
  directory names

* Wed Jul 20 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-3
- fix #716621 - suexec now works without setuid bit

* Thu Jul 14 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-2
- fix #689091 - backported patch from 2.3 branch to support IPv6 in logresolve

* Fri Jul  1 2011 Joe Orton <jorton@redhat.com> - 2.2.19-1
- update to 2.2.19
- enable dbd, authn_dbd in default config

* Thu Apr 14 2011 Joe Orton <jorton@redhat.com> - 2.2.17-13
- fix path expansion in service files

* Tue Apr 12 2011 Joe Orton <jorton@redhat.com> - 2.2.17-12
- add systemd service files (#684175, thanks to Jóhann B. Guðmundsson)

* Wed Mar 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-11
- minor updates to httpd.conf
- drop old patches

* Wed Mar  2 2011 Joe Orton <jorton@redhat.com> - 2.2.17-10
- rebuild

* Wed Feb 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-9
- use arch-specific mmn

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Joe Orton <jorton@redhat.com> - 2.2.17-7
- generate dummy mod_ssl cert with CA:FALSE constraint (#667841)
- add man page stubs for httpd.event, httpd.worker
- drop distcache support
- add STOP_TIMEOUT support to init script

* Sat Jan  8 2011 Joe Orton <jorton@redhat.com> - 2.2.17-6
- update default SSLCipherSuite per upstream trunk

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-5
- fix requires (#667397)

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-4
- de-ghost /var/run/httpd

* Tue Jan  4 2011 Joe Orton <jorton@redhat.com> - 2.2.17-3
- add tmpfiles.d configuration, ghost /var/run/httpd (#656600)

* Sat Nov 20 2010 Joe Orton <jorton@redhat.com> - 2.2.17-2
- drop setuid bit, use capabilities for suexec binary

* Wed Oct 27 2010 Joe Orton <jorton@redhat.com> - 2.2.17-1
- update to 2.2.17

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 2.2.16-2
- link everything using -z relro and -z now

* Mon Jul 26 2010 Joe Orton <jorton@redhat.com> - 2.2.16-1
- update to 2.2.16

* Fri Jul  9 2010 Joe Orton <jorton@redhat.com> - 2.2.15-3
- default config tweaks:
 * harden httpd.conf w.r.t. .htaccess restriction (#591293)
 * load mod_substitute, mod_version by default
 * drop proxy_ajp.conf, load mod_proxy_ajp in httpd.conf
 * add commented list of shipped-but-unloaded modules
 * bump up worker defaults a little
 * drop KeepAliveTimeout to 5 secs per upstream
- fix LSB compliance in init script (#522074)
- bundle NOTICE in -tools
- use init script in logrotate postrotate to pick up PIDFILE
- drop some old Obsoletes/Conflicts

* Sun Apr 04 2010 Robert Scheck <robert@fedoraproject.org> - 2.2.15-1
- update to 2.2.15 (#572404, #579311)

