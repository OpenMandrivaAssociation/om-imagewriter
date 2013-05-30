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
Requires:   b64qt5gui5-x11
BuildRequires:  qt5-devel
BuildRequires:  qmake5

%description
ROSA Image Writer is a tool for creating bootable ROSA installation USB flash
drives.

%prep
%setup -q -n %{name}-%{version}

%build
/usr/lib/qt5/bin/qmake
make

%install
mkdir -p %{buildroot}%{_sbindir}
install -m 0755 RosaImageWriter %{buildroot}%{_sbindir}/rosa-imagewriter

%files
%defattr(-,root,root)
%{_sbindir}/rosa-imagewriter
