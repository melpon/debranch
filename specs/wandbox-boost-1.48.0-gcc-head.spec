Summary: boost for wandbox
Name: wandbox-boost-1.48.0-gcc-head
Version: 1.48.0
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: wandbox-gcc-head libbz2-dev python-dev
Source0: http://downloads.sourceforge.net/project/boost/boost/1.48.0/boost_1_48_0.tar.gz
Source1: boost-1.48.0-gcc-head-fix-stdlibcpp3-config.patch
Source2: boost-1.47.0-gcc-head-fix-stdlibcpp3-config.patch
Source3: boost-1.48.0-gcc-4.8.2-fix-stdlibcpp3-config.patch
Source4: boost-1.47.0-gcc-4.8.2-fix-stdlibcpp3-config.patch
Source5: boost-1.48.0-gcc-4.8.1-fix-stdlibcpp3-config.patch
Source6: boost-1.47.0-gcc-4.8.1-fix-stdlibcpp3-config.patch
Source7: boost-1.48.0-gcc-4.7.3-fix-stdlibcpp3-config.patch
Source8: boost-1.47.0-gcc-4.7.3-fix-stdlibcpp3-config.patch
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/boost-1.48.0-gcc-head
%define _gccdir /opt/wandbox/gcc-head

%description
a component of wandbox service

%prep
%setup -q -n boost_1_48_0
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} .
find . -maxdepth 1 -name 'boost-1.48.0-gcc-head*.patch' -print0 | xargs -0 cat | patch -p1

%build
LD_LIBRARY_PATH=%{_gccdir}/lib:%{_gccdir}/lib64 PATH=%{_gccdir}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games ./bootstrap.sh --prefix=%{_prefix}
sed "s#using[ 	]*gcc.*;#using gcc : : %{_gccdir}/bin/g++ ;#" -i project-config.jam
LD_LIBRARY_PATH=%{_gccdir}/lib:%{_gccdir}/lib64 ./b2 stage release link=shared runtime-link=shared --without-mpi %{_smp_mflags}

%install
LD_LIBRARY_PATH=%{_gccdir}/lib:%{_gccdir}/lib64 ./b2 install release link=shared runtime-link=shared --without-mpi --prefix=%{buildroot}%{_prefix}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include
%{_prefix}/lib

%changelog
 * Sun Jan 26 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

