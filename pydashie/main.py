import json
import logging
import os
from flask import Flask, render_template, Response, send_from_directory, request, current_app
from libs.dashboard import DashingBoard



def saveFile(strId, dcInput):
    import os, json
    strFile = os.path.realpath(__file__)
    strPath = os.path.dirname(strFile)
    strSave = os.path.join(strPath, "dashboards", strId + '.json')
    print strSave
    f = open(strSave, 'w')
    f.write(json.dumps(dcInput))
    f.close()

def loadFile(strId):
    import os, json
    strFile = os.path.realpath(__file__)
    strPath = os.path.dirname(strFile)
    strSave = os.path.join(strPath, "dashboards", strId + '.json')
    print strSave
    f = open(strSave, 'r')
    objResponse = json.loads(f.read())
    f.close()
    return objResponse


dcDefinitions = loadFile("test")
objDashboard = DashingBoard(dcDefinitions)
app = Flask(__name__)
logging.basicConfig()
log = logging.getLogger(__name__)


@app.route("/")
def main():
    dcDashboard = objDashboard._dcDefinitions
    return render_template('index.html', dashboard=dcDashboard)
    
@app.route("/dashboard/<dashlayout>/")
def custom_layout(dashlayout):
    return render_template('%s.html'%dashlayout, title='pyDashie')

@app.route("/assets/application.js")
def javascripts():
    if not hasattr(current_app, 'javascripts'):
        scripts = [
            'assets/javascripts/jquery.js',
            'assets/javascripts/d3-3.2.8.js',
            'assets/javascripts/gridster/jquery.gridster.min.js',
            'assets/javascripts/gridster/jquery.leanModal.min.js',
            'assets/javascripts/jquery.knob.js',
            'assets/javascripts/rickshaw-1.4.3.min.js',
            'assets/javascripts/es5-shim.js',
            'assets/javascripts/batman.js',
            'assets/javascripts/batman.jquery.js',
            'assets/javascripts/dashing.js',
            'assets/javascripts/dashing.gridster.js',
            'assets/javascripts/application.js',
        ]
        print scripts
        print objDashboard._arJavascript
        scripts.extend(objDashboard._arJavascript)

        current_app.javascripts = ""
        import coffeescript
        for path in scripts:
            current_app.javascripts += '// JS: %s\n' % str(path)
            if '.coffee' in path:
                log.info('Compiling Coffee for %s ' % path)
                contents = str(coffeescript.compile_file(path, bare=True))
                print '-----------', path, '--------------'
                print contents
            else:
                f = open(path)
                contents = f.read()
                f.close()
            current_app.javascripts += contents
    return Response(current_app.javascripts, mimetype='application/javascript')

@app.route('/assets/application.css')
def application_css():
    scripts = [
        'assets/stylesheets/font-awesome.css',
        'assets/stylesheets/application.css',
        'assets/stylesheets/jquery.gridster.min.css',
    ]
    scripts.extend(objDashboard._arStyles)
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
    response = objDashboard.push(widget_id, nValue)
    return Response(json.dumps(response), mimetype='text/json')

@app.route('/events')
def events():
    event_stream_port = request.environ['REMOTE_PORT']
    current_app.logger.info('New Client %s connected. Total Clients: %s' % (event_stream_port, len(objDashboard._objStreams)))
    #current_event_queue = xyzzy.openStream(event_stream_port)
    return Response(objDashboard._objStreams.openStream(event_stream_port), mimetype='text/event-stream')

@app.route('/update', methods=['POST', 'GET'])
def update():
    print request
    content = request.get_json(silent=True)
    print content
    return Response(json.dumps(True), mimetype='text/json')

@app.route('/test')
def test():
    import random
    respoonse = {"value" : random.randint(0,100)}
    return Response(json.dumps(respoonse), mimetype='text/json')


@app.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'





def purge_streams():
    big_queues = [port for port, queue in objDashboard._objStreams.events_queue if len(queue) > objDashboard._objStreams.MAX_QUEUE_LENGTH]
    for big_queue in big_queues:
        current_app.logger.info('Client %s is stale. Disconnecting. Total Clients: %s' %
                                (big_queue, len(objDashboard._objStreams.events_queue)))
        del queue[big_queue]


def close_stream(*args, **kwargs):
    event_stream_port = args[2][1]
    objDashboard._objStreams.closeStream(event_stream_port)
    log.info('Client %s disconnected. Total Clients: %s' % (event_stream_port, len(objDashboard._objStreams.events_queue)))



if __name__ == "__main__":
    import SocketServer
    SocketServer.BaseServer.handle_error = close_stream
    try:
        app.run(debug=True,
                port=5000,
                threaded=True,
                use_reloader=False,
                use_debugger=True
                )
        print "test"
    finally:
        print "Disconnecting clients"
        saveFile("test", objDashboard._dcDefinitions)
        objDashboard.stop()
    print "Done"
    exit()
