How to use this setup

1. Get an osu replay
2. Use osu!renderer! https://ordr.issou.best/ to generate the replay video. Disable skipping & stuff
3. Go to test.blend, replace the material (for the monitor screen, harumachi) movie with the video
4. run test.py, putting the replay as replay.osr in the same directory
5. run the blender python script, selecting the cube (child of PC)
6. Adjust the animation offset (shift the animation) to match the video
7. Go to video sequencer and import the audio file (drag video, delete the video to leave the audio)

All this can probably be optimised
