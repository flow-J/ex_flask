def simple_decorator(f):
    def wrapper():
        print "ENtering FUnction"
        f()
        print "Exited!"

    return wrapper

@simple_decorator
def hello():
    print "Hello, nerd!"


hello()
