from django.conf import settings
import random
import os

class Mosaicer():

    def __init__(self, mosaic):
        self.mosaic = mosaic
        #Constants
        self.full_img_width = 1024
        self.full_img_height = 682
        #Vars
        self.curr_column = self.curr_row = self.img_count = 0
        
    def increment_position(self):
        self.img_count += 1
        self.curr_column += 1
        # are we past the end of the image?
        if (self.curr_column * int(self.mosaic.tile_width)) >= self.full_img_width:
            self.curr_column = 0
            self.curr_row += 1
        
        
    ## Create image segments
    def slice_imgs(self, working_dir):
        ##Get img names
        imgs = []
  
        #Add the images in our photoset to the imgs array
        for ps_img in self.mosaic.photoset.images.all():
            imgs.append(ps_img.flickr_id + "_large.jpg")
        print 'imgs: ' + str(imgs)
  
        ##Create cropped version
        prev_img = ''
        while self.img_count < ((self.full_img_width / int(self.mosaic.tile_width)) * (self.full_img_height / int(self.mosaic.tile_height))):
            ## do it this way so we get a proper random sampling of the images
            curr_img = imgs[ random.randint(0, len(imgs)-1) ]
    
            # make sure we dont get the same image twice in a row
            if curr_img != prev_img:
                prev_img = curr_img
                
                cmd_args = {'ps_dir':settings.PS_IMG_DIR, 
                            'curr_img':curr_img,
                            'tile_width':str(self.mosaic.tile_width), 
                            'tile_height':str(self.mosaic.tile_height), 
                            'offset_width':str(self.curr_column * int(self.mosaic.tile_width)), 
                            'offset_height':str(self.curr_row * int(self.mosaic.tile_height)),
                            'working_dir':working_dir, 
                            'img_count':str(self.img_count).rjust(6, "0")
                            }
                cmd = "convert {ps_dir}/{curr_img} -crop '{tile_width}x{tile_height}!+{offset_width}+{offset_height}' {working_dir}/tile_{img_count}.png".format(**cmd_args)
                print cmd
                os.system(cmd)
                self.increment_position()
                
    def run(self):
        ##Create working dir
        working_dir = settings.WORKING_DIR + "/" + str(random.randint(0,1000))
        cmd = "mkdir {working_dir}".format(working_dir=working_dir)
        print cmd
        os.system(cmd)

        self.slice_imgs(working_dir)
  
        ##Create montage
        cmd_args = {'tile_width':str(self.mosaic.tile_width),
                    'tile_height':str(self.mosaic.tile_height),
                    'tiles_across':str(self.full_img_width / int(self.mosaic.tile_width)),
                    'tiles_high':str(self.full_img_height / int(self.mosaic.tile_height)),
                    'working_dir':working_dir,
                    'mosaic_dir':settings.MOSAIC_IMG_DIR,
                    'mosaic_id':str(self.mosaic.id)
                    }
        cmd = "montage -border 0 -geometry '{tile_width}x{tile_height}' -tile {tiles_across}x{tiles_high} \"{working_dir}/tile_*\" {mosaic_dir}/{mosaic_id}.png".format(**cmd_args)
        print cmd
        os.system(cmd)
        
        #Create thumbnail of montage
        cmd = "convert -resize 75x75 {mosaic_dir}/{mosaic_id}.png {mosaic_dir}/{mosaic_id}_thumb.jpg".format(**cmd_args)
        print cmd
        os.system(cmd)
        
        ##Delete working dir
        cmd = "rm -r {working_dir}".format(working_dir=working_dir)
        print(cmd)
        os.system(cmd)