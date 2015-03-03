from kotti.security import get_principals
from kotti_contentgenerator.generator import Generator
import pytest


class TestUtils:

    def test_infinite_list_as_stream(self):
        from kotti_contentgenerator.generator import infinite_list

        z = infinite_list(['a', 'b', 'c'])
        assert [z.next() for i in range(5)] == ['a', 'b', 'c', 'a', 'b']

        z = infinite_list(['a'])
        assert [z.next() for i in range(5)] == ['a', 'a', 'a', 'a', 'a']

        z = infinite_list([])
        with pytest.raises(IndexError):
            z.next()


class TestGenerator:

    def test_it(self, db_session):
        root = {}
        gen = Generator(1, depth=1, top_level=5, sub_level=1, users=2)
        gen.generate(root)

        principals = get_principals()
        assert len(principals) == 3

        assert principals['stamm.leandra'].email == u'yoel.oconner@botsford.com'

        assert len(root) == 5
        assert root[u'nam-exercitationem'].type_info.name == 'Document'

    def test_depth_2(self, db_session):
        root = {}
        gen = Generator(1, depth=2, top_level=2, sub_level=10, users=2)
        gen.generate(root)
