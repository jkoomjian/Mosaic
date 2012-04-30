from mosaic_shake_app.models import Photoset, Mosaic, Image
from mosaic_shake_app.forms import PhotosetForm, MosaicForm
from django.shortcuts import render_to_response
from mosaic_shake_app.downloader import Downloader
from mosaic_shake_app.mosaicer import Mosaicer
from mosaic_shake_app.gallery import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.forms.util import ErrorList
from django.core import serializers
from django.http import HttpResponse


def gallery(request, **args):
    msc_id = user_id = None
    if args.has_key('msc_id'): msc_id = args['msc_id']
    if args.has_key('user_id'): user_id = args['user_id']
    msc = get_mosaic(user_id, msc_id)
    return render_to_response('gallery.html', {'msc':msc, 'settings':settings, 'user_id': user_id}, context_instance=RequestContext(request))

def gallery_next_json(request, **args):
    msc_id = user_id = None
    if args.has_key('msc_id'): msc_id = args['msc_id']
    if args.has_key('user_id'): user_id = args['user_id']
    msc = get_next_mosaic(user_id, msc_id)
    mscA = [msc]  #serializer requires an array
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(mscA, ensure_ascii=False)
    return HttpResponse(data)

@login_required
def home(request):
    args = {
            'all_ps': Photoset.objects.filter(user=request.user),
            'all_mosaic': Mosaic.objects.filter(user=request.user),
            'settings': settings
            }
    return render_to_response('home.html', args, context_instance=RequestContext(request))

@login_required
def new_photoset(request):
    form = PhotosetForm(request.POST) if request.method == 'POST' else PhotosetForm()
    if request.method == 'POST' and form.is_valid():
        ## Create the new photoset
        ps = Photoset.objects.create(
                                user=request.user,
                                name=form.cleaned_data["name"],
                                num_photos_to_get=form.cleaned_data["num_photos_to_get"],
                                search_query=form.cleaned_data["search_query"],
                                latitude=form.cleaned_data["latitude"],
                                longitude=form.cleaned_data["longitude"]
                                )
        #Now begin the download
        Downloader(ps).download()
        
        return HttpResponseRedirect('/m/edit_photoset/{id}?begin=true'.format(id=ps.id))
    
    return render_to_response('new_photoset.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def edit_photoset(request, ps_id):
    #get out Photoset
    ps = Photoset.objects.get(id=ps_id, user=request.user)
    all_ps = Photoset.objects.filter(user=request.user)
    print ps.id
    return render_to_response('edit_photoset.html', {'curr_ps': ps, 'all_ps':all_ps, 'settings':settings}, context_instance=RequestContext(request))

@login_required
def new_mosaic(request):
    form = MosaicForm(request.POST) if request.method == 'POST' else MosaicForm()
    if request.method == 'POST' and form.is_valid():

        #make sure the selected photoset has images
        print 'imgs: ' + str( len(form.cleaned_data["photoset"].images.all()) )
        if len(form.cleaned_data["photoset"].images.all()) == 0:
            errors = form._errors.setdefault("photoset", ErrorList())
            errors.append(u"Your selected photoset doesn't contain any images!")
            return render_to_response('new_mosaic.html', {'form': form}, context_instance=RequestContext(request))
        
        ## Create the new photoset
        msc = Mosaic.objects.create(
                                user=request.user,
                                name=form.cleaned_data["name"],
                                photoset=form.cleaned_data["photoset"],
                                tile_width=form.cleaned_data["tile_width"],
                                tile_height=form.cleaned_data["tile_height"]
                                )
        #Create the mosaic
        Mosaicer(msc).run()
        
        return HttpResponseRedirect('/m/gallery/{uid}/{id}'.format(uid=request.user.id,id=msc.id))
    return render_to_response('new_mosaic.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def delete_img_json(request):
    #using GET to avoid dealing with csrf for now
    img_id = request.GET.get('img_id')
    ps_id = request.GET.get('ps_id')
    ps = Photoset.objects.get(id=ps_id)
    img = Image.objects.get(id=img_id)
    print 'delete '+ img_id
    ## remove from photoset
    ps.images.remove(img)
    return HttpResponse("")
    
@login_required
def copy_img_json(request):
    dest_ps = Photoset.objects.get(id=request.GET.get('dest_ps_id'))
    img = Image.objects.get(id=request.GET.get('img_id'))
    dest_ps.images.add(img)
    return HttpResponse("")

@login_required
def recreate_msc(request, msc_id):
    src_msc= Mosaic.objects.get(id=msc_id)
    ## Create the new photoset in db
    msc = Mosaic.objects.create(
                            user=request.user,
                            name=src_msc.name,
                            photoset=src_msc.photoset,
                            tile_width=src_msc.tile_width,
                            tile_height=src_msc.tile_height
                            )
    #Create the mosaic file
    Mosaicer(msc).run()
    return HttpResponseRedirect('/m/gallery/{uid}/{id}'.format(uid=request.user.id,id=msc.id))
