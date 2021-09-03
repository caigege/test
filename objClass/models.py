from django.db import models


# 1. Create your models here. 1.一个写入，一个分析， 再次写入（方案库）,2.另一个判断和分析
# 1.先生成数据 2.再分析 3.再获取方案 4.再统计


class Objective(models.Model):
    '''
    1.目标
    '''
    name = models.CharField("目标名", max_length=100, null=True, unique=True)
    description = models.TextField("目标简介", max_length=2000, null=True)
    models.AutoField


class Plan(models.Model):
    '''
    2 计划
    '''
    name = models.CharField("计划名", max_length=100, null=True)
    description = models.TextField("计划简介", max_length=2000, null=True)
    step = models.IntegerField("序号", default=1)
    objectiveId = models.ForeignKey("Objective", on_delete=models.DO_NOTHING, verbose_name="目标id")
    models.AutoField


class PlanStepProblem(models.Model):
    '''
    3 计划问题 收集不考虑属性
    problemJson:[{"id":1,"name":"问题名称","do":1}] do:1 需要解决的属性;0不需要解决属性
    '''
    name = models.CharField("计划问题名", max_length=100, null=True)
    description = models.TextField("计划问题简介", max_length=2000, null=True)
    planId = models.ForeignKey("Plan", on_delete=models.DO_NOTHING, verbose_name="计划id")
    step = models.IntegerField("序号", default=1)
    problemJson = models.JSONField("问题属性json", max_length=2000, null=True)
    up_planStepProblemId=models.JSONField("上个问题id",null=True)
    down_planStepProblemId=models.JSONField("下个问题id",null=True)

    models.AutoField


class PlanStepProblemScheme(models.Model):
    '''
    4 计划方案 收集时,不用问题属性 result: 2 待判定  1 判定通过 0 判定失败
    '''
    name = models.CharField("计划问题名", max_length=100, null=True)
    description = models.TextField("计划问题简介", max_length=2000, null=True)
    planStepProblemId = models.ForeignKey("PlanStepProblem", on_delete=models.DO_NOTHING, verbose_name="计划问题id")
    result = models.IntegerField("方案结果", default=2)
    step = models.IntegerField("序号", default=1)
    schemeJson = models.JSONField("方案json", max_length=2000, null=True)
    models.AutoField


# 2 . 分析
# 2.1 问题分析(粒子)

class Attribute_problem(models.Model):
    '''
    2.1 问题属性
    '''
    Attribute_problem_Lv = models.IntegerField('问题属性级别', default=1)
    name = models.CharField("问题属性名", max_length=100, null=True, unique=True)
    description = models.TextField("问题属性简介", max_length=2000, null=True)
    models.AutoField


# 2.2 方案分析

class Attribute(models.Model):
    '''
    2.2 方案属性
    '''
    attributeLv = models.IntegerField('属性级别', default=1)
    name = models.CharField("属性名", max_length=100, null=True, unique=True)
    description = models.TextField("属性简介", max_length=2000, null=True)
    models.AutoField


class Relation(models.Model):
    '''
     2.3关系
     '''
    relationLv = models.IntegerField('属性级别', default=1)
    name = models.CharField("属性名", max_length=100, null=True, unique=True)
    description = models.TextField("属性简介", max_length=2000, null=True)
    models.AutoField


class Prototype(models.Model):
    '''
    2.4原型:上级属性--关系-->下级属性 记录本步骤的失败/成功 Attribute  Relation
    '''
    name = models.CharField("原型名", max_length=100, null=True,unique=True)
    up_Attribute = models.IntegerField("上个属性id")
    up_AttributeName = models.CharField("上个属性名称", max_length=100, null=True)
    down_Attribute = models.IntegerField("下个属性id")
    down_AttributeName = models.CharField("下个属性名称", max_length=100, null=True)
    relation = models.IntegerField("关系id")
    relationName = models.CharField("关系名称", max_length=100, null=True)
    step = models.IntegerField("序号")
    models.AutoField
# class Prototype(models.Model):
#     '''
#     2.4原型:上级属性--关系-->下级属性 记录本步骤的失败/成功 Attribute  Relation
#     '''
#     name = models.CharField("原型名", max_length=100, null=True)
#     up_Attribute = models.IntegerField("上个属性id")
#     up_AttributeName = models.CharField("上个属性名称", max_length=100, null=True)
#     down_Attribute = models.IntegerField("下个属性id")
#     down_AttributeName = models.CharField("下个属性名称", max_length=100, null=True)
#     relation = models.IntegerField("关系id")
#     relationName = models.CharField("关系名称", max_length=100, null=True)
#     step = models.IntegerField("序号")
#     models.AutoField

class EnvironmentProblemPrototype(models.Model):
    '''
    2.5原型环境:
    '''
    up_Attribute_problem = models.IntegerField("上个问题属性id", default=0)
    up_Attribute_problemName = models.CharField("上个问题属性名称", default="无", max_length=100, null=True)

    down_Attribute_problem = models.IntegerField("当前问题属性id")
    down_Attribute_problemName = models.CharField("当前问题属性名称", max_length=100, null=True)

    up_Prototype = models.IntegerField("原型id", default=0)
    up_PrototypeName = models.CharField("原型名称", default="无", max_length=100, null=True)

    successNum = models.IntegerField("成功次数", default=0)
    failNum = models.IntegerField("失败次数", default=0)
    models.AutoField


class ObjInit(models.Model):
    '''
    3.对象实例 Attribute
    '''
    name = models.CharField("对象实例名", max_length=100, null=True, unique=True)
    description = models.TextField("对象实例简介", max_length=2000, null=True)
    attributeId = models.JSONField("Attribute属性id", null=True)
    # [{'id':1,'name':2}]
    models.AutoField


# class Scheme(models.Model):
#     '''
#
#     '''


# *****************************************************
'''
class Environment(models.Model):
     2.5原型环境: 废弃
    up_Prototype = models.IntegerField("上个原型id", default=0)
    up_PrototypeName = models.CharField("上个原型名称", default="无", max_length=100, null=True)
    down_Prototype = models.IntegerField("下个原型id", unique=True)
    down_PrototypeName = models.CharField("下个原型名称", max_length=100, null=True, unique=True)
    successNum = models.IntegerField("成功次数", default=0)
    failNum = models.IntegerField("失败次数", default=0)
    models.AutoField


# - - - - -- - - - -- - - - - - --   - - -- -  - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - -
class Problem_collect(models.Model):
    # 2 步骤上遇到的问题收集 分析属性
    # problemJson:[{"id":1,"name":"问题名称","do":1}] do:1 需要解决的属性;0不需要解决属性
    name = models.CharField("问题名", max_length=100, null=True)
    description = models.TextField("问题简介", max_length=2000, null=True)
    problemJson = models.JSONField("问题属性json", max_length=2000, null=True)
    # execute_planId = models.ForeignKey("Execute_plan", on_delete=models.DO_NOTHING, verbose_name="计划执行id")
    planId = models.ForeignKey("Plan", on_delete=models.DO_NOTHING, verbose_name="计划id")
    objectiveId = models.ForeignKey("Objective", on_delete=models.DO_NOTHING, verbose_name="目标id")
    models.AutoField


class Problem_Execute(models.Model):
    # 3 步骤上遇到的问题方案解决收集 根据属性匹配方案
    # executeJson: Prototype id
    #     [{"id":1,"name":"方案名称","result":1,"losesText":"失败原因"}]
    #     result:0 执行失败,1 执行成功, 2 待执行,losesText 没有就为空
    # 问题id
    problem_collectId = models.ForeignKey("Problem_collect", on_delete=models.DO_NOTHING, verbose_name="问题id")
    # 问题属性Id
    problemAttributeId = models.ForeignKey("Attribute_problem", on_delete=models.DO_NOTHING, verbose_name="问题属性id")
    executeJson = models.JSONField("方案json", max_length=4000, null=True)
    models.AutoField


# class Execute_plan(models.Model):
#     1 执行方案 找出问题
#     problemJson:[{"id":1,"name":"问题名称","result":1}] result:0 执行失败,1 执行成功, 2 待执行
#     problemJson = models.JSONField("问题json", max_length=2000, null=True)
#     step = models.IntegerField("序号", default=1)
#     planId = models.ForeignKey("Plan", on_delete=models.DO_NOTHING, verbose_name="计划id")
#     objectiveId = models.ForeignKey("Objective", on_delete=models.DO_NOTHING, verbose_name="目标id")
#     models.AutoField


# class Analysis_plan(models.Model):
#     分析方案 存入方案
#     # 
    name = models.CharField("方案名", max_length=100, null=True, unique=True)
    description = models.TextField("方案简介", max_length=2000, null=True)
    step = models.IntegerField("序号", default=1)
    objectiveId = models.ForeignKey("Plan", on_delete=models.DO_NOTHING, verbose_name="目标id")
    models.AutoField



class Problem_scheme(models.Model):
    EnvironmentIds:
    [{"id":1,"successNum":1}]
    Attribute_problemId = models.ForeignKey("Attribute_problem", on_delete=models.DO_NOTHING, verbose_name="问题属性id")
    EnvironmentIds = models.JSONField("方案json", max_length=4000, null=True)
    models.AutoField

# **********************************************************************************

'''
