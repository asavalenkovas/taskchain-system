def current_language(request):
    return {
        "lang": request.session.get("lang", "lt")
    }