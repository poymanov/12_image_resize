import argparse
import sys
import os
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path to image file')
    parser.add_argument('--width', help='The width of the processed image',
                        type=int)
    parser.add_argument('--height', help='The height of the processed image',
                        type=int)
    parser.add_argument('--scale', help='Image scale ratio', type=float)
    parser.add_argument('--output', help='Path to save resized image',
                        type=str)
    return parser.parse_args()


def get_image_object(filepath):
    try:
        image = Image.open(filepath)
        return image
    except (FileNotFoundError, OSError):
        return None


def get_image_proporsion_ratio(image_object):
    return image_object.width / image_object.height


def resize_image_all_sides(image_object, width, height):
    resized_image_object = resize_image(image_object, width, height)
    origin_proporsion_ratio = get_image_proporsion_ratio(image_object)
    resized_proporsion_ratio = get_image_proporsion_ratio(resized_image_object)

    if origin_proporsion_ratio != resized_proporsion_ratio:
        print('Attention! The proportions of the new image do not match' +
              'the proportions of the original')

    return resized_image_object


def resize_image_one_side(image_object, width=None, height=None):
    origin_proporsion_ratio = get_image_proporsion_ratio(image_object)

    if height is None:
        height = int(width / origin_proporsion_ratio)
    elif width is None:
        width = int(height * origin_proporsion_ratio)

    return resize_image(image_object, width, height)


def scale_image(image_object, ratio):
    scaled_width = int(image_object.width * ratio)
    scaled_height = int(image_object.height * ratio)
    return resize_image(image_object, scaled_width, scaled_height)


def resize_image(image_object, width, height):
    return image_object.resize((width, height))


def validate_arguments(arguments):
    if arguments.width == arguments.height == arguments.scale is None:
        return 'You must specify at least one argument.'
    elif arguments.width and arguments.height and arguments.scale:
        return 'You must specify only width/height or scale. Not both.'

    return True


def get_resize_mode(arguments):
    if args.scale:
        mode = 'scale'
    elif args.width and args.height:
        mode = 'all_sides'
    elif args.width:
        mode = 'by_width'
    elif args.height:
        mode = 'by_height'

    return mode


def get_resized_image(image_object, arguments):
    resize_mode = get_resize_mode(arguments)

    if resize_mode == 'scale':
        resized_image = scale_image(image_object, arguments.scale)
    elif resize_mode == 'all_sides':
        resized_image = resize_image_all_sides(image_object, arguments.width,
                                               arguments.height)
    elif resize_mode == 'by_width':
        resized_image = resize_image_one_side(image_object,
                                              width=arguments.width)
    elif resize_mode == 'by_height':
        resized_image = resize_image_one_side(image_object,
                                              height=arguments.height)

    return resized_image


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
    except (KeyError, IOError):
        return None


if __name__ == '__main__':
    args = parse_args()

    validate_arguments_status = validate_arguments(args)

    if validate_arguments_status is not True:
        sys.exit(validate_arguments_status)

    image_object = get_image_object(args.file)

    if not image_object:
        sys.exit('Failed to open image: file not found or wrong file format')

    resized_image = get_resized_image(image_object, args)
    save_status = save_image(resized_image, args.file, args.output)

    if not save_status:
        sys.exit('Failed to save resized image')
    else:
        sys.exit('Resized file saved to: ' + save_status)
