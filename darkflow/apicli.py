from .defaults import argHandler #Import the default arguments
import os
import shutil
from .net.build import TFNet

def cliHandlerApi():
    FLAGS = argHandler()
    FLAGS.setApiDefaults()
    # FLAGS.parseArgs(args)

    print('*** apicli flags:', FLAGS)

    # make sure all necessary dirs exist (블러 디렉토리도 만들기!)
    def _get_dir(dirs):
        for d in dirs:
            this = os.path.abspath(os.path.join(os.path.curdir, d))
            if not os.path.exists(this): os.makedirs(this)
    requiredDirectories = [FLAGS.imgdir, FLAGS.binary, FLAGS.backup, os.path.join(FLAGS.imgdir,'out'), os.path.join(FLAGS.imgdir,'blur')]
    if FLAGS.summary:
        requiredDirectories.append(FLAGS.summary)

    _get_dir(requiredDirectories)

    # fix FLAGS.load to appropriate type
    try: FLAGS.load = int(FLAGS.load)
    except: pass

    tfnet = TFNet(FLAGS)
    
    if FLAGS.demo:
        tfnet.camera()
        exit('Demo stopped, exit.')

    if FLAGS.train:
        print('Enter training ...'); tfnet.train()
        if not FLAGS.savepb: 
            exit('Training finished, exit.')

    if FLAGS.savepb:
        print('Rebuild a constant version ...')
        tfnet.savepb(); exit('Done')

    tfnet.predict()