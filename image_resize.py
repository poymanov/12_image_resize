import argparse
import sys
import os
from PIL import Image


def get_args_descriptions():
    return {'file': 'Path to image file',
            'width': 'The width of the processed image',
            'height': 'The height of the processed image',
            'scale': 'Image scale ratio',
            'output': 'Path to save resized image'}


def validate_arguments(args):
    if args.width == args.height == args.scale is None:
        return 'You must specify at least one argument.'
    elif (args.width or args.height) and args.scale:
        return 'You must specify only width/height or scale. Not both.'
    elif 0 in [args.width, args.height, args.scale]:
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


def check_proportions(origin_ratio, new_ratio):
    ratio_delta = abs(origin_ratio - new_ratio)
    allowed_ratio_delta = 0.1

    if ratio_delta > allowed_ratio_delta:
        print(('Attention! The proportions of the new image do not match'
               'the proportions of the original'))


def get_proporsion_ratio(width, height):
    return width / height


def get_resize_info(image_object, width, height, scale):
    origin_proporsion_ratio = get_proporsion_ratio(image_object.width,
                                                   image_object.height)

    if scale:
        new_width = int(image_object.width * scale)
        new_height = int(image_object.height * scale)
    elif width and height:
        new_width = width
        new_height = height
        resized_proporsion_ratio = get_proporsion_ratio(new_width, new_height)
        check_proportions(origin_proporsion_ratio, resized_proporsion_ratio)
    elif width:
        new_width = width
        new_height = int(width / origin_proporsion_ratio)
    elif height:
        new_width = int(height * origin_proporsion_ratio)
        new_height = height

    return new_width, new_height


def resize_image(image_object, width, height):
    return image_object.resize((width, height))


def save_image(image_object, origin_filepath, output_filepath):
    origin_filename, origin_file_extension = os.path.splitext(origin_filepath)
    image_width = image_object.width
    image_height = image_object.height
    new_filename = '{}__{}x{}{}'.format(origin_filename, image_width,
                                        image_height, origin_file_extension)

    if output_filepath:
        new_filepath = os.path.join(output_filepath, new_filename)
    else:
        new_filepath = new_filename

    try:
        image_object.save(new_filepath)
        return new_filepath
    except IOError:
        return None


if __name__ == '__main__':
    args = parse_args()

    image_object = get_image_object(args.file)

    if not image_object:
        sys.exit(('Failed to open image: '
                  'file not found or have got wrong file format'))

    new_width, new_height = get_resize_info(image_object, args.width,
                                            args.height, args.scale)

    resized_image = resize_image(image_object, new_width, new_height)

    save_status = save_image(resized_image, args.file, args.output)

    if not save_status:
        sys.exit('Failed to save resized image')
    else:
        sys.exit('Resized file saved to: ' + save_status)
