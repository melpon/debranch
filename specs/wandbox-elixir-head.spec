%define erlangver 18.1
Summary: elixir for wandbox
Name: wandbox-elixir-head
Version: %(eval date +%Y%m%d)
Release: 4
License: Apache
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-erlang-%{erlangver}
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/elixir-head
%define erlangdir /opt/wandbox/erlang-%{erlangver}

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/elixir-lang/elixir.git` . -b master

%build
PATH=%{erlangdir}/bin:$PATH %{__make} PREFIX=%{_prefix} %{_smp_mflags}

%install
mkdir -p %{buildroot}%{_prefix}
PATH=%{erlangdir}/bin:$PATH %{__make} DESTDIR= PREFIX=%{buildroot}%{_prefix} install
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_prefix}/bin
%{_prefix}/lib

%changelog
* Sun Dec 27 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache

* Sun Oct 18 2015 kikairoya <kikairoya@gmail.com>
- use erlang 18

* Sat Jun 13 2015 kikairoya <kikairoya@gmail.com>
- use PREFIX instead of DESTDIR

* Sat Jun 21 2014 kikairoya <kikairoya@gmail.com>
- Initial build

