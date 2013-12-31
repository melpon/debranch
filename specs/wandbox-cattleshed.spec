Summary: backend of wandbox
Name: wandbox-cattleshed
Version: 0.1
Release: 1
License: Boost
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-head-%{release}-buildroot
Requires: libcap2-bin
BuildRequires: libboost1.48-all-dev autoconf automake m4 git
Source0: wandbox-compilers.list
URL: http://melpon.org/wandbox

%define _prefix /usr/local/wandbox/cattleshed
%define _sysconfdir %{_prefix}/etc
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

%install
cd cattleshed
%{make_install}
rm %{buildroot}%{_sysconfdir}/cattleshed.conf.d/compilers.default
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/cattleshed.conf.d

%clean
rm -rf %{buildroot}

%post
setcap cap_sys_admin,cap_sys_chroot,cap_mknod=p  %{_bindir}/cattlegrid

%files
%defattr(-,root,root,-)
%{_bindir}
%{_datadir}/cattleshed/upstart
%dir %{_sysconfdir}/cattleshed.conf.d
%config %{_sysconfdir}/cattleshed.conf
%config %{_sysconfdir}/cattleshed.conf.d/wandbox-compilers.list

%changelog
 * Mon Dec 30 2013 kikairoya <kikairoya@gmail.com>
 - Initial build
