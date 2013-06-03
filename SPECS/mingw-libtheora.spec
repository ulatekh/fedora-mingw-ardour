%{?mingw_package_header}

%global _basename libtheora

Name:           mingw-%{_basename}
Summary:        Theora Video Compression Codec
Version:        1.1.1
Release:        4%{?dist}
License:        BSD
Group:          System Environment/Libraries
URL:            http://www.theora.org
Source0:        http://downloads.xiph.org/releases/theora/%{_basename}-%{version}.tar.xz
Patch0:         libtheora-mingw.patch

Requires:       pkgconfig

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libogg
BuildRequires:  mingw32-libvorbis
BuildRequires:  mingw32-SDL mingw32-libpng

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-libogg
BuildRequires:  mingw64-libvorbis
BuildRequires:  mingw64-SDL mingw64-libpng


%description
Theora is Xiph.Org's first publicly released video codec, intended
for use within the Ogg's project's Ogg multimedia streaming system.
Theora is derived directly from On2's VP3 codec; Currently the two are
nearly identical, varying only in encapsulating decoder tables in the
bitstream headers, but Theora will make use of this extra freedom
in the future to improve over what is possible with VP3.


%package -n mingw32-%{_basename}
Summary:    Theora Video Compression Codec
Group:      Development/Libraries

%description -n mingw32-%{_basename}
Theora is Xiph.Org's first publicly released video codec, intended
for use within the Ogg's project's Ogg multimedia streaming system.

This is the MinGW version, built for the win32 target.

%package -n mingw32-%{_basename}-static
Summary:    Static libraries for Theora Video Compression Codec
Group:      Applications/Multimedia
Requires:   mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-%{_basename}-static
Static libraries for the MinGW version of %{_basename}, built for
the win32 target.

%package -n mingw32-theora-tools
Summary:    Command line tools for Theora videos
Group:      Applications/Multimedia
Requires:   mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-theora-tools
The theora-tools package contains simple command line tools for use
with theora bitstreams.

This is the MinGW version, built for the win32 target.

%package -n mingw64-%{_basename}
Summary:    Theora Video Compression Codec
Group:      Development/Libraries

%description -n mingw64-%{_basename}
Theora is Xiph.Org's first publicly released video codec, intended
for use within the Ogg's project's Ogg multimedia streaming system.

This is the MinGW version, built for the win64 target.

%package -n mingw64-%{_basename}-static
Summary:    Static libraries for Theora Video Compression Codec
Group:      Applications/Multimedia
Requires:   mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-%{_basename}-static
Static libraries for the MinGW version of %{_basename}, built for
the win64 target.

%package -n mingw64-theora-tools
Summary:    Command line tools for Theora videos
Group:      Applications/Multimedia
Requires:   mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-theora-tools
The theora-tools package contains simple command line tools for use
with theora bitstreams.

This is the MinGW version, built for the win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}-%{version}
%patch0 -p1
# no custom CFLAGS please
sed -i 's/CFLAGS="$CFLAGS $cflags_save"/CFLAGS="$cflags_save"/g' configure


%build
%{mingw_configure} --enable-shared --disable-examples
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' build_win32/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' build_win32/libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' build_win64/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' build_win64/libtool

# Fix libtool to recognize win64 archives
sed -i 's|file format pe-i386(\.\*architecture: i386)?|file format pe-x86-64|g' build_win64/libtool

%{mingw_make} %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%{mingw_make} install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/%{mingw32_libdir}/*.la
rm $RPM_BUILD_ROOT/%{mingw64_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{mingw32_docdir}
rm -rf $RPM_BUILD_ROOT/%{mingw64_docdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files -n mingw32-%{_basename}
%doc README COPYING
%{mingw32_bindir}/libtheora-0.dll
%{mingw32_bindir}/libtheoradec-1.dll
%{mingw32_includedir}/theora
%{mingw32_libdir}/libtheora.dll.a
%{mingw32_libdir}/libtheoradec.dll.a
%{mingw32_libdir}/pkgconfig/theora*.pc

%files -n mingw32-%{_basename}-static
%{mingw32_libdir}/libtheora.a
%{mingw32_libdir}/libtheoradec.a
%{mingw32_libdir}/libtheoraenc.a

#files -n mingw32-theora-tools
#defattr(-,root,root,-)
#{mingw32_bindir}/*.exe

%files -n mingw64-%{_basename}
%doc README COPYING
%{mingw64_bindir}/libtheora-0.dll
%{mingw64_bindir}/libtheoradec-1.dll
%{mingw64_includedir}/theora
%{mingw64_libdir}/libtheora.dll.a
%{mingw64_libdir}/libtheoradec.dll.a
%{mingw64_libdir}/pkgconfig/theora*.pc

%files -n mingw64-%{_basename}-static
%{mingw64_libdir}/libtheora.a
%{mingw64_libdir}/libtheoradec.a
%{mingw64_libdir}/libtheoraenc.a

#files -n mingw64-theora-tools
#defattr(-,root,root,-)
#{mingw64_bindir}/*.exe


%changelog
* Mon Jun 3 2013 Steven Boswell <ulatekh@yahoo.com> - 1.1.1-4
- Ported existing Fedora package to MinGW
