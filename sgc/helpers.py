from django.shortcuts import redirect


def redirect_with_next(request, reverse):
    params = request.GET.copy()
    if 'next' in params and params['next'] == '/':
        response = redirect('home')
    else:
        response = redirect(reverse)
    response['Location'] += '?' + params.urlencode()
    return response
