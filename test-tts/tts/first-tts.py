# pip install coqui-tts
# pip install espeakng

from espeakng import ESpeakNG
esng = ESpeakNG()
esng.say('Hello World!')

#! espeak-ng "This is a test!" >´3.wav




# https://github.com/espeak-ng/espeak-ng/blob/master/docs/building.md
# Building eSpeak NG
# a copy of Visual C++ Redistributable for Visual Studio 2015 or later, such as the Community Edition;
# the Windows 8.1 SDK;
# the WiX installer plugin; : https://www.firegiant.com/wixtoolset/
# the pcaudiolib project checked out to src (as src/pcaudiolib).
# cd C:\Development\workspace\python\espeak-ng\src\windows
# msbuild espeak-ng.sln
# https://marketplace.visualstudio.com/items?itemName=FireGiant.FireGiantHeatWaveDev17
