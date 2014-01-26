Summary: backend of wandbox
Name: wandbox-cattleshed
Version: 0.1
Release: 2
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
Requires: libcap2-bin
BuildRequires: libboost1.48-all-dev autoconf automake m4 git
Source0: wandbox-compilers.list
Source1: cattleshed.upstart.in
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/cattleshed
%define _datadir %{_prefix}/share

%description
a component of wandbox service

%prep
%setup -q -c -T
git clone https://github.com/melpon/wandbox .

%build
cd cattleshed
autoreconf -i
%{configure} --disable-install-setcap
%{__make} %{_smp_mflags}
sed 's#@@bindir@@#%{_bindir}#g' %{SOURCE1} > cattleshed.upstart

%install
cd cattleshed
%{make_install}
rm %{buildroot}%{_sysconfdir}/cattleshed.conf.d/compilers.default
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/cattleshed.conf.d
install -d -m 755 %{buildroot}%{_initrddir}
install -m 644 cattleshed.upstart %{buildroot}%{_initrddir}/cattleshed.conf

%clean
rm -rf %{buildroot}

%post
setcap cap_sys_admin,cap_sys_chroot,cap_mknod=p  %{_bindir}/cattlegrid
if [ "$1" == 1 ]; then
  groupadd -r cattleshed || true
  useradd -r -N -g cattleshed -s /bin/nologin cattleshed || true
fi

%postun
if [ "$1" == 0 ]; then
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
%config %{_initrddir}/cattleshed.conf

%changelog
 * Sun Jun 1 2014 kikairoya <kikairoya@gmail.com>
 - add upstart script
 - create user at install

 * Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
