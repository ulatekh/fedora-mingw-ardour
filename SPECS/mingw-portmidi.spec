%{?mingw_package_header}

%global _basename portmidi

Summary:        Real-time Midi I/O Library
Name:           mingw-%{_basename}
Version:        217
Release:        7%{?dist}
License:        MIT
Group:          System Environment/Libraries
URL:            http://portmedia.sourceforge.net/
Source0:        http://downloads.sourceforge.net/portmedia/%{_basename}-src-%{version}.zip
Source1:        pmdefaults.desktop
# Build fixes:
Patch0:         portmidi-cmake.patch
# Fix multilib conflict RHBZ#831432
Patch1:         portmidi-no_date_footer.patch
Patch2:         portmidi-mingw.patch
#BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  java-1.7.0-openjdk-devel
BuildRequires:  jpackage-utils
#BuildRequires:  python2-devel
BuildRequires:  doxygen
BuildRequires:  tex(latex)

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
PortMedia is a set of simple clean APIs and cross-platform library
implementations for music and other media. PortMidi sub-project provides a
real-time MIDI input/output library. This package contains the PortMidi
libraries.

%package -n mingw32-%{_basename}
Summary:        Real-time Midi I/O Library
Group:          System Environment/Libraries

%description -n mingw32-%{_basename}
PortMedia is a set of simple clean APIs and cross-platform library
implementations for music and other media. PortMidi sub-project provides a
real-time MIDI input/output library. This package contains the header files
and the documentation of PortMidi libraries.
This is the MinGW version, built for the win32 target.

%package -n mingw64-%{_basename}
Summary:        Real-time Midi I/O Library
Group:          System Environment/Libraries

%description -n mingw64-%{_basename}
PortMedia is a set of simple clean APIs and cross-platform library
implementations for music and other media. PortMidi sub-project provides a
real-time MIDI input/output library. This package contains the header files
and the documentation of PortMidi libraries.
This is the MinGW version, built for the win32 target.


%{?mingw_debug_package}


%prep
%setup -q -n %{_basename}
%patch0 -p1 -b .buildfix
%patch1 -p1 -b .no.date
%patch2 -p1

# ewwww... binaries
rm -f portmidi_cdt.zip */*.exe */*/*.exe

# Fix permissons and encoding issues:
find . -name "*.c" -exec chmod -x {} \;
find . -name "*.h" -exec chmod -x {} \;
for i in *.txt */*.txt */*/*.txt ; do
   chmod -x $i
   sed 's|\r||' $i > $i.tmp
   touch -r $i $i.tmp
   mv -f $i.tmp $i
done

# Fedora's jni library location is different
sed -i 's|loadLibrary.*|load("%{_libdir}/portmidi/libpmjni.so");|' \
   pm_java/jportmidi/JPortMidiApi.java

# Add shebang, lib and class path
sed -i -e 's|^java|#!/bin/sh\njava \\\
   -Djava.library.path=%{_libdir}/portmidi/|' \
   -e 's|/usr/share/java/|%{_libdir}/portmidi/|' \
   pm_java/pmdefaults/pmdefaults

%build
export JAVA_HOME=%{java_home}
# FindJNI.cmake is being really stupid for no apparent reason...
# so hardcode the paths
%{mingw_cmake} -DCMAKE_SKIP_BUILD_RPATH=1 \
	-DCMAKE_CACHEFILE_DIR=%{_builddir}/portmidi/build \
	-DJAVA_INCLUDE_PATH:STRING=${JAVA_HOME}/include \
	-DJAVA_INCLUDE_PATH2:STRING=${JAVA_HOME}/include/linux \
	-DJAVA_AWT_LIBRARY:STRING=${JAVA_HOME}/lib/i386 \
	-DJAVA_AWT_INCLUDE_PATH:STRING=${JAVA_HOME}/include \
	-DJAVA_JVM_LIBRARY:STRING=${JAVA_HOME}/jre/lib/i386/client \
	-DVERSION=%{version} .
%{mingw_make} %{?_smp_mflags}

%install
%{mingw_make_install} DESTDIR=%{buildroot}

# Fedora's jni library location is different
mkdir -p %{buildroot}%{mingw32_libdir}/portmidi/
mv %{buildroot}%{mingw32_libdir}/libpmjni.dll.a \
   %{buildroot}%{mingw32_libdir}/portmidi/
mkdir -p %{buildroot}%{mingw64_libdir}/portmidi/
mv %{buildroot}%{mingw64_libdir}/libpmjni.dll.a \
   %{buildroot}%{mingw64_libdir}/portmidi/

# Not being installed under MinGW?
mkdir -p %{buildroot}%{mingw32_bindir}
install -pm 644 build_win32/libportmidi.dll \
	%{buildroot}%{mingw32_bindir}
install -pm 644 build_win32/libportmidi_s.dll \
	%{buildroot}%{mingw32_bindir}
mkdir -p %{buildroot}%{mingw64_bindir}
install -pm 644 build_win64/libportmidi.dll \
	%{buildroot}%{mingw64_bindir}
install -pm 644 build_win64/libportmidi_s.dll \
	%{buildroot}%{mingw64_bindir}

# Why don't they install this header file?
install -pm 644 pm_common/pmutil.h %{buildroot}%{mingw32_includedir}/
install -pm 644 pm_common/pmutil.h %{buildroot}%{mingw64_includedir}/

# Remove duplicate library
rm -f %{buildroot}%{mingw32_libdir}/libportmidi_s.so
rm -f %{buildroot}%{mingw64_libdir}/libportmidi_s.so

# Argh...WTF?  This hasn't happened with any other MinGW package...
cat < /dev/null > debugfiles.list

%files -n mingw32-%{_basename}
%doc CHANGELOG.txt license.txt
%{mingw32_bindir}/*.dll
%doc README.txt
%{mingw32_includedir}/*
%{mingw32_libdir}/lib*.a
%{mingw32_libdir}/portmidi/lib*.a

%files -n mingw64-%{_basename}
%doc CHANGELOG.txt license.txt
%{mingw64_bindir}/*.dll
%doc README.txt
%{mingw64_includedir}/*
%{mingw64_libdir}/lib*.a
%{mingw64_libdir}/portmidi/lib*.a

%changelog
* Fri May 17 2013 Steven Boswell <ulatekh@yahoo.com> - 217-7
- Ported current Fedora package to MinGW
