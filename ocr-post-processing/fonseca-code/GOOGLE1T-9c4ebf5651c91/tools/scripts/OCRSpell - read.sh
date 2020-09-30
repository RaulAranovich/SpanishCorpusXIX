#!/bin/bash
# Script to run OCRSpell

container=($(docker ps | grep unlvcs))

if [ -z $container ]
then
    gnome-terminal -- docker run -it unlvcs/ocrspell-master /bin/bash
    echo "Waiting for docker to load"
    sleep 5
    echo "Finished"
    echo " "
    container=($(docker ps | grep unlvcs/ocrspell))
fi

length=${#container[@]}
name=${container[ $length - 1 ]}
srcpath="ocrspell-master/src"
inpath="ocrspell-master/source-docs"

docker exec $name mkdir "/home/ocrspell/ocrspell-master/out/"

docker cp output/source-docs/ "$name:/home/ocrspell/ocrspell-master/"

files=$(docker exec $name ls "/home/ocrspell/ocrspell-master/source-docs/")

#Original code: Ran everything in one docker instance
####################
#  Begin OCRSpell  #
####################
#Parallelizable!
for file in $files; do
    echo "Running $file"
    docker exec $name bash -c "$srcpath/ocrspell -a -f $srcpath/ocr.freq < $inpath/$file > ocrspell-master/out/$file.output"
    echo "Done"
    echo " "
done
####################
#   End OCRSpell   #
####################

docker cp "$name:/home/ocrspell/ocrspell-master/out" output/OCRSpell/
mv output/OCRSpell/out/*.output output/OCRSpell/

rm -r output/OCRSpell/out/

#docker container stop $name  #Uncomment to stop container instead of leaving it running (may be useful for debugging to wait and manually close it)
sleep 5
