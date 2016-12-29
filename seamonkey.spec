%if 0%{!?rhel}
%bcond_without	system_nspr
%bcond_without	system_nss
%bcond_without	system_libvpx
%bcond_without	system_icu
%bcond_without	system_sqlite
%endif

%bcond_without	system_ffi
%bcond_with	system_cairo

%bcond_without	langpacks
%bcond_with	calendar

%global nspr_version	4.12
%global nss_version	3.25
%global libvpx_version	1.5.0
%global icu_version	50.1
%global sqlite_version	3.13.0
%global ffi_version	3.0.9
%global cairo_version	1.10

%define homepage file:///usr/share/doc/HTML/index.html

%define sources_subdir %{name}-%{version}

%define seamonkey_app_id	\{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a\}


Name:           seamonkey
Summary:        Web browser, e-mail, news, IRC client, HTML editor
Version:        2.46
Release:        2%{?dist}
URL:            http://www.seamonkey-project.org
License:        MPLv2.0
Group:          Applications/Internet

Source0:        http://archive.mozilla.org/pub/seamonkey/releases/%{version}/source/seamonkey-%{version}.source.tar.xz

%if %{with langpacks}
#  Generate it by moz-grab-langpacks script, which can be obtained from
#  http://fedorapeople.org/cgit/caillon/public_git/gecko-maint.git/
#  and probably perform "sed -i 's/pyfedpkg/pyrpkg/g' moz-grab-langpacks"
#  and correct urls:
#     sed -i 's|ftp://ftp.mozilla.org/pub/mozilla.org|http://archive.mozilla.org/pub|' moz-grab-langpacks"
#
#   Run script as  ./moz-grab-langpacks --app seamonkey %{version}
#
Source1:        seamonkey-langpacks-%{version}-20161222.tar.xz
%endif

Source3:        seamonkey.sh.in
Source4:        seamonkey.desktop
Source12:       seamonkey-mail.desktop
Source13:       seamonkey-mail.svg
Source100:      seamonkey-find-requires.sh

Patch2:		firefox-48-jemalloc-ppc.patch
Patch3:		xulrunner-27.0-build-arm.patch
Patch4:		firefox-33-rhbz-966424.patch
Patch5:		firefox-35-rhbz-1173156.patch
Patch6:		firefox-48-build-prbool.patch
Patch7:		firefox-48-mozilla-1005640.patch
Patch8:		firefox-48-mozilla-256180.patch
Patch10:	firefox-49-mozilla-440908.patch
Patch11:	firefox-49-old-ffmpeg.patch
Patch22:	seamonkey-2.46-installdir.patch
Patch27:	seamonkey-2.46-exthandler.patch

Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{?with_system_nspr:BuildRequires:      nspr-devel >= %{nspr_version}}
%{?with_system_nss:BuildRequires:       nss-devel >= %{nss_version}}
%{?with_system_nss:BuildRequires:       nss-static >= %{nss_version}}
%{?with_system_libvpx:BuildRequires:    libvpx-devel >= %{libvpx_version}}
%{?with_system_icu:BuildRequires:       libicu-devel >= %{icu_version}}
%{?with_system_sqlite:BuildRequires:    sqlite-devel >= %{sqlite_version}}
%{?with_system_ffi:BuildRequires:       libffi-devel >= %{ffi_version}}
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
BuildRequires:  libnotify-devel
BuildRequires:  yasm >= 1.1
BuildRequires:  mesa-libGL-devel
BuildRequires:  pulseaudio-libs-devel

BuildRequires:  autoconf213

Requires:       system-bookmarks
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
# armv7hl: http://bugzilla.redhat.com/bugzilla/1035485
ExclusiveArch:  %{ix86} x86_64

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
%patch2 -p1 -b .jemalloc-ppc
%patch3 -p2 -b .build-arm
%patch4 -p2 -b .966424
%patch5 -p2 -b .1173156
%patch6 -p1 -b .prbool
%patch7 -p1 -b .1005640
%patch8 -p1 -b .256180
%patch10 -p1 -b .440908
%patch11 -p1 -b .old-ffmpeg
popd

%patch22 -p2 -b .installdir
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
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}

ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-bz2
#  system png is disabled because Mozilla requires APNG support in libpng
#ac_add_options --with-system-png
ac_add_options --with-pthreads
ac_add_options --disable-tests
ac_add_options --disable-install-strip
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-extensions=default
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
echo "ac_add_options --with%{!?with_system_libvpx:out}-system-libvpx" >> .mozconfig
echo "ac_add_options --with%{!?with_system_icu:out}-system-icu" >> .mozconfig

echo "ac_add_options --%{?with_system_sqlite:en}%{!?with_system_sqlite:dis}able-system-sqlite" >> .mozconfig
echo "ac_add_options --%{?with_system_ffi:en}%{!?with_system_ffi:dis}able-system-ffi" >> .mozconfig
echo "ac_add_options --%{?with_system_cairo:en}%{!?with_system_cairo:dis}able-system-cairo" >> .mozconfig

echo "ac_add_options --%{?with_calendar:en}%{!?with_calendar:dis}able-calendar" >> .mozconfig


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
pref("gfx.xrender.enabled",true);

/*  use system dictionaries (hunspell)   */
pref("spellchecker.dictionary_path","%{_datadir}/myspell");

/* Allow sending credetials to all https:// sites */
pref("network.negotiate-auth.trusted-uris", "https://");

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

#  needed for -Werror=format-security
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat"

# Disable null pointer gcc6 optimization in gcc6 (rhbz#1328045)
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"

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
update-desktop-database -q &> /dev/null
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database -q &> /dev/null
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
* Thu Dec 29 2016 Jajauma's Packages <jajauma@yandex.ru> - 2.46-2
- Adaptation for RHEL

* Fri Dec 23 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.46-1
- update to 2.46
- apply some patches from firefox-49 package
- avoid runtime linking with too old ffmpeg libraries (#1330898)
- still enable XRender extension by default

* Thu Aug  4 2016 Jan Horak <jhorak@redhat.com> - 2.40-9
- Revert changes introduced by 2.40-7. The system-bookmarks is
  required for new profiles

* Tue Aug  2 2016 Jan Horak <jhorak@redhat.com> - 2.40-8
- Bump release due to rebuild

* Mon Aug  1 2016 Jan Horak <jhorak@redhat.com> - 2.40-7
- Seamonkey no longer require system-bookmarks during installation
  (rhbz#1361851)

* Tue Jul 22 2016 Tom Callaway <spot@fedoraproject.org> - 2.40-6
- rebuild for libvpx 1.6.0

* Tue Jul  5 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.40-5
- Disable null pointer gcc6 optimization in gcc-6.x (#1328045)

* Sun Jul  3 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.40-4
- add fix for gcc-6.x (mozilla bug #1245783)

* Tue Jun 14 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.40-3
- disable extra updatecheck (#1346171)
- enable full-screen-api by default for media support

* Mon Apr 18 2016 Caolán McNamara <caolanm@redhat.com> 2.40-2
- rebuild for hunspell 1.4.0

* Tue Mar 15 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.40-1
- update to 2.40

* Tue Feb 16 2016 Martin Stransky <stransky@redhat.com> 2.39-5
- Added gcc6 build fix

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Dmitry Butskoy <Dmitry@Butskoy.name> 2.39-3
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
- more robast helper detection when content type reported wrongly
- change some defaults to be the same as in Firefox:
    - delete temporary helpers files on exit
    - disable autoupdates by default
    - match OS locale by default
- avoid ppc64le builds as well (#866589)
- build with system sqlite and libffi

* Tue Dec  1 2015 Tom Callaway <spot@fedoraproject.org> 2.39-2
- rebuild for libvpx 1.5.0

* Mon Nov 16 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.39-1
- update to 2.39

* Sun Oct 11 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.38-1
- update to 2.38

* Sun Sep 13 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.35-1
- update to 2.35

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.33.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Mon Apr 13 2015 Dmitry Butskoy <Dmitry@Butskoy.name>
- cleanup of the startup script (#1210035)

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 2.33.1-2
- rebuild against libvpx 1.4.0

* Thu Mar 26 2015 Dmitry Butskoy <Dmitry@Butskoy.name> 2.33.1-1
- update to 2.33.1

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

* Fri Sep 26 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.29.1-1
- update to 2.29.1

* Sat Sep 20 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.29-1
- update to 2.29
- apply some patches from firefox-32 package

* Wed Aug 20 2014 Kevin Fenzi <kevin@scrye.com> - 2.26.1-3
- Rebuild for rpm bug 1131892

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.26.1-1
- update to 2.26.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  9 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.26-2
- rebuild with new find-requires script

* Fri May  9 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.26-1
- update to 2.26

* Mon Mar 24 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.25-1
- update to 2.25

* Mon Feb 10 2014 Dmitry Butskoy <Dmitry@Butskoy.name> 2.24-1
- update to 2.24

* Wed Dec 18 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.23-1
- update to 2.23

* Wed Nov 27 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.22.1-1
- update to 2.22.1
- don't build for armv7hl (seems not enough memory on the build system, #1035485)

* Sat Nov  2 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.22-1
- update to 2.22

* Thu Sep 19 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.21-1
- update to 2.21

* Thu Aug  8 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.20-1
- update to 2.20

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.19-2
- implement separate switches for system/native nspr, nss and libvpx

* Mon Jul  8 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.19-1
- update to 2.19

* Mon Apr 15 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.17.1-1
- update to 2.17.1

* Wed Apr  3 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.17-1
- update to 2.17
- explicitly require libjpeg-turbo (for JCS_EXTENSIONS)

* Tue Mar 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.16.2-2
- Only build WebRTC on x86 to fix FTBFS on other arches

* Fri Mar 15 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.16.2-1
- update to 2.16.2
- fix desktop files (#887297)

* Tue Mar 12 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.16.1-1
- update to 2.16.1

* Fri Feb 22 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.16-1
- update to 2.16
- fix build langpacks

* Tue Feb  5 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.15.2-1
- update to 2.15.2

* Sun Jan 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.15.1-2
- silence scriptlet output

* Tue Jan 22 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.15.1-1
- update to 2.15.1

* Fri Jan 11 2013 Dmitry Butskoy <Dmitry@Butskoy.name> 2.15-1
- update to 2.15
- don't try to change global user settings for default browser/mail etc.
- add fix for #304121 (derived from Xulrunner)

* Mon Dec  3 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.14.1-1
- update to 2.14.1

* Thu Nov 22 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.14-1
- update to 2.14
- fix elfhack compile

* Wed Oct 31 2012 Dmitry Butskoy <Dmitry@Butskoy.name> 2.13.2-2
- exclude ppc64 arch (hoping it is temporary, #866589)
- fix startup warnings (error console) for omni and inspector
- fix build langpacks
- change License to MPLv2.0
- add seamonkey-related directories in mozilla-filesystem (#865054)
- use proper MOZ_SMP_FLAGS
- add patch for jemalloc for powerpc arches (#852698)
- add patch to avoid decommit memory on powerpc arches (#852698)
- some cleanups in spec file
- drop version from install directories (follow the current firefox
  and thunderbird way)

* Fri Oct 26 2012 Martin Stransky <stransky@redhat.com> 2.13.2-1
- Update to 2.13.2

* Tue Oct 16 2012 Martin Stransky <stransky@redhat.com> 2.13.1-1
- Update to 2.13.1

* Tue Oct 9 2012 Martin Stransky <stransky@redhat.com> 2.13-1
- Update to 2.13

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
