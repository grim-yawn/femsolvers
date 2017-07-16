from dolfin import FunctionSpace
from ufl import Mesh

from logger import get_logger


class FiniteElementTypeNotFound(Exception):
    """
    Exception that will be raised when one try to use unknown finite element
    """

    def __init__(self, fe_type: str):
        """
        Constructor from fe_type
        :param fe_type: type of finite element that hasn't been founded
        """
        self.fe_type = fe_type

    def __str__(self) -> str:
        return 'Finite element with type: "{type}" not found'.format(type=self.fe_type)


def create_function_space(mesh: Mesh, finite_element: dict) -> FunctionSpace:
    """
    Creates function space from finite element type and mesh
    :param finite_element: Config that specifies finite element
    :raise FiniteElementTypeNotFound if there is no finite element with type that was declared in config
    :return: function space
    """

    if finite_element['type'] == 'lagrange':
        get_logger(__name__).info('Using finite element: P-{kind}'.format(kind=finite_element['kind']))
        return FunctionSpace(mesh, 'P', finite_element['kind'])
    else:
        raise FiniteElementTypeNotFound(finite_element['type'])
