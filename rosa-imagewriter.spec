%define debug_package %{nil}

Name:       rosa-imagewriter
Summary:    Tool for writing to USB
Version:    2.1
Release:    1
URL:        https://abf.rosalinux.ru/captainflint/rosa-image-writer
Source0:    %{name}-%{version}.tar.xz
License:    GPL
Group:      File tools
Requires:   %mklibname qt5core5
Requires:   %mklibname qt5gui5
Requires:   %mklibname qt5widgets5
Requires:   %mklibname qt5gui5-x11
BuildRequires:  qt5-devel
BuildRequires:  qt5-linguist-tools
BuildRequires:  qmake5

%description
ROSA Image Writer is a tool for creating bootable ROSA installation USB flash
drives.

%prep
%setup -q -n %{name}-%{version}

%build
/usr/lib/qt5/bin/qmake
make
/usr/lib/qt5/bin/lrelease RosaImageWriter.pro

%install
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_bindir} %{buildroot}%{_libdir}/%{name}/lang %{buildroot}%{_docdir}/%{name}
install -m 0755 RosaImageWriter %{buildroot}%{_libdir}/%{name}
install -m 0644 lang/*.qm %{buildroot}%{_libdir}/%{name}/lang/
install -m 0644 doc/* %{buildroot}%{_docdir}/%{name}/
#ln -sf consolehelper %{buildroot}%{_bindir}/%{name}

#cat > %{buildroot}%{_sysconfdir}/pam.d/%{name}  <<EOF
##%PAM-1.0
#auth		include		config-util
#account		include		config-util
#session		include		config-util
#EOF

cat > %{buildroot}%{_bindir}/%{name}  <<EOF
#!/bin/sh
kdesu %{_libdir}/%{name}
EOF

cat > %{buildroot}%{_sbindir}/%{name}  <<EOF
#!/bin/sh
%{_libdir}/%{name}
EOF

chmod 0755 %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_libdir}/%{name}
%{_libdir}/%{name}/lang
%{_docdir}/%{name}
