%define llvmver 3.5
%define boostver 1.57.0
Summary: rill for wandbox
Name: wandbox-rill-head
Version: %(eval date +%Y%m%d)
Release: 1
License: Boost
Group: wandbox
BuildRequires: zlib1g-dev wandbox-cmake
Requires: wandbox-clang-%{llvmver} wandbox-boost-%{boostver}-clang-%{llvmver}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/rill-head
%define llvmprefix /opt/wandbox/llvm-%{llvmver}
%define boostprefix /opt/wandbox/boost-%{boostver}-clang-%{llvmver}

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/yutopp/rill.git --depth 1 .
find -name CMakeLists.txt -print0 | xargs -0 sed -i "s#Boost_USE_STATIC_LIBS[ 	]*ON#Boost_USE_STATIC_LIBS OFF#g"

%build
PATH="%{llvmprefix}/bin:$PATH" \
CC="%{llvmprefix}/bin/clang" \
CXX="%{llvmprefix}/bin/clang++" \
CXXFLAGS="-stdlib=libc++" \
 /opt/wandbox/cmake/bin/cmake \
  -DBOOST_ROOT=%{boostprefix} \
  -DLLVM_CONFIG_PATH=%{llvmprefix}/bin/llvm-config \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_EXE_LINKER_FLAGS="-static-libgcc -static-libstdc++" \
  .
PATH="%{llvmprefix}/bin:$PATH" \
CC="%{llvmprefix}/bin/clang" \
CXX="%{llvmprefix}/bin/clang++" \
CXXFLAGS="-stdlib=libc++" \
 %{__make} %{_smp_mflags}

%install
PATH="%{llvmprefix}/bin:$PATH" \
CC="%{llvmprefix}/bin/clang" \
CXX="%{llvmprefix}/bin/clang++" \
CXXFLAGS="-stdlib=libc++" \
 %{make_install}

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_bindir}
%{_prefix}/lib
%defattr(644,root,root,755)
%{_prefix}/include

%changelog
 * Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

