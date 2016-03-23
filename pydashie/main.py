import json
import logging
import os
import sys
from flask import Flask, render_template, Response, send_from_directory, request, current_app

#sys.path.append(os.pardir(__file__))
from libs.dashboard import DashingBoard

#TODO: save / load from file
#TODO: GET in push sampler.
#TODO: docker file
#TODO: package installer


def saveFile(strId, dcInput):
    import os, json
    strFile = os.path.realpath(__file__)
    strPath = os.path.dirname(strFile)
    strSave = os.path.join(strPath, "dashboards", strId + '.json')
    print(strSave)
    f = open(strSave, 'w')
    f.write(json.dumps(dcInput))
    f.close()

def loadFile(strId):
    import os, json
    strFile = os.path.realpath(__file__)
    strPath = os.path.dirname(strFile)
    strSave = os.path.join(strPath, "dashboards", strId + '.json')
    print(strSave)
    f = open(strSave, 'r')
    objResponse = json.loads(f.read())
    f.close()
    return objResponse


dcDefinitions = loadFile("test")
print(dcDefinitions.get('widgets', None))
objDashboard = DashingBoard(dcDefinitions)
app = Flask(__name__)
logging.basicConfig()
log = logging.getLogger(__name__)

arJavaScripts = [
            'projects/dashing/javascripts/jquery.js',
            'projects/dashing/templates/project/assets/javascripts/d3-3.2.8.js',
            'projects/gridster/dist/jquery.gridster.min.js',
            'projects/dashing/templates/project/assets/javascripts/gridster/jquery.leanModal.min.js',
            'projects/dashing/templates/project/assets/javascripts/jquery.knob.js',
            'projects/dashing/templates/project/assets/javascripts/rickshaw-1.4.3.min.js',
            'projects/dashing/javascripts/es5-shim.js',
            'projects/dashing/javascripts/batman.js',
            'projects/dashing/javascripts/batman.jquery.js',
            'projects/dashing/javascripts/dashing.js',
            'projects/dashing/templates/project/assets/javascripts/dashing.gridster.js',
            'dashingInternal.js',
            'pyDashing.js'
        ]

arStyleSheets = [
        'projects/fontawesome/css/font-awesome.min.css',
        'projects/gridster/dist/jquery.gridster.min.css',
        'projects/dashing/templates/project/assets/stylesheets/application.css',
        'pyDashing.css'
    ]

strFontPath = 'projects/fontawesome/fonts'

bForceReload = True


def loadContent(strPath):
    try:
        if os.path.isfile(strPath):
            f = open(strPath)
            contents = f.read()
            f.close()
            return contents
    except Exception as e:
        print(e)
    return ''

@app.route("/")
def main():
    strTitle = objDashboard._dcDefinitions.get('title', 'pyDashing')
    arWidgets = objDashboard.getWidget()
    bEdit = request.args.get('edit', False)
    return render_template('index.html', title=strTitle, widgets=arWidgets, edit=bEdit)
    
@app.route("/dashboard/<dashlayout>/")
def custom_layout(dashlayout):
    return render_template('%s.html'%dashlayout, title='pyDashie')

@app.route("/assets/application.js")
def javascripts():
    global arJavaScripts, bForceReload
    if not hasattr(current_app, 'javascripts') or bForceReload:
        arJavaScripts.extend(objDashboard._arJavascript)
        current_app.javascripts = ""
        import coffeescript
        for path in arJavaScripts:
            current_app.javascripts += '// JS: %s\n' % str(path)
            if '.coffee' in path:
                log.info('Compiling Coffee for %s ' % path)
                contents = str(coffeescript.compile_file(path, bare=True))
                print('-----------', path, '--------------')
                print(contents)
            else:
                contents = loadContent(path)
            current_app.javascripts += contents
    return Response(current_app.javascripts, mimetype='application/javascript')

@app.route("/assets/edit.js")
def edit():
    return Response(loadContent('edit.js'), mimetype='application/javascript')

@app.route('/assets/application.css')
def stylesheets():
    global arStyleSheets
    arStyleSheets.extend(objDashboard._arStyles)
    output = ''
    for strPath in arStyleSheets:
        output += loadContent(strPath)
    return Response(output, mimetype='text/css')

@app.route('/assets/fonts/<path:strPath>')
@app.route('/fonts/<path:strPath>')
def send_js(strPath):
    global strFontPath
    return send_from_directory(strFontPath, strPath)

@app.route('/assets/images/<path:filename>')
@app.route('/images/<path:filename>')
def send_static_img(filename):
    directory = os.path.join('assets', 'images')
    return send_from_directory(directory, filename)

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    if widget_name == 'dashing_internal':
        return '<span data-bind="internal"></span>'
    if '_' in widget_name:
        arTitles = [s.title() for s in widget_name.split('_')]
        arTitles[0] = arTitles[0].lower()
        strWidget = ''.join(arTitles)
    else:
        strWidget = widget_name
    html = '%s.html' % widget_name
    return loadContent(os.path.join('widgets', strWidget, html))



@app.route('/events')
def events():
    event_stream_port = request.environ['REMOTE_PORT']
    current_app.logger.info('New Client %s connected. Total Clients: %s' % (event_stream_port, len(objDashboard._objStreams)))
    return Response(objDashboard._objStreams.openStream(event_stream_port), mimetype='text/event-stream')


@app.route('/update', methods=['POST'])
def update():
    print(request)
    content = request.get_json(silent=True)
    print(content)
    if content:
        objDashboard.updateLayout(content)
    return Response(json.dumps(True), mimetype='text/json')


@app.route('/reload', methods=['GET'])
def reload():
    bResponse = objDashboard.refresh()
    return Response(json.dumps(bResponse), mimetype='text/json')


@app.route('/shutdown', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


@app.route('/add/widget', methods=['POST'])
def addValue():
    objResponse = None
    dcSettings = request.get_json(silent=True)
    if dcSettings:
        objResponse = objDashboard.startWidget(dcSettings)
    return Response(json.dumps(objResponse), mimetype='text/json')


@app.route('/add/sampler', methods=['POST'])
def addSampler():
    objResponse = None
    dcSettings = request.get_json(silent=True)
    if dcSettings:
        objResponse = objDashboard.startSampler(dcSettings)
    return Response(json.dumps(objResponse), mimetype='text/json')


@app.route('/push/<strType>/<path:strUrl>', methods=['POST'])
def push(strType, strUrl):
    objResponse = False
    try:
        strType = strType.lower()
        if strType == 'json':
            objContent = request.get_json(silent=True)
        elif strType == 'integer':
            objContent = int(request.data)
        elif strType == 'decimal':
            objContent = float(request.data)
        #elif strType == 'xml':
        #    import xmltodict
        #    objContent = xmltodict.parse(request.data)
        print(request.args)
        print(request.headers)
        if objContent:
            objResponse = objDashboard.push(strUrl, objContent)
    except Exception as e:
        print(e)
    return Response(json.dumps(objResponse), mimetype='text/json')


@app.route('/test')
def test():
    import random
    response = {
        "number1": random.randint(0,100),
        "number2": random.randint(0,100),
        "number3": random.randint(0,100),
        "graph1": [random.randint(0,100)],
        "graph2": [random.randint(0,100)]
    }
    return Response(json.dumps(response), mimetype='text/json')




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
    if sys.version_info >= (3, 0):
        import socketserver as SocketServer
    else:
        import SocketServer

    SocketServer.BaseServer.handle_error = close_stream
    try:
        app.run(host="0.0.0.0",
                debug=True,
                port=8666,
                threaded=True,
                use_reloader=False,
                use_debugger=True
                )
    finally:
        print("Disconnecting clients")
        saveFile("test", objDashboard.getSettings())
        objDashboard.stop()
    exit()
