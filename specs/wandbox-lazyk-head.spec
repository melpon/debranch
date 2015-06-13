Summary: lazyk for wandbox
Name: wandbox-lazyk
Version: 2013.01.26
Release: 1
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: https://raw.github.com/msullivan/LazyK/74964d493699f8c57cb7ce2e92f251aac8f67bf4/lazy.cpp
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/lazyk

%description
a component of wandbox service

%prep
%setup -q -c -T -n lazyk
cp %{SOURCE0} .

%build
g++ ${CXXFLAGS:-%optflags} lazy.cpp -o lazyk

%install
install -d -m755 %{buildroot}%{_prefix}/bin
install -m755 lazyk %{buildroot}%{_prefix}/bin

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin/lazyk

%changelog
 * Sun Feb 16 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

