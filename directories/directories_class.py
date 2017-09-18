import logging
import os
from yaml import safe_load
import readline  # pyreadline on Windows
import persistentdatatools as pdt
__author__ = 'Benjamin P. Trachtenberg'
__copyright__ = "Copyright (c) 2017, Benjamin P. Trachtenberg"
__credits__ = 'Benjamin P. Trachtenberg'
__license__ = ''
__status__ = 'prod'
__version_info__ = (1, 0, 3, __status__)
__version__ = '.'.join(map(str, __version_info__))
__maintainer__ = 'Benjamin P. Trachtenberg'
__email__ = 'e_ben_75-python@yahoo.com'

LOGGER = logging.getLogger(__name__)


class Directories(object):
    """
    Class to hold directory structure

    The base directories this has are the following
    Data/
    Input/
    Output/
    Logs/

    They are created in the base directory you give the class I would recommend deriving it from one of the following
    depending on if you are compiling the script:

    os.path.dirname(os.path.realpath(sys.argv[0]))
    os.path.dirname(os.path.realpath(__file__))

    !!!  config.yml !!!
    You can change behavior by modifying config.yml in the Data directory, the only directory
    you can not change is the Data directory

    You can also add more directories adding the add_directories kwarg, and giving it a dict of values

    """
    def __init__(self, base_dir, **kwargs):
        self.base_dir = base_dir
        self.logging_level = logging.WARNING
        self.data_dir = os.path.join(self.base_dir, 'Data')
        pdt.verify_directory('Data', self.base_dir, directory_create=True)
        try:
            self.yml_config_data = open(os.path.join(self.data_dir, 'config.yml'))

        except FileNotFoundError as e:
            self.__create_config_yml_file()
            self.yml_config_data = open(os.path.join(self.data_dir, 'config.yml'))

        self.dir_config = safe_load(self.yml_config_data).get('config')

        self.input_dir = self.__set_directory('input_directory', 'Input')

        self.output_dir = self.__set_directory('output_directory', 'Output')

        self.logging_dir = self.__set_directory('logging_directory', 'Logs')

        if kwargs.get('add_directories'):
            if isinstance(kwargs.get('add_directories'), dict):
                for dir_key, dir_value in kwargs.get('add_directories').items():
                    setattr(Directories, dir_key, self.__set_directory(dir_key, dir_value))

            else:
                error = 'The add_directories kwarg takes a dict, ' \
                        'you entered a {}'.format(type(kwargs.get('add_directories')))
                LOGGER.critical(error)
                raise TypeError(error)

        # This sets the default logging level
        if self.dir_config.get('logging_level'):
            self.set_logging_level(self.dir_config.get('logging_level'))

    def __str__(self):
        """
        Method to return object instance name
        :return:
            The object instance name

        """
        return '<class {}>'.format('Directories')

    def set_logging_level(self, level):
        """
        Method to set the logging level, using the defaults in the logging module
        :return:
            None

        """
        if str(level) == '1':
            self.logging_level = logging.DEBUG
        elif str(level) == '2':
            self.logging_level = logging.INFO
        elif str(level) == '3':
            self.logging_level = logging.WARNING
        elif str(level) == '4':
            self.logging_level = logging.ERROR
        elif str(level) == '5':
            self.logging_level = logging.CRITICAL

    def get_logging_level(self):
        """
        Method to get the logging level
        :return:
            Logging level

        """
        return self.logging_level

    def __set_directory(self, yml_key, default_dir):
        """
        Method to create a default directory, or use the yml config file
        :param yml_key: The key in the yml file to use
        :param default_dir: The default directory
        :return:
            The "Created" directory

        """
        if self.dir_config.get(yml_key):
            temp_dir = self.dir_config.get(yml_key)
            if not os.path.isdir(temp_dir):
                LOGGER.critical('Could not find directory stated in config.yml file {}'.format(temp_dir))
                exit('Bad directory {}'.format(temp_dir))

        else:
            temp_dir = os.path.join(self.base_dir, default_dir)
            pdt.verify_directory(default_dir, self.base_dir, directory_create=True)

        return temp_dir

    def __tab_completer(self, starts_with_text, state):
        """
        Method for the callback function of readline
        :param starts_with_text: Begin text
        :param state: Found or not
        :return:
            A state

        """
        options = [x for x in self.__create_file_list() if x.startswith(starts_with_text)]
        try:
            return options[state]
        except IndexError:
            return None

    def __create_file_list(self):
        """
        Method to create a list of files in an input directory
        :return:
            A list of files

        """
        return pdt.list_files_in_directory(self.input_dir)

    def __create_config_yml_file(self):
        """
        Method to create a config.yml if one does not exist
        :return:
            None

        """
        temp_list = list()
        temp_list.append('---  # Version 1.0.0')
        temp_list.append('config:')
        temp_list.append('    input_directory: ')
        temp_list.append('    output_directory: ')
        temp_list.append('    logging_directory: ')
        temp_list.append('    logging_level: ')
        temp_list.append('# Logging level is 3 by default, highest is 1 lowest is 5')
        pdt.list_to_file(temp_list, 'config.yml', self.data_dir)

    def get_tab_completion(self):
        """
        Method to have tab complete for input files
        :return:
            A readline instance

        """
        readline.set_completer(self.__tab_completer)
        return readline.parse_and_bind("tab: complete")

    def set_output_dir_folder(self, output_folder):
        """
        Method to send output to a folder in the output directory
        :param output_folder: The name of the folder
        :return:
            None

        """
        if isinstance(output_folder, str):
            pdt.verify_directory(output_folder, self.output_dir, directory_create=True)
            self.output_dir = os.path.join(self.output_dir, output_folder)

        else:
            error = 'A string is required as a argument for method set_output_dir_folder in class {}'.format(self)
            LOGGER.critical(error)
            raise TypeError(error)

    def get_output_dir(self):
        """
        Method to get the output directory
        :return:
            The output directory
        """
        return self.output_dir

    def get_input_dir(self):
        """
        Method to get the input directory
        :return:
            The input directory
        """
        return self.input_dir

    def get_logging_dir(self):
        """
        Method to get the logging directory
        :return:
            The logging directory
        """
        return self.logging_dir
