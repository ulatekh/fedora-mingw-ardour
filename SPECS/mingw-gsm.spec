%{?mingw_package_header}

%global _basename gsm

Name:           mingw-%{_basename}
Version:        1.0.13
Release:        7%{?dist}
Summary:        Shared libraries for GSM speech compressor

Group:          System Environment/Libraries
License:        MIT
URL:            http://www.quut.com/gsm/
Source:         http://www.quut.com/gsm/%{_basename}-%{version}.tar.gz
Patch0:         gsm-makefile.patch
Patch1:         gsm-warnings.patch
Patch2:         gsm-64bit.patch
Patch3:         %{_basename}-%{version}-mingw.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  gzip

%global srcver 1.0-pl13
%global soname 1.0.12

%description
Contains runtime shared libraries for libgsm, an implementation of
the European GSM 06.10 provisional standard for full-rate speech
transcoding, prI-ETS 300 036, which uses RPE/LTP (residual pulse
excitation/long term prediction) coding at 13 kbit/s.

GSM 06.10 compresses frames of 162 13-bit samples (8 kHz sampling
rate, i.e. a frame rate of 50 Hz) into 260 bits; for compatibility
with typical UNIX applications, our implementation turns frames of 160
16-bit linear samples into 33-byte frames (1650 Bytes/s).
The quality of the algorithm is good enough for reliable speaker
recognition; even music often survives transcoding in recognizable
form (given the bandwidth limitations of 8 kHz sampling rate).

The interfaces offered are a front end modelled after compress(1), and
a library API.  Compression and decompression run faster than realtime
on most SPARCstations.  The implementation has been verified against the
ETSI standard test patterns.


%package -n     mingw32-%{_basename}
Summary:        Shared libraries for GSM speech compressor
%description -n mingw32-%{_basename}
An implementation of the European GSM 06.10 provisional standard for
full-rate speech transcoding, prI-ETS 300 036, which uses RPE/LTP
(residual pulse excitation/long term prediction) coding at 13 kbit/s.

This is the MinGW version, built for the win32 target.


%package -n     mingw64-%{_basename}
Summary:        Shared libraries for GSM speech compressor
%description -n mingw64-%{_basename}
An implementation of the European GSM 06.10 provisional standard for
full-rate speech transcoding, prI-ETS 300 036, which uses RPE/LTP
(residual pulse excitation/long term prediction) coding at 13 kbit/s.

This is the MinGW version, built for the win64 target.


%{?mingw_debug_package}


%prep
%setup -n %{_basename}-%{srcver} -q
%patch0 -p1 -b .mk
%patch1 -p1 -b .warn
%patch2 -p1 -b .64bit
%patch3 -p1

%build
# gsm has a very rudimentary makefile -- there's no build configuration
# system, e.g. autoconf / cmake / scons.  So we roll our own.
cd ..
rm -rf %{_basename}-%{srcver}-build32
cp -Rp %{_basename}-%{srcver} %{_basename}-%{srcver}-build32
rm -rf %{_basename}-%{srcver}-build64
cp -Rp %{_basename}-%{srcver} %{_basename}-%{srcver}-build64

pushd %{_basename}-%{srcver}-build32
export RPM_OPT_FLAGS="%{mingw32_cflags} -fPIC";
export CC=%mingw32_cc
export AR=%mingw32_ar
export RANLIB=%mingw32_ranlib
make %{?_smp_mflags} all
popd

pushd %{_basename}-%{srcver}-build64
export RPM_OPT_FLAGS="%{mingw64_cflags} -fPIC"
export CC=%mingw64_cc
export AR=%mingw64_ar
export RANLIB=%mingw64_ranlib
make %{?_smp_mflags} all
popd

%install
rm -rf $RPM_BUILD_ROOT
cd ..

pushd %{_basename}-%{srcver}-build32
mkdir -p $RPM_BUILD_ROOT%{mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{mingw32_includedir}/gsm
mkdir -p $RPM_BUILD_ROOT%{mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{mingw32_mandir}/{man1,man3}

make install \
	CC=%mingw32_cc \
	AR=%mingw32_ar \
	RANLIB=%mingw32_ranlib \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{mingw32_prefix} \
	GSM_INSTALL_INC=$RPM_BUILD_ROOT%{mingw32_includedir}/gsm \
	GSM_INSTALL_LIB=$RPM_BUILD_ROOT%{mingw32_libdir} \
	TOAST_INSTALL_ROOT=$RPM_BUILD_ROOT%{mingw32_prefix} \
	TOAST_INSTALL_BIN=$RPM_BUILD_ROOT%{mingw32_bindir} \
	TOAST_INSTALL_MAN=$RPM_BUILD_ROOT%{mingw32_mandir}/man1

mkdir -p $RPM_BUILD_ROOT%{mingw32_libdir}
cp -p $RPM_BUILD_DIR/%{_basename}-%{srcver}-build32/lib/libgsm.dll $RPM_BUILD_ROOT%{mingw32_bindir}

# some apps look for this in /usr/include
ln -s gsm/gsm.h $RPM_BUILD_ROOT%{mingw32_includedir}

# Fix permissions
chmod u+w $RPM_BUILD_ROOT%{mingw32_libdir}/lib*.a
chmod g-w $RPM_BUILD_ROOT%{mingw32_bindir}/libgsm.dll
popd

pushd %{_basename}-%{srcver}-build64
mkdir -p $RPM_BUILD_ROOT%{mingw64_bindir}
mkdir -p $RPM_BUILD_ROOT%{mingw64_includedir}/gsm
mkdir -p $RPM_BUILD_ROOT%{mingw64_libdir}
mkdir -p $RPM_BUILD_ROOT%{mingw64_mandir}/{man1,man3}

make install \
	CC=%mingw64_cc \
	AR=%mingw64_ar \
	RANLIB=%mingw64_ranlib \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{mingw64_prefix} \
	GSM_INSTALL_INC=$RPM_BUILD_ROOT%{mingw64_includedir}/gsm \
	GSM_INSTALL_LIB=$RPM_BUILD_ROOT%{mingw64_libdir} \
	TOAST_INSTALL_ROOT=$RPM_BUILD_ROOT%{mingw64_prefix} \
	TOAST_INSTALL_BIN=$RPM_BUILD_ROOT%{mingw64_bindir} \
	TOAST_INSTALL_MAN=$RPM_BUILD_ROOT%{mingw64_mandir}/man1

# Compress man pages
gzip -9 $RPM_BUILD_ROOT%{mingw32_mandir}/man3/*.3
gzip -9 $RPM_BUILD_ROOT%{mingw64_mandir}/man3/*.3

mkdir -p $RPM_BUILD_ROOT%{mingw64_libdir}
cp -p $RPM_BUILD_DIR/%{_basename}-%{srcver}-build64/lib/libgsm.dll $RPM_BUILD_ROOT%{mingw64_bindir}

# some apps look for this in /usr/include
ln -s gsm/gsm.h $RPM_BUILD_ROOT%{mingw64_includedir}

# Fix permissions
chmod u+w $RPM_BUILD_ROOT%{mingw64_libdir}/lib*.a
chmod g-w $RPM_BUILD_ROOT%{mingw64_bindir}/libgsm.dll
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files -n mingw32-%{_basename}
%defattr(-,root,root,-)
%doc ChangeLog COPYRIGHT MACHINES README
%{mingw32_libdir}/lib*.a
%{mingw32_bindir}/libgsm.dll
%dir %{mingw32_includedir}/gsm
%{mingw32_includedir}/gsm/gsm.h
%{mingw32_includedir}/gsm.h
%{mingw32_mandir}/man3/*

%files -n mingw64-%{_basename}
%defattr(-,root,root,-)
%doc ChangeLog COPYRIGHT MACHINES README
%{mingw64_libdir}/lib*.a
%{mingw64_bindir}/libgsm.dll
%dir %{mingw64_includedir}/gsm
%{mingw64_includedir}/gsm/gsm.h
%{mingw64_includedir}/gsm.h
%{mingw64_mandir}/man3/*

%changelog
* Fri May 17 2013 Steven Boswell <ulatekh@yahoo.com> - 1.0.13-7
- Ported Fedora package to MinGW
