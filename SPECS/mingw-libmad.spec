%{?mingw_package_header}

%global _basename libmad

Name:		mingw-%{_basename}
Version:	0.15.1b
Release:	15%{?dist}
Summary:	MPEG audio decoder library

Group:		System Environment/Libraries
License:	GPLv2
URL:		http://www.underbit.com/products/mad/
Source0:	http://download.sourceforge.net/mad/%{_basename}-%{version}.tar.gz
Patch0:		libmad-0.15.1b-multiarch.patch
Patch1:		libmad-0.15.1b-ppc.patch
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/534287
Patch2:	    Provide-Thumb-2-alternative-code-for-MAD_F_MLN.diff
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/513734
Patch3:         libmad.thumb.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool

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
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2 extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.


%package -n mingw32-%{_basename}
Summary:	MPEG audio decoder library
Group:		Development/Libraries
Requires:	pkgconfig

%description -n mingw32-%{_basename}
%{summary}.
This is the MinGW version, built for the win32 target.


%package -n mingw64-%{_basename}
Summary:	MPEG audio decoder library
Group:		Development/Libraries
Requires:	pkgconfig

%description -n mingw64-%{_basename}
%{summary}.
This is the MinGW version, built for the win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}-%{version}
%ifarch %{ix86} x86_64 ppc ppc64
%patch0 -p1 -b .multiarch
%endif
%patch1 -p1 -b .ppc
%patch2 -p1 -b .alt_t2
%patch3 -p1 -b .thumb

sed -i -e /-fforce-mem/d configure* # -fforce-mem gone in gcc 4.2, noop earlier
touch -r aclocal.m4 configure.ac NEWS AUTHORS ChangeLog

# Create an additional pkgconfig file
%{__cat} << EOF > mad32.pc
prefix=%{mingw32_prefix}
exec_prefix=%{mingw32_prefix}
libdir=%{mingw32_libdir}
includedir=%{mingw32_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{mingw32_libdir} -lmad -lm
Cflags: -I%{mingw32_includedir}
EOF

# Create an additional pkgconfig file
%{__cat} << EOF > mad64.pc
prefix=%{mingw64_prefix}
exec_prefix=%{mingw64_prefix}
libdir=%{mingw64_libdir}
includedir=%{mingw64_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{mingw64_libdir} -lmad -lm
Cflags: -I%{mingw64_includedir}
EOF


%build
autoreconf -sfi
%{mingw_configure} \
%if 0%{?__isa_bits} == 64
	--enable-fpm=64bit \
%endif
%ifarch %{arm}
        --enable-fpm=arm \
%endif
	--disable-dependency-tracking \
	--enable-accuracy \
	--disable-debugging \
	--disable-static    

%{mingw_make} %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
%{mingw_make} install DESTDIR=%{buildroot}
rm -f %{buildroot}%{mingw32_libdir}/*.la
rm -f %{buildroot}%{mingw64_libdir}/*.la
%{__install} -D -p -m 0644 mad32.pc %{buildroot}%{mingw32_libdir}/pkgconfig/mad.pc
%{__install} -D -p -m 0644 mad64.pc %{buildroot}%{mingw64_libdir}/pkgconfig/mad.pc
touch -r mad.h.sed %{buildroot}/%{mingw32_includedir}/mad.h
touch -r mad.h.sed %{buildroot}/%{mingw64_includedir}/mad.h

%clean
rm -rf %{buildroot}


%files -n mingw32-%{_basename}
%defattr(-,root,root,-)
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
#%{mingw32_bindir}/libmad*.dll
%{mingw32_libdir}/libmad*.a
%{mingw32_libdir}/pkgconfig/mad.pc
%{mingw32_includedir}/mad.h


%files -n mingw64-%{_basename}
%defattr(-,root,root,-)
#%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
#%{mingw64_bindir}/libmad*.dll
%{mingw64_libdir}/libmad*.a
%{mingw64_libdir}/pkgconfig/mad.pc
%{mingw64_includedir}/mad.h


%changelog
* Fri May 17 2013 Steven Boswell <ulatekh@yahoo.com> - 0.15.1b-15
- Ported existing Fedora package to MinGW
