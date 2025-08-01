Summary:	CDF (Common Data Format) software
Summary(pl.UTF-8):	Oprogramowanie obsługujące CDF (Common Data Format)
Name:		cdflib
Version:	3.7.1
Release:	1
License:	freely usable, non-commercially distributable
Group:		Libraries
# see https://cdf.gsfc.nasa.gov/html/sw_and_docs.html
Source0:	https://cdaweb.gsfc.nasa.gov/pub/software/cdf/dist/cdf37_1/linux/cdf37_1-dist-all.tar.gz
# Source0-md5:	0f434ffbb7f6ffe39b2bb20c5a940aee
Patch0:		%{name}-opt.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-no-common.patch
URL:		https://cdf.gsfc.nasa.gov/cdf_home.html
BuildRequires:	gcc-fortran >= 6:4.4.2
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CDF (Common Data Format) software.

%description -l pl.UTF-8
Oprogramowanie obsługujące CDF (Common Data Format).

%package devel
Summary:	C and Fortran header files for CDF library
Summary(pl.UTF-8):	Pliki nagłówkowe C i Fortranu do biblioteki CDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
C and Fortran header files for CDF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe C i Fortranu do biblioteki CDF.

%package static
Summary:	Static CDF library
Summary(pl.UTF-8):	Statyczna biblioteka CDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CDF library.

%description static -l pl.UTF-8
Statyczna biblioteka CDF.

%package -n java-cdflib
Summary:	Java API for CDF library
Summary(pl.UTF-8):	API Javy do biblioteki CDF
Group:		Libraries/Java
URL:		http://cdf.gsfc.nasa.gov/cdfjava_doc/index.html
Requires:	%{name} = %{version}-%{release}

%description -n java-cdflib
Java API for CDF library.

%description -n java-cdflib -l pl.UTF-8
API Javy do biblioteki CDF.

%prep
%setup -q -n cdf37_1-dist
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

# note: included zlib (src/lib/zlib) is modified (at last public symbol names)

%build
%{__make} all \
	OS=linux \
	ENV=gnu \
	CC_linux_gnu="%{__cc}" \
	LD_linux_gnu="%{__cc}" \
	LIBCDFa="../lib/libcdf.so" \
	LIBs1="-L../lib -lcdf -lm" \
	LIBs2="-L../lib -lcdf -lncurses -lm" \
	UCOPTIONS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	INSTALLDIR=$RPM_BUILD_ROOT%{_prefix}

# resolve conflict with dcdflib.c
install -d $RPM_BUILD_ROOT%{_includedir}/cdf
%{__mv} $RPM_BUILD_ROOT%{_includedir}/*.{h,inc} $RPM_BUILD_ROOT%{_includedir}/cdf
%if "%{_lib}" != "lib"
%{__mv} $RPM_BUILD_ROOT%{_prefix}/{lib,%{_lib}}
%endif

install -d $RPM_BUILD_ROOT%{_datadir}/cdf
%{__mv} $RPM_BUILD_ROOT%{_prefix}/CDFLeapSeconds.txt $RPM_BUILD_ROOT%{_datadir}/cdf
%{__mv} $RPM_BUILD_ROOT%{_bindir}/definitions.* $RPM_BUILD_ROOT%{_datadir}/cdf

install -d $RPM_BUILD_ROOT%{_javadir}
cp -p cdfjava/classes/cdfjava.jar $RPM_BUILD_ROOT%{_javadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CDF_copyright.txt CHANGES.txt README_cdf_tools.txt Release.notes Welcome.txt
%attr(755,root,root) %{_bindir}/cdf*
%attr(755,root,root) %{_bindir}/skeletoncdf
%attr(755,root,root) %{_bindir}/skeletontable
%attr(755,root,root) %{_libdir}/libcdf.so.%{version}
%attr(755,root,root) %ghost %{_libdir}/libcdf.so.3
%{_libdir}/cdf
%{_datadir}/cdf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdf.so
%dir %{_includedir}/cdf
# C
%{_includedir}/cdf/cdf.h
%{_includedir}/cdf/cdfconfig.h
%{_includedir}/cdf/cdfdist.h
%{_includedir}/cdf/cdflib.h
%{_includedir}/cdf/cdflib64.h
# fortran
%{_includedir}/cdf/cdf.inc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcdf.a

%files -n java-cdflib
%defattr(644,root,root,755)
%{_javadir}/cdfjava.jar
