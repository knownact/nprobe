Summary: network probe
Name: nprobe
Version: 5.5.5
Release: 0
License: GPL
Group: Networking/Utilities
URL: http://www.ntop.org/nProbe.html
Source: nProbe-%{version}.tgz
Packager: Fernanda Weiden <nanda@google.com>
# Temporary location where the RPM will be built
BuildRoot:  %{_tmppath}/%{name}-%{version}-root
Requires: libpcap >= 0.8.3 glibc >= 2.3.5 GeoIP >= 1.4.5

%description
nprobe is a software NetFlow v5/v9 and nFlow probe that allows to turn 
a PC into a NetFlow probe. It has been designed to be compact, easy to 
embed, an memory/CPU savvy.

%prep

%setup -q

%build
PATH=/usr/bin:/bin:/usr/sbin:/sbin

if [ -x ./configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./configure 
else
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh 
fi
make

# Installation may be a matter of running an install make target or you
# may need to manually install files with the install command.
%install
PATH=/usr/bin:/bin:/usr/sbin:/sbin
make DESTDIR=$RPM_BUILD_ROOT install 

# Clean out our build directory
%clean
rm -fr $RPM_BUILD_ROOT

%files
/usr/local/bin/nprobe
/usr/local/lib/libnprobe-5.5.5.so
/usr/local/lib/libnprobe.a
/usr/local/lib/libnprobe.la
/usr/local/lib/libnprobe.so
/usr/local/lib/nprobe/plugins/librtpPlugin-5.5.5.so
/usr/local/lib/nprobe/plugins/librtpPlugin.a
/usr/local/lib/nprobe/plugins/librtpPlugin.la
/usr/local/lib/nprobe/plugins/librtpPlugin.so
/usr/local/lib/nprobe/plugins/libsipPlugin-5.5.5.so
/usr/local/lib/nprobe/plugins/libsipPlugin.a
/usr/local/lib/nprobe/plugins/libsipPlugin.la
/usr/local/lib/nprobe/plugins/libsipPlugin.so
/usr/local/lib/nprobe/plugins/libdbPlugin-5.5.5.so
/usr/local/lib/nprobe/plugins/libdbPlugin.a
/usr/local/lib/nprobe/plugins/libdbPlugin.la
/usr/local/lib/nprobe/plugins/libdbPlugin.so
/usr/local/lib/nprobe/plugins/libsmtpPlugin-5.5.5.so
/usr/local/lib/nprobe/plugins/libsmtpPlugin.a
/usr/local/lib/nprobe/plugins/libsmtpPlugin.la
/usr/local/lib/nprobe/plugins/libsmtpPlugin.so
/usr/local/lib/nprobe/plugins/libdumpPlugin-5.5.5.so
/usr/local/lib/nprobe/plugins/libdumpPlugin.a
/usr/local/lib/nprobe/plugins/libdumpPlugin.la
/usr/local/lib/nprobe/plugins/libdumpPlugin.so
/usr/local/lib/nprobe/plugins/libhttpPlugin-5.5.5.so
/usr/local/lib/nprobe/plugins/libhttpPlugin.a
/usr/local/lib/nprobe/plugins/libhttpPlugin.la
/usr/local/lib/nprobe/plugins/libhttpPlugin.so
/usr/local/lib/nprobe/plugins/libflowIdPlugin-5.5.5.so
/usr/local/lib/nprobe/plugins/libflowIdPlugin.a
/usr/local/lib/nprobe/plugins/libflowIdPlugin.la
/usr/local/lib/nprobe/plugins/libflowIdPlugin.so
/usr/local/lib/nprobe/plugins/libl7Plugin-5.5.5.so
/usr/local/lib/nprobe/plugins/libl7Plugin.a
/usr/local/lib/nprobe/plugins/libl7Plugin.la
/usr/local/lib/nprobe/plugins/libl7Plugin.so






# Set the default attributes of all of the files specified to have an
# owner and group of root and to inherit the permissions of the file
# itself.
%defattr(-, root, root)

%changelog
* Fri Jan 27 2006 Fernanda Weiden <nanda@google.com> 4.0
- Original upstream version


