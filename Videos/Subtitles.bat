cd ..\videos
ffmpeg.exe \
-i video.mp4 \
-i ..\scripts\metadata.txt \
-i ..\subtitles\EN\EN.ass \
-i ..\subtitles\TW\TW.ass \
-i ..\subtitles\CN\CN.ass \
-i ..\subtitles\JP\JP.ass \
-c copy -map_metadata 1 -map 0:v -map 0:a \
-map 2 -c:s mov_text -metadata:s:s:0 language=eng \
-map 3 -c:s mov_text -metadata:s:s:1 language=zht \
-map 4 -c:s mov_text -metadata:s:s:2 language=zhs \
-map 5 -c:s mov_text -metadata:s:s:3 language=jpn \
-y video-subtitle.mp4
