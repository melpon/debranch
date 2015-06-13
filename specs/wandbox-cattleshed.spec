%define _gccver 4.8.4
%define _boostver 1.57.0
Summary: backend of wandbox
Name: wandbox-cattleshed
Version: 0.1
Release: 7
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
BuildRequires: wandbox-gcc-%{_gccver} wandbox-boost-%{_boostver}-gcc-%{_gccver} autoconf automake m4 git libcap-dev libcap2-bin
Source0: wandbox-compilers.list
Source1: cattleshed.upstart.in
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/cattleshed
%define _datadir %{_prefix}/share
%define _sysconfdir %{_prefix}/etc
%define _gccprefix /opt/wandbox/gcc-%{_gccver}
%define _boostprefix /opt/wandbox/boost-%{_boostver}-gcc-%{_gccver}
%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/melpon/wandbox .

%build
cd cattleshed
autoreconf -i
export CXX="%{_gccprefix}/bin/g++ -static-libstdc++"
%{configure} --disable-install-setcap --with-boost=%{_boostprefix}
%{__make} %{_smp_mflags}
sed 's#@@bindir@@#%{_bindir}#g' %{SOURCE1} > cattleshed.upstart

%install
cd cattleshed
%{make_install}
rm %{buildroot}%{_sysconfdir}/cattleshed.conf.d/compilers.default
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/cattleshed.conf.d
install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}/var
install -d -m 755 %{buildroot}/var/log
install -d -m 755 %{buildroot}/var/log/wandbox

%clean
rm -rf %{buildroot}

%pre
groupadd -r cattleshed || true
useradd -r -N -g cattleshed -s /sbin/nologin cattleshed || true

%post
setcap cap_sys_admin,cap_sys_chroot,cap_mknod,cap_net_admin=p  %{_bindir}/cattlegrid

%postun
if [ "$1" == 0 ] || [ "$1" == "purge" ]; then
  userdel cattleshed || true
  groupdel cattleshed || true
fi

%files
%defattr(-,root,root,-)
%{_bindir}
%{_datadir}/cattleshed/upstart
%dir %{_sysconfdir}/cattleshed.conf.d
%config %{_sysconfdir}/cattleshed.conf
%config %{_sysconfdir}/cattleshed.conf.d/wandbox-compilers.list
%dir /var/log
%defattr(600,cattleshed,cattleshed,700)
%dir /var/log/wandbox

%changelog
* Tue May 26 2015 kikairoya <kikairoya@gmail.com>
- prepare logdir

* Sat May 16 2015 kikairoya <kikairoya@gmail.com>
- useradd at \%pre

* Sat Jan 17 2015 kikairoya <kikairoya@gmail.com>
- sysconfdir

* Fri May 30 2014 kikairoya <kikairoya@gmail.com>
- use wandbox's boost

* Mon Jan 27 2014 kikairoya <kikairoya@gmail.com>
- moidfy install hook script to work with debian

* Sun Jan 26 2014 kikairoya <kikairoya@gmail.com>
- add upstart script
- create user at install

* Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
- Initial build
