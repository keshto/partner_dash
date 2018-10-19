def save_profile(backend, user, response, *args, **kwargs):
  if backend.name == 'slack':
    user.avatar512 = response['user']['image_512']
    user.save()