from PIL import Image



class ResizeImageMixin:
    def resize_image(self, image_field, size, size_title='large'):
        """
            This function will resize any image with given size
            and return new image path

            :param imageField: Original Image
            :param size: desire width of resized image.
            :param size_title: size title of the desire size.
            :return: file path of the new image
        """

        # opening original image file
        source_image = Image.open(image_field.path)

        # Resize to desire size
        source_image.thumbnail(size, resample=Image.ANTIALIAS)

        # extracting original file name
        original_file_name = image_field.path.split('/')[-1]

        # create new file name with concating original file name and  desire size
        tmp_original_file_name = original_file_name.split(".")

        # create new file name without file extension
        new_file_name = f'{tmp_original_file_name[0]}_{size_title}'

        # if extension exist in original file, add extension in new file
        if len(tmp_original_file_name)>1:
            new_file_name = f'{new_file_name}.{tmp_original_file_name[1]}'

        # making new image file path
        new_file_path = image_field.path.replace(original_file_name, new_file_name)

        # storing new image file
        source_image.save(new_file_path, quality=100)

        return new_file_path