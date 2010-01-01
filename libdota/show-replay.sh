#!/bin/bash

wc3dir=~"/.wine/drive_c/Program Files/Warcraft III/"
cp ${1} ${wc3dir}/replay
cd ${wc3dir}
wine "Frozen Throne.exe" -opengl -window -loadfile replay/$(basename ${1})
