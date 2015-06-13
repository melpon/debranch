Summary: clang for wandbox
Name: wandbox-clang-3.4
Version: 3.4
Release: 9
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-gcc-4.8.4 g++
BuildRequires: wandbox-cmake
URL: http://melpon.org/wandbox
Source0: llvm-3.4.tar.xz
Source1: clang-cfe-3.4.tar.xz
Source2: clang-rt-3.4.tar.xz
Source3: clang-tools-extra-3.4.tar.xz
Source4: libcpp-3.4.tar.xz
Source10: libcxx-3.5-fix-install-bitsdir.patch
Source11: clang-3.2-add-searchdir.patch.in
Source12: clang-3.3-add-searchdir.patch.in
Source13: clang-3.4-add-searchdir.patch.in
Source14: clang-3.4-add-searchdir.patch.in

%define _prefix /opt/wandbox/llvm-3.4
%define _ccprefix /opt/wandbox/gcc-4.8.4

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0 -a 1 -a 2 -a 3 -a 4
mv llvm-3.4 source
mv clang-cfe-3.4 source/tools/clang
mv clang-rt-3.4 source/projects/compiler-rt
mv clang-tools-extra-3.4 source/tools/clang/tools/extra
mv libcpp-3.4 libcxx
cp %{SOURCE10} .
for f in %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14}; do
  sed "s#@@prefix@@#%{_prefix}#" $f > $(basename $f .in)
done
cd source/tools/clang
find ../../.. -maxdepth 1 -name "clang-3.4*.patch" -print0 | xargs -0 cat | patch -p1
cd ../../..
cd libcxx
find .. -maxdepth 1 -name "libcxx-3.4*.patch" -print0 | xargs -0 cat | patch -p1
cd ..
sed -i s#\"/usr/include/c++/v1#\"%{_prefix}/include/c++/v1# source/tools/clang/lib/Frontend/InitHeaderSearch.cpp;sed -i s#getDriver\(\).SysRoot\ +\ \"/usr/include/c++/v1\"#\"%{_prefix}/include/c++/v1\"# source/tools/clang/lib/Driver/ToolChains.cpp

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
export CC="%{_ccprefix}/bin/gcc"
export CXX="%{_ccprefix}/bin/g++"
export LIBRARY_PATH="%{_ccprefix}/lib:%{_ccprefix}/lib64:%{_ccprefix}/lib32"
export LD_LIBRARY_PATH="%{_ccprefix}/lib:%{_ccprefix}/lib64:%{_ccprefix}/lib32"
cd build
/opt/wandbox/cmake/bin/cmake -G "Unix Makefiles" \
  -DLLVM_TARGETS_TO_BUILD="$arch" \
  -DLLVM_TARGET_ARCH="$arch" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  ../source
%{__make} %{_smp_mflags}
cd ../b_libcxx
export CC="$PWD/../build/bin/clang"
export CXX="$PWD/../build/bin/clang++"
export LIBRARY_PATH=
export LD_LIBRARY_PATH=
/opt/wandbox/cmake/bin/cmake -G "Unix Makefiles" \
  -DLIBCXX_CXX_ABI=libsupc++ "-DCMAKE_SHARED_LINKER_FLAGS="-Wl,--start-group,-dn,--whole-archive,-lsupc++,--no-whole-archive,--end-group,-dy"" \
  -DLIBCXX_LIBSUPCXX_INCLUDE_PATHS="." \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  ../libcxx
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}
cd ../b_libcxx
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs
rm -rf %{buildroot}%{_prefix}/include/c++/v1/c++

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/include
%{_prefix}/lib

%changelog
 * Sat May 16 2015 kikairoya <kikairoya@gmail.com>
 - use prefetched source archive

 * Sun Feb 8 2015 kikairoya <kikairoya@gmail.com>
 - embed libsupc++.a to libc++.so

 * Fri Jan 2 2015 kikairoya <kikairoya@gmail.com>
 - use clang for clang>3.4

 * Sun Sep 14 2014 kikairoya <kikairoya@gmail.com>
 - add workaround for http://llvm.org/bugs/show_bug.cgi?id=20936

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

