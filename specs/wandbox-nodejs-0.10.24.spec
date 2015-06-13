Summary: nodejs for wandbox
Name: wandbox-nodejs-0.10.24
Version: 0.10.24
Release: 2
License: MIT
Group: wandbox
Requires: openssl
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://nodejs.org/dist/v0.10.24r/node-v0.10.24.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/node-%{version}

%description
a component of wandbox service

%prep
%setup -q -n node-v%{version}
find -type f -exec sed \
  -e 's_^#!/usr/bin/env python$_&2_' \
  -e 's_^\(#!/usr/bin/python2\).[45]\genspec\1_' \
  -e 's_^#!/usr/bin/python$_&2_' \
  -e "s_'python'_'python2'_" -i {} \;
find test/ -type f -exec sed 's_python _python2 _' -i {} \;

%build
export PYTHON=python2
%{_configure} --prefix=%{_prefix} --shared-openssl
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}
%{_prefix}/lib
%defattr(644,root,root,755)
%{_includedir}

%changelog
*Sat  Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
- Initial build
