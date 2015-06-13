Summary: spidermonkey for wandbox
Name: wandbox-spidermonkey-24.2.0
Version: 24.2.0
Release: 2
License: MPL
Group: wandbox
Requires: nspr
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: https://ftp.mozilla.org/pub/mozilla.org/js/mozjs-%{version}.tar.bz2
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/mozjs-%{version}

%description
a component of wandbox service

%prep
%setup -q -n mozjs-%{version}/js/src

%build
%{configure} --disable-debug --disable-debug-symbols --disable-tests
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share

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

* Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
- Initial build
