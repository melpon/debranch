Summary: clang for wandbox
Name: wandbox-clang-head
Version: %(eval date +%Y%m%d)
Release: 11
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-clang-3.5 g++
BuildRequires: wandbox-cmake
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/llvm-head
%define _ccprefix /opt/wandbox/llvm-3.5

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/llvm-mirror/llvm.git` source
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/llvm-mirror/clang.git` source/tools/clang
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/llvm-mirror/compiler-rt.git` source/projects/compiler-rt
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/llvm-mirror/clang-tools-extra.git` source/tools/clang/tools/extra
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/llvm-mirror/libcxx.git` libcxx

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
export CC="%{_ccprefix}/bin/clang"
export CXX="%{_ccprefix}/bin/clang++ -stdlib=libc++ -I/opt/wandbox/llvm-3.5/include/c++/v1"
export LIBRARY_PATH="%{_ccprefix}/lib:%{_ccprefix}/lib64:%{_ccprefix}/lib32"
export LD_LIBRARY_PATH="%{_ccprefix}/lib:%{_ccprefix}/lib64:%{_ccprefix}/lib32"
cd build
/opt/wandbox/cmake/bin/cmake -G "Unix Makefiles"   -DLLVM_TARGETS_TO_BUILD="$arch"   -DLLVM_TARGET_ARCH="$arch"   -DCMAKE_BUILD_TYPE=Release   -DCMAKE_INSTALL_PREFIX=%{_prefix}   ../source
%{__make} %{_smp_mflags}
cd ../b_libcxx
export CC="$PWD/../build/bin/clang"
export CXX="$PWD/../build/bin/clang++"
#export LIBRARY_PATH=
#export LD_LIBRARY_PATH=
/opt/wandbox/cmake/bin/cmake -G "Unix Makefiles"   -DLIBCXX_CXX_ABI=libsupc++ "-DCMAKE_SHARED_LINKER_FLAGS="-Wl,--start-group,-dn,--whole-archive,-lsupc++,--no-whole-archive,--end-group,-dy""   -DLIBCXX_CXX_ABI_INCLUDE_PATHS="/usr/include;/usr/include/c++/4.6;/usr/include/c++/4.6/x86_64-linux-gnu/.;/usr/include/x86_64-linux-gnu;/usr/include/x86_64-linux-gnu/gnu;/usr/include/x86_64-linux-gnu/sys;/usr/lib/gcc/x86_64-linux-gnu/4.6/include;."   -DCMAKE_INSTALL_PREFIX=%{_prefix}   ../libcxx
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
%{_prefix}/libexec

%changelog
* Sun Dec 27 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache
- add libexec

* Sun Oct 18 2015 kikairoya <kikairoya@gmail.com>
- use clang for clang>3.5

* Sat May 16 2015 kikairoya <kikairoya@gmail.com>
- separate from generator
 
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

