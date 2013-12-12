%define old_libxslt		%mklibname xslt 1
%define old_libexslt		%mklibname exslt 0
%define old_libxslt_devel	%mklibname xslt -d
%define old_libexslt_devel	%mklibname exslt -d

Summary: Library providing the Gnome XSLT engine
Name: libxslt
Version: 1.1.28
Release: 5%{?dist}%{?extra_release}
License: MIT

Source: ftp://xmlsoft.org/XSLT/libxslt-%{version}.tar.gz
URL: http://xmlsoft.org/XSLT/
BuildRequires: libxml2-devel >= 2.6.27
BuildRequires: python-devel
BuildRequires: libxml2-python
BuildRequires: libgcrypt-devel
BuildRequires: automake autoconf

# Fedora specific patches
Patch0: multilib.patch
Patch1: libxslt-1.1.26-utf8-docs.patch
%rename xsltproc
%rename %{old_libxslt}
%rename %{old_libexslt}

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine

%package devel
Summary: Development files for %{name}

Requires: libxslt = %{version}-%{release}
Requires: libgcrypt-devel
%rename %{old_libxslt_devel}
%rename %{old_libexslt_devel}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package python
Summary: Python bindings for the libxslt library

Requires: libxslt = %{version}-%{release}
Requires: libxml2-python

%description python
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .utf8
# Now fix up the timestamps of patched docs files
# ChangeLog needs to be retouched before gzip as well
# since timestamp affects output
touch -r ChangeLog.utf8 ChangeLog
gzip -9 ChangeLog
touch -r ChangeLog.utf8 ChangeLog.gz
touch -r NEWS.utf8 NEWS

chmod 644 python/tests/*

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# multiarch crazyness on timestamp differences
touch -m --reference=$RPM_BUILD_ROOT/%{_includedir}/libxslt/xslt.h $RPM_BUILD_ROOT/%{_bindir}/xslt-config

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}{,-python}-%{version}

%check
make tests

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root,-)
%doc AUTHORS ChangeLog.gz NEWS README Copyright FEATURES
%doc %{_mandir}/man1/xsltproc.1*
%{_libdir}/lib*.so.*
%{_libdir}/libxslt-plugins
%{_bindir}/xsltproc

%files devel
%defattr(-, root, root,-)
%doc doc/libxslt-api.xml
%doc doc/libxslt-refs.xml
%doc doc/EXSLT/libexslt-api.xml
%doc doc/EXSLT/libexslt-refs.xml
%doc %{_mandir}/man3/libxslt.3*
%doc %{_mandir}/man3/libexslt.3*
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/images
%doc doc/tutorial
%doc doc/tutorial2
%doc doc/EXSLT
%{_libdir}/lib*.so
%{_libdir}/*.sh
%{_datadir}/aclocal/libxslt.m4
%{_includedir}/*
%{_bindir}/xslt-config
%{_libdir}/pkgconfig/libxslt.pc
%{_libdir}/pkgconfig/libexslt.pc

%files python
%defattr(-, root, root,-)
%{python_sitearch}/libxslt.py*
%{python_sitearch}/libxsltmod*
%doc python/libxsltclass.txt
%doc python/tests/*.py
%doc python/tests/*.xml
%doc python/tests/*.xsl
