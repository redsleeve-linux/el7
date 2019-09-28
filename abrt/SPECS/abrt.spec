%{!?python_site: %global python_site %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
# platform-dependent
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# http://fedoraproject.org/wiki/Packaging:Guidelines#PIE
# http://fedoraproject.org/wiki/Hardened_Packages
%global _hardened_build 1

%if 0%{?fedora} >= 14
    %bcond_without systemd
%else
    %bcond_with systemd
%endif

# systemd wasn't set by the code above - so we're on old Fedora or we're not on Fedora at all
%if %{without systemd}
    %if 0%{?rhel} >= 7
        %bcond_without systemd
    %else
        %bcond_with systemd
    %endif
%endif

%if 0%{?rhel} >= 6
%define desktopvendor redhat
%else
%define desktopvendor fedora
%endif

%define libreport_ver 2.1.11-43
%define satyr_ver 0.13-10

Summary: Automatic bug detection and reporting tool
Name: abrt
Version: 2.1.11
Release: 55%{?dist}.redsleeve
License: GPLv2+
Group: Applications/System
URL: https://abrt.readthedocs.org/
Source: %{name}-%{version}.tar.gz

Patch1: 0001-Do-not-enabled-Shortened-reporting-in-GNOME.patch
Patch2: 0002-remove-abrt-bodhi-from-configuration.patch
Patch3: 0003-replace-all-Fedora-URLs-by-corresponding-values-for-.patch
Patch4: 0004-have-AutoreportingEnabled-by-default.patch
Patch5: 0005-Enable-sosreport.patch
Patch6: 0006-post_report-always-exit-silenty.patch
Patch7: 0007-collect-installed-RPM-details-in-sosreport.patch
#Patch8: 0008-use-elfutils-stack-unwinder.patch
Patch9: 0009-fix-a-double-free-error-in-abrt-applet.patch
Patch10: 0010-vmcore-properly-configure-Augeas.patch
Patch11: 0011-applet-don-t-notify-missing-ignored_problems-file.patch
Patch12: 0012-configui-show-Close-button-in-the-dialog.patch
Patch13: 0013-applet-do-not-say-the-report-is-anonymous-when-urepo.patch
#Patch14: 0014-spec-abrt-cli-requires-a-pkg-providing-workflows.patch
#Patch15: 0015-testsuite-encourage-users-to-create-a-case-in-RHTS.patch
Patch16: 0016-cli-list-show-a-hint-about-creating-a-case-in-RHTS.patch
Patch17: 0017-harvest-vmcore-properly-handle-inaccessible-dir-erro.patch
Patch18: 0018-don-t-break-the-event-run-by-failures-of-abrt-action.patch
Patch19: 0019-Fix-handling-of-Machine-Check-Exceptions.patch
Patch20: 0020-move-MCE-handling-in-event-to-abrt-action-check-oops.patch
Patch21: 0021-abrt-action-check-oops-for-hw-error-i18n-add-error-c.patch
Patch22: 0022-Add-a-manpage-for-abrt-action-check-oops-for-hw-erro.patch
Patch23: 0023-oops-post-create-do-not-fail-the-event-if-check-oops.patch
Patch24: 0024-doc-MCE_readme.txt-new-file-documentation-about-MCE-.patch
Patch25: 0025-examples-mce2.test-an-example-of-non-fatal-MCE.patch
Patch26: 0026-MCE-cover-cases-where-kernel-version-isn-t-detected-.patch
Patch27: 0027-MCE-make-oops-and-vmcore-MCEs-a-bit-more-similar.patch
Patch28: 0028-python-install-modules-to-sitearch-directory.patch
#Patch29: 0029-spec-abrt-python-s-files-to-arch-specific-dir.patch
Patch30: 0030-retrace-client-stop-failing-on-SSL2.patch
#Patch31: 0031-add-transifex-configuration-for-RHEL7.patch
#Patch32: 0032-correct-rhel7-tx-configuration.patch
Patch33: 0033-upload-watch-remove-busy-wait-for-SIGUSR1.patch
Patch34: 0034-turn-off-Autoreporting.patch
#Patch35: 0035-make-dist-use-tar-ustar-due-to-long-filenames.patch
Patch36: 0036-never-search-for-MCE-strings-in-dmesg.patch
Patch37: 0037-sos-capture-all-necessary-data.patch
Patch38: 0038-stop-sending-ureports-from-abrt-applet.patch
Patch39: 0039-ccpp-run-vulnerability-analysis-in-analyze_LocalGDB.patch
Patch40: 0040-Translation-updates.patch
Patch41: 0041-Translation-updates.patch
Patch42: 0042-vmcore-start-the-service-after-kdump-service.patch
Patch43: 0043-configu-UI-use-glade-file-extension-instead-of-ui.patch
Patch44: 0044-localization-fixes.patch
Patch45: 0045-gdb-disable-loading-of-auto-loaded-files.patch
#Patch46: 0046-spec-add-dependency-on-abrt-python.patch
#Patch47: 0047-spec-add-missing-requires-for-python-api.patch
#Patch48: 0048-spec-remove-stray-space-from-description.patch
Patch49: 0049-koops-add-an-option-controlling-MCE-detection.patch
#Patch50: 0050-spec-hook-Kernel-oops-configuration-files.patch
Patch51: 0051-python-support-exceptions-without-traceback.patch
#Patch52: 0052-spec-don-t-use-native-unwinder-on-arm-arch.patch
Patch53: 0053-gettext-fix-the-initialization-in-python-scripts.patch
Patch54: 0054-oops-add-man-page.patch
#Patch55: 0055-spec-hook-abrt-oops.conf.5.patch
Patch56: 0056-cli-make-consistent-commands-in-abrt-cli.patch
#Patch57: 0057-spec-remove-dependency-on-crash-from-abrt-addon-vmco.patch
Patch58: 0058-cli-robustize-abrt-console-notification.sh.patch
Patch59: 0059-plugins-add-abrt-action-generate-machine-id.patch
#Patch60: 0060-spec-add-abrt-action-generate-machine-id.patch
Patch61: 0061-dbus-fixed-abrt-dbus-memory-leaks.patch
Patch62: 0062-applet-chown-each-notified-problem-before-reporting-.patch
Patch63: 0063-cli-add-option-remove-crash-dirs-after-reporting.patch
Patch64: 0064-applet-confirm-ignoring-of-notifications.patch
Patch65: 0065-cli-batch-reporting-in-abrt-cli.patch
Patch66: 0066-Translation-updates.patch
Patch67: 0067-koops-don-t-analyze-MCEs-like-standard-oopses.patch
Patch68: 0068-ureport-attach-contact-email-if-configured.patch
Patch69: 0069-console-notifications-use-return-instead-of-exit.patch
Patch70: 0070-applet-don-t-show-duphash-instead-of-component.patch
Patch71: 0071-console-notifications-skip-non-interactive-shells.patch
Patch72: 0072-applet-ensure-writable-dump-directory-before-reporti.patch
Patch73: 0073-a-a-g-machine-id-add-systemd-s-machine-id.patch
Patch74: 0074-a-a-g-machine-id-suppress-its-failures-in-abrt_event.patch
Patch75: 0075-Translation-updates.patch
Patch76: 0076-Revert-gdb-disable-loading-of-auto-loaded-files.patch
Patch77: 0077-gdb-make-gdb-aware-of-the-abrt-s-debuginfo-dir.patch
#Patch78: 0078-spec-update-the-required-gdb-version.patch
Patch79: 0079-cli-mark-the-suggestion-text-for-translation.patch
Patch80: 0080-auto-reporting-add-options-to-specify-auth-type.patch
#Patch81: 0081-testsuite-abrt-auto-reporting-uReport-authentication.patch
Patch82: 0082-translations-pull-the-newest-PO-files.patch
#Patch83: 0083-translations-move-from-transifex-to-zanata.patch
#Patch84: 0084-spec-add-missing-augeas-dependency.patch
#Patch85: 0085-zanata-add-gettext-mappings.patch
Patch86: 0086-translations-update-the-PO-files.patch
Patch87: 0087-abrt-auto-reporting-make-the-code-more-safer.patch
# git format-patch 2.1.11-19.el7 -N --start-number 88 --topo-order
Patch88: 0088-a-a-save-package-data-turn-off-reading-data-from-roo.patch
Patch89: 0089-ccpp-fix-symlink-race-conditions.patch
Patch90: 0090-ccpp-stop-reading-hs_error.log-from-tmp.patch
Patch91: 0091-ccpp-do-not-read-data-from-root-directories.patch
Patch92: 0092-ccpp-open-file-for-dump_fd_info-with-O_EXCL.patch
Patch93: 0093-ccpp-postpone-changing-ownership-of-new-dump-directo.patch
Patch94: 0094-ccpp-create-dump-directory-without-parents.patch
Patch95: 0095-ccpp-do-not-override-existing-files-by-compat-cores.patch
Patch96: 0096-ccpp-do-not-use-value-of-proc-PID-cwd-for-chdir.patch
Patch97: 0097-ccpp-harden-dealing-with-UID-GID.patch
Patch98: 0098-ccpp-check-for-overflow-in-abrt-coredump-path-creati.patch
Patch99: 0099-ccpp-emulate-selinux-for-creation-of-compat-cores.patch
Patch100: 0100-make-the-dump-directories-owned-by-root-by-default.patch
Patch101: 0101-configure-move-the-default-dump-location-to-var-spoo.patch
#Patch102: 0102-spec-create-vat-spool-abrt.patch
Patch103: 0103-ccpp-avoid-overriding-system-files-by-coredump.patch
#Patch104: 0104-spec-add-libselinux-devel-to-BRs.patch
Patch105: 0105-daemon-use-libreport-s-function-checking-file-name.patch
Patch106: 0106-lib-add-functions-validating-dump-dir.patch
Patch107: 0107-dbus-process-only-valid-sub-directories-of-the-dump-.patch
Patch108: 0108-dbus-avoid-race-conditions-in-tests-for-dum-dir-avai.patch
Patch109: 0109-dbus-report-invalid-element-names.patch
Patch110: 0110-a-a-i-d-t-a-cache-sanitize-arguments.patch
Patch111: 0111-a-a-i-d-t-a-cache-sanitize-umask.patch
Patch112: 0112-ccpp-revert-the-UID-GID-changes-if-user-core-fails.patch
Patch113: 0113-upload-validate-and-sanitize-uploaded-dump-directori.patch
Patch114: 0114-daemon-harden-against-race-conditions-in-DELETE.patch
Patch115: 0115-daemon-allow-only-root-user-to-trigger-the-post-crea.patch
Patch116: 0116-daemon-dbus-allow-only-root-to-create-CCpp-Koops-vmc.patch
# Temporary RHEL-7.1.z patch #1219464
#Patch117: 0117-dumpers-avoid-AVC-when-creating-dump-directories.patch
# git format-patch 2.1.11-20.el7 -N --start-number 118 --topo-order
Patch118: 0118-dbus-validate-parameters-of-all-calls.patch
# git format-patch 2.1.11-21.el7 -N --start-number 119 --topo-order
Patch119: 0119-ccpp-do-not-unlink-failed-and-big-user-cores.patch
Patch120: 0120-a-a-i-d-t-a-cache-don-t-open-the-build_ids-file-as-a.patch
Patch121: 0121-a-a-i-d-t-a-cache-fix-command-line-argument-generati.patch
# git format-patch 2.1.11-22.el7 -N --start-number 122 --topo-order
Patch122: 0122-Do-not-use-bool-in-OPT_BOOL-macro-it-expects-int.patch
Patch123: 0123-abrt-auto-reporting-require-rhtsupport.conf-file-onl.patch
#Patch124: 0124-spec-add-AUTHENTICATED_AUTOREPORTING-conditional.patch
#Patch125: 0125-spec-abrt-requires-libreport-plugin-rhtsupport-on-rh.patch
Patch126: 0126-doc-fix-in-Makefile.patch
Patch127: 0127-sosreport-add-processor-information-to-sosreport.patch
Patch128: 0128-dbus-add-a-new-method-GetProblemData.patch
Patch129: 0129-libabrt-add-new-function-fetching-full-problem-data-.patch
Patch130: 0130-dbus-add-new-method-to-test-existence-of-an-element.patch
Patch131: 0131-libabrt-add-wrappers-TestElemeExists-and-GetInfo-for.patch
Patch132: 0132-cli-use-the-DBus-methods-for-getting-problem-informa.patch
Patch133: 0133-cli-status-don-t-return-0-if-there-is-a-problem-olde.patch
Patch134: 0134-cli-do-not-exit-with-segfault-if-dbus-fails.patch
Patch135: 0135-cli-chown-before-reporting.patch
Patch136: 0136-cli-exit-with-the-number-of-unreported-problems.patch
Patch137: 0137-cli-remove-dead-code.patch
Patch138: 0138-doc-update-abrt-cli-man-page.patch
Patch139: 0139-cli-enable-polkit-authentication-on-command-line.patch
Patch140: 0140-dbus-keep-the-polkit-authorization-for-all-clients.patch
Patch141: 0141-cli-get-list-of-possible-workflows-for-problem_data_.patch
Patch142: 0142-cli-warn-users-about-Private-Reports.patch
Patch143: 0143-cli-enable-authetication-for-all-commands.patch
Patch144: 0144-cli-do-not-notify-root-about-Private-Reports.patch
Patch145: 0145-cli-remove-useless-code-from-print_crash.patch
Patch146: 0146-cli-use-internal-command-impl-in-the-command-process.patch
# git format-patch 2.1.11-23.el7 -N --start-number 147 --topo-order
Patch147: 0147-abrt-hook-ccpp-minor-refactoring.patch
Patch148: 0148-Create-core-backtrace-in-unwind-hook.patch
Patch149: 0149-abrt-install-ccpp-hook-check-configuration.patch
#Patch150: 0150-spec-enable-dump-time-unwind-by-default.patch
Patch151: 0151-disable-CreateCoreBacktrace-by-default.patch
# git format-patch 2.1.11-24.el7 -N --start-number 152 --topo-order
Patch152: 0152-abrt-hook-ccpp-save-core_backtrace-from-hook.patch
# git format-patch 2.1.11-25.el7 -N --start-number 153 --topo-order
Patch153: 0153-abrt-hook-ccpp-reset-ownership-after-saving-core-bac.patch
# git format-patch 2.1.11-26.el7 -N --start-number 154 --topo-order
Patch154: 0154-abrt-merge-pstoreoops-merge-files-in-descending-orde.patch
Patch155: 0155-abrt-auto-reporting-fix-related-to-conditional-compi.patch
Patch156: 0156-Update-translations.patch
# git format-patch 2.1.11-27.el7 -N --start-number 157 --topo-order
Patch157: 0157-Fix-missing-newline-in-po-fr.po.patch
Patch158: 0158-doc-fix-related-to-conditional-compilation-of-man-pa.patch
#Patch159: 0159-spec-add-dbus-dependency-for-abrt-cli-and-abrt-pytho.patch
# git format-patch 2.1.11-28.el7 -N --start-number 160 --topo-order
Patch160: 0160-dbus-api-unify-reporting-of-errors.patch
Patch161: 0161-cli-fix-testing-of-DBus-API-return-codes.patch
Patch162: 0162-ccpp-fix-comment-related-to-MakeCompatCore-option-in.patch
Patch163: 0163-ccpp-use-global-TID.patch
# git format-patch 2.1.11-29.el7 -N --start-number 164 --topo-order
Patch164: 0164-Warn-against-disabling-private-reports-in-abrt.conf.patch
# git format-patch 2.1.11-30.el7 -N --start-number 165 --topo-order
Patch165: 0165-Only-analyze-vulnerabilities-when-coredump-present.patch
# git format-patch 2.1.11-31.el7 -N --start-number 166 --topo-order
Patch166: 0166-UUID-from-core-backtrace-if-coredump-is-missing.patch
# git format-patch 2.1.11-32.el7 -N --start-number 167 --topo-order
Patch167: 0167-ccpp-correct-comments-mentioning-TID.patch
Patch168: 0168-ccpp-Use-Global-PID.patch
Patch169: 0169-doc-add-example-into-the-abrt-auto-reporting-man-pag.patch
Patch170: 0170-abrt-auto-reporting-add-example-into-the-help.patch
# git format-patch 2.1.11-33.el7 -N --start-number 171 --topo-order
#Patch171: 0171-runtests-stick-to-new-BZ-password-rules.patch
#Patch172: 0172-testsuite-use-rpm-to-remove-packages.patch
#Patch173: 0173-testsuite-more-verbose-fail-in-get_crash_path.patch
#Patch174: 0174-testsuite-cli-sanity-comment-not-reportable-phase-ou.patch
#Patch175: 0175-testsuite-new-test-dumpdir_completedness.patch
#Patch176: 0176-testsuite-upload-handling-fix-irrelevant-AVCs.patch
Patch177: 0177-sos-use-services-instead-of-startup.patch
# git format-patch 2.1.11-34.el7 -N --start-number 178 --topo-order
Patch178: 0178-a-a-i-d-to-abrt-cache-make-own-random-temporary-dire.patch
Patch179: 0179-conf-introduce-DebugLevel.patch
Patch180: 0180-ccpp-ignore-crashes-of-ABRT-binaries-if-DebugLevel-0.patch
Patch181: 0181-ccpp-save-abrt-core-files-only-to-new-files.patch
Patch182: 0182-lib-add-convenient-wrappers-for-ensuring-writable-di.patch
Patch183: 0183-abrtd-switch-owner-of-the-dump-location-to-root.patch
#Patch184: 0184-spec-switch-owner-of-the-dump-location-to-root.patch
#Patch185: 0185-testsuite-ccpp-plugin-debug.patch
#Patch186: 0186-testsuite-a-a-i-debuginfo-the-set-uid-wrapper-uses-s.patch
#Patch187: 0187-testsuite-check-file-system-attributes-of-the-dump-l.patch
# git format-patch 2.1.11-35.el7 -N --start-number 188 --topo-order
#Patch188: 0188-testsuite-port-abrtd-directories-to-journald.patch
#Patch189: 0189-testsuite-ccpp-plugin-debug-fix-logs-bundling.patch
#Patch190: 0190-testsuite-ccpp-plugin-debug-normalize-ABRT_BINARY_CO.patch
#Patch191: 0191-testsuite-search-in-journal-logs-for-the-current-boo.patch
#Patch192: 0192-testsuite-add-test-for-reporter-upload-SSH-keys.patch
#Patch193: 0193-testsuite-add-test-for-reporter-upload-passwd-asking.patch
#Patch194: 0194-testsuite-test-abrt-hook-ccpp-selinux-awareness.patch
#Patch195: 0195-testsuite-abrtd-directories-normalize-ABRT_CONF_DUMP.patch
#Patch196: 0196-testsuite-rhts-test-fix-typo-and-URL-change-in-respo.patch
#Patch197: 0197-testsuite-event-configuration-add-missing-xml-files.patch
#Patch198: 0198-translations-update-zanata-configuration.patch
#Patch199: 0199-testsuite-add-ureport-attachments-test.patch
#Patch200: 0200-testsuite-reporter-upload-appending-results-to-repor.patch
#Patch201: 0201-testsuite-remove-ureport-attachments-from-aux.patch
#Patch202: 0202-testsuite-add-concurrent-processing-test-for-abrtd.patch
#Patch203: 0203-testsuite-reporter-upload-ssh-keys-fixes-to-work-on-.patch
#Patch204: 0204-testsuite-Bugzilla-private-bugs.patch
#Patch205: 0205-testsuite-reply-with-invalid-data-for-unexpected-que.patch
Patch206: 0206-augeas-augtool-save-files-etc-abrt-plugins-oops.conf.patch
Patch207: 0207-vmcore-catch-IOErrors-and-OSErrors.patch
#Patch208: 0208-testsuite-add-a-per-test-timeout-for-15m.patch
Patch209: 0209-lib-hooklib-make-signal_is_fatal-public.patch
Patch210: 0210-ccpp-add-IgnoredPath-option.patch
#Patch211: 0211-testsuite-add-test-for-abrt-hook-ccpp-IgnoredPath-op.patch
#Patch212: 0212-testsuite-add-test-for-AllowedUsers-and-AllowedGroup.patch
Patch213: 0213-ccpp-add-AllowedUsers-and-AllowedGroups-feature.patch
Patch214: 0214-Save-Vendor-and-GPG-Fingerprint.patch
#Patch215: 0215-testsuite-add-tests-for-pgk_vendor-and-pkg_fingerpri.patch
#Patch216: 0216-testsuite-add-rhtsupport-discourage-tests.patch
#Patch217: 0217-testsuite-reporter-rhtsupport-should-attach-whole-du.patch
#Patch218: 0218-testsuite-use-problem-report-API-to-create-descripti.patch
#Patch219: 0219-testsuite-test-for-reporter-mailx-email-formatting.patch
#Patch220: 0220-testsuite-mailx-does-not-create-dead.letter-in-failu.patch
Patch221: 0221-lib-prevent-from-creating-non-root-sub-dirs-in-dump-.patch
# git format-patch 2.1.11-36.el7 -N --start-number 222 --topo-order
Patch222: 0222-ccpp-exit-with-error-if-cannot-get-executable.patch
# git format-patch 2.1.11-37.el7 -N --start-number 223 --topo-order
Patch223: 0223-ccpp-add-xfunc_die-if-cannot-get-executable.patch
# git format-patch 2.1.11-38.el7 -N --start-number 224 --topo-order
#Patch224: 0224-testsuite-augeas-set-DropNotReportableOopses-test.patch
Patch225: 0225-vmcore-generate-reason-file-in-all-cases.patch
#Patch226: 0226-testsuite-fix-the-kernel-vmcore-harvest-test.patch
Patch227: 0227-console-notifications-add-timeout.patch
Patch228: 0228-Fix-memory-leaks-in-abrt-dbus.patch
Patch229: 0229-python-fix-check-for-absolute-path.patch
#Patch230: 0230-testsuite-add-test-for-RequireAbsolutePath-option.patch
# git format-patch 2.1.11-39.el7 -N --start-number 231 --topo-order
#Patch231: 0231-testsuite-add-test-which-tests-log-messages-of-ingor.patch
Patch232: 0232-ccpp-unify-log-message-of-ignored-crashes.patch
Patch233: 0233-abrt-hook-ccpp-save-get_fsuid-return-values-in-int-v.patch
# git format-patch 2.1.11-40.el7 -N --start-number 234 --topo-order
#Patch234: 0234-testsuite-fix-ccpp-plugin-debug-test.patch
#Patch235: 0235-testsuite-mailx-reporting-hardcode-locale-and-timezo.patch
#Patch236: 0236-testsuite-rhts-test-relax-a-grep-pattern-a-bit.patch
#Patch237: 0237-testsuite-mailx-reporting-force-creating-symlink.patch
Patch238: 0238-vmcore-fix-finding-partitions-by-UUID-and-LABEL.patch
#Patch239: 0239-spec-add-utils-linux-to-vmcore-s-Require.patch
Patch240: 0240-vmcore-use-findmnt-to-get-mountpoint.patch
# git format-patch 2.1.11-41.el7 -N --start-number 241 --topo-order
#Patch241: 0241-testsuite-do-not-exit-mailx-notify-event-with-1.patch
#Patch242: 0242-testsuite-add-prepare-to-cli-authentication-test.patch
#Patch243: 0243-testsuite-libreport-plugin-mantisbt-is-not-installed.patch
#Patch244: 0244-testsuite-use-crashing-binary-from-signed-package.patch
Patch245: 0245-daemon-trigger-dump-location-cleanup-after-detection.patch
Patch246: 0246-handle-event-stop-creating-post-create-lock.patch
# git format-patch 2.1.11-42.el7 -N --start-number 247 --topo-order
#Patch247: 0247-testsuite-check-fingerprint-only-if-a-kernel-is-sign.patch
#Patch248: 0248-testsuite-fix-reporter-upload-ssh-keys-test.patch
#Patch249: 0249-testsuite-ccpp-plugin-hook-ignoring-fix-typo.patch
Patch250: 0250-lib-check_recent_crash_file-do-not-produce-error_msg.patch
#Patch251: 0251-testsuite-do-not-die-if-crash-is-not-generated.patch
# git format-patch 2.1.11-43.el7 -N --start-number 252 --topo-order
#Patch252: 0252-testsuite-reporter-rhtsupport-no-longer-uses-checks-.patch
#Patch253: 0253-testsuite-puts-NULL-didn-t-cause-segfault-on-s390x.patch
Patch254: 0254-daemon-send-base-names-from-abrt-server-to-abrtd.patch
# git format-patch 2.1.11-44.el7 -N --start-number 255 --topo-order
#Patch255: 0255-testsuite-make-dumpdir_completedness-test-runnable-o.patch
Patch256: 0256-Translation-updates.patch
# git format-patch 2.1.11-45.el7 -N --start-number 257 --topo-order
#Patch257: 0257-testsuite-use-exported-gpg-keys-in-dumpdir_completed.patch
Patch258: 0258-lib-don-t-expect-kernel-s-version-2.6.-or-3.patch
Patch259: 0259-koops-do-not-assume-version-has-3-levels.patch
Patch260: 0260-xorg-rewrite-skip_pfx-function-to-work-with-journal-.patch
#Patch261: 0261-testsuite-add-tescase-for-a-dump-xorg.patch
Patch262: 0262-lib-stop-printing-out-a-debug-message-adding.patch
Patch263: 0263-cli-don-t-start-reporting-of-not-reportable-problems.patch
Patch264: 0264-cli-introduce-unsafe-reporting-for-not-reporable-pro.patch
Patch265: 0265-cli-configure-libreport-to-ignore-not-reportable.patch
Patch266: 0266-cli-print-out-the-not-reportable-reason.patch
#Patch267: 0267-testsuite-add-cli-process-test-case.patch
Patch268: 0268-vmcore-remove-not-implemented-option-AttemptHardlink.patch
# git format-patch 2.1.11-46.el7 -N --start-number 269 --topo-order
Patch269: 0269-ccpp-add-h-parameter-into-abrt-hook-ccpp.patch
#Patch270: 0270-testsuite-add-test-for-core-template-substitution.patch
# git format-patch 2.1.11-47.el7 -N --start-number 271 --topo-order
Patch271: 0271-Translation-updates.patch
# git format-patch 2.1.11-48.el7 -N --start-number 272 --topo-order
#Patch272: 0272-spec-allow-deprecated-declarations-warning.patch
#Patch273: 0273-spec-add-missing-dependecy-on-dbus-glib-devel.patch
Patch274: 0274-python-provide-more-information-about-exception.patch
#Patch275: 0275-testsuite-provide-more-information-about-exception.patch
Patch276: 0276-Translation-updates.patch
Patch277: 0277-Fix-pt_BR.po-translation.patch
Patch278: 0278-koops-add-suspicious-strings-blacklist.patch
#Patch279: 0279-testsuite-suspicious-strings-blacklist-test.patch
Patch280: 0280-koops-Improve-fatal-MCE-check-when-dumping-backtrace.patch
#Patch281: 0281-testsuite-add-test-for-dumping-kernel-panic-oom-oops.patch
Patch282: 0282-Add-oops-processing-for-kernel-panics-caused-by-hung.patch
Patch283: 0283-vmcore-remove-original-vmcore-file-in-the-last-step.patch
Patch284: 0284-vmcore-use-libreport-dd-API-in-the-harvestor.patch
#Patch285: 0285-testsuite-add-test-case-for-copyvmcore.patch
Patch286: 0286-koops-Improve-not-reportable-for-oopses-with-taint-f.patch
Patch287: 0287-a-a-ureport-add-check-if-crash-is-from-packaged-exec.patch
#Patch288: 0288-testsuite-test-not-sending-ureport-from-unpackaged-e.patch
#Patch289: 289-spec-update-URL-and-Source-to-recent-values.patch
#Patch290: 0290-Revert-testsuite-reporter-rhtsupport-no-longer-uses-.patch
#Patch291: 0291-testsuite-reporter-rhtsupport-parameter-t-extend-fun.patch
# git format-patch 2.1.11-49.el7 -N --start-number 292 --topo-order
#Patch292: 0292-testsuite-switch-order-of-g_crash_path-and-wait_f_h.patch
#Patch293: 0293-testsuite-wait-for-hooks-at-least-1-second.patch
#Patch294: 0294-testsuite-tell-the-runner-about-problem-sub-director.patch
#Patch295: 0295-CI-make-debugging-easier-with-more-log-messages.patch
#Patch296: 0296-testsuite-rhts-test-remove-trailing-characters.patch
#Patch297: 0297-testsuite-restart-abrt-ccpp-in-abrtd-directories.patch
#Patch298: 0298-testsuite-Install-missing-rpm-sign-package.patch
#Patch299: 0299-testsuite-Show-warning-instead-of-failing-test.patch
#Patch300: 0300-testsuite-check-for-correct-group-and-permissions.patch
#Patch301: 0301-testsuite-disable-failing-tests.patch
#Patch302: 0302-testsuite-extend-timeout-to-10-minutes.patch
#Patch303: 0303-testsuite-Correct-the-name-of-configuration-file.patch
#Patch304: 0304-tests-cli-sanity-re-enable-report-non-reportable-pha.patch
#Patch305: 0305-testsuite-fix-backtrace-verification-on-power.patch
Patch306: 0306-a-harvest-vmcore-fix-regresion.patch
# git format-patch 2.1.11-50.el7 -N --start-number 307 --topo-order
#Patch307: 0307-spec-use-dmidecode-instead-of-python-dmidecode.patch
Patch308: 0308-plugins-a-a-g-machine-id-use-dmidecode-command.patch
#Patch309: 0309-spec-turn-on-enable-native-unwinder-aarch64.patch
Patch310: 0310-a-a-s-p-data-fix-segfault-if-GPGKeysDir-isn-t-config.patch
# git format-patch 2.1.11-51.el7 -N --start-number 311 --topo-order
Patch311: 0311-plugin-general-from-sos-has-been-split-into-two-new-.patch
# git format-patch 2.1.11-52.el7 -N --start-number 312 --topo-order
Patch312: 0312-cli-load-config-file-at-the-beginning.patch
Patch313: 0313-ccpp-fast-dumping-and-abrt-core-limit.patch
Patch314: 0314-conf-increase-MaxCrashReportsSize-to-5GiB.patch
#Patch315: 0315-testsuite-abrt-core-dump-file-size-limits.patch
#Patch316: 0316-testsuite-the-prepare-fn-resets-socket-problem-timeo.patch
Patch317: 0317-Resolves-bz1647841.patch
Patch318: 0318-testsuite-move-examples-to-tests.patch
Patch319: 0319-koops-Filter-kernel-oopses-based-on-logged-hostname.patch
#Patch320: 0320-spec-add-hostname-BR-for-tests.patch
Patch321: 0321-daemon-Fix-double-closed-fd-race-condition.patch
Patch322: 0322-hooks-ccpp-Honor-CreateCoreBacktrace.patch
# git format-patch 2.1.11-53.el7 -N --start-number 323 --topo-order


# autogen.sh is need to regenerate all the Makefile files
Patch1006: 1000-Add-autogen.sh.patch
Patch1000: 1000-event-don-t-run-the-reporter-bugzilla-h-on-RHEL-and-.patch
#Patch1002: 1002-plugin-set-URL-to-retrace-server.patch
Patch1004: 1004-turn-sosreport-off.patch
Patch1005: 1005-cli-list-revert-patch-7966e5737e8d3af43b1ecdd6a82323.patch


# git is need for '%%autosetup -S git' which automatically applies all the
# patches above. Please, be aware that the patches must be generated
# by 'git format-patch'
BuildRequires: git

BuildRequires: dbus-devel
BuildRequires: hostname
BuildRequires: gtk3-devel
BuildRequires: rpm-devel >= 4.6
BuildRequires: desktop-file-utils
BuildRequires: libnotify-devel
BuildRequires: dbus-glib-devel
#why? BuildRequires: file-devel
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: nss-devel
BuildRequires: asciidoc
BuildRequires: doxygen
BuildRequires: xmlto
BuildRequires: libreport-devel >= %{libreport_ver}
BuildRequires: satyr-devel >= %{satyr_ver}
BuildRequires: systemd-python
BuildRequires: augeas
BuildRequires: libselinux-devel
Requires: abrt-python = %{version}-%{release}
Requires: libreport >= %{libreport_ver}
Requires: satyr >= %{satyr_ver}
Requires: sos >= 3.6

%if %{with systemd}
Requires: systemd-units
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-python = %{version}-%{release}
Requires(pre): shadow-utils
Requires: python-augeas
Requires: python-dbus
%ifarch aarch64 i686 x86_64
Requires: dmidecode
%endif
Requires: libreport-plugin-ureport >= %{libreport_ver}
#%if 0%{?rhel}
#Requires: libreport-plugin-rhtsupport
#%endif

# we used to have abrt-plugin-bodhi, but we have removed it
# and we want allow users to update abrt without necessity to
# to remove the obsoleted package:
Obsoletes: abrt-plugin-bodhi < 2.1.7-7

%description
%{name} is a tool to help users to detect defects in applications and
to create a bug report with all information needed by maintainer to fix it.
It uses plugin system to extend its functionality.

%package libs
Summary: Libraries for %{name}
Group: System Environment/Libraries

%description libs
Libraries for %{name}.

%package devel
Summary: Development libraries for %{name}
Group: Development/Libraries
Requires: abrt-libs = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%package gui-libs
Summary: Libraries for %{name}-gui
Group: System Environment/Libraries

%description gui-libs
Libraries for %{name}-gui.

%package gui-devel
Summary: Development libraries for %{name}-gui
Group: Development/Libraries
Requires: abrt-gui-libs = %{version}-%{release}

%description gui-devel
Development libraries and headers for %{name}-gui.

%package gui
Summary: %{name}'s gui
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: %{name}-dbus = %{version}-%{release}
Requires: gnome-abrt
BuildRequires: libreport-gtk-devel >= %{libreport_ver}
BuildRequires: libICE-devel
BuildRequires: libSM-devel
# we used to have abrt-applet, now abrt-gui includes it:
Provides: abrt-applet = %{version}-%{release}
Obsoletes: abrt-applet < 0.0.5
Conflicts: abrt-applet < 0.0.5
Requires: abrt-libs = %{version}-%{release}
Requires: abrt-gui-libs = %{version}-%{release}

%description gui
GTK+ wizard for convenient bug reporting.

%package addon-ccpp
Summary: %{name}'s C/C++ addon
Group: System Environment/Libraries
Requires: cpio
Requires: gdb >= 7.6.1-63
Requires: elfutils
# abrt-action-perform-ccpp-analysis wants to run analyze_RetraceServer:
Requires: %{name}-retrace-client
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}
Requires: libreport-python

%description addon-ccpp
This package contains hook for C/C++ crashed programs and %{name}'s C/C++
analyzer plugin.

%package addon-upload-watch
Summary: %{name}'s upload addon
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}

%description addon-upload-watch
This package contains hook for uploaded problems.

%package retrace-client
Summary: %{name}'s retrace client
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: xz
Requires: tar

%description retrace-client
This package contains the client application for Retrace server
which is able to analyze C/C++ crashes remotely.

%package addon-kerneloops
Summary: %{name}'s kerneloops addon
Group: System Environment/Libraries
Requires: curl
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}
%if 0%{!?rhel:1}
Requires: libreport-plugin-kerneloops >= %{libreport_ver}
%endif

%description addon-kerneloops
This package contains plugin for collecting kernel crash information from
system log.

%package addon-xorg
Summary: %{name}'s Xorg addon
Group: System Environment/Libraries
Requires: curl
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description addon-xorg
This package contains plugin for collecting Xorg crash information from Xorg
log.

%package addon-vmcore
Summary: %{name}'s vmcore addon
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops
Requires: kexec-tools
Requires: abrt-python = %{version}-%{release}
Requires: python-augeas
Requires: util-linux

%description addon-vmcore
This package contains plugin for collecting kernel crash information from
vmcore files.

%package addon-pstoreoops
Summary: %{name}'s pstore oops addon
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}
Requires: abrt-addon-kerneloops
Obsoletes: abrt-addon-uefioops < 2.1.7

%description addon-pstoreoops
This package contains plugin for collecting kernel oopses from pstore storage.

%package addon-python
Summary: %{name}'s addon for catching and analyzing Python exceptions
Group: System Environment/Libraries
Requires: python
Requires: %{name} = %{version}-%{release}
Requires: systemd-python
Requires: abrt-python

%description addon-python
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%package tui
Summary: %{name}'s command line interface
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: libreport-cli >= %{libreport_ver}
Requires: abrt-libs = %{version}-%{release}
Requires: %{name}-dbus = %{version}-%{release}

%description tui
This package contains a simple command line client for processing abrt reports
in command line environment.

%package cli
Summary: Virtual package to make easy default installation on non-graphical environments
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: abrt-tui
Requires: abrt-addon-kerneloops
Requires: abrt-addon-pstoreoops
Requires: abrt-addon-vmcore
Requires: abrt-addon-ccpp
Requires: abrt-addon-python
Requires: abrt-addon-xorg
%if 0%{?rhel}
#%if 0%{?centos_ver}
#Requires: libreport-centos >= %{libreport_ver}
#Requires: libreport-plugin-mantisbt >= %{libreport_ver}
#%else
#Requires: libreport-rhel >= %{libreport_ver}
#Requires: libreport-plugin-rhtsupport >= %{libreport_ver}
#%endif
#%else
Requires: abrt-retrace-client
Requires: libreport-plugin-bugzilla >= %{libreport_ver}
Requires: libreport-plugin-logger >= %{libreport_ver}
Requires: libreport-plugin-ureport >= %{libreport_ver}
%endif

%description cli
Virtual package to install all necessary packages for usage from command line
environment.

%package desktop
Summary: Virtual package to make easy default installation on desktop environments
Group: User Interface/Desktops
# This package gets installed when anything requests bug-buddy -
# happens when users upgrade Fn to Fn+1;
# or if user just wants "typical desktop installation".
# Installing abrt-desktop should result in the abrt which works without
# any tweaking in abrt.conf (IOW: all plugins mentioned there must be installed)
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops
Requires: abrt-addon-pstoreoops
Requires: abrt-addon-vmcore
Requires: abrt-addon-ccpp
Requires: abrt-addon-python
Requires: abrt-addon-xorg
# Default config of addon-ccpp requires gdb
Requires: gdb >= 7.6.1-63
Requires: elfutils
Requires: abrt-gui
Requires: gnome-abrt
%if 0%{?rhel}
#%if 0%{?centos_ver}
#Requires: libreport-centos >= %{libreport_ver}
#Requires: libreport-plugin-mantisbt >= %{libreport_ver}
#%else
#Requires: libreport-rhel >= %{libreport_ver}
#Requires: libreport-plugin-rhtsupport >= %{libreport_ver}
#%endif
#%else
Requires: abrt-retrace-client
Requires: libreport-plugin-bugzilla >= %{libreport_ver}
Requires: libreport-plugin-logger >= %{libreport_ver}
Requires: libreport-plugin-ureport >= %{libreport_ver}
#Requires: libreport-fedora >= %{libreport_ver}
%endif
#Requires: abrt-plugin-firefox
Provides: bug-buddy = 2.28.0

%description desktop
Virtual package to install all necessary packages for usage from desktop
environment.

%package dbus
Summary: ABRT DBus service
Group: Applications/System
Requires: %{name} = %{version}-%{release}
BuildRequires: polkit-devel
Requires: abrt-libs = %{version}-%{release}

%description dbus
ABRT DBus service which provides org.freedesktop.problems API on dbus and
uses PolicyKit to authorize to access the problem data.


%package python
Summary: ABRT Python API
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-dbus = %{version}-%{release}
Requires: pygobject2
Requires: dbus-python
Requires: libreport-python
BuildRequires: python-nose
BuildRequires: python-sphinx

%description python
High-level API for querying, creating and manipulating
problems handled by ABRT in Python.

%package python-doc
Summary: ABRT Python API Documentation
Group: Documentation
BuildArch: noarch
BuildRequires: python2-devel
Requires: %{name} = %{version}-%{release}
Requires: %{name}-python = %{version}-%{release}

%description python-doc
Examples and documentation for ABRT Python API.

%package console-notification
Summary: ABRT console notification script
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}

%description console-notification
A small script which prints a count of detected problems when someone logs in
to the shell

%prep
# http://www.rpm.org/wiki/PackagerDocs/Autosetup
# Default '__scm_apply_git' is 'git apply && git commit' but this workflow
# doesn't allow us to create a new file within a patch, so we have to use
# 'git am' (see /usr/lib/rpm/macros for more details)
%define __scm_apply_git(qp:m:) %{__git} am
%autosetup -S git

%build
./autogen.sh
autoconf
# -Wno-error=deprecated-declarations because there are some warning about
# deprecated gtk3 functions because of gtk3 rebase
CFLAGS="%{optflags} -Werror -Wno-error=deprecated-declarations" %configure --enable-doxygen-docs \
        --disable-silent-rules \
        --without-bodhi \
%ifnarch %{arm}
        --enable-native-unwinder \
%endif
        --enable-dump-time-unwind \
        --enable-suggest-autoreporting
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} \
             dbusabrtdocdir=%{_defaultdocdir}/%{name}-dbus-%{version}/html/ \
             example_pythondir=%{_defaultdocdir}/%{name}-python-%{version}/examples

%find_lang %{name}

# remove all .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p ${RPM_BUILD_ROOT}/%{_initrddir}
mkdir -p $RPM_BUILD_ROOT/var/cache/abrt-di
mkdir -p $RPM_BUILD_ROOT/var/run/abrt
mkdir -p $RPM_BUILD_ROOT/var/spool/abrt
mkdir -p $RPM_BUILD_ROOT/var/spool/abrt-upload

desktop-file-install \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
        src/applet/abrt-applet.desktop

ln -sf %{_datadir}/applications/abrt-applet.desktop ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart/

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check || {
    # find and print the logs of failed test
    # do not cat tests/testsuite.log because it contains a lot of bloat
    find tests/testsuite.dir -name "testsuite.log" -print -exec cat '{}' \;
    exit 1
}

%pre
#uidgid pair 173:173 reserved in setup rhbz#670231
%define abrt_gid_uid 173
getent group abrt >/dev/null || groupadd -f -g %{abrt_gid_uid} --system abrt
getent passwd abrt >/dev/null || useradd --system -g abrt -u %{abrt_gid_uid} -d /etc/abrt -s /sbin/nologin abrt

OLD_LOCATION="/var/tmp/abrt"
# $1 == 1 if install; 2 if upgrade
if [ "$1" -eq 2 ]
then
    test -d "$OLD_LOCATION" || exit 0

    # remove old dump directories
    for DD in `find "$OLD_LOCATION" -maxdepth 1 -type d`
    do
        # in order to not remove user stuff remove only directories containing 'time' file
        if [ -f "$DD/time" ]; then
            rm -rf $DD
        fi
    done
fi

# doesn't mather if it fails or not for any reason
if which restorecon 1>/dev/null 2>&1; then
    restorecon -R "$NEW_LOCATION" 1>/dev/null 2>&1 || true
fi
exit 0

%post
# $1 == 1 if install; 2 if upgrade
%systemd_post abrtd.service

%post addon-ccpp
# this is required for transition from 1.1.x to 2.x
# because /cache/abrt-di/* was created under root with root:root
# so 2.x fails when it tries to extract debuginfo there..
chown -R abrt:abrt %{_localstatedir}/cache/abrt-di
%systemd_post abrt-ccpp.service

%post addon-kerneloops
%systemd_post abrt-oops.service

%post addon-xorg
%systemd_post abrt-xorg.service

%post addon-vmcore
%systemd_post abrt-vmcore.service

%post addon-pstoreoops
%systemd_post abrt-pstoreoops.service

%post addon-upload-watch
%systemd_post abrt-upload-watch.service

%preun
%systemd_preun abrtd.service

%preun addon-ccpp
%systemd_preun abrt-ccpp.service

%preun addon-kerneloops
%systemd_preun abrt-oops.service

%preun addon-xorg
%systemd_preun abrt-xorg.service

%preun addon-vmcore
%systemd_preun abrt-vmcore.service

%preun addon-pstoreoops
%systemd_preun abrt-pstoreoops.service

%preun addon-upload-watch
%systemd_preun abrt-upload-watch.service

%postun
%systemd_postun_with_restart abrtd.service

%postun addon-ccpp
%systemd_postun_with_restart abrt-ccpp.service

%postun addon-kerneloops
%systemd_postun_with_restart abrt-oops.service

%postun addon-xorg
%systemd_postun_with_restart abrt-xorg.service

%postun addon-vmcore
%systemd_postun_with_restart abrt-vmcore.service

%postun addon-pstoreoops
%systemd_postun_with_restart abrt-pstoreoops.service

%postun addon-upload-watch
%systemd_postun_with_restart abrt-upload-watch.service

%post gui
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post gui-libs -p /sbin/ldconfig

%postun gui-libs -p /sbin/ldconfig

%postun gui
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
service abrtd condrestart >/dev/null 2>&1 || :

%posttrans addon-ccpp
service abrt-ccpp condrestart >/dev/null 2>&1 || :

%posttrans addon-kerneloops
service abrt-oops condrestart >/dev/null 2>&1 || :

%posttrans addon-xorg
service abrt-xorg condrestart >/dev/null 2>&1 || :

%posttrans addon-vmcore
service abrt-vmcore condrestart >/dev/null 2>&1 || :
# Copy the configuration file to plugin's directory
test -f /etc/abrt/abrt-harvest-vmcore.conf && {
    mv -b /etc/abrt/abrt-harvest-vmcore.conf /etc/abrt/plugins/vmcore.conf
}
exit 0

%posttrans addon-pstoreoops
service abrt-pstoreoops condrestart >/dev/null 2>&1 || :

%posttrans addon-upload-watch
service abrt-upload-watch condrestart >/dev/null 2>&1 || :

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%if %{with systemd}
%{_unitdir}/abrtd.service
%{_tmpfilesdir}/abrt.conf
%else
%{_initrddir}/abrtd
%endif
%{_sbindir}/abrtd
%{_sbindir}/abrt-server
%{_sbindir}/abrt-auto-reporting
%{_libexecdir}/abrt-handle-event
%{_libexecdir}/abrt-action-ureport
%{_libexecdir}/abrt-action-generate-machine-id
%{_bindir}/abrt-handle-upload
%{_bindir}/abrt-action-notify
%{_bindir}/abrt-action-save-package-data
%{_bindir}/abrt-watch-log
%{_bindir}/abrt-action-analyze-xorg
%config(noreplace) %{_sysconfdir}/%{name}/abrt.conf
%{_datadir}/%{name}/conf.d/abrt.conf
%config(noreplace) %{_sysconfdir}/%{name}/abrt-action-save-package-data.conf
%{_datadir}/%{name}/conf.d/abrt-action-save-package-data.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/xorg.conf
%{_datadir}/%{name}/conf.d/plugins/xorg.conf
%{_mandir}/man5/abrt-xorg.conf.5.gz
%config(noreplace) %{_sysconfdir}/%{name}/gpg_keys.conf
%{_datadir}/%{name}/conf.d/gpg_keys.conf
%{_mandir}/man5/gpg_keys.conf.5.gz
%config(noreplace) %{_sysconfdir}/libreport/events.d/abrt_event.conf
%{_mandir}/man5/abrt_event.conf.5.gz
%config(noreplace) %{_sysconfdir}/libreport/events.d/smart_event.conf
%{_mandir}/man5/smart_event.conf.5.gz
%dir %attr(0751, root, abrt) %{_localstatedir}/spool/%{name}
%dir %attr(0700, abrt, abrt) %{_localstatedir}/spool/%{name}-upload
# abrtd runs as root
%dir %attr(0755, root, root) %{_localstatedir}/run/%{name}
%ghost %attr(0666, -, -) %{_localstatedir}/run/%{name}/abrt.socket
%ghost %attr(0644, -, -) %{_localstatedir}/run/%{name}/abrtd.pid

%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/conf.d
%dir %{_datadir}/%{name}/conf.d/plugins
%{_mandir}/man1/abrt-handle-upload.1.gz
%{_mandir}/man1/abrt-server.1.gz
%{_mandir}/man1/abrt-action-save-package-data.1.gz
%{_mandir}/man1/abrt-watch-log.1.gz
%{_mandir}/man1/abrt-action-analyze-xorg.1.gz
%{_mandir}/man1/abrt-action-notify.1.gz
%{_mandir}/man1/abrt-auto-reporting.1.gz
%{_mandir}/man8/abrtd.8.gz
%{_mandir}/man5/abrt.conf.5.gz
%{_mandir}/man5/abrt-action-save-package-data.conf.5.gz
# {_mandir}/man5/pyhook.conf.5.gz

# filesystem package should own /usr/share/augeas/lenses directory
%{_datadir}/augeas/lenses/abrt.aug

%files libs
%defattr(-,root,root,-)
%{_libdir}/libabrt.so.*

%files devel
%defattr(-,root,root,-)
# The complex pattern below (instead of simlpy *) excludes Makefile{.am,.in}:
%doc apidoc/html/*.{html,png,css,js}
%{_includedir}/abrt/abrt-dbus.h
%{_includedir}/abrt/hooklib.h
%{_includedir}/abrt/libabrt.h
%{_includedir}/abrt/problem_api.h
%{_libdir}/libabrt.so
%{_libdir}/pkgconfig/abrt.pc

%files gui-libs
%defattr(-,root,root,-)
%{_libdir}/libabrt_gui.so.*

%files gui-devel
%defattr(-,root,root,-)
%{_includedir}/abrt/abrt-config-widget.h
%{_includedir}/abrt/system-config-abrt.h
%{_libdir}/libabrt_gui.so
%{_libdir}/pkgconfig/abrt_gui.pc

%files gui
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
# all glade, gtkbuilder and py files for gui
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/status/*
%{_datadir}/%{name}/icons/hicolor/*/status/*
%{_datadir}/%{name}/ui/*
%{_bindir}/abrt-applet
%{_bindir}/system-config-abrt
#%%{_bindir}/test-report
%{_datadir}/applications/abrt-applet.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/abrt-applet.desktop
%{_mandir}/man1/abrt-applet.1*
%{_mandir}/man1/system-config-abrt.1*

%files addon-ccpp
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp.conf
%{_datadir}/%{name}/conf.d/plugins/CCpp.conf
%{_mandir}/man5/abrt-CCpp.conf.5.gz
%dir %attr(0775, abrt, abrt) %{_localstatedir}/cache/abrt-di
%if %{with systemd}
%{_unitdir}/abrt-ccpp.service
%else
%{_initrddir}/abrt-ccpp
%endif
%{_libexecdir}/abrt-hook-ccpp
%{_libexecdir}/abrt-gdb-exploitable
%attr(6755, abrt, abrt) %{_libexecdir}/abrt-action-install-debuginfo-to-abrt-cache
%{_bindir}/abrt-action-analyze-c
%{_bindir}/abrt-action-trim-files
%{_bindir}/abrt-action-analyze-core
%{_bindir}/abrt-action-analyze-vulnerability
%{_bindir}/abrt-action-install-debuginfo
%{_bindir}/abrt-action-generate-backtrace
%{_bindir}/abrt-action-generate-core-backtrace
%{_bindir}/abrt-action-analyze-backtrace
%{_bindir}/abrt-action-list-dsos
%{_bindir}/abrt-action-perform-ccpp-analysis
%{_bindir}/abrt-action-analyze-ccpp-local
%{_sbindir}/abrt-install-ccpp-hook
%config(noreplace) %{_sysconfdir}/libreport/events.d/ccpp_event.conf
%{_mandir}/man5/ccpp_event.conf.5.gz
%config(noreplace) %{_sysconfdir}/libreport/events.d/gconf_event.conf
%{_mandir}/man5/gconf_event.conf.5.gz
%config(noreplace) %{_sysconfdir}/libreport/events.d/vimrc_event.conf
%{_mandir}/man5/vimrc_event.conf.5.gz
%{_datadir}/libreport/events/analyze_CCpp.xml
%{_datadir}/libreport/events/analyze_LocalGDB.xml
%{_datadir}/libreport/events/collect_xsession_errors.xml
%{_datadir}/libreport/events/collect_GConf.xml
%{_datadir}/libreport/events/collect_vimrc_user.xml
%{_datadir}/libreport/events/collect_vimrc_system.xml
%{_datadir}/libreport/events/post_report.xml
%{_mandir}/man*/abrt-action-analyze-c.*
%{_mandir}/man*/abrt-action-trim-files.*
%{_mandir}/man*/abrt-action-generate-backtrace.*
%{_mandir}/man*/abrt-action-generate-core-backtrace.*
%{_mandir}/man*/abrt-action-analyze-backtrace.*
%{_mandir}/man*/abrt-action-list-dsos.*
%{_mandir}/man*/abrt-install-ccpp-hook.*
%{_mandir}/man*/abrt-action-install-debuginfo.*
%{_mandir}/man*/abrt-action-analyze-ccpp-local.*
%{_mandir}/man*/abrt-action-analyze-core.*
%{_mandir}/man*/abrt-action-analyze-vulnerability.*
%{_mandir}/man*/abrt-action-perform-ccpp-analysis.*

%files addon-upload-watch
%defattr(-,root,root,-)
%{_sbindir}/abrt-upload-watch
%if %{with systemd}
%{_unitdir}/abrt-upload-watch.service
%else
%{_initrddir}/abrt-upload-watch
%endif
%{_mandir}/man*/abrt-upload-watch.*


%files retrace-client
%{_bindir}/abrt-retrace-client
%{_mandir}/man1/abrt-retrace-client.1.gz
%config(noreplace) %{_sysconfdir}/libreport/events.d/ccpp_retrace_event.conf
%{_mandir}/man5/ccpp_retrace_event.conf.5.gz
%{_datadir}/libreport/events/analyze_RetraceServer.xml

%files addon-kerneloops
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/koops_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/oops.conf
%{_datadir}/%{name}/conf.d/plugins/oops.conf
%{_mandir}/man5/koops_event.conf.5.gz
%if %{with systemd}
%{_unitdir}/abrt-oops.service
%else
%{_initrddir}/abrt-oops
%endif
%{_bindir}/abrt-dump-oops
%{_bindir}/abrt-action-analyze-oops
%{_bindir}/abrt-action-save-kernel-data
%{_mandir}/man1/abrt-dump-oops.1*
%{_mandir}/man1/abrt-action-analyze-oops.1*
%{_mandir}/man1/abrt-action-save-kernel-data.1*
%{_mandir}/man5/abrt-oops.conf.5*

%files addon-xorg
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/xorg_event.conf
%{_mandir}/man5/xorg_event.conf.5.gz
%if %{with systemd}
%{_unitdir}/abrt-xorg.service
%else
%{_initrddir}/abrt-xorg
%endif
%{_bindir}/abrt-dump-xorg
%{_mandir}/man1/abrt-dump-xorg.1*

%files addon-vmcore
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/vmcore_event.conf
%{_mandir}/man5/vmcore_event.conf.5.gz
%config(noreplace) %{_sysconfdir}/%{name}/plugins/vmcore.conf
%{_datadir}/%{name}/conf.d/plugins/vmcore.conf
%{_datadir}/libreport/events/analyze_VMcore.xml
%if %{with systemd}
%{_unitdir}/abrt-vmcore.service
%else
%{_initrddir}/abrt-vmcore
%endif
%{_sbindir}/abrt-harvest-vmcore
%{_bindir}/abrt-action-analyze-vmcore
%{_bindir}/abrt-action-check-oops-for-hw-error
%{_mandir}/man1/abrt-harvest-vmcore.1*
%{_mandir}/man5/abrt-vmcore.conf.5*
%{_mandir}/man1/abrt-action-analyze-vmcore.1*
%{_mandir}/man1/abrt-action-check-oops-for-hw-error.1*

%files addon-pstoreoops
%defattr(-,root,root,-)
%if %{with systemd}
%{_unitdir}/abrt-pstoreoops.service
%else
%{_initrddir}/abrt-pstoreoops
%endif
%{_sbindir}/abrt-harvest-pstoreoops
%{_bindir}/abrt-merge-pstoreoops
%{_mandir}/man1/abrt-harvest-pstoreoops.1*
%{_mandir}/man1/abrt-merge-pstoreoops.1*

%files addon-python
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python.conf
%{_datadir}/%{name}/conf.d/plugins/python.conf
%{_mandir}/man5/abrt-python.conf.5.gz
# TODO? Do we need %%config(noreplace) in the below line too?
%config(noreplace) %{_sysconfdir}/libreport/events.d/python_event.conf
%{_mandir}/man5/python_event.conf.5.gz
%{_bindir}/abrt-action-analyze-python
%{_mandir}/man1/abrt-action-analyze-python.1*
%{python_sitearch}/abrt*.py*
%{python_sitearch}/abrt.pth

%files cli
%defattr(-,root,root,-)

%files tui
%defattr(-,root,root,-)
%{_bindir}/abrt-cli
%{_mandir}/man1/abrt-cli.1.gz

%files desktop
%defattr(-,root,root,-)

%files dbus
%defattr(-,root,root,-)
%{_sbindir}/abrt-dbus
%{_sbindir}/abrt-configuration
%{_mandir}/man8/abrt-dbus.8.gz
%{_mandir}/man8/abrt-configuration.8.gz
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dbus-abrt.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.Problems.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.abrt.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.ccpp.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.oops.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.python.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.vmcore.xml
%{_datadir}/dbus-1/interfaces/com.redhat.problems.configuration.xorg.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.problems.service
%{_datadir}/dbus-1/system-services/com.redhat.problems.configuration.service
%{_datadir}/polkit-1/actions/abrt_polkit.policy
%dir %{_defaultdocdir}/%{name}-dbus-%{version}/
%dir %{_defaultdocdir}/%{name}-dbus-%{version}/html/
%{_defaultdocdir}/%{name}-dbus-%{version}/html/*.html
%{_defaultdocdir}/%{name}-dbus-%{version}/html/*.css

%files python
%{python_sitearch}/problem/
%{_mandir}/man5/abrt-python.5.gz

%files python-doc
%{python_sitelib}/problem_examples

%files console-notification
%config(noreplace) %{_sysconfdir}/profile.d/abrt-console-notification.sh

%changelog
* Fri Aug 16 2019 Jacco Ligthart <jacco@redsleeve.org> - 2.1.11-55.el7.redsleeve
- removed requirements to proprietary CentOS end RHEL libreport packages

* Tue Aug 06 2019 CentOS Sources <bugs@centos.org> - 2.1.11-55.el7.centos
- Drop RHTS hint
-  Change by David Mansfield <david@orthanc.cobite.com>
-  Per http://bugs.centos.org/view.php?id=7192
- Remove cli suggestion text patch
- set URL to retrace server
- update to not run sosreport
-  Per http://bugs.centos.org/view.php?id=7913

* Wed Mar 20 2019 Ernestas Kulik <ekulik@redhat.com> - 2.1.11-55
- Add patch for #1677476

* Thu Jan 3 2019 Martin Kutlak <mkutlak@redhat.com> - 2.1.11-54
- testsuite: move examples to 'tests'
- testsuite: Fix failing tests
- Add autogen.sh

* Tue Dec 18 2018 Martin Kutlak <mkutlak@redhat.com> - 2.1.11-53
- cli: load config file at the beginning
- ccpp: fast dumping and abrt core limit
- conf: increase MaxCrashReportsSize to 5GiB
- vmcore: /var/tmp/abrt is no longer a dump location
- koops: Filter kernel oopses based on logged hostname
- daemon: Fix double closed fd race condition
- Related: #1618818, #1647841, #1613236, #1613182, #1655241

* Mon Aug 20 2018 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-52
- plugin "general" from sos has been split into two new plugins
- Related: #1608444

* Mon Jun 25 2018 Matej Marusak <mmarusak@redhat.com> - 2.1.11-51
- a-a-s-p-data: fix segfault if GPGKeysDir isn't configured
- spec: turn on --enable-native-unwinder aarch64
- plugins: a-a-g-machine-id use dmidecode command
- spec: use dmidecode instead of python-dmidecode
- Related: #1566707, #1566707, #1260074, #1591141

* Thu Feb 8 2018 Martin Kutlak <mkutlak@redhat.com> - 2.1.11-50
- vmcore: fix analyzer regression
- Related: #1543323

* Thu Oct 26 2017 Martin Kutlak <mkutlak@redhat.com> - 2.1.11-49
- Translation updates
- Stop creating uReports for unpackaged executables
- koops: add detailed taint flag description for kernel oopses
- koops: fix kernel oops and fatal MCE recognition
- python: provide more information about Python exceptions
- vmcore: fix replication of vmcore files
- Related: #1271213, #1460224, #1374648, #1361116, #1228344,
- Related: #1395285, #1214730, #1446410, #1319828, #1501718

* Tue May 30 2017 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-48
- Translation updates
- Related: #1449488

* Tue Feb 21 2017 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-47
- add %h parameter into abrt-hook-ccpp
- Related: #1364899

* Wed Feb  8 2017 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-46
- remove not implemented option AttemptHardlink in vmcore.conf
- introduce unsafe reporting for not-reporable problems
- rewrite skip_pfx() function to work with journal msgs
- don't expect kernel's version '2.6.*' or '3.*.*'
- Related: #1416586, #1257159, #1328264, #1378469

* Thu Sep  1 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-45
- Translation updates
- Related: #1304240

* Thu Aug 18 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-44
- daemon: send  base names from abrt-server to abrtd
- Resolves: #1132459

* Thu Aug 18 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-43
- check_recent_crash_file do not produce error_msg
- Resolves: #1337186

* Mon Aug 01 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-42
- trigger dump location cleanup after detection
- Resolves: #1132459

* Tue Jun 14 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-41
- vmcore: fix finding partitions by UUID and LABEL
- Related: rhbz#1147053

* Thu May 26 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-40
- ccpp: unify log message of ignored crashes
- Resolves: #1337186

* Tue May 03 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-39
- python: fix check for absolute path
- console-notifications: add timeout
- vmcore: generate 'reason' file in all cases
- Fix memory leaks in abrt-dbus
- Resolves: #1250337, #1166633, #1249101, #1319704

* Thu Apr 14 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-38
- ccpp: add xfunc_die() if cannot get executable
- Resolves: #1277849

* Thu Apr 14 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-37
- ccpp: exit with error if cannot get executable
- Resolves: #1277849

* Thu Apr 14 2016 Matej Habrnal <mhabrnal@redhat.com> - 2.1.11-36
- lib: prevent from creating non-root sub-dirs in dump dir
- Save Vendor and GPG Fingerprint
- augeas: augtool save /files/etc/abrt/plugins/oops.conf/DropNotReportableOopses
- ccpp: add AllowedUsers and AllowedGroups feature
- ccpp: add IgnoredPath option
- lib: hooklib: make signal_is_fatal() public
- vmcore: catch IOErrors and OSErrors
- translations: update zanata configuration
- Resolves: #1311100, #1277848, #1277849, #1175679

* Fri Oct 30 2015 Jakub Filak <jfilak@redhat.com> - 2.1.11-35
- make /var/spool/abrt owned by root
- remove 'r' from /var/spool/abrt for other users
- abrt-action-install-debug-info: use secure temporary directory
- stop saving abrt's core files to /var/spool/abrt if DebugLevel < 1
- Fixes for: CVE-2015-5273 and CVE-2015-5287
- Resolves: #1266853

* Fri Oct 16 2015 Jakub Filak <jfilak@redhat.com> - 2.1.11-34
- sos: use 'services' instead of 'startup'
- Resolves: #1272005

* Thu Sep 17 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-33
- abrt-auto-reporting documentation
- ccpp: Use global PID
- ccpp: correct comments mentioning TID
- Related: #1252590, #1261036, #1223805

* Mon Aug 31 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-32
- Create UUID from core backtrace if coredump is missing
- Related: #1210601

* Wed Aug 19 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-31
- Only analyze vulnerabilities when coredump present
- Only generate core_backtrace if it's not already present.
- Related: #1210601

* Fri Aug 14 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-30
- Warn against disabling private reports in abrt.conf
- Related: #1253166

* Thu Aug 13 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-29
- ccpp: use global TID
- ccpp: fix comment related to 'MakeCompatCore' option in CCpp.conf
- cli: fix testing of DBus API return codes
- dbus-api: unify reporting of errors
- Related: #1210601, #1252419, #1224984

* Thu Jul 30 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-28
- doc: fix related to conditional compilation of man page
- spec: add dbus dependency for abrt-cli and abrt-python
- Related: #1191572, #1245527

* Wed Jul 29 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-27
- abrt-merge-pstoreoops: merge files in descending order
- abrt-auto-reporting: fix related to conditional compilation
- Update translations
- Related: #1233662, #1191572, #1181248

* Fri Jul 17 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-26
- reset ownership after saving core_backtrace
- Related: #1210601

* Fri Jul 17 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-25
- save core_backtrace from hook
- Related: #1210601

* Fri Jul 17 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-24
- support generating backtrace in core hook
- Resolves: #1210601

* Thu Jul 09 2015 Richard Marko <rmarko@redhat.com> - 2.1.11-23
- abrt-auto-reporting fixes
- include processor information in sosreport
- abrt-cli uses abrt-dbus to get the detected problems
- Related: #1191572, #1221118, #1224984

* Thu May 21 2015 Jakub Filak <jfilak@redhat.com> - 2.1.11-22
- do not open the build_ids file as the user abrt
- do not unlink failed and big user core files
- Related: #1212820, #1216974

* Wed May 13 2015 Jakub Filak <jfilak@redhat.com> - 2.1.11-21
- validate all D-Bus method arguments
- Related: #1214612

* Tue May 05 2015 Jakub Filak <jfilak@redhat.com> - 2.1.11-20
- remove the old dump directories during upgrade
- abrt-action-install-debuginfo-to-abrt-cache: sanitize arguments and umask
- fix race conditions and directory traversal issues in abrt-dbus
- use /var/spool/abrt instead of /var/tmp/abrt
- make the problem directories owned by root and the group abrt
- validate uploaded problem directories in abrt-handle-upload
- don't override files with user core dump files
- fix symbolic link and race condition flaws
- Resolves: #1211971, #1212820, #1212864, #1212870
- Resolves: #1214454, #1214612, #1216974, #1238724

* Fri Jan 09 2015 Jakub Filak <jfilak@redhat.com> - 2.1.11-19
- abrt-auto-reporting: add ureport authentication command line arguments
- add python-augeas to the requirements
- mark all strings for translations
- translation updates
- Related: #1087880, #1174833

* Thu Nov 20 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-18
- allow gdb to auto-load scripts from /var/cache/abrt-di
- Resolves: #1128637

* Fri Oct 31 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-17
- Translation updates
- machineid is a copy of /etc/machine-id
- Related: #1139552

* Tue Oct 21 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-16
- applet: ensure writable directory before reporting
- Resolves: #1084027

* Mon Oct 13 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-15
- console-notifications: skip non-interactive shells
- applet: show component instead of duphash in the notification
- Related: #1084031, #1150169

* Thu Oct 09 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-14
- ureport: attach contact email
- mce: separate mce analysis from Kernel oops analysis
- console-notifications: use return instead of exit
- Resolves: #1150389, #1150169
- Related: #1076820

* Fri Oct 03 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-13
- Translation updates
- localization fixes
- applet: confirm ignoring of notifications
- cli: batch reporting in abrt-cli
- cli: add option remove crash dirs after reporting
- cli: robustize abrt-console-notification.sh
- cli: make consistent commands in abrt-cli
- applet: chown each notified problem before reporting it
- dbus: fixed abrt-dbus memory leaks
- plugins: add abrt-action-generate-machine-id
- spec: add abrt-action-generate-machine-id
- spec: remove dependency on crash from abrt-addon-vmcore
- spec: hook abrt-oops.conf.5
- spec: don't use native unwinder on arm arch
- spec: remove stray space from %%description
- spec: add missing requires for python api
- spec: add dependency on abrt-python
- python: support exceptions without traceback
- spec: hook Kernel oops configuration files
- koops: add an option controlling MCE detection
- gdb: disable loading of auto-loaded files
- vmcore: start the service after kdump service
- Resolves: #1066482, #1084031, #1067545, #1084027, #1087880, #1087777
- Resolves: #1015473, #1139001, #1076820, #1139552, #1128637, #1066501
- Resolves: #1086642


* Mon Mar 03 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-12
- Translation updates
- Resolves: #1030314

* Wed Feb 26 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-11
- Capture all necessary logs in sosreport.tar.gz
- do not send ureport from abrt-applet
- do not run gdb under root
- Resolves: #1067114, #1069278, #1069719

* Wed Feb 19 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-10
- Search for MCE strings in 'backtrace' file
- Resolves: #1064458

* Mon Feb 10 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-9
- Stop consuming 100%%CPU in abrt-upload-watch
- Turn off Autoreporting
- Enabled GPG check
- Resolves: #1051480, #1063317

* Tue Feb 04 2014 Jakub Filak <jfilak@redhat.com> -  2.1.11-8
- retrace-client: do not require SSL2
- Resolves: #1060796

* Thu Jan 30 2014 Jakub Filak <jfilak@redhat.com> - 2.1.11-7
- Fix-handling-of-Machine-Check-Exceptions
- abrt-harvest-vmcore recovers from Permission denied errors
- never stop 'notify' event
- install abrt-python files to arch specific dir
- Resolves: #1032077, #1032511, #1057710
- Related: #881123

* Tue Jan 28 2014 Daniel Mach <dmach@redhat.com> - 2.1.11-6
- Mass rebuild 2014-01-24

* Thu Jan 23 2014 Jakub Filak <jfilak@redhat.com> 2.1.11-5
- abrt-cli requires libreport-rhel (the reporting workflows)
- applet: don't notify missing ignored_problems file
- abrt-cli: show a hint about creating a case in RHTS
- abrt-cli: show a info text suggesting enabling the autoreporting
- Related: #1044424
- Resolves: #1054291, #1055565, #1056980

* Wed Jan 22 2014 Jakub Filak <jfilak@redhat.com> 2.1.11-4
- applet: do not say the report is anonymous when ureport auth is enabled
- Resolves: #1055619

* Tue Jan 21 2014 Jakub Filak <jfilak@redhat.com> 2.1.11-3
- fix a double free error in abrt-applet
- configure Augeas to parse only required files
- show 'Close' button in the Configuration dialogue
- Resolves: #1050167, #1053534, #1054158

* Tue Jan 14 2014 Jakub Filak <jfilak@redhat.com> 2.1.11-2
- use elfutils stack unwinder
- collect installed RPM details in sosreport
- Resolves: #1048210, #1052920

* Wed Jan 08 2014 Jakub Filak <jfilak@redhat.com> 2.1.11-1
- Update translations
- harvest_vmcore: replace regexp config parsing with augeas
- introduce D-Bus Configuration Service
- mark koopses with unsupporeted HW as not-reportable
- bodhi: use the right exit codes
- abrt-handle-event: don't use already freed memory
- introduce abrt-auto-reporting utility
- abrt-action-notify: fix couple of flaws
- Use satyr to compute koops duphash
- koops: tweak koops parser for s390 Call Traces
- configui: do not use deprecated gtk3 API
- completely remove abrt-dedup-client
- move /etc/abrt/abrt-harvest-vmcore.conf to /etc/abrt/plugins/vmcore.conf
- Resolves: #1027259, #1035405, #1036585, #1040892, #1044424, #1050160

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.7-8
- Mass rebuild 2013-12-27

* Fri Dec 06 2013 Jakub Filak <jfilak@redhat.com> 2.1.7-7
- Remove the bodhi addon
- Resolves: #1038923

* Tue Dec 03 2013 Jakub Filak <jfilak@redhat.com> 2.1.7-6
- Add a dependency on abrt-python
- Resolves: #1037290

* Wed Nov 20 2013 Jakub Filak <jfilak@redhat.com> 2.1.7-5
- Enabled sosreport
- Resolves: #1032585

* Mon Nov 18 2013 Jakub Filak <jfilak@redhat.com> 2.1.7-4
- Enable autoreporting
- Resolves: #1031572

* Tue Nov 12 2013 Jakub Filak <jfilak@redhat.com> 2.1.7-3
- remove Fedora strings
- Resolves: #1029508

* Thu Oct 10 2013 Jakub Filak <jfilak@redhat.com> 2.1.7-2
- add python-doc package

* Wed Sep 11 2013 Jakub Filak <jfilak@redhat.com> 2.1.7-1
- fix debuginfo installer expecting user input from a pipe - closes #696
- add environment variable whitelist to debuginfo install wrapper - closes #692
- add repo_pattern argument as a custom repository filter - closes #688
- abrt-cli list: replace "@" prefix by "id " prefix
- fix a crash in 'abrt-cli info' when short id isn't found
- Use common string-to-sha1_hash functions. #694
- doc: update OpenGPGCheck in a-a-save-package-data rhbz#997922
- abrt-cli report: accept sha1 hashes of directory names. #693
- abrt-dump-oops: emit a message if throttling for a significant period of time
- abrt-gdb-exploitable: print current instruction
- spec: posttrans scriptlet regenerating core_backtraces
- abrt-handle-event: add check for missing crash thread
- provide tmpfiles.d configuration
- abrt-cli list: use sha1 hash as short ids instead of @N thing. rhbz#906733
- vmcore: fail gracefully if dump_dir is not accessible
- spec: vmcore: require kexec-tools
- vmcore: use re.MULTILINE instead of numerical value
- vmcore: don't fail if /etc/kdump.conf is not readable
- abrt-cli info: add "-s SIZE" option. closes #689
- fix noninteractive mode in debuginfo installer - rhbz#737066
- fixed the gpg keys loading - closes #686
- Fix type of OPT_BOOL's referenced flag variable - it must be int, not bool!
- adds a kdump.conf parser to get the correct dump dir location, closes #640
- xorg_event.conf: use abrt-action-list-dsos to create dso_list
- abrt-action-list-dsos: extend it to be able to parse Xorg backtrace.
- don't require debuginfo for vmcore analysis rhbz#768389
- specfile: make addon-pstoreoops obsolete addon-uefioops
- abrt-dump-oops: add -t option which slows down problem creation. rhbz#902398.
- rename uefioops to pstoreoops rhbz#949721
- spec: create type element for problem dirs where it doesn't exist - rhbz#958968
- introduce abrt-upload-watch
- fix ccpp hook to create the type element - closes #682
- specfile: use systemd-rpm macros. rhbz#850019
- abrt-harvest-vmcore: notify new path - #657
- abrt-dump-oops: remove redundant g_list_length() call, make messages clearer
- updated translation - rhbz#860555
- updated transifex url
- GUI config: add Close/Defaults button
- GUI config: hide option descriptions in tool tips
- GUI config: add Silent shortened reporting support
- applet: silent shortened reporting
- applet: less misleading label for Ignore button
- abrt-handle-upload: switch from shell to python; send socket notification. #657
- spec: add build requires for XSMP depencies
- applet: update seen list when X Session dies
- improved the error messages in abrt-server - closes #679
- fix typo in abrt-config-widget.ui
- spec: add new packages abrt-gui-libs and abrt-gui-devel
- delete desktop file for system-config-abrt
- expose abrt configuration GUI in public API
- rewrite abrt-harvest-uefioops to python - closes #678
- spec: abrt-python is no longer noarch - related #677
- created python binding for notify_new_path - closes #677
- spec: install applet's desktop file to system dir
- applet: configure notification source
- rewrite shell script for moving vmcores into python closes #676
- abrtd: ensure that the dump location directory exists
- a-a-ureport: generate core_backtrace only for CCpp problems
- do not store potentially big data in /tmp
- abrt-dbus: send new problem notify signal to socket
- abrtd: remove "post-create" machinery. Related to #657
- Avoid leaving stale rpmdb locks behind (rhbz#918184)
- abrtd: improve parsing of pidfile in create_pidfile()
- abrt-dump-{oops,xorg}: send new problem notify signal to socket
- abrtd: disable inotify watch on DUMP_LOC
- abrt-hook-ccpp: send "POST /creation_notification" after creating problem dir
- Stop dying in check_free_space(); rename it to low_free_space()
- abrt-server: make create_problem_dir() run "post-create"
- abrt-handle-event: create DUMP_LOC/post-create.lock when running "post-create"
- abrt-server: add support for "POST /creation_notification"
- abrt-handle-event: free more of allocated data
- Resolves: #880694, #895745, #906733, #949721, #953927, #960549, #961520, #967644, #990208, #993591, #993592

* Tue Aug 06 2013 Jakub Filak <jfilak@redhat.com> 2.1.6-3
- try to generate core_backtrace only for CCpp problems
- Resolves: #993630

* Tue Jul 30 2013 Jakub Filak <jfilak@redhat.com> 2.1.6-4
- do not require abrt-retrace-client

* Mon Jul 29 2013 Jakub Filak <jfilak@redhat.com> 2.1.6-3
- use RHTSupport even in report-cli events

* Mon Jul 29 2013 Jakub Filak <jfilak@redhat.com> 2.1.6-2
- disable gcc unused-typedef warning for GLib
- use right dependencies for RHEL

* Fri Jul 26 2013 Jakub Filak <jfilak@redhat.com> 2.1.6-1
- replace functions deprecated in Gtk-3.10 with their substitutes
- integrate with satyr, drop btparser
- use absolute path in python shebang rhzb#987010
- abrt-action-save-package-data: properly close rpm database. Closes #674.
- abrt-action-save-package-data: fix handling of ProcessUnpackaged on scripts
- abrt-action-save-package-data manpage: typo fix
- change /var/spool/abrt/ to /var/tmp/abrt in doc rhbz#912750
- Fix RPMdiff warnings about abrtd and abrt-action-install-debuginfo-to-abrt-cache
- specfile: add dependency on abrt-libs to abrt-addon-uefioops
- stop using the hardcoded event list, use workflows instead rhbz#866027
- retrace-client: build correct release for Fedora Rawhide
- spec: drop unnecessary Obsoletes and Provides
- correct FSF address in python exception hook
- add missing manual pages for binaries and scripts
- fix rpmlint issues in the spec file
- move event option XML files to /usr/share/libreport/
- abrt-hook-ccpp: always fall back to creating user core.
- dbus: add GetForeignProblems method
- the system tray icon opens recently detected problem
- add gdb python plugin which analyzes coredump for vulnerability
- applet: stop saving configuration at exit
- introduce system-config-abrt
- abrt-cli status: make the output more natural
- Fix wrong path in shell include
- abrt-dump-xorg: save "type=xorg" along with "analyzer=xorg"
- Update python hook to use fixed socket interface
- abrt-server: updates/fixes for future rasdaemon needs
- Resolves: #988165

* Fri Jun 14 2013 Jakub Filak <jfilak@redhat.com> 2.1.5-1
- abrt-retrace-client requires tar closes #635
- abrt-tui requires abrt closes #633
- a-d-oops: obtain kernel version from the oops
- a-a-p-ccpp-analysis: import all used attributes
- vmcore: provide all problem elements necessary for the reporting
- a-d-oops: add 'update' command line argument
- a-a-g-core-backtrace: don't crash if kernel file doesn't exist
- a-a-a-vmcore: save kernel version in 'kernel' file
- abrt-cli: make status help message more precise
- abrt-cli status: don't include reported problems into count
- abrt-cli list: implement --since and --until
- abrt-python: open dirs read-only if possible
- dbus: ChownProblemDir method really changes the owner
- python: disable events in collision with anaconda
- abrt-python requires pygobject2
- systemd units: start services only if it make sense
- abrt-harvest-uefioops.in: test for abrtd after testing for pstore, not before
- make abrt-uefioops.service conditional on /sys/fs/pstore being populated
- dbus: fix SetElement failing when shrinking an item
- spec: fix unowned directories
- abrt-python: whole python API path in POTFILES.skip
- abrt-python: fix dbus compatibility on RHEL6
- abrt-python: check if gid equals current users gid
- abrt-python: fix tests compatibility with python 2.6
- abrt-python: pass DD_OPEN_READONLY only if available
- abrt-python: fix deprecation warnings
- console notification shouldn't ask confirmation - closes #652
- Short BT deduplication false positives workaround
- Only problems of same type can be duplicates
- abrt-python: fix bug in problem.get
- abrt-python: pep8 cleanup
- koops parse: support <NMI> frame prefix
- don't show non critical errors in console notification
- Resolves: #958961, #974670

* Mon May 06 2013 Jakub Filak <jfilak@redhat.com> 2.1.4-3
- don't show non critical errors in console notification
- use last_occurrence with --since

* Fri May 03 2013 Jakub Filak <jfilak@redhat.com> 2.1.4-2
- start abrtd.service after livecd
- udpate translation
- add addon-uefioops
- Resolves: #928753

* Tue Apr 30 2013 Jakub Filak <jfilak@redhat.com> 2.1.4-1
- build abrtd and setuided executables with full relro rhbz#812284
- added a console notification script to profile.d closes #641
- return the right exit code for user cancellation
- add more examples to Problem API doc
- updated translation Related: #951416
- Replace "THANKYOU" with EXIT_STOP_EVENT_RUN exit code (70)
- abrt-action-ureport: rewrite in python, improve messages
- abrt-cli: added 'status' command
- abrt-cli: make "report -v[vv]" export correct $ABRT_VERBOSE value
- bodhi, retrace: support /etc/os-release
- abrt-action-generate-core-backtrace: be a bit more verbose
- abrt-dump-oops: add "Machine Check Exception" to the list of watched strings rhbz#812537
- abrt-action-install-debuginfo: do not assume os.execvp never returns
- abrtd: mark unprocessed dump directories as not-reportable
- abrtd: update last occurrence dump dir file
- spec: remove the commented macros rhbz#864851
- spec: added the versioned abrt-libs requires to silence rpmdiff rhbz#881123
- spec: create a new subpackage for the console notification #641
- spec: add deps. required for reporting to abrt-cli pkg
- spec: inc required version of libreport

* Mon Apr 08 2013 Jakub Filak <jfilak@redhat.com> 2.1.3-2
- Require correct version of libreport
- Add dependecies required for reporting to abrt-cli package
- Resolves: #947651

* Wed Mar 27 2013 Jakub Filak <jfilak@redhat.com> 2.1.3-1
- record runlevel
- Integration with satyr
- dbus: check correct errno after dump_dir_is_accessible_by_uid()
- require libreport workflow package acc. to OS type
- remove the abrt-gui closes #629
- retrace-client: do not allow space in os_release_id; closes #625
- Remove all smolt-related files and code bits
- abrtd: recreate Dump Location directory if it is delete

* Mon Mar 25 2013 Jakub Filak <jfilak@redhat.com> 2.1.2-4
- Check if restorecon cmd exists and run it only if it does
- Resolves: #926934

* Fri Mar 22 2013 Jakub Filak <jfilak@redhat.com> 2.1.2-3
- Fix problems with spaces in retrace-client

* Fri Mar 22 2013 Jakub Filak <jfilak@redhat.com> 2.1.2-2
- Require correct version of libreport
- Add a patch for abrtd which ensures that the dump location always exists
- disable shortened and auto reporting in RHEL
- Resolves: #918040, #918041

* Tue Mar 19 2013 Jakub Filak <jfilak@redhat.com> 2.1.2-1
- Improve log messages
- Update translation
- Introduce helpers for management of list of ignored problems
- applet: show a confirmation notify bubble for reported problems in ShortenedReporting mode
- applet: mark problems as ignored and don't notify ignored problems
- applet: remove confusing "Show" button
- applet: pass problem's id to the gui app
- abrt-ccpp: try to read hs_err.log from crash's CWD
- abrt-action-perform-ccpp-analysis: Complain if analyze_RetraceServer can't run. Closes 619
- abrt-gui: change URL to point to most recent doc
- add abrt-action-analyze-ccpp-local to ccpp-addon related to rhbz#759443
- analyze-ccpp don't suid to abrt when run as root, related rhbz#759443
- abrtd: prohibit DumpLocation == WatchCrashdumpArchiveDir. Closes rhbz#854668
- abrtd: don't blame interpreter, blame the running script #609
- a-a-ureport: don't fail on missing counter file
- a-a-ureport: allow to send ureport more than once
- dbus doc: install abrt-dbus documentation files to the correct places
- dbus doc: extend the documentation of DBus API
- dbus doc: make xml interface parseable by qtdbusxml2cpp
- dbus: add basics to a new problem
- abrt-harvest-vmcore: don't copy dir from var/spool if copy already exists
- fix path in the collect_xsession_errors event
- retrace-client: print dots instead of repeated status message
- move abrt.pth to arch specific location rhbz#912540
- Make forking code paths more robust.
- add more logging to catch "stuck core-backtrace" problem; reduce gdb looping
- Resolves: #879160, #854668, #885044, #903005, #905412, #909968, #912540

* Tue Mar 05 2013 Jakub Filak <jfilak@redhat.com> 2.1.1-2
- remove ureport events from the reporting workflow in RHEL

* Fri Feb 08 2013 Jakub Filak <jfilak@redhat.com> 2.1.1-1
- add SETGID bit to abrt-action-install-debuginfo-to-abrt-cache
- add abrt-desktop depency on libreport-fedora
- abrt-dump-{oops,xorg}: limit amount of created dirs, add cooldown sleep if exceeded
- abrt-watch-log: handle a case when child doesn't process its input
- abrt-watch-log: fix a bug in mmap error check
- abrt-action-analyze-xorg: fix the case with DIR != "."
- Resolves: #908256

* Mon Feb 04 2013 Jakub Filak <jfilak@redhat.com> 2.1.0-1
- pkg-config: export defaultdumplocation variable
- configure: set default dump location to /var/tmp/abrt
- abrtd: sanitize mode and ovner of all elements
- updated translation
- abrtd-inotify-flood test: expend it to check for another inotify-related bug
- gnome-abrt is default GUI
- applet: on requrest open gnome-abrt instead of abrt-gui
- Make it so that g_io_channel_read_chars(channel_inotify) does not buffer data.
- multilib fixes
- daemon: unify accessibility check before delete with dbus
- dbus: move dir accessibility check from abrt to libreport
- dbus: user dd_chown instead of own impl.
- allow default dump directory to be configured through cmd line args
- introduce abrt-python
- reporter-bz: post a comment to dup bug, if we found a dup. version 2.
- replace left over magic dd modes by macro
- synchronize default dump dir mode with libreport
- replace all occurrences of hardcoded dump location by a variable
- harvest-vmcore: read dump dir path from configuration
- use lchown when chowning files over dbus
- use lchown when chowning newly created problem directory
- verify-that-report-edits test: fix to account for new CLI interface
- koops: add all x86 TRAP prefixes to list of suspicious strings
- koops: put all suspicious strings to global variable
- applet: extend comment. No code changes
- applet: introduce shortened reporting
- abrt-applet: handle SIGTERM and perform nice termination
- abrt-applet: update the seen list on every possible action
- applet: don't notify outdated new problems
- Add and use "report-cli" event instead of removed "report-cli -r" option
- fixed the relro flags rhbz#812284
- applet: unref unused GIOChannel
- Resolves: #892230, #895742

* Thu Dec 20 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.20-1
- New version 2.0.20
- Fix typo: usefull->useful
- koops: generate core backtrace if missing
- udpated po files
- Cosmetic fixes in abrtd-inotify-flood test
- Hook up abrtd-inotify-flood to test infrastructure
- Add a testcase for inotify flood
- replace 'Start Autoreport' btn by a popup dialog
- dbus: NewProblem returns full path as problem_id
- abrt-action-analyze-xorg: fix /usr/include/paths.h -> paths.h
- abrtd: set inotify fd to non-blocking mode; ignore 0-sized inotify reads. Closes rhbz#873815
- s/ABRT dump/problem directory/g
- abrt-applet: don't leak component name
- abrt-applet: alerts only not reported problems
- build system: Remove leftover of abrt-action-analyze-xorg shell script
- Rewrite abrt-action-analyze-xorg in C (partially)
- rework abrt-gui>Help>'Report problem with ABRT'
- abrt-action-analyze-oops: fix help text - we have no -s option
- Help text fix - using "problem directory" consistently
- abrt-dump-oops: add list of tainted modules to NOT_REPORTABLE string. Closes trac#821
- a-a-p-c-a: use ask_yes_no_yesforever() fn from reportclient
- abrt-dump-oops: save /proc/modules contents. Partially closes trac#821
- add ureporter wrapper sending ureport only once per problem dir
- introduce Desktop Session Autoreporting
- add Autoreporting configuration options
- abrt-action-analyze-xorg: robustify 'test "a" = "b"' against bugs
- Collect ~/.xsession_errors from its new path, if it is there. Closes trac#791
- reflect recent libreport API changes .trac#822
- Indentation fix. No code changes.
- minor fix to previous commit realted to .trac#541
- don't use gtk_main* when using gtk_application .trac#890
- minor fix to quit button
- Make "Open problem data" open the expert mode GUI
- Teach kernel oops hash to ignore "<IRQ>" / "<EOI>" prefixes. Closes rhbz#875852
- introduce DeleteElement D-Bus method
- introduce SetElement D-Bus method
- allow only one instance of gui trac#541
- runtests/bugzilla-comment-format: fix false positive AGAIN
- update translations
- a-a-p-c-a: use correct name in gettext initialization
- Fix build system so that make rpm works again
- runtests/bugzilla-comment-format: fix false positive
- Improve xorg post-create. closes trac#838
- Update po files
- fix problem occurrence counter updating algorithm
- abrt-dbus: immediately return an error if not-existing problem is requested
- bugzilla-comment-format: new test
- a-a-p-c-a: use event python API instead of abrt-handle-event
- doc: add dbus problems service specification

* Mon Nov 26 2012 Jakub Filak <jfilak@redhat.com> 2.0.19-2
- update translations
- Resolves: #880201

* Wed Nov 14 2012 Jakub Filak <jfilak@redhat.com> 2.0.19-1
- call g_type_init() only in GLib version < 2.35
- plugins/*_event.conf: use reporter-bz -F FMTFILE as appropriate
- repeat unchaged retrace status message only in verbose mode
- check the correct return value of yesforever answer
- abrt-handle-event: forward event process requests to parent
- don't leak optional retrace path and kernel tainted string
- enhance koops tainted flag parser
- Use "comment" element instead of "description"
- Resolves: #873488

* Thu Nov 01 2012 Jakub Filak <jfilak@redhat.com> 2.0.18-1
- bugzilla-dupe-search: fix os_release to contain the same OS version as bug 755535
- Do not stop reporting when GConf entry is not found. Closes rhbz#869833
- Fix false positive caused by English language fix
- pyhook: import inspect lazily
- Resolves: #869833

* Wed Oct 24 2012 Jakub Filak <jfilak@redhat.com> 2.0.17-2
- remove ABRT1.0-to-ABRT2.0 upgrade script from spec file

* Wed Oct 24 2012 Jakub Filak <jfilak@redhat.com> 2.0.17-1
- provide a problem item containing versions of binaries listed in Xorg backtrace
  Adresses #867694 comment 1
- import rpm lazily
- Resolves: #864324

* Wed Oct 17 2012 Jakub Filak <jfilak@redhat.com> 2.0.16-1
- xorg_event: make post-create save dmesg, drop problems w/ binary modules
  Partially addresses: #856790
- collect_xsession_errors should not fail if !xsession-errors
  Resolves: #866698

* Thu Oct 11 2012 Jakub Filak <jfilak@redhat.com> 2.0.15-1
- add collect_* event to reporting chains for CCpp/Python/Kernel
- core-backtrace: make sure kernel version does not contain spaces
- core-backtrace: also include '?' flag for kerneloops
- don't check EXECUTABLE if it isn't present in list
- retrace-client: check whether all included files are regular
- abrt_exception_handler.py: save 'environ' element
- add Makefile target release-fix
- Make it possible for developer to disable crash processing for specific apps. Closes rhbz#848786
- s/Dump directory/Problem directory/
- Resolves: #864014, #864331, #848786

* Sun Oct 07 2012 Jakub Filak <jfilak@redhat.com> 2.0.14-2
- added forgotten Requires

* Fri Oct 05 2012 Jakub Filak <jfilak@redhat.com> 2.0.14-1
- abrt-dump-oops: save /sys/kernel/debug/suspend_stats. Closes rhbz#787749
- abrt-hook-ccpp: save /proc/sys/crypto/fips_enabled value if it isn't "0". Closes rhbz#747870
- abrt-dump-oops: save /proc/sys/crypto/fips_enabled value if it isn't "0". Closes rhbz#747870
- abrt-action-analyze-oops: fail if we end up hashing "" (empty string). Closes rhbz#862013
- retrace-client: respect chrooted os_release in pkgcheck
- Added oops_recursive_locking1.right to Makefile.am
- fix koops-parser.at, remove bastardized copy of oops_recursive_locking1.test
- add new oops example (currently fails, the fix is coming up)
- fix oops jiffies time stamp counter removal code
- trivia: s/dump/problem directory; fix false positive in oops-with-jiffies.right
- testsuite: added f18 kickstart
- open files for appned not for write rhbz#854266
- added more info about locking - rewrote with vda's comments rhbz#859724
- ccpp_event.conf: ignore crashes with nonzero TracerPid. Closes rhbz#812350
- show more info when abrtd can't acquire lock on pid, related to rhbz#859724
- abrt-hook-ccpp: save "proc_pid_status" element
- use FILENAME_ABRT_VERSION instead of string literal
- Fix pyhook test to reflect changes made in write_dump
- trac#333: Add code generating dso_list to the python hook
- spec: tui should require libreport-cli rhbz#859770
- trac#682: emit Crash DBus signal on org.freedesktop.problems bus
- spec: added deps on elfutils rhbz#859674
- Resolves: #859674, #859770, #859724, #812350, #854266, #862013, #747870, #787749

* Fri Sep 21 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.13-1
-

* Tue Aug 21 2012 Jakub Filak <jfilak@redhat.com> 2.0.12-1
- move abrtd.pid to /var/run/abrt/abrtd.pid
- abrt-harvest-vmcore: add CopyVMcore config option to copy vmcores. Closes 448, rhbz#811733, rhbz#844679
- update po files rhzb#800784
- applet: fix a SEGV caused by notify_init() not being called
- minor fix to pkg-config file
- ignore results of setregid() and setreuid() after glibc update
- hopefully fixed ugly applet icon rhbz#797078
- add update of abrt server database to event chains
- Resolves: #761431, #811733, #844679, #797078

* Fri Aug 10 2012 Jakub Filak <jfilak@redhat.com> 2.0.11-2
- fix abrt-dbus crash if no element is found in GetInfo()
- set sending-sensitive-data option to 'yes' for analyze_RetraceServer event

* Thu Aug 02 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.11-1
- new upstream release
- Resolves: #622773, #741222, #823299, #825116, #826058, #826800, #831333, #832085, #838842

* Tue May 22 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-4
- abrt-desktop should require abrt-retrace-client
- Resolves: #823812

* Thu May 10 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-3
- enable plugins unconditionally rhbz#819113

* Wed Apr 18 2012 Jiri Moskovcak <jmoskovc@redhat.com>
- fixed freeze in crashing python apps rhbz#808562
- Resolves: #808562

* Wed Apr 18 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-2
- minor rhel7 build fixes

* Mon Apr 02 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.10-1
- new upstream release
- fixed problem with empty problem directory rhzb#808131
- fixed exception in a-a-a-core when eu-unstrip output is broken
- Resolves: #808131, #804309

* Mon Mar 19 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-7
- fixed problems with rhel gpg keys rhbz#800419

* Thu Feb 02 2012 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.7-6
- abrt-desktop shouldn't require bodhi on rhel (2nd try)

* Wed Feb 01 2012 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.7-5
- abrt-desktop shouldn't require bodhi on rhel

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-3
- build fixes

* Thu Dec 08 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-2
- added man page
- fixed weird number formatting

* Wed Dec 07 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.7-1
- new version
- disabled kerneloops.org
- abrt-ccpp hook fixes
- catch indentation errors in python rhbz#578969
- fixed make check
- fixed retrace-client to work with rawhide
- require abrtd service in other services rhbz#752014
- fixed problems with dupes rhbz#701717
- keep abrt services enabled when updating F15->F16
- Resolves: 752014 749891 749603 744887 730422 665210 639068 625445 701717 752014 578969 732876 757683 753183 756146 749100

* Fri Nov 04 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.6-1
- new version
- Resolves: #701171 #712508 #726033 #728194 #728314 #730107 #733389 #738602
- Resolves: #741242 #749365 #700252 #734298 #736016 #738324 #748457 #692274
- Resolves: #711986 #723219 #749891 #712602 #744887 #749603 #625445 #665210
- Resolves: #737991 #639068 #578969 #636000 #631856

* Fri Oct 07 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 2.0.4.981-3
- don't file kernel bugs if "tainted: B" is set.
- don't file bugs about BIOS bugs.
- incorrect TAINTED description in bugs.
- Resoves: #718097 #708534 724838

* Mon Oct 3  2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4-981-2
- added abrt-retrace-client as a dependency

* Thu Sep 22 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4.981-1
- updated translation
- don't allow to skip the analyze step
- don't send ~ backups
- added hint to report only in English
- renamed abrt-action-kerneloops -> reporter-kerneloops
- explain option bugtracker and logger
- gui added padding to main window
- better message when gdb time outs
- added support for catching vmcores
- added version to Logger output
- [RFE] abrt should have an easy way to include smolt-profile
- Resolves: #694828 #694833 #704958 #735071 #731189 #739182 #704452 #734037 #606123 #631822

* Tue Sep 13 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4-5
- minor spec file fix

* Tue Sep 13 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4-4
- fixed sigsegv in a-a-save-package-data rhbz#737961
- fixed privs for /var/run/abrt rhbz#725974
- fixed segv in free space check
- Resolves: #737961 #725974

* Tue Aug 30 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4-3
- fixed abrt1-abrt2 update

* Fri Aug 19 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4-2
- enable bugzilla for kerneloops rhbz#725970
- Resolves: #725970

* Thu Jul 21 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4-1
- new upstream version
- resolves wrong provs/obsolete rhbz#723376
- split main UI into two panes
- debuginfo-install script asks before downloading
- Resolves: #723376

* Mon Jun 20 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.3-1
- new upstream release

* Fri May 20 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.2-6
- make abrt-ccpp and abrt-oops start on boot

* Fri May 13 2011 Karel Klíč <kklic@redhat.com> - 2.0.2-5
- Do not force service startup in %%posttrans, as it breaks live media
  creation (rhbz#704415)

* Sun May 08 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.2-4
- fixed prgname, fixes problem where Gnome3 shows lowres icons instead
  nice highres ones

* Fri May 06 2011 Christopher Aillon <caillon@redhat.com> - 2.0.2-3
- Update icon cache scriptlet per packaging guidelines

* Fri May 06 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.2-2
- flush messages in retrace client

* Thu May 05 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.2-1
- updated translation
- new icons (thanks to Lapo Calamandrei)
- changed address of retrace01 to retrace
- fixed problem with not trusted ssl certificate #695977
- #692713 Dialogue Box Buttons Wrong Way Around
- #695452 abrt crashing when trying to generate backtrace
- #698458 RFE: report separators between reports in abrt.log
- #699098 999 futile attempts to delete excess debuginfo
- #691881 GUI doesn't sort by last occurrence by default, and doesn't remember that sort order if you set it and restart the app
- #698418 Can't access '/var/spool/abrt/ccpp-2011-04-18-11:53:22-2661': Permission denied
- #698934 abrt-applet segfault on abrtd restart
- #695450 Retrace client - show meaningful message on failure
- #616407 RFE: Change abrt to catch TRAP signal crashes
- #584352 running service abrtd a non-root user doesn't show error
- retrace client: fail on servers with problematic SSL certificates (kklic@redhat.com)
- retrace-client: Load system-wide certificates. Move NSS init/shutdown to main, as it shouldn't be run multiple times. (kklic@redhat.com)
- abrt-cli: update manpage. Closes #243 (dvlasenk@redhat.com)
- move abrt-handle-crashdump to abrt-cli package. No code changes (dvlasenk@redhat.com)
- add abrt-action-print manpage. Closes #238 (dvlasenk@redhat.com)
- add abrt-action-trim-files manpage. Closes #241 (dvlasenk@redhat.com)
- added abrt-action-generate-backtrace manpage (dvlasenk@redhat.com)
- add abrt-action-analyze-backtrace manpage. Closes #227 (dvlasenk@redhat.com)
- retrace server: do not create zombie workers (mtoman@redhat.com)
- btparser: Remove top frame with address 0x0000 (jump to NULL) during normalization to avoid incorrect backtrace ratings (rhbz#639049) (kklic@redhat.com)
- abrt-gui: better list refreshing. Closes #251 (dvlasenk@redhat.com)
- fix for spurious "Lock file 'DIR/.lock' is locked by process PID" message (dvlasenk@redhat.com)
- Asciidoc manpage support; abrt-action-mailx manpage (kklic@redhat.com)
- list-dsos: don't list the same library multiple times (jmoskovc@redhat.com)
- call abrt-action-trim-files from abrt-action-install-debuginfo (dvlasenk@redhat.com)
- list-dsos: added package install time trac#123 (jmoskovc@redhat.com)
- retrace client: handle messages in HTTP body (mtoman@redhat.com)
- retrace server: remove chroot on failure (mtoman@redhat.com)
- spec: use versioned deps on libreport (jmoskovc@redhat.com)
- generate abrt version from git (npajkovs@redhat.com)
- abrt-action-trim-files needs to be suided rhbz#699098 (jmoskovc@redhat.com)
- gui: suppress printing dumpdir access errors (bz#698418) (mlichvar@redhat.com)
- Do not leave dump dir locked by abrt-action-generate-backtrace. (kklic@redhat.com)
- wizard: expand explanatory text on 1st screen. Closes 201 (dvlasenk@redhat.com)
- gui: fixed the OK and CANCEL buttons order in event config dialog (jmoskovc@redhat.com)
- Make abrt-action-list-dsos.py take -m maps -o dsos params; and abrt-action-analyze-core.py to take -o build_ids param (dvlasenk@redhat.com)
- abrt-action-install-debuginfo.py: don't die on some Yum exceptions. closes bz#681281 (dvlasenk@redhat.com)

* Thu Apr 21 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.1-2
- don't allow reporting of backtrace with rating = 0 rhbz#672023
- use versioned deps on libreport

* Wed Apr 20 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.1-1
- updated to 2.0.1
- updated translation
- allowed reporting oops to bugzilla
- added warning when the plugin settings are wrong
- added help text in plugins settings
- the plugin settings dialog is translatable
- improved dir rescanning logic in abrt-gui
- fixed icons for child dialogs
- retrace-client: human readable messages instead of http codes
- save envirnment variables when app crashes
- fixed gpg/pgp check
- revert to the old icon

* Fri Apr 15 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.0-5
- fixed problem with abrt-action-debuginfo-install rhbz#692064

* Thu Mar 31 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.0-4
- fixed prgname in wizard rhbz#692442

* Wed Mar 30 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.0-3
- fixed notification persistence in gnome3 (again)
- fixed wrong group:user on /var/cache/abrt-di afte rupdate from abrt 1.x #692064
- added mono-core to blacklist

* Tue Mar 29 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.0-2
- use %%ghost on files in /var/run and /var/lock rhbz#656542
- fixed notification persistence in gnome3
- added analyze selector to CLI
- refuse reporting to bz without backtrace or hash
- use g_set_prgname to set the prgname of abrt-gui trac#180

* Wed Mar 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.0-1
- update to the latest upstream version
- many improvements
- FIXME: add closed bugzillas

* Fri Feb 18 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.17-2
- removed gnome-python2-vfs dependency

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.17-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 05 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.17-1
- rewritten abrt-debuginfo-install script to use the yum API
- GUI: added search box to backtrace view rhbz#612017 (jmoskovc@redhat.com)
- fixed some gui warnings rhbz#671488 (jmoskovc@redhat.com)
- btparser/dupechecker improvements:
  - Better handling of glibc architecture-specific functions (kklic@redhat.com)
  - support format of thread header: "Thread 8 (LWP 6357):" (kklic@redhat.com)

* Fri Feb 04 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.16-1
- rhtsupport: added list of attachments to comment rhbz#668875
- rhtsupport: stop consuming non-standard header rhbz#670492
- Resolves: #670492, #668875

* Wed Jan 19 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.15-2
- add a gui/uid to useradd/groupadd command (reserved in setup rhbz#670231)
- Resolves: #650975

* Wed Jan 19 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.15-1
- removed unused files (jmoskovc@redhat.com)
- update po files (jmoskovc@redhat.com)
- removed some unused files (jmoskovc@redhat.com)
- pass old pattern to ccpp hook and use it (dvlasenk@redhat.com)
- GUI: added warning when gnome-keyring can't be accessed rhbz#576866 (jmoskovc@redhat.com)
- 666893 - Unable to make sense of XML-RPC response from server (npajkovs@redhat.com)
- PyHook: ignore SystemExit exception rhbz#636913 (jmoskovc@redhat.com)
- 665405 - ABRT's usage of sos does not grab /var/log/messages (npajkovs@redhat.com)
- add a note in report if kernel is tainted (npajkovs@redhat.com)
- KerneloopsScanner.cpp: make a room for NULL byte (npajkovs@redhat.com)
- fix multicharacter warring (npajkovs@redhat.com)
- open help page instead of about rhbz#666267

* Wed Jan 19 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.14-3
- fixed build with rpm 4.9 (thx panu pmatilai for the patch)

* Wed Jan 19 2011 Matthias Clasen <mclasen@redhat.com> 1.1.14-2
- Rebuild against new rpm

* Wed Nov 17 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.14-1
- made howto mandatory
- fixed segv in abrt-hook-ccpp rhbz#652338
- added warning if kernel was tainted
- make the "install debuginfo" hint selectable rhbz#644343
- wrap howto and comments rhbz#625237
- wrap lines in the backtrace window rhbz#625232
- changed '*' to '•' rhbz#625236
- make the bt viewer not-editable rhbz#621871
- removed unneeded patches

* Wed Nov 10 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.13-3
- Rebuild for libnotify-0.7

* Wed Aug 25 2010 Jochen Schmitt <Jochen herr-schmitt de> 1.1.13-2
- Rebuild for python-2.7

* Tue Aug 10 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.13-1
- updated translation
- added native systemd file rhbz#617316 (jmoskovc@redhat.com)
- added ar to LINGUAS (jmoskovc@redhat.com)
- made /etc/abrt/plugins/Bugzilla.conf world-readable again (jmoskovc@redhat.com)
- l10n: adding fa locale (lashar@fedoraproject.org)
- l10n: new Persian (lashar@fedoraproject.org)
- remove libzip code (npajkovs@redhat.com)
- add libxml-2.0 into configure (npajkovs@redhat.com)
- fixed typo in man page rhbz#610748 (jmoskovc@redhat.com)
- RHTSupport: GUI's SSLVerify checkbox had one missing bit of code (vda.linux@googlemail.com)
- abrt_curl: discard headers from HTTP redirection (vda.linux@googlemail.com)
- moved abrt.socket and abrtd.lock into /var/run/abrt making selinux happy (jmoskovc@redhat.com)
- Mention --info and --backtrace in the abrt-cli man page. (kklic@redhat.com)
- build fixes for gcc 4.5 (jmoskovc@redhat.com)
- abrt-hook-ccpp: small fixes prompted by testing on RHEL5 (vda.linux@googlemail.com)
- Added --info action to abrt-cli (mtoman@redhat.com)
- wire up SSLVerify in RHTSupport.conf to actually have the desired effect (vda.linux@googlemail.com)
- fixed tooltip localization rhbz#574693 (jmoskovc@redhat.com)
- dumpoops/KerneloopsScanner: add pid to crashdump name (vda.linux@googlemail.com)
- A message change suggested by dhensley (kklic@redhat.com)

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.10-4
- rebuild

* Tue Jul 27 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.10-3
- blacklist /usr/bin/nspluginviewer

* Mon Jul 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.10-2
- minor build fixes

* Mon Jul 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.10-1
- blacklisted mono-core package
- die with an error message if the database plugin is not accessible when needed (kklic@redhat.com)
- change RHTSupport URL protocol from HTTP to HTTPS (dvlasenk@redhat.com)
- the Logger plugin returns a message as the result of Report() call instead of a file URL (kklic@redhat.com)
- Cut off prelink suffixes from executable name if any (mtoman@redhat.com)
- CCpp: abrt-debuginfo-install output lines can be long, accomodate them (dvlasenk@redhat.com)
- do not pop up message on crash if the same crash is the same (dvlasenk@redhat.com)
- fedora bugs do not depend on rhel bugs (npajkovs@redhat.com)
- GUI: fixed problem with no gkeyring and just one reporter enabled rhbz#612457 (jmoskovc@redhat.com)
- added a document about interpreted language integration (kklic@redhat.com)
- moved devel header files to inc/ and included them in -devel package (jmoskovc@redhat.com, npajkovs@redhat.com)
- renamed abrt-utils.pc to abrt.pc (jmoskovc@redhat.com)
- string updates based on a UI text review (kklic@redhat.com)
- rhtsupport obsoletes the old rh plugins (jmoskovc@redhat.com)
- list allowed items in RHTSupport.conf (kklic@redhat.com)
- GUI: fixed package name in warning message when the packge is kernel rhbz#612191 (jmoskovc@redhat.com)
- remove rating for python crashes (jmoskovc@redhat.com)
- CCpp: give zero rating to an empty backtrace (jmoskovc@redhat.com)
- GUI: allow sending crashes without rating (jmoskovc@redhat.com)
- RHTSupport: set default URL to api.access.redhat.com/rs (dvlasenk@redhat.com)
- abort initialization on abrt.conf parsing errors (dvlasenk@redhat.com)
- changing NoSSLVerify to SSLVerify in bugzilla plugin (mtoman@redhat.com)
- added rating to python crashes
- show hostname in cli (kklic@redhat.com)
- updated po files (jmoskovc@redhat.com)
- added support for package specific actions rhbz#606917 (jmoskovc@redhat.com)
- renamed TicketUploader to ReportUploader (jmoskovc@redhat.com)
- bad hostnames on remote crashes (npajkovs@redhat.com)
- unlimited MaxCrashReportsSize (npajkovs@redhat.com)
- abrt_rh_support: improve error messages rhbz#608698 (vda.linux@googlemail.com)
- Added BacktraceRemotes option. (kklic@redhat.com)
- Allow remote crashes to not to belong to a package. Skip GPG check on remote crashes. (kklic@redhat.com)
- remove obsolete Catcut and rhfastcheck reporters (vda.linux@googlemail.com)
- make rhel bug point to correct place rhbz#578397 (npajkovs@redhat.com)
- Show comment and how to reproduce fields when reporing crashes in abrt-cli (kklic@redhat.com)
- Bash completion update (kklic@redhat.com)
- Rename --get-list to --list (kklic@redhat.com)
- Update man page (kklic@redhat.com)
- Options overhaul (kklic@redhat.com)
- abrt should not point to Fedora bugs but create new RHEL bug instead (npajkovs@redhat.com)
- Don't show global uuid in report (npajkovs@redhat.com)
- GUI: don't try to use action plugins as reporters (jmoskovc@redhat.com)
- Added WatchCrashdumpArchiveDir directive to abrt.conf and related code (vda.linux@googlemail.com)
- GUI: don't show the placehondler icon rhbz#605693 (jmoskovc@redhat.com)
- Make "Loaded foo.conf" message less confusing (vda.linux@googlemail.com)
- Fixed a flaw in strbuf_prepend_str (kklic@redhat.com)
- TicketUploader: do not add '\n' to text files in crashdump (vda.linux@googlemail.com)
- GUI: skip the plugin selection, if it's not needed (jmoskovc@redhat.com)
- Check conf file for syntax errors (kklic@redhat.com)
- move misplaced sanity checks in cron parser (vda.linux@googlemail.com)
- GUI: don't require the rating for all reporters (jmoskovc@redhat.com)
- GUI: fixed exception when there is no configure dialog for plugin rhbz#603745 (jmoskovc@redhat.com)
- Add a GUI config dialog for RHTSupport plugin (vda.linux@googlemail.com)
- abrt_curl: fix a problem with incorrect content-length on 32-bit arches (vda.linux@googlemail.com)
- sosreport: save the dump directly to crashdump directory (vda.linux@googlemail.com)
- plugin rename: rhticket -> RHTSupport (vda.linux@googlemail.com)
- Daemon socket for reporting crashes (karel@localhost.localdomain)
- GUI: fixed few typos (jmoskovc@redhat.com)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 09 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.5-1
- GUI: polished the reporter assistant (jmoskovc@redhat.com)
- Logger reporter: do not store useless info (vda.linux@googlemail.com)
- ccpp hook: add SaveBinaryImage option which saves of the crashed binary (vda.linux@googlemail.com)
- SPEC: added CFLAGS="-fno-strict-aliasing" to fix the rpmdiff warnings rhbz#599364 (jmoskovc@redhat.com)
- GUI: don't remove user comments when re-reporting the bug rhbz#601779 (jmoskovc@redhat.com)
- remove "(deleted)" from executable path rhbz#593037 (jmoskovc@redhat.com)
- CCpp analyzer: add 60 sec cap on gdb run time. (vda.linux@googlemail.com)
- add new file *hostname* into debugdump directory (npajkovs@redhat.com)
- rhticket: upload real tarball, not a bogus file (vda.linux@googlemail.com)
- abrt-hook-ccpp: eliminate race between process exit and compat coredump creation rhbz#584554 (vda.linux@googlemail.com)
- rhticket: actually do create ticket, using Gavin's lib code (vda.linux@googlemail.com)
- properly obsolete gnome-python2-bugbuddy rhbz#579748 (jmoskovc@redhat.com)
- GUI: remember comment and howto on backtrace refresh rhbz#545690 (jmoskovc@redhat.com)
- use header case in button label rhbz#565812 (jmoskovc@redhat.com)
- make log window resizable (vda.linux@googlemail.com)
- rename a few remaining /var/cache/abrt -> /var/spool/abrt (vda.linux@googlemail.com)

* Wed May 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.4-1
- added reporting wizard
- fixed few leaked fds
- fixed kerneloops --- cut here --- problem
- updated translations

* Fri May 21 2010 Denys Vlasenko <dvlasenk@redhat.com> 1.1.3-1
- More fixes for /var/cache/abrt -> /var/spool/abrt conversion

* Fri May 21 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.2-3
- fixed spec file to create /var/spool/abrt rhbz#593670
- updated init script to reflect the pid file renaming

* Wed May 19 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.2-1
- updated translation
- obsolete gnome-python2-bugbuddy rhbz#579748 (jmoskovc@redhat.com)
- Report "INFO: possible recursive locking detected rhbz#582378 (vda.linux@googlemail.com)
- kill yumdownloader if abrt-debuginfo-install is terminated mid-flight (vda.linux@googlemail.com)
- do not create Python dumps if argv[0] is not absolute (vda.linux@googlemail.com)
- improve kerneloops hash (vda.linux@googlemail.com)
- Move /var/cache/abrt to /var/spool/abrt. rhbz#568101. (vda.linux@googlemail.com)
- bugzilla: better summary and decription messages (npajkovs@redhat.com)
- renamed daemon pid and lock file rhbz#588315 (jmoskovc@redhat.com)
- Daemon socket for reporting crashes (kklic@redhat.com)
- Move hooklib from src/Hooks to lib/Utils (kklic@redhat.com)

* Thu May 13 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.1-1
- updated translations
- removed avant-window-navigator from blacklist (jmoskovc@redhat.com)
- Abort debuginfo download if low on disk space (partially addresses #564451) (vda.linux@googlemail.com)
- fix bug 588945 - sparse core files performance hit (vda.linux@googlemail.com)
- Add BlackListedPaths option to abrt.conf. Fixes #582421 (vda.linux@googlemail.com)
- Do not die when /var/cache/abrt/*/uid does not contain a number (rhbz#580899) (kklic@redhat.com)
- rid of rewriting config in /etc/abrt/abrt.conf (npajkovs@redhat.com)
- fix bug 571411: backtrace attachment of the form /var/cache/abrt/foo-12345-67890/backtrace (vda.linux@googlemail.com)
- Do not echo password to terminal in abrt-cli (kklic@redhat.com)
- improved daemon error messages (kklic@redhat.com)

* Mon May 03 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.0-1
- updated transaltions
- added Hebrew into languages
- updated icons rhbz#587698 (jmoskovc@redhat.com)
- Bugzilla login/password emptiness check uses 'or' instead of 'and' (kklic@redhat.com)
- Show error message when abrtd service is run as non-root. rhbz#584352 (kklic@redhat.com)
- Rename EnableOpenGPG to OpenGPGCheck in the man page rhbz#584332 (kklic@redhat.com)
- Document ProcessUnpackaged in abrt.conf.5. Document default values. (kklic@redhat.com)
- Crash function is now detected even for threads without an abort frame (kklic@redhat.com)
- comment can be private (npajkovs@redhat.com)
- do not catch perl/python crashes when the script is not of known package origin (kklic@redhat.com)
- kerneloop is more informative when failed (npajkovs@redhat.com)
- add function name into summary(if it's found) (npajkovs@redhat.com)
- Change kerneloops message when it fails (npajkovs@redhat.com)

* Fri Apr 30 2010 Karel Klic <kklic@redhat.com> 1.0.9-3
- fixed crash function detection (a part of duplication detection)

* Wed Apr 14 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.0.9-2
- fixed problem with localized yum messages rhbz#581804
- better bugzilla summary (napjkovs@redhat.com)
- ignore interpreter (py,perl) crashes caused by unpackaged scripts (kklic@redhat.com)

* Tue Apr 06 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.0.9-1
- hooklib: fix excessive rounding down in free space calculation (bz#575644) (vda.linux@googlemail.com)
- gui: fix 551989 "crash detected in abrt-gui-1.0.0-1.fc12" and such (vda.linux@googlemail.com)
- trivial: fix 566806 "abrt-gui sometimes can't be closed" (vda.linux@googlemail.com)
- gui: fix the last case where gnome-keyring's find_items_sync() may throw DeniedError (vda.linux@googlemail.com)
- fixed some compilation problems on F13 (jmoskovc@redhat.com)
- updated translations (jmoskovc@redhat.com)
- minor fix to sosreport to make it work with latest sos rhbz#576861 (jmoskovc@redhat.com)

* Wed Mar 31 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.0.9-0.201003312045.1
- test day build
- updated translation
- minor fix to sosreport to make it work with latest sos rhbz#576861 (jmoskovc@redhat.com)
- GUI: total rewrite based on design from Mairin Duffy (jmoskovc@redhat.com)
- trivial: better HTTP/curl error reporting (vda.linux@googlemail.com)
- Use backtrace parser from abrtutils, new backtrace rating algorithm, store crash function if it's known (kklic@redhat.com)
- abrt-rate-backtrace is replaced by abrt-backtrace --rate (kklic@redhat.com)
- Ignore some temp files (kklic@redhat.com)
- PYHOOK: don't use sitecustomize.py rhbz#539497 (jmoskovc@redhat.com)
- rhfastcheck: a new reporter plugin based on Gavin's work (vda.linux@googlemail.com)
- rhticket: new reporter plugin (vda.linux@googlemail.com)
- GUI: fixed few window icons (jmoskovc@redhat.com)
- Allow user to select which reporter he wants to use to report a crash using CLI.(kklic@redhat.com)
- bz reporter: s/uuid/duphash; more understandable message; simplify result str generation; fix indentation (vda.linux@googlemail.com)
- GUI: fixed crash count column sorting rhbz#573139 (jmoskovc@redhat.com)
- Kerneloops: use 1st line of oops as REASON. Closes rhbz#574196. (vda.linux@googlemail.com)
- Kerneloops: fix a case when we file an oops w/o backtrace (vda.linux@googlemail.com)
- minor fix in abrt-debuginfo-install to make it work with yum >= 3.2.26 (jmoskovc@redhat.com)
- GUI: added action to applet to directly report last crash (jmoskovc@redhat.com)
- Never flag backtrace as binary file (fixes problem observed in bz#571411) (vda.linux@googlemail.com)
- improve syslog file detection. closes bz#565983 (vda.linux@googlemail.com)
- add arch, package and release in comment (npajkovs@redhat.com)
- add ProcessUnpackaged option to abrt.conf (vda.linux@googlemail.com)
- abrt-debuginfo-install: use -debuginfo repos which match enabled "usual" repos (vda.linux@googlemail.com)
- fix format security error (fcrozat@mandriva.com)
- icons repackaging (jmoskovc@redhat.com)
- partial fix for bz#565983 (vda.linux@googlemail.com)
- SPEC: Updated source URL (jmoskovc@redhat.com)
- removed unneeded patches
- and much more ...

* Sat Mar 13 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.8-3
- fixed kerneloops reporting rhbz#570081
- fixed Source url
- fixed debuginfo-install to work on F13
  - improved debuginfo-install (vda.linux@googlemail.com)
  - fix debuginfo-install to work with yum >= 3.2.26 (jmoskovc@redhat.com)

* Wed Mar  3 2010  Denys Vlasenko <dvlasenk@redhat.com> 1.0.8-2
- fix initscript even more (npajkovs@redhat.com)
- remove -R2 from yum command line

* Mon Feb 22 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.8-1
- fix initscript (npajkovs@redhat.com)
- Kerneloops: make hashing more likely to produce same hash on different oopses (vda.linux@googlemail.com)

* Mon Feb 22 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.8-0.git-20100222
- Kerneloops: make hashing more likely to produce same hash on different oopses (vda.linux@googlemail.com)
- make abrt work with the latest kernels (>= 2.6.33) (jmoskovc@redhat.com)
- lib/Utils/abrt_dbus: utf8-sanitize all strings in dbus messages (fixes #565876) (vda.linux@googlemail.com)

* Fri Feb 12 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.7-1
- enabled column sorting rhbz#541853
- Load plugin settings also from ~/.abrt/*.conf (kklic@redhat.com)
- fix bz#541088 "abrt should not catch python excp EPIPE" (vda.linux@googlemail.com)
- fix bz#554242 "Cannot tab between input areas in report dialog" (vda.linux@googlemail.com)
- fix bz#563484 "abrt uses unnecessary disk space when getting debug info" (vda.linux@googlemail.com)
- Don't show empty 'Not loaded plugins' section - fix#2 rhbz#560971 (jmoskovc@redhat.com)
- fix big-endian build problem (vda.linux@googlemail.com)
- Fixes, displays package owners (kklic@redhat.com)
- GUI: fixed exception in plugin settings dialog rhbz#560851 (jmoskovc@redhat.com)
- GUI: respect system settings for toolbars rhbz#552161 (jmoskovc@redhat.com)
- python hook: move UUID generation to abrtd; generate REASON, add it to bz title (vda.linux@googlemail.com)
- make "reason" field less verbose; bz reporter: include it in "summary" (vda.linux@googlemail.com)
- added avant-window-navigator to blacklist per maintainer request (jmoskovc@redhat.com)
- CCpp analyzer: fix rhbz#552435 (bt rating misinterpreting # chars) (vda.linux@googlemail.com)
- Ask for login and password if missing from reporter plugin. (kklic@redhat.com)
- abrtd: fix handling of dupes (weren't deleting dup's directory); better logging (vda.linux@googlemail.com)
- abrtd: handle "perl -w /usr/bin/script" too (vda.linux@googlemail.com)
- Component-wise duplicates (kklic@redhat.com)
- abrtd: fix rhbz#560642 - don't die on bad plugin names (vda.linux@googlemail.com)
- Fixed parsing backtrace from rhbz#549293 (kklic@redhat.com)
- GUI: fixed scrolling in reporter dialog rhbz#559687 (jmoskovc@redhat.com)
- fixed button order in plugins windows rhbz#560961 (jmoskovc@redhat.com)
- GUI: fixed windows icons and titles rhbz#537240, rhbz#560964 (jmoskovc@redhat.com)
- Fix to successfully parse a backtrace from rhbz#550642 (kklic@redhat.com)
- cli: fix the problem of not showing oops text in editor (vda.linux@googlemail.com)
- GUI: fix rhbz#560971 "Don't show empty 'Not loaded plugins' section" (vda.linux@googlemail.com)

* Tue Feb  2 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.6-1
- print __glib_assert_msg (rhbz#549735);
- SPEC: added some requires to abrt-cli to make it work out-of-the-box (jmoskovc@redhat.com)
- abrt-hook-ccpp: fix rhbz#560612 "limit '18446744073709551615' is bogus" rhbz#560612(vda.linux@googlemail.com)
- APPLET: don't show the icon when abrtd is not running rhbz#557866 (jmoskovc@redhat.com)
- GUI: made report message labels wrap (jmoskovc@redhat.com)
- GUI: don't die if daemon doesn't send the gpg keys (jmoskovc@redhat.com)
- disabled the autoreporting of kerneloopses (jmoskovc@redhat.com)
- Kerneloops: fix BZ reporting of oopses (vda.linux@googlemail.com)
- GUI: wider report message dialog (jmoskovc@redhat.com)
- moved the gpg key list from abrt.conf to gpg_keys file (jmoskovc@redhat.com)
- Logger: create log file with mode 0600 (vda.linux@googlemail.com)
- GUI: fixed the rating logic, to prevent sending BT with rating < 3 (jmoskovc@redhat.com)
- Report GUI: made more fields copyable - closed rhbz#526209; tweaked wording (vda.linux@googlemail.com)
- GUI: fixed bug caused by failed gk-authorization (jmoskovc@redhat.com)

* Fri Jan 29 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.5-1
- moved the gpg key list from abrt.conf to gpg_keys file (jmoskovc@redhat.com)
- Logger: create log file with mode 0600 rhbz#559545 (vda.linux@googlemail.com)
- GUI: fixed the rating logic, to prevent sending BT with rating < 3 (jmoskovc@redhat.com)
- Report GUI: made more fields copyable - closed rhbz#526209; tweaked wording (vda.linux@googlemail.com)
- GUI: fixed bug caused by failed gk-authorization (jmoskovc@redhat.com)
- fix bug 559881 (kerneloops not shown in "new" GUI) (vda.linux@googlemail.com)
- GUI ReporterDialog: hide log button (vda.linux@googlemail.com)
- added valgrind and strace to blacklist (jmoskovc@redhat.com)
- SOSreport: do not leave stray files in /tmp (vda.linux@googlemail.com)
- Save the core where it belongs if ulimit -c is > 0 (jmoskovc@redhat.com)
- reenabled gpg check (jmoskovc@redhat.com)
- SOSreport: run it niced (vda.linux@googlemail.com)
- report GUI: rename buttons: Log -> Show log, Send -> Send report (vda.linux@googlemail.com)
- applet: reduce blinking timeout to 3 sec (vda.linux@googlemail.com)
- fix dbus autostart (vda.linux@googlemail.com)
- abrtd: set "Reported" status only if at least one reporter succeeded (vda.linux@googlemail.com)
- SQLite3: disable newline escaping, SQLite does not handle it (vda.linux@googlemail.com)
- SOSreport: make it avoid double runs; add forced regeneration; upd PLUGINS-HOWTO (vda.linux@googlemail.com)
- attribute SEGVs in perl to script's package, like we already do for python (vda.linux@googlemail.com)

* Wed Jan 20 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.4-1
- enabled sosreport
- fixes in ticketuploader
- GUI: redesign of reporter dialog (jmoskovc@redhat.com)
- Set the prgname to "Automatic Bug Reporting Tool" fixes rhbz#550357 (jmoskovc@redhat.com)
- CCpp analyzer: display __abort_msg in backtrace. closes rhbz#549735 (vda.linux@googlemail.com)
- s/os.exit/sys.exit - closes rhbz#556313 (vda.linux@googlemail.com)
- use repr() to print variable values in python hook rhbz#545070 (jmoskovc@redhat.com)
- gui: add logging infrastructure (vda.linux@googlemail.com)
- Added "Enabled = yes" to all plugin's config files (jmoskovc@redhat.com)
- *: disable plugin loading/unloading through GUI. Document keyring a bit (vda.linux@googlemail.com)
- fix memory leaks in catcut plugin (npajkovs@redhat.com)
- fix memory leaks in bugzilla (npajkovs@redhat.com)
- abrt-hook-python: sanitize input more; log to syslog (vda.linux@googlemail.com)
- Fixed /var/cache/abrt/ permissions (kklic@redhat.com)
- Kerneloops: we require commandline for every crash, save dummy one for oopses (vda.linux@googlemail.com)
- *: remove nss dependencies (vda.linux@googlemail.com)
- CCpp: use our own sha1 implementation (less pain with nss libs) (vda.linux@googlemail.com)
- DebugDump: more consistent logic in setting mode and uid:gid on dump dir (vda.linux@googlemail.com)
- fixes based on security review (vda.linux@googlemail.com)
- SOSreport/TicketUploader: use more restrictive file modes (vda.linux@googlemail.com)
- abrt-hook-python: add input sanitization and directory size guard (vda.linux@googlemail.com)
- RunApp: safer chdir. Overhauled "sparn a child and get its output" in general (vda.linux@googlemail.com)
- DebugDump: use more restrictive modes (vda.linux@googlemail.com)
- SQLite3: check for SQL injection (vda.linux@googlemail.com)
- replace plugin enabling via EnabledPlugins by par-plugin Enabled = yes/no (vda.linux@googlemail.com)
- abrt.spec: move "requires: gdb" to abrt-desktop (vda.linux@googlemail.com)
- ccpp: add a possibility to disable backtrace generation (vda.linux@googlemail.com)
- abrtd: limit the number of frames in backtrace to 3000 (vda.linux@googlemail.com)

* Tue Jan  5 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.3-1
- speed optimalization of abrt-debuginfo-install (jmoskovc@redhat.com)
- updated credits (jmoskovc@redhat.com)
- GUI: fixed crash when abrt-gui is run without X server rhbz#552039 (jmoskovc@redhat.com)
- abrt-backtrace manpage installed (kklic@redhat.com)
- cmdline and daemon checking is done by abrt-python-hook (kklic@redhat.com)
- moved get_cmdline() and daemon_is_ok() to abrtlib (kklic@redhat.com)
- large file support for whole abrt (kklic@redhat.com)
- made s_signal_caught volatile (vda.linux@googlemail.com)
- abrt-debuginfo-install: fixes for runs w/o cachedir (vda.linux@googlemail.com)
- remove unsafe log() from signal handler (vda.linux@googlemail.com)
- src/Hooks/CCpp.cpp: use and honour 'c' (core limit size). (vda.linux@googlemail.com)
- lib/Plugins/CCpp.cpp: save gdb error messages too (vda.linux@googlemail.com)
- prevent destructors from throwing exceptions; check curl_easy_init errors (vda.linux@googlemail.com)
- don't blame python for every crash in /usr/bin/python rhbz#533521 trac#109 (jmoskovc@redhat.com)
- GUI: autoscroll log window (jmoskovc@redhat.com)
- Kerneloops.conf: better comments (vda.linux@googlemail.com)
- applet: reduce blinking time to 30 seconds (vda.linux@googlemail.com)
- add paranoia checks on setuid/setgid (vda.linux@googlemail.com)
- more "obviously correct" code for secure opening of /dev/null (vda.linux@googlemail.com)
- get rid of ugly sleep call inside while() (vda.linux@googlemail.com)

* Mon Dec 14 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.2-1
- disabled GPG check again (jmoskovc@redhat.com)
- abrt-pyhook-helper rename (vda.linux@googlemail.com)
- abrt-cli: report success/failure of reporting. closes bug 71 (vda.linux@googlemail.com)
- less logging (vda.linux@googlemail.com)
- mkde abrt-gui --help and --version behave as expected. closes bug 85 (vda.linux@googlemail.com)
- dbus lib: fix parsing of 0-element arrays. Fixes bug 95 (vda.linux@googlemail.com)
- make "abrt-cli --delete randomuuid" report that deletion failed. closes bug 59 (vda.linux@googlemail.com)
- applet: make animation stop after 1 minute. (closes bug 108) (vda.linux@googlemail.com)
- show comment and how to reproduce fields, when BT rating > 3 (jmoskovc@redhat.com)
- Gui: make report status window's text wrap. Fixes bug 82 (vda.linux@googlemail.com)
- CCpp analyzer: added "info sharedlib" (https://fedorahosted.org/abrt/ticket/90) (vda.linux@googlemail.com)
- added link to bugzilla new account page to Bugzilla config dialog (jmoskovc@redhat.com)
- GUI: added log window (jmoskovc@redhat.com)

* Tue Dec  8 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.1-1
- PyHook: better logic for checking if abrtd is running rhbz#539987 (jmoskovc@redhat.com)
- re-enabled gpg sign checking (jmoskovc@redhat.com)
- PyHook: use repr() for displaying variables rhbz#545070 (jmoskovc@redhat.com)
- kerneloops: fix the linux kernel version identification (aarapov@redhat.com)
- gui review (rrakus@redhat.com)
- when we trim the dir, we must delete it from DB too rhbz#541854 (vda.linux@googlemail.com)
- improved dupe checking (kklic@redhat.com)
- GUI: handle cases when gui fails to start daemon on demand rhbz#543725 (jmoskovc@redhat.com)
- Add abrt group only if it is missing; fixes rhbz#543250 (kklic@redhat.com)
- GUI: more string fixes rhbz#543266 (jmoskovc@redhat.com)
- abrt.spec: straighten out relations between abrt-desktop and abrt-gui (vda.linux@googlemail.com)
- refuse to start if some required plugins are missing rhbz#518422 (vda.linux@googlemail.com)
- GUI: survive gnome-keyring access denial rhbz#543200 (jmoskovc@redhat.com)
- typo fixes rhbz#543266 (jmoskovc@redhat.com)
- abrt-debuginfo-install: better fix for incorrect passing double quotes (vda.linux@googlemail.com)
- APPLET: stop animation when it's not needed rhbz#542157 (jmoskovc@redhat.com)
- ccpp hook: reanme it, and add "crash storm protection" (see rhbz#542003) (vda.linux@googlemail.com)
- Hooks/CCpp.cpp: add MakeCompatCore = yes/no directive. Fixes rhbz#541707 (vda.linux@googlemail.com)
- SPEC: removed sqlite3 package, fixed some update problems (jmoskovc@redhat.com)
- Kerneloops are reported automaticky now when AutoReportUIDs = root is in Kerneloops.conf (npajkovs@redhat.com)
- remove word 'detected' from description rhbz#541459 (vda.linux@googlemail.com)
- src/Hooks/CCpp.cpp: do save abrtd's own coredumps, but carefully... (vda.linux@googlemail.com)
- CCpp.cpp: quote parameters if needed rhbz#540164 (vda.linux@googlemail.com)

* Fri Nov 20 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.0-1
- new version
- comment input wraps words rhbz#531276
- fixed hiding password dialog rhbz#529583
- easier kerneloops reporting rhbz#528395
- made menu entry translatable rhbz#536878 (jmoskovc@redhat.com)
- GUI: don't read the g-k every time we want to use the setting (jmoskovc@redhat.com)
- GUI: survive if g-k access is denied rhbz#534171 (jmoskovc@redhat.com)
- include more info into oops (we were losing the stack dump) (vda.linux@googlemail.com)
- make BZ insert small text attachments inline; move text file detection code (vda.linux@googlemail.com)
- GUI: fixed text wrapping in comment field rhbz#531276 (jmoskovc@redhat.com)
- GUI: added cancel to send dialog rhbz#537238 (jmoskovc@redhat.com)
- include abrt version in bug descriptions (vda.linux@googlemail.com)
- ccpp hook: implemented ReadonlyLocalDebugInfoDirs directive (vda.linux@googlemail.com)
- GUI: added window icon rhbz#537240 (jmoskovc@redhat.com)
- add support for \" escaping in config file (vda.linux@googlemail.com)
- add experimental saving of /var/log/Xorg*.log for X crashes (vda.linux@googlemail.com)
- APPLET: changed icon from default gtk-warning to abrt specific, add animation (jmoskovc@redhat.com)
- don't show icon on abrtd start/stop rhbz#537630 (jmoskovc@redhat.com)
- /var/cache/abrt permissions 1775 -> 0775 in spec file (kklic@redhat.com)
- Daemon properly checks /var/cache/abrt attributes (kklic@redhat.com)
- abrt user group; used by abrt-pyhook-helper (kklic@redhat.com)
- pyhook-helper: uid taken from system instead of command line (kklic@redhat.com)
- KerneloopsSysLog: fix breakage in code which detects abrt marker (vda.linux@googlemail.com)
- GUI: added support for backtrace rating (jmoskovc@redhat.com)
- InformAllUsers support. enabled by default for Kerneloops. Tested wuth CCpp. (vda.linux@googlemail.com)
- abrtd: call res_init() if /etc/resolv.conf or friends were changed rhbz#533589 (vda.linux@googlemail.com)
- supress errors in python hook to not colide with the running script (jmoskovc@redhat.com)

* Tue Nov 10 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.11-2
- spec file fixes

* Mon Nov  2 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.11-1
- re-enabled kerneloops
- abrt-debuginfo-install: download packages one-by-one - better logging (vda.linux@googlemail.com)
- do not report empty fields (vda.linux@googlemail.com)
- Added abrt.png, fixed rhbz#531181 (jmoskovc@redhat.com)
- added option DebugInfoCacheMB to limit size of unpacked debuginfos (vda.linux@googlemail.com)
- fixed the problem with overwriting the default plugin settings (jmoskovc@redhat.com)
- disabled kerneloops in config file (jmoskovc@redhat.com)
- added dependency to gdb >= 7.0 (jmoskovc@redhat.com)
- better format of report text (vda.linux@googlemail.com)
- Python backtrace size limited to 1 MB (kklic@redhat.com)
- lib/Plugins/Bugzilla: better message at login failure (vda.linux@googlemail.com)
- build fixes, added plugin-logger to abrt-desktop (jmoskovc@redhat.com)
- blacklisted nspluginwrapper, because it causes too many useless reports (jmoskovc@redhat.com)
- GUI: Wrong settings window is not shown behind the reporter dialog rhbz#531119 (jmoskovc@redhat.com)
- Normal user can see kerneloops and report it Bugzilla memory leaks fix (npajkovs@redhat.com)
- dumpoops: add -s option to dump results to stdout (vda.linux@googlemail.com)
- removed kerneloops from abrt-desktop rhbz#528395 (jmoskovc@redhat.com)
- GUI: fixed exception when enabling plugin rhbz#530495 (jmoskovc@redhat.com)
- Improved abrt-cli (kklic@redhat.com)
- Added backtrace rating to CCpp analyzer (dnovotny@redhat.com)
- GUI improvements (jmoskovc@redhat.com)
- Added abrt-pyhook-helper (kklic@redhat.com)

* Thu Oct 15 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.10-1
- new version
- added more logging (vda.linux@googlemail.com)
- made polkit policy to be more permissive when installing debuginfo (jmoskovc@redhat.com)
- lib/Plugins/CCpp.cpp: add build-ids to backtrace (vda.linux@googlemail.com)
- lib/Plugins/CCpp.cpp: do not use temp file for gdb commands - use -ex CMD instead (vda.linux@googlemail.com)
- GUI: added refresh button, added sanity check to plugin settings (jmoskovc@redhat.com)
- Initial man page for abrt-cli (kklic@redhat.com)
- Added --version, -V, --help, -? options. Fixed crash caused by unknown option. (kklic@redhat.com)
- Date/time honors current system locale (kklic@redhat.com)
- fixed saving/reading user config (jmoskovc@redhat.com)
- SPEC: added gnome-python2-gnomekeyring to requirements (jmoskovc@redhat.com)
- GUI: call Report() with the latest pluginsettings (jmoskovc@redhat.com)
- Fix Bug 526220 -  [abrt] crash detected in abrt-gui-0.0.9-2.fc12 (vda.linux@googlemail.com)
- removed unsecure reading/writting from ~HOME directory rhbz#522878 (jmoskovc@redhat.com)
- error checking added to archive creation (danny@rawhide.localdomain)
- try using pk-debuginfo-install before falling back to debuginfo-install (vda.linux@googlemail.com)
- abrt-gui: make "report" toolbar button work even if abrtd is not running (vda.linux@googlemail.com)
- set LIMIT_MESSAGE to 16k, typo fix and daemon now reads config information from dbus (npajkovs@redhat.com)
- add support for abrtd autostart (vda.linux@googlemail.com)
- GUI: reversed the dumplist, so the latest crashes are at the top (jmoskovc@redhat.com)
- rewrite FileTransfer to use library calls instead of commandline calls for compression (dnovotny@redhat.com)
- and many minor fixes ..

* Wed Sep 23 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.9-2
- added bug-buddy to provides rhbz#524934

* Tue Sep 22 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.9-1
- new version
- comments and how to reproduce are stored now (npajkovs@redhat.com)
- reduce verbosity a bit (vda.linux@googlemail.com)
- GUI: fixed word wrap in Comment field rhbz#524349 (jmoskovc@redhat.com)
- remove last vestives of dbus-c++ from build system (vda.linux@googlemail.com)
- GUI: added popup menu, fixed behaviour when run with root privs (jmoskovc@redhat.com)
- add dbus signalization when quota exceeded (npajkovs@redhat.com)
- Added cleaning of attachment variable, so there should not be mixed attachmetn anymore. (zprikryl@redhat.com)
- fixed closing of debug dump in case of existing backtrace (zprikryl@redhat.com)
- remove C++ dbus glue in src/CLI; fix a bug in --report (vda.linux@googlemail.com)
- new polkit action for installing debuginfo, default "yes" (danny@rawhide.localdomain)
- Polkit moved to Utils (can be used both in daemon and plugins) (danny@rawhide.localdomain)
- oops... remove stray trailing '\' (vda.linux@googlemail.com)
- GUI: added missing tooltips (jmoskovc@redhat.com)
- PYHOOK: ignore KeyboardInterrupt exception (jmoskovc@redhat.com)
- added ticket uploader plugin (gavin@redhat.com) (zprikryl@redhat.com)
- GUI: added UI for global settings (just preview, not usable!) (jmoskovc@redhat.com)
- Add checker if bugzilla login and password are filled in. (npajkovs@redhat.com)
- Add new config option InstallDebuginfo into CCpp.conf (npajkovs@redhat.com)
- translation updates
- many other fixes

* Fri Sep  4 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.8.5-1
- new version
- APPLET: added about dialog, removed popup, if icon is not visible, fixed (trac#43) (jmoskovc@redhat.com)
- renamed abrt to abrtd, few minor spec file fixes (jmoskovc@redhat.com)
- Made abrt service start by deafult (jmoskovc@redhat.com)
- add gettext support for all plugins (npajkovs@redhat.com)
- APPLET: removed the warning bubble about not running abrt service (walters)
- APPLET: changed tooltip rhbz#520293 (jmoskovc@redhat.com)
- CommLayerServerDBus: rewrote to use dbus, not dbus-c++ (vda.linux@googlemail.com)
- fixed timeout on boot causing [ FAILED ] message (vda.linux@googlemail.com)
- and many other fixes

* Wed Sep 02 2009  Colin Walters <watlers@verbum.org> 0.0.8-2
- Change Conflicts: kerneloops to be an Obsoletes so we do the right thing
  on upgrades.  Also add an Obsoletes: bug-buddy.

* Wed Aug 26 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.8-1
- new version
- resolved: Bug 518420 -  ordinary user's abrt-applet shows up for root owned crashes (npajkovs)
- GUI: added support for gettext (+part of czech translation) (jmoskovc)
- added support for saving settings (zprikryl)
- fixed conf: comment in the middle of the line isn't supported anymore (zprikryl)
- BZ#518413 PATCH ... furious kerneloops reporting (aarapov)
- GUI: added first part of support for gettext (jmoskovc)
- add new parameter to FileTransfer plugin (dnovotny)
- added support for updating abrt's table (zprikryl)
- added check for cc-list and reporter. +1 is created iff reporter is somebody else and current user isn't in cc list. (zprikryl)
- GUI: few improvements, to be more userfriendly (jmoskovc)
- LOGGER: return valid uri of the log file on succes (jmoskovc)
- GUI: bring the GUI up to front instead of just blinking in taskbar (trac#60, rhbz#512390) (jmoskovc)
- Try to execute $bindir/abrt-gui, then fall back to $PATH search. Closes bug 65 (vda.linux)
- APPLET: added popup menu (trac#37, rhbz#518386) (jmoskovc)
- Improved report results (zprikryl)
- Fixed sigsegv (#rhbz 518609) (zprikryl)
- GUI: removed dependency on libsexy if gtk2 >= 2.17 (jmoskovc)
- fixed signature check (zprikryl)
- KerneloopsSysLog: check line length to be >= 4 before looking for "Abrt" (vda.linux)
- Comment cannot start in the middle of the line. Comment has to start by Char # (first char in the line) (zprikryl)
- command mailx isn't run under root anymore. (zprikryl)
- GUI: added horizontal scrolling to report window (jmoskovc)
- GUI: added clickable link to "after report" status window (jmoskovc)
- added default values for abrt daemon (zprikryl)
- Plugins/CCpp: remove trailing \n from debuginfo-install's output (vda.linux)
- explain EnableGPGCheck option better (vda.linux)
- mailx: correct English (vda.linux)
- Bugzilla.conf: correct English (vda.linux)
- GUI: nicer after report message (jmoskovc)
- BZ plugin: removed /xmlrpc.cgi from config, made the report message more user friendly (jmoskovc)
- CCpp plugin: do not abort if debuginfos aren't found (vda.linux)
- abrt.spec: bump version to 0.0.7-2 (vda.linux)
- mailx removed dangerous parameter option (zprikryl)
- minimum timeout is 1 second (zprikryl)
- in case of plugin error, don't delete debug dumps (zprikryl)
- abrt-gui: fix crash when run by root (vda.linux)
- and lot more in git log ...

* Thu Aug 20 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.7.2-1
- new version
- fixed some bugs found during test day

* Wed Aug 19 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.7.1-1
- fixes to bugzilla plugin and gui to make the report message more user-friendly

* Tue Aug 18 2009  Denys Vlasenko <dvlasenk@redhat.com> 0.0.7-2
- removed dangerous parameter option
- minimum plugin activation period is 1 second
- in case of plugin error, don't delete debug dumps
- abrt-gui: fix crash when run by root
- simplify parsing of debuginfo-install output

* Tue Aug 18 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.7-1
- new version
- added status window to show user some info after reporting a bug

* Mon Aug 17 2009  Denys Vlasenko <dvlasenk@redhat.com> 0.0.6-1
- new version
- many fixes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.4-3
- fixed dependencies in spec file

* Tue Jun 16 2009 Daniel Novotny <dnovotny@redhat.com> 0.0.4-2
- added manual pages (also for plugins)

* Mon Jun 15 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.4-1
- new version
- added cli (only supports sockets)
- added python hook
- many fixes

* Fri Apr 10 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.3-1
- new version
- added bz plugin
- minor fix in reporter gui
- Configurable max size of debugdump storage rhbz#490889
- Wrap lines in report to keep the window sane sized
- Fixed gui for new daemon API
- removed unneeded code
- removed dependency on args
- new guuid hash creating
- fixed local UUID
- fixed debuginfo-install checks
- renamed MW library
- Added notification thru libnotify
- fixed parsing settings of action plugins
- added support for action plugins
- kerneloops - plugin: fail gracefully.
- Added commlayer to make dbus optional
- a lot of kerneloops fixes
- new approach for getting debuginfos and backtraces
- fixed unlocking of a debugdump
- replaced language and application plugins by analyzer plugin
- more excetpion handling
- conf file isn't needed
- Plugin's configuration file is optional
- Add curl dependency
- Added column 'user' to the gui
- Gui: set the newest entry as active (ticket#23)
- Delete and Report button are no longer active if no entry is selected (ticket#41)
- Gui refreshes silently (ticket#36)
- Added error reporting over dbus to daemon, error handling in gui, about dialog

* Wed Mar 11 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.2-1
- added kerneloops addon to rpm (aarapov)
- added kerneloops addon and plugin (aarapov)
- Made Crash() private
- Applet requires gui, removed dbus-glib deps
- Closing stdout in daemon rhbz#489622
- Changed applet behaviour according to rhbz#489624
- Changed gui according to rhbz#489624, fixed dbus timeouts
- Increased timeout for async dbus calls to 60sec
- deps cleanup, signal AnalyzeComplete has the crashreport as an argument.
- Fixed empty package Description.
- Fixed problem with applet tooltip on x86_64

* Wed Mar  4 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-13
- More renaming issues fixed..
- Changed BR from gtkmm24 to gtk2
- Fixed saving of user comment
- Added a progress bar, new Comment entry for user comments..
- FILENAME_CMDLINE and FILENAME_RELEASE are optional
- new default path to DB
- Rename to abrt

* Tue Mar  3 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-12
- initial fedora release
- changed SOURCE url
- added desktop-file-utils to BR
- changed crash-catcher to %%{name}

* Mon Mar  2 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-11
- more spec file fixes according to review
- async dbus method calls, added exception handler
- avoid deadlocks (zprikryl)
- root is god (zprikryl)
- create bt only once (zprikryl)

* Sat Feb 28 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-10
- New gui
- Added new method DeleteDebugDump to daemon
- Removed gcc warnings from applet
- Rewritten CCpp hook and removed dealock in DebugDumps lib (zprikryl)
- fixed few gcc warnings
- DBusBackend improvements

* Fri Feb 27 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-9
- fixed few gcc warnings
- added scrolled window for long reports

* Thu Feb 26 2009 Adam Williamson <awilliam@redhat.com> 0.0.1-8
- fixes for all issues identified in review

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-7
- Fixed cancel button behaviour in reporter
- disabled core file sending
- removed some debug messages

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-6
- fixed DB path
- added new signals to handler
- gui should survive the dbus timeout

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-5
- fixed catching debuinfo install exceptions
- some gui fixes
- added check for GPGP public key

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-4
- changed from full bt to simple bt

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-3
- spec file cleanups
- changed default paths to crash DB and log DB
- fixed some memory leaks

* Tue Feb 24 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-2
- spec cleanup
- added new subpackage gui

* Wed Feb 18 2009 Zdenek Prikryl <zprikryl@redhat.com> 0.0.1-1
- initial packing
