%{?mingw_package_header}

%global _basename protobuf

# Don't build -python subpackage
%bcond_with python
# Don't build -java subpackage
%bcond_with java
# Don't require gtest
%bcond_with gtest

%if %{with python}
%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%endif

Summary:        Protocol Buffers - Google's data interchange format
Name:           mingw-%{_basename}
Version:        2.4.1
Release:        12%{?dist}
License:        BSD
Group:          Development/Libraries
Source:         http://protobuf.googlecode.com/files/%{_basename}-%{version}.tar.bz2
Source1:        ftdetect-proto.vim
Source2:        protobuf-init.el
Patch1:         protobuf-2.3.0-fedora-gtest.patch
Patch2:    	    protobuf-2.4.1-java-fixes.patch
URL:            http://code.google.com/p/protobuf/
BuildRequires:  automake autoconf libtool pkgconfig protobuf-compiler
BuildRequires:  mingw32-zlib mingw64-zlib
%if %{with gtest}
BuildRequires:  gtest-devel
%endif

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
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package -n mingw32-%{_basename}
Summary:        Protocol Buffers - Google's data interchange format
Group:          Development/Libraries

%description -n mingw32-%{_basename}
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

This is the MinGW version, built for the win32 target.

%package -n mingw32-%{_basename}-compiler
Summary: Protocol Buffers compiler
Group: Development/Libraries
Requires: mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-%{_basename}-compiler
This package contains Protocol Buffers compiler for all programming
languages, for the win32 target of MinGW.

%package -n mingw32-%{_basename}-static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: mingw32-%{_basename} = %{version}-%{release}

%description -n mingw32-%{_basename}-static
Static libraries for Protocol Buffers, for the win32 target of MinGW.

%package -n mingw32-%{_basename}-lite
Summary: Protocol Buffers LITE_RUNTIME libraries
Group: Development/Libraries

%description -n mingw32-%{_basename}-lite
Protocol Buffers built with optimize_for = LITE_RUNTIME. for the
win32 target of MinGW.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package -n mingw32-%{_basename}-lite-static
Summary: Static development files for %{name}-lite
Group: Development/Libraries
Requires: mingw32-%{_basename}-lite = %{version}-%{release}

%package -n mingw64-%{_basename}
Summary:        Protocol Buffers - Google's data interchange format
Group:          Development/Libraries

%description -n mingw64-%{_basename}
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

This is the MinGW version, built for the win64 target.

%description -n mingw32-%{_basename}-lite-static
This package contains static development libraries built with
optimize_for = LITE_RUNTIME, for the win32 target of MinGW.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package -n mingw64-%{_basename}-compiler
Summary: Protocol Buffers compiler
Group: Development/Libraries
Requires: mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-%{_basename}-compiler
This package contains Protocol Buffers compiler for all programming
languages, for the win64 target of MinGW.

%package -n mingw64-%{_basename}-static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: mingw64-%{_basename} = %{version}-%{release}

%description -n mingw64-%{_basename}-static
Static libraries for Protocol Buffers, for the win64 target of MinGW.

%package -n mingw64-%{_basename}-lite
Summary: Protocol Buffers LITE_RUNTIME libraries
Group: Development/Libraries

%description -n mingw64-%{_basename}-lite
Protocol Buffers built with optimize_for = LITE_RUNTIME. for the
win64 target of MinGW.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package -n mingw64-%{_basename}-lite-static
Summary: Static development files for %{name}-lite
Group: Development/Libraries
Requires: mingw64-%{_basename}-lite = %{version}-%{release}

%description -n mingw64-%{_basename}-lite-static
This package contains static development libraries built with
optimize_for = LITE_RUNTIME, for the win64 target of MinGW.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%if %{with python}
%package python
Summary: Python bindings for Google Protocol Buffers
Group: Development/Languages
BuildRequires: python-devel
BuildRequires: python-setuptools-devel
Conflicts: %{name}-compiler > %{version}
Conflicts: %{name}-compiler < %{version}

%description python
This package contains Python libraries for Google Protocol Buffers
%endif

%if %{with java}
%package java
Summary: Java Protocol Buffers runtime library
Group:   Development/Languages
BuildRequires:    java-devel >= 1.6
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-resources-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    maven-antrun-plugin
Requires:         java
Requires:         jpackage-utils
Conflicts:        %{name}-compiler > %{version}
Conflicts:        %{name}-compiler < %{version}

%description java
This package contains Java Protocol Buffers runtime library.

%package javadoc
Summary: Javadocs for %{name}-java
Group:   Documentation
Requires: jpackage-utils
Requires: %{name}-java = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}-java.

%endif

%{?mingw_debug_package}

%prep
%setup -q -n %{_basename}-%{version}
%if %{with gtest}
rm -rf gtest
%patch1 -p1 -b .gtest
%endif
chmod 644 examples/*
%if %{with java}
%patch2 -p1 -b .java-fixes
rm -rf java/src/test
%endif

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%mingw_configure --with-protoc=protoc

%mingw_make %{?_smp_mflags}

%if %{with python}
pushd python
python ./setup.py build
sed -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
popd
%endif

%if %{with java}
pushd java
mvn-rpmbuild install javadoc:javadoc
popd
%endif

%check
#make %{?_smp_mflags} check

%install
rm -rf %{buildroot}
%mingw_make %{?_smp_mflags} install DESTDIR=%{buildroot} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -exec rm -f {} \;

%if %{with python}
pushd python
python ./setup.py install --root=%{buildroot} --single-version-externally-managed --record=INSTALLED_FILES --optimize=1
popd
%endif
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

%if %{with java}
pushd java
install -d -m 755 %{buildroot}%{_javadir}
install -pm 644 target/%{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs %{buildroot}%{_javadocdir}/%{name}

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar
popd
%endif

# Don't install these.
rm -rf %{buildroot}/usr/share/vim

%files -n mingw32-%{_basename}
%defattr(-, root, root, -)
%{mingw32_bindir}/libprotobuf-7.dll
%doc CHANGES.txt CONTRIBUTORS.txt COPYING.txt README.txt
%dir %{mingw32_includedir}/google
%{mingw32_includedir}/google/protobuf/
%{mingw32_libdir}/libprotobuf.dll.a
%{mingw32_libdir}/libprotoc.dll.a
%{mingw32_libdir}/pkgconfig/protobuf.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.txt

%files -n mingw32-%{_basename}-compiler
%defattr(-, root, root, -)
%{mingw32_bindir}/i686-w64-mingw32-protoc.exe
%{mingw32_bindir}/libprotoc-7.dll
#%doc COPYING.txt README.txt

%files -n mingw32-%{_basename}-static
%defattr(-, root, root, -)
%{mingw32_libdir}/libprotobuf.a
%{mingw32_libdir}/libprotoc.a

%files -n mingw32-%{_basename}-lite
%defattr(-, root, root, -)
%{mingw32_bindir}/libprotobuf-lite-7.dll
%{mingw32_libdir}/libprotobuf-lite.dll.a
%{mingw32_libdir}/pkgconfig/protobuf-lite.pc

%files -n mingw32-%{_basename}-lite-static
%defattr(-, root, root, -)
%{mingw32_libdir}/libprotobuf-lite.a

%files -n mingw64-%{_basename}
%defattr(-, root, root, -)
%{mingw64_bindir}/libprotobuf-7.dll
#%doc CHANGES.txt CONTRIBUTORS.txt COPYING.txt README.txt
%dir %{mingw64_includedir}/google
%{mingw64_includedir}/google/protobuf/
%{mingw64_libdir}/libprotobuf.dll.a
%{mingw64_libdir}/libprotoc.dll.a
%{mingw64_libdir}/pkgconfig/protobuf.pc
#%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.txt

%files -n mingw64-%{_basename}-compiler
%defattr(-, root, root, -)
%{mingw64_bindir}/x86_64-w64-mingw32-protoc.exe
%{mingw64_bindir}/libprotoc-7.dll
#%doc COPYING.txt README.txt

%files -n mingw64-%{_basename}-static
%defattr(-, root, root, -)
%{mingw64_libdir}/libprotobuf.a
%{mingw64_libdir}/libprotoc.a

%files -n mingw64-%{_basename}-lite
%defattr(-, root, root, -)
%{mingw64_bindir}/libprotobuf-lite-7.dll
%{mingw64_libdir}/libprotobuf-lite.dll.a
%{mingw64_libdir}/pkgconfig/protobuf-lite.pc

%files -n mingw64-%{_basename}-lite-static
%defattr(-, root, root, -)
%{mingw64_libdir}/libprotobuf-lite.a

%if %{with python}
%files python
%defattr(-, root, root, -)
%dir %{python_sitelib}/google
%{python_sitelib}/google/protobuf/
%{python_sitelib}/protobuf-%{version}-py2.?.egg-info/
%{python_sitelib}/protobuf-%{version}-py2.?-nspkg.pth
%doc python/README.txt
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%if %{with java}
%files java
%defattr(-, root, root, -)
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar
%doc examples/AddPerson.java examples/ListPeople.java

%files javadoc
%defattr(-, root, root, -)
%{_javadocdir}/%{name}
%endif

%changelog
* Fri May 17 2013 Steven Boswell <ulatekh@yahoo.com> - 2.4.1-12
- Ported existing Fedora package to MinGW
