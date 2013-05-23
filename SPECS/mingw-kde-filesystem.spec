%{?mingw_package_header}

%global _basename kde-filesystem

# Not defined in /etc/rpm/macros.* yet...but will be after this package
# is installed
%global mingw32_kde4_prefix %mingw32_prefix
%global mingw32_kde4_sysconfdir %mingw32_sysconfdir
%global mingw32_kde4_libdir %mingw32_libdir
%global mingw32_kde4_libexecdir %mingw32_libexecdir/kde4
%global mingw32_kde4_datadir %mingw32_datadir
%global mingw32_kde4_sharedir %mingw32_datadir
%global mingw32_kde4_iconsdir %mingw32_kde4_sharedir/icons
%global mingw32_kde4_configdir %mingw32_kde4_sharedir/config
%global mingw32_kde4_appsdir %mingw32_kde4_sharedir/kde4/apps
%global mingw32_kde4_docdir %mingw32_kde4_prefix/share/doc
%global mingw32_kde4_bindir %mingw32_kde4_prefix/bin
%global mingw32_kde4_sbindir %mingw32_kde4_prefix/sbin
%global mingw32_kde4_includedir %mingw32_kde4_prefix/include/kde4
%global mingw32_kde4_buildtype release
%global mingw32_kde4_macros_api 2

%global mingw64_kde4_prefix %mingw64_prefix
%global mingw64_kde4_sysconfdir %mingw64_sysconfdir
%global mingw64_kde4_libdir %mingw64_libdir
%global mingw64_kde4_libexecdir %mingw64_libexecdir/kde4
%global mingw64_kde4_datadir %mingw64_datadir
%global mingw64_kde4_sharedir %mingw64_datadir
%global mingw64_kde4_iconsdir %mingw64_kde4_sharedir/icons
%global mingw64_kde4_configdir %mingw64_kde4_sharedir/config
%global mingw64_kde4_appsdir %mingw64_kde4_sharedir/kde4/apps
%global mingw64_kde4_docdir %mingw64_kde4_prefix/share/doc
%global mingw64_kde4_bindir %mingw64_kde4_prefix/bin
%global mingw64_kde4_sbindir %mingw64_kde4_prefix/sbin
%global mingw64_kde4_includedir %mingw64_kde4_prefix/include/kde4
%global mingw64_kde4_buildtype release
%global mingw64_kde4_macros_api 2

Summary: KDE filesystem layout
Name: mingw-%{_basename}
Version: 4
Release: 42%{?dist}

Group: System Environment/Base
License: Public Domain

# noarch->arch transition
Obsoletes: mingw32-%{_basename} < 4-36
Obsoletes: mingw64-%{_basename} < 4-36

# teamnames (locales) borrowed from kde-i18n packaging
Source1: teamnames

Source2: macros.kde4
# increment whenever dirs change in an incompatible way
# kde4 apps built using macros.kde4 should

Source3: applnk-hidden-directory

Provides: kde4-macros(api) = %{_kde4_macros_api} 

Requires:  rpm

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils

%description
This package provides some directories that are required/used by KDE. 


%package -n mingw32-%{_basename}
Summary: KDE filesystem layout
%description -n mingw32-%{_basename}
This package provides some directories that are required/used by KDE. 
This is the MinGW version, built for the win32 target.


%package -n mingw64-%{_basename}
Summary: KDE filesystem layout
%description -n mingw64-%{_basename}
This package provides some directories that are required/used by KDE. 
This is the MinGW version, built for the win32 target.


%{?mingw_debug_package}


%prep


%build


%install
rm -f $RPM_BUILD_DIR/%{name}-win32.list
rm -f $RPM_BUILD_DIR/%{name}-win64.list
rm -rf $RPM_BUILD_ROOT

#
# Win32
#

## KDE3 
mkdir -p $RPM_BUILD_ROOT%{mingw32_sysconfdir}/kde/{env,shutdown,kdm}
mkdir -p $RPM_BUILD_ROOT%{mingw32_datadir}/{applications/kde,applnk,apps,autostart,config,config.kcfg,emoticons,mimelnk,services,servicetypes,templates,source}
mkdir -p $RPM_BUILD_ROOT%{mingw32_datadir}/apps/konqueror/servicemenus
# not sure who best should own locolor, so we'll included it here, for now. -- Rex
mkdir -p $RPM_BUILD_ROOT%{mingw32_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes}
mkdir -p $RPM_BUILD_ROOT%{mingw32_datadir}/applnk/{.hidden,Applications,Edutainment,Graphics,Internet,Settings,System,Toys,Utilities}
mkdir -p $RPM_BUILD_ROOT%{mingw32_datadir}/mimelnk/{all,application,audio,fonts,image,inode,interface,media,message,model,multipart,print,text,uri,video}
# do qt3 too?
# mkdir -p $RPM_BUILD_ROOT%{mingw32_prefix}/{lib,%{_lib}}/qt-3.3/plugins
mkdir -p $RPM_BUILD_ROOT%{mingw32_prefix}/{lib,%{_lib}}/kde3/plugins
mkdir -p $RPM_BUILD_ROOT%{mingw32_docdir}/HTML/en

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
 mkdir -p $RPM_BUILD_ROOT%{mingw32_docdir}/HTML/${locale}/common
 # do docs/common too, but it could be argued that apps/pkgs using or
 # depending on is a bug -- Rex
 mkdir -p $RPM_BUILD_ROOT%{mingw32_docdir}/HTML/${locale}/docs/
 ln -s ../common $RPM_BUILD_ROOT%{mingw32_docdir}/HTML/${locale}/docs/common
 echo "%lang($locale) %{mingw32_docdir}/HTML/$locale/" >> %{name}-win32.list
done

# internal services shouldn't be displayed in menu
install -p -m644 -D %{SOURCE3} $RPM_BUILD_ROOT%{mingw32_datadir}/applnk/.hidden/.directory

## KDE4
mkdir -p $RPM_BUILD_ROOT%{mingw32_sysconfdir}/rpm \
         $RPM_BUILD_ROOT%{mingw32_kde4_sysconfdir}/kde/{env,shutdown,kdm} \
         $RPM_BUILD_ROOT%{mingw32_kde4_includedir} \
         $RPM_BUILD_ROOT%{mingw32_kde4_libexecdir} \
         $RPM_BUILD_ROOT%{mingw32_kde4_appsdir}/color-schemes \
         $RPM_BUILD_ROOT%{mingw32_kde4_datadir}/applications/kde4 \
         $RPM_BUILD_ROOT%{mingw32_kde4_datadir}/{autostart,wallpapers} \
         $RPM_BUILD_ROOT%{mingw32_kde4_configdir} \
         $RPM_BUILD_ROOT%{mingw32_kde4_sharedir}/config.kcfg \
         $RPM_BUILD_ROOT%{mingw32_kde4_sharedir}/emoticons \
         $RPM_BUILD_ROOT%{mingw32_kde4_sharedir}/kde4/services/ServiceMenus \
         $RPM_BUILD_ROOT%{mingw32_kde4_sharedir}/kde4/servicetypes \
         $RPM_BUILD_ROOT%{mingw32_kde4_sharedir}/templates/.source \
         $RPM_BUILD_ROOT%{mingw32_kde4_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes} \
         $RPM_BUILD_ROOT%{mingw32_kde4_docdir}/HTML/en/common
# do qt4 too?
# mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/qt4/plugins
mkdir -p $RPM_BUILD_ROOT%{mingw32_kde4_prefix}/{lib,%{_lib}}/kde4/plugins/{gui_platform,styles}

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
  mkdir -p $RPM_BUILD_ROOT%{mingw32_kde4_docdir}/HTML/${locale}/common
  echo "%lang($locale) %{mingw32_kde4_docdir}/HTML/$locale/" >> %{name}-win32.list
done

# rpm macros
cat >$RPM_BUILD_ROOT%{mingw32_sysconfdir}/rpm/macros.kde4<<EOF
%%mingw32_kde4_prefix %%mingw32_prefix
%%mingw32_kde4_sysconfdir %%mingw32_sysconfdir
%%mingw32_kde4_libdir %%mingw32_libdir
%%mingw32_kde4_libexecdir %%mingw32_libexecdir/kde4
%%mingw32_kde4_datadir %%mingw32_datadir
%%mingw32_kde4_sharedir %%mingw32_datadir
%%mingw32_kde4_iconsdir %%mingw32_kde4_sharedir/icons
%%mingw32_kde4_configdir %%mingw32_kde4_sharedir/config
%%mingw32_kde4_appsdir %%mingw32_kde4_sharedir/kde4/apps
%%mingw32_kde4_docdir %mingw32_kde4_prefix/share/doc
%%mingw32_kde4_bindir %%mingw32_kde4_prefix/bin
%%mingw32_kde4_sbindir %%mingw32_kde4_prefix/sbin
%%mingw32_kde4_includedir %%mingw32_kde4_prefix/include/kde4
%%mingw32_kde4_buildtype %mingw32_kde4_buildtype
%%mingw32_kde4_macros_api %mingw32_kde4_macros_api
EOF
sed "s/BT/32/g" < %{SOURCE2} >> $RPM_BUILD_ROOT%{mingw32_sysconfdir}/rpm/macros.kde4
install -pD -m644 $RPM_BUILD_ROOT%{mingw32_sysconfdir}/rpm/macros.kde4 \
	$RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.mingw32-kde4

#
# Win64
#

## KDE3 
mkdir -p $RPM_BUILD_ROOT%{mingw64_sysconfdir}/kde/{env,shutdown,kdm}
mkdir -p $RPM_BUILD_ROOT%{mingw64_datadir}/{applications/kde,applnk,apps,autostart,config,config.kcfg,emoticons,mimelnk,services,servicetypes,templates,source}
mkdir -p $RPM_BUILD_ROOT%{mingw64_datadir}/apps/konqueror/servicemenus
# not sure who best should own locolor, so we'll included it here, for now. -- Rex
mkdir -p $RPM_BUILD_ROOT%{mingw64_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes}
mkdir -p $RPM_BUILD_ROOT%{mingw64_datadir}/applnk/{.hidden,Applications,Edutainment,Graphics,Internet,Settings,System,Toys,Utilities}
mkdir -p $RPM_BUILD_ROOT%{mingw64_datadir}/mimelnk/{all,application,audio,fonts,image,inode,interface,media,message,model,multipart,print,text,uri,video}
# do qt3 too?
# mkdir -p $RPM_BUILD_ROOT%{mingw64_prefix}/{lib,%{_lib}}/qt-3.3/plugins
mkdir -p $RPM_BUILD_ROOT%{mingw64_prefix}/{lib,%{_lib}}/kde3/plugins
mkdir -p $RPM_BUILD_ROOT%{mingw64_docdir}/HTML/en

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
 mkdir -p $RPM_BUILD_ROOT%{mingw64_docdir}/HTML/${locale}/common
 # do docs/common too, but it could be argued that apps/pkgs using or
 # depending on is a bug -- Rex
 mkdir -p $RPM_BUILD_ROOT%{mingw64_docdir}/HTML/${locale}/docs/
 ln -s ../common $RPM_BUILD_ROOT%{mingw64_docdir}/HTML/${locale}/docs/common
 echo "%lang($locale) %{mingw64_docdir}/HTML/$locale/" >> %{name}-win64.list
done

# internal services shouldn't be displayed in menu
install -p -m644 -D %{SOURCE3} $RPM_BUILD_ROOT%{mingw64_datadir}/applnk/.hidden/.directory

## KDE4
mkdir -p $RPM_BUILD_ROOT%{mingw64_sysconfdir}/rpm \
         $RPM_BUILD_ROOT%{mingw64_kde4_sysconfdir}/kde/{env,shutdown,kdm} \
         $RPM_BUILD_ROOT%{mingw64_kde4_includedir} \
         $RPM_BUILD_ROOT%{mingw64_kde4_libexecdir} \
         $RPM_BUILD_ROOT%{mingw64_kde4_appsdir}/color-schemes \
         $RPM_BUILD_ROOT%{mingw64_kde4_datadir}/applications/kde4 \
         $RPM_BUILD_ROOT%{mingw64_kde4_datadir}/{autostart,wallpapers} \
         $RPM_BUILD_ROOT%{mingw64_kde4_configdir} \
         $RPM_BUILD_ROOT%{mingw64_kde4_sharedir}/config.kcfg \
         $RPM_BUILD_ROOT%{mingw64_kde4_sharedir}/emoticons \
         $RPM_BUILD_ROOT%{mingw64_kde4_sharedir}/kde4/services/ServiceMenus \
         $RPM_BUILD_ROOT%{mingw64_kde4_sharedir}/kde4/servicetypes \
         $RPM_BUILD_ROOT%{mingw64_kde4_sharedir}/templates/.source \
         $RPM_BUILD_ROOT%{mingw64_kde4_datadir}/icons/locolor/{16x16,22x22,32x32,48x48}/{actions,apps,mimetypes} \
         $RPM_BUILD_ROOT%{mingw64_kde4_docdir}/HTML/en/common
# do qt4 too?
# mkdir -p $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}/qt4/plugins
mkdir -p $RPM_BUILD_ROOT%{mingw64_kde4_prefix}/{lib,%{_lib}}/kde4/plugins/{gui_platform,styles}

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
  mkdir -p $RPM_BUILD_ROOT%{mingw64_kde4_docdir}/HTML/${locale}/common
  echo "%lang($locale) %{mingw64_kde4_docdir}/HTML/$locale/" >> %{name}-win64.list
done

# rpm macros
cat >$RPM_BUILD_ROOT%{mingw64_sysconfdir}/rpm/macros.kde4<<EOF
%%mingw64_kde4_prefix %%_prefix
%%mingw64_kde4_sysconfdir %%_sysconfdir
%%mingw64_kde4_libdir %%_libdir
%%mingw64_kde4_libexecdir %%_libexecdir/kde4
%%mingw64_kde4_datadir %%_datadir
%%mingw64_kde4_sharedir %%_datadir
%%mingw64_kde4_iconsdir %%mingw64_kde4_sharedir/icons
%%mingw64_kde4_configdir %%mingw64_kde4_sharedir/config
%%mingw64_kde4_appsdir %%mingw64_kde4_sharedir/kde4/apps
%%mingw64_kde4_docdir %mingw64_kde4_prefix/share/doc
%%mingw64_kde4_bindir %%mingw64_kde4_prefix/bin
%%mingw64_kde4_sbindir %%mingw64_kde4_prefix/sbin
%%mingw64_kde4_includedir %%mingw64_kde4_prefix/include/kde4
%%mingw64_kde4_buildtype %_kde4_buildtype
%%mingw64_kde4_macros_api %_kde4_macros_api
EOF
sed "s/BT/64/g" < %{SOURCE2} >> $RPM_BUILD_ROOT%{mingw64_sysconfdir}/rpm/macros.kde4
install -pD -m644 $RPM_BUILD_ROOT%{mingw64_sysconfdir}/rpm/macros.kde4 \
	$RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.mingw64-kde4

# Argh...WTF?  This hasn't happened with any other MinGW package...
cat < /dev/null > mingw32-debugfiles.list
cat < /dev/null > mingw64-debugfiles.list


%clean
rm -rf $RPM_BUILD_ROOT %{name}-win32.list %{name}-win64.list


%files -n mingw32-%{_basename} -f %{name}-win32.list
%defattr(-,root,root,-)

%config %{_sysconfdir}/rpm/macros.mingw32-kde4

# KDE3
%{mingw32_datadir}/applications/kde/
%{mingw32_datadir}/applnk/
%{mingw32_datadir}/apps/
%{mingw32_datadir}/autostart/
%{mingw32_datadir}/config/
%{mingw32_datadir}/config.kcfg/
%{mingw32_datadir}/emoticons/
%{mingw32_datadir}/icons/locolor
%{mingw32_datadir}/mimelnk/
%{mingw32_datadir}/services/
%{mingw32_datadir}/servicetypes/
%{mingw32_datadir}/templates/
%{mingw32_prefix}/lib/kde3/
%{mingw32_prefix}/%{_lib}/kde3/
%dir %{mingw32_docdir}/HTML/
%lang(en) %{mingw32_docdir}/HTML/en/

# KDE4
%config %{mingw32_sysconfdir}/rpm/macros.kde4
%{mingw32_kde4_sysconfdir}/kde/
%{mingw32_kde4_libexecdir}/
%{mingw32_kde4_includedir}/
%{mingw32_kde4_appsdir}/
%{mingw32_kde4_configdir}/
%{mingw32_kde4_sharedir}/config.kcfg/
%{mingw32_kde4_sharedir}/emoticons/
%{mingw32_kde4_sharedir}/kde4/
%{mingw32_kde4_sharedir}/templates/
%{mingw32_kde4_datadir}/applications/kde4/
%{mingw32_kde4_datadir}/autostart/
%{mingw32_kde4_datadir}/icons/locolor/
%{mingw32_kde4_datadir}/wallpapers/
%{mingw32_kde4_prefix}/lib/kde4/
%{mingw32_kde4_prefix}/%{_lib}/kde4/
%dir %{mingw32_kde4_docdir}/HTML/
%lang(en) %{mingw32_kde4_docdir}/HTML/en/


%files -n mingw64-%{_basename} -f %{name}-win64.list
%defattr(-,root,root,-)

%config %{_sysconfdir}/rpm/macros.mingw64-kde4

# KDE3
%{mingw64_datadir}/applications/kde/
%{mingw64_datadir}/applnk/
%{mingw64_datadir}/apps/
%{mingw64_datadir}/autostart/
%{mingw64_datadir}/config/
%{mingw64_datadir}/config.kcfg/
%{mingw64_datadir}/emoticons/
%{mingw64_datadir}/icons/locolor
%{mingw64_datadir}/mimelnk/
%{mingw64_datadir}/services/
%{mingw64_datadir}/servicetypes/
%{mingw64_datadir}/templates/
%{mingw64_prefix}/lib/kde3/
%{mingw64_prefix}/%{_lib}/kde3/
%dir %{mingw64_docdir}/HTML/
%lang(en) %{mingw64_docdir}/HTML/en/

# KDE4
%config %{mingw64_sysconfdir}/rpm/macros.kde4
%{mingw64_kde4_sysconfdir}/kde/
%{mingw64_kde4_libexecdir}/
%{mingw64_kde4_includedir}/
%{mingw64_kde4_appsdir}/
%{mingw64_kde4_configdir}/
%{mingw64_kde4_sharedir}/config.kcfg/
%{mingw64_kde4_sharedir}/emoticons/
%{mingw64_kde4_sharedir}/kde4/
%{mingw64_kde4_sharedir}/templates/
%{mingw64_kde4_datadir}/applications/kde4/
%{mingw64_kde4_datadir}/autostart/
%{mingw64_kde4_datadir}/icons/locolor/
%{mingw64_kde4_datadir}/wallpapers/
%{mingw64_kde4_prefix}/lib/kde4/
%{mingw64_kde4_prefix}/%{_lib}/kde4/
%dir %{mingw64_kde4_docdir}/HTML/
%lang(en) %{mingw64_kde4_docdir}/HTML/en/


%changelog
* Sat May 18 2013 Steven Boswell <ulatekh@yahoo.com> - 4-42
- Ported Fedora package to MinGW
