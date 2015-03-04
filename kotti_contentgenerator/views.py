from kotti_contentgenerator.generator import Generator
from kotti.views.form import BaseFormView
import colander
import deform

#seed, depth, top_level, sub_level, users, root_types, content_types

class GeneratorSchema(colander.MappingSchema):
    seed = colander.SchemaNode(
        colander.Integer(),
        title=_(u'Seed'),
        default=1,
        )
    depth = colander.SchemaNode(
        colander.Integer(),
        title=_('Depth'),
        description=_('How many sublevels to create'),
        default=2,
        )
    top_level = colander.SchemaNode(
        colander.Integer(),
        title=_('Top level'),
        description=_('How many objects to put in this context'),
        default=10,
        )
    sub_level = colander.SchemaNode(
        colander.Integer(),
        title=_('Sub level'),
        description=_('How many objects to put in each sublevel'),
        default=10,
        )
    users = colander.SchemaNode(
        colander.Integer(),
        title=_('Users'),
        description=_('How many users to create'),
        default=10,
        )
    root_types = colander.SchemaNode(
        colander.String(),
        title=_('Root types'),
        description=_('What type of content to put in the top level'),
        default=u'',
        )
    content_types = colander.SchemaNode(
        colander.Integer(),
        title=_('Sublevel content types'),
        description=_('What type of content to create in sublevels'),
        default=u'',
        )


class GeneratorView(BaseFormView):
    """ A generator form to be called as a view
    """

    buttons = (
        deform.Button('generate', _(u'Generate content')),
        deform.Button('cancel', _(u'Cancel')))

    success_message = _(u"Your content has been generated.")

    def generate_success(self, appstruct):
        generator = Generator(**appstruct)
        count = generator.generate(self.context)
        return {'count': count}


def includeme(config):
    config.scan(__name__)
