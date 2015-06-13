Summary: boost headers for wandbox
Name: wandbox-boost-headers-1.50.0
Version: 1.50.0
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://downloads.sourceforge.net/project/boost/boost/1.50.0/boost_1_50_0.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/boost-headers-1.50.0

%description
a component of wandbox service

%prep
%setup -q -n boost_1_50_0

%build

%install
mkdir -p %{buildroot}%{_prefix}/docs
rsync -a boost %{buildroot}%{_prefix}/
install -c -m 644 LICENSE_1_0.txt %{buildroot}%{_prefix}/docs/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/boost
%{_prefix}/docs/LICENSE_1_0.txt

%changelog
 * Fri May 30 2014 kikairoya <kikairoya@gmail.com>
 - Separate headers

