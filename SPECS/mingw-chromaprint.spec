%{?mingw_package_header}

%global _basename chromaprint

Name:           mingw-%{_basename}
Version:        0.7
Release:        1%{?dist}
Summary:        Library implementing the AcoustID fingerprinting

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.acoustid.org/chromaprint/
Source:         https://github.com/downloads/lalinsky/chromaprint/%{_basename}-%{version}.tar.gz

BuildRequires:  cmake

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-fftw

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-fftw

%description
Chromaprint library is the core component of the AcoustID project. It's a 
client-side library that implements a custom algorithm for extracting 
fingerprints from raw audio sources.

The library exposes a simple C API. The documentation for the C API can be
found in the main header file.


%package -n mingw32-lib%{_basename}
Summary:        Library implementing the AcoustID fingerprinting
Group:          System Environment/Libraries

%description -n mingw32-lib%{_basename}
Chromaprint library is the core component of the AcoustID project. It's a 
client-side library that implements a custom algorithm for extracting 
fingerprints from raw audio sources.

The library exposes a simple C API. The documentation for the C API can be
found in the main header file.
This is the MinGW version, built for the win32 target.

%package -n mingw64-lib%{_basename}
Summary:        Library implementing the AcoustID fingerprinting
Group:          System Environment/Libraries

%description -n mingw64-lib%{_basename}
Chromaprint library is the core component of the AcoustID project. It's a 
client-side library that implements a custom algorithm for extracting 
fingerprints from raw audio sources.

The library exposes a simple C API. The documentation for the C API can be
found in the main header file.
This is the MinGW version, built for the win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}-%{version}

# examples require ffmpeg, so turn off examples
%{mingw_cmake} -DBUILD_EXAMPLES=off -DBUILD_TESTS=off


%build
%{mingw_make} %{?_smp_mflags}


%install
%{mingw_make} install DESTDIR=%{buildroot}
rm  -f %{buildroot}%{mingw32_libdir}/lib*.la
rm  -f %{buildroot}%{mingw64_libdir}/lib*.la


%files -n mingw32-lib%{_basename}
%doc CHANGES.txt COPYING.txt NEWS.txt README.txt
%{mingw32_bindir}/libchromaprint.dll
%{mingw32_includedir}/chromaprint.h
%{mingw32_libdir}/libchromaprint.dll.a
%{mingw32_libdir}/pkgconfig/*.pc

%files -n mingw64-lib%{_basename}
%doc CHANGES.txt COPYING.txt NEWS.txt README.txt
%{mingw64_bindir}/libchromaprint.dll
%{mingw64_includedir}/chromaprint.h
%{mingw64_libdir}/libchromaprint.dll.a
%{mingw64_libdir}/pkgconfig/*.pc

%changelog
* Sun Jun  2 2013 Steven Boswell <ulatekh@yahoo.com> - 0.7-1
- Ported existing Fedora package to MinGW
