Summary: libcxx for wandbox
Name: wandbox-libcxx-3.3
Version: 3.3
Release: 1
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-llvm-%{version}
BuildRequires: cmake
Source0: http://llvm.org/releases/%{version}/libcxx-%{version}.src.tar.gz
URL: http://melpon.org/wandbox

%define llvmdir /usr/local/wandbox/llvm-%{version}
%define _prefix /usr/local/wandbox/libcxx-%{version}
%define _configure ../libcxx-%{version}.src/configure

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0

%build
mkdir -p build
cd build
CC=%{llvmdir}/bin/clang \
CXX=%{llvmdir}/bin/clang++ \
cmake -G "Unix Makefiles" \
  -DLIBCXX_CXX_ABI=libsupc++ \
  -DLIBCXX_LIBSUPCXX_INCLUDE_PATHS="/usr/include/c++/4.6;/usr/include/c++/4.6/x86_64-linux-gnu" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  ../libcxx-%{version}.src
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/include
%{_prefix}/lib

%changelog
 * Sun Dec 29 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
