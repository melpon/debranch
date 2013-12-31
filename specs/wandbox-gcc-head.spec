Summary: gcc for wandbox
Name: wandbox-gcc-head
Version: %(eval date +%Y%m%d)
Release: 1
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev subversion bison flex m4
URL: http://melpon.org/wandbox

%define _prefix /usr/local/wandbox/gcc-head
%define _configure ../gcc/configure

%description
a component of wandbox service

%prep
%setup -q -c -T
rm -rf gcc
svn co svn://gcc.gnu.org/svn/gcc/trunk gcc

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
%{_prefix}/lib
%{_prefix}/lib64

%changelog
 * Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
