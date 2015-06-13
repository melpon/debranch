%define gccver 4.8.4
%define gccdir /opt/wandbox/gcc-%{gccver}
%define javaver 7
%define updatever 79
%define icedteaver 2.5.5
Summary: java for wandbox
Name: wandbox-openjdk-%{javaver}.%{updatever}-icedtea-%{icedteaver}
Version: %{javaver}.%{updatever}.%{icedteaver}
Release: 1
License: Custom
Group: wandbox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: wandbox-gcc-%{gccver}
BuildRequires: rsync pkg-config zip fastjar gawk gcj-jdk gcj-jre-headless ant-gcj libkrb5-dev x11proto-core-dev libcups2-dev libattr1-dev libxt-dev libxinerama-dev libxrender-dev libxtst-dev libxft-dev libalsaplayer-dev libasound2-dev
URL: http://melpon.org/wandbox

Source0: icedtea-%{icedteaver}.tar.gz
Source1: icedtea_%{icedteaver}_openjdk.tar.bz2
Source2: icedtea_%{icedteaver}_corba.tar.bz2
Source3: icedtea_%{icedteaver}_jaxp.tar.bz2
Source4: icedtea_%{icedteaver}_jaxws.tar.bz2
Source5: icedtea_%{icedteaver}_jdk.tar.bz2
Source6: icedtea_%{icedteaver}_langtools.tar.bz2
Source7: icedtea_%{icedteaver}_hotspot.tar.bz2

%define _prefix /opt/wandbox/openjdk-%{javaver}.%{updatever}-icedtea-%{icedteaver}

%description
a component of wandbox service

%prep
%setup -q -n icedtea-%{icedteaver}
for f in "%{SOURCE1}" "%{SOURCE2}" "%{SOURCE3}" "%{SOURCE4}" "%{SOURCE5}" "%{SOURCE6}" "%{SOURCE7}"; do
  cp "$f" "$(basename "$f" | sed s/^.*_//g)"
done

%build
export CC='%{gccdir}/bin/gcc'
export CXX='%{gccdir}/bin/g++ -Wl,-rpath,%{gccdir}/lib64'
./autogen.sh
%{configure} \
  --enable-bootstrap \
  --with-parallel-jobs=${RPM_BUILD_NCPUS:-1} \
  --disable-tests \
  --disable-downloading \
  --disable-Werror \
  --without-rhino \
  --disable-infinality \
  --disable-system-zlib \
  --disable-system-jpeg \
  --disable-system-png \
  --disable-system-gif \
  --disable-system-gtk \
  --disable-system-gio \
  --disable-system-fontconfig \
  --disable-system-pcsc \
  --disable-system-lcms

%{__make}

%install
cd openjdk.build/j2sdk-image
install -d -m755 "%{buildroot}/%{_prefix}"
rsync -a bin lib include jre "%{buildroot}/%{_prefix}"
mv -f "%{buildroot}/%{_prefix}/jre/lib/fontconfig.Ubuntu.properties.src" "%{buildroot}/%{_prefix}/jre/lib/fontconfig.properties"
mv -f "%{buildroot}/%{_prefix}/jre/lib/fontconfig.Ubuntu.bfc" "%{buildroot}/%{_prefix}/jre/lib/fontconfig.bfc"
mv -f "%{buildroot}/%{_prefix}/jre/lib/management/jmxremote.password.template" "%{buildroot}/%{_prefix}/jre/lib/management/jmxremote.password"
mv -f "%{buildroot}/%{_prefix}/jre/lib/management/snmp.acl.template" "%{buildroot}/%{_prefix}/jre/lib/management/snmp.acl"
rm -f "%{buildroot}/%{_prefix}"/jre/lib/fontconfig.*.bfc
rm -f "%{buildroot}/%{_prefix}"/jre/lib/fontconfig.*.properties.src
rm -f "%{buildroot}/%{_prefix}"/jre/lib/fontconfig.properties.src
chmod go+r "%{buildroot}/%{_prefix}"/lib/sa-jdi.jar

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_prefix}/bin
%{_prefix}/lib
%{_prefix}/include
%{_prefix}/jre

%changelog
 * Sat May 02 2015 kikairoya <kikairoya@gmail.com>
 - Initial build

