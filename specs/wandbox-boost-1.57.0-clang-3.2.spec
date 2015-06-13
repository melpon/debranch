Summary: boost for wandbox
Name: wandbox-boost-1.57.0-clang-3.2
Version: 1.57.0
Release: 3
License: Boost
Group: wandbox
Requires: wandbox-boost-headers-%{version}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: wandbox-clang-3.2 libbz2-dev python-dev
Source0: http://downloads.sourceforge.net/project/boost/boost/1.57.0/boost_1_57_0.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/boost-1.57.0-clang-3.2
%define _clangdir /opt/wandbox/llvm-3.2
%define _clanggccdir /opt/wandbox/gcc-4.8.3
%define _libcxxdir /opt/wandbox/libcxx-

%description
a component of wandbox service

%prep
%setup -q -n boost_1_57_0

%build
find . -maxdepth 1 -name "boost-1.57.0-clang-3.2*.patch" -print0 | xargs -0 cat | patch -p1
PATH=%{_clangdir}/bin:$PATH ./bootstrap.sh --prefix=%{_prefix}
sed "s#using[ 	]*gcc.*;#using clang : : %{_clangdir}/bin/clang++ : <cxxflags>-I%{_clangdir}/include/c++/v1 <cxxflags>-stdlib=libc++ <linkflags>-L%{_clangdir}/lib <linkflags>-stdlib=libc++ <linkflags>-Wl,-rpath,%{_clangdir}/lib ;#" -i project-config.jam
./b2 toolset=clang stage release link=shared runtime-link=shared --without-mpi --without-signals --without-python --without-test %{_smp_mflags}

%install
./b2 toolset=clang install release link=shared runtime-link=shared --without-mpi --without-signals --without-python --without-test --prefix=%{buildroot}%{_prefix}
rm -rf %{buildroot}%{_prefix}/include/*
ln -s %{_prefix}/../boost-headers-1.57.0/boost %{buildroot}%{_prefix}/include/boost
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include/boost
%{_prefix}/lib

%changelog
* Sat May 16 2015 kikairoya <kikairoya@gmail.com.
- disable python, boost
- -Wno-unused-local-typedefs

* Fri May 30 2014 kikairoya <kikairoya@gmail.com>
- Separate headers

* Mon Feb 17 2014 kikairoya <kikairoya@gmail.com>
- Initial build

