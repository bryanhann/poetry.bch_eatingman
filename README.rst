To assemble episodes of 'The Solitary Eater' by the following steps.

Let
    [$EPISODE]  = [S1E02]
    [$FILE]     = [./episodes/$EPISODE.txt]
    [$PREFIX]   = [https://proxy-01.eightytwovideoprogood.xyz/cdn01/hls/61566024dd75dfb79e39833ai]
    [$NNNN]     = [0000]
    [$PNG]      = [7492933fc80e3a3469ce592303348e30.png]
    [$URL]      = [${PREFIX}/${PNG}]
    [$MP4]      = [${EPISODE}_${NNNN}.mp4

Here
    (1) [$EPISODE] is the standard name of an episode.
    (2) [$FILE] is an episode file which has embeded within it an ordered
        list of URLS to PNG files needed to assemble the episod.e
    (3) [$PREFIX] is a common prefix to each URL in the list
    (4) [$NNNN] is an ordinal denoting which URL in the list
        is being considered. (Ordinals are 4 digit, zero based).
    (5) [$PNG] is the name of the PNG file corresponding to the ordinal
    (6) [$MP4] is the [$PNG] file renamed.

NOTWITHSTANDING THIS:
    The prefix alternates between the following:
        [https://proxy-1.{stuff}]
        [https://proxy-2.{stuff}]
    but this does not affect the assembly order.

We generate a script that will parse all episode files, wget all
it's PNG files, and rename them as MP4 files in a way that indicates
their order of assembly.

What is left to implement are the steps:

EXTRACT MP4
-----------
    mkvmerge \
    --ui-language en \
    --output ^"$$OUTPUT-1$$.mp4^" \
    --language 0:und \
    --compression 0:none \
    --language 1:und \
    --compression 1:none ^"^(^" ^"$$INPUT-1$$.mp4^" ^"^)^" \
    --track-order 0:0,0:1


CONVERT TO TS
-------------
    ffmpeg \
    -i $$INPUT-2$$.mp4 \
    -c copy \
    -bsf:v h264_mp4toannexb \
    -f mpegts $$OUTPUT-2$$.ts

MERGE TO MP4
------------
    ffmpeg \
    -i "concat:$$001$$.ts|$$002$$.ts|$$003$$.ts" \
    -c copy $$DONE-1$$.mp4
