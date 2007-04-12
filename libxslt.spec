%define mdkversion             %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)

%define xml_version_required 2.6.27
%define major 1
%define libname %mklibname xslt %{major}

%if %mdkversion >= 720 && %mdkversion <= 800
%define py_ver      2.0
%endif

%if %mdkversion == 810
%define py_ver      2.1
%endif

%if %mdkversion >= 820 && %mdkversion <= 910
%define py_ver      2.2
%endif

%if %mdkversion >= 920
%define py_ver      2.3
%endif

%if %mdkversion <= 1000
%define __libtoolize true
%endif

%if %mdkversion >= 1020
%define py_ver      %pyver
%endif

%if %mdkversion >= 920
%define pylibxml2   python-libxml2
%else
%define pylibxml2   libxml2-python
%endif

Summary: Library providing XSLT support
Name:    libxslt
Version: 1.1.20
Release: %mkrel 2
License: MIT
Group: System/Libraries
Source: ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: libxml2 >= %{xml_version_required}
BuildRequires: libxml2-devel >= %{xml_version_required}
BuildRequires: python-devel >= %{py_ver}
BuildRequires: %{pylibxml2} >= %{xml_version_required}
BuildRequires: libgcrypt-devel
%if %mdkversion >= 1020
BuildRequires:        multiarch-utils >= 1.0.3
%endif
URL: http://xmlsoft.org/XSLT/

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%package proc
Summary: XSLT processor using libxslt
Group: System/Libraries
Requires: %{libname} = %{version}

%description proc
This package provides an XSLT processor based on the libxslt C library. 
It allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%package -n %{libname}
Summary: Library providing XSLT support
Group: System/Libraries
Requires: libxml2 >= %{xml_version_required}

%description  -n %{libname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 
A xslt processor based on this library, named xsltproc, is provided by 
the libxslt-proc package.

%package -n python-%{name}
Summary: Python bindings for the libxslt library
Group: Development/Python
Obsoletes: %{name}-python
Requires: %{libname} = %{version}
Requires: python >= %{py_ver}
Requires: %{pylibxml2} >= %{xml_version_required}

%description -n python-%{name}
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.


%package -n %{libname}-devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/C
Provides: %{_lib}%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}
Requires: libxml2-devel >= %{xml_version_required}

%description -n %{libname}-devel
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%prep
%setup -q
%{__mkdir_p} python/examples
%{__cp} -a python/tests/*.{py,xml,xsl} python/examples

%build
%if %mdkversion <= 810
%{configure}
%else
%{configure2_5x}
%endif

%{make}

%check
%{__make} check

%install
%{__rm} -rf %{buildroot}
%{makeinstall}

# remove unpackaged files
%{__rm} -rf %{buildroot}%{_docdir}/%{name}-%{version} %{buildroot}%{_docdir}/%{name}-python-%{version} \
  %{buildroot}%{_libdir}/python%{py_ver}/site-packages/*.{la,a}

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/xslt-config
%endif

%clean
%{__rm} -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig 

%postun -n %{libname} -p /sbin/ldconfig

%files proc
%defattr(-, root, root)
%{_bindir}/xsltproc
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-, root, root)
%doc AUTHORS NEWS README Copyright FEATURES TODO
%{_libdir}/lib*.so.*

%files -n python-%{name}
%defattr(-, root, root)
%doc AUTHORS README Copyright FEATURES python/TODO python/examples python/libxsltclass.txt
%{_libdir}/python%{py_ver}/site-packages/*.so
%{_libdir}/python%{py_ver}/site-packages/*.py

%files -n %{libname}-devel
%defattr(-, root, root)
%doc doc/*.html doc/tutorial doc/html
%{_mandir}/man3/*
%{_libdir}/lib*.so
%{_libdir}/*a
%{_libdir}/*.sh
%{_includedir}/*
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/xslt-config
%endif
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*


