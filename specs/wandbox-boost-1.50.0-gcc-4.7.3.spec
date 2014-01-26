Summary: boost for wandbox
Name: wandbox-boost-1.50.0-gcc-4.7.3
Version: 1.50.0
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: wandbox-gcc-head libbz2-dev python-dev
Source0: http://downloads.sourceforge.net/project/boost/boost/1.50.0/boost_1_50_0.tar.gz
Source1: boost-1.48.0-gcc-head-fix-stdlibcpp3-config.patch
Source2: boost-1.47.0-gcc-head-fix-stdlibcpp3-config.patch
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/boost-1.50.0-gcc-4.7.3
%define _gccdir /opt/wandbox/gcc-4.7.3

%description
a component of wandbox service

%prep
%setup -q -n boost_1_50_0

%build
cp %{SOURCE1} %{SOURCE2} .
find . -maxdepth 1 -name 'boost-1.50.0-gcc-4.7.3*.patch' -print0 | xargs -0 cat | patch -p1
LD_LIBRARY_PATH=%{_gccdir}/lib:%{_gccdir}/lib64 PATH=%{_gccdir}/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games ./bootstrap.sh --prefix=%{_prefix}
sed "s#using[ 	]*gcc.*;#using gcc : : %{_gccdir}/bin/g++ ;#" -i project-config.jam
LD_LIBRARY_PATH=%{_gccdir}/lib:%{_gccdir}/lib64 ./b2 stage release link=shared runtime-link=shared --without-mpi %{_smp_mflags}

%install
LD_LIBRARY_PATH=%{_prefix}/lib:%{_prefix}/lib64 ./b2 install release link=shared runtime-link=shared --without-mpi --prefix=%{buildroot}%{_prefix}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include
%{_prefix}/lib

%changelog
 * Sun Jun 26 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

