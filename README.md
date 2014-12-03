CaptureBate
==========

CaptureBate lets you follow and archive your favorite models shows on chaturbate.com

Requirements
==========
(Debian 7, minimum)

[RTMPDump(ksv)](https://github.com/BurntSushi/rtmpdump-ksv) used to capture the streams.

[BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4/4.3.2) the screen-scraping library.

[ffmpeg](https://www.ffmpeg.org/download.html) compiled with support for `libmp3lame` & `libspeex` audio for converting the output files.

Setup
===========

Install requirements `sudo pip install -r requirements.txt`

Get a [chaturbate account](https://chaturbate.com/accounts/register/), once you're signed up put your credentials in the `config.conf` file, next you need to get your hashed password for RTMPDump. To get your hash you need to be signed in, then go any models page who is currently online, right click to view page source and search for `pbkdf2_sha256$` the full hash will look something like `pbkdf2_sha256$12000$QwwcaxjaV3Ik$cZHXVde52w+Fl6In54Ay5ZeMQMAFueQgwnnLbkTWT5g\u003D` copy your hash into a text editor and escape each `$` with a `\` then replace `u003D` with `=` once you've formatted your hash it should look like `pbkdf2_sha256\$12000\$QwwcaxjaV3Ik\$cZHXVde52w+Fl6In54Ay5ZeMQMAFueQgwnnLbkTWT5g\=` you can then paste it into the rtmpdump line [modellists.py#L79](https://github.com/ohhdemgirls/CaptureBate/blob/master/modellists.py#L79) be sure to also replace the username on the same line just before your hash.

Now set your output directory in `config.conf` *optional, will default to `CaptureBate/Captured/` Be mindful when capturing many streams at once to have plenty of space on disk and the bandwidth available or you'll endup dropping a lot of frames and the files will be useless.

Before you can start capturing streams you first need to [follow](https://i.imgur.com/o9QyAVC.png) the models you want on site and then paste their usernames into the `wishlist.txt` file, once you have done this you're ready to start `main.py`

Running & Output
===========

To start capturing streams you need to run `python main.py` I reccomend you do this in [screen](https://www.gnu.org/software/screen/) as there is no output and it can just be left running in the background. To see what's going on run `tail -f output.log` 

Standard output should look something this when recording streams ..

    17/11/2014 09:37:13 PM INFO:Connecting to https://chaturbate.com/auth/login/
    17/11/2014 09:37:13 PM INFO:Starting new HTTPS connection (1): chaturbate.com
    17/11/2014 09:37:15 PM INFO:0 Models in the list before checking: []
    17/11/2014 09:37:15 PM INFO:Redirecting to https://chaturbate.com/followed-cams/
    17/11/2014 09:37:16 PM INFO:[Models_list] 2 models are online: [u'hottminx', u'adryeenmely']
    17/11/2014 09:37:16 PM INFO:[Compare_lists] Checking model list:
    17/11/2014 09:37:16 PM INFO:[Compare_lists] hottminx is still being recorded
    17/11/2014 09:37:16 PM INFO:[Compare_lists] adryeenmely is still being recorded
    17/11/2014 09:37:16 PM INFO:[Loop]List of new models for adding: []
    17/11/2014 09:37:16 PM INFO:[Select_models] Which models are approved?
    17/11/2014 09:37:16 PM WARNING:[Select_models]  No models for approving
    17/11/2014 09:37:16 PM INFO:[Loop]Model list after check looks like: 0 models:
     [] 
     and models currently being recorded are:
     ['adryeenmely', 'hottminx']
    17/11/2014 09:37:16 PM INFO:[Sleep] Waiting for next check (45 seconds)

Encoding
===========

Once you've captured some streams you're going to need to convert the audio to have them play nice in vlc, etc. This is where ffmpeg comes in, there is no need to convert the video so this doesn't take too long. To convert individual files do `ffmpeg -i input.flv -vcodec copy -acodec libmp3lame output.mp4` this will convert the speex audio to mp3 and change the container to mp4 (stream is h264)

If you want to batch convert your captured streams run `find ./ -name '*.flv' -execdir mkdir converted_bates \;; for file in *.flv; do ffmpeg -i "$file" -vcodec copy -acodec libmp3lame "converted_bates/${file%.flv}.mp4"; done` from your `CaptureBate/Captured/` directory.

If you don't want to do any conversion you can install the [speex audio codec](http://speex.org/downloads/) which is a huge pain in the ass to get working correctly under linux/vlc.

......tbc
