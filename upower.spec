Summary:        Power Management Service
Name:           upower
Version:        0.9.5
Release:        5%{?dist}
License:        GPLv2+
Group:          System Environment/Libraries
URL:            http://hal.freedesktop.org/releases/
Source0:        http://hal.freedesktop.org/releases/upower-%{version}.tar.bz2
BuildRequires:  sqlite-devel
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  libgudev1-devel
%ifnarch s390 s390x
BuildRequires:  libusb1-devel
BuildRequires:  libimobiledevice-devel
%endif
BuildRequires:  glib2-devel >= 2.6.0
BuildRequires:  dbus-devel  >= 1.2
BuildRequires:  dbus-glib-devel >= 0.82
BuildRequires:  polkit-devel >= 0.92
BuildRequires:  gobject-introspection-devel
Requires:       polkit >= 0.92
Requires:       udev
Requires:       pm-utils >= 1.2.2.1
Requires:       gobject-introspection

# Upstream: don't crash with new polkits.
Patch0:    upower-0.9.6-ensure-gerror-is-init.patch

# Old project name
Obsoletes: DeviceKit-power < 1:0.9.0-2

# We will drop this in F15
Provides: DeviceKit-power

%description
UPower (formerly DeviceKit-power) provides a daemon, API and command
line tools for managing power devices attached to the system.

%package devel
Summary: Headers and libraries for UPower
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: gtk-doc
Obsoletes: DeviceKit-power-devel < 1:0.9.0-2
# We will drop this in F15
Provides: DeviceKit-power-devel

%description devel
Headers and libraries for UPower.

%prep
%setup -q
%patch0 -p1 -b .new-polkit

%build
%configure \
        --enable-gtk-doc \
        --disable-static \
        --enable-introspection \
%ifarch s390 s390x
	--with-backend=dummy
%endif

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang upower

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f upower.lang
%defattr(-,root,root,-)
%doc NEWS COPYING AUTHORS HACKING README
%{_libdir}/libdevkit-power-gobject*.so.*
%{_libdir}/libupower-glib.so.*
%{_sysconfdir}/dbus-1/system.d/*.conf
%ifnarch s390 s390x
/lib/udev/rules.d/*.rules
%endif
%dir %{_localstatedir}/lib/upower
%dir %{_sysconfdir}/UPower
%config %{_sysconfdir}/UPower/UPower.conf
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service

%files devel
%defattr(-,root,root,-)
%{_datadir}/dbus-1/interfaces/*.xml
%dir %{_datadir}/gtk-doc/html/UPower
%{_datadir}/gtk-doc/html/UPower/*
%{_libdir}/libdevkit-power-gobject*.so
%{_libdir}/libupower-glib.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/DeviceKit-power/devkit-power-gobject
%{_includedir}/DeviceKit-power/devkit-power-gobject/*.h
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/gir-1.0/*.gir
%dir %{_includedir}/libupower-glib
%{_includedir}/libupower-glib/up-*.h
%{_includedir}/libupower-glib/upower.h

%changelog
* Tue Aug 10 2010 Richard Hughes <rhughes@redhat.com> - 0.9.5-5
- Ensure we've initialized errors when calling into PolicyKit.
- Resolves: #622830

* Mon Jul 26 2010 Bastien Nocera <bnocera@redhat.com> 0.9.5-4
- Add support for iDevice battery checking

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 0.9.5-3
- use dummy backend on s390(x) because the Linux backend requires USB

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.9.5-2
- Rebuild against new gobject-introspection

* Mon Jul 12 2010 Richard Hughes <rhughes@redhat.com> - 0.9.5-1
- New upstream release.

* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> - 0.9.4-1
- Make my laptop suspend again when I close the lid

* Thu May 06 2010 Richard Hughes <rhughes@redhat.com> - 0.9.3-1
- New upstream release.

* Tue Apr 06 2010 Richard Hughes <rhughes@redhat.com> - 0.9.2-1
- New upstream release.

* Wed Mar 17 2010 Richard Hughes <rhughes@redhat.com> - 0.9.1-4
- It seems people don't like pain.

* Mon Mar 15 2010 Richard Hughes <rhughes@redhat.com> - 0.9.1-3
- Obsolete DeviceKit-power.

* Mon Mar 15 2010 Richard Hughes <rhughes@redhat.com> - 0.9.1-2
- Actually enable the introspection support.

* Wed Mar 03 2010 Richard Hughes <rhughes@redhat.com> - 0.9.1-1
- Initial release of 0.9.1

