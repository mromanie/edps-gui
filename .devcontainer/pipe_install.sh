#!/bin/bash

pipe=$1

if [ "$pipe" == "amber" ]; then
    true
elif [[ "$pipe" == "crires+" || "$pipe" == "cr2re" ]]; then
    pipe="cr2re"
elif [ "$pipe" == "crires" ]; then
    true
elif [ "$pipe" == "eris" ]; then
    true
elif [ "$pipe" == "esotk" ]; then
    true
elif [[ "$pipe" == "espresso_da" || "$pipe" == "espda" ]]; then
    pipe="espda"
elif [[ "$pipe" == "espresso" || "$pipe" == "espresso_dr" || "$pipe" == "espdr" ]]; then
    pipe="espdr"
elif [[ "$pipe" == "fors1" || "$pipe" == "fors2" || "$pipe" == "fors" ]]; then
    pipe="fors"
elif [[ "$pipe" == "giraffe" || "$pipe" == "giraf" ]]; then
    pipe="giraf"
elif [ "$pipe" == "gravity" ]; then
    true
elif [ "$pipe" == "harps" ]; then
    true
elif [ "$pipe" == "hawki" ]; then
    true
elif [ "$pipe" == "iiinstrument" ]; then
    true
elif [ "$pipe" == "isaac" ]; then
    true
elif [ "$pipe" == "kmos" ]; then
    true
elif [ "$pipe" == "matisse" ]; then
    true
elif [ "$pipe" == "midi" ]; then
    true
elif [ "$pipe" == "molecfit" ]; then
    true
elif [ "$pipe" == "muse" ]; then
    true
elif [ "$pipe" == "naco" ]; then
    true
elif [ "$pipe" == "nirps" ]; then
    true
elif [[ "$pipe" == "sinfoni" || "$pipe" == "sinfo" ]]; then
    pipe="sinfo"
elif [ "$pipe" == "sofi" ]; then
    true
elif [[ "$pipe" == "sphere" || "$pipe" == "spher" ]]; then
    pipe="spher"
elif [ "$pipe" == "uves" ]; then
    true
elif [[ "$pipe" == "vircam" || "$pipe" == "vcam" ]]; then
    pipe="vcam"
elif [ "$pipe" == "vimos" ]; then
    true
elif [ "$pipe" == "visir" ]; then
    true
elif [[ "$pipe" == "xshooter" || "$pipe" == "xshoo" ]]; then
    pipe="xshoo"
else
    echo Pipeline not in the list ... a typo, perhaps?
    pipe=""
    exit 1
fi

echo Installing pipeline ${pipe}
dnf install -y esopipe-${PIPE}-wkf esopipe-${PIPE}-datastatic
dnf clean all
