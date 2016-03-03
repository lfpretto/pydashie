import os
import logging
from flask import Flask, render_template, Response, send_from_directory, request, current_app
import json
import datetime
from connection_streams import ConnectionStreams

xyzzy = ConnectionStreams()
app = Flask(__name__)
logging.basicConfig()
log = logging.getLogger(__name__)
dcSamplers = dict()


def addSampler(strID, objSampler, bRestart=False):
    #from dashie_sampler import DashieSampler
    print objSampler
    if objSampler:
        if strID in dcSamplers:
            if bRestart:
                objCurrentSampler = dcSamplers[strID]
                del objCurrentSampler
            else:
                return False
        dcSamplers[strID] = objSampler
        return True
    return False, 'not Sampler'

def startSampler(objConnections, strID, strType, dcConfig=dict(), bRestart=False):
    import importlib
    objModule = importlib.import_module("dashie_sampler")
    print objModule
    objSampler = getattr(objModule, strType + "Sampler")
    print objSampler
    if objSampler:
        nInterval = dcConfig.get("interval", 5)
        nSamples = dcConfig.get("samples", 2)
        print 'Adding', addSampler(strID, objSampler(strID, objConnections, nInterval, dcConfig, nSamples))
    return True

@app.route("/")
def main():
    return render_template('test.html', title='pyDashie')
    
@app.route("/dashboard/<dashlayout>/")
def custom_layout(dashlayout):
    return render_template('%s.html'%dashlayout, title='pyDashie')

@app.route("/assets/application.js")
def javascripts():
    if not hasattr(current_app, 'javascripts'):
        import coffeescript
        scripts = [
            'assets/javascripts/coffee-script.js',
            'assets/javascripts/jquery.js',
            'assets/javascripts/es5-shim.js',
            'assets/javascripts/d3.v2.min.js',
            'assets/javascripts/batman.js',
            'assets/javascripts/batman.jquery.js',
            'assets/javascripts/jquery.gridster.js',
            'assets/javascripts/jquery.leanModal.min.js',
            'assets/javascripts/dashing.js',
            #'assets/javascripts/dashing.coffee',
            #'assets/javascripts/dashing.gridster.coffee',
            'assets/javascripts/jquery.knob.js',
            'assets/javascripts/rickshaw.min.js',
            'assets/javascripts/application-compiled.js',
            #'assets/javascripts/application.coffee',
            #'assets/javascripts/app.js',

            'widgets/number/number.js',
            'widgets/meter/meter.js',

            #'widgets/clock/clock.coffee',
            #'widgets/number/number.coffee',
            #'widgets/meter/meter.coffee',
            #'widgets/comments/comments.coffee',
        ]
        nizzle = True
        if not nizzle:
            scripts = ['assets/javascripts/application.js']

        output = []
        for path in scripts:
            output.append('// JS: %s\n' % path)
            if '.coffee' in path:
                log.info('Compiling Coffee for %s ' % path)
                contents = str(coffeescript.compile_file(path, bare=True))
                print '-----------', path, '--------------'
                print contents
            else:
                f = open(path)
                contents = f.read()
                f.close()
            output.append(contents)

        if not nizzle:
            f = open('/tmp/foo.js', 'w')
            for o in output:
                print >> f, o
            f.close()

            f = open('/tmp/foo.js', 'rb')
            output = f.read()
            f.close()
            current_app.javascripts = output
        else:
            #print output
            current_app.javascripts = '\n'.join(output)

    return Response(current_app.javascripts, mimetype='application/javascript')

@app.route('/assets/application.css')
def application_css():
    scripts = [
        #'assets/stylesheets/application2.css',
        'assets/font-awesome.css',
        'assets/stylesheets/app.css',
        'assets/stylesheets/jquery.gridster.css',
    ]
    output = ''
    for path in scripts:
        output += open(path).read()
    return Response(output, mimetype='text/css')


@app.route('/fonts/<path:path>')
def send_js(path):
    return send_from_directory('assets/fonts', path)

@app.route('/assets/images/<path:filename>')
def send_static_img(filename):
    directory = os.path.join('assets', 'images')
    return send_from_directory(directory, filename)

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    html = '%s.html' % widget_name
    path = os.path.join('widgets', widget_name, html)
    if os.path.isfile(path):
        f = open(path)
        contents = f.read()
        f.close()
        return contents

@app.route('/add/<widget_id>/<nValue>')
def addValue(widget_id, nValue):
    if widget_id in dcSamplers:
        print nValue
        objResult = dcSamplers[widget_id].process(int(nValue))
        return Response(json.dumps(objResult), mimetype='text/json')
    print dcSamplers
    return Response('{False}', mimetype='text/json')


@app.route('/events')
def events():
    event_stream_port = request.environ['REMOTE_PORT']
    current_app.logger.info('New Client %s connected. Total Clients: %s' % (event_stream_port, len(xyzzy)))
    #current_event_queue = xyzzy.openStream(event_stream_port)
    return Response(xyzzy.openStream(event_stream_port), mimetype='text/event-stream')


@app.route('/test')
def test():

    print dcSamplers

    print dcSamplers['luiz']._send({'current': 10})

    print xyzzy.events_queue

    import random
    respoonse = {"value" : random.randint(0,100)}
    return Response(json.dumps(respoonse), mimetype='text/event-stream')







def purge_streams():
    big_queues = [port for port, queue in xyzzy.events_queue if len(queue) > xyzzy.MAX_QUEUE_LENGTH]
    for big_queue in big_queues:
        current_app.logger.info('Client %s is stale. Disconnecting. Total Clients: %s' %
                                (big_queue, len(xyzzy.events_queue)))
        del queue[big_queue]


def close_stream(*args, **kwargs):
    event_stream_port = args[2][1]
    xyzzy.closeStream(event_stream_port)
    log.info('Client %s disconnected. Total Clients: %s' % (event_stream_port, len(xyzzy.events_queue)))



if __name__ == "__main__":
    import SocketServer
    SocketServer.BaseServer.handle_error = close_stream
    import example_app

    from samplers.request_sampler import GetRequestNumber

    objRequest = GetRequestNumber('luiz', xyzzy, 5, {'url': 'http://127.0.0.1:5000/test'})
    startSampler(xyzzy, "luiz2", "Meter", {"interval": 0})
    addSampler("luiz", objRequest)

    #example_app.run(app, xyzzy)
    try:
        app.run(debug=True,
                port=5000,
                threaded=True,
                use_reloader=False,
                use_debugger=True
                )
    finally:
        print "Disconnecting clients"
        xyzzy.stop()

        print "Stopping %d timers" % len(dcSamplers)
        for (i, sampler) in dcSamplers:
            sampler.stop()

    print "Done"
