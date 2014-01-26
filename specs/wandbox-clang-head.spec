Summary: clang for wandbox
Name: wandbox-clang-head
Version: %(eval date +%Y%m%d)
Release: 1
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: subversion
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/llvm-head
%define _configure ../source/configure

%description
a component of wandbox service

%prep
%setup -q -c -T
svn co 'http://llvm.org/svn/llvm-project/llvm/trunk' source
svn co 'http://llvm.org/svn/llvm-project/cfe/trunk' source/tools/clang
svn co 'http://llvm.org/svn/llvm-project/clang-tools-extra/trunk' source/tools/clang/tools/extra
svn co 'http://llvm.org/svn/llvm-project/compiler-rt/trunk' source/projects/compiler-rt
svn revert -R source

%build
mkdir -p build
cd build
%{configure} --enable-optimized --enable-assertions=no --enable-targets=host-only
%{__make} %{_smp_mflags}

%install
cd build
%{makeinstall}
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
 * Sat Dec 28 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
