#!/bin/bash
mkdir MorseKit.app
mkdir MorseKit.app/Contents
mkdir MorseKit.app/Contents/MacOS
cp ../*.py MorseKit.app/Contents/MacOS/
cp ../README MorseKit.app/Contents/MacOS/
cp ../COPYING MorseKit.app/Contents/MacOS/

# build cwtext
pushd .
cd ../cwtext-0.96
make
popd

cp -R ../cwtext-0.96 MorseKit.app/Contents/MacOS/
cp -R ../sox-14.3.1 MorseKit.app/Contents/MacOS/
cp MorseKit MorseKit.app/Contents/MacOS/
