#!/bin/sh
#
#
#
CONFIGDIR="/etc/adm"
OUTPUTDIR="/var/backups"
MYSQLDUMP=$(which mysqldump)
GZIP=$(which gzip)
DBUSER="root"
DBHOST="localhost"
DBPASSWD=
RESPONSE=
RSNAPSHOT="no"
COMPRESS="yes"
TIME_FMT="%Y-%m-%d"
CONFIG_FOLDER="/etc/adm"
BACKUP_FOLDER="/var/backups"
MANUAL_FILE="/usr/share/man/man1/mysqldumpall.1"
SCRIPT_FILE=

header() {
  clear
  NAME=`echo $@| tr a-z A-Z`
  echo "--------------------------------------------------------------------------------"
  echo " ${NAME}:"
  echo "                                      For the cowardly: Ctrl-C aborts the script"
  echo "--------------------------------------------------------------------------------"
  echo ""
}

update_script() {
  SCRIPTFILE=$1
  [[ -f "${SCRIPTFILE}.back" ]] || cp "${SCRIPTFILE}" "${SCRIPTFILE}.back"

  # Ugly, ugly, ugly
  cat ${SCRIPTFILE} | sed "s,\@CONFIG_FOLDER\@,$CONFIG_FOLDER,g" >${SCRIPTFILE}.tmp
  mv  ${SCRIPTFILE}.tmp ${SCRIPTFILE}

  cat ${SCRIPTFILE} | sed "s,\@OUTPUTDIR\@,$OUTPUTDIR,g" >${SCRIPTFILE}.tmp
  mv  ${SCRIPTFILE}.tmp ${SCRIPTFILE}

  cat ${SCRIPTFILE} | sed "s,\@MYSQLDUMP\@,$MYSQLDUMP,g" >${SCRIPTFILE}.tmp
  mv  ${SCRIPTFILE}.tmp ${SCRIPTFILE}

  cat ${SCRIPTFILE} | sed "s,\@GZIP\@,$GZIP,g" >${SCRIPTFILE}.tmp
  mv  ${SCRIPTFILE}.tmp ${SCRIPTFILE}

  cat ${SCRIPTFILE} | sed "s,\@BACKUP_FOLDER\@,$BACKUP_FOLDER,g" >${SCRIPTFILE}.tmp
  mv  ${SCRIPTFILE}.tmp ${SCRIPTFILE}

}

echo "mysqldump installer - use this script to install mysqldumpall"
echo "answer the questions, you'll be fine"
echo ""
echo "For the cowardly: Ctrl-C aborts the script"
echo ""
read
header "Script parameters"
# --------------------------------------
# MYSQLDUMP
# --------------------------------------
if [ ! "${MYSQLDUMP}x" = "x" ]
then
  echo -n "mysqldump path [default: $MYSQLDUMP]: "
else
  echo -n "mysqldump path: "
fi

read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || MYSQLDUMP=$RESPONSE
RESPONSE=

# --------------------------------------
# GZIP
# --------------------------------------
if [ ! "${GZIP}x" = "x" ]
then
  echo -n "gzip path [default: $GZIP]: "
else
  echo -n "gzip path: "
fi

read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || GZIP=$RESPONSE
RESPONSE=

# --------------------------------------
# CONFIG_FOLDER
# --------------------------------------
if [ ! "${CONFIG_FOLDER}x" = "x" ]
then
  echo -n "config folder [default: $CONFIG_FOLDER]: "
else
  echo -n "config folder : "
fi

read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || CONFIG_FOLDER=$RESPONSE
RESPONSE=

header "Paths"
# --------------------------------------
# SCRIPT_FILE
# --------------------------------------
SCRIPT_FILE="$(dirname $MYSQLDUMP)/mysqldumpall"
if [ ! "${SCRIPT_FILE}x" = "x" ]
then
  echo -n "mysqldumpall path [default: $SCRIPT_FILE]: "
else
  echo -n "mysqldumpall path: "
fi

read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || SCRIPT_FILE=$RESPONSE
RESPONSE=

# --------------------------------------
# MANUAL_FILE
# --------------------------------------
if [ ! "${MANUAL_FILE}x" = "x" ]
then
  echo -n "manual file path [default: $MANUAL_FILE]: "
else
  echo -n "manual file path: "
fi

read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || MANUAL_FILE=$RESPONSE
RESPONSE=

# ------------------------------------------------------------------------------
# 
# ------------------------------------------------------------------------------
header "Configuration file - main"

echo -n "Configure for rsnapshot (YES|no): "
read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || RSNAPSHOT=`echo $RESPONSE | tr A-Z a-z`
RESPONSE=

echo -n "Use compression (YES|no): "
read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || COMPRESS=`echo $RESPONSE | tr A-Z a-z`
RESPONSE=

echo -n "Set time format [${TIME_FMT}]: "
read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || TIME_FMT=$RESPONSE
RESPONSE=

echo -n "Set backup folder format [${BACKUP_FOLDER}]: "
read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || BACKUP_FOLDER=$RESPONSE
RESPONSE=


header "Configuration file - database"
# --------------------------------------
# DBHOST
# --------------------------------------
echo -n "database host [${DBHOST}]: "
read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || DBHOST=$RESPONSE
RESPONSE=

# --------------------------------------
# DBUSER
# --------------------------------------
echo -n "database user [${DBUSER}]: "
read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || DBUSER=$RESPONSE
RESPONSE=

# --------------------------------------
# DBPASSWD
# --------------------------------------
echo -n "database passwd: "
stty -echo
read RESPONSE
stty echo 
[[ "${RESPONSE}x" = "x" ]] || DBPASSWD=$RESPONSE
RESPONSE=

echo
for parm in CONFIGDIR OUTPUTDIR MYSQLDUMP GZIP DBUSER DBHOST DBPASSWD RSNAPSHOT COMPRESS TIME_FMT CONFIG_FOLDER BACKUP_FOLDER MANUAL_FILE SCRIPT_FILE 
do
  PARM="echo \$${parm}"
  name=$(echo $parm|tr A-Z a-z)
  value=$(eval $PARM)
  printf "%-40s %s\n" $name $value
done

echo -n "Continue (yes|NO): "
read RESPONSE
[[ "${RESPONSE}x" = "x" ]] || RESPONSE=`echo $RESPONSE | tr A-Z a-z`

if [ ! "${RESPONSE}" = "yes" ]
then
  echo "Got ${RESPONSE}. Aborting."
  exit
fi

if [ ! -d "${CONFIG_FOLDER}" ]
then
  install -d -g root -o root -m 0700 $CONFIG_FOLDER
else
  echo "config folder $CONFIG_FOLDER exists"
fi

OF="${CONFIG_FOLDER}/mysqldumpall.cfg"
if [ -f "$OF" ]
then
  echo "Moving original ${OF} to ${OF}.orig"
  mv ${OF} "${OF}.orig"
fi

echo "[main]" >>$OF
echo "rsnapshot = ${RSNAPSHOT}" >>$OF
echo "compress = ${COMPRESS}" >>$OF
echo "time_fmt = ${TIME_FMT}" >>$OF
echo "backup_folder = ${BACKUP_FOLDER}" >>$OF
echo "" >>$OF
echo "[database]" >>$OF
echo "user = $DBUSER" >>$OF
echo "password = $DBPASSWD" >>$OF
echo "host = $DBHOST" >>$OF

if [ ! -d "${BACKUP_FOLDER}" ]
then
  install -d -g root -o root -m 0700 $BACKUP_FOLDER
else
  echo "backup folder $BACKUP_FOLDER exists"
fi

update_script mysqldumpall

pod2man mysqldumpall > mysqldumpall.1
install -g root -o root -m 0755 mysqldumpall $SCRIPT_FILE
install -g root -o root -m 0644 mysqldumpall.1 $MANUAL_FILE
