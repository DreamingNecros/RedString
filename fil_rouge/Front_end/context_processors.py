#ajoute des variables automatiquement dans tous tes templates Django. 
#il faut les rajouter des les setings

def auth_status(request):
    return {
        'is_authenticated_token': bool(request.session.get('access_token')),
        'is_superuser': request.session.get('is_superuser', False),
    }