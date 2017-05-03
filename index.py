# coding: utf-8

import datetime
import json

import webapp2


IP_LIST = {}

def base_handler(self):
    IP_LIST[self.request.GET.get('location', 'non-Known')] = {
        'ip': self.request.remote_addr,
        'updated_at': (datetime.timedelta(8/24.0) + datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S')  # noqa
    }
    self.response.headers['Content-Type'] = 'application/json'

def base_post_handler(self):
    IP_LIST[self.request.GET.get('location', 'non-Known')]['body'] = self.request.body

class Home(webapp2.RequestHandler):
    def get(self):
        base_handler(self)

        self.response.write(json.dumps({
            self.request.GET.get('location', 'non-Known'): self.request.remote_addr
        }))

    def post(self):
        base_handler(self)
        base_post_handler(self)

        self.response.write(json.dumps({
            self.request.GET.get('location', 'non-Known'): self.request.remote_addr
        }))

class IPList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(IP_LIST))

class Client(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(self.request.headers))

application = webapp2.WSGIApplication([
    ('/', Home),
    ('/ip_list', IPList),
    ('/client', Client),
    # ('/taisys', Taisys),
    # ('/hsinchu', Hsinchu),
    # ('/taipei', Taipei),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()

# $ pip install WebOb
# $ pip install Paste
# $ pip install webapp2
# $ python index.py
