%{?mingw_package_header}
	
%global mingw_build_win32 1
%global mingw_build_win64 1

%global mingw_pkg_name jack-audio-connection-kit

Summary:       The Jack Audio Connection Kit
Name:          mingw-%{mingw_pkg_name}
Version:       1.9.9.5
Release:       1%{?dist}
# The entire source (~500 files) is a mixture of these three licenses
License:       GPLv2 and GPLv2+ and LGPLv2+
Group:         System Environment/Daemons
URL:           http://www.jackaudio.org
Source0:       http://www.grame.fr/~letz/jack-%{version}.tar.bz2
Patch0:        jack-1.9.9-mingw-waf.patch
patch1:        jack-1.9.9-SHGFP_CURRENT_TYPE-mingw.patch
patch2:        jack-1.9.9-portaudio-no-asio.patch
Patch3:        jack-1.9.9-example-clients.patch

BuildArch:     noarch

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw32-gcc
BuildRequires: mingw64-gcc
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw32-binutils
BuildRequires: mingw64-binutils

BuildRequires: mingw32-libsamplerate
BuildRequires: mingw64-libsamplerate
BuildRequires: mingw32-portaudio
BuildRequires: mingw64-portaudio
# for examples
BuildRequires: mingw32-pthreads
BuildRequires: mingw64-pthreads
# for regex.h
BuildRequires: mingw32-libgnurx
BuildRequires: mingw64-libgnurx
#BuildRequires: python?
BuildRequires: pkgconfig

Requires:      pkgconfig


%description
JACK is a low-latency audio server, written primarily for the Linux
operating system. It can connect a number of different applications to
an audio device, as well as allowing them to share audio between
themselves. Its clients can run in their own processes (i.e. as a
normal application), or can they can run within a JACK server (i.e. a
"plugin").

JACK is different from other audio server efforts in that it has been
designed from the ground up to be suitable for professional audio
work. This means that it focuses on two key areas: synchronous
execution of all clients, and low latency operation.

%package -n     mingw32-%{mingw_pkg_name}
Summary:        %{summary}
Group:          Development/Libraries

%description -n mingw32-%{mingw_pkg_name}
JACK is a low-latency audio server, written primarily for the Linux
operating system. It can connect a number of different applications to
an audio device, as well as allowing them to share audio between
themselves. Its clients can run in their own processes (i.e. as a
normal application), or can they can run within a JACK server (i.e. a
"plugin").

JACK is different from other audio server efforts in that it has been
designed from the ground up to be suitable for professional audio
work. This means that it focuses on two key areas: synchronous
execution of all clients, and low latency operation.


%package -n     mingw64-%{mingw_pkg_name}
Summary:        %{summary}
Group:          Development/Libraries

%description -n mingw64-%{mingw_pkg_name}
JACK is a low-latency audio server, written primarily for the Linux
operating system. It can connect a number of different applications to
an audio device, as well as allowing them to share audio between
themselves. Its clients can run in their own processes (i.e. as a
normal application), or can they can run within a JACK server (i.e. a
"plugin").

JACK is different from other audio server efforts in that it has been
designed from the ground up to be suitable for professional audio
work. This means that it focuses on two key areas: synchronous
execution of all clients, and low latency operation.


%package -n     mingw32-%{mingw_pkg_name}-static
Summary:        Static cross compiled version of the portaudio library
Requires:       mingw32-%{mingw_pkg_name} = %{version}-%{release}
Group:          Development/Libraries

%description -n mingw32-%{mingw_pkg_name}-static
Static cross compiled version of the portaudio library.

%package -n     mingw64-%{mingw_pkg_name}-static
Summary:        Static cross compiled version of the portaudio library
Requires:       mingw64-%{mingw_pkg_name} = %{version}-%{release}
Group:          Development/Libraries

%description -n mingw64-%{mingw_pkg_name}-static
Static cross compiled version of the portaudio library.

%package -n     mingw32-%{mingw_pkg_name}-example-clients
Summary:       Example clients that use Jack 
Group:         Applications/Multimedia
Requires:      %{name} = %{version}-%{release}

%description -n mingw32-%{mingw_pkg_name}-example-clients
Small example clients that use the Jack Audio Connection Kit.

%package -n     mingw64-%{mingw_pkg_name}-example-clients
Summary:       Example clients that use Jack 
Group:         Applications/Multimedia
Requires:      %{name} = %{version}-%{release}

%description -n mingw64-%{mingw_pkg_name}-example-clients
Small example clients that use the Jack Audio Connection Kit.


%{?mingw_debug_package}


%prep
%setup -q -c jack-%{version}

pushd jack-%{version}

%patch0 -p1 -b .mingw
%patch1 -p1 -b .shgfp
%patch2 -p1 -b .noasio
%patch3 -p1 -b .examples

# Fix encoding issues
for file in ChangeLog README TODO; do
	sed 's|\r||' $file > $file.tmp
	iconv -f ISO-8859-1 -t UTF8 $file.tmp > $file.tmp2
	touch -r $file $file.tmp2
	mv -f $file.tmp2 $file
done
popd

# now copy
for dir in win32 win64; do
	cp -a jack-%{version} $dir
done
rm -rf jack-%{version}


%build
pushd win32
	export PREFIX=%{mingw32_prefix}

	%{mingw32_env}
	./waf configure --debug --dist-target=mingw \
		--portaudio --winmme

	# doesn't like concurrent builds
	./waf build -j1 -v
popd

pushd win64
	export PREFIX=%{mingw64_prefix}

	%{mingw64_env}
	./waf configure --debug --dist-target=mingw \
		--portaudio --winmme

	# doesn't like concurrent builds
	./waf build -j1 -v
popd


%install
pushd win32
	./waf --destdir=$RPM_BUILD_ROOT install
	cp -a ChangeLog README README_NETJACK2 TODO ../
popd

pushd win64
	./waf --destdir=$RPM_BUILD_ROOT install
popd


%files -n mingw32-%{mingw_pkg_name}
%doc ChangeLog README README_NETJACK2 TODO
%{mingw32_bindir}/jackd.exe
%{mingw32_includedir}/jack/
%{mingw32_bindir}/jack/
%{mingw32_bindir}/jack*.dll
%{mingw32_bindir}/jack_*.exe
%{mingw32_libdir}/pkgconfig/jack.pc
%{mingw32_libdir}/libaudioadapter.dll.a
%{mingw32_libdir}/libdummy.dll.a
%{mingw32_libdir}/libjack.dll.a
%{mingw32_libdir}/libjackserver.dll.a
%{mingw32_libdir}/libloopback.dll.a
%{mingw32_libdir}/libnet.dll.a
%{mingw32_libdir}/libnetmanager.dll.a
%{mingw32_libdir}/libnetadapter.dll.a
%{mingw32_libdir}/libprofiler.dll.a
%{mingw32_libdir}/libinprocess.dll.a
%{mingw32_libdir}/libjacknet.dll.a
%{mingw32_libdir}/libnetone.dll.a
# this conflicts from the real portaudio import lib
%exclude %{mingw32_libdir}/libportaudio.dll.a
%{mingw32_libdir}/libwinmme.dll.a

%files -n mingw64-%{mingw_pkg_name}
%doc ChangeLog README README_NETJACK2 TODO
%{mingw64_bindir}/jackd.exe
%{mingw64_includedir}/jack/
%{mingw64_bindir}/jack/
%{mingw64_bindir}/jack*.dll
%{mingw64_bindir}/jack_*.exe
%{mingw64_libdir}/pkgconfig/jack.pc
%{mingw64_libdir}/libaudioadapter.dll.a
%{mingw64_libdir}/libdummy.dll.a
%{mingw64_libdir}/libjack.dll.a
%{mingw64_libdir}/libjackserver.dll.a
%{mingw64_libdir}/libloopback.dll.a
%{mingw64_libdir}/libnet.dll.a
%{mingw64_libdir}/libnetmanager.dll.a
%{mingw64_libdir}/libnetadapter.dll.a
%{mingw64_libdir}/libprofiler.dll.a
%{mingw64_libdir}/libinprocess.dll.a
%{mingw64_libdir}/libjacknet.dll.a
%{mingw64_libdir}/libnetone.dll.a
# this conflicts from the real portaudio import lib
%exclude %{mingw64_libdir}/libportaudio.dll.a
%{mingw64_libdir}/libwinmme.dll.a


%changelog
* Tue May 21 2013 Steven Boswell <ulatekh@yahoo.com> - 1.9.9.5-1
- Built with updated sources
- Got 64-bit working

* Sun Jul 1 2012 Tim Mayberry <mojofunk@gmail.com> - 1.9.9-1
- Update to Fedora 17 MinGW package guidelines
- Disable 64 bit build due to portaudio 64 bit issue

* Wed Dec 14 2011 Tim Mayberry <mojofunk@gmail.com> - 1.9.8-1
- Initial mingw-w64 package, svn@4638 snapshot, plus waf patches
