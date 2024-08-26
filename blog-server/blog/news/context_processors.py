
def choosed_categories(request):
    request.session.setdefault('active_categories', [])
    return {'choosed_categories': request.session['active_categories']}

def show_type(request):
    request.session.setdefault('show_type', 'type_4')
    return {'show_type': request.session['show_type']}