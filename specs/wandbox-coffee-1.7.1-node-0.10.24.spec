%define nodever 0.10.24
Summary: coffee for wandbox
Name: wandbox-coffee-1.7.1-node-%{nodever}
Version: 1.7.1
Release: 2
License: MIT
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-nodejs-%{nodever}
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/coffee-%{version}-node-%{nodever}
%define nodedir /opt/wandbox/node-%{nodever}

%description
a component of wandbox service

%prep
%setup -q -c -T
git init .
git remote add origin https://github.com/jashkenas/coffee-script.git
git fetch origin refs/tags/%{version} --depth 1
git checkout FETCH_HEAD

%build

%install
mkdir -p "%{buildroot}%{_prefix}/lib/node_modules"
cd "%{buildroot}%{_prefix}/lib/node_modules"
%{nodedir}/bin/npm install -g --prefix "%{buildroot}%{_prefix}" coffee-script@%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_prefix}/bin
%{_prefix}/lib/node_modules

%changelog
*Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
- Initial build
