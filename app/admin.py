
# implementing admin page

from flask_admin.contrib.sqla import ModelView  # contrib pakage contains special veiw classes
from flask_admin import Admin
from app import db, App
from app.models import User, Cards, Dht11, Gaz
from wtforms.fields import PasswordField
from flask_admin.contrib.fileadmin import FileAdmin
from flask import g, url_for, redirect, request
from flask_admin import AdminIndexView, expose   #


class IndexView(AdminIndexView):
    @expose('/')  # decorator for index_admin page
    def index(self):
        if not (g.user.is_authenticated and g.user.is_admin()):  # redirect authenticated users to a login page
            return redirect(url_for('login', next=request.path))
        return self.render('index_admin.html')


admin = Admin(App, 'Administrator Page', index_view=IndexView())     # visit this page /admin/


class AdminAuthentication(object):

    def is_accessible(self):
        return g.user.is_authenticated and g.user.is_admin()


class UserModelView(AdminAuthentication, ModelView):

    # override the admin colum_list for 'User table'
    column_list = ['firstname', 'lastname', 'email', 'user_password', 'created_timestamp',
                   'last_seen', 'admin']
    # add search box
    column_searchable_list = ['firstname', 'lastname', 'email']
    # specify sortable list
    column_sortable_list = ['firstname', 'lastname', 'email', 'created_timestamp', 'last_seen', 'admin']
    # add filter capability to easy search
    column_filters = [User.firstname, User.lastname, User.email, 'created_timestamp']

    # #customizing the create from

    form_columns = ['firstname', 'lastname','email', 'password', 'admin']

    # fix the password_hash from create User admin page
    form_extra_fields = {
        'password': PasswordField('password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)


class CardModelView(AdminAuthentication, ModelView):
    column_sortable_list = ['name', 'timestamp', 'user_id']
    column_filters = [Cards.name, 'timestamp', 'user_id']
    column_searchable_list = ['name', 'timestamp', 'user_id']

    # #custom the create form
    form_columns = ['name', 'owner']

    # add search capability to fetch the desired user ( foreign key )
    form_ajax_refs = {
        'owner': {
            'fields': (User.firstname, User.lastname,  User.email)
        }
    }


class BlogFileAdmin(AdminAuthentication, FileAdmin):
    pass


admin.add_view(UserModelView(User, db.session))  # db.session: to access to database
admin.add_view(CardModelView(Cards, db.session))
#admin.add_view(ModelView(Dht11, db.session))
#admin.add_view(ModelView(Gaz, db.session))
admin.add_view(BlogFileAdmin(App.config['STATIC_DIR'], './static', name='Static Files'))


