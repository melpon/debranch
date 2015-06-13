Summary: clang for wandbox
Name: wandbox-clang-3.0
Version: 3.0
Release: 2
License: Modified BSD
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0: http://llvm.org/releases/%{version}/llvm-%{version}.tar.gz
Source1: http://llvm.org/releases/%{version}/clang-%{version}.tar.gz
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/llvm-%{version}
%define _configure ../llvm-%{version}.src/configure

%description
a component of wandbox service

%prep
%setup -q -c -T -a 0 -a 1 -a 2
mv clang-%{version}.src llvm-%{version}.src/tools/clang

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
 * Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
 - generate from script

 * Sun Dec 29 2013 kikairoya <kikairoya@gmail.com>
 - Initial build

