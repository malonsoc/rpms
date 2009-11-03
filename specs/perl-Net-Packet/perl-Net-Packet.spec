# $Id$
# Authority: dag
# Upstream: GomoR <perl$gomor,org>

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define real_name Net-Packet

Summary: Framework to easily send and receive frames from layer 2 to layer 7
Name: perl-Net-Packet
Version: 3.26
Release: 1%{?dist}
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Net-Packet/

Source: http://www.cpan.org/modules/by-module/Net/Net-Packet-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl

%description
A framework to easily send and receive frames from layer 2 to layer 7.

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install

### Clean up buildroot
find %{buildroot} -name .packlist -exec %{__rm} {} \;

### Clean up docs
find examples/ -type f -exec %{__chmod} a-x {} \;

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes LICENSE LICENSE.Artistic MANIFEST META.yml README examples/
%doc %{_mandir}/man3/Net::Packet.3pm*
%doc %{_mandir}/man3/Net::Packet::*.3pm*
%dir %{perl_vendorlib}/Net/
%{perl_vendorlib}/Net/Packet/
%{perl_vendorlib}/Net/Packet.pm

%changelog
* Wed May 14 2008 Dag Wieers <dag@wieers.com> - 3.26-1
- Updated to release 3.26.

* Mon Nov 26 2007 Dag Wieers <dag@wieers.com> - 3.25-1
- Initial package. (using DAR)
