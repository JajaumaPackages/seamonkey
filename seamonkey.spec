
%bcond_without	system_nspr
%bcond_without	system_nss
%bcond_with	system_sqlite
%bcond_without	system_libffi
%bcond_with	system_cairo

%bcond_without	gstreamer

%bcond_without	langpacks

%global nspr_version	4.10.8
%global nss_version	3.19.1
%global sqlite_version	3.8.11.1
%global libffi_version	3.0.9
%global cairo_version	1.10

%define homepage file:///usr/share/doc/HTML/index.html

%define sources_subdir %{name}-%{version}

%define seamonkey_app_id	\{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a\}


Name:           seamonkey
Summary:        Web browser, e-mail, news, IRC client, HTML editor
Version:        2.40
Release:        2%{?dist}
URL:            http://www.seamonkey-project.org
License:        MPLv2.0
Group:          Applications/Internet

Source0:        http://archive.mozilla.org/pub/seamonkey/releases/%{version}/source/seamonkey-%{version}.source.tar.xz

#  Generate it by moz-grab-langpacks script, which can be obtained from
#  http://fedorapeople.org/cgit/caillon/public_git/gecko-maint.git/
#  and probably perform "sed -i 's/pyfedpkg/pyrpkg/g' moz-grab-langpacks"
#  and correct urls:
#     sed -i 's|ftp://ftp.mozilla.org/pub/mozilla.org|http://archive.mozilla.org/pub|' moz-grab-langpacks"
#
#   Run script as  ./moz-grab-langpacks --app seamonkey %{version}
#
Source1:        seamonkey-langpacks-%{version}-20160315.tar.xz

Source3:        seamonkey.sh.in
Source4:        seamonkey.desktop
Source12:       seamonkey-mail.desktop
Source13:       seamonkey-mail.svg
Source100:      find-external-requires

Patch2:		xulrunner-24.0-jemalloc-ppc.patch
Patch3:		xulrunner-27.0-build-arm.patch
Patch4:		firefox-33-rhbz-966424.patch
Patch7:		firefox-35-rhbz-1173156.patch
Patch10:	firefox-33-build-prbool.patch
Patch15:        seamonkey-2.35-enable-addons.patch
Patch20:	seamonkey-2.39-libsuite.patch
Patch22:	seamonkey-2.32-installdir.patch
Patch24:	seamonkey-2.40-nss_3_19_1.patch
Patch27:	seamonkey-2.35-exthandler.patch

Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{?with_system_nspr:BuildRequires:      nspr-devel >= %{nspr_version}}
%{?with_system_nss:BuildRequires:       nss-devel >= %{nss_version}}
%{?with_system_nss:BuildRequires:       nss-static >= %{nss_version}}
%{?with_system_sqlite:BuildRequires:    sqlite-devel >= %{sqlite_version}}
%{?with_system_libffi:BuildRequires:    libffi-devel >= %{libffi_version}}
%{?with_system_cairo:BuildRequires:     cairo-devel >= %{cairo_version}}

BuildRequires:  libpng-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  zlib-devel
BuildRequires:  zip
BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  glib2-devel
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  fileutils
BuildRequires:  alsa-lib-devel
BuildRequires:  hunspell-devel
BuildRequires:  system-bookmarks
BuildRequires:  libnotify-devel
BuildRequires:  libvpx-devel >= 1.3.0
BuildRequires:  yasm >= 1.1
BuildRequires:  mesa-libGL-devel
BuildRequires:  pulseaudio-libs-devel
%if %{with gstreamer}
BuildRequires:  gstreamer-devel, gstreamer-plugins-base-devel
%endif

Requires:       system-bookmarks
Requires:       redhat-indexhtml
Requires:       mozilla-filesystem
Requires:       hicolor-icon-theme
%if %{with system_nspr}
Requires:       nspr >= %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo %{nspr_version})
%endif
%if %{with system_nss}
Requires:       nss >= %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo %{nss_version})
%endif
%if %{with system_sqlite}
Requires:       sqlite >= %(pkg-config --silence-errors --modversion sqlite 2>/dev/null || echo %{sqlite_version})
%endif

# ppc64:   http://bugzilla.redhat.com/bugzilla/866589
ExcludeArch: ppc64
ExcludeArch: ppc64le

AutoProv: 0
%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}


%description
SeaMonkey is an all-in-one Internet application suite. It includes 
a browser, mail/news client, IRC client, JavaScript debugger, and 
a tool to inspect the DOM for web pages. It is derived from the 
application formerly known as Mozilla Application Suite.
 

%prep

%setup -q -c
cd %{sources_subdir}

pushd mozilla
%patch2 -p2 -b .jemalloc-ppc
%patch3 -p2 -b .build-arm
%patch4 -p2 -b .966424
%patch7 -p2 -b .1173156
%patch10 -p1 -b .prbool
popd

%patch15 -p2 -b .addons

%patch20 -p1 -b .libsuite
%patch22 -p2 -b .installdir
%patch24 -p2 -b .nss_3_19_1
%patch27 -p2 -b .exthandler

sed -e 's/-MOZILLA_VERSION//g' \
    -e 's,LIBDIR,%{_libdir},g' %{SOURCE3} >seamonkey.sh

#
#   generate .mozconfig
#

cat >.mozconfig <<EOF
ac_add_options --enable-application=suite

export BUILD_OFFICIAL=1
export MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1

ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}

#  to know where to remove extra things...
ac_add_options --bindir=%{_bindir}
ac_add_options --datadir=%{_datadir}
ac_add_options --libdir=%{_libdir}
ac_add_options --includedir=%{_includedir}

ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-bz2
#  system png is disabled because Mozilla requires APNG support in libpng
#ac_add_options --with-system-png
ac_add_options --with-system-libvpx
ac_add_options --with-pthreads
ac_add_options --disable-tests
ac_add_options --disable-install-strip
ac_add_options --disable-installer
ac_add_options --enable-xinerama
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --disable-xprint
ac_add_options --enable-pango
ac_add_options --enable-svg
ac_add_options --enable-canvas
ac_add_options --enable-extensions=default,irc
ac_add_options --disable-crashreporter
ac_add_options --enable-safe-browsing
ac_add_options --enable-system-hunspell
ac_add_options --disable-updater
ac_add_options --enable-chrome-format=omni
ac_add_options --disable-necko-wifi

EOF
#  .mozconfig


echo "ac_add_options --with%{!?with_system_nspr:out}-system-nspr" >> .mozconfig
echo "ac_add_options --with%{!?with_system_nss:out}-system-nss" >> .mozconfig

echo "ac_add_options --%{?with_system_sqlite:en}%{!?with_system_sqlite:dis}able-system-sqlite" >> .mozconfig
echo "ac_add_options --%{?with_system_libffi:en}%{!?with_system_libffi:dis}able-system-libffi" >> .mozconfig
echo "ac_add_options --%{?with_system_cairo:en}%{!?with_system_cairo:dis}able-system-cairo" >> .mozconfig

echo "ac_add_options --%{?with_gstreamer:en}%{!?with_gstreamer:dis}able-gstreamer" >> .mozconfig

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif


#
#   generate default prefs
#
cat >all-fedora.js <<EOF

pref("app.update.auto", false);
pref("app.update.enabled", false);
pref("app.updatecheck.override", true);
pref("browser.display.use_system_colors", true);
pref("browser.helperApps.deleteTempFileOnExit", true);
pref("general.smoothScroll", true);
pref("intl.locale.matchOS",   true);
pref("extensions.shownSelectionUI", true);
pref("extensions.autoDisableScopes", 0);
pref("shell.checkDefaultApps",   0);
pref("media.gmp-gmpopenh264.provider.enabled",false);
pref("media.gmp-gmpopenh264.autoupdate",false);
pref("media.gmp-gmpopenh264.enabled",false);
pref("media.fragmented-mp4.ffmpeg.enabled",false);
pref("full-screen-api.enabled", true);

/*  use system dictionaries (hunspell)   */
pref("spellchecker.dictionary_path","%{_datadir}/myspell");

EOF
# all-fedora.js

#  default homepage can be actually changed in localized properties only
sed -i -e "s|browser.startup.homepage.*$|browser.startup.homepage = %{homepage}|g" \
	suite/locales/en-US/chrome/browser/region.properties


%build

cd %{sources_subdir}

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e 's/-Wall//')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

%if %(awk '/^MemTotal:/ { print $2 }' /proc/meminfo) <= 4200000
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
export LDFLAGS=$MOZ_LINK_FLAGS
%endif
  
MOZ_SMP_FLAGS=%{?_smp_mflags}
[ ${MOZ_SMP_FLAGS#-j} -gt 8 ] && MOZ_SMP_FLAGS=-j8

make -f client.mk build MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT

cd %{sources_subdir}

DESTDIR=$RPM_BUILD_ROOT make -f client.mk install

#  not needed in non-sdk install
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_libdir}/seamonkey-devel
rm -rf $RPM_BUILD_ROOT%{_datadir}/idl/seamonkey

rm -f $RPM_BUILD_ROOT%{_bindir}/seamonkey
install -p -m 755 seamonkey.sh $RPM_BUILD_ROOT%{_bindir}/seamonkey

#   default prefs
install -p -m 644 all-fedora.js \
	$RPM_BUILD_ROOT/%{_libdir}/seamonkey/defaults/pref/all-fedora.js

ln -f -s %{_datadir}/bookmarks/default-bookmarks.html \
	$RPM_BUILD_ROOT/%{_libdir}/seamonkey/defaults/profile/bookmarks.html

install -d -m 755 $RPM_BUILD_ROOT/%{_libdir}/seamonkey/plugins || :


echo >../seamonkey.lang

%if %{with langpacks}
# Install langpacks 
tar -xf %{SOURCE1}

for langpack in `ls seamonkey-langpacks/*.xpi`; do
    #  seamonkey-langpacks/seamonkey-VERSION.LANG.langpack.xpi
    language=${langpack%.langpack.xpi}
    #  seamonkey-langpacks/seamonkey-VERSION.LANG
    language=${language##*.}
    #  LANG

    dir=$RPM_BUILD_ROOT/%{_libdir}/seamonkey/extensions/langpack-$language@seamonkey.mozilla.org
    mkdir -p $dir

    unzip $langpack -d $dir
    find $dir -type f | xargs chmod 644
    find $dir -name ".mkdir.done" | xargs rm -f

    sed -i -e "s|browser.startup.homepage.*$|browser.startup.homepage = %{homepage}|g" \
           $dir/chrome/$language/locale/$language/navigator-region/region.properties

    jarfile=$dir/chrome/$language.jar
    pushd $dir/chrome/$language
    zip -r -D $jarfile locale
    popd
    rm -rf $dir/chrome/$language  #  now in jarfile

    mv -f $dir/chrome/$language.manifest $dir/chrome.manifest
    #  fix manifest to point to jar
    sed -i -e "s,$language/locale,jar:chrome/$language.jar!/locale," $dir/chrome.manifest 

    language=${language/-/_}
    dir=${dir#$RPM_BUILD_ROOT}
    echo "%%lang($language) $dir" >>../seamonkey.lang
done

rm -rf seamonkey-langpacks
%endif #  with_langpacks


# install desktop files in correct directory
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
desktop-file-install --vendor mozilla \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    --add-category X-Fedora \
    --add-category Application \
    --add-category Network \
    %{SOURCE4}
desktop-file-install --vendor mozilla \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    --add-category X-Fedora \
    --add-category Application \
    --add-category Network \
    %{SOURCE12}

# install icons
pushd $RPM_BUILD_ROOT%{_libdir}/seamonkey/chrome/icons/default
icons=$RPM_BUILD_ROOT%{_datadir}/icons/hicolor
# seamonkey icons
install -p -m 644 -D main-window16.png	$icons/16x16/apps/seamonkey.png
install -p -m 644 -D main-window.png	$icons/32x32/apps/seamonkey.png
install -p -m 644 -D main-window48.png	$icons/48x48/apps/seamonkey.png
install -p -m 644 -D seamonkey.png	$icons/128x128/apps/seamonkey.png
# seamonkey mail icons
install -p -m 644 -D messengerWindow16.png	$icons/16x16/apps/seamonkey-mail.png
install -p -m 644 -D messengerWindow.png	$icons/32x32/apps/seamonkey-mail.png
install -p -m 644 -D messengerWindow48.png	$icons/48x48/apps/seamonkey-mail.png
install -p -m 644 -D %{SOURCE13}		$icons/scalable/apps/seamonkey-mail.svg
popd


# System extensions
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{seamonkey_app_id}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{seamonkey_app_id}


%clean
rm -rf $RPM_BUILD_ROOT


%post
update-desktop-database %{_datadir}/applications
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database %{_datadir}/applications
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f seamonkey.lang
%defattr(-,root,root)

%{_libdir}/seamonkey

%ghost %{_libdir}/seamonkey/removed-files

%{_bindir}/seamonkey
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/*.desktop

%dir %{_datadir}/mozilla/extensions/%{seamonkey_app_id}
%dir %{_libdir}/mozilla/extensions/%{seamonkey_app_id}


%changelog
* Tue Jun 14 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.40-2
- disable extra updatecheck (#1346171)
- enable full-screen-api by default for media support

* Tue Mar 15 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.40-1
- update to 2.40
- more robast helper detection when content type reported wrongly
- delete temporary helpers files on exit (match Firefox way)
- avoid ppc64le builds as well (#866589)

* Tue Jan 19 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.39-2
- use system dictionaries for spell checking
- specify default homepage for builtin default locale (en_US) as well
- drop tons of garbage from libsuite.so component
- massive spec and config files cleanup, including:
    - simplifying of install process and filelist generation
    - drop unneeded sources
    - generate mozconfig and prefs files inside spec file
      (better atomic support for changes and different releases)
    - actually provide information of files' locales for rpm package
    - conditionally build with system cairo, sqlite, libffi

* Mon Nov 16 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.39-1
- update to 2.39

* Mon Oct 19 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.38-1
- update to 2.38
- adapt for EPEL
- use bundled gcc-4.8 for build
- enable gstreamer-0.10 support

* Sun Sep 13 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.35-1
- update to 2.35

* Mon Mar 16 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.33-1
- update to 2.33
- apply some patches from firefox-36 package

* Sun Feb  8 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.32.1-1
- update to 2.32.1

* Tue Jan 20 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.32-1
- update to 2.32
- apply some patches from firefox-35 package
- enable gstreamer-1.0 support

* Mon Dec 15 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.31-1
- update to 2.31
- apply some patches from firefox-34 package

* Sat Oct 25 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.30-1
- update to 2.30
- apply some patches from firefox-33 package

* Sat Sep 20 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.29-1
- update to 2.29
- apply some patches from firefox-32 package
- build with system libvpx now

* Tue Jun 24 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.26.1-1
- update to 2.26.1

* Thu May  8 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.26-1
- update to 2.26
- build with native nss and nspr for now

* Sat Mar 22 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.25-1
- update to 2.25

* Mon Feb 10 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.24-1
- update to 2.24

* Wed Dec 18 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.23-1
- update to 2.23
- drop no more needed patches

* Thu Nov 21 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.22.1-1
- update to 2.22.1

* Fri Nov  1 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.22-1
- update to 2.22
- fix for BEAST issue in startup script (as in #1005611 for Firefox)
- now need to enable rtti for C++ compiling by gcc-4.4
  (ie. drop -fno-rtti flag)

* Wed Sep 18 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.21-1
- update to 2.21
- add patch to avoid c++0x code (not supported with gcc-4.4)

* Wed Aug 14 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.20-2
- rebuild with new system's nspr-4.9.5 and nss-3.14.3

* Thu Aug  8 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.20-1
- update to 2.20
- fix build with system nss-3.14.0

* Mon Jul 15 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.19-2
- use native nspr (version of 4.9.6) instead of the system one (4.9.2).
  Seamonkey-2.19 with nspr patches seems to require at least nspr >= 4.9.3

* Sat Jul  6 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.19-1
- update to 2.19
- use bundled python-2.7 for build
- no more touch omni.ja

* Mon Apr 15 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.17.1-1
- update to 2.17.1

* Wed Apr  3 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.17-1
- update to 2.17
- enable WebRTC
- explicitly require libjpeg-turbo (since old libjpeg
  does not provide all the needed features), drop libjpeg62 patch
- fix build with NSS's hasht.h header from the system nss-softokn-devel < 3.14

* Fri Mar 15 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.16.2-1
- update to 2.16.2

* Tue Mar 12 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.16.1-1
- update to 2.16.1

* Fri Feb 22 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.16-1
- update to 2.16
- fix patch to allow build with system's nspr-4.9.2 instead of nspr-4.9.4
- fix build langpacks

* Mon Feb  4 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.15.2-1
- update to 2.15.2
- fix build with new system nspr-4.9.2

* Mon Jan 21 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.15.1-1
- update to 2.15.1
- add fix for #304121 (derived from Xulrunner)

* Wed Jan  9 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.15-1
- update to 2.15
- disable WebRTC support until nss >= 3.14 appear in RHEL6
- fix build with RHEL6 system nss-3.13.5 (actually cosmetic things was changed)
- fix build with RHEL6 libjpeg library (just use some little old stuff from 3.14.1)
- don't try to change global user settings for default browser/mail etc.

* Mon Dec  3 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.14.1-1
- update to 2.14.1

* Wed Nov 21 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.14-1
- update to 2.14
- change collapsed sidebar patch to upstream git applied one
- fix elfhack compile
 
* Wed Oct 31 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.13.2-1
- update to 2.13.2

* Tue Oct 16 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.13.1-2
- add patch for broken context menus when started with collapsed sidebar
  (upstream bug 802166)

* Mon Oct 15 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.13.1-1
- update to 2.13.1
- build with separate objdir
- exclude ppc64 arch (hoping it is temporary, #866589)

* Thu Oct 11 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.13-1
- update to 2.13
- add patch to avoid decommit memory on powerpc arches (#852698)
- add seamonkey-related directories in mozilla-filesystem (#865054)
- fix build with RHEL6 system nspr-4.9.1 (drop setting nspr thread names,
  as it requires nspr >= 4.9.2, but just can be safely removed from the code)

* Mon Oct  8 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.12.1-2
- drop version from install directories (follow the current
  firefox and thunderbird way)
- change License to MPLv2.0

* Thu Sep 27 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.12.1-1.el6
- port to EPEL6
- use EL6 homepage way
- use proper MOZ_SMP_FLAGS
- fix build langpacks
- fix startup warnings (error console) for omni and inspector
- complete default prefs from the latest RHEL6 Firefox and Fedora 18 Seamonkey
- add patch for jemalloc for powerpc arches (#852698)

* Tue Aug 28 2012 Martin Stransky <stransky@redhat.com> 2.12.1-1
- Update to 2.12.1

* Tue Aug 28 2012 Martin Stransky <stransky@redhat.com> 2.12-1
- Update to 2.12

* Fri Jul 27 2012 Martin Stransky <stransky@redhat.com> 2.11-1
- Update to 2.11

* Thu Jun 21 2012 Martin Stransky <stransky@redhat.com> 2.10.1-1
- Update to 2.10.1

* Thu Jun 7 2012 Allen Hewes <allen@decisiv.net> 2.10-1
- Update to 2.10
- change sed string for version number to support 2 digits
- remove specific .so's from installer manifest
- fix the cache path for header.py and associated files when building
  in srcdir (vs using seperate objdir)

* Mon May 7 2012 Martin Stransky <stransky@redhat.com> 2.9.1-4
- Fixed #717242 - does not adhere to Static Library Packaging Guidelines

* Thu May 3 2012 Martin Stransky <stransky@redhat.com> 2.9.1-3
- Fixed #747411 - seamonkey needs better icons (by Edward Sheldrake)

* Thu May 3 2012 Martin Stransky <stransky@redhat.com> 2.9.1-2
- Fixed directories (#566901)

* Wed May 2 2012 Martin Stransky <stransky@redhat.com> 2.9.1-1
- Update to 2.9.1

* Fri Apr 27 2012 Martin Stransky <stransky@redhat.com> 2.9-1
- Update to 2.9

* Wed Apr  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.8-3
- Add ARM configuration options

* Fri Mar 16 2012 Martin Stransky <stransky@redhat.com> 2.8-2
- gcc 4.7 build fixes

* Thu Mar 15 2012 Martin Stransky <stransky@redhat.com> 2.8-1
- Update to 2.8

* Fri Feb 24 2012 Martin Stransky <stransky@redhat.com> 2.7.1-2
- Added fix for mozbz#727401 - libpng crash

* Tue Feb 14 2012 Martin Stransky <stransky@redhat.com> 2.7.1-1
- Update to 2.7.1

* Mon Feb  6 2012 Martin Stransky <stransky@redhat.com> 2.7-2
- gcc 4.7 build fixes

* Fri Feb  3 2012 Martin Stransky <stransky@redhat.com> 2.7-1
- Update to 2.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Martin Stransky <stransky@redhat.com> 2.5-2
- Fixed langpacks

* Thu Dec  8 2011 Martin Stransky <stransky@redhat.com> 2.5-1
- Update to 2.5

* Fri Oct 14 2011 Dan Horák <dan[at]danny.cz> - 2.4.1-3
- fix build on secondary arches

* Tue Oct 11 2011 Kai Engert <kaie@redhat.com> - 2.4.1-2
- Update to 2.4.1

* Tue Sep 06 2011 Kai Engert <kaie@redhat.com> - 2.3.3-2
- Update to 2.3.3
 
* Sun Aug 21 2011 Kai Engert <kaie@redhat.com> - 2.3-2
- Update to 2.3
 
* Wed May 25 2011 Caolán McNamara <caolanm@redhat.com> - 2.0.14-2
- rebuild for new hunspell

* Fri Apr 29 2011 Jan Horak <jhorak@redhat.com> - 2.0.14-1
- Update to 2.0.14

* Sat Apr  9 2011 Christopher Aillon <caillon@redhat.com> 2.0.13-1
- Update to 2.0.13

* Mon Mar  7 2011 Martin Stransky <stransky@redhat.com> 2.0.12-1
- Update to 2.0.12

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Adel Gadllah <adel.gadllah@gmail.com> 2.0.11-3
- BR dbus-glib-devel

* Tue Jan 04 2011 Adel Gadllah <adel.gadllah@gmail.com> 2.0.11-2
- disabled system cairo, breaks animated gifs (rhbz#628331)

* Mon Dec 13 2010 Martin Stransky <stransky@redhat.com> 2.0.11-1
- Update to 2.0.11

* Mon Nov 1 2010 Martin Stransky <stransky@redhat.com> 2.0.10-1
- Update to 2.0.10

* Thu Oct 21 2010 Martin Stransky <stransky@redhat.com> 2.0.9-1
- Update to 2.0.9

* Wed Oct 13 2010 Martin Stransky <stransky@redhat.com> 2.0.8-2
- Added fix for mozbz#522635

* Wed Sep 22 2010 Martin Stransky <stransky@redhat.com> 2.0.8-1
- Update to 2.0.8

* Tue Jul 20 2010 Martin Stransky <stransky@redhat.com> 2.0.6-1
- Update to 2.0.6

* Wed Jun 23 2010 Martin Stransky <stransky@redhat.com> 2.0.5-1
- Update to 2.0.5

* Thu Apr  1 2010 Martin Stransky <stransky@redhat.com> 2.0.4-1
- Update to 2.0.4

* Wed Feb 17 2010 Martin Stransky <stransky@redhat.com> 2.0.3-1
- Update to 2.0.3

* Thu Dec 17 2009 Jan Horak <jhorak@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Tue Oct 27 2009 Martin Stransky <stransky@redhat.com> 2.0-7
- Update to 2.0

* Wed Oct 21 2009 Martin Stransky <stransky@redhat.com> 2.0-6
- Fixed launcher script

* Mon Oct 19 2009 Martin Stransky <stransky@redhat.com> 2.0-5
- Update to 2.0 RC2

* Tue Oct 13 2009 Martin Stransky <stransky@redhat.com> 2.0-4
- Update to 2.0 RC1

* Wed Sep 23 2009 Martin Stransky <stransky@redhat.com> 2.0-3.beta2
- Update to 2.0 beta 2

* Thu Aug 6 2009 Martin Stransky <stransky@redhat.com> 2.0-2.beta1
- Added fix for #437596

* Wed Jul 22 2009 Martin Stransky <stransky@redhat.com> 2.0-1.beta1
- Update to 2.0 beta 1

* Fri Jul 10 2009 Martin Stransky <stransky@redhat.com> 1.1.17-1
- Update to 1.1.17

* Thu Jun 18 2009 Kai Engert <kaie@redhat.com> 1.1.16-3
- fix categories in desktop files

* Thu May  7 2009 Kai Engert <kaie@redhat.com> 1.1.16-2
- Update to 1.1.16

* Wed May 6 2009 Martin Stransky <stransky@redhat.com> 1.1.15-4
- build with -fno-strict-aliasing (#468415)

* Fri Mar 27 2009 Christopher Aillon <caillon@redhat.com> - 1.15.1-3
- Add patches for MFSA-2009-12, MFSA-2009-13

* Wed Mar 25 2009 Christopher Aillon <caillon@redhat.com> - 1.15.1-2
- Update default homepage

* Wed Mar  4 2009 Fedora Security Response Team <fedora-security-list@redhat.com> - 1.1.15-1
- Update to 1.1.15

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Christopher Aillon <caillon@redhat.com> - 1.1.14-3
- Drop explicit requirement on desktop-file-utils

* Wed Jan 07 2009 Christopher Aillon <caillon@redhat.com> - 1.1.14-2
- Disable the crash dialog

* Wed Dec 17 2008 Kai Engert <kengert@redhat.com> - 1.1.14-1
- Update to 1.1.14
* Thu Dec 11 2008 Kai Engert <kengert@redhat.com> - 1.1.13-1
- Update to 1.1.13
- own additional directories, bug 474039
* Thu Sep 25 2008 Christopher Aillon <caillon@redhat.com> - 1.1.12-1
- Update to 1.1.12
* Sat Jul  6 2008 Christopher Aillon <caillon@redhat.com> - 1.1.10-1
- Update to 1.1.10
- Use bullet characters to match GTK+
* Wed Apr 30 2008 Christopher Aillon <caillon@redhat.com> - 1.1.9-4
- Require mozilla-filesystem and drop its requires
* Thu Apr 17 2008 Kai Engert <kengert@redhat.com> - 1.1.9-3
- add several upstream patches, not yet released:
  425576 (crash), 323508, 378132, 390295, 421622
* Fri Mar 28 2008 Kai Engert <kengert@redhat.com> - 1.1.9-2
- SeaMonkey 1.1.9
* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> - 1.1.8-6
- Use the Fedora system bookmarks as default
* Sat Mar 15 2008 Christopher Aillon <caillon@redhat.com> - 1.1.8-5
- Avoid conflicts between gecko debuginfo packages
* Thu Feb 14 2008 Kai Engert <kengert@redhat.com> - 1.1.8-4
- remove workaround for 432138, use upstream patch
* Sat Feb 09 2008 Kai Engert <kengert@redhat.com> - 1.1.8-3
- make it build with nss 3.12, mozilla bug 399589
- work around an issue with gcc 4.3.0, redhat bug 432138
* Fri Feb 08 2008 Kai Engert <kengert@redhat.com> - 1.1.8-2
- SeaMonkey 1.1.8
* Mon Jan 07 2008 Kai Engert <kengert@redhat.com> - 1.1.7-4
- Create and own /etc/skel/.mozilla
* Mon Dec 03 2007 Kai Engert <kengert@redhat.com> - 1.1.7-3
- fix dependencies, requires nspr 4.6.99 / nss 3.11.99
* Sun Dec 02 2007 Kai Engert <kengert@redhat.com> - 1.1.7-2
- SeaMonkey 1.1.7
* Mon Nov 05 2007 Kai Engert <kengert@redhat.com> - 1.1.6-2
- SeaMonkey 1.1.6
* Fri Oct 19 2007 Kai Engert <kengert@redhat.com> - 1.1.5-2
- SeaMonkey 1.1.5
* Mon Sep 10 2007 Martin Stransky <stransky@redhat.com> 1.1.3-8
- added fix for #246248 - firefox crashes when searching for word "do"
* Tue Aug 28 2007 Kai Engert <kengert@redhat.com> - 1.1.3-7
- Updated license tag
* Tue Aug  7 2007 Martin Stransky <stransky@redhat.com> 1.1.3-6
- removed plugin configuration utility
* Mon Aug 6 2007 Martin Stransky <stransky@redhat.com> 1.1.3-5
- unwrapped plugins moved to the old location
* Mon Jul 30 2007 Martin Stransky <stransky@redhat.com> 1.1.3-4
- added nspluginwrapper support
* Fri Jul 27 2007 Martin Stransky <stransky@redhat.com> - 1.1.3-3
- added pango patches
* Fri Jul 20 2007 Kai Engert <kengert@redhat.com> - 1.1.3-2
- SeaMonkey 1.1.3
* Thu May 31 2007 Kai Engert <kengert@redhat.com> 1.1.2-2
- SeaMonkey 1.1.2
* Wed Feb 28 2007 Kai Engert <kengert@redhat.com> 1.1.1-2
- SeaMonkey 1.1.1
* Wed Feb 07 2007 Kai Engert <kengert@redhat.com> 1.1-2
- Update to SeaMonkey 1.1
- Pull in patches used by Firefox Fedora RPM package.
- Fix the DND implementation to not grab, so it works with new GTK+.
- Fix upgrade path from FC-5 by obsoleting the seamonkey subset
  packages which recently obsoleted mozilla in FC-5.
* Sat Dec 23 2006 Kai Engert <kengert@redhat.com> 1.0.7-1
- SeaMonkey 1.0.7
* Fri Nov 10 2006 Kai Engert <kengert@redhat.com> 1.0.6-2
- Do not run regchrome.
- Fix some .dat and .rdf ghost files.
* Thu Nov 09 2006 Kai Engert <kengert@redhat.com> 1.0.6-1
- SeaMonkey 1.0.6
* Thu Sep 14 2006 Kai Engert <kengert@redhat.com> 1.0.5-1
- SeaMonkey 1.0.5
* Wed Sep 06 2006 Kai Engert <kengert@redhat.com> 1.0.4-8
- patch5 -p0
* Wed Sep 06 2006 Kai Engert <kengert@redhat.com> 1.0.4-7
- Synch patches with those found in the Firefox package.
- Add missing, clean up BuildRequires
- Use --enable-system-cairo
- Use a dynamic approach to require at least the NSPR/NSS 
  library release used at build time.
* Tue Aug 15 2006 Kai Engert <kengert@redhat.com> 1.0.4-6
- Yet another forgotten patch file.
* Tue Aug 15 2006 Kai Engert <kengert@redhat.com> 1.0.4-5
- Commit forgotten visibility patch file.
* Fri Aug  4 2006 Kai Engert <kengert@redhat.com> 1.0.4-4
- Use a different patch to disable visibility.
* Fri Aug  4 2006 Kai Engert <kengert@redhat.com> 1.0.4-3
- Fix a build failure in mailnews mime code.
* Thu Aug 03 2006 Kai Engert <kengert@redhat.com> 1.0.4-2
- SeaMonkey 1.0.4
* Wed Jun 07 2006 Kai Engert <kengert@redhat.com> 1.0.2-1
- Update to SeaMonkey 1.0.2 release
* Fri Apr 14 2006 Kai Engert <kengert@redhat.com> 1.0.1-1
- Update to SeaMonkey 1.0.1 release
* Tue Apr 11 2006 Kai Engert <kengert@redhat.com> 1.0-11
- Fix PreReq statements
* Tue Apr 11 2006 Kai Engert <kengert@redhat.com> 1.0-10
- Added libXt-devel BuildRequires
* Mon Apr 10 2006 Kai Engert <kengert@redhat.com> 1.0-9
- Added dist suffix to release
* Fri Mar 17 2006 Kai Engert <kengert@redhat.com> 1.0-8
- Changed license to MPL
* Tue Mar 14 2006 Kai Engert <kengert@redhat.com> 1.0-7
- updated %%files section, removed %%preun,
- removed explicit nspr/nss requires
* Thu Mar 02 2006 Kai Engert <kengert@redhat.com> 1.0-6
- Use a single package for all included applications.
- Make sure installed JavaScript files are not executable.
- Disable AutoProv, use find-external-requires.
* Fri Feb 10 2006 Kai Engert <kengert@redhat.com> 1.0-4
- Addressed several review comments, see bugzilla.redhat.com #179802.
* Sat Jan 28 2006 Kai Engert <kengert@redhat.com> 1.0-1
- Initial version based on Seamonkey 1.0, using a combination of patches 
  from Mozilla 1.7.x, Firefox 1.5 and Thunderbird 1.5 RPM packages.
