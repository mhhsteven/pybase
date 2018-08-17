'''
Created on 2018年08月16日

@author: Administrator
'''

import os
import re

#接口类名
interFaceDict = {}
allInterfaceDict = {}

'''
处理import代码
'''
def findImport(lineStr):
    importLineStr = lineStr.strip()
    if importLineStr.startswith('import'):
        isMgzfServiceApi = re.match(r'(.*)com.mgzf.(.*).service.api.(.*)', importLineStr)
        if isMgzfServiceApi:
            findMgzfService(importLineStr)
        isMogoroomServiceApi = re.match(r'(.*)com.mogoroom.service.(.*)', importLineStr)
        if isMogoroomServiceApi:
            findMogoroomService(importLineStr)


'''
mgzf的service接口处理成一个dict
com.mgzf.loan.service.api.cpay.ILoanCreditPayApplyService;
'''
def findMgzfService(lineStr):
    mgzfPackage = re.search(r'com.mgzf.(.*).service.api.(.*);', lineStr).group()
    className = mgzfPackage[0:len(mgzfPackage) - 1]
    classNameList = className.split('.')
    module = classNameList[2]
    interfaceName = classNameList[-1]
    # print('module is [%s], class is [%s], interface is [%s]' % (module, className, interfaceName))
    saveInterface(module, className, interfaceName)


'''
mogoroom的service接口处理成一个dict
com.mogoroom.service.bill.IBillService;
'''
def findMogoroomService(lineStr):
    mogoroomPackage = re.search(r'com.mogoroom.service.(.*);', lineStr).group()
    className = mogoroomPackage[0:len(mogoroomPackage) - 1]
    classNameList = className.split('.')
    module = classNameList[3]
    interfaceName = classNameList[-1]
    # print('module is [%s], class is [%s], interface is [%s]' % (module, className, interfaceName))
    saveInterface(module, className, interfaceName)


'''
保存接口的dict
'''
def saveInterface(module, className, interfaceName):
    if (interfaceName not in interFaceDict):
        interFaceDetail = {'className': className, 'module': module}
        interFaceDict[interfaceName] = interFaceDetail


'''
@Autowired
private IBillAccountMappingService billAccountMappingService;
'''
def findAutowire(lineStr, interfaceParamDict):
    autoWireLineStr = lineStr.strip()
    autoWireLineStr = autoWireLineStr[0:len(autoWireLineStr) - 1]
    autoWireLineStr = re.split(r'\s+', autoWireLineStr)
    if len(autoWireLineStr) > 1:
        interfaceName = autoWireLineStr[-2]
        interfaceParamName = autoWireLineStr[-1]
        if len(interfaceName) > 0 and len(interfaceParamName) > 0:
            # print('%s, %s' % (interfaceName, interfaceParamName))
            interfaceParamDict[interfaceParamName] = interfaceName


'''
处理接口方法
'''
def findMethod(lineStr, interfaceParamDict):
    for interfaceParamName in interfaceParamDict:
        methodName = interfaceParamName + '.'
        if methodName in lineStr:
            methodLine = lineStr.strip()
            if(not methodLine.startswith("//") and not methodLine.startswith("/*")):
                methodindex = methodLine.index(methodName) + len(methodName)
                #print(methodName, lineStr)
                endIndex = methodLine.index('(', methodindex)
                interfaceName = interfaceParamDict[interfaceParamName]
                if interfaceName in interFaceDict:
                    interface = interFaceDict[interfaceName]
                    interfaceMethod = interface['className'] + '.' + methodLine[methodindex:endIndex]
                    if interfaceMethod not in allInterfaceDict:
                        allInterfaceDict[interfaceMethod] = interface['module']


def listAllFile(path):
    for file in os.listdir(path):
        tempPath = os.path.join(path, file)
        if os.path.isdir(tempPath):
            listAllFile(tempPath)
        else:
            if tempPath.endswith('.java'):
                readFile(tempPath)


def readFile(path):
    fileHandle = open(path, encoding='gb18030', errors='ignore')
    lineList = fileHandle.readlines()
    isAutowire = False
    # 接口变量名和接口类名
    interfaceParamDict = {}
    for line in lineList:
        findImport(line)
        if isAutowire:
            findAutowire(line, interfaceParamDict)
            isAutowire = False
        isAutowire = '@Autowired' in line or '@Resource' in line
        findMethod(line, interfaceParamDict)


rootPath = 'D:\\IdeaWorkspaceAll\\mgzf-fina'

# print(interFaceDict)
# print(interfaceParamDict)
# print(allInterfaceDict)
listAllFile(rootPath)

import xlwt

wbk = xlwt.Workbook()

sheetDict = {}

for interface in allInterfaceDict:
    module = allInterfaceDict[interface]
    sheet = None
    try:
        sheet = wbk.get_sheet(module)
    except Exception as e:
        sheet = wbk.add_sheet(module)
    row = None
    if sheet not in sheetDict:
        row = 0
    else:
        row = sheetDict[sheet]
    sheet.write(row, 0, interface)
    row = row + 1
    sheetDict[sheet] = row

wbk.save('E:\\极光依赖的Service模块接口汇总.xls')