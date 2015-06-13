Summary: boost for wandbox
Name: wandbox-boost-1.49.0-gcc-4.9.2
Version: 1.49.0
Release: 4
License: Boost
Group: wandbox
Requires: wandbox-boost-headers-%{version}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: wandbox-gcc-4.9.2 libbz2-dev
Source0: http://downloads.sourceforge.net/project/boost/boost/1.49.0/boost_1_49_0.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/boost-1.49.0-gcc-4.9.2
%define _gccdir /opt/wandbox/gcc-4.9.2

%description
a component of wandbox service

%prep
%setup -q -n boost_1_49_0

%build
PATH=%{_gccdir}/bin:$PATH ./bootstrap.sh --prefix=%{_prefix}
sed "s#using[ 	]*gcc.*;#using gcc : : %{_gccdir}/bin/g++ : <linkflags>-Wl,-rpath,%{_gccdir}/lib,-rpath,%{_gccdir}/lib64  <cxxflags>-Wno-unused-local-typedefs <cxxflags>-std=gnu++11 ;#" -i project-config.jam
./b2 stage release link=shared runtime-link=shared --without-mpi --without-python --without-test %{_smp_mflags}

%install
./b2 install release link=shared runtime-link=shared --without-mpi --without-python --without-test --prefix=%{buildroot}%{_prefix}
rm -rf %{buildroot}%{_prefix}/include/*
ln -s %{_prefix}/../boost-headers-1.49.0/boost %{buildroot}%{_prefix}/include/boost
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include/boost
%{_prefix}/lib

%changelog
* Sat May 16 2015 kikairoya <kikairoya@gmail.com>
- disable python, test

* Sat Sep 13 2014 kikairoya <kikairoya@gmail.com>
- warkaround for gcc 5.x

* Fri May 30 2014 kikairoya <kikairoya@gmail.com>
- Separate headers

* Sun Jan 26 2014 kikairoya <kikairoya@gmail.com>
- Initial build

