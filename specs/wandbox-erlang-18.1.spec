Summary: erlang for wandbox
Name: wandbox-erlang-18.1
Version: 18.1
Release: 3
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libssl-dev libncurses5-dev autotools-dev unixodbc-dev ed libglu1-mesa-dev libsctp-dev
Source0: http://www.erlang.org/download/otp_src_%{version}.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/erlang-%{version}

%description
a component of wandbox service

%prep
%setup -q -n otp_src_%{version}

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
* Sun Oct 18 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Sat May 23 2015 kikairoya <kikairoya@gmail.com>
- disable java

* Sat Jun 21 2014 kikairoya <kikairoya@gmail.com>
- Initial build
