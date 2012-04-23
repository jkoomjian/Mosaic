import flickrapi
from django.conf import settings
from mosaic_shake_app.models import Image
import os

class Downloader():
    def __init__(self, photoset):
        self.flickr_api_key="d1a1dd6914f1edf7d7716ed165f9645f"
        self.flickr_shared_secret="d187cc9d0b5bf422"
        self.photoset = photoset
        self.count = 0
        self.page = 0
    
    def download(self):
        saved_imgs = {} #this is a hack - for some reason the api is returning duplicate results
        flickr = flickrapi.FlickrAPI(self.flickr_api_key, self.flickr_shared_secret)
        
        while self.count < self.photoset.num_photos_to_get:
        
            # get a page of search results
            print self.photoset.search_query + " " + self.photoset.latitude + " " + self.photoset.longitude + " " + str(self.count) + " photos page" + str(self.page)
            photos = flickr.photos_search(
                                        text=self.photoset.search_query,
#                                        text='seattle',
                                        lat=self.photoset.latitude, 
#                                        lat='47.629508', 
                                        lon=self.photoset.longitude, 
#                                        lon='-122.359972', 
                                        radius='1', 
                                        content_type='1', 
                                        per_page='10', 
                                        page=self.page
                                    )
            for photo in photos[0]:
#                print str(photo.attrib['title'])
                
                #make sure this photo is the right size
                photoSizes = flickr.photos_getSizes(photo_id=photo.attrib['id'])
                thumb = large = None
                for photoSize in photoSizes[0]:
                    if photoSize.attrib['label'] == 'Square': thumb = photoSize
                    if photoSize.attrib['label'] == 'Large': large = photoSize
                    if large is not None and                                                                \
                        large.attrib['width'] == "1024" and                                                 \
                        (682 <= int(large.attrib['height']) and int(large.attrib['height']) <= 700) and     \
                        not saved_imgs.has_key( photo.attrib['id'] ):
                        #we have a usable image!
                        print photo.attrib['id'] + ' ' + photoSize.attrib['label'] + ' ' + photoSize.attrib['width'] + 'x' + photoSize.attrib['height'] + ' ' + photoSize.attrib['source']
                        try:
                            #save image to db
                            self.saveToDb(photo, thumb, large)
                            #save the image + thumb
                            self.downloadImg(photo, thumb, large)
                            saved_imgs[ photo.attrib['id'] ] = "1"
                            self.count += 1
                        except:
                            pass
                        
            #check if we are out of results
            if len(photos[0]) < 10: break;
            self.page+=1

    def saveToDb(self, photo, thumb, large):
#        print "saving: " + photo.attrib['id'] + " title: " + unicode(photo.attrib['title'], 'utf-8', errors='ignore')
        img = Image.objects.create(
                                   flickr_id = photo.attrib['id'],
                                   flickr_title = unicode(photo.attrib['title'], 'utf-8', errors='ignore'),
                                   flickr_author = unicode(photo.attrib['owner'], 'utf-8', errors='ignore'),
                                   flickr_html_url = large.attrib['url']
                                   )
        self.photoset.images.add(img)

    
    def downloadImg(self, photo, thumb, large):
        cmd = 'wget -O {save_dir}/{flickr_id}_{size}.jpg {flickr_source}'.format(save_dir=settings.PS_IMG_DIR, flickr_id=photo.attrib['id'], size='thumb', flickr_source=thumb.attrib['source'])
        print cmd
        os.system(cmd)
        cmd = 'wget -O {save_dir}/{flickr_id}_{size}.jpg {flickr_source}'.format(save_dir=settings.PS_IMG_DIR, flickr_id=photo.attrib['id'], size='large', flickr_source=large.attrib['source'])
        print cmd
        os.system(cmd)
        pass
    
#Testing
#Downloader(None).download()
#Downloader(None).downloadImg(None, None, None)