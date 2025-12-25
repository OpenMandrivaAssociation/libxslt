# Make python "great" again
%define _disable_ld_no_undefined 1

%global build_ldflags %{build_ldflags} -Wl,--undefined-version

%define major 1
%define emajor 0
%define oldlibname %mklibname xslt 1
%define oldlibename %mklibname exslt 0
%define libname %mklibname xslt
%define libename %mklibname exslt
%define develname %mklibname xslt -d
%define beta %nil
%define _python_bytecompile_build 0

# libxslt is used by wine as well as some
# other libraries wine depends on
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%define oldlib32name libxslt1
%define oldlib32ename libexslt0
%define lib32name libxslt
%define lib32ename libexslt
%define devel32name libxslt-devel

%bcond_without python 

Name:		libxslt
Version:	1.1.45

%if "%{beta}" != ""
Release:	0.%{beta}.1
Source0:	ftp://xmlsoft.org/libxslt/libxslt-%{version}-%{beta}.tar.gz
%else
Release:	2
Source0:	https://download.gnome.org/sources/libxslt/1.1/%{name}-%{version}.tar.xz
%endif

Summary:	Library providing XSLT support
License:	MIT
Group:		System/Libraries
URL:		https://gitlab.gnome.org/GNOME/libxslt

BuildSystem:    cmake
BuildOption:    -DLIBXSLT_WITH_DEBUGGER=ON
%if %{with python}
BuildRequires:	pkgconfig(python)
BuildRequires:	python-libxml2
%if %{with compat32}
BuildRequires:  pkgconfig(python)
BuildOption:    -DPython_LIBRARIES="/usr/lib/python%{python3_version}"
BuildOption:    -DPython_EXECUTABLE="%{_bindir}/python"
BuildOption:    -DPython_INCLUDE_DIRS="%{_includedir}/python%{python3_version}"
%endif
%else
BuildOption:    -DLIBXSLT_WITH_PYTHON=OFF
%endif
BuildOption:    -DLIBSXLT_WITH_CRYPTO=ON

BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	gettext-devel
%if %{with compat32}
BuildRequires:	devel(libgcrypt)
BuildRequires:	devel(libgpg-error)
BuildRequires:	devel(libxml2)
%endif

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%package -n xsltproc
Summary:	XSLT processor using libxslt
Group:		System/Libraries
Provides:	libxslt-proc = %{version}-%{release}

%description -n xsltproc
This package provides an XSLT processor based on the libxslt C library.
It allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%package -n %{libname}
Summary:	Library providing XSLT support
Group:		System/Libraries
# Renamed after 6.0 2025-09-24
%rename %{oldlibname}

%description  -n %{libname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.
A xslt processor based on this library, named xsltproc, is provided by
the libxslt-proc package.

%package -n %{libename}
Summary:	Library providing EXSLT support
Group:		System/Libraries
# Renamed after 6.0 2025-09-24
%rename %{oldlibename}

%description  -n %{libename}
This C library adds EXSLT extensions to libxslt.

%package -n %{develname}
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libename} = %{version}-%{release}
Requires:	pkgconfig(libxml-2.0)
Obsoletes:	%{mklibname xslt 1 -d} < %{version}-%{release}

%description -n %{develname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%if %{with compat32}
%if "%{name}" != "%{lib32name}"
%package -n %{lib32name}
Summary:	Library providing XSLT support (32-bit)
Group:		System/Libraries
%rename %{olblib32name}

%description  -n %{lib32name}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.
A xslt processor based on this library, named xsltproc, is provided by
the libxslt-proc package.
%endif

%package -n %{lib32ename}
Summary:	Library providing EXSLT support (32-bit)
Group:		System/Libraries
%rename %{oldlib32ename}

%description  -n %{lib32ename}
This C library adds EXSLT extensions to libxslt.

%package -n %{devel32name}
Summary:	Libraries, includes, etc. to develop XML and HTML applications (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib32ename} = %{version}-%{release}
Requires:	%{develname} = %{EVRD}
Requires:	devel(libxml2)

%description -n %{devel32name}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.
%endif

%if %{with python}
%package -n python-%{name}
Summary:	Python bindings for the libxslt library
Group:		Development/Python
Obsoletes:	%{name}-python < %{version}-%{release}
Requires: 	%{libname} = %{version}-%{release}
Requires:	python
Requires:	python-libxml2

%description -n python-%{name}
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.
%endif

%files -n xsltproc
%{_bindir}/xsltproc
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libxslt.so.%{major}*

%files -n %{libename}
%{_libdir}/libexslt.so.%{emajor}*

%if %{with python}
%files -n python-%{name}
%defattr(0644,root, root,0755)
%{_prefix}/lib/debug/usr/python/*.debug
%{_prefix}/python/%name.py
%{_prefix}/python/%{name}mod.*
%endif

%files -n %{develname}
%doc %{_datadir}/doc/libxslt/
%{_mandir}/man3/*
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/libxslt-%version/*.cmake


%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libxslt.so.%{major}*

%files -n %{lib32ename}
%{_prefix}/lib/libexslt.so.%{emajor}*

%files -n %{devel32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/*.sh
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/cmake/libxslt-%version/*.cmake

%endif
