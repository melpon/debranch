Summary: perl for wandbox
Name: wandbox-perl-5.18.0
Version: 5.18.0
Release: 1
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# BuildRequires:
Source0: http://www.cpan.org/src/5.0/perl-%{version}.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/perl-%{version}
%global __os_install_post %{nil}

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0

%build
cd perl-%{version}
./Configure -des -Dprefix=%{_prefix}
%{__make}

%install
cd perl-%{version}
%{make_install}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
 * Fri Mar 14 2014 melpon <shigemasa7watanabe@gmail.com>
 - Initial build

