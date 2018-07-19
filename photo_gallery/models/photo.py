from photo_gallery.dao.photo import PhotoDAO
from photo_gallery.domain.photo import Photo


class PhotoModel():
    def __init__(self):
        self.photo_dao = PhotoDAO()

    def save_photo(self, image, storage, bucket):
        err = self.validate(image, storage, bucket)
        if err:
            return err

        s3_file = storage.save(image, randomize=True)
        photo = Photo(s3_file, storage.url(s3_file), False)
        self.photo_dao.insert(photo)

    def approved_photos(self):
        return self.photo_dao.get_approved_photos()

    def all_photos(self):
        return self.photo_dao.get_all_photos()

    def toggle_photo_status(self, photo_id):
        return self.photo_dao.toggle_photo_status(photo_id)

    def validate(self, image, storage, bucket):
        err = {}
        if image is None:
            err['no_image'] = True
        if storage is None:
            err['no_storage'] = True
        if bucket == '':
            err['no_bucket'] = True
        return err
