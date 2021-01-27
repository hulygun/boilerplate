import pkgutil

def load_services(app):
    """load services and include theirs routes in the app"""
    modules = list(pkgutil.iter_modules(__path__))
    if modules:
        importer = modules[0][0]
        for submodule in modules:
            s = importer.find_module(submodule.name).load_module(submodule.name)
            app.include_router(s.router, prefix='/{}'.format(submodule.name))
