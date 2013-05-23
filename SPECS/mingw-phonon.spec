%{?mingw_package_header}

%global _basename phonon

# Not defined in /etc/rpm/macros.* yet
%global mingw32_qt4_plugindir %{mingw32_libdir}/qt4/plugins
%global mingw32_qt4_datadir %{mingw32_datadir}/qt4
%global mingw64_qt4_plugindir %{mingw64_libdir}/qt4/plugins
%global mingw64_qt4_datadir %{mingw64_datadir}/qt4

# enabling for the build sanity, the results
# aren't all that useful, yet.
%global phonon_build_tests -DPHONON_BUILD_TESTS:BOOL=ON

Summary: Multimedia framework api
Name:    mingw-%{_basename}
Version: 4.6.0
Release: 5%{?dist}
Group:   System Environment/Libraries
License: LGPLv2+
URL:     http://phonon.kde.org/
%if 0%{?snap}
Source0: %{_basename}-%{version}-%{snap}.tar.bz2
%else
Source0: ftp://ftp.kde.org/pub/kde/stable/phonon/%{version}/src/%{_basename}-%{version}.tar.xz
%endif

Patch0:  %{_basename}-%{version}-mingw.patch

## upstreamable patches
# phonon_backend ... could not be loaded
# http://bugzilla.redhat.com/760039
Patch50: phonon-4.5.57-plugindir.patch 
Patch51: phonon-4.6.0-syntax.patch
# https://git.reviewboard.kde.org/r/103423
Patch52: phonon-4.6.0-rpath.patch

## Upstream patches

BuildRequires: automoc4 >= 0.9.86
BuildRequires: cmake >= 2.6.0
BuildRequires: mingw32-kde-filesystem
BuildRequires: mingw64-kde-filesystem
BuildRequires: pkgconfig
BuildRequires: mingw32-glib2
BuildRequires: mingw64-glib2
#BuildRequires: pkgconfig(libpulse-mainloop-glib) > 0.9.15
BuildRequires: mingw32-libxml2
BuildRequires: mingw64-libxml2
BuildRequires: mingw32-qt >= 4.7.2
BuildRequires: mingw64-qt >= 4.7.2
#BuildRequires: pkgconfig(xcb)

%global pulseaudio_version %(pkg-config --modversion libpulse 2>/dev/null || echo 0.9.15)

## Beware bootstrapping, have -Requires/+Requires this for step 0, then build at least one backend
Requires: phonon-backend%{?_isa} => 4.4
#Provides: phonon-backend%{?_isa} = 4.4
#Requires: pulseaudio-libs%{?_isa} >= %{pulseaudio_version}
Requires: mingw32-qt >= %{_qt4_version}

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
%{summary}.


%package -n mingw32-%{_basename}
Summary: Multimedia framework API
Group:   Development/Libraries
Requires: mingw32-kde-filesystem
Requires: mingw32-qt
Requires: pkgconfig
%description -n mingw32-%{_basename}
The phonon multimedia framework API.
This is the MinGW version, built for the win32 target.


%package -n mingw64-%{_basename}
Summary: Multimedia framework API
Group:   Development/Libraries
Requires: mingw32-kde-filesystem
Requires: mingw64-qt
Requires: pkgconfig
%description -n mingw64-%{_basename}
The phonon multimedia framework API.
This is the MinGW version, built for the win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}-%{version}

%patch0 -p1
%patch50 -p1 -b .plugindir
%patch51 -p1 -b .syntax
%patch52 -p1 -b .rpath

%build
%{mingw_cmake} \
  %{?phonon_build_tests} \
  -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON \
  -DHOST_PREFIX_PATH:STRING="%{_bindir}" \
  -DHOST_PACKAGE_PATH:STRING="%{_libdir}/automoc4" \
  ..

%{mingw_make} %{?_smp_mflags}


%install
rm -rf %{buildroot}

%{mingw_make} install/fast DESTDIR=%{buildroot}

# symlink for qt/phonon compatibility
ln -s ../KDE/Phonon %{buildroot}%{mingw32_includedir}/phonon/Phonon
ln -s ../KDE/Phonon %{buildroot}%{mingw64_includedir}/phonon/Phonon

# own these dirs
mkdir -p %{buildroot}%{mingw32_kde4_libdir}/kde4/plugins/phonon_backend/
mkdir -p %{buildroot}%{mingw32_kde4_datadir}/kde4/services/phononbackends/
mkdir -p %{buildroot}%{mingw64_kde4_libdir}/kde4/plugins/phonon_backend/
mkdir -p %{buildroot}%{mingw64_kde4_datadir}/kde4/services/phononbackends/


%clean
rm -rf %{buildroot}


%files -n mingw32-%{_basename}
%defattr(-,root,root,-)
%doc COPYING.LIB
%{mingw32_bindir}/libphonon.dll
%{mingw32_bindir}/libphononexperimental.dll
%{mingw32_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%{mingw32_qt4_plugindir}/designer/libphononwidgets.dll
%dir %{mingw32_datadir}/phonon/
%dir %{mingw32_kde4_libdir}/kde4/plugins/phonon_backend/
%dir %{mingw32_kde4_datadir}/kde4/services/phononbackends/
%{mingw32_datadir}/phonon/buildsystem/
%dir %{mingw32_libdir}/cmake/
%{mingw32_libdir}/cmake/phonon/
%dir %{mingw32_includedir}/KDE
%{mingw32_includedir}/KDE/Phonon/
%{mingw32_includedir}/phonon/
%{mingw32_libdir}/pkgconfig/phonon.pc
%{mingw32_libdir}/libphonon.dll.a
%{mingw32_libdir}/libphononexperimental.dll.a
%{mingw32_qt4_datadir}/mkspecs/modules/qt_phonon.pri


%files -n mingw64-%{_basename}
%defattr(-,root,root,-)
%doc COPYING.LIB
%{mingw64_bindir}/libphonon.dll
%{mingw64_bindir}/libphononexperimental.dll
%{mingw64_datadir}/dbus-1/interfaces/org.kde.Phonon.AudioOutput.xml
%{mingw64_qt4_plugindir}/designer/libphononwidgets.dll
%dir %{mingw64_datadir}/phonon/
%dir %{mingw64_kde4_libdir}/kde4/plugins/phonon_backend/
%dir %{mingw64_kde4_datadir}/kde4/services/phononbackends/
%{mingw64_datadir}/phonon/buildsystem/
%dir %{mingw64_libdir}/cmake/
%{mingw64_libdir}/cmake/phonon/
%dir %{mingw64_includedir}/KDE
%{mingw64_includedir}/KDE/Phonon/
%{mingw64_includedir}/phonon/
%{mingw64_libdir}/pkgconfig/phonon.pc
%{mingw64_libdir}/libphonon.dll.a
%{mingw64_libdir}/libphononexperimental.dll.a
%{mingw64_qt4_datadir}/mkspecs/modules/qt_phonon.pri


%changelog
* Sat May 18 2013 Steven Boswell <ulatekh@yahoo.com> - 4.6.0-5
- Ported Fedora package to MinGW.
