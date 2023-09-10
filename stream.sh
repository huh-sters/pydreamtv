#!/bin/bash
# ffmpeg -f x11grab -framerate 15 -video_size 1280x720 -i :0.0 -f v4l2 /dev/video0
# ffmpeg -y -i IPTV_URL_minus_channel/$1.ts -vcodec copy -acodec copy -map 0:v -map 0:a -t $2 $dt-CH$1.ts &> /dev/null
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts -c:v copy -c:a copy -framerate 15 -video_size 1280x720 -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts -vcodec copy -acodec copy -map 0:v -video_size 1280x720 -f v4l2 /dev/video0
# ffmpeg -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts -vf "scale=640:360" -f v4l2 /dev/video0
# ffmpeg -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts -s 640x360 -aspect 640:360 -r 15 -b 360k -bt 416k -vcodec libx264 -pass 1 -vpre fastfirstpass -an "$1"-out.mp4
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts -s 640x360 -aspect 640:360 -r 15 -b 360k -bt 416k -vcodec libx264 -acodec libfaac -ac 2 -ar 44100 -ab 64k -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -vf "scale=iw/2:ih/2" -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -f v4l2 /dev/video0
# vlc -vvv http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts --sout="#transcode{vcodec=h264,vb=800,scale=0.5}:v4l2:///dev/video0"
# vlc -vvv http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts --sout="v4l2:///dev/video0"
# vlc -vvv http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts --sout="#transcode{vcode=x264}:v4l2:///dev/video0"
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -vf format=yuv420p -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -pix_fmt yuv420p -c:v libx264 -preset faster -threads 1 -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -vf format=yuv420p -vcodec h264 -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -vf format=yuv420p -vcodec h264 -c:a copy -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -vf format=yuv420p -vcodec h264 -crf 27 -preset ultrafast -c:a copy -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -c:v libx264 -vf "scale=iw/2:ih/2" -c:a copy -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -vf format=yuyv422 -f v4l2 /dev/video0
# ffmpeg -y -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TOQL7iLZhrECuiPpjNZJIZQ/ts -vf format=yuv420p -vcodec libx264 -preset ultrafast -f v4l2 /dev/video0
ffmpeg -i http://neczmabfa.to:80/play/Mb_As84PELDIm3i5VJ_8nJiRif9MkF8lvTpXiBjQ5TM5sbhQXiNr8gHdV0FOxn6-/ts -vf format=yuv420p -c:v libx264 -pix_fmt yuv420p -c:a copy -f v4l2 /dev/video0
