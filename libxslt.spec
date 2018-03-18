%define major 1
%define emajor 0
%define libname %mklibname xslt %{major}
%define libename %mklibname exslt %{emajor}
%define develname %mklibname xslt -d

Name:		libxslt
Version:	1.1.32
Release:	2
Summary:	Library providing XSLT support
License:	MIT
Group:		System/Libraries
URL:		http://xmlsoft.org/XSLT/
Source0:	ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.gz
# S1 was taken from libxslt-1.1.26
Source1:	autogen.sh
Patch0:		multilib.patch
Patch1:		libxslt-1.1.26-utf8-docs.patch
Patch3:		libxslt-1.1.28-detect-python3.patch
Patch4:		libxslt-1.1.28-python3.patch
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(icu-i18n)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-libxml2
BuildRequires:	pkgconfig(libgcrypt)

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

%package -n %{develname}
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libename} = %{version}-%{release}
Requires:	libxml2-devel
Obsoletes:	%{mklibname xslt 1 -d} < %{version}-%{release}

%description -n %{develname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%prep
%setup -q
%autopatch -p1

mkdir -p python/examples
cp -a python/tests/*.{py,xml,xsl} python/examples

cp %{SOURCE1} autogen.sh
chmod 755 autogen.sh

%build
NOCONFIGURE=yes ./autogen.sh
%configure --disable-static
%make_build

%check
make check

%install
%make_install

# remove unpackaged files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version} %{buildroot}%{_docdir}/%{name}-python-%{version}

%if %{mdvver} <= 3000000
%multiarch_binaries %{buildroot}%{_bindir}/xslt-config
%endif

%files -n xsltproc
%{_bindir}/xsltproc
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libxslt.so.%{major}*

%files -n %{libename}
%{_libdir}/libexslt.so.%{emajor}*

%files -n python-%{name}
%defattr(0644,root, root,0755)
%doc AUTHORS README Copyright FEATURES python/TODO python/examples python/libxsltclass.txt
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py*

%files -n %{develname}
%doc doc/*.html doc/tutorial doc/html
%{_mandir}/man3/*
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%if %{mdvver} <= 3000000
%{multiarch_bindir}/xslt-config
%endif
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*
