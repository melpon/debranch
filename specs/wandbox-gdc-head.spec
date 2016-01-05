Summary: gdc for wandbox
Name: wandbox-gdc-head
Version: %(eval date +%Y%m%d)
Release: 3
Epoch: 2
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: libgmp-dev libmpfr-dev libmpc-dev subversion bison flex m4 curl unzip
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/gdc-head
%define _configure ../gcc/configure
%define _libexecdir %{_prefix}/libexec

%description
a component of wandbox service

%prep
%setup -q -c -T %{name}-head-%{release}
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/D-Programming-GDC/GDC.git` GDC-master
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/gcc-mirror/gcc.git` gcc
cd gcc
git checkout $(TZ=UTC git log -n1 --pretty=tformat:%H --before=$(date "+%Y-%m-%d" -d "$(cut -d- -f3 < ../GDC-master/gcc.version) next day"))
cd ../GDC-master
sed -i "s/d-warn = .*/\\\\0 -Wno-suggest-attribute=format/" gcc/d/Make-lang.in
./setup-gcc.sh ../gcc
cd ..


%build
mkdir -p build
cd build
%{configure} --enable-languages=c,c++,d --enable-lto --disable-multilib --without-ppl --without-cloog-ppl --enable-checking=release --disable-nls
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
* Sat Dec 12 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache

* Wed Oct 21 2015 kikairoya <kikairoya@gmail.com>
- use github's pre-archived zip

* Mon May 26 2014 kikairoya <kikairoya@gmail.com>
- separate from gcc-head

* Mon Feb 3 2014 kikairoya <kikairoya@gmail.com>
- add gdc
- use git+ssh instead of svn

* Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
- Initial build
