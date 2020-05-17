# coding:utf-8
import autopep8,os,argparse,subprocess

class Parserpep8():
    def __init__(self):
        self.args = self.parserPep8()
        self.JudgeMethod = (None,None)
        self.JudgeFixOrCheck()
        print('exmethod',self.JudgeMethod)
        self.ExMethod()

    '''
    command: 
    python CodeToPep8.py --check filename
    python CodeToPep8.py --check all
    python CodeToPep8.py --fix filename
    python CodeToPep8.py --fix all
    '''
    def parserPep8(self):
        parser = argparse.ArgumentParser(prog='myprogram', description='choose funciton')
        parser.add_argument('--fix', help='Choose filename or all')
        parser.add_argument('--check', help='choose filename or all')
        args = parser.parse_args()
        return vars(args)

    def JudgeFixOrCheck(self):
        if self.args['check']:
            self.JudgeMethod=('check',self.args['check'])
        elif self.args['fix']:
            self.JudgeMethod=('fix',self.args['fix'])
        else:
            return False

    def ExMethod(self):
        if self.JudgeMethod[0] == 'check':
            if self.JudgeMethod[1] == 'all':
                print('当前正在对此文件夹进行检查')
                self.check_all_file_pep8()
            else:
                print('当前正在对%s文件进行检查' % self.JudgeMethod[1])
                self.check_file_pep8(self.JudgeMethod[1])
        elif self.JudgeMethod[0] == 'fix':
            if self.JudgeMethod[1] == 'all':
                print('当前正在对xxx文件夹进行修复' % self.JudgeMethod[1])
                self.fix_all_file_pep8()
            else:
                print('当前正在对xxx文件进行修复' % self.JudgeMethod[1])
                self.fix_file_pep8(self.JudgeMethod[1])
        else:
            return False

    def check_file_pep8(self,FileName):
        if os.path.isfile(FileName):
            result=subprocess.getoutput('autopep8 -v %s' % FileName )
            CharCount,IssueCount=result.count('--->'),result.count('issue')
            if CharCount <= IssueCount:
                print('此文件共有 %s 处不规范问题'% CharCount-1)
            elif CharCount > IssueCount:
                print('此文件共有 %s 处不规范问题'% IssueCount)
        else:
            print ('当前文件路径不存在')

    def check_all_file_pep8(self):
        AllIssueCount=0
        for i in os.listdir(os.getcwd()):
            if i[-3:] == '.py':
                result=subprocess.getoutput('autopep8 -v %s' % i)
                CharCount, IssueCount = result.count('--->'), result.count('issue')
                if CharCount <= IssueCount:
                    AllIssueCount = AllIssueCount + CharCount -1
                elif CharCount > IssueCount:
                    AllIssueCount = AllIssueCount + IssueCount
        print('此文件夹共有 %s 处不规范问题' % AllIssueCount)

    def fix_file_pep8(self,FileName):
        if os.path.isfile(FileName):
            subprocess.getoutput('autopep8 --in-place --aggressive --aggressive --aggressive %s' % FileName)
        else:
            print('当前文件路径不存在')

    def fix_all_file_pep8(self):
        subprocess.getoutput('autopep8 --in-place --aggressive --aggressive --aggressive -r %s' % os.getcwd())


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

