import vpw
from vpw.vpr_api import vpr_create_person

__author__ = 'huyvq'


# Declare Signs
def user_activated_callback(sender, user, request, **kwargs):
    try:
        author = vpw.models.Author.objects.get(user=user)
    except vpw.models.Author.DoesNotExist:
        # create person on vpr
        params = dict()
        params["fullname"] = '%s %s' % (user.first_name, user.last_name)
        params["user_id"] = user.username
        params["first_name"] = user.first_name
        params["last_name"] = user.last_name
        params["email"] = user.email

        new_person = vpr_create_person(**params)

        if 'id' in new_person:
            if new_person["id"] > 0:
                author = vpw.models.Author(user=user)
                author.author_id = new_person['id']
                author.save()
