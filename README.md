# Docker NGINX VOD Module

[![Build Status](https://travis-ci.org/alfg/docker-nginx-vod-module.svg?branch=master)](https://travis-ci.org/alfg/docker-nginx-vod-module)
[![Docker Automated build](https://img.shields.io/docker/automated/alfg/nginx-vod-module.svg)](https://hub.docker.com/r/alfg/nginx-vod-module/builds/)

A Dockerized NGINX build with the `nginx-vod-module` and `ngx_aws_auth` for serving VOD content to DASH, HLS, and MSS.

`nginx-vod-module` is configured in remote-mode with `ngx_aws_auth` to securely serve content stored in a private S3 bucket.


# Setup
#### Requirements
* Docker
* AWS Account for S3
* Python 2.7

#### Setup AWS Credentials
* Create an AWS account and S3 Bucket (private)
* Create a user via IAM with Programmatic Access and read access to the S3 Bucket
* Run `python scripts/generate_signing_key.py -k <aws secret access key> -r <aws region>` to generate a signing_key and key_scope.

#### Setup Server
* Configure `docker-compose.yml` with the following environment variables:
```
- AWS_ACCESS_KEY=<aws access key>
- AWS_S3_BUCKET=<aws s3 bucket>
- AWS_SIGNING_KEY=<aws signing key from script>
- AWS_KEY_SCOPE=<aws key scope from script>
```

* Start server:
```
docker-compose up
```

* Test
Upload an MP4 to your S3 bucket and load the manifest to test different outputs:

* DASH - http://localhost:8080/dash/video.mp4/manifest.mpd
* HLS - http://localhost:8080/hls/video.mp4/master.m3u8
* MSS - http://localhost:8080/mss/video.mp4/manifest

#### Live
* DASH - http://localhost:8080/live/dash/manifest.mpd
* HLS - http://localhost:8080/live/hls/master.m3u8
* MSS - http://localhost:8080/live/mss/manifest

```
λ curl -I http://localhost:8080/dash/video.mp4/manifest.mpd
HTTP/1.1 200 OK
```

Use one of the players below to test playback.

#### Setup CDN
TODO

# Demo

| Type | Source | URL |
| ---- | --- | --- |
| DASH | Origin | [Shaka Player](https://shaka-player-demo.appspot.com/demo/#asset=https://vod.herokuapp.com/dash/videos/tears-of-steel/tears-of-steel_,h264_baseline_360p_600.mp4,h264_main_480p_1000.mp4,h264_main_720p_3000.mp4,h264_main_1080p_6000.mp4,audio.mp4,.urlset/manifest.mpd;lang=en-US) |
| HLS  | Origin | [HLS.js PLayer](https://video-dev.github.io/hls.js/demo/?src=https%3A%2F%2Fvod.herokuapp.com%2Fhls%2Fvideos%2Ftears-of-steel%2Ftears-of-steel_%2Ch264_baseline_360p_600.mp4%2Ch264_main_480p_1000.mp4%2Ch264_main_720p_3000.mp4%2Ch264_main_1080p_6000.mp4%2Caudio.mp4%2C.urlset%2Fmaster.m3u8&enableStreaming=true&autoRecoverError=true&enableWorker=true&dumpfMP4=false&levelCapping=-1) |
| MSS  | Origin | [HASPlayer.js](http://orange-opensource.github.io/hasplayer.js/1.13.0/samples/DemoPlayer/index.html?url=https://vod.herokuapp.com/mss/videos/tears-of-steel/tears-of-steel_,h264_baseline_360p_600.mp4,h264_main_480p_1000.mp4,h264_main_720p_3000.mp4,h264_main_1080p_6000.mp4,audio.mp4,.urlset/manifest) |
| DASH | CDN | [Shaka Player](https://shaka-player-demo.appspot.com/demo/#asset=https://d22kgg8psbxs19.cloudfront.net/dash/videos/tears-of-steel/tears-of-steel_,h264_baseline_360p_600.mp4,h264_main_480p_1000.mp4,h264_main_720p_3000.mp4,h264_main_1080p_6000.mp4,audio.mp4,.urlset/manifest.mpd;lang=en-US) |
| HLS  | CDN | [HLS.js Player](https://video-dev.github.io/hls.js/demo/?src=https%3A%2F%2Fd22kgg8psbxs19.cloudfront.net%2Fhls%2Fvideos%2Ftears-of-steel%2Ftears-of-steel_%2Ch264_baseline_360p_600.mp4%2Ch264_main_480p_1000.mp4%2Ch264_main_720p_3000.mp4%2Ch264_main_1080p_6000.mp4%2Caudio.mp4%2C.urlset%2Fmaster.m3u8&enableStreaming=true&autoRecoverError=true&enableWorker=true&dumpfMP4=false&levelCapping=-1) |
| MSS  | CDN | [HASPlayer.js](http://orange-opensource.github.io/hasplayer.js/1.13.0/samples/DemoPlayer/index.html?url=https://d22kgg8psbxs19.cloudfront.net/mss/videos/tears-of-steel/tears-of-steel_,h264_baseline_360p_600.mp4,h264_main_480p_1000.mp4,h264_main_720p_3000.mp4,h264_main_1080p_6000.mp4,audio.mp4,.urlset/manifest) |


# Test Players
HTML5 Players for testing.

* https://shaka-player-demo.appspot.com
* http://video-dev.github.io/hls.js/demo/
* http://orange-opensource.github.io/hasplayer.js/ 


# TODO
* DRM Example
* Test with S3-compatible APIs (Digital Ocean Spaces)


# References
* https://www.nginx.com
* https://github.com/kaltura/nginx-vod-module
* https://github.com/anomalizer/ngx_aws_auth
