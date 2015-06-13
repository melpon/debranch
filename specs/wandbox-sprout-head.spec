Summary: sprout library for wandbox
Name: wandbox-sprout-head
Version: %(eval date +%Y%m%d)
Release: 2
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: git
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/sprout

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/bolero-MURAKAMI/Sprout.git --depth 1 .

%build

%install
install -d -m 755 %{buildroot}%{_prefix}
rsync -a sprout %{buildroot}%{_prefix}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/sprout

%changelog
 * Sun Jun 22 2014 kikairoya <kikairoya@gmail.com>
 - do shallow clone

 * Mon Jan 27 2014 kikairoya <kikairoya@gmail.com>
 - Initial build
