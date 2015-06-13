%define _gccver 4.8.2
Summary: libcxx for wandbox
Name: wandbox-libcxx-head
Version: %(eval date +%Y%m%d)
Release: 1
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/libcxx-head-%{release}-buildroot
Requires: wandbox-llvm-head
BuildRequires: cmake subversion
URL: http://melpon.org/wandbox

%define llvmdir /opt/wandbox/llvm-head
%define _prefix /opt/wandbox/libcxx-head
%define _gccprefix /opt/wandbox/gcc-%{_gccver}
%define _configure ../source/configure

%description
a component of wandbox service

%prep
%setup -q -c -T -n %{name}-head-%{release}
svn co 'http://llvm.org/svn/llvm-project/libcxx/trunk' source
svn revert -R source

%build
mkdir -p build
cd build
CC=%{llvmdir}/bin/clang \
CXX=%{llvmdir}/bin/clang++ \
cmake -G "Unix Makefiles" \
  -DLIBCXX_CXX_ABI=libsupc++ \
  -DLIBCXX_LIBSUPCXX_INCLUDE_PATHS="%{_gccprefix}/include/c++/%{_gccver};%{_gccprefix}/include/c++/%{_gccver}/x86_64-pc-linux-gnu" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  ../source
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
