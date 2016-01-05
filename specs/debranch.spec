Summary: debranch support service
Name: debranch
Version: 0.1
Release: 1
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: git subversion base64
URL: http://melpon.org/wandbox

SOURCE0: debranch.sh

%define _prefix /opt/wandbox/debranch

%description
a component of wandbox service

%prep
%setup -q -c -T %{name}-%{version}-%{release}
cp %{SOURCE0} .

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 debranch.sh %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}

%changelog
* Sat Dec 12 2015 kikairoya <kikairoya@gmail.com>
- Initial build
