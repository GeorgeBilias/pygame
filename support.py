from os import walk

import pygame.image


# walk allows us to 'walk' through different folders

def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):

        for image in img_files:  # iterate in the folder
            full_path = path + '/' + image  # create path variable
            image_surf = pygame.image.load(full_path).convert_alpha()  # load the image from the full path
            surface_list.append(image_surf)

    return surface_list

def import_folder_dict(path):
    surface_dict = {}

    for _, __, img_files in walk(path):
        for image in img_files:  # iterate in the folder
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    print(surface_dict)

    return surface_dict
