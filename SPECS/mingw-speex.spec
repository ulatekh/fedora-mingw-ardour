%{?mingw_package_header}

%global _basename speex

Summary:	A voice compression format (codec)
Name:		mingw-%{_basename}
Version:	1.2
%define rc_ver	rc1
Release:	0.15.%{rc_ver}%{?dist}
License:	BSD
Group:		System Environment/Libraries
URL:		http://www.speex.org/
Source0:	http://downloads.xiph.org/releases/speex/%{_basename}-%{version}%{rc_ver}.tar.gz

Requires: 	    pkgconfig

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libogg

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-libogg

%description
Speex is a patent-free compression format designed especially for
speech. It is specialized for voice communications at low bit-rates in
the 2-45 kbps range. Possible applications include Voice over IP
(VoIP), Internet audio streaming, audio books, and archiving of speech
data (e.g. voice mail).


%package -n mingw32-%{_basename}
Summary:    A voice compression format (codec)
Group:     	Development/Libraries

%description -n mingw32-%{_basename}
Speex is a patent-free compression format designed especially for
speech.
This is the MinGW version, built for the win32 target.

%package -n mingw32-%{_basename}-static
Summary:    A voice compression format (codec)
Group:     	Development/Libraries
Requires:   mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-%{_basename}-static
Static libraries for the MinGW version of speex, built for the
win32 target.

%package -n mingw32-%{_basename}-tools
Summary:    The tools package for mingw32-%{_basename}
Group:      Applications/Multimedia
Requires:   mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-%{_basename}-tools
Speex is a patent-free compression format designed especially for
speech. This package contains tools files and user's manual for the
MinGW version of %{_basename}, built for the win32 target.

%package -n mingw64-%{_basename}
Summary:    A voice compression format (codec)
Group:     	Development/Libraries

%description -n mingw64-%{_basename}
Speex is a patent-free compression format designed especially for
speech.
This is the MinGW version, built for the win64 target.

%package -n mingw64-%{_basename}-static
Summary:    A voice compression format (codec)
Group:     	Development/Libraries
Requires:   mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-%{_basename}-static
Static libraries for the MinGW version of speex, built for the
win64 target.

%package -n mingw64-%{_basename}-tools
Summary:    The tools package for mingw64-%{_basename}
Group:      Applications/Multimedia
Requires:   mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-%{_basename}-tools
Speex is a patent-free compression format designed especially for
speech. This package contains tools files and user's manual for the
MinGW version of %{_basename}, built for the win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}-%{version}%{rc_ver}

%build
%{mingw_configure}

# Remove rpath from speexenc and speexdec
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' build_win32/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' build_win32/libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' build_win64/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' build_win64/libtool

# Fix libtool to recognize win64 archives
sed -i 's|file format pe-i386(\.\*architecture: i386)?|file format pe-x86-64|g' build_win64/libtool

%{mingw_make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{mingw_make} DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{mingw32_docdir}/speex/manual.pdf
rm -f $RPM_BUILD_ROOT%{mingw64_docdir}/speex/manual.pdf

%clean
rm -rf $RPM_BUILD_ROOT


%files -n mingw32-%{_basename}
%defattr(-,root,root,-)
%doc AUTHORS COPYING TODO ChangeLog README NEWS
%{mingw32_bindir}/libspeex-1.dll
%{mingw32_bindir}/libspeexdsp-1.dll
%doc doc/manual.pdf
%{mingw32_includedir}/speex
%{mingw32_datadir}/aclocal/speex.m4
%{mingw32_libdir}/pkgconfig/speex*.pc
%{mingw32_libdir}/libspeex.dll.a
%{mingw32_libdir}/libspeexdsp.dll.a
%exclude %{mingw32_libdir}/libspeex*.la

%files -n mingw32-%{_basename}-static
%{mingw32_libdir}/libspeex.a
%{mingw32_libdir}/libspeexdsp.a

%files -n mingw32-%{_basename}-tools
%defattr(-,root,root,-)
%{mingw32_bindir}/speexenc.exe
%{mingw32_bindir}/speexdec.exe
%{mingw32_mandir}/man1/speexenc.1*
%{mingw32_mandir}/man1/speexdec.1*

%files -n mingw64-%{_basename}
%defattr(-,root,root,-)
%doc AUTHORS COPYING TODO ChangeLog README NEWS
%{mingw64_bindir}/libspeex-1.dll
%{mingw64_bindir}/libspeexdsp-1.dll
%doc doc/manual.pdf
%{mingw64_includedir}/speex
%{mingw64_datadir}/aclocal/speex.m4
%{mingw64_libdir}/pkgconfig/speex*.pc
%{mingw64_libdir}/libspeex.dll.a
%{mingw64_libdir}/libspeexdsp.dll.a
%exclude %{mingw64_libdir}/libspeex*.la

%files -n mingw64-%{_basename}-static
%{mingw64_libdir}/libspeex.a
%{mingw64_libdir}/libspeexdsp.a

%files -n mingw64-%{_basename}-tools
%defattr(-,root,root,-)
%{mingw64_bindir}/speexenc.exe
%{mingw64_bindir}/speexdec.exe
%{mingw64_mandir}/man1/speexenc.1*
%{mingw64_mandir}/man1/speexdec.1*


%changelog
* Mon Jun 3 2013 Steven Boswell <ulatekh@yahoo.com> - 1.2-0.15.rc1
- Ported existing Fedora package to MinGW
