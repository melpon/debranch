Summary: frontend of wandbox
Name: wandbox-kennel
Version: 0.2
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libpcre3-dev libsqlite3-dev libssl-dev
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/kennel
%define _sysconfdir %{_prefix}/etc

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/melpon/wandbox .
git submodule init
git submodule update

%build
cd kennel2
./autogen.sh
%{configure} --prefix=%{_prefix} --with-cppcms=/opt/wandbox/cppcms --with-cppdb=/opt/wandbox/cppdb
%{__make} %{_smp_mflags}

%install
cd kennel2
%{make_install}
touch %{buildroot}%{_localstatedir}/lib/kennel/kennel_production.sqlite3

%clean
rm -rf %{buildroot}

%pre
groupadd -r kennel || true
useradd -r -N -g kennel -s /sbin/nologin kennel || true

%postun
if [ "$1" == 0 ] || [ "$1" == "purge" ]; then
  userdel kennel || true
  groupdel kennel || true
fi

%files
%defattr(-,root,root,-)
%{_bindir}
%{_sysconfdir}
%defattr(600,kennel,kennel,700)
%dir %{_localstatedir}/lib/kennel
%config(noreplace) %{_localstatedir}/lib/kennel/kennel_production.sqlite3

%changelog
* Sat May 16 2015 kikairoya <kikairoya@gmail.com>
- Requires cppcms/cppdb and their depends
- useradd at \%pre

* Sun Sep 28 2014 kikairoya <kikairoya@gmail.com>
- use kennel2

* Tue Aug 19 2014 kikairoya <kikairoya@gmail.com>
- fix typo
- move files from \%_datadir to \%_localstatedir
- glob files yesod will generate
- workaround for broken package dependencies

* Sun May 25 2014 kikairoya <kikairoya@gmail.com>
- remove garbage dependency

* Mon Jan 27 2014 kikairoya <kikairoya@gmail.com>
- moidfy install hook script to work with debian

* Sun Jan 26 2014 kikairoya <kikairoya@gmail.com>
- add upstart script
- create user at install

* Tue Dec 31 2013 kikairoya <kikairoya@gmail.com>
- Initial build
