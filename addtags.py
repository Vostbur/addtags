#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import codecs
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TYER, TRCK, APIC, error

TEXT_ENCODING = 'utf8'

# get workdir from first arg or use current dir 
if (len(sys.argv) > 1):
    fpath = sys.argv[1]
else:
    fpath = os.path.abspath(os.path.dirname(sys.argv[0]))

with open('settings.json') as json_data:
    tags = json.load(json_data)

for fn in os.listdir(fpath):

    fname = os.path.join(fpath, fn)
    if fname.lower().endswith('.mp3'):
        
        # get lyrics from txt file
        lyrics = None
        lyrfname = fname[:-3] + 'txt'
        if not os.path.exists(lyrfname):
            print 'ERROR: No lyrics file found:', lyrfname, '...skipping'
            lyrics = ''
        else:
            lyrics = open(lyrfname).read().strip()

        # try to find the right encoding
        for enc in ('utf8','cp1251','cp1252','iso-8859-1','iso-8859-15','latin1'):
            try:
                lyrics = lyrics.decode(enc)
                print enc
                break
            except:
                pass
        
        # delete existing ID3 tags
        mp3 = MP3(fname, ID3=ID3)        
        try:
            mp3.delete()
            mp3.save()
            print 'delete existing ID3 tags in ', fn 
        except:
            pass

        # add ID3 tag if it doesn't exist
        try:
            mp3.add_tags()
        except error:
            pass
            
        mp3.tags.add(TALB(encoding=3, text=tags['album']))
        mp3.tags.add(TPE2(encoding=3, text=tags['artist']))
        mp3.tags.add(TPE1(encoding=3, text=tags['artist']))
        mp3.tags.add(COMM(encoding=3, lang='rus', desc=u'', text=lyrics))
        mp3.tags.add(TCOM(encoding=3, text=tags['artist']))
        mp3.tags.add(TCON(encoding=3, text=tags['genre']))
        mp3.tags.add(TYER(encoding=3, text=tags['year']))
        mp3.tags.add(USLT(encoding=3, lang=u'rus', desc=u'', text=lyrics))
        
        # extract number of issue from filename
        try:
            number = unicode(re.search(r'\d+', fn).group())
        except:
            number = u'0'
        mp3.tags.add(TRCK(encoding=3, text=number))

        if tags['title'] == '':
            title = unicode(os.path.splitext(os.path.split(fn)[-1])[0])
        else:
            title = eval(tags['title'])
        mp3.tags.add(TIT2(encoding=3, text= title))
        
        
        imgfname = os.path.join(fpath, tags['image'])
        try:
            mp3.tags.add(
                APIC(
                    encoding=3, # 3 is for utf-8
                    mime=tags['imgtype'], # image/jpeg or image/png
                    type=3, # 3 is for the cover image
                    desc=tags['cover'],
                    data=open(imgfname, 'rb').read()
                )
            )
        except:
            print 'ERROR: No cover image found:', imgfname, '...skipping'

        mp3.save(v2_version=3) # for supporting Windows Media player

        print 'Added ID3 tags to', fn
print 'Done'