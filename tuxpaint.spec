%define major   0
%define libname %mklibname %{name} %{major}
%define libnamedev %mklibname %{name} -d

Summary:	Simple and fun paint program for kids
Name: 		tuxpaint
Version:	0.9.21
Release:	3
#newer than 9.0 cvs build:
Epoch:		1
License:	GPLv2+
Group:		Graphics
URL:		http://www.newbreedsoftware.com/tuxpaint/
Source: 	%{name}-%{version}.tar.gz
Patch0:		tuxpaint-0.9.20-lin_with_libpng.diff
Patch1:		tuxpaint-0.9.20-fix-makefile_lib64.patch
Patch2:		tuxpaint-0.9.21-libpng15.patch
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	libpaper-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_Pango-devel
#for printing:
Requires: 	netpbm
Suggests:	tuxpaint-config
Suggests:	tuxpaint-stamps
Conflicts:	%{libnamedev}

%description
Tux Paint is a simple paint program gear towards young children. 
It provides a simple but entertaining interface, allows drawing
with brushes, lines, shapes, and 'stamps,' and has a 'magic' 
tool, for special effects. Loading and saving is done via a 
graphical interface, and the underlying environment's 
filesystem isn't exposed (much like programs on PDAs).

%package devel
Summary:	Headers and development libraries from %{name}
Group:		Development/Other
Obsoletes:	%{libnamedev} < 1:0.9.21-3

%description devel
%{name} development headers and libraries.

%prep
%setup -q 
%patch0 -p0
%patch1 -p0
%patch2 -p1
# Fix unreadable files
find . -perm 0600 -exec chmod 0644 '{}' \;

%build
make OPTFLAGS="%{optflags}" PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
make install BUILDPREFIX="%{buildroot}" PKG_ROOT="%{buildroot}" PREFIX="%{_usr}" X11_ICON_PREFIX="%{buildroot}%{_includedir}/X11/pixmaps" LIBDIR=%{_libdir}

%find_lang %{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install	--vendor="" \
			--dir %{buildroot}%{_datadir}/applications \
			--remove-category="Art" \
			src/tuxpaint.desktop

install -m644 data/images/icon16x16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 data/images/icon32x32.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 data/images/icon48x48.png -D %{buildroot}%{_liconsdir}/%{name}.png

rm -Rf %{buildroot}%{_datadir}/applnk

#Fix perms:
chmod -R go+r docs/

#Remove useless installed things 
rm -Rf %{buildroot}%{_datadir}/doc/%{name}
rm -Rf %{buildroot}%{_datadir}/%{name}/images/icon32x32.xpm

%files -f %{name}.lang
%defattr(755,root,root,755)
%{_bindir}/%{name}
%{_bindir}/%{name}-import
%defattr(644,root,root,755)
%doc docs/*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-import.1*
%lang(pl) %{_mandir}/pl/man1/%{name}.1*
%dir %{_sysconfdir}/tuxpaint
%config(noreplace) %{_sysconfdir}/tuxpaint/tuxpaint.conf
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/tuxpaint.desktop
%{_datadir}/pixmaps/*png
%{_includedir}/X11/pixmaps/tuxpaint.xpm
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png

%files devel
%doc %{_datadir}/doc/tuxpaint-dev
%{_bindir}/tp-magic-config
%{_includedir}/%{name}/*.h
%{_mandir}/man1/tp-magic-config.1*


%changelog
* Thu Mar 17 2011 Angelo Naselli <anaselli@mandriva.org> 1:0.9.21-2mdv2011.0
+ Revision: 646211
- Removed unused patches
- Fixed menu position to Educational (some users found hard to find it in Educational/Other)

* Wed Aug 19 2009 Frederik Himpe <fhimpe@mandriva.org> 1:0.9.21-1mdv2010.0
+ Revision: 417890
- Add fribidi-devel BuildRequires
- Update to new version 0.9.21

* Fri Sep 26 2008 Funda Wang <fwang@mandriva.org> 1:0.9.20-3mdv2009.0
+ Revision: 288508
- disable system font as it breaks for latin users

* Fri Sep 26 2008 Funda Wang <fwang@mandriva.org> 1:0.9.20-2mdv2009.0
+ Revision: 288499
- use system font to render

* Fri Aug 01 2008 Funda Wang <fwang@mandriva.org> 1:0.9.20-1mdv2009.0
+ Revision: 259582
- drop kde3 BR
- New version 0.9.20
- rediff patch2, patch5
- drop patch3,4, merged upstream

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat May 03 2008 Funda Wang <fwang@mandriva.org> 1:0.9.19-3mdv2009.0
+ Revision: 200713
- clean file list

* Mon Mar 10 2008 Antoine Ginies <aginies@mandriva.com> 1:0.9.19-2mdv2008.1
+ Revision: 183526
- bump release
- fix 64b
- fix 64b built
- fix SDL_Pango-devel buildrequires
- add SDL_pango-devel buildrequires
- new source
- fix comment lang patch, new version 0.9.19, new devel package, fix png patch

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 16 2007 Jérôme Soyer <saispo@mandriva.org> 1:0.9.17-3mdv2008.0
+ Revision: 88652
- Add patch4 for printing Fix bug #33462

* Sat Aug 25 2007 Funda Wang <fwang@mandriva.org> 1:0.9.17-2mdv2008.0
+ Revision: 71127
- fix comment tag lang name

* Tue Jul 10 2007 Funda Wang <fwang@mandriva.org> 1:0.9.17-1mdv2008.0
+ Revision: 50999
- fix build in x86_64
- Fix desktop entry categories
- BR libpaper-devel
- remove invalid desktop file dir
  more BR
- New version
  removed unused patches


* Mon Dec 11 2006 Jérôme Soyer <saispo@mandriva.org> 0.9.16-1mdv2007.0
+ Revision: 94814
- Add BuildRequires

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Bunzip patches

  + Lenny Cartier <lenny@mandriva.com>
    - Update to 0.9.16
    - Import tuxpaint

* Wed Sep 06 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 0.9.15b-1mdv2007.0
- cleanups
- do parallel build
- xdg menu
- saispo:
	o 0.9.15b
	o force linking against libpng

* Tue Oct 19 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.14-1mdk
- 0.9.14
- regenerate P0 & P1
- parallell make is broken

* Sun Jan 04 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.13-1mdk
- 0.9.13
- fix buildrequires (lib64..)
- regenerate P0 & P1

