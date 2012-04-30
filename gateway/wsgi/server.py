def start(port):
    import os
    from tornado.web import Application
    from tornado.ioloop import IOLoop
    import handlers
    Application([
        ('/', handlers.Index),
        ('/status', handlers.StatusHandler),
        ('/action', handlers.ActionHandler),
        ('/cmd', handlers.Commander),
    ], **{
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    }).listen(port)
    IOLoop.instance().start()
