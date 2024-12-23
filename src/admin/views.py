from starlette_admin.contrib.sqla import ModelView


class PKModelView(ModelView):
    form_include_pk = True
