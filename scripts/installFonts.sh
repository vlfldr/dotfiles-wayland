#! /bin/bash

# usage: installFont.sh /path/to/font FamilyName

mkdir -p /usr/local/share/fonts/"$2"
cp "$1" /usr/local/share/fonts/"$2"
chown -R root: /usr/local/share/fonts/"$2"
chmod 644 /usr/local/share/fonts/"$2"/*
restorecon -RF /usr/local/share/fonts/"$2"
fc-cache -v
