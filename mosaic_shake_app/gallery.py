from mosaic_shake_app.models import Mosaic
from django.contrib.auth.models import User


def get_mosaic(user_id, img_id):
    #if we have img and user, return the ing
    if img_id:
        return Mosaic.objects.get(id=img_id)
    
    #if we have only a user id, get the user's first img
    if user_id:
        usr = User.objects.get(id=user_id)
        _get_item_or_none( Mosaic.objects.get(user=usr) )
    
    #if we have nothing just get the first image
    return _get_item_or_none( Mosaic.objects.all() )
    

def get_next_mosaic(user_id, img_id):
    #if we have img and user, return the img
    if img_id and user_id:
        usr = User.objects.get(id=user_id)
        return _get_next(Mosaic.objects.filter(user=usr), Mosaic.objects.get(id=img_id))
    
    #if we have img but no user, get the next img
    if img_id:
        return _get_next(Mosaic.objects.all(), Mosaic.objects.get(id=img_id))


def _get_item_or_none(results):
    if len(results) > 0:
        return results[0]
    else:
        return None


#given an array, and an item, get the item in array after item
def _get_next(arr, item):
    if arr[len(arr)-1] == item:  return arr[0]
    
    i = 0
    for it in arr:
        if it == item:
            return arr[i+1]
        i += 1
    return None