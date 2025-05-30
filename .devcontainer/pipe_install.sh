#!/bin/bash

input=$1

if [ "$input" == "amber" ]; then
    pipe="amber"
elif [[ "$input" == "crires+" || "$input" == "cr2re" ]]; then
    pipe="cr2re"
elif [ "$input" == "crires" ]; then
    pipe="crires"
elif [ "$input" == "eris" ]; then
    pipe="eris"
elif [ "$input" == "esotk" ]; then
    pipe="esotk"
elif [[ "$input" == "espresso_da" || "$input" == "espda" ]]; then
    pipe="espda"
elif [[ "$input" == "espresso" || "$input" == "espresso_dr" || "$input" == "espdr" ]]; then
    pipe="espdr"
elif [[ "$input" == "fors1" || "$input" == "fors2" || "$input" == "fors" ]]; then
    pipe="fors"
elif [[ "$input" == "giraffe" || "$input" == "giraf" ]]; then
    pipe="giraf"
elif [ "$input" == "gravity" ]; then
    pipe="gravity"
elif [ "$input" == "harps" ]; then
    pipe="harps"
elif [ "$input" == "hawki" ]; then
    pipe="hawki"
elif [ "$input" == "iiinstrument" ]; then
    pipe="iiinstrument"
elif [ "$input" == "isaac" ]; then
    pipe="isaac"
elif [ "$input" == "kmos" ]; then
    pipe="kmos"
elif [ "$input" == "matisse" ]; then
    pipe="matisse"
elif [ "$input" == "midi" ]; then
    pipe="midi"
elif [ "$input" == "molecfit" ]; then
    pipe="molecfit"
elif [ "$input" == "muse" ]; then
    pipe="muse"
elif [ "$input" == "naco" ]; then
    pipe="naco"
elif [ "$input" == "nirps" ]; then
    pipe="nirps"
elif [[ "$input" == "sinfoni" || "$input" == "sinfo" ]]; then
    pipe="sinfo"
elif [ "$input" == "sofi" ]; then
    pipe="sofi"
elif [[ "$input" == "sphere" || "$input" == "spher" ]]; then
    pipe="spher"
elif [ "$input" == "uves" ]; then
    pipe="uves"
elif [[ "$input" == "vircam" || "$input" == "vcam" ]]; then
    pipe="vcam"
elif [ "$input" == "vimos" ]; then
    pipe="vimos"
elif [ "$input" == "visir" ]; then
    pipe="visir"
elif [[ "$input" == "xshooter" || "$input" == "xshoo" ]]; then
    pipe="xshoo"
else
    echo Pipeline not in the list ... a typo, perhaps?
    pipe=""
    exit 1
fi

echo Installing pipeline ${pipe} (${input}) ...
sudo dnf install -y esopipe-${pipe}-wkf esopipe-${pipe}-datastatic
sudo dnf clean all
