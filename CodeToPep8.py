# coding:utf-8
import autopep8
import os
import argparse
import subprocess


class Parserpep8():
    def __init__(self):
        self.args = self.parserPep8()
        self.JudgeMethod = []
        self.JudgeFixOrCheck()
        self.ExMethod()

    '''
    command:
    python CodeToPep8.py --check filename
    python CodeToPep8.py --check all
    python CodeToPep8.py --fix filename
    python CodeToPep8.py --fix all
    '''

    def parserPep8(self):
        self.parser = argparse.ArgumentParser(
            prog='myprogram', description='choose funciton')
        self.parser.add_argument(
            '--fix',
            action="store",
            help='Choose filename or all')
        self.parser.add_argument(
            '--check',
            action="store",
            help='choose filename or all')
        self.parser.add_argument(
            '-d',
            '--detail',
            dest='detail',
            action='store_true',
            help='')
        args = self.parser.parse_args()
        return vars(args)

    def JudgeFixOrCheck(self):
        try:
            if self.args['check']:
                self.JudgeMethod = ['check', self.args['check']]
            elif self.args['fix']:
                self.JudgeMethod = ['fix', self.args['fix']]
            else:
                self.parser.print_help()
            if self.args['detail']:
                self.JudgeMethod.append(True)
            else:
                self.JudgeMethod.append(False)
        except KeyError:
            self.parser.print_help()

    def ExMethod(self):
        if self.JudgeMethod[0] == 'check':
            if self.JudgeMethod[1] == 'all':
                print('当前正在对此文件夹进行检查')
                self.check_all_file_pep8(self.JudgeMethod[2])
            else:
                print('当前正在对%s文件进行检查' % self.JudgeMethod[1])
                self.check_file_pep8(self.JudgeMethod[1], self.JudgeMethod[2])
        elif self.JudgeMethod[0] == 'fix':
            if self.JudgeMethod[1] == 'all':
                print('当前正在对此文件夹进行修复')
                self.fix_all_file_pep8(self.JudgeMethod[2])
            else:
                print('当前正在对%s文件进行修复' % self.JudgeMethod[1])
                self.fix_file_pep8(self.JudgeMethod[1], self.JudgeMethod[2])
        else:
            return False

    def check_file_pep8(self, FileName, JudgeDetail):
        if os.path.isfile(FileName):
            result = subprocess.getoutput('autopep8 -v %s' % FileName)
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

    def AllPath(self):
        result = []
        LisPath = []
        for maindir, subdir, file_name_list in os.walk(os.getcwd()):
            for filename in file_name_list:
                apath = os.path.join(maindir, filename)
                result.append(apath)
        for i in result:
            if i[-3:] == '.py':
                LisPath.append(i)
        return LisPath

    def check_all_file_pep8(self, JudgeDetail):
        AllIssueCount = 0
        print('当前正在对文件进行检查，所需时间根据文件大小与文件夹迭代程度，请耐心等待！')
        for i in self.AllPath():
            result = subprocess.getoutput('autopep8 -v %s' % i)
            CharCount, IssueCount = result.count(
                '--->'), result.count('issue(s) to fix')
            if CharCount <= IssueCount:
                AllIssueCount = AllIssueCount + CharCount - 1
                print('%s 有 %s 处不规范问题' % (i, CharCount - 1))
                # if CharCount > 2:
                #     print('%s 有 %s 处不规范问题' % (i, CharCount - 1))
            elif CharCount > IssueCount:
                AllIssueCount = AllIssueCount + IssueCount
                print('%s 有 %s 处不规范问题' % (i, IssueCount))
                # if IssueCount > 1:
                #     print('%s 有 %s 处不规范问题' % (i, IssueCount))
        print('此 %s 文件夹共有 %s 处不规范问题' % (os.getcwd(), AllIssueCount))

        # for i in os.listdir(os.getcwd()):
        #     if i[-3:] == '.py':
        #         result = subprocess.getoutput('autopep8 -v %s' % i)
        #         CharCount, IssueCount = result.count(
        #             '--->'), result.count('issue(s) to fix')
        #         if CharCount <= IssueCount:
        #             AllIssueCount = AllIssueCount + CharCount - 1
        #             print('%s 有 %s 处不规范问题' % (i, CharCount - 1))
        #         elif CharCount > IssueCount:
        #             AllIssueCount = AllIssueCount + IssueCount
        #             print('%s 有 %s 处不规范问题' % (i, IssueCount))
        # print('此 %s 文件夹共有 %s 处不规范问题' % (os.getcwd(), AllIssueCount))

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


if __name__ == '__main__':
    Parserpep8()

# class Optionst(object):
#     def __init__(self):
#         self.in_place = True
#         self.pep8_passes = -1
#         self.jobs = 0
#         self.ignore = []
#         self.diff = None
#         self.aggressive = 2
#         self.max_line_length = 79
#
#
# options = Optionst()
# file = ("case.py")
#
# autopep8.fix_file(file, options)
