Summary: frontend of wandbox
Name: wandbox-cppdb
Version: 0.3.1
Release: 2
License: LGPLv3
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: libpcre3 libpcrecpp0 libsqlite3-0 libsqlite3-dev
BuildRequires: libpcre3-dev wandbox-cmake
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/cppdb

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/melpon/cppdb source

%build
mkdir -p build
cd build
/opt/wandbox/cmake/bin/cmake ../source/ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -DDISABLE_MYSQL=ON -DDISABLE_PQ=ON -DDISABLE_ODBC=ON
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include
%{_prefix}/lib


%changelog
* Wed Apr 29 2015 kikairoya <kikairoya@gmail.com>
- require libsqlite3

* Sun Sep 28 2014 kikairoya <kikairoya@gmail.com>
- Initial build
