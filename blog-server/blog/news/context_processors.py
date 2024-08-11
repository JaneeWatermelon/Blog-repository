
def choosed_categories(request):
    if 'active_categories' in request.session:
        return {'choosed_categories': request.session['active_categories']}
    else:
        return {'choosed_categories': []}