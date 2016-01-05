%define gccver 4.8.2
Summary: rust for wandbox
Name: wandbox-rust-head
Version: %(eval date +%Y%m%d)
Release: 2
License: Apache
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-gcc-%{gccver}
BuildRequires: libffi-dev
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/rust-head
%define gccdir /opt/wandbox/gcc-%{gccver}

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone `/opt/wandbox/debranch/bin/debranch.sh https://github.com/mozilla/rust.git` .
/opt/wandbox/debranch/bin/debranch.sh --git-submodule https://github.com/mozilla/rust.git
git submodule update

%build
export CC="%{gccdir}/bin/gcc"
export CXX="%{gccdir}/bin/g++"
export LDFLAGS="-Wl,-rpath,%{gccdir}/lib64"
export RUSTFLAGS="-C linker=%{gccdir}/bin/g++ -C link-args=-Wl,-rpath,%{gccdir}/lib64"
%{_configure} --prefix=%{_prefix} --sysconfdir=%{_prefix}/etc --disable-docs --disable-llvm-assertions --disable-debug --enable-llvm-static-stdcpp
%{__make} RUSTFLAGS="$RUSTFLAGS" %{_smp_mflags} -k
%{__make} RUSTFLAGS="$RUSTFLAGS" %{_smp_mflags} -k
%{__make} RUSTFLAGS="$RUSTFLAGS"

%install
%{make_install}
rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_prefix}/bin
%{_prefix}/lib

%changelog
* Sun Dec 27 2015 kikairoya <kikairoya@gmail.com>
- use debranch repository cache

* Sat Jun 21 2014 kikairoya <kikairoya@gmail.com>
- Initial build

