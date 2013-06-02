%{?mingw_package_header}

%global mingw_pkg_name fftw
%global openmp 0

Name:           mingw-%{mingw_pkg_name}
Version:        3.3.3
Release:        1%{?dist}
Summary:        MinGW Fast Fourier Transform library
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-gcc-gfortran
BuildRequires:  mingw64-gcc-gfortran
BuildArch:      noarch


%description
This package contains the MinGW windows port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

# Mingw32
%package -n mingw32-%{mingw_pkg_name}
Summary:                %{summary}

%description -n mingw32-%{mingw_pkg_name}
This package contains the MinGW win32 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains cross-compiled libraries and development tools
for Windows.

%package -n mingw32-%{mingw_pkg_name}-static
Summary:                %{summary}

%description -n mingw32-%{mingw_pkg_name}-static
This package contains the MinGW win32 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains static cross-compiled library

# Mingw64
%package -n mingw64-%{mingw_pkg_name}
Summary:                %{summary}

%description -n mingw64-%{mingw_pkg_name}
This package contains the MinGW win64 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains cross-compiled libraries and development tools
for Windows.

%package -n mingw64-%{mingw_pkg_name}-static
Summary:                %{summary}

%description -n mingw64-%{mingw_pkg_name}-static
This package contains the MinGW win64 port of the FFTW library.

FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains static cross-compiled library

%{?mingw_debug_package}

%prep
%setup -q -n %{mingw_pkg_name}-%{version}


%build
#export F77=gfortran

BASEFLAGS="--enable-shared --disable-dependency-tracking --disable-threads"
%if %{openmp}
BASEFLAGS="$BASEFLAGS --enable-openmp"
%endif

# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

# Corresponding flags
prec_flags[0]=--enable-single
prec_flags[1]=--enable-double
prec_flags[2]=--enable-long-double
prec_flags[3]=--enable-quad-precision

# Loop over precisions
for((iprec=0;iprec<4;iprec++))
do
  export MINGW_BUILDDIR_SUFFIX=${prec_name[iprec]}
  export MINGW_CONFIGURE_ARGS="${BASEFLAGS} ${prec_flags[iprec]}"
  %{mingw_configure} 
  #sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
  #sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
  %{mingw_make} %{?_smp_mflags}
done

%install
# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

rm -rf %{buildroot}
for((iprec=0;iprec<4;iprec++))
do
  export MINGW_BUILDDIR_SUFFIX=${prec_name[iprec]}
 %{mingw_make} install DESTDIR=%{buildroot}
done
rm -f %{buildroot}%{mingw32_infodir}/dir
rm -f %{buildroot}%{mingw64_infodir}/dir
rm -f %{buildroot}%{mingw32_libdir}/*.la
rm -f %{buildroot}%{mingw64_libdir}/*.la

rm -f %{buildroot}%{mingw32_bindir}/fftw*-wisdom*
rm -f %{buildroot}%{mingw64_bindir}/fftw*-wisdom*
rm -rf %{buildroot}%{mingw32_infodir}
rm -rf %{buildroot}%{mingw64_infodir}
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}


%clean
rm -rf %{buildroot}

%files -n mingw32-%{mingw_pkg_name}
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{mingw32_bindir}/libfftw3f-3.dll
%{mingw32_bindir}/libfftw3-3.dll
%{mingw32_bindir}/libfftw3l-3.dll
#{mingw32_bindir}/libfftw3q-3.dll
%{mingw32_libdir}/libfftw3f.dll.a
%{mingw32_libdir}/libfftw3.dll.a
%{mingw32_libdir}/libfftw3l.dll.a
#{mingw32_libdir}/libfftw3q.dll.a
%if %{openmp}
%{mingw32_bindir}/libfftw3f_omp-3.dll
%{mingw32_bindir}/libfftw3_omp-3.dll
%{mingw32_bindir}/libfftw3l_omp-3.dll
#{mingw32_bindir}/libfftw3q_omp-3.dll
%{mingw32_libdir}/libfftw3f_omp.dll.a
%{mingw32_libdir}/libfftw3_omp.dll.a
%{mingw32_libdir}/libfftw3l_omp.dll.a
#{mingw32_libdir}/libfftw3q_omp.dll.a
%endif
%{mingw32_includedir}/fftw3*
%{mingw32_libdir}/pkgconfig/fftw3f.pc
%{mingw32_libdir}/pkgconfig/fftw3.pc
%{mingw32_libdir}/pkgconfig/fftw3l.pc
%{mingw32_libdir}/pkgconfig/fftw3q.pc

%files -n mingw32-%{mingw_pkg_name}-static
%defattr(-,root,root,-)
%{mingw32_libdir}/libfftw3f.a
%{mingw32_libdir}/libfftw3.a
%{mingw32_libdir}/libfftw3l.a
%{mingw32_libdir}/libfftw3q.a

%files -n mingw64-%{mingw_pkg_name}
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{mingw64_bindir}/libfftw3f-3.dll
%{mingw64_bindir}/libfftw3-3.dll
%{mingw64_bindir}/libfftw3l-3.dll
#{mingw64_bindir}/libfftw3q-3.dll
%{mingw64_libdir}/libfftw3f.dll.a
%{mingw64_libdir}/libfftw3.dll.a
%{mingw64_libdir}/libfftw3l.dll.a
#{mingw64_libdir}/libfftw3q.dll.a
%if %{openmp}
%{mingw64_bindir}/libfftw3f_omp-3.dll
%{mingw64_bindir}/libfftw3_omp-3.dll
%{mingw64_bindir}/libfftw3l_omp-3.dll
#{mingw64_bindir}/libfftw3q_omp-3.dll
%{mingw64_libdir}/libfftw3f_omp.dll.a
%{mingw64_libdir}/libfftw3_omp.dll.a
%{mingw64_libdir}/libfftw3l_omp.dll.a
#{mingw64_libdir}/libfftw3q_omp.dll.a
%endif
%{mingw64_includedir}/fftw3*
%{mingw64_libdir}/pkgconfig/fftw3f.pc
%{mingw64_libdir}/pkgconfig/fftw3.pc
%{mingw64_libdir}/pkgconfig/fftw3l.pc
%{mingw64_libdir}/pkgconfig/fftw3q.pc

%files -n mingw64-%{mingw_pkg_name}-static
%defattr(-,root,root,-)
%{mingw64_libdir}/libfftw3f.a
%{mingw64_libdir}/libfftw3.a
%{mingw64_libdir}/libfftw3l.a
%{mingw64_libdir}/libfftw3q.a

%changelog
* Sat Jan 19 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.3-1
- update to 3.3.3

* Sat Aug 25 2012 Thomas Sailer <t.sailer@alumni.ethz.ch> - 3.3.1-1
- create from native spec file

