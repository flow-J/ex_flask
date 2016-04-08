class notFlask():
    def __init__(self):
        self.routes = {}

    def route(self, route_str):
        def decorator(f):
            self.routes[route_str] = f
            return f

        return decorator

    def serve(self, path):
        view_function = self.routes.get(path)
        if view_function:
            return view_function()
        else:
            raise ValueError('Route "{}" has not been registered'.format(path))


app = notFlask()

def hello():
    return "Hello, World!"

@app.route("/")

print app.serve("/")

hello()
