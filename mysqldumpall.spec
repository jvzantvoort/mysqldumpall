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
Version:   1.0.2
Release:   1
License:   Artistic/GPL
Vendor:    John van Zantvoort
Packager:  John van Zantvoort
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
* Sat Sep 08 2012 John van Zantvoort <John@vanZantvoort.org> 1.0.2-1
- new package built with tito

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
