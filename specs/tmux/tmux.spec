# $Id$
# Authority: dag

Summary: Terminal multiplexer program
Name: tmux
Version: 1.0
Release: 1%{?dist}
License: BSD
Group: Applications/System
URL: http://tmux.sourceforge.net/

Source: http://downloads.sourceforge.net/tmux/tmux-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
tmux is a "terminal multiplexer". It allows a number of terminals (or windows)
to be accessed and controlled from a single terminal. It is intended to be
a simple, modern, BSD-licensed alternative to programs such as GNU screen.

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
#%{__make} install DESTDIR="%{buildroot}"
%{__install} -Dp -m0755 tmux %{buildroot}%{_bindir}/tmux
%{__install} -Dp -m0644 tmux.1 %{buildroot}%{_mandir}/man1/tmux.1

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc NOTES TODO
%doc %{_mandir}/man1/tmux.1*
%{_bindir}/tmux

%changelog
* Thu Sep 24 2009 Dag Wieers <dag@wieers.com> - 1.0-1
- Updated to release 1.0.

* Fri Jul 10 2009 Dag Wieers <dag@wieers.com> - 0.9-1
- Updated to release 0.9.

* Mon Apr 27 2009 Dag Wieers <dag@wieers.com> - 0.8-1
- Updated to release 0.8.

* Sun Feb 08 2009 Dag Wieers <dag@wieers.com> - 0.7-1
- Updated to release 0.7.

* Mon Jan 19 2009 Dag Wieers <dag@wieers.com> - 0.6-1
- Updated to release 0.6.

* Mon Nov 17 2008 Dag Wieers <dag@wieers.com> - 0.5-1
- Updated to release 0.5.

* Fri Jul 04 2008 Dag Wieers <dag@wieers.com> - 0.4-1
- Updated to release 0.4.

* Thu Jun 19 2008 Dag Wieers <dag@wieers.com> - 0.3-1
- Updated to release 0.3.

* Fri Jun 06 2008 Dag Wieers <dag@wieers.com> - 0.2-1
- Initial package. (using DAR)
