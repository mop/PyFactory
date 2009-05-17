# =========================================================================== 
# Exceptions
# =========================================================================== 
class FactoryException(Exception):
    """
    An instance of this exception class is thrown, if an error occured. 

    msg -- the message, which should be printed as the representation of the
    object
    """
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg
    
# =========================================================================== 
# Core
# =========================================================================== 

class FactoryBuilder(object):
    """
    The main class of the module. The single FactoryBuilder object contains all
    FactoryElement-instances and is responsible for accepting user-requests for
    factories. The actual creation-work is delegated to the FactoryBuilder
    objects.
    """
    def __init__(self):
        self._elements = []

    def _add_factory(self, element):
        """
        Adds the given element to the list of available factories.

        element -- An instance of FactoryElement
        """
        self._elements.append(element)

    def _find_factory(self, name):
        """
        Tries to find a factory with the given name. If no such factory exists
        a FactoryException is thrown.

        name -- a string which represents the name of the FactoryElement object
        which should be returned by this method.
        returns -- the first factory is returned, whose name matches with the
        given name.
        """
        elems = filter(lambda e: e.name == name, self._elements)
        if not elems:
            raise FactoryException("Factory :name doesn't exists!".format({
                'name': name
            }))
        return elems[0]

    def build(self, name):
        """
        Builds (no save!) an object using the Factory with the given name. 

        name -- the name of the factory, which should be used to build the
        object.
        returns -- the created object.
        """
        factory_object = self._find_factory(name)
        return factory_object.build()

    def attributes_for(self, name):
        """
        Returns a dictionary with the attributes for the object the Factory
        with the given name would have created otherwise.

        name -- the name of the factory, whose attributes should be returned
        returns -- a dictionary with all the attributes for the object, which
        would have been created, is returned.
        """
        factory_object = self._find_factory(name)
        return factory_object.attributes_for()

    def create(self, name):
        """
        Creates (saves!) an object using the Factory with the given name.

        name -- the name of the factory, which should be used to create the
        object.
        returns -- a saved object.
        """
        factory_object = self._find_factory(name)
        return factory_object.create()
        
# The global Factory-object
Factory = FactoryBuilder()

class FactoryElement(object):
    """
    This class represents one factory, which holds the metadata, the user
    priveded when defining the factory. It's responsibility is to actually
    create the object using the meta-information of the user.
    """
    def __init__(self, name, klass, attrs):
        self.name       = name
        self.klass      = klass
        self.attributes = attrs

    @property
    def klass_name(self):
        """
        Returns the name of the model-class, without the module-part
        """
        return self.klass.split('.')[-1]

    def _import_module(self):
        """
        Imports the module for the model-class.

        returns --- The model is returned if found, otherwise None is
        returned.
        """
        modules = self.klass.split('.')[:-1]
        if not modules:
            return None
        return __import__('.'.join(modules), globals(), locals(), [''])

    def _fetch_class(self):
        """
        Tries to fetch the model-class by searching through modules.

        returns -- The model-class is returned.
        """
        module = self._import_module()
        if module:
            return getattr(module, self.klass_name)
        return globals[self.klass_name]

    def _filter_attributes(self, vals):
        """
        Substitutes special attributes (FactoryAttribute) with their actual
        values and returns a tuple with the new (key, value) pair.

        vals -- A tuple in the form (key, value) representing a single
        attribute of the model.
        returns -- A tuple in the form (key, value)
        """
        key = vals[0]
        val = vals[1]
        if not isinstance(val, FactoryAttribute):
            return (key, val)
        return (key, val(self._method))

    def build(self):
        """
        Builds the object using the given meta-data.

        returns -- the built object is returned.
        """
        klass = self._fetch_class()
        return klass(**self.attributes_for('build'))

    def attributes_for(self, method='attributes_for'):
        """
        Returns an attribute-dictionary for the model-class.

        returns -- A dictionary containing all attributes of the class is
        returned.
        """
        self._method = method
        return dict(map(self._filter_attributes, self.attributes.items()))

    def create(self):
        """
        Creates the object using the given meta-data.

        returns -- the created object is returned.
        """
        klass = self._fetch_class()
        obj = klass(**self.attributes_for('create'))
        obj.save()
        return obj
        
class FactoryInitializer(type):
    """
    A metaclass, which is responsible for fetching the metadata on the
    FactoryObject-classes and creating FactoryElement-instances and adding them
    to the global factory object.
    """
    def __init__(cls, name, bases, dict):
        if 'Meta' in dict:
            attrs = cls._collect_attributes(dict)
            Factory._add_factory(FactoryElement(
                dict['Meta'].name, 
                dict['Meta'].klass,
                attrs
            ))
    
    def _collect_attributes(cls, d):
        """
        Returns a dictionary with all key-value pairs in the 'Elements'
        nested-class.
        """
        if 'Elements' not in d:
            return {}

        keys = filter(
            lambda k: not k.startswith('__'), 
            d['Elements'].__dict__.keys()
        )
        vals = map(lambda k: (k, getattr(d['Elements'], k)), keys)
        return dict(vals)

        
class FactoryObject(object):
    """
    Derive your actual Factory-classes from this class, which simply injects
    the FactoryInitializer as Metaclass.
    """
    __metaclass__ = FactoryInitializer

# =================================================================
# Attributes
# =================================================================

class FactoryAttribute(object):
    pass
        
class Generator(FactoryAttribute):
    """
    Creates a unique ID and calls the given callback function with it.
    The result of the callback-function is the new value of the specified
    attribute.
    """
    def __init__(self, callback):
        self._callback = callback
    
    def __call__(self, type):
        return self._callback(UniqueIDGenerator.generate())

class Foreign(FactoryAttribute):
    """
    Allows to use a Factory for the attribute. The name of the Factory to use
    must be given to the constructor of the object.
    """
    def __init__(self, factory_name):
        self.factory_name = factory_name

    def __call__(self, type):
        method = getattr(Factory, type)
        # e.g. Factory.build('user')
        return method(self.factory_name)
    
class UniqueIDGenerator(object):
    """
    Helperclass which creates unique integer-ids by simply incrementing a
    global variable.
    """
    @classmethod
    def generate(cls):
        if 'id' not in cls.__dict__:
            cls.id = 0
        cls.id += 1
        return cls.id
        
