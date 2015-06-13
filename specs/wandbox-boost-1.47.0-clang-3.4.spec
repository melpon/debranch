Summary: boost for wandbox
Name: wandbox-boost-1.47.0-clang-3.4
Version: 1.47.0
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: wandbox-clang-3.4 libbz2-dev python-dev
Source0: http://downloads.sourceforge.net/project/boost/boost/1.47.0/boost_1_47_0.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/boost-1.47.0-clang-3.4
%define _clangdir /opt/wandbox/llvm-3.4
%define _clanggccdir /opt/wandbox/gcc-4.8.3
%define _libcxxdir /opt/wandbox/libcxx-@@libcxxver@@

%description
a component of wandbox service

%prep
%setup -q -n boost_1_47_0

%build
find . -maxdepth 1 -name 'boost-1.47.0-clang-3.4*.patch' -print0 | xargs -0 cat | patch -p1
LD_LIBRARY_PATH=%{_clangdir}/lib:%{_clangdir}/lib64:%{_clanggccdir}/lib:%{_clanggccdir}/lib64 PATH=%{_clangdir}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games ./bootstrap.sh --prefix=%{_prefix}
sed "s#using[ 	]*gcc.*;#using clang : : %{_clangdir}/bin/clang++ : <cxxflags>-I%{_clangdir}/include/c++/v1 <cxxflags>-stdlib=libc++ <linkflags>-L%{_clangdir}/lib <linkflags>-stdlib=libc++ <linkflags>-Wl,-rpath,%{_clangdir}/lib ;#" -i project-config.jam
LD_LIBRARY_PATH=%{_clangdir}/lib:%{_clangdir}/lib64:%{_clanggccdir}/lib:%{_clanggccdir}/lib64 ./b2 toolset=clang stage release link=shared runtime-link=shared --without-mpi --without-signals %{_smp_mflags}

%install
LD_LIBRARY_PATH=%{_clangdir}/lib:%{_clangdir}/lib64:%{_clanggccdir}/lib:%{_clanggccdir}/lib64 ./b2 toolset=clang install release link=shared runtime-link=shared --without-mpi --without-signals --prefix=%{buildroot}%{_prefix}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include
%{_prefix}/lib

%changelog
 * Mon Feb 17 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

