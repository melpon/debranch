Summary: pypy for wandbox
Name: wandbox-pypy-2.1
Version: 2.1
Release: 2
License: MIT
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libbz2-dev libexpat1-dev libffi-dev libncurses-dev libssl-dev python python-dev valgrind zlib1g-dev rsync
Source0: https://bitbucket.org/pypy/pypy/downloads/pypy-%{version}-src.tar.bz2
URL: http://melpon.org/wandbox

%define _prefix /opt/wandbox/pypy-%{version}
%define _datadir %{_prefix}/share

%description
a component of wandbox service

%prep
%setup -q -n pypy-%{version}-src

%build
python rpython/bin/rpython -Ojit pypy/goal/targetpypystandalone.py

%install
echo %{make_install}
install -d -m755 %{buildroot}%{_prefix}/bin
install -m755 ./pypy-c %{buildroot}%{_prefix}/bin/pypy
rsync -a include %{buildroot}%{_prefix}
rsync -a lib_pypy %{buildroot}%{_prefix}
rsync -a lib-python %{buildroot}%{_prefix}
rsync -a site-packages %{buildroot}%{_prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}

%changelog
* Sat Jun 6 2015 kikairoya <kikairoya@gmail.com>
- use generator

* Sun Feb 16 2014 kikairoya <kikairoya@gmail.com>
- Initial build
