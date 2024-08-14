
def choosed_categories(request):
    if 'active_categories' in request.session:
        return {'choosed_categories': request.session['active_categories']}
    else:
        return {'choosed_categories': []}

def show_type(request):
    request.session.setdefault('show_type', 'type_4')
    return {'show_type': request.session['show_type']}