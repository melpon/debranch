Summary: mruby for wandbox
Name: wandbox-mruby-head
Version: %(eval date +%Y%m%d)
Release: 1
License: MIT
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl libreadline6 libreadline6-dev libssl-dev libyaml-dev libsqlite3-0 libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev ssl-cert subversion rsync ruby
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/mruby-head

%description
a component of wandbox service

%prep
%setup -q -c -T -n mruby-%{version}
git clone https://github.com/mruby/mruby.git --depth 1 .

%build
ruby ./minirake

%install
install -d -m755 %{buildroot}%{_prefix}/
rsync -a build/host/bin build/host/lib %{buildroot}%{_prefix}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
 * Sun Feb 16 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

