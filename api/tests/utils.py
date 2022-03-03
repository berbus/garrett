import string
import random

from django.contrib.auth.models import User
from django.db.utils import IntegrityError


username = 'a'
admin_username = 'b'
password = 'a'

try:
    _regular_user = User.objects.create_user(username=username, password=password)
    _regular_user.save()
except IntegrityError:
    _regular_user = User.objects.get(username=username)

try:
    _admin_user = User.objects.create_user(username=admin_username, password=password, is_staff=True)
    _admin_user.save()
except IntegrityError:
    _admin_user = User.objects.get(username=admin_username)


def login_client(client, admin=False):
    if admin:
        client.force_authenticate(user=_admin_user)
    else:
        client.force_authenticate(user=_regular_user)


def get_random_name():
    return ''.join([random.choice(string.ascii_letters) for i in range(0, 10)])
