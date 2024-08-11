
# Тип активной вкладки новостей в профиле
def get_type(request):
    if 'type' in request.session:
        return {'type': request.session['type']}
    else:
        return {'type': 'like'}