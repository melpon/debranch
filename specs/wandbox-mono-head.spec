Summary: mono for wandbox
Name: wandbox-mono-head
Version: %(eval date +%Y%m%d)
Release: 3
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: libgdiplus
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/mono-head
%define _sysconfdir %{_prefix}/etc
%define gccver 4.8.2
%define _configure ./autogen.sh
%define bootstrapmonodir /opt/wandbox/mono-3.12.0/bin

%description
a component of wandbox service

%prep
%setup -q -T -c
git clone https://github.com/mono/mono.git . --depth 1

%build
export CC="/opt/wandbox/gcc-%{gccver}/bin/gcc -static-libgcc -static-libstdc++"
export CXX="/opt/wandbox/gcc-%{gccver}/bin/g++ -static-libgcc -static-libstdc++"
%{configure} --disable-nls --disable-quiet-build --disable-system-aot --target=x86_64-linux-gnu
export PATH="%{bootstrapmonodir}:$PATH"
%{__make} -C eglib %{_smp_mflags}
%{__make} -C libgc %{_smp_mflags}
%{__make} -C mono %{_smp_mflags}
%{__make} %{_smp_mflags}

%install
export PATH="%{bootstrapmonodir}:$PATH"
%{make_install}
rm %{buildroot}%{_prefix}/bin/mono
ln -s mono-sgen %{buildroot}%{_prefix}/bin/mono
rm -rf %{buildroot}/usr/share

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
 * Sun Jun 08 2015 kikairoya <kikairoya@gmail.com>
 - use mono-3.12.0 as bootstrap compiler

 * Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
 - do parallel build

 * Sat Jun 14 2014 kikairoya <kikairoya@gmail.com>
 - Initial build

