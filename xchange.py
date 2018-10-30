# -*- coding: utf-8 -*-
from tornado.web import MissingArgumentError
from tornado.escape import json_encode
import time
import logging
import tornado.ioloop
import tornado.web as tw
import urllib.request
from xml import sax

logger = logging.getLogger("IGENIOUS.WEB")
PATH_LOG = "./Cx.log"
exchange_rate = {}
class MySaxHandler(sax.ContentHandler, object):
    date_key = ""

    def startElement(self, name, attrs):
        global exchange_rate
        if name == "Cube":
            if "time" in attrs:
                print("Date %s" %attrs['time'])
                self.date_key = attrs['time']
                if not self.date_key in exchange_rate:
                    exchange_rate[self.date_key] = {}
            if "rate" in attrs:
                print("Currency: %s, rate: %s" % (attrs['currency'], attrs['rate']))
                exchange_rate[self.date_key][attrs['currency']] = [attrs['rate']]

class MainHandler(tw.RequestHandler):

    def return_error_page(self, title, mesg):
       self.write("<!doctype html> <html> <head><title>%s</title></head> <body><main><h1>%s</h1></main>" % (title, mesg))

    def get(self):
        global exchange_rate
        try:
            self.amount = float(self.get_argument('amount'))
        except tw.MissingArgumentError:
            logger.error('missing amount')
            raise tw.HTTPError(400)
        if float(self.amount) < 0:
            logger.error('negative amount')
            raise tw.HTTPError(400)
        try:
            self.src_currency = self.get_argument('src_currency')
        except tw.MissingArgumentError:
            logger.error('missing src_currency')
            raise tw.HTTPError(400)
            #self.return_error_page("Parameter missing", "Missing parameter 'src_currency'")
        try:
            self.dest_currency = self.get_argument('dest_currency')
        except tw.MissingArgumentError:
            logger.error('missing dest_currency')
            raise tw.HTTPError(400)
            #self.return_error_page("Parameter missing", "Missing parameter 'dest_currency'")
        try:
            self.reference_date = self.get_argument('reference_date')
        except tw.MissingArgumentError:
            logger.error('missing reference_date')
            raise tw.HTTPError(400)
            #self.return_error_page("Parameter missing", "Missing parameter 'reference_date'")
        if not self.reference_date in exchange_rate.keys():
            logger.error('reference date not found in exchange rate file')
            raise tw.HTTPError(400)
        if not self.src_currency in exchange_rate[self.reference_date].keys() and self.src_currency != "EUR":
            logger.error('source currency not found in exchange rate file')
            raise tw.HTTPError(400)
        if not self.dest_currency in exchange_rate[self.reference_date].keys() and self.dest_currency != "EUR":
            logger.error('destination currency not found in exchange rate file')
            raise tw.HTTPError(400)

        if self.src_currency == "EUR":
            src = 1
        else:
            src = float(exchange_rate[self.reference_date][self.src_currency][0])
        if self.dest_currency == "EUR":
            dst = 1
        else:
            dst = float(exchange_rate[self.reference_date][self.dest_currency][0])
        euros = self.amount / src
        logger.info("euros: %f" % euros)
        final_convert = euros * dst
        logger.info("final_convert %f" % final_convert)
        answer = {"amount" : final_convert, "currency" : self.dest_currency}
        self.set_header('Content-Type', 'application/json')
        self.write(json_encode(answer))

def setLogger(level):
    logger.setLevel(level)
    logger.propagate = False
    ch = logging.handlers.WatchedFileHandler(PATH_LOG)
    ch2 = logging.StreamHandler()
    ch.setLevel(level)
    ch2.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    ch.setFormatter(formatter)
    ch2.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(ch2)

def make_app():
    return tw.Application([
        (r"/convert", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    try:
        urllib.request.urlretrieve("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml", "xchange.xml")
    except Exception:
        logger.error("Can't retrieve currency change xml file. Using the stored one")
        pass
    setLogger("INFO")
    sax.parse('xchange.xml', MySaxHandler())

    tornado.ioloop.IOLoop.current().start()
