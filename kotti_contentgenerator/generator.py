from faker import Faker
from kotti.resources import Document
from kotti.resources import File
from kotti.resources import Image
from kotti.resources import DBSession
from kotti.security import Principal
from kotti.security import get_principals
from kotti.security import set_groups


def infinite_list(list_):
    """ return an infinite stream of items from a list

    :param list_: a python list
    """
    i = 0

    while True:
        yield list_[i]
        i = i + 1
        if i == len(list_):
            i = 0


class Generator(object):

    def __init__(self, seed=None, depth=3, top_level=10, sub_level=10,
                 users=10, root_types=(Document,),
                 content_types=(Document, File, Image),
                 factories=None):
        """
        :param seed: a number that will seed the faker
        :param depth: how many levels deep to go
        :param top_level: how many items in the top level
        :param sub_level: how many content items to create per level
        :param users: how many users to create
        :param root_types: content type names of objects to put in root
        :param content_types: a list of content type names to build content from
        :param factories: a mapping of factories for content, mapped by their
                          content type name. This can be used to add new
                          factories

        The default configuration will create 10 root objects, each with 10
        children. These children will also get their own 10 children, down to
        3 levels deep (including the root objects).
        """

        self.faker = Faker()
        self.faker.seed(seed)

        self.depth = depth
        self.top_level = top_level
        self.sub_level = sub_level
        self.users = users
        self.root_types = root_types
        self.content_types = content_types

        self.factories = {
            Document: self._factory_Document,
            File: self._factory_File,
            Image: self._factory_Image,
            Principal: self._factory_Principal,
        }
        self.factories.update(factories or {})

        self.session = DBSession()

    def generate(self, root):
        """ Generate and add the content to the provided root

        To make the process deterministic we iterate over the provided types

        :param root: the object where content will be added
        :result: the number of create objects
        """

        obc = [0]   # total created objects. Using list to avoid enclosure issue
        users = []
        principals = get_principals()

        for i in range(self.users):
            user = self._factory_Principal()
            principals[user.id] = user
            users.append(user)

        users = infinite_list(users)

        # add toplevel content to root
        root_types = infinite_list(self.root_types)
        for i in range(self.top_level):
            obj = self.factories[root_types.next()](users.next())
            root[obj.name] = obj
            obc[0] = obc[0] + 1

        content_types = infinite_list(self.content_types)

        def create_children(parent, level):
            # prevent an infinite loop when no child is addable
            if not [True
                    for x in self.content_types
                    if parent.type_info.name in x.type_info.addable_to]:
                return

            level = level + 1
            if level == self.depth:
                return

            i = 0
            while i < self.sub_level:
                ct = content_types.next()
                if parent.type_info.name not in ct.type_info.addable_to:
                    continue

                obj = self.factories[ct](users.next())
                parent[obj.name] = obj
                obc[0] = obc[0] + 1

                i += 1
                for j in range(self.sub_level):
                    create_children(obj, level)

        level = 0
        for child in root.values():
            create_children(child, level)

        self.session.flush()

        return obc[0]

    def _factory_Document(self, owner=None):
        doc = Document(name=self.faker.slug(),
                       title=self.faker.sentence(),
                       body=u"\n".join(self.faker.sentences(10)))
        self.session.add(doc)
        if owner:
            with self.session.no_autoflush:
                set_groups(owner, doc, ['role:owner'])

        return doc

    def _factory_File(self, owner=None):
        obj = File(name=self.faker.slug(), title=self.faker.sentence())
        self.session.add(obj)
        if owner:
            with self.session.no_autoflush:
                set_groups(owner, obj, ['role:owner'])

        return obj

    def _factory_Image(self, owner=None):
        obj = Image(name=self.faker.slug(), title=self.faker.sentence())
        self.session.add(obj)
        if owner:
            with self.session.no_autoflush:
                set_groups(owner, obj, ['role:owner'])

        return obj

    def _factory_Principal(self):
        """ Construct a principal
        """
        principal = Principal(self.faker.user_name(), email=self.faker.email())
        return principal
