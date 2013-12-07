%define major 1
%define exslt_major 0
%define libname %mklibname xslt %{major}
%define libename %mklibname exslt %{exslt_major}
%define devname %mklibname xslt -d

Summary:	Library providing XSLT support
Name:		libxslt
Version:	1.1.28
Release:	3
License:	MIT
Group:		System/Libraries
Url:		http://xmlsoft.org/XSLT/
Source0:	ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.gz
BuildRequires:	libtool
BuildRequires:	python-libxml2
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(python) >= %{py_ver}

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%package -n xsltproc
Summary:	XSLT processor using libxslt
Group:		System/Libraries

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
Summary:	Library providing XSLT support
Group:		System/Libraries
Conflicts:	%{_lib}xslt1 < 1.1.26-7

%description  -n %{libename}
This package contains the exslt shared library.

%package -n python-%{name}
Summary:	Python bindings for the libxslt library
Group:		Development/Python
Requires:	python >= %{py_ver}
Requires:	python-libxml2

%description -n python-%{name}
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.

%package -n %{devname}
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libename} = %{version}-%{release}

%description -n %{devname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%prep
%setup -q

mkdir -p python/examples
cp -a python/tests/*.{py,xml,xsl} python/examples

%build
%configure2_5x \
	--disable-static
%make

%install
%makeinstall_std

# remove unpackaged files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version} \
	%{buildroot}%{_docdir}/%{name}-python-%{version}

%multiarch_binaries %{buildroot}%{_bindir}/xslt-config

%files -n xsltproc
%doc AUTHORS NEWS README Copyright FEATURES TODO
%{_bindir}/xsltproc
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libxslt.so.%{major}*

%files -n %{libename}
%{_libdir}/libexslt.so.%{exslt_major}*

%files -n python-%{name}
%doc AUTHORS README Copyright FEATURES python/TODO python/examples python/libxsltclass.txt
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py

%files -n %{devname}
%doc doc/*.html doc/tutorial doc/html
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{multiarch_bindir}/xslt-config
%{_bindir}/xslt-config
%{_datadir}/aclocal/*
%{_mandir}/man3/*

