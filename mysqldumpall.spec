# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
%define is_mandrake %(test -e /etc/mandrake-release && echo 1 || echo 0)
%define is_suse %(test -e /etc/SuSE-release && echo 1 || echo 0)
%define is_fedora %(test -e /etc/fedora-release && echo 1 || echo 0)
%define is_centos %(( test -e /etc/redhat-release && grep -qi centos /etc/redhat-release ) && echo 1 || echo 0)

%define dist redhat
%define disttag rh

%if %is_mandrake
%define dist mandrake
%define disttag mdk
%endif
%if %is_suse
%define dist suse
%define disttag suse
%define kde_path /opt/kde3
%endif
%if %is_fedora
%define dist fedora
%define disttag rhfc
%endif
%if %is_centos
%define dist centos
%define disttag centos
%endif

%define distver %(release="`rpm -q --queryformat='%{VERSION}' %{dist}-release 2> /dev/null | tr . : | sed s/://g`" ; if test $? != 0 ; then release="" ; fi ; echo "$release")

# Derive the version from the file's svn tag
%define svn_version %(echo '$Rev$'| awk '{ print $2 }')

# cmdb server's root
%define config_folder /etc/adm
%define backup_folder /var/backups

%define appl_conf %{appl_root}/etc
%define appl_bin %{appl_root}/bin
%define appl_doc %{appl_root}/doc
%define appl_libexec %{appl_root}/libexec

# --------------------------------------
# Header
# --------------------------------------
Name:      mysqldumpall
Summary:   a non-interactive mysql dumping tool
Version:   %{svn_version}
Release:   1.%{disttag}%{distver}
License:   Artistic/GPL
Vendor:    John van Zantvoort
Packager:  John van Zantvoort <snl.jydawg@gmail.com>
Group:     Applications/System
Source:    %{name}-%version.tar.gz
Requires:  perl,mysql,gzip,perl-DBD-MySQL
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-build
BuildRequires: perl,bash,perl-DBD-MySQL
BuildArch: noarch

# --------------------------------------
# Description
# --------------------------------------
%description
mysqldumpall is meant as a non-interactive mysql dumping tool. It can be
used to keep an archive of "past versions" or to use in combination with
e.g. rsnapshot. It's a Q&D script so no doubt it can be revamped
thoroughly.

%prep
%setup

%build
%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{config_folder}
%{__mkdir_p} %{buildroot}%{backup_folder}

%{__cat} mysqldumpall | %{__sed} "s,\@CONFIG_FOLDER\@,/etc/adm,g" >mysqldumpall.tmp
%{__mv}  mysqldumpall.tmp mysqldumpall
%{__cat} mysqldumpall | %{__sed} "s,\@OUTPUTDIR\@,/var/backups,g" >mysqldumpall.tmp
%{__mv}  mysqldumpall.tmp mysqldumpall
%{__cat} mysqldumpall | %{__sed} "s,\@MYSQLDUMP\@,/usr/bin/mysqldump,g" >mysqldumpall.tmp
%{__mv}  mysqldumpall.tmp mysqldumpall
%{__cat} mysqldumpall | %{__sed} "s,\@GZIP\@,/bin/gzip,g" >mysqldumpall.tmp
%{__mv}  mysqldumpall.tmp mysqldumpall
%{__cat} mysqldumpall | %{__sed} "s,\@BACKUP_FOLDER\@,/var/backups,g" >mysqldumpall.tmp
%{__mv}  mysqldumpall.tmp mysqldumpall
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__mkdir_p} %{buildroot}%{_bindir}
%{__perl} "-MExtUtils::Command::MM" -e pod2man "--" --section=3 --perm_rw=644 mysqldumpall %{buildroot}%{_mandir}/man1/mysqldumpall.1
%{__install} -m 755 mysqldumpall %{buildroot}%{_bindir}/mysqldumpall
%{__install} -m 700 examples/mysqldumpall.cfg.normal %{buildroot}%{config_folder}/mysqldumpall.cfg

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc %{_mandir}/man1/*
%config %{config_folder}/*
%{_bindir}/*

# LC_TIME=en_US date +"%a %b %e %Y"
%changelog
* Thu Feb 07 2008 John van Zantvoort
- trunk/mysqldumpall.spec:
  updated changelog and revision handling, fixed typo

* Mon Feb 04 2008 John van Zantvoort 
- trunk/mysqldumpall: Moved some of the functionality to subroutines.
  Added extended insert support.

* Tue Jan 22 2008 John van Zantvoort
- trunk/mysqldumpall.spec
  - initial version of the spec file
  - added keywords

* Mon Jan 21 2008 John van Zantvoort
- trunk/install.sh:
  - added installer script
  - minor mods
  - typo's
- trunk/mysqldumpall:
  - updated pod and set a default folder for the output.
  - minor mod
  - typo's
- trunk/examples/mysqldumpall.cfg.normal:
  - added example
- trunk/examples/mysqldumpall.cfg.weekly: added
  - added examples

* Fri Jan 18 2008 John van Zantvoort
- mysqldumpall:
  - intial import
  - minor bugfix in the output filename. And some comment correction
- branches:
  - created forgotten branches
- tags:
  - created forgotten branches
- trunk:
  - created forgotten branches
- mysqldumpall -> trunk/mysqldumpall:
  - moved file to correct location
