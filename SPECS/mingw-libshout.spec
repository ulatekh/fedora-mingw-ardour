%{?mingw_package_header}

%global _basename libshout

Name:           mingw-%{_basename}
Version:        2.2.2
Release:        8%{?dist}
Summary:        Icecast source streaming library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.icecast.org/
Source:         http://downloads.us.xiph.org/releases/libshout/%{_basename}-%{version}.tar.gz
Patch0:         libshout-2.2.2-fix_speex.patch
# http://permalink.gmane.org/gmane.comp.audio.icecast.devel/1960
Patch1:         libshout-mingw.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libogg
BuildRequires:  mingw32-libvorbis
BuildRequires:  mingw32-libtheora
BuildRequires:  mingw32-speex

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-libogg
BuildRequires:  mingw64-libvorbis
BuildRequires:  mingw64-libtheora
BuildRequires:  mingw64-speex


%description
libshout is a library for communicating with and sending data to an
icecast server.  It handles the socket connection, the timing of the
data, and prevents most bad data from getting to the icecast server.

%package -n     mingw32-%{_basename}
Summary:        Icecast source streaming library
Group:          Development/Libraries

%description -n mingw32-%{_basename}
libshout is a library for communicating with and sending data to an
icecast server.  It handles the socket connection, the timing of the
data, and prevents most bad data from getting to the icecast server.

This is the MinGW version, built for the win32 target.

%package -n     mingw32-%{_basename}-static
Summary:        Icecast source streaming library
Group:          Development/Libraries
Requires:       mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-%{_basename}-static
Static libraries for the MinGW version of %{_basename}, built for
the win32 target.

%package -n     mingw64-%{_basename}
Summary:        Icecast source streaming library
Group:          Development/Libraries

%description -n mingw64-%{_basename}
libshout is a library for communicating with and sending data to an
icecast server.  It handles the socket connection, the timing of the
data, and prevents most bad data from getting to the icecast server.

This is the MinGW version, built for the win64 target.

%package -n     mingw64-%{_basename}-static
Summary:        Icecast source streaming library
Group:          Development/Libraries
Requires:       mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-%{_basename}-static
Static libraries for the MinGW version of %{_basename}, built for
the win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}-%{version}
%patch0 -p1 -b .fix_speex
%patch1 -p1

%build
%{mingw_configure} --enable-shared --enable-static

# clean unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' build_win32/libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' build_win64/libtool

# Fix libtool to recognize win64 archives
sed -i 's|file format pe-i386(\.\*architecture: i386)?|file format pe-x86-64|g' build_win64/libtool
sed -i 's|file format pei\*-i386(\.\*architecture: i386)?|file format pe-x86-64|g' build_win64/libtool

%{mingw_make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%{mingw_make} DESTDIR="$RPM_BUILD_ROOT" INSTALL="install -p " install

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{mingw32_docdir}
rm -rf $RPM_BUILD_ROOT%{mingw64_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n mingw32-%{_basename}
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{mingw32_bindir}/libshout-3.dll
%doc examples/*.c doc/*.xml doc/*.xsl
%{mingw32_libdir}/libshout.dll.a
%{mingw32_libdir}/pkgconfig/shout.pc
%dir %{mingw32_includedir}/shout/
%{mingw32_includedir}/shout/shout.h
%{mingw32_datadir}/aclocal/shout.m4

%files -n mingw32-%{_basename}-static
%{mingw32_libdir}/libshout.a

%files -n mingw64-%{_basename}
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{mingw64_bindir}/libshout-3.dll
%doc examples/*.c doc/*.xml doc/*.xsl
%{mingw64_libdir}/libshout.dll.a
%{mingw64_libdir}/pkgconfig/shout.pc
%dir %{mingw64_includedir}/shout/
%{mingw64_includedir}/shout/shout.h
%{mingw64_datadir}/aclocal/shout.m4

%files -n mingw64-%{_basename}-static
%{mingw64_libdir}/libshout.a

%changelog
* Mon Jun 3 2013 Steven Boswell <ulatekh@yahoo.com> - 2.2.2-8
- Ported existing Fedora package to MinGW
