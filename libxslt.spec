%define xml_version_required 2.6.27
%define major 1
%define libname %mklibname xslt %{major}
%define develname %mklibname xslt -d

Name:    libxslt
Version: 1.1.26
Release: 5
Summary: Library providing XSLT support
License: MIT
Group: System/Libraries
URL: http://xmlsoft.org/XSLT/
Source0: ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.gz
# fix python linking
Patch1: libxslt-1.1.25-fix-python-linking.patch
Requires: libxml2 >= %{xml_version_required}
BuildRequires: libxml2-devel >= %{xml_version_required}
BuildRequires: python-devel >= %{pyver}
BuildRequires: python-libxml2 >= %{xml_version_required}
BuildRequires: libgcrypt-devel
BuildRequires: autoconf automake libtool

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism.

%package -n xsltproc
Summary: XSLT processor using libxslt
Group: System/Libraries
Obsoletes: libxslt-proc < %{version}-8
Provides: libxslt-proc = %{version}-%{release}

%description -n xsltproc
This package provides an XSLT processor based on the libxslt C library. 
It allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%package -n %{libname}
Summary: Library providing XSLT support
Group: System/Libraries

%description  -n %{libname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 
A xslt processor based on this library, named xsltproc, is provided by 
the libxslt-proc package.

%package -n python-%{name}
Summary: Python bindings for the libxslt library
Group: Development/Python
Obsoletes: %{name}-python < %{version}-%{release}
Requires: %{libname} >= %{version}-%{release}
Requires: python >= %{pyver}
Requires: python-libxml2 >= %{xml_version_required}

%description -n python-%{name}
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.

%package -n %{develname}
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}
Requires: libxml2-devel >= %{xml_version_required}
Obsoletes: %{mklibname xslt 1 -d} < %{version}-%{release}

%description -n %{develname}
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. 

%prep
%setup -q
%patch1 -p1 -b .fix-python-linking

%{__mkdir_p} python/examples
%{__cp} -a python/tests/*.{py,xml,xsl} python/examples

#needed by patch1 
autoreconf -fi

%build
%configure2_5x
%make

%install
%{__rm} -rf %{buildroot}

%makeinstall_std

# remove unpackaged files
%{__rm} -rf %{buildroot}%{_docdir}/%{name}-%{version} %{buildroot}%{_docdir}/%{name}-python-%{version} \
  %{buildroot}%{py_platsitedir}/*.{la,a}

%multiarch_binaries %{buildroot}%{_bindir}/xslt-config

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n xsltproc
%{_bindir}/xsltproc
%{_mandir}/man1/*

%files -n %{libname}
%doc AUTHORS NEWS README Copyright FEATURES TODO
%{_libdir}/lib*.so.*

%files -n python-%{name}
%doc AUTHORS README Copyright FEATURES python/TODO python/examples python/libxsltclass.txt
%defattr(-, root, root)
%{py_platsitedir}/*.so
%{py_platsitedir}/*.py

%files -n %{develname}
%doc doc/*.html doc/tutorial doc/html
%{_mandir}/man3/*
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_includedir}/*
%{multiarch_bindir}/xslt-config
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*
