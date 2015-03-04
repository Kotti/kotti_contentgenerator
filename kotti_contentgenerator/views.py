from kotti.views.form import BaseFormView
from kotti_contentgenerator.generator import Generator
from kotti_contentgenerator import _
from pyramid.util import object_description
import colander
import deform


def make_generator_schema(generator):
    """ Create the colander schema based on generator's factories

    :return: a colander Schema
    :rtype: `colander.Schema`
    """

    type_choices = []
    for klass in generator.factories.keys():
        od = object_description(klass)
        type_choices.append((od, od))

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
            colander.Set(),
            title=_('Root types'),
            description=_('What type of content to put in the top level'),
            widget=deform.widget.CheckboxChoiceWidget(
                                    values=type_choices, inline=True),
            validator=colander.Length(min=1),
            )
        content_types = colander.SchemaNode(
            colander.Set(),
            title=_('Sublevel content types'),
            description=_('What type of content to create in sublevels'),
            widget=deform.widget.CheckboxChoiceWidget(
                                    values=type_choices, inline=True),
            validator=colander.Length(min=1),
            )

    return GeneratorSchema()


class GeneratorView(BaseFormView):
    """ A generator form to be called as a view
    """

    buttons = (
        deform.Button('generate', _(u'Generate content')),
        deform.Button('cancel', _(u'Cancel')))

    success_message = _(u"Your content has been generated.")

    def __init__(self, context, request):
        super(GeneratorView, self).__init__(context, request)
        self.schema_factory = lambda: make_generator_schema(Generator())

    def _convert_factories(self, appstruct):
        _map = {}
        for klass in Generator().factories.keys():
            od = object_description(klass)
            _map[od] = klass

        for k in ['root_types', 'content_types']:
            appstruct[k] = [_map[x] for x in appstruct[k]]

    def generate_success(self, appstruct):
        appstruct.pop('csrf_token', None)
        self._convert_factories(appstruct)
        generator = Generator(**appstruct)
        count = generator.generate(self.context)
        self.request.session.flash(_("${count} items generated",
                                     mapping={'count':count}))


def includeme(config):  # pragma: nocover
    config.add_view(GeneratorView,
                    name='contentgenerator',
                    permission='add',
                    renderer='kotti:templates/edit/simpleform.pt'
                    )
