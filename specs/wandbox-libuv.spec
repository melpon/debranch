%define gccver 4.8.2
Summary: libuv for wandbox
Name: wandbox-libuv
Version: 0.11.25
Release: 1
License: custom
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-gcc-%{gccver}
Source0: https://github.com/joyent/libuv/archive/v%{version}.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/libuv
%define gccdir /opt/wandbox/gcc-%{gccver}

%description
a component of wandbox service

%prep
%setup -q -n libuv-%{version}

%build
./autogen.sh
export CC="%{gccdir}/bin/gcc -fPIC"
export CXX="%{gccdir}/bin/g++ -fPIC"
%{configure}
%{__make} %{_smp_mflags}

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_libdir}
%defattr(644,root,root,755)
%{_includedir}

%changelog
 * Sat Jun 21 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

