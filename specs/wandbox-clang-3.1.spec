%define _gccver 4.8.3
Summary: clang for wandbox
Name: wandbox-clang-3.1
Version: 3.1
Release: 5
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-gcc-%{_gccver}
BuildRequires: wandbox-cmake
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/llvm-3.1
%define _gccprefix /opt/wandbox/gcc-%{_gccver}
%define branchname branches/release_31
%define extra_branchname %{nil}
%define libcxx_branchname branches/release_30

%description
a component of wandbox service

%prep
%setup -q -c -T
svn co 'https://llvm.org/svn/llvm-project/llvm/%{branchname}' source
svn co 'https://llvm.org/svn/llvm-project/cfe/%{branchname}' source/tools/clang
svn co 'https://llvm.org/svn/llvm-project/compiler-rt/%{branchname}' source/projects/compiler-rt
[ -n "%{extra_branchname}" ] && svn co 'https://llvm.org/svn/llvm-project/clang-tools-extra/%{extra_branchname}' source/tools/clang/tools/extra
[ -n "%{libcxx_branchname}" ] && svn co 'https://llvm.org/svn/llvm-project/libcxx/%{libcxx_branchname}' libcxx

%build
mkdir -p build b_libcxx
case %{_host_cpu} in
  i?86* | amd64* | x86_64*) arch="X86" ;;
  sparc*)               arch="Sparc" ;;
  powerpc*)             arch="PowerPC" ;;
  arm*)                 arch="ARM" ;;
  aarch64*)             arch="AArch64" ;;
  mips* | mips64*)      arch="Mips" ;;
  xcore*)               arch="XCore" ;;
  msp430*)              arch="MSP430" ;;
  hexagon*)             arch="Hexagon" ;;
  nvptx*)               arch="NVPTX" ;;
  s390x*)               arch="SystemZ" ;;
  *)                    arch="Unknown" ;;
esac
export CC="%{_gccprefix}/bin/gcc"
export CXX="%{_gccprefix}/bin/g++"
export LD_LIBRARY_PATH="%{_gccprefix}/lib:%{_gccprefix}/lib64:%{_gccprefix}/lib32"
cd build
/opt/wandbox/cmake/bin/cmake -G "Unix Makefiles"   -DLLVM_TARGETS_TO_BUILD="$arch"   -DLLVM_TARGET_ARCH="$arch"   -DCMAKE_EXE_LINKER_FLAGS="-static-libgcc -static-libstdc++ -L$(dirname $($CXX -print-file-name=libstdc++.a)) -lstdc++"   -DCMAKE_BUILD_TYPE=Release   -DCMAKE_INSTALL_PREFIX=%{_prefix}   ../source
%{__make} %{_smp_mflags}
cd ../b_libcxx
export CC="$PWD/../build/bin/clang"
export CXX="$PWD/../build/bin/clang++"
export LD_LIBRARY_PATH=
/opt/wandbox/cmake/bin/cmake -G "Unix Makefiles"   -DLIBCXX_CXX_ABI=libsupc++   -DLIBCXX_LIBSUPCXX_INCLUDE_PATHS="%{_gccprefix}/include/c++/%{_gccver};%{_gccprefix}/include/c++/%{_gccver}/$(%{_gccprefix}/bin/gcc -dumpmachine)"   -DCMAKE_INSTALL_PREFIX=%{_prefix}   ../libcxx
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}
cd ../b_libcxx
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/include
%{_prefix}/lib

%changelog
 * Fri May 30 2014 kikairoya <kikairoya@gmail.com>
 - link libstdc++ statically

 * Tue May 27 2014 kikairoya <kikairoya@gmail.com>
 - use gcc 4.8.3

 * Sun Feb 16 2014 kikairoya <kikairoya@gmail.com>
 - use svn

 * Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
 - generate from script

 * Sun Dec 29 2013 kikairoya <kikairoya@gmail.com>
 - Initial build

