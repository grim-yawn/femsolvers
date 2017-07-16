import os
import sys

from dolfin.cpp.io import File

from boundary_conditions.factory import create_dirichlet
from config import parser
from function_spaces.factory import create_function_space
from logger import get_logger, configure_logger
from meshes.factory import create_mesh
from solvers.factory import create_solver


def get_parameters_file_path() -> str:
    """
    Get path to config file path from commandline args or return default
    :return:
    """
    logger = get_logger(__name__)

    if len(sys.argv) == 1:
        default_filename = 'config.json'
        root = os.path.dirname(os.path.abspath(__file__))
        parameters_file = os.path.join(root, default_filename)

        logger.info('Using default "%(params)s" config file', {'params': parameters_file})

        return parameters_file

    parameters_file = os.path.abspath(sys.argv[1])

    logger.info('Using "%(params)s" config file', {'params': parameters_file})

    return parameters_file


class Runner:
    """
    Class that creates solver and passes config to it
    """

    def __init__(self):
        """
        Constructor that parses commandline args and provide default config if
        there is not other
        """
        configure_logger()
        parameters_file = get_parameters_file_path()

        self._config = parser.parse(parameters_file)
        get_logger(__name__).info('Config:\n%(config)s', {'config': self._config})

    def run(self):
        """
        Creates solver and passes config to it
        :raises SolverTypeNotFound when solver type in config invalid
        """
        mesh = create_mesh(self._config['geometry'])
        function_space = create_function_space(mesh, self._config['finite_element'])

        bcs = create_dirichlet(function_space, self._config['boundary_conditions']['dirichlet'])
        solver = create_solver(self._config['solver']['type'])

        solution = solver(function_space, bcs)

        vtkfile = File(os.path.join(self._config['solver']['output']['root'], 'result.pvd'))
        vtkfile << solution


if __name__ == '__main__':
    runner = Runner()
    runner.run()
