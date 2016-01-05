Summary: ruby for wandbox
Name: wandbox-ruby-2.0.0p647
Version: 2.0.0p647
Release: 1
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl libreadline6 libreadline6-dev libssl-dev libyaml-dev libsqlite3-0 libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev ssl-cert subversion
Source0: http://cache.ruby-lang.org/pub/ruby/./ruby-2.0.0-p647.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/ruby-2.0.0p647

%description
a component of wandbox service

%prep
%setup -q -n ruby-2.0.0-p647

%build
%{configure}
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}
%{_includedir}
%{_libdir}

%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Mon Jan 27 2014 kikairoya <kikairoya@gmail.com>
- Initial build
