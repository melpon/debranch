Summary: lua for wandbox
Name: wandbox-lua-5.2.3
Version: 5.2.3
Release: 2
License: MIT
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://www.lua.org/ftp/lua-%{version}.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/lua-%{version}

%description
a component of wandbox service

%prep
%setup -q -n lua-%{version}

%build
%{__make} linux %{_smp_mflags}

%install
%{__make} INSTALL_TOP=%{buildroot}%{_prefix} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
*Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Sun Feb 16 2014 kikairoya <kikairoya@gmail.com>
- Initial build
