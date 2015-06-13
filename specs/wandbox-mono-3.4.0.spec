Summary: mono for wandbox
Name: wandbox-mono-3.4.0
Version: 3.4.0
Release: 3
License: GPL
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: libgdiplus
Source0: http://download.mono-project.com/sources/mono/mono-%{version}.tar.bz2
URL: http://melpon.org/wandbox
Source1: Microsoft.Portable.Common.targets

%define _prefix /opt/wandbox/mono-%{version}
%define _sysconfdir %{_prefix}/etc
%define gccver 4.8.4

%description
a component of wandbox service

%prep
%setup -q -n mono-%{version}
cp %{SOURCE1} mcs/tools/xbuild/targets/

%build
export CC="/opt/wandbox/gcc-%{gccver}/bin/gcc -static-libgcc -static-libstdc++"
export CXX="/opt/wandbox/gcc-%{gccver}/bin/g++ -static-libgcc -static-libstdc++"
%{configure} --disable-nls --disable-quiet-build --disable-system-aot
%{__make} -C eglib %{_smp_mflags}
%{__make} -C libgc %{_smp_mflags}
%{__make} -C mono %{_smp_mflags}
%{__make} %{_smp_mflags} || %{__make}

%install
%{make_install}
rm %{buildroot}%{_prefix}/bin/mono
ln -s mono-sgen %{buildroot}%{_prefix}/bin/mono
cat > %{buildroot}%{_prefix}/bin/mono-aot <<EOS
#!/bin/sh
%{_prefix}/bin/mono --aot=full -O=all ""
%{_prefix}/bin/mono --full-aot ""
EOS
rm -rf %{buildroot}/usr/share

%clean
rm -rf %{buildroot}

%post
find %{_prefix}/lib -name '*.dll.so' -delete || true
find %{_prefix}/lib -path '*gac' -prune -o -name '*.dll' -exec %{_prefix}/bin/mono --aot=full -O=all "{}" ";" || true

%preun
find %{_prefix}/lib -name '*.dll.so' -delete || true

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
* Sun May 24 2015 kikairoya <kikairoya@gmail.com>
- use generator
- add aot-ed libs
- add aot wrapper

* Sun Jun 15 2014 kikairoya <kikairoya@gmail.com>
- do parallel build

* Sat Jun 14 2014 kikairoya <kikairoya@gmail.com>
- Initial build
