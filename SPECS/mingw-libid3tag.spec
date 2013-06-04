%{?mingw_package_header}

%global _basename libid3tag

Name:           mingw-%{_basename}
Version:        0.15.1b
Release:        13%{?dist}
Summary:        ID3 tag manipulation library

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.underbit.com/products/mad/
Source0:        http://downloads.sourceforge.net/mad/%{_basename}-%{version}.tar.gz
Patch0:         libid3tag-0.15.1b-fix_overflow.patch
Patch1:         libid3tag-mingw.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-zlib >= 1.1.4

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-zlib >= 1.1.4

Requires:       pkgconfig
BuildRequires:  gperf

%description
libid3tag is a library for reading and (eventually) writing ID3 tags,
both ID3v1 and the various versions of ID3v2.


%package -n     mingw32-%{_basename}
Summary:        ID3 tag manipulation library
Group:          Development/Libraries

%description -n mingw32-%{_basename}
libid3tag is a library for reading and (eventually) writing ID3 tags,
both ID3v1 and the various versions of ID3v2.
This is the MinGW version, built for the win32 target.

%package -n     mingw32-%{_basename}-static
Summary:        ID3 tag manipulation library
Group:          Development/Libraries
Requires:       mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-%{_basename}-static
Static libraries for the MinGW version of %{_basename}, built for
the win32 target.

%package -n     mingw64-%{_basename}
Summary:        ID3 tag manipulation library
Group:          Development/Libraries

%description -n mingw64-%{_basename}
libid3tag is a library for reading and (eventually) writing ID3 tags,
both ID3v1 and the various versions of ID3v2.
This is the MinGW version, built for the win64 target.

%package -n     mingw64-%{_basename}-static
Summary:        ID3 tag manipulation library
Group:          Development/Libraries
Requires:       mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-%{_basename}-static
Static libraries for the MinGW version of %{_basename}, built for
the win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}-%{version}
%patch0 -p0 -b .CVE-2008-2109
%patch1 -p0

# *.pc originally from the Debian package.
cat << \EOF > %{name}32.pc
prefix=%{mingw32_prefix}
exec_prefix=%{mingw32_exec_prefix}
libdir=%{mingw32_libdir}
includedir=%{mingw32_includedir}

Name: id3tag
Description: ID3 tag manipulation library
Requires:
Version: %{version}
Libs: -L${libdir} -lid3tag
Cflags: -I${includedir}
EOF

cat << \EOF > %{name}64.pc
prefix=%{mingw64_prefix}
exec_prefix=%{mingw64_exec_prefix}
libdir=%{mingw64_libdir}
includedir=%{mingw64_includedir}

Name: id3tag
Description: ID3 tag manipulation library
Requires:
Version: %{version}
Libs: -L${libdir} -lid3tag
Cflags: -I${includedir}
EOF


%build
%{mingw_configure} --disable-dependency-tracking

# Fix libtool to recognize win64 archives
sed -i 's|file format pe-i386(\.\*architecture: i386)?|file format pe-x86-64|g' build_win64/libtool
sed -i 's|file format pei\*-i386(\.\*architecture: i386)?|file format pe-x86-64|g' build_win64/libtool

%{mingw_make} %{?_smp_mflags}


%install
rm -rf %{buildroot}
%{mingw_make} install DESTDIR=%{buildroot}
rm -f %{buildroot}{_libdir}/*.la
install -Dpm 644 %{name}32.pc %{buildroot}%{mingw32_libdir}/pkgconfig/id3tag.pc
install -Dpm 644 %{name}64.pc %{buildroot}%{mingw64_libdir}/pkgconfig/id3tag.pc

rm -f %{buildroot}/%{mingw32_libdir}/*.la
rm -f %{buildroot}/%{mingw64_libdir}/*.la


%clean
rm -rf %{buildroot}



%files -n mingw32-%{_basename}
%defattr(-,root,root,-)
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{mingw32_bindir}/libid3tag-0.dll
%{mingw32_includedir}/id3tag.h
%{mingw32_libdir}/libid3tag.dll.a
%{mingw32_libdir}/pkgconfig/id3tag.pc

%files -n mingw32-%{_basename}-static
%{mingw32_libdir}/libid3tag.a

%files -n mingw64-%{_basename}
%defattr(-,root,root,-)
#%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{mingw64_bindir}/libid3tag-0.dll
%{mingw64_includedir}/id3tag.h
%{mingw64_libdir}/libid3tag.dll.a
%{mingw64_libdir}/pkgconfig/id3tag.pc

%files -n mingw64-%{_basename}-static
%{mingw64_libdir}/libid3tag.a


%changelog
* Fri May 17 2013 Steven Boswell <ulatekh@yahoo.com> - 0.15.1b-13
- Ported Fedora package to MinGW
