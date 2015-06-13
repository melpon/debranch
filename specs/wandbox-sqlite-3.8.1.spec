Summary: sqlite for wandbox
Name: wandbox-sqlite-3.8.1
Version: 3.8.1
Release: 1
License: custom
Group: wandbox
BuildRequires: tcl libreadline-dev
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://www.sqlite.org/2013/sqlite-autoconf-3080100.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/sqlite-%{version}

%description
a component of wandbox service

%prep
%setup -q -n sqlite-autoconf-3080100

%build
%{configure}
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}
%{_libdir}
%defattr(644,root,root,755)
%{_includedir}

%changelog
 * Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

