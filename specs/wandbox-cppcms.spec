Summary: frontend of wandbox
Name: wandbox-cppcms
Version: 1.0.4
Release: 1
License: LGPLv3
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: libpcre3 libpcrecpp0
BuildRequires: libpcre3-dev wandbox-cmake
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/cppcms

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/melpon/cppcms source

%build
mkdir -p build
cd build
/opt/wandbox/cmake/bin/cmake ../source/ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -DDISABLE_SHARED=ON -DDISABLE_FCGI=ON -DDISABLE_SCGI=ON -DDISABLE_ICU_LOCALE=ON -DDISABLE_TCPCACHE=ON
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/include
%{_prefix}/lib


%changelog
 * Sun Sep 28 2014 kikairoya <kikairoya@gmail.com>
 - Initial build
