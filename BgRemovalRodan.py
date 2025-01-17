import os

from rodan.jobs.base import RodanTask
from celery.utils.log import get_task_logger

class BgRemoval(RodanTask):

    name = 'Remove background'
    author = 'Wanyi Lin and Khoi Nguyen'
    description = "Use Sauvola threshold to remove background"
    logger = get_task_logger(__name__)

    enabled = True
    category = 'Background removal - remove image background'
    interactive = False

    input_port_types = [{
        'name': 'PNG Image',
        'resource_types': lambda mime: mime.startswith('image/'),
        'minimum': 1,
        'maximum': 1
    }]
    output_port_types = [{
        'name': 'RGB PNG image',
        'resource_types': ['image/rgb+png'],
        'minimum': 1,
        'maximum': 1
    }]

    settings = {
        'title': 'Remove Background',
        'type': 'object',
        'job_queue': 'Python3',

        'properties': {
            'window_size': {
                'type': 'integer',
                'minimum': 1,
                'default': 15
            },
            'k': {
                'type': 'number',
                'minimum': 0.0,
                'default': 0.2
            },
            'contrast': {
                'type': 'number',
                'default': 127
            },
            'brightness': {
                'type': 'number',
                'default': 0
            }
        }
    }

    def run_my_task(self, inputs, settings, outputs):
        from . import background_removal_engine as Engine
        from . import LoaderWriter

        mode = 'rgb'
        load_image_path = inputs['PNG image'][0]['resource_path']
        image_bgr = LoaderWriter.load_image(load_image_path, mode=mode)

        # Remove background here.
        image_processed = Engine.remove_background(image_bgr, settings["window_size"], settings["k"], settings["contrast"], settings["brightness"])

        save_image_path = "{}.png".format(outputs['RGB PNG image'][0]['resource_path'])
        LoaderWriter.write_image(save_image_path, image_processed, mode=mode)
        os.rename(save_image_path,outputs['RGB PNG image'][0]['resource_path'])
        return True

    def my_error_information(self, exc, traceback):
        return
