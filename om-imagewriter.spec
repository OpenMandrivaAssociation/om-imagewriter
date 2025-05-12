%define debug_package %{nil}
%define _empty_manifest_terminate_build 0
%global srcname rosa-imagewriter
%global _qt6_bindir %{_libdir}/qt6/bin/
# lto causes crash
%define _disable_lto 1

Summary:	Tool for writing installer to USB drive
Name:		om-imagewriter
Version:	2.7.0
Release:	1
License:	GPLv3+
Group:		File tools
# Original (seemingly dead) upstream: https://abf.io/soft/rosa-imagewriter
# Another interesting fork: https://github.com/KaOSx/isowriter
Url:		https://github.com/OpenMandrivaSoftware/om-imagewriter
#Source0:	https://github.com/OpenMandrivaSoftware/om-imagewriter/archive/refs/tags/%{version}.tar.gz
Source0:	https://github.com/OpenMandrivaSoftware/om-imagewriter/archive/refs/tags/%{name}-%{version}.tar.xz
Source1:	om-imagewriter.desktop
Source2:	riw_write_iso_image.desktop

BuildRequires:	pkgconfig(Qt6Linguist)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(udev)

BuildSystem:		cmake

Suggests:	%mklibname udev 1
# (tpg) needed for kdesu
Suggests:	kde-cli-tools >= 6.0.0
%rename rosa-imagewriter

%description
OpenMandriva Image Writer is a tool for creating bootable installation USB flash
drives.

#----------------------------------------------------------------------------

%install -a
mkdir -p  %{buildroot}%{_datadir}/applications/ \
					%{buildroot}%{_datadir}/kio/servicemenus/
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Name=OM Image Writer
Comment=Tool for writing installer to USB drive
Comment[ru]=Инструментарий записи загрузочных образов на USB-флэш
Exec=pkexec %{_bindir}/%{name}/%{name} %%U
Icon=%{name}
Terminal=false
Type=Application
Categories=System;
MimeType=application/x-iso;application/x-cd-image
EOF

cat > %{buildroot}%{_datadir}/kio/servicemenus/riw_write_iso_image.desktop <<EOF
[Desktop Entry]
Type=Service
Actions=WriteIsoImageToUsb;
ServiceTypes=KonqPopupMenu/Plugin
MimeType=application/x-iso;application/x-cd-image;inode/ISO-image

[Desktop Action WriteIsoImageToUsb]
Exec=pkexec %{_bindir}/%{name}/%{name} %%U
Name=Write to USB using OM ImageWriter
Name[ru]=Записать на USB, используя OM ImageWriter
Icon=%{name}
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license %{_licensedir}/%name/LICENSE.html
%{_bindir}/%{name}
%{_docdir}/%{name}
%{_datadir}/polkit-1/actions/org.openmandriva.pkexec.om-imagewriter.policy
%{_datadir}/applications/%{name}.desktop
%{_datadir}/kio/servicemenus/*.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

