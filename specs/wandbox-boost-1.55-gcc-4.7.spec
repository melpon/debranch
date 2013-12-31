Summary: boost for wandbox
Name: wandbox-boost-1.55-gcc-4.7
Version: 1.55.0
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: wandbox-gcc-4.7
Source0: http://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /usr/local/wandbox/gcc-4.7.3

%description
a component of wandbox service

%prep
%setup -q -n boost_1_55_0

%build
LD_LIBRARY_PATH=%{_prefix}/lib:%{_prefix}/lib64 ./bootstrap.sh --prefix=%{_prefix}
sed "s#using[ 	]*gcc.*;#using gcc : : %{_prefix}/bin/g++ ;#" -i project-config.jam
LD_LIBRARY_PATH=%{_prefix}/lib:%{_prefix}/lib64 ./b2 stage release runtime-link=shared link=shared --without-mpi %{_smp_mflags}

%install
LD_LIBRARY_PATH=%{_prefix}/lib:%{_prefix}/lib64 ./b2 install release runtime-link=shared link=shared --without-mpi --prefix=%{buildroot}%{_prefix}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include
%{_prefix}/lib

%changelog
 * Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
