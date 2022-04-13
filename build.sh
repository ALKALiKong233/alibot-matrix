#!/bin/bash

cd $3
. build/envsetup.sh
lunch $4
if [ $1 -eq 1 ]
then
	mka installclean
else 
	echo "NO installclean!"
fi
if [ $2 -eq 1 ]
then
	export TARGET_BUILD_GAPPS=true
	make yaap -j$(nproc --all) | tee build.log
else
	export TARGET_BUILD_GAPPS=false
	make yaap -j$(nproc --all) | tee build.log
fi

