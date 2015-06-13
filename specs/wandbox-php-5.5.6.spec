Summary: php for wandbox
Name: wandbox-php-5.5.6
Version: 5.5.6
Release: 4
License: PHP
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libxml2-dev
Source0: http://jp1.php.net/distributions/php-5.5.6.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/php-%{version}
%define _sysconfdir %{_prefix}/etc

%description
a component of wandbox service

%prep
%setup -q -n php-%{version}

%build
%{configure} --disable-cgi
%{__make} %{_smp_mflags}

%install
%{make_install} INSTALL_ROOT=%{buildroot}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}/.??* %{buildroot}/etc/pear.conf

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}
%defattr(644,root,root,755)
%{_includedir}
%{_libdir}
%{_sysconfdir}

%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Mon Jun 16 2014 kikairoya <kikairoya@gmail.com>
- dependencies

* Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
- glob forgotten file

* Sat Jun 14 2014 kikairoya <kikairoya@gmail.com>
- Initial build
