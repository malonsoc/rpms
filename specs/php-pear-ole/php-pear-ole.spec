# $Id$

%define php_dir %(eval "`pear config-get php_dir`"; echo $php_dir)

Summary: PEAR package for reading and writing OLE containers
Name: php-pear-ole
Version: 0.5
Release: 1
License: PHP
Group: Development/Languages
URL: http://pear.php.net/package/OLE/
Source1: http://pear.php.net/get/OLE-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: php
BuildRequires: php

%description
This package allows reading and writing of OLE (Object Linking and Embedding)
files, the format used as container for Excel, Word and other MS file formats.
Documentation for the OLE format can be found at:
http://user.cs.tu-berlin.de/~schwartz/pmh/guide.html


%prep


%install
rm -rf %{buildroot}
pear install -R %{buildroot} -n %{SOURCE1}
# Remove .filemap and .lock, we don't want to include those
rm -f %{buildroot}%{php_dir}/{.filemap,.lock}


%clean
rm -rf %{buildroot}


%files
%defattr(0644, root, root, 0755)
%{php_dir}


%changelog
* Thu Mar 11 2004 Matthias Saou <http://freshrpms.net/> 0.5-1
- Initial RPM release.

