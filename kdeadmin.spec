Name: kdeadmin
Summary: KDE Administrative tools
Epoch: 7
Version: 4.3.4
Release: 4%{?dist}

Group: User Interface/Desktops
License: GPLv2
URL: http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1: kuser.pam
Source2: kuser.pamd

# drop BR on PyQt
Patch0: kdeadmin-4.2.85-printing.patch

# upstream patches
Patch100: kdeadmin-4.3.5.patch

BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: python-devel

Requires: kdelibs4 >= %{version}
Requires: kdepimlibs >= %{version}

%description
The %{name} package includes administrative tools including:
* kcron: systemsettings module for the cron task scheduler
* knetworkconf: systemsettings module for network settings
* ksystemlog: system log viewer
* kuser: user manager

%prep
%setup -q

%patch0 -p1 -b .printing

# upstream patches
%patch100 -p1 -b .kde435

%build

# disable system-config-printer for rhel, use system-config-printer
sed -i -e 's:macro_optional_add_subdirectory(system-config-printer-kde):#macro_optional_add_subdirectory(system-config-printer-kde):g' CMakeLists.txt

# disable kpackage in rhel
sed -i -e 's:macro_optional_add_subdirectory(kpackage):#macro_optional_add_subdirectory(kpackage):g' CMakeLists.txt
sed -i -e 's:add_subdirectory(kpackage):#add_subdirectory(kpackage):g' doc/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# remove broken .pc file which has no business to be in a non-devel pkg anyway
rm -rf %{buildroot}%{_libdir}/pkgconfig


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_kde4_bindir}/ksystemlog
%{_kde4_bindir}/kuser
%{_kde4_appsdir}/knetworkconf/
%{_kde4_appsdir}/ksystemlog/
%{_kde4_appsdir}/kuser/
%{_kde4_datadir}/applications/kde4/kuser.desktop
%{_kde4_datadir}/applications/kde4/ksystemlog.desktop
%{_kde4_datadir}/config.kcfg/kuser.kcfg
%{_kde4_datadir}/kde4/services/kcm_cron.desktop
%{_kde4_datadir}/kde4/services/kcm_knetworkconfmodule.desktop
%{_kde4_docdir}/HTML/en/kcontrol/
%{_kde4_docdir}/HTML/en/kcron/
%{_kde4_docdir}/HTML/en/ksystemlog/
%{_kde4_docdir}/HTML/en/kuser/
%{_kde4_iconsdir}/hicolor/*/*/knetworkconf.*
%{_kde4_iconsdir}/hicolor/*/*/kuser.*
%{_kde4_iconsdir}/hicolor/*/*/network*
%{_kde4_libdir}/kde4/kcm_cron.so
%{_kde4_libdir}/kde4/kcm_knetworkconfmodule.so

%changelog
* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 4.3.4-4
- rebuilt against qt 4.6.2

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 4.3.4-3
- update translation

* Fri Dec 04 2009 Than Ngo <than@redhat.com> - 4.3.4-2
- fix rhel conditionals

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.3-1
- 4.3.3

* Sun Oct 04 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Tue Jul 28 2009 Than Ngo <than@redhat.com> - 4.2.98-5
- don't include kpackage fo rhel

* Mon Jul 27 2009 Than Ngo <than@redhat.com> - 4.2.98-4
- don't include system_config_printer_kde for rhel

* Mon Jul 27 2009 Than Ngo <than@redhat.com> - 4.2.98-3
- fix knetworkconf backend to recognize fedora network settings

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:4.2.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 09 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 04 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 7:4.2.90-1
- KDE 4.3 Beta 2

* Wed May 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-2
- reenable sytem-config-printer-kde
- rebase printing patch, drop hunks fixed upstream
- BR python-devel instead of just python
- fix file list, system-config-printer-kde is now a System Settings module

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Tue Apr 21 2009 Than Ngo <than@redhat.com> - 4.2.2-4
- get rid of the dependency of system-config-printer
- drop the BR on PyKDE4, system-config-printer-libs
  it's just needed for runtime

* Mon Apr 20 2009 Than Ngo <than@redhat.com> - 4.2.2-3
- fix #496646, system-config-printer-kde doesn't start

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.2-2
- optimize scriptlets

* Mon Mar 30 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Wed Jan 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.1.96-2
- include system-config-printer-kde

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Thu Dec 11 2008 Than Ngo <than@redhat.com> -  4.1.85-1
- 4.2beta2

* Thu Dec 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-4
- rebuild for fixed kde-filesystem (macros.kde4) (get rid of rpaths)

* Thu Dec 04 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.80-3
- drop Requires: kdebase-workspace

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- get rid of duplicated BRs

* Wed Nov 19 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 7:4.1.80-1
- 4.1.80
- BR cmake 2.6
- BR python-devel
- make install/fast

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Mon Oct 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-4
- make %%description for kcron, knetworkconf more clear (#467650)
- Requires: kdebase-workspace (for kcm modules)
- cleanup extraneous scriptlets

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-3
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- (re)add unpackaged HTML/en/kcontrol/ files

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Thu Jul 24 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-2
- remove broken .pc file (segfaults RPM, #456100), drop Requires: pkgconfig

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 7:4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72
- add files and description for ksystemlog
- kcron is now a KCM (update file list)
- remove secpolicy from file list and description (dropped upstream)

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 7:4.0.1-1
- 4.0.1
- don't use consolehelper for kuser (for now anyway, didn't work anyway)
- -kpackage scriptlet fixes

* Tue Jan 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 7:4.0.0-1
- update to 4.0.0

* Thu Dec 20 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 7:3.97.0-3
- don't run kpackage through consolehelper, it can elevate privileges on demand
  (see also #344751, though that bug appears not to have affected KDE 4)

* Thu Dec 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7:3.97.0-2
- cosmetics (drop extraneous BR's, touchup %%description)

* Thu Dec 06 2007 Than Ngo <than@redhat.com> 7:3.97.0-1
- 3.97.0

* Fri Nov 30 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.2-1
- kde-3.96.2

* Fri Nov 23 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.1-1
- kde-3.96.1
- also use epoch in changelog (also backwards)

* Thu Nov 22 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-7
- use consolehelper for kuser and kpackage

* Wed Nov 21 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-6
- put kpackage in a subpkg (for the smart requirement)

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-5
- BR: kde-filesystem >= 4

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-4
- BR: libXcomposite-devel
- BR: libXdamage-devel
- BR: libxkbfile-devel
- BR: libXpm-devel
- BR: libXv-devel
- BR: libXxf86misc-devel
- BR: libXtst-devel
- BR: libXScrnSaver-devel

* Fri Nov 16 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-3
- +BR: kde4-macros(api)

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-2
- included AUTHORS
- added %%post and %%postun
- BR: kde-filesystem

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 7:3.96.0-1
- Initial version for Fedora
