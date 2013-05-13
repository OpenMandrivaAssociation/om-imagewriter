Name: rosa-imagewriter
Summary: Utility for writing raw disk images and hybrid isos to USB keys
Version: 1.10
Release: 2
License: GPLv2
Group:   Networking/File transfer 
Source0: %{name}-%{version}.tar.gz
Url: https://abf.rosalinux.ru/dsilakov/rosa-imagewriter

BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: pkgconfig(Qt3Support)

%description
Utility for writing raw disk images and hybrid isos to USB keys.
Based on SUSE Studio Imagewriter

%prep
%setup -q

%build
qmake DEFINES=USEUDISKS2
make

%install
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_datadir}
install -m 755 -p imagewriter %{buildroot}/%{_sbindir}/rosa-imagewriter
cp -r icons %{buildroot}/%{_datadir}

%files
%{_sbindir}/rosa-imagewriter
%{_iconsdir}/*