from factory import Factory, FactoryException, FactoryBuilder, FactoryObject, \
                    FactoryAttribute, Foreign, Generator, UniqueIDGenerator
save_functions = {
    'django-orm': 'save',
    'appengine':  'put'
}
type = 'django-orm'

def save_function():
    return save_functions[type]

__all__ = [ 
    'Factory',
    'FactoryException',
    'FactoryObject',
    'FactoryAttribute',
    'Foreign',
    'Generator',
    'UniqueIDGenerator',
    'type'
]
