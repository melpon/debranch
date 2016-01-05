%define rubyver 2.0.0p647
Summary: mruby for wandbox
Name: wandbox-mruby-head
Version: %(eval date +%Y%m%d)
Release: 3
License: MIT
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl libreadline6 libreadline6-dev libssl-dev libyaml-dev libsqlite3-0 libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev ssl-cert subversion rsync wandbox-ruby-%{rubyver}
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/mruby-head

%description
a component of wandbox service

%prep
%setup -q -c -T -n mruby-%{version}
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/mruby/mruby.git` .

%build
%{_prefix}/../ruby-%{rubyver}/bin/ruby ./minirake

%install
install -d -m755 %{buildroot}%{_prefix}/
rsync -a build/host/bin build/host/lib %{buildroot}%{_prefix}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
* Sun Dec 27 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache

* Sun Oct 18 2015 kikairoya <kikairoya@gmail.com>
- specify bootstrapping ruby version

* Sun Feb 16 2014 kikairoya <kikairoya@gmail.com>
- Initial build

