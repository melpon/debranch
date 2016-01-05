Summary: python for wandbox
Name: wandbox-python-3.4.3
Version: 3.4.3
Release: 3
License: Python
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: python
BuildRequires: libreadline-dev libncurses5-dev tk8.5-dev blt-dev libssl-dev zlib1g-dev libbz2-dev libexpat1-dev libbluetooth-dev libsqlite3-dev libffi-dev netbase libdb5.1-dev libgdbm-dev gdb python
Source0: http://www.python.org/ftp/python/3.4.3/Python-3.4.3.tar.xz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/python-%{version}
%define _libdir %{_prefix}/lib

%description
a component of wandbox service

%prep
%setup -q -n Python-%{version}

%build
%{configure}
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
chmod -R +w %{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}
%{_libdir}
%defattr(644,root,root,755)
%{_includedir}

%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Wed May 27 2015 kikairoya <kikairoya@gmail.com>
- merge \%{_libdir} to \%{_prefix}/lib

* Mon Jan 27 2014 kikairoya <kikairoya@gmail.com>
- Initial build
