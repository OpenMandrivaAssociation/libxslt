%define major 1
%define emajor 0
%define libname %mklibname xslt %{major}
%define libename %mklibname exslt %{emajor}
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
%define lib32name libxslt%{major}
%define lib32ename libexslt%{emajor}
%define devel32name libxslt-devel

%bcond_without python

Name:		libxslt
Version:	1.1.35
%if "%{beta}" != ""
Release:	0.%{beta}.1
Source0:	ftp://xmlsoft.org/libxslt/libxslt-%{version}-%{beta}.tar.gz
%else
Release:	1
Source0:  https://download.gnome.org/sources/libxslt/1.1/%{name}-%{version}.tar.xz
#Source0:	ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.gz
%endif
Summary:	Library providing XSLT support
License:	MIT
Group:		System/Libraries
URL:		http://xmlsoft.org/XSLT/
# S1 was taken from libxslt-1.1.26
Source1:	autogen.sh
Patch0:		multilib.patch
Patch1:		libxslt-1.1.26-utf8-docs.patch

BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(icu-i18n)
%if %{with python}
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-libxml2
%endif
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

%description  -n %{libname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.
A xslt processor based on this library, named xsltproc, is provided by
the libxslt-proc package.

%package -n %{libename}
Summary:	Library providing EXSLT support
Group:		System/Libraries

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
%package -n %{lib32name}
Summary:	Library providing XSLT support (32-bit)
Group:		System/Libraries

%description  -n %{lib32name}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.
A xslt processor based on this library, named xsltproc, is provided by
the libxslt-proc package.

%package -n %{lib32ename}
Summary:	Library providing EXSLT support (32-bit)
Group:		System/Libraries

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

%prep
%autosetup -p1

mkdir -p python/examples
cp -a python/tests/*.{py,xml,xsl} python/examples

cp %{SOURCE1} autogen.sh
chmod 755 autogen.sh
NOCONFIGURE=yes ./autogen.sh

export CONFIGURE_TOP="`pwd`"
%if %{with compat32}
mkdir build32
cd build32
%configure32 --without-python
cd ..
%endif
mkdir build
cd build
%configure %{?_with_python}

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

# remove unpackaged files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version} %{buildroot}%{_docdir}/%{name}-python-%{version}

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
%doc AUTHORS README Copyright FEATURES python/TODO python/examples python/libxsltclass.txt
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py*
%endif

%files -n %{develname}
%doc doc/*.html doc/tutorial doc/html
%{_mandir}/man3/*
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libxslt.so.%{major}*

%files -n %{lib32ename}
%{_prefix}/lib/libexslt.so.%{emajor}*

%files -n %{devel32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/*.sh
%{_prefix}/lib/pkgconfig/*.pc
%endif
