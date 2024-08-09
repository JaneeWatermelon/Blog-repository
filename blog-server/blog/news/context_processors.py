
def choosed_categories(request):
    return {'choosed_categories': request.session['active_categories']}