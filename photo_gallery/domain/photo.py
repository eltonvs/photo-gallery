class Photo():
    def __init__(self, s3_file_name, url, approved):
        self._id = None
        self._s3_file_name = s3_file_name
        self._url = url
        self._approved = approved

    def __str__(self):
        return self.s3_file_name

    @property
    def s3_file_name(self):
        return self._s3_file_name

    @s3_file_name.setter
    def s3_file_name(self, value):
        self._s3_file_name = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def approved(self):
        return self._approved

    @approved.setter
    def approved(self, value):
        self._approved = value
