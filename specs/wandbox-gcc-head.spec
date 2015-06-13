Summary: gcc for wandbox
Name: wandbox-gcc-head
Version: %(eval date +%Y%m%d)
Release: 1
Epoch: 2
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev git openssh-client bison flex m4
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/gcc-head
%define _configure ../gcc/configure
%define _libexecdir %{_prefix}/libexec

%description
a component of wandbox service

%prep
%setup -q -c -T %{name}-head-%{release}
rm -rf gcc
git clone https://github.com/mirrors/gcc.git gcc --depth 1

%build
mkdir -p build
cd build
%{configure} --enable-languages=c,c++ --enable-lto --disable-multilib --without-ppl --without-cloog-ppl --enable-checking=release --disable-nls
%{__make} %{_smp_mflags}

%install
cd build
%{make_install}
rm -rf %{buildroot}%{_prefix}/share
rm -rf %{buildroot}%{_prefix}/docs
rm -rf %{buildroot}/usr/share

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/bin
%{_prefix}/include
%{_prefix}/lib64
%{_prefix}/libexec

%changelog
 * Mon May 26 2014 kikairoya <kikairoya@gmail.com>
 - separate gdc

 * Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
 - add gdc
 - use git+ssh instead of svn

 * Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
