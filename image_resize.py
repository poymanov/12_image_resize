import argparse
import sys
import os
from PIL import Image


def get_args_descriptions():
    descr = {}
    descr['file'] = 'Path to image file'
    descr['width'] = 'The width of the processed image'
    descr['height'] = 'The height of the processed image'
    descr['scale'] = 'Image scale ratio'
    descr['output'] = 'Path to save resized image'

    return descr


def validate_arguments(args):
    width = args.width
    height = args.height
    scale = args.scale

    if width == height == scale is None:
        return 'You must specify at least one argument.'
    elif (width or height) and scale:
        return 'You must specify only width/height or scale. Not both.'
    elif not all(arg is None or arg > 0 for arg in [width, height, scale]):
        return 'Values of arguments must be greater than 0'


def parse_args():
    parser = argparse.ArgumentParser()
    descr = get_args_descriptions()

    parser.add_argument('file', help=descr['file'])
    parser.add_argument('--width', help=descr['width'], type=int)
    parser.add_argument('--height', help=descr['height'], type=int)
    parser.add_argument('--scale', help=descr['scale'], type=float)
    parser.add_argument('--output', help=descr['output'], type=str)

    parsed_args = parser.parse_args()
    validation_status = validate_arguments(parsed_args)

    if validation_status:
        parser.error(validation_status)

    return parsed_args


def get_image_object(filepath):
    try:
        image = Image.open(filepath)
        return image
    except OSError:
        return None


def check_resized_proportions(new_sizes, params):
    new_width, new_height = new_sizes
    new_ratio = get_proporsion_ratio(new_width, new_height)

    ratio_delta = abs(params['origin_ratio'] - new_ratio)
    allowed_ratio_delta = 0.1

    if ratio_delta > allowed_ratio_delta:
        print('Attention! The proportions of the new image do not match'
              'the proportions of the original')


def get_proporsion_ratio(width, height):
    return width / height


def get_resize_info(params):
    width = params['width']
    height = params['height']
    scale = params['scale']

    if scale:
        new_width = int(params['image_width'] * scale)
        new_height = int(params['image_height'] * scale)
    elif width and height:
        new_width = width
        new_height = height
    elif width:
        new_width = width
        new_height = int(width / params['origin_ratio'])
    elif height:
        new_width = int(height * params['origin_ratio'])
        new_height = height

    return new_width, new_height


def resize_image(params, new_sizes):
    return params['image'].resize(new_sizes)


def save_image(image, params):
    filename, extension = os.path.splitext(params['file'])
    width = image.width
    height = image.height
    new_filename = '{}__{}x{}{}'.format(filename, width, height, extension)

    if params['output']:
        new_filepath = os.path.join(params['output'], new_filename)
    else:
        new_filepath = new_filename

    try:
        image.save(new_filepath)
        return new_filepath
    except IOError:
        return None


def get_resize_params(image, args):
    params = {}
    params['image'] = image
    params['file'] = args.file
    params['width'] = args.width
    params['height'] = args.height
    params['scale'] = args.scale
    params['output'] = args.output
    params['image_width'] = image.width
    params['image_height'] = image.height
    params['origin_ratio'] = get_proporsion_ratio(image.width, image.height)

    return params


if __name__ == '__main__':
    args = parse_args()

    image = get_image_object(args.file)

    if not image:
        sys.exit('Failed to open image: '
                 'file not found or have got wrong file format')

    resize_params = get_resize_params(image, args)

    new_sizes = get_resize_info(resize_params)

    check_resized_proportions(new_sizes, resize_params)

    resized_image = resize_image(resize_params, new_sizes)

    save_status = save_image(resized_image, resize_params)

    if not save_status:
        sys.exit('Failed to save resized image')
    else:
        sys.exit('Resized file saved to: {}'.format(save_status))
