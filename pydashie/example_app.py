from example_samplers import *
from samplers.request_sampler import GetRequestNumber, GetRequestMeter

def run(app, xyzzy):
    samplers = [
        SynergySampler('synergy', xyzzy, 3),
        BuzzwordsSampler('buzzwords', xyzzy, 2), # 10
        ConvergenceSampler('convergence', xyzzy, 1),

        GetRequestMeter('meterTest', xyzzy, 4, {'url': 'http://127.0.0.1:5000/test'}),
        GetRequestNumber('luiz', xyzzy, 5, {'url': 'http://127.0.0.1:5000/test'})
    ]

    try:
        app.run(debug=True,
                port=5000,
                threaded=True,
                use_reloader=False,
                use_debugger=True
                )
    finally:
        print "Disconnecting clients"
        xyzzy.stopped = True
        
        print "Stopping %d timers" % len(samplers)
        for (i, sampler) in enumerate(samplers):
            sampler.stop()

    print "Done"
