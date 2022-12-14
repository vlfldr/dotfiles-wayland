#!/bin/sh

music_dir=~/music

AART_TEMP=${AART_TEMP:-"/tmp/aart"}
AART_NOART=~/.config/ncmpcpp/placeholder.png
AART_VIEWER=${AART_VIEWER:-"sxiv -b"}

extract_art() {
	current_path=$music_dir/$1

	# use ffmpeg to extract album art embedded in music files. copies the same
	# codec to (hopefully) not modify the file at all. Not sure if I have the
	# options for it set correctly, especially the format being image2 for
	# everything.
	ffmpeg -loglevel error -y -i "$current_path" -map "v?" -c copy -f image2 "$AART_TEMP" || return 1

	art="$AART_TEMP"
	printf "found embedded art\n"
	return 0
}

find_folder_art() {
	for art in "$album_dir"/folder.*; do
		[ -f "$art" ] || continue
		printf "found folder art\n"
		return 0
	done

	printf "no folder.*\n"
	return 1
}

find_cover_art() {
	for art in "$album_dir"/cover.*; do
		[ -f "$art" ] || continue
		printf "found cover art\n"
		return 0
	done

	printf "no cover.*\n"
	return 1
}

copy_art() {
	# get diretory of currently playing song
	album_dir="$music_dir/$1"
	album_dir=${album_dir:-}
	album_dir=${album_dir%%"${album_dir##*[!/]}"}
	[ "${album_dir##*/*}" ] && album_dir=.
	album_dir=${album_dir%/*}
	album_dir=${album_dir%%"${album_dir##*[!/]}"}

	find_cover_art || find_folder_art || return 1

	printf "found external art\n"
	return 0
}

no_art() {
	printf "no art found! falling back to default\n"
	art="$AART_NOART"
}

set_art() {
	# attempt to get the album art in various ways
	printf "finding art for %s\n" "$(mpc current)"
	copy_art "$1" || extract_art "$1" || no_art

	# copy the art to the file that's open in the image viewer
	cp -f "$art" "$AART_TEMP"

    # update eww image
    eww update albumArt="$AART_TEMP"

	# make output a bit easier to read
	printf "\n"
}

first_start() {
    # wait for mpd to start
    sleep 10
	# check if mpd is running
	pgrep mpd >/dev/null || exit 1

	# check status of mpd, if it's stopped then wait for mpd to start playing
	# a song. Maybe only check for playing, I leave mpd paused quite often
	mpc status | grep -o "playing\|paused" > /dev/null || mpc current --wait > /dev/null

	# set the art
	set_art "$(mpc -q current -f %file%)"

	# open image viewer on the art and store the pid
}

close_script() {
    # replace file with placeholder until next run
    cp "$AART_NOART" "$AART_TEMP"

	# remove weird artifact when closing
	printf "\n"
	exit 0
}

first_start

trap close_script INT

while true;
do
	old_song="$(mpc current -f %file%)"

	# wait for a player event, if mpd closes then exit
	mpc -q idle player > /dev/null || close_script

	# make sure viewer is still open

	# only change the art if the song changes
	new_song="$(mpc current -f %file%)"
	[ "$old_song" != "$new_song" ] && set_art "$new_song"
done
