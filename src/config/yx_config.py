#!/usr/bin/python
# -*- coding: UTF-8 -*-

class YxConfig:
    """云效配置类"""
    
    # 云效用户名称
    userName = 'dt_1176306168'
    # 云效用户密码
    password = '62483768dd'
    
    # 自动化标注方式
    # autoType: 自动化类型标注模式
    # autoResult: 自动化结果标注模式
    # getPlanCase: 测试计划用例导出模式
    # selectCase: 用例挑选模式
    autoLabel = 'getPlanCase'
    
    # 文件名配置
    typeFileName = '自动化类型标注.csv'  # 自动化类型标注文件名称
    resultFileName = '自动化结果标注.csv'  # 自动化结果标注文件名称
    selectCaseFileName = '测试计划用例挑选.xlsx'  # 测试计划用例挑选文件名称
    
    # 产品配置
    # 可选值：01_BIOS、02_BMC、03_昆仑卫士、04_机房管理系统
    yxProductName = '03_昆仑卫士'
    
    # 云效测试计划名称配置
    # 自动化结果标注模式和测试计划用例挑选模式，只能填一个名称，例如：[BMC-AORUN-ZX1000]B019
    # 测试计划用例导出模式，可以填一个或者多个名称（多个名称需用逗号隔开）
    # 例如：[BMC-AORUN-ZX1000]B019,[BMC-AORUN-ZX1000]B020，[BMC-DIKU-ZX]B007
    autoPlanName = "[昆仑卫士-Klsec-GHZL-1.44]B015"
    
    # 自动化用例库配置
    # 自动化类型标记量：
    # - 全部标记："all"
    # - 部分标记：直接填行号，例如："113"
    # - 多行标记：用逗号隔开，例如："113,174,187"
    lineNum = "all"
    
    # 新计划名称
    newPlanName = "[昆仑卫士-Klsec-GHZL-1.44]B015" 