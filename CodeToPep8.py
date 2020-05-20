# coding:utf-8
import autopep8
import os
import argparse
import subprocess
from os import listdir
from os.path import isfile,join


class source(object):
    def __init__(self):
        pass

    def check_result(self,FileName):
        return subprocess.run('autopep8 -v %s' % FileName,shell=True,stdout=subprocess.PIPE)

    def fix_result(self,FileName):
        return subprocess.run('autopep8 --in-place --aggressive --aggressive --aggressive %s' %
                FileName,shell=True)

    def fix_all_result(self,DirName):
        return subprocess.run('autopep8 --in-place --aggressive --aggressive --aggressive %s' %
                DirName,shell=True)

    def list_all_files(self,file_path):
        return [f for f in listdir(file_path) if isfile(join(file_path, f))]

    def list_all(self, file_path):
        return listdir(file_path)

    def all_pyfile(self):
        result=[]
        for maindir, subdir, file_name_list in os.walk(os.getcwd()):
            result.extend([os.path.join(maindir, filename) for filename in file_name_list])
        return  [i for i in result  if i[-3:] == '.py']

    def dir_all_pyfile(self,file_path):
        return [i for i in self.list_all_files(file_path) if i[-3:] == '.py']


class Parserpep8(source):
    def __init__(self):
        self.ArgparseInit()
        self.ParserPep8()

    '''
    command:
    python CodeToPep8.py -c/--check filename/dir/.
    python CodeToPep8.py -f/--fix filename/dir/.
    '''

    def ArgparseInit(self):
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

    def ParserPep8(self):
        args = self.parser.parse_args()
        if args.fix:
            self.fix_pep8(args.fix)
        elif args.check:
            self.check_pep8(args.check)
        else:
            self.parser.print_help()

    def check_pep8(self, FileName):
        #check more file or dir
        for str_file_name in FileName.split(','):
            #check project all python file
            if str_file_name=='.':
                for i in self.all_pyfile():
                    self.check_result(i)
                break
            # check a python file
            elif os.path.isfile(str_file_name):
                self.check_result(str_file_name)
            #check a dir
            elif os.path.isdir(str_file_name):
                for dir_file_name in self.dir_all_pyfile(str_file_name):
                    self.check_result(join(str_file_name, dir_file_name))
            else:
                print('当前文件路径不存在')

    def fix_pep8(self, FileName):
        for str_file_name in FileName.split(','):
            if str_file_name=='.':
                print('当前正在对文件夹进行修复，所需时间根据文件大小与文件夹迭代程度，请耐心等待！')
                self.fix_all_result(os.getcwd())
                print('SUCCESS')
                break
            elif os.path.isfile(str_file_name):
                print('当前正在对 %s 文件进行修复' % str_file_name)
                self.fix_result(str_file_name)
                print('SUCCESS')
            elif os.path.isdir(str_file_name):
                print('当前正在对 %s 文件夹进行修复' % str_file_name)
                self.fix_all_result(str_file_name)
                print('SUCCESS')
            else:
                print('文件路径不存在')

#####################################################

    def check_file_pep8(self, FileName, JudgeDetail):
        if os.path.isfile(FileName):
            print('当前正在对%s文件进行检查' % FileName)
            result = subprocess.getoutput('autopep8 -v %s' % FileName)
            if JudgeDetail:
                print(result)
            else:
                CharCount, IssueCount = result.count(
                    '--->'), result.count('issue(s) to fix')
                if CharCount <= IssueCount:
                    print('%s 文件有 %s 处不规范问题' % (FileName, CharCount - 1))
                elif CharCount > IssueCount:
                    print('%s 文件有 %s 处不规范问题' % (FileName, IssueCount))
                elif IssueCount == 0:
                    print('此文件无不规范的地方')
        else:
            print('当前文件路径不存在')


    def check_all_file_pep8(self, JudgeDetail):
        AllIssueCount = 0
        print('当前正在对文件夹进行检查，所需时间根据文件大小与文件夹迭代程度，请耐心等待！')
        for i in self.AllPath():
            result = subprocess.getoutput('autopep8 -v %s' % i)
            CharCount, IssueCount = result.count(
                '--->'), result.count('issue(s) to fix')
            if CharCount <= IssueCount:
                AllIssueCount = AllIssueCount + CharCount - 1
                print('%s 有 %s 处不规范问题' % (i, CharCount - 1))
            elif CharCount > IssueCount:
                AllIssueCount = AllIssueCount + IssueCount
                print('%s 有 %s 处不规范问题' % (i, IssueCount))
        print('此 %s 文件夹共有 %s 处不规范问题' % (os.getcwd(), AllIssueCount))

    def fix_file_pep8(self, FileName, JudgeDetail):
        if os.path.isfile(FileName):
            self.check_file_pep8(FileName, JudgeDetail)
            subprocess.getoutput(
                'autopep8 --in-place --aggressive --aggressive --aggressive %s' %
                FileName)
            print('修复后，', end='')
            self.check_file_pep8(FileName, JudgeDetail)
        else:
            print('当前文件路径不存在')

    def fix_all_file_pep8(self, JudgeDetail):
        print('当前正在对文件进行修复，所需时间根据文件大小与文件夹迭代程度，请耐心等待！')
        subprocess.getoutput(
            'autopep8 --in-place --aggressive --aggressive --aggressive -r %s' %
            os.getcwd())
        print('已对此文件夹所有python文件进行规范！')


if __name__ == '__main__':
    Parserpep8()
    # a=source()
    # print(a.all_pyfile())