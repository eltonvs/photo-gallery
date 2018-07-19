from bson import ObjectId

from .mongo_database import MongoDatabase
from ..domain.photo import Photo


class PhotoDAO():
    def __init__(self):
        self.db = MongoDatabase().instance()

    def insert(self, photo):
        photo_to_insert = {
            "s3_file": photo.s3_file_name,
            "url": photo.url,
            "approved": photo.approved
        }
        return self.db.photos.insert(photo_to_insert)

    def get_approved_photos(self):
        photos = self.db.photos.find({"approved": True})
        return [self.photo_from_dict(photo) for photo in photos]

    def get_all_photos(self):
        photos = self.db.photos.find()
        return [self.photo_from_dict(photo) for photo in photos]

    def get_photo_from_id(self, photo_id):
        photo = self.db.photos.find_one({"_id": ObjectId(photo_id)})
        return self.photo_from_dict(photo)

    def toggle_photo_status(self, photo_id):
        photo = self.get_photo_from_id(photo_id)
        if photo:
            self.db.photos.update(
                {"_id": photo.id},
                {"$set": {"approved": not(photo.approved)}}
            )
            return not(photo.approved)

    def photo_from_dict(self, photo):
        if photo:
            photo_obj = Photo(
                photo.get('s3_file', ''),
                photo.get('url', ''),
                photo.get('approved', ''),
            )
            photo_obj.id = photo.get('_id', '')
            return photo_obj
