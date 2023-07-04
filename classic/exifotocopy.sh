#!/bin/bash
#------------------------------------------------------------------------------------------
# exifotocopy - image file download script
# 2008-2010 Johannes Braun (hannenz@freenet.de), scuba
#------------------------------------------------------------------------------------------
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#
#------------------------------------------------------------------------------------------
# see README for details
#
# NO USER EDITABLE VARS IN HERE!!!! User exifotoconfig instead!!!!!
#------------------------------------------------------------------------------------------

SCRIPTNAME="exifotocopy"
ZENITY_TITLE=${SCRIPTNAME}
CONFIGFILE="${HOME}/.exifotocopy/exifotocopyrc"
VERBOSE=1
source ${CONFIGFILE}

START_TIME=$(date +%s)
declare -a ASKTEXT1
declare -a ASKTEXT2
ASKTEXT1=("enter y or j" "Click OK")
ASKTEXT2=("enter n" "Click CANCEL")

#------------------------------------------------------------------------------------------
# FUNCTIONS
#------------------------------------------------------------------------------------------

#output something (zenity window, stdout and/or logfile)
function output {
	MSSG=${2}
	if [[ ${3} == "fatal" ]] ; then
		MSSG="${MSSG}\nfatal error: exiting."
	fi
	if [[ ${1} != "log" ]] ; then
		((${HAS_ZENITY})) && zenity --${1} --title=${SCRIPT_NAME} --text="${MSSG}" || echo -e "[${SCRIPT_NAME}] $(date) [${1}]\n- ${MSSG}"
	fi
	#log everything
	echo -e "[$0:$(date):$1] ${MSSG}" | tee -a ${LOGFILE}
	if [[ ${3} == "fatal" ]] ; then
		exit
	fi
}

#ask something, either from zenity window or from command line
function ask {
	((${HAS_ZENITY})) && return $(zenity --question --title=${ZENITY_TITLE} --text="${1}")

	#if no zenity, remove all Pango Markup Tags from message
	TEXT=$(echo "${1}" | sed 's/<[^>]*>//g p')
	echo -e -n "${TEXT}\n> "
	read ANSWER
	[ -z ${ANSWER} ] || [ ${ANSWER} = "j" ] || [ ${ANSWER} = "y" ]
	return ${?}
}

#------------------------------------------------------------------------------------------
# MAIN CODE
#------------------------------------------------------------------------------------------

#chedck for dependencies
which ${CMD} >/dev/null || output error "${CMD} is not installed! Either install it or change your CMD variable in ${CONFIGFILE}"

#check if we have zenity
HAS_ZENITY=0
if ((${WANT_ZENITY})) ; then
	which zenity >> /dev/null && HAS_ZENITY=1 || output warning "Zenity is not installed. Output to stdout only, no fancy windows.";
fi

#check if we have jhead
which jhead >/dev/null || output error "jhead is not installed but required by $SCRIPTNAME." fatal

# source directory is either given as parameter 1 to the script or the current directory is used.
SRCDIR="${1:-$(pwd)}"

#let's get going...
INFO_MESSAGE="${SCRIPTNAME} invoked in ${SRCDIR}"
output log "${INFO_MESSAGE}"

if ((${HAS_ZENITY})) ; then
	if ((${NOTIFICATION})) ; then
		exec 3> >( zenity --window-icon="${HOME}/bin/exifotocopy/logo.64.png" --notification --listen)
		echo "message:${INFO_MESSAGE}" >&3
	else
		exec 3> >( zenity --progress --pulsate --auto-close --title="${SCRIPTNAME}" --text="${INFO_MESSAGE}")
	fi
fi

#Search all relevant files
FILES=""
for EXT in ${EXTENSIONS} ; do
	((${HAS_ZENITY})) &&echo "#scanning for ${EXT}" >&3
	RESULT=$(find "${SRCDIR}" -type f -iname "*.$EXT")
	if [ "${RESULT}" != "" ] ; then
		FILES=${FILES}${RESULT}$'\n'
	fi
done

#if no files were found, issue a warning and exit...
[ -z "${FILES}" ] && output warning "no files in ${SRCDIR} matching ${EXTENSIONS}" fatal

#how many files do we have?
N=$(echo "${FILES}" | wc -l)
N=$((N - 1))
output log "${N} files to process:"

if ((${HAS_ZENITY})) && !((${NOTIFICATION})) ; then
	exec 3>&-
fi



#Ask User about the Folder where the photos should be copied to
while [ -z "${PHOTOBASEDIR}" ] ; do
	if ((${HAS_ZENITY})) ; then
		PHOTOBASEDIR=$(zenity --file-selection --title="choose destination folder" --directory --text="choose destination folder")
		if [ ${?} -ne 0 ] ; then
			output info "<b>${SCRIPTNAME}</b>\nOperation cancelled by user"
			exit
		fi
	else
		echo "Please enter the destination path:"
		read PHOTOBASEDIR;
	fi
done

#Optionally prompt user for CMD Options
if [ ${CMD} = "convert" -a -z "${CMDOPTS}" ]; then
	if ((${HAS_ZENITY})) ; then
		ETXT="-resize 1280x800"
		CMDOPTS=$(zenity --entry --text="Enter Options for command: '${CMD}'" --entry-text="${ETXT}")
	else
		echo "Enter Options for command: '${CMD}'"
		read CMDOPTS
	fi
fi

if ((${HAS_ZENITY})) && !((${NOTIFICATION})) ; then
	exec 3> >(zenity --progress --percentage=0 --title="${SCRIPTNAME} (${CMD} ${CMDOPTS})")
fi


#set Inter Field Seperator to split by Newline only so we can have Spaces in Filenames...
IFS='
'
CF=0		#set file counter to zero




#for each file do the following...
for FILE in ${FILES} ; do
	ZENITY_TITLE="${SCRIPTNAME}: processing ${FILE}"
	[ ${VERBOSE} ] && output log "-------------------------------------------------------------------"
	output log "[$(( ${CF} + 1))/${N}] processing ${FILE}"

	#output to zenity progress bar
	if ((${HAS_ZENITY})) ; then
		if ((!${NOTIFICATION})) ; then
			echo $((${CF}*100/${N})) >&3
			if [ ${?} -ne 0 ] ; then
			output info "<b>${SCRIPTNAME}</b>\nOperation cancelled by user"
				exit
			fi
		fi
	fi
	while ((1)) ; do
		#extract date info from EXIF
		DATE=$(jhead "${FILE}" | grep -w 'Date/Time' | tr -d -c "[0-9: ]")
		DATE=${DATE##*: }
		# at this point we should have the date in this format "YYYY:MM:DD HH:MM:SS"
		# to make it readable for the date command, we need it in "YYYY-MM-DD HH:MM:SS"
		DATE="$(echo ${DATE%% *} | tr : -) ${DATE##* }"
		[ ${VERBOSE} ] && output log "EXIF Date=[${DATE}]"

		#do we have a valid date?
		if [ "${DATE}" = " " ] || ! date -d "${DATE}" > /dev/null ; then
			#no, so read the file's timestamp
			output log "invalid EXIF Date (${DATE:-empty}), reading timestamp"
			TIMESTAMP=$(stat -c %z "${FILE}")
			DATE=${TIMESTAMP%%.*}

			if ((${ASK})) ; then
				#ask user what to do...
				output log "asking user what to do"
				QUESTION="\n<b>No Exif Date</b>\n\n<i>'${FILE}'</i>\ndoes not offer Exif information about its creation date.\n${ASKTEXT1[${HAS_ZENITY}]} to use the file's timestamp:\n<i>(${TIMESTAMP})</i>\nor ${ASKTEXT2[${HAS_ZENITY}]} if you know the date and want to enter it manually"
				if ask "${QUESTION}" ; then
					#set date to the file's timestamp
					output log "using timestamp ${TIMESTAMP} as date"
				else
				#prompt calendar to choose a date
					if ((${HAS_ZENITY})) ; then
						DATE=$(zenity --calendar --year="$(echo $((10#${TIMESTAMP:0:4})))" --month="$(echo $((10#${TIMESTAMP:5:2})))" --day="$(echo $((10#${TIMESTAMP:8:2})))" --date-format="%Y-%m-%d %H:%M:%S")
					else
						DATE="invalid"
						until date -d ${DATE} >> /dev/null 2>/dev/null;
						do
							echo "enter date (YYYY-MM-DD HH:MM:SS)"
							read DATE
						done
					fi
					output log "USERdate=${DATE}"
				fi
			fi
			#if for some reason the date is still invalid...
			if ! date -d "$DATE" >> /dev/null ; then
				output error "date ${DATE:+empty} is invalid!"
			fi
		fi
		if [ $(date +%s -d "$DATE") -gt $(date +%s) ] ; then
			ask "Warning! Date ($DATE) is in the future! Are you sure you want to proceed?" && break
		else
			break
		fi
	done


	case ${DESTDEPTH} in
		"1")
			if [ -z "${FMTYEAR}" ] ; then
				output error "using DESTDEPTH=1 requires FMTYEAR to be set. Check Configuration!" fatal
			fi
			DESTPATH="${PHOTOBASEDIR}/$(date +"${FMTYEAR}" -d "${DATE}")"
			;;
		"2")
			if [ -z "${FMTYEAR}" ] || [ -z "${FMTMONTH}" ] ; then
				output error "using DESTDEPTH=2 requires FMTYEAR and FMTMONTH to be set. Check Configuration!" fatal
			fi
			DESTPATH="${PHOTOBASEDIR}/$(date +"${FMTYEAR}" -d "${DATE}")/$(date +"${FMTMONTH}" -d "${DATE}")"
			;;
		"3")
			if [ -z "${FMTYEAR}" ] || [ -z "${FMTMONTH}" ] || [ -z "${FMTDAY}" ] ; then
				output error "using DESTDEPTH=2 requires FMTYEAR, FMTMONTH and FMTDAY to be set. Check Configuration!" fatal
			fi
			DESTPATH="${PHOTOBASEDIR}/$(date +"${FMTYEAR}" -d "${DATE}")/$(date +"${FMTMONTH}" -d "${DATE}")/$(date +"${FMTDAY}" -d "${DATE}")"
			;;
		*)
			output error "invalid DESTDEPTH setting: ${DESTDEPTH}! Check your configuration. Valid choices are 1,2 or 3." fatal
			;;
	esac

	FILENAME_EXTENSION=".${FILE##*.}"

	#assemble dir- & filename
	if [ -z "$DESTPATH" ] ; then
		output error "DESTPATH is empty! Cannot create a directory without a name! Check your settings!"
	fi
	#create a destination directory if not yet existent
	if [ ! -e "$DESTPATH" ] ; then
		mkdir -p "$DESTPATH" || output error "mkdir $DESTPATH failed: Exit Code: $?"
		[ ${VERBOSE} ] && output log "mkdir -p $DESTPATH: success"
	fi
	#how many files do we have in this folder yet?
	NR=`ls -l "$DESTPATH" | wc -l`

	#assemble filename, check if exists
	FILENAME=${FILENAMEHEADER}${FILEDATEFORMAT:+$(date +"${FILEDATEFORMAT}" -d "${DATE}")}${NRFORMAT:+$(printf "$NRFORMAT" "$NR")}${FILENAME_EXTENSION}
	if [ -z "${FILENAME}" ] ; then
		output error "FILENAME is empty. Cannot create a file without a name! Using original filename instead... Check your settings!"
		FILENAME=$(basename "$FILE")
	fi
	DESTFILE="${DESTPATH}/${FILENAME}"
	if [ -e "${DESTFILE}" ] ; then
		#ask user if we can overwrite it
		ask "File \'${DESTFILE}\' exists, overwrite?" || continue
	fi

	#output to Zenity progress bar window
	if ((${HAS_ZENITY})) ; then
		if ((${NOTIFICATION})) ; then
			echo "tooltip:$((CF * 100 / ${N}))% ($CF/$N)\n${FILE}\n${DESTFILE}" >&3
		else
			echo "#${FILE}\n${DESTFILE}" >&3
		fi
	fi
	#finally, do this copy stuff ;)
	[ ${VERBOSE} ] && output log "${CMD} ${CMDOPTS} ${FILE} ${DESTFILE}"
	unset IFS
	${CMD} ${CMDOPTS} "${FILE}" "${DESTFILE}" && let CF=${CF}+1 || output error "${CMD} failed. Exit Code: $?"
done

ELAPSED=$(( $(date +%s) - ${START_TIME} ))
INFO_MESSAGE="${CF} (${N}) files copied from ${SRCDIR} to ${PHOTOBASEDIR} in ${ELAPSED} seconds"

#exit zenity progress bar
if ((${HAS_ZENITY})) ; then
	if ((${NOTIFICATION})) ; then
		echo "message:${INFO_MESSAGE}" >&3
	else
		echo "#${INFO_MESSAGE}" >&3
	fi
	exec 3>&-
fi
output log "${INFO_MESSAGE}"
#SCRIPT END
