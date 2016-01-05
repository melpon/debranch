Summary: erlang for wandbox
Name: wandbox-erlang-maint
Version: %(eval date +%Y%m%d)
Release: 4
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libssl-dev libncurses5-dev autotools-dev unixodbc-dev ed libglu1-mesa-dev libsctp-dev
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/erlang-maint

%description
a component of wandbox service

%prep
%setup -q -c -T %{name}-head-%{release}
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/erlang/otp.git` . --depth 1 -b maint

%build
./otp_build autoconf
%{configure} --with-javac=no
%{__make} %{_smp_mflags}

%install
%{make_install}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}
%{_prefix}/lib64

%changelog
* Sat Dec 12 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache

* Sat May 23 2015 kikairoya <kikairoya@gmail.com>
- disable java

* Sat Jun 14 2014 kikairoya <kikairoya@gmail.com>
- do shallow clone

* Tue Jan 28 2014 kikairoya <kikairoya@gmail.com>
- Initial build
