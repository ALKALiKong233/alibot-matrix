#!/bin/bash

cd $3
export USE_CCACHE=1
export CCACHE_EXEC=/usr/bin/ccache
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
	make $5 -j$(nproc --all) | tee build.log
else
	export TARGET_BUILD_GAPPS=false
	make $5 -j$(nproc --all) | tee build.log
fi

