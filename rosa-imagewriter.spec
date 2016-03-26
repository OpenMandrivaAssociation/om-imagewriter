%global srcname rosa-imagewriter
# lto causes crash
%define _disable_lto 1

Summary:	Tool for writing ROSA installer to USB drive
Name:		rosa-imagewriter
Version:	2.6.1.1
Release:	3
License:	GPLv3+
Group:		File tools
Url:		https://abf.io/soft/%{srcname}
Source0:	%{url}/archive/%{srcname}-version-%{version}.tar.gz
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(udev)
Requires:	qt5-output-driver-default
Suggests:	%mklibname udev 1
# (tpg) needed for kdesu
Suggests:	kde-cli-tools >= 5.5.5

%description
ROSA Image Writer is a tool for creating bootable ROSA installation USB flash
drives.

%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_docdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/kde4/services/ServiceMenus/*.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

#----------------------------------------------------------------------------

%prep
%setup -q -n %{srcname}-version-%{version}
%apply_patches

%build
%qmake_qt5
make
%{_qt5_bindir}/lrelease RosaImageWriter.pro

# for lrelease
export PATH=%{_qt5_bindir}:$PATH
lang/build-translations

%install
mkdir -p                                                   \
	%{buildroot}%{_bindir}                             \
	%{buildroot}%{_libdir}/%{name}/lang                \
	%{buildroot}%{_docdir}/%{name}                     \
	%{buildroot}%{_iconsdir}/hicolor/scalable/apps     \
	%{buildroot}%{_datadir}/applications               \
	%{buildroot}%{_datadir}/kde4/services/ServiceMenus
install -m 0755 RosaImageWriter %{buildroot}%{_libdir}/%{name}/%{name}
install -m 0644 lang/*.qm %{buildroot}%{_libdir}/%{name}/lang/
install -m 0644 doc/* %{buildroot}%{_docdir}/%{name}/
install -m 0644 res/icon-rosa.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
ln -sf %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Name=ROSA Image Writer
Name[ru]=ROSA Image Writer
Comment=Tool for writing ROSA installer to USB drive
Comment[ru]=Инструментарий записи загрузочных образов ROSA на USB-флэш
Exec=%{_libdir}/%{name}/%{name} %%U
Icon=%{name}
Terminal=false
Type=Application
Categories=System;
MimeType=application/x-iso;application/x-cd-image
EOF

cat > %{buildroot}%{_datadir}/kde4/services/ServiceMenus/riw_write_iso_image.desktop <<EOF
[Desktop Entry]
Type=Service
Actions=WriteIsoImageToUsb;
ServiceTypes=KonqPopupMenu/Plugin
MimeType=application/x-iso;application/x-cd-image;inode/ISO-image

[Desktop Action WriteIsoImageToUsb]
Exec=%{_libdir}/%{name}/%{name} %%U
Name=Write to USB using ROSA ImageWriter
Name[ru]=Записать на USB, используя ROSA ImageWriter
Icon=%{name}
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop
