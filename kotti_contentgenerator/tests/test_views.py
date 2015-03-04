from kotti.testing import DummyRequest


class TestGeneratorView:

    def make_one(self):
        from kotti_contentgenerator.views import GeneratorView
        return GeneratorView({}, DummyRequest())

    def test_it(self, db_session, monkeypatch):
        from kotti.resources import Document, File, Image
        from kotti_contentgenerator.generator import default_factories

        params = {}

        class DummyGenerator:
            def __init__(self, **kwargs):
                self.factories = default_factories
                params.update(kwargs)

            def generate(self, root):
                return 100

        monkeypatch.setattr(
            'kotti_contentgenerator.generator.Generator',
            DummyGenerator)

        view = self.make_one()
        appstruct = {'content_types': set([u'class kotti.resources.Document',
                                           u'class kotti.resources.File',
                                           u'class kotti.resources.Image']),
                     'depth': 2,
                     'root_types': set([u'class kotti.resources.Document']),
                     'seed': 1,
                     'sub_level': 10,
                     'top_level': 10,
                     'users': 10}
        view.generate_success(appstruct)

        assert set(params['content_types']) == set([Document, File, Image])
        assert params['root_types'] == [Document]
