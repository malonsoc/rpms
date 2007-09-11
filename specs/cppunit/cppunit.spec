# $Id$
# Authority:    hadams

Name: cppunit
Version: 1.12.0
Release: 3

Summary: C++ unit testing framework
License: LGPL
Group: Development/Libraries
Url: http://cppunit.sourceforge.net/
Source: http://download.sf.net/cppunit/cppunit-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: doxygen, graphviz

%description
CppUnit is the C++ port of the famous JUnit framework for unit testing.
Test output is in XML for automatic testing and GUI based for supervised tests.

%package devel
Summary: Libraries and headers for cppunit development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the libraries and headers necessary for developing
programs that use cppunit.

%package doc
Summary: HTML formatted API documention for cppunit
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
The cppunit-doc package contains HTML formatted API documention generated by
the popular doxygen documentation generation tool.

%prep
%setup -q

%build
%configure --enable-doxygen
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
# remove double of doc
rm -rf $RPM_BUILD_ROOT/%{_datadir}/cppunit

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/DllPlugInTester
%{_mandir}/man1/*
%{_datadir}/aclocal/*
%{_libdir}/libcppunit*.so.*
%doc AUTHORS COPYING NEWS README THANKS ChangeLog TODO BUGS doc/FAQ

%files devel
%defattr(-,root,root,-)
%{_bindir}/cppunit-config
%{_includedir}/cppunit
%{_libdir}/libcppunit.a
%{_libdir}/libcppunit.so
%{_libdir}/pkgconfig/cppunit.pc

%files doc
%defattr(-,root,root,-)
%doc doc/html/*

%changelog
* Thu Sep 11 2007 Heiko Adams <info@fedora-blog.de> 1.12.0-3
- rebuild for rpmforge

* Sun Sep 10 2006 Patrice Dumas <pertusus@free.fr> 1.12.0-2
- rebuild for FC6

* Wed Jul  5 2006 Patrice Dumas <pertusus@free.fr> 1.12.0-1
- update to 1.12

* Sun May 21 2006 Patrice Dumas <pertusus@free.fr> 1.11.6-1
- update to 1.11.6

* Wed Dec 21 2005 Patrice Dumas <pertusus@free.fr> 1.11.4-1
- update

* Mon Aug 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.11.0-2
- various cleanups

* Mon Jul  4 2005 Patrice Dumas <pertusus@free.fr> 1.11.0-1
- update using the fedora template 
 
* Sat Apr 14 2001 Bastiaan Bakker <bastiaan.bakker@lifeline.nl>
- Initial release
