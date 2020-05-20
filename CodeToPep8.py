# coding:utf-8
import autopep8
import os
import argparse
import subprocess
from os import listdir
from os.path import isfile, join


class ClassSource(object):
    def __init__(self):
        pass

    def check_result(self, FileName):
        return subprocess.run(
            'autopep8 -v %s' %
            FileName,
            shell=True,
            stdout=subprocess.PIPE)

    def fix_result(self, FileName):
        return subprocess.run(
            'autopep8 --in-place --aggressive --aggressive --aggressive %s' %
            FileName, shell=True)

    def fix_all_result(self, DirName):
        return subprocess.run(
            'autopep8 --in-place --aggressive --aggressive --aggressive -r %s' %
            DirName, shell=True)

    def list_all_files(self, file_path):
        return [i for i in listdir(file_path) if isfile(join(file_path, i))]

    def all_pyfile(self):
        result = []
        for maindir, subdir, file_name_list in os.walk(os.getcwd()):
            result.extend([os.path.join(maindir, filename)
                           for filename in file_name_list])
        return [i for i in result if i[-3:] == '.py']

    def dir_all_pyfile(self, file_path):
        return [i for i in self.list_all_files(file_path) if i[-3:] == '.py']


class ParserPep8(ClassSource):
    def __init__(self):
        self.argparse_init()
        self.parser_pep8()

    '''
    command:
    python CodeToPep8.py -c/--check filename/dir/.
    python CodeToPep8.py -f/--fix filename/dir/.
    '''

    def argparse_init(self):
        self.parser = argparse.ArgumentParser(
            prog='myprogram', description='Choose funciton')
        self.parser.add_argument(
            '-f',
            '--fix',
            action="store",
            dest='fix',
            help='Please enter filename/dir/.')
        self.parser.add_argument(
            '-c',
            '--check',
            dest='check',
            action="store",
            help='Please enter filename/dir/.')

    def parser_pep8(self):
        args = self.parser.parse_args()
        if args.fix:
            self.fix_pep8(args.fix)
        elif args.check:
            self.check_pep8(args.check)
        else:
            self.parser.print_help()

    def check_pep8(self, all_file_name):
        for file_name in all_file_name.split(','):
            if file_name == '.':
                for py_file in self.all_pyfile():
                    self.check_result(py_file)
                break
            elif os.path.isfile(file_name):
                self.check_result(file_name)
            elif os.path.isdir(file_name):
                for dir_file_name in self.dir_all_pyfile(file_name):
                    self.check_result(join(file_name, dir_file_name))
            else:
                print('No such file or directory: %s' % file_name)

    def fix_pep8(self, all_file_name):
        for file_name in all_file_name.split(','):
            if file_name == '.':
                print('当前正在对文件夹进行修复，所需时间根据文件大小与文件夹迭代程度，请耐心等待！')
                self.fix_all_result(os.getcwd())
                print('SUCCESS')
                break
            elif os.path.isfile(file_name):
                print('当前正在对 %s 文件进行修复' % file_name)
                self.fix_result(file_name)
                print('SUCCESS')
            elif os.path.isdir(file_name):
                print('当前正在对 %s 文件夹进行修复' % file_name)
                for dir_file_name in self.dir_all_pyfile(file_name):
                    self.fix_result(join(file_name, dir_file_name))
                print('SUCCESS')
            else:
                print('No such file or directory: %s' % file_name)

if __name__ == '__main__':
    ParserPep8()
