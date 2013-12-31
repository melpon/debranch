Summary: clang for wandbox
Name: wandbox-clang-3.3
Version: 3.3
Release: 1
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://llvm.org/releases/%{version}/llvm-%{version}.src.tar.gz
Source1: http://llvm.org/releases/%{version}/cfe-%{version}.src.tar.gz
Source2: http://llvm.org/releases/%{version}/compiler-rt-%{version}.src.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /usr/local/wandbox/llvm-%{version}
%define _configure ../llvm-%{version}.src/configure

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0 -a 1 -a 2
mv cfe-%{version}.src llvm-%{version}.src/tools/clang
mv compiler-rt-%{version}.src llvm-%{version}.src/projects/compiler-rt

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
 * Sun Dec 29 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
