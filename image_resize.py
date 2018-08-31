import argparse
import sys
import os
from PIL import Image


def get_args_descriptions():
    descriptions = {}
    descriptions['file'] = 'Path to image file'
    descriptions['width'] = 'The width of the processed image'
    descriptions['height'] = 'The height of the processed image'
    descriptions['scale'] = 'Image scale ratio'
    descriptions['output'] = 'Path to save resized image'

    return descriptions


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
    descriptions = get_args_descriptions()

    parser.add_argument('file', help=descriptions['file'])
    parser.add_argument('--width', help=descriptions['width'], type=int)
    parser.add_argument('--height', help=descriptions['height'], type=int)
    parser.add_argument('--scale', help=descriptions['scale'], type=float)
    parser.add_argument('--output', help=descriptions['output'], type=str)

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


def check_resized_proportions(origin_sizes, new_sizes):
    origin_width, origin_height = origin_sizes
    origin_ratio = get_proporsion_ratio(origin_width, origin_height)

    new_width, new_height = new_sizes
    new_ratio = get_proporsion_ratio(new_width, new_height)

    ratio_delta = abs(origin_ratio - new_ratio)
    allowed_ratio_delta = 0.1

    if ratio_delta > allowed_ratio_delta:
        print('Attention! The proportions of the new image do not match'
              'the proportions of the original')


def get_proporsion_ratio(width, height):
    return width / height


def get_new_image_size(origin_sizes, width, height, scale):
    image_width, image_height = origin_sizes
    origin_ratio = get_proporsion_ratio(image_width, image_height)

    if scale:
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)
    elif width and height:
        new_width = width
        new_height = height
    elif width:
        new_width = width
        new_height = int(width / origin_ratio)
    elif height:
        new_width = int(height * origin_ratio)
        new_height = height

    return new_width, new_height


def resize_image(image, new_sizes):
    return image.resize(new_sizes)


def save_image(image, origin_file, output_path):
    filename, extension = os.path.splitext(origin_file)
    width = image.width
    height = image.height
    new_filename = '{}__{}x{}{}'.format(filename, width, height, extension)

    if output_path:
        new_filepath = os.path.join(output_path, new_filename)
    else:
        new_filepath = new_filename

    try:
        image.save(new_filepath)
        return new_filepath
    except IOError:
        return None


if __name__ == '__main__':
    args = parse_args()

    image = get_image_object(args.file)

    if not image:
        sys.exit('Failed to open image: '
                 'file not found or have got wrong file format')

    origin_sizes = (image.width, image.height)

    new_sizes = get_new_image_size(origin_sizes, args.width,
                                   args.height, args.scale)

    check_resized_proportions(origin_sizes, new_sizes)

    resized_image = resize_image(image, new_sizes)

    save_status = save_image(resized_image, args.file, args.output)

    if not save_status:
        sys.exit('Failed to save resized image')
    else:
        sys.exit('Resized file saved to: {}'.format(save_status))
