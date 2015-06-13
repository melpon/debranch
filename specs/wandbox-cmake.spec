Summary: cmake for wandbox
Name: wandbox-cmake
Version: 2.8.12.2
Release: 1
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: https://github.com/Kitware/CMake/archive/v%{version}.tar.gz
URL: https://github.com/Kitware/CMake

%description
a component of wandbox service

%define _prefix /opt/wandbox/cmake

%prep
%setup -q -n CMake-%{version}

%build
./configure --prefix=%{_prefix}
%{__make} %{_smp_mflags}

%install
%{make_install}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
 * Sun Feb 16 2014 kikairoya <kikairoya@gmail.com>
 - initial packaging

