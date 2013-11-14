Name:       rosa-imagewriter
Summary:    Tool for writing ROSA installer to USB drive
Version:    2.4
Release:    1
URL:        https://abf.rosalinux.ru/captainflint/rosa-image-writer
Source0:    %{name}-%{version}.tar.xz
License:    GPL
Group:      File tools
Requires:   %mklibname qt5core5
Requires:   %mklibname qt5gui5
Requires:   %mklibname qt5widgets5
Requires:   %mklibname qt5gui5-x11
Requires:   usermode-consoleonly
BuildRequires:  gcc-c++
BuildRequires:  qt5-devel
BuildRequires:  qt5-linguist-tools
BuildRequires:  qmake5

%description
ROSA Image Writer is a tool for creating bootable ROSA installation USB flash
drives.

%prep
%setup -q -n %{name}-%{version}

%build
%qmake_qt5
make
%_qt5_bindir/lrelease RosaImageWriter.pro

%install
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_bindir} %{buildroot}%{_libdir}/%{name}/lang %{buildroot}%{_docdir}/%{name} %{buildroot}%{_iconsdir}/hicolor/scalable/apps %{buildroot}%{_datadir}/applications %{buildroot}%{_sysconfdir}/pam.d %{buildroot}%{_sysconfdir}/security/console.apps
install -m 0755 RosaImageWriter %{buildroot}%{_libdir}/%{name}/%{name}
install -m 0644 lang/*.qm %{buildroot}%{_libdir}/%{name}/lang/
install -m 0644 doc/* %{buildroot}%{_docdir}/%{name}/
install -m 0644 res/icon-rosa.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Name=ROSA Image Writer
Comment=Tool for writing ROSA installer to USB drive
Exec=/usr/bin/rosa-imagewriter
Icon=rosa-imagewriter
Terminal=false
Type=Application
Categories=System
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop

ln -sf consolehelper %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_sysconfdir}/pam.d/%{name} <<EOF
#%PAM-1.0
auth		include		config-util
account		include		config-util
session		include		config-util
EOF

cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<EOF
USER=root
PROGRAM=/usr/sbin/rosa-imagewriter
FALLBACK=false
SESSION=true
EOF

cat > %{buildroot}%{_sbindir}/%{name}  <<EOF
#!/bin/sh
%{_libdir}/%{name}/%{name}
EOF

chmod 0755 %{buildroot}%{_sbindir}/%{name}

%files
%defattr(-,root,root)
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/security/console.apps/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_libdir}/%{name}
%{_docdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
