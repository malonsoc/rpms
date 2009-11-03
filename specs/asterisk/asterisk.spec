# $Id$
# Authority: matthias

# The user and group names
%define uname asterisk
%define gname asterisk

Summary: PBX and telephony application and toolkit
Name: asterisk
Version: 1.2.15
Release: 1%{?dist}
License: GPL
Group: Applications/Internet
URL: http://www.asterisk.org/
Source0: http://ftp.digium.com/pub/asterisk/asterisk-%{version}.tar.gz
Source1: asterisk.init
Source2: asterisk.logrotate
Patch0: asterisk-1.0.9-agi_streamfile_video_raw_special.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: perl, zaptel
BuildRequires: openssl-devel, zlib-devel, perl, bison, speex-devel, doxygen
BuildRequires: zaptel-devel, gtk+-devel, newt-devel, ncurses-devel, libpri-devel
# for /usr/include/linux/compiler.h :
BuildRequires: glibc-kernheaders
%{!?_without_postgresql:BuildRequires: postgresql-devel}
%{!?_without_sqlite:BuildRequires: sqlite2-devel}

%description
Asterisk is an Open Source PBX and telephony development platform that
can both replace a conventional PBX and act as a platform for developing
custom telephony applications for delivering dynamic content over a
telephone similarly to how one can deliver dynamic content through a
web browser using CGI and a web server.

Asterisk talks to a variety of telephony hardware including BRI, PRI,
POTS, and IP telephony clients using the Inter-Asterisk eXchange
protocol (e.g. gnophone or miniphone).


%package devel
Summary: Header files and development documentation for Asterisk
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package contains the header files needed to compile modules for Asterisk
as well as the developer documentation generated by doxygen.


%prep
%setup
%patch0 -p0
# Replace /var/run by /var/run/asterisk since we don't run as root
%{__perl} -pi -e 's|/var/run$|%{_var}/run/asterisk|g' Makefile
# Fix lib vs. lib64 directory
%{__perl} -pi -e 's|/usr/lib/asterisk$|%{_libdir}/asterisk|g' Makefile
%{__perl} -pi -e 's|lib/libpri.so|%{_lib}/libpri.so|g' channels/Makefile


%build
%{__make} PROC="%{_arch}" OPTIMIZE="%{optflags}"
%{__make} progdocs


%install
%{__rm} -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

# Install all sample config files
%{__make} samples DESTDIR=%{buildroot}

%{__install} -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/rc.d/init.d/asterisk

%{__install} -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/logrotate.d/asterisk

# We need that directory, see above
%{__mkdir_p} %{buildroot}%{_var}/run/asterisk

# Install demo sounds
for file in sounds/demo-*; do
    %{__install} -p -m 0644 $file %{buildroot}%{_var}/lib/asterisk/sounds/
done
for file in sounds/*.mp3; do
    %{__install} -p -m 0644 $file %{buildroot}%{_var}/lib/asterisk/mohmp3/
done


%clean
%{__rm} -rf %{buildroot}


%pre
# Add the "asterisk" user
/usr/sbin/useradd -c "Asterisk PBX" -G tty -s /sbin/nologin -r \
    -d "%{_var}/lib/asterisk" %{uname} 2>/dev/null || :

%post
# Register the asterisk service
/sbin/chkconfig --add asterisk
# Fix the permission on tty9
/bin/chmod g+r /dev/tty9

%preun
if [ $1 -eq 0 ]; then
    /sbin/service asterisk stop >/dev/null 2>&1
    /sbin/chkconfig --del asterisk
fi


%files
%defattr(-, root, root, 0755)
%doc BUGS ChangeLog configs/ CREDITS doc/*.txt HARDWARE LICENSE README SECURITY
%doc sounds.txt
%attr(750, %{uname}, %{gname}) %dir %{_sysconfdir}/asterisk
%attr(640, %{uname}, %{gname}) %config(noreplace) %{_sysconfdir}/asterisk/*.conf
%attr(640, %{uname}, %{gname}) %config(noreplace) %{_sysconfdir}/asterisk/*.adsi
%attr(640, %{uname}, %{gname}) %config(noreplace) %{_sysconfdir}/asterisk/*.ael
%config(noreplace) %{_sysconfdir}/logrotate.d/asterisk
%{_sysconfdir}/rc.d/init.d/asterisk
%{_libdir}/asterisk/
%{_sbindir}/*
%{_mandir}/man8/*.8*
%attr(-  , %{uname}, %{gname}) %{_var}/lib/asterisk/
%attr(750, %{uname}, %{gname}) %{_var}/run/asterisk/
%attr(750, %{uname}, %{gname}) %dir %{_var}/log/asterisk/
%attr(750, %{uname}, %{gname}) %dir %{_var}/log/asterisk/cdr-csv/
%attr(750, %{uname}, %{gname}) %dir %{_var}/log/asterisk/cdr-custom/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/
#                                   %{_var}/spool/asterisk/vm/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/voicemail/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/voicemail/default/
%attr(750, %{uname}, %{gname}) %dir %{_var}/spool/asterisk/voicemail/default/1234/
                                    %{_var}/spool/asterisk/voicemail/default/1234/*.gsm


%files devel
%defattr(-, root, root, 0755)
%doc doc/api/html/*
%{_includedir}/asterisk/


%changelog
* Mon Feb 12 2007 Matthias Saou <http://freshrpms.net> 1.2.15-1
- Update to 1.2.15.

* Fri Nov 24 2006 Matthias Saou <http://freshrpms.net> 1.2.13-1
- Update to 1.2.13.

* Thu Sep  7 2006 Matthias Saou <http://freshrpms.net> 1.2.11-1
- Update to 1.2.11.

* Thu May  4 2006 Matthias Saou <http://freshrpms.net> 1.2.7.1-1
- Update to 1.2.7.1.

* Thu Mar 23 2006 Matthias Saou <http://freshrpms.net> 1.2.5-4
- Add missing log directories, cdr-csv and cdr-custom.
- Add logrotate entry.

* Mon Mar 20 2006 Matthias Saou <http://freshrpms.net> 1.2.5-3
- Add libpri-devel build requirement to enable libpri support.
- Fix libpri detection on 64bit archs.

* Tue Mar  7 2006 Matthias Saou <http://freshrpms.net> 1.2.5-1
- Update to 1.2.5.

* Tue Jan 31 2006 Matthias Saou <http://freshrpms.net> 1.2.4-1
- Update to 1.2.4.
- Change sqlite-devel build requirement to sqlite2-devel.
- Remove MySQL stuff from the spec since it's been removed from asterisk
  (licensing issues).

* Fri Jan 27 2006 Matthias Saou <http://freshrpms.net> 1.2.3-1
- Update to 1.2.3.
- Fix build requirement zaptel -> zaptel-devel.

* Thu Dec  1 2005 Matthias Saou <http://freshrpms.net> 1.2.0-2
- Remove the fix that added /usr/sbin/ in the safe_asterisk script, as it is
  no longer needed, thanks to "${ASTSBINDIR}".

* Fri Nov 25 2005 Matthias Saou <http://freshrpms.net> 1.2.0-1
- Update to 1.2.0.
- No more spool/asterisk/vm/ (why?).

* Thu Oct 27 2005 Matthias Saou <http://freshrpms.net> 1.0.9-2
- Add agi_streamfile_video_raw_special patch.

* Tue Aug 23 2005 Matthias Saou <http://freshrpms.net> 1.0.9-1
- Update to 1.0.9.
- Change ASTLIBDIR to fix lib64 file location issue.

* Tue Apr  5 2005 Matthias Saou <http://freshrpms.net> 1.0.7-1
- Update to 1.0.7.

* Tue Mar  8 2005 Matthias Saou <http://freshrpms.net> 1.0.6-1
- Update to 1.0.6.

* Wed Feb  2 2005 Matthias Saou <http://freshrpms.net> 1.0.5-1
- Update to 1.0.5.
- Don't create nor include sbin/safe_asterisk.orig.
- Remove now unneeded absolute symlink overriding (they point inside now).
- Replace localstatedir by var for mdk compat and initrddir by full path.

* Fri Nov 26 2004 Matthias Saou <http://freshrpms.net> 1.0.2-1.20041125.0
- Update to CVS snapshot.

* Mon Oct 18 2004 Matthias Saou <http://freshrpms.net> 1.0.1-0
- Update to 1.0.1.

* Wed Sep  1 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC2.1
- Fix safe_asterisk again, ${CLIARGS} instead of ${ASTARGS}.

* Thu Aug 26 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC2.0
- Update to 1.0-RC2.
- Updated cdr patch, one fix made it upstream.

* Thu Jul 29 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC1.5
- Added Areski's cdr patch -2.
- Fix /var/run/asterisk -3.
- Change sample install to use the Makefile -4.
- Fix safe_asterisk -5.

* Mon Jul 26 2004 Matthias Saou <http://freshrpms.net> 1.0-0.RC1.1
- Update to 1.0-RC1.

* Thu Feb  5 2004 Matthias Saou <http://freshrpms.net> 0.7.2-1
- Update to 0.7.2.

* Tue Dec  2 2003 Matthias Saou <http://freshrpms.net>
- Updated to today's CVS code.
- Added asterisk-addons (cdr_addon_mysql).

* Tue Nov  4 2003 Matthias Saou <http://freshrpms.net>
- Added CVS release support.
- Changed ownership of the config directory to asterisk user.

* Fri Sep 19 2003 Matthias Saou <http://freshrpms.net>
- Initial RPM release.

