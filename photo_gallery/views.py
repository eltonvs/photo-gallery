from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config, view_defaults

from photo_gallery.models.user import UserModel
from photo_gallery.models.photo import PhotoModel
from photo_gallery.domain.user import User


@view_defaults(renderer='templates/gallery.jinja2')
class PhotoGalleryViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid
        self.settings = request.registry.settings

    @view_config(route_name='index')
    def index(self):
        user_model = UserModel()
        user = user_model.get_user_from_email(self.logged_in)

        photo_model = PhotoModel()
        photos = photo_model.approved_photos()

        return {
            'user': user,
            'photos': photos
        }

    @view_config(route_name='restrict', renderer='templates/restrict.jinja2')
    def restrict(self):
        user_model = UserModel()
        user = user_model.get_user_from_email(self.logged_in)

        # Redirect to Index if the user isn't logged in
        if not user or not user.admin:
            url = self.request.route_url('index')
            return HTTPFound(location=url)

        photo_model = PhotoModel()
        photos = photo_model.all_photos()

        return {
            'page_title': 'Restrict Page',
            'user': user,
            'photos': photos
        }

    @view_config(route_name='restrict', request_method="POST", renderer='json')
    def restrict_request(self):
        params = self.request.params

        in_photo_id = params.get("photo_id", '')

        photo_model = PhotoModel()
        res = photo_model.toggle_photo_status(in_photo_id)

        return {"approved": res}

    @view_config(route_name='login', renderer='templates/login.jinja2')
    def login(self):
        return {
            'page_title': 'Login',
        }

    @view_config(
        route_name='login',
        request_method='POST',
        renderer='templates/login.jinja2'
    )
    def login_request(self):
        request = self.request
        params = request.params

        in_email = params.get('email', '')
        in_password = params.get('password', '')

        # Try to log in user
        user_model = UserModel()
        err = user_model.login(in_email, in_password)
        if not err:
            url = request.route_url('index')
            headers = remember(request, in_email)
            return HTTPFound(location=url, headers=headers)

        return {
            'page_title': 'Login',
            'errors': err,
            'email': in_email,
        }

    @view_config(route_name='register', renderer='templates/register.jinja2')
    def register(self):
        return {
            'page_title': 'Register'
        }

    @view_config(
        route_name='register',
        request_method='POST',
        renderer='templates/register.jinja2'
    )
    def register_request(self):
        params = self.request.params

        in_name = params.get('name', '')
        in_email = params.get('email', '')
        in_password = params.get('password', '')
        in_confirm_password = params.get('confirm-password', '')
        in_admin = params.get('admin', False)
        if in_admin:
            in_admin = True

        user = User(in_name, in_email, in_password, in_admin)

        user_model = UserModel()
        register_user = user_model.register(user, in_confirm_password)

        return {
            'page_title': 'Registered User',
            'errors': register_user,
            'user': user
        }

    @view_config(route_name='upload', renderer='templates/upload.jinja2')
    def upload(self):
        user_model = UserModel()
        user = user_model.get_user_from_email(self.logged_in)

        # Redirect to Index if the user isn't logged in
        if not user:
            url = self.request.route_url('index')
            return HTTPFound(location=url)

        return {
            'page_title': 'Upload',
            'user': user
        }

    @view_config(
        route_name='upload',
        request_method="POST",
        renderer='templates/upload.jinja2'
    )
    def upload_request(self):
        user_model = UserModel()
        user = user_model.get_user_from_email(self.logged_in)

        # Redirect to Index if the user isn't logged in
        if not user:
            url = self.request.route_url('index')
            return HTTPFound(location=url)

        params = self.request.params
        storage = self.request.storage
        bucket_name = self.settings['storage.aws.bucket_name']

        in_photo = params.get('photo', None)

        photo_model = PhotoModel()
        errors = photo_model.save_photo(in_photo, storage, bucket_name)

        return {
            'page_title': 'Upload',
            'user': user,
            'errors': errors,
            'photo': in_photo
        }

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('index')

        return HTTPFound(location=url, headers=headers)
