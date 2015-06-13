Summary: perl for wandbox
Name: wandbox-perl-5.18.0
Version: 5.18.0
Release: 1
License: GPL1+
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: perl
BuildRequires: libdb-dev libgdbm-dev netbase zlib1g-dev libbz2-dev
Source0: http://www.cpan.org/src/5.0/perl-%{version}.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/perl-%{version}

%description
a component of wandbox service

%prep
%setup -q -n perl-%{version}

%build
./Configure -des -Dprefix=%{_prefix}
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/man
chmod -R +w %{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}
%{_prefix}/lib

%changelog
 * Mon Jan 27 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

