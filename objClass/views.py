# Create your views here.
import json
import time

import django
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import objClass
from objClass.models import Attribute, Relation, Prototype, ObjInit, Attribute_problem, Objective, Plan, \
    PlanStepProblem, PlanStepProblemScheme, EnvironmentProblemPrototype


# UI
def page(request):
    '''
        首页
    '''

    objective = Objective.objects.all()

    return render(request, 'model/Objective.html', {"objective": objective})


def planStepProblemSchemePage(request):
    proName = request.GET.get("proname")
    step = request.GET.get("step")
    planName = request.GET.get("planName")
    problemName = request.GET.get("problemName")
    planStepProblemId = request.GET.get("planStepProblemId")
    psp = PlanStepProblem.objects.get(id=planStepProblemId)

    planStepProblemScheme = PlanStepProblemScheme.objects.filter(planStepProblemId=psp)

    print(locals())
    objId = {"step": step, "planStepProblemId": planStepProblemId, "proName": proName, "planName": planName,
             "problemName": problemName}
    cxt = {"objId": objId, "psps": planStepProblemScheme}
    return render(request, 'model/planStepProblemSchemePage.html', cxt)


def planStepProblemPage(request):
    '''
    计划问题页面
    :param request:
    :return:
    '''
    planId = request.GET.get("planId")
    step = request.GET.get("step")
    print("step", step)
    plan = Plan.objects.get(id=planId)

    planStepProblem = PlanStepProblem.objects.filter(planId=plan)
    objId = {"id": planId, "proName": request.GET.get("proname"), "planName": request.GET.get("planName"),
             "step": step}
    cxt = {"objId": objId, "planStepProblem": planStepProblem, "step": step}
    # print(locals())
    # print(cxt["objId"]["proName"])
    return render(request, 'model/planStepProblemPage.html', cxt)


def planPage(request):
    '''
    计划
    :param request:
    :return:
    '''
    id = request.GET.get("projectId")
    objective = Objective.objects.get(id=id)
    plan = Plan.objects.filter(objectiveId=objective)
    objId = {"id": id, "proName": objective.name}
    cxt = {"objId": objId, "plan": plan}

    # print(locals())
    # print(cxt["objId"]["proName"])
    return render(request, 'model/planPage.html', cxt)


def analysisPageGetProblemAtt(request):
    '''
    获取问题属性缓存
    :param request:
    :return:
    '''
    print("request.GET.get('planStepProblemId'))", request.GET.get("planStepProblemId"))
    att = request.GET.get("planStepProblemId")
    return JsonResponse(json.dumps(getProblemAtt(att), ensure_ascii=False), safe=False)


def setProblemAtt(request):
    '''
    设置主要属性
    :param request:
    :return:
    '''
    id = request.GET.get("id")
    pJson = checkStepProlem(id)
    attrId = int(request.GET.get("attrId"))
    do = int(request.GET.get("do"))
    # do = request.GET.get("do")
    # print(locals())
    num = 0
    for s in pJson:
        # print("s",s," * ",type(s),s.get("id") == attrId)
        # print("s.get('id')", s.get("id"), " * ", type(s.get("id")), s.get("id") == attrId, "attrId:", attrId,
        # "attrIdType", type(attrId))
        print()
        print("s ：", s)
        print("pJson[num]1", pJson[num], "num", num)
        if s.get("id") == attrId:
            # pJson.remove(s)

            pJson[num]["do"] = do
            print("pJson[num]",pJson[num],"num",num)
        num += 1;
    print("pJson : ",pJson)
    res = PlanStepProblem.objects.filter(id=id).update(problemJson=pJson)
    if res >= 1:
        return HttpResponse("ok")
    else:
        return HttpResponse("更新失败")


def analysisPageRemoveAtt(request):
    '''
    移除属性
    :param request:
    :return:
    '''
    id = request.GET.get("id")
    pJson = checkStepProlem(id)
    attrId = int(request.GET.get("attrId"))
    print("pJson : ", type(pJson), pJson, "attrId ", attrId)
    for s in pJson:
        # print("s",s," * ",type(s),s.get("id") == attrId)
        print("s.get('id')", s.get("id"), " * ", type(s.get("id")), s.get("id") == attrId, "attrId:", attrId,
              "attrIdType", type(attrId))
        if s.get("id") == attrId:
            pJson.remove(s)
    PlanStepProblem.objects.filter(id=id).update(problemJson=pJson)
    return HttpResponse(attrId)


def analysisPage(request):
    '''
    分析页面
    :param request:
    :return:
    '''
    planStepProblemId = request.GET.get("planStepProblemId")
    planStepProblemSchemeId = request.GET.get("planStepProblemSchemeId")

    psp = data_PlanStepProblem(planStepProblemId)
    pspObject = psp[0];
    # pspO = {"problem": pspObject,"pJson":pJson}
    # upName=""
    up_PspID = pspObject.up_planStepProblemId
    print("up_PspID: ", up_PspID, up_PspID[0])

    psps = data_planStepProblemScheme(planStepProblemSchemeId)
    pspsObject = psps[0];
    # print("upName ： ",upName)
    pspO = {"problem": pspObject, "problemScheme": pspsObject, "up_PspID": up_PspID[0]}

    return render(request, 'model/analysisPage.html', pspO)


def SelectObjective(request):
    '''
    选择项目
    :param request:
    :return:
    '''
    pass


# data
def data_PlanStepProblem(planStepProblemId):
    # id=request.GET.get("planStepProblemId")
    return PlanStepProblem.objects.filter(id=planStepProblemId)


def data_planStepProblemScheme(planStepProblemSchemeId):
    return PlanStepProblemScheme.objects.filter(id=planStepProblemSchemeId)


# ************************************************************
# 1 写入数据--流程写入
def createObjective(request):
    '''
    创造目标-1
    :return:
    '''
    name = request.GET.get("name")
    description = request.GET.get("description")
    print("name:" + name)
    try:
        Objective.objects.create(name=name, description=description)
    except django.db.utils.IntegrityError:
        return HttpResponse("属性name命名重复")
    return HttpResponse("ok")


def createPlan(request):
    '''
    计划 -2
    :return:
    '''
    name = request.GET.get("name")
    description = request.GET.get("description")
    step = request.GET.get("step")
    objectiveId = request.GET.get("objectiveId")
    objective = Objective.objects.filter(id=objectiveId)
    if (objective.count() == 0):
        return HttpResponse("目标id:" + str(objectiveId) + " 不存在")
    print("计划 : ", name, description, step, objectiveId)
    Plan.objects.create(name=name, description=description, step=step, objectiveId=objective[0])
    return HttpResponse("ok")


def createPlanStepProblem(request):
    '''
    3 - 0
    发现计划问题
    :param request:
    :return:
    '''
    name = request.GET.get("name")
    step = request.GET.get("step")
    description = request.GET.get("description")
    planId = request.GET.get("planId")
    plan = Plan.objects.get(id=planId)
    PlanStepProblem.objects.create(step=step, name=name, description=description, planId=plan)
    return HttpResponse("ok")


def addPlanStepProblemDown(request):
    id = request.GET.get("id")
    jsonDown = request.GET.get("jsonDown")
    print("jsonDown**", jsonDown)
    PlanStepProblem.objects.filter(id=id).update(down_planStepProblemId=json.loads(jsonDown))
    return HttpResponse("ok")


def addPlanStepProblemUp(request):
    id = request.GET.get("id")
    jsonUp = request.GET.get("jsonUp")

    PlanStepProblem.objects.filter(id=id).update(up_planStepProblemId=json.loads(jsonUp))
    return HttpResponse("ok")


def addPlanStepProblem(request):
    '''
    3 - 1
    添加问题属性 problemJson:[{"id":1,"name":"问题名称","do":1}] do:1 需要解决的属性;0不需要解决属性 2待确认
    '''
    planStepProblemId = request.GET.get("planStepProblemId")
    problemJsonStr = request.GET.get("problemJson")
    problemJson = json.loads(problemJsonStr)
    # 查询问题属性
    pJson = checkStepProlem(planStepProblemId)
    print("pJson : ", pJson, type(pJson))
    num = 1
    #
    pJs = []
    pJss = []
    if pJson is None:
        pJss.append(problemJson)
        print("pJss:", pJss)
        num = PlanStepProblem.objects.filter(id=planStepProblemId).update(problemJson=pJss)
        return HttpResponse("ok")
    else:
        for pJ in pJson:
            pJs.append(pJ.get("id"))
    print("pJs:", pJs)
    if problemJson.get("id") in pJs:
        return HttpResponse("问题属性已存在")
    else:
        pJson.append(problemJson)
        # 已存在的问题属性判断
        print("pJson2 : ", pJson, type(pJson))
        num = PlanStepProblem.objects.filter(id=planStepProblemId).update(problemJson=pJson)
        print("num2:", num)

    if num == 0:
        return HttpResponse("fail")
    else:
        return HttpResponse("ok")


def getProblemAtt(planStepProblemId):
    '''
    查询属性
    :param planStepProblemId:
    :return:
    '''
    pJson = checkStepProlem(planStepProblemId)

    return pJson


def checkStepProlem(planStepProblemId):
    '''
    查询问题 问题属性
    :param planStepProblemId:
    :return:
    '''
    planSPro = PlanStepProblem.objects.filter(id=planStepProblemId)
    pJson = planSPro[0].problemJson
    return pJson


def planStepProblemSchemeJudge(request):
    '''
    4 - 3
    添加一期方案的执行结果
    :param request:
    :return:
    '''
    id = request.GET.get("planStepProblemSchemeId")
    result = request.GET.get("result")
    PlanStepProblemScheme.objects.filter(id=id).update(result=result)
    return JsonResponse({"msg": "ok"})


def addPlanStepProblemScheme(request):
    '''
    4 - 2
    添加一期收集方案属性
    :param request:
    :return:
    '''
    id = request.GET.get("planStepProblemSchemeId")
    schemeJsonStr = request.GET.get("schemeJsonStr")
    schemeJson = json.load(schemeJsonStr)
    PlanStepProblemScheme.objects.filter(id=id).update(schemeJson=schemeJson)
    return HttpResponse("ok")


def createPlanStepProblemScheme(request):
    '''
    4 - 1
    写入方案
    :param request:
    :return:
    '''
    name = request.GET.get("name")
    step = request.GET.get("step")
    description = request.GET.get("description")
    planStepProblemId = request.GET.get("planStepProblemId")
    planStepProblem = PlanStepProblem.objects.get(id=planStepProblemId)
    PlanStepProblemScheme.objects.create(step=step, name=name, description=description,
                                         planStepProblemId=planStepProblem)
    return HttpResponse("ok")


# 2.分析数据 分析类别
def createAttribute(sth):
    '''
    方案属性类型
    :return:
    '''

    attributeLv = sth.GET.get("attributeLv")
    if (attributeLv is None):
        attributeLv = 1
    name = sth.GET.get("name")
    description = sth.GET.get("description")
    try:
        Attribute.objects.create(attributeLv=attributeLv, name=name, description=description)
    except django.db.utils.IntegrityError:
        return HttpResponse("属性命名重复")
    return HttpResponse("ok")


def createAttribute_problem(sth):
    '''
    问题属性类型
    :return:
    '''
    name = sth.GET.get("name")
    description = sth.GET.get("description")
    try:
        Attribute_problem.objects.create(name=name, description=description)
    except django.db.utils.IntegrityError as e:
        return HttpResponse("属性命名重复:" + str(e))
    return HttpResponse("ok")


def createRelation(sth):
    '''
    关系属性类型
    :return:
    '''
    relationLv = sth.GET.get("relationLv")
    if (relationLv is None):
        relationLv = 1
    name = sth.GET.get("name")
    description = sth.GET.get("description")
    try:
        Relation.objects.create(relationLv=relationLv, name=name, description=description)
    except django.db.utils.IntegrityError as e:
        return HttpResponse("属性命名重复:")
    return HttpResponse("ok")


def createPrototype(request):
    '''
    原型
    :return:
    '''
    # 判断是否存在

    up_Attribute = request.GET.get("up_Attribute")
    relationId = request.GET.get("relation")
    down_Attribute = request.GET.get("down_Attribute")
    step = request.GET.get("step")
    name = request.GET.get("name")

    if (hasPrototypeObject(down_Attribute, relationId, up_Attribute, step)[0]):
        cdf = createDef(name, down_Attribute, relationId, step, up_Attribute)
        print("cdf:", cdf)
        if (not cdf):
            return HttpResponse("ok")
        else:
            return HttpResponse(cdf)
    else:
        return HttpResponse("重复fail")


def addPrototype(request):
    '''
    原型打分
    :param request:
    :return:
    '''
    down_Attribute = request.GET.get("down_Attribute")
    relationId = request.GET.get("relation")
    up_Attribute = request.GET.get("up_Attribute")
    step = request.GET.get("step")
    successNum = request.GET.get("successNum")
    failNum = request.GET.get("failNum")
    hasResult = hasPrototypeObject(down_Attribute, relationId, up_Attribute, step)
    print("hasResult  : ", hasResult)
    # print("hasResult-dir  : ", dir(hasResult[1][0]))
    if (hasResult[0]):
        # 不存在 True
        cdf = createDef(down_Attribute, relationId, request, step, up_Attribute)
        print("cdf:", cdf)
        if (not cdf):
            return HttpResponse("ok")
        else:
            return HttpResponse(cdf)
    else:
        # 添加成功/失败 存在 False
        print("successNum ： ", successNum)
        sucR = Prototype.objects.filter(id=hasResult[1][0].id)[0]
        try:
            if (int(successNum) == 1):
                num = sucR.successNum
                Prototype.objects.filter(id=hasResult[1][0].id).update(successNum=(int(num) + 1))
            elif (int(failNum == 1)):
                num2 = sucR.failNum
                Prototype.objects.filter(id=hasResult[1][0].id).update(successNum=(int(num2) + 1))
            else:
                return HttpResponse("统计参数错误1 successNum " + successNum + " *  failNum:" + failNum + " *")
        except:
            return HttpResponse("统计参数错误2 successNum " + successNum + " *  failNum:" + failNum + " *")
    return HttpResponse("ok")


def addEnvironmentProblemPrototype(request):
    '''
    添加问题和方案积分
    djsonstr {"successNum":1}{}

    :param request:
    :return:
    '''
    id = request.GET.get("id")
    djsonstr = request.GET.get("json")
    djson = json.load(djsonstr)
    if (djson.get("successNum") is None):
        EnvironmentProblemPrototype.objects.filter(id=id).update(
            failNum=EnvironmentProblemPrototype.objects.filter(id=id)[0].failNum + 1)
    else:
        EnvironmentProblemPrototype.objects.filter(id=id).update(
            failNum=EnvironmentProblemPrototype.objects.filter(id=id)[0].successNum + 1)

    return HttpResponse("ok")


def createEnvironmentProblemPrototype2(request):
    pass


def createEnvironmentProblemPrototype(request):
    '''
    关联 问题 - 方案属性
    :param request:
    :return:
    '''
    # 问题属性id
    down_Attribute_problem = request.GET.get("down_Attribute_problem")
    down_Attribute_problemName = request.GET.get("down_Attribute_problemName")
    # down_Attribute_problemName = Attribute_problem.objects.get(id=down_Attribute_problem).name

    up_Attribute_problem = request.GET.get("up_Attribute_problem")
    up_Attribute_problemName = request.GET.get("up_Attribute_problemName")

    up_Prototype = request.GET.get("up_Prototype")
    up_PrototypeName = request.GET.get("up_PrototypeName")
    # up_PrototypeName = Prototype.objects.get(id=up_Prototype).name

    if (up_Attribute_problem is None or len(up_Attribute_problem) == 0):
        EnvironmentProblemPrototype.objects.create(down_Attribute_problem=down_Attribute_problem,
                                                   down_Attribute_problemName=down_Attribute_problemName,
                                                   up_Prototype=up_Prototype, up_PrototypeName=up_PrototypeName)
    else:
        up_Attribute_problemName = Attribute_problem.objects.get(id=up_Attribute_problem).name
        EnvironmentProblemPrototype.objects.create(up_Attribute_problem=up_Attribute_problem,
                                                   up_Attribute_problemName=up_Attribute_problemName,
                                                   down_Attribute_problem=down_Attribute_problem,
                                                   down_Attribute_problemName=down_Attribute_problemName,
                                                   up_Prototype=up_Prototype, up_PrototypeName=up_PrototypeName)
    return HttpResponse("ok")


def createObjInit(request):
    '''
    属性实例
    :return:
    '''
    name = request.GET.get("name")
    description = request.GET.get("description")
    attributeId = request.GET.get("attributeId")
    print("attributeId : ", attributeId, type(attributeId))
    attributeIdJson = json.loads(attributeId)

    for i in attributeIdJson:
        Id = i.get("id")
        if (Attribute.objects.filter(id=Id).count() == 0):
            return HttpResponse("属性" + str(Id) + "不存在")
    print("attributeId : ", attributeIdJson)
    objInitObject = ObjInit.objects.filter(name=name)
    if objInitObject.count() == 0:

        ObjInit.objects.create(name=name, description=description, attributeId=attributeIdJson)

    else:
        attributeIds = objInitObject[0].attributeId
        for attr in attributeIds:
            print("attr:", attr)
            if Id == attr.get("id"):
                return HttpResponse("属性已存在")

        attributeIds.append(attributeIdJson[0])
        # print("attributeIds:", attributeIds)
        objInitObject.update(attributeId=attributeIds)
        return JsonResponse(json.dumps(attributeIds, ensure_ascii=False), safe=False)

    return HttpResponse("ok")


# 2.1分析数据 分析数据

# ---Prototype---
def getPrototype2(request):
    name = request.GET.get("name")

    pass


def getHadPrototype(request):
    name = request.GET.get("name")
    up_AttributeName = request.GET.get("upName")
    relationName = request.GET.get("relationName")
    down_AttributeName = request.GET.get("downName")
    # if name
    vstr = "";
    datas = [{"name": "name", "key": name},
             {"name": "up_AttributeName", "key": up_AttributeName},
             {"name": "relationName", "key": relationName},
             {"name": "down_AttributeName", "key": down_AttributeName}]
    # print(locals())
    print(len(datas))
    v = 0
    datasCopy = datas.copy()
    for data in datas:
        print(v, ":", data.get("key"))
        if data.get("key") == "":
            datasCopy.remove(data)
        v = +1;
    time.sleep(1)
    print("datasCopy:", datasCopy)
    # print("datas:",datas)
    for d in datasCopy:
        vstr = d.get("name") + "__contains=" + d.get("key") + "," + vstr
    vstr = vstr[0:len(vstr)]
    print("vstr : " + vstr);
    rusl = eval("Prototype.objects.filter(" + vstr + ")[0:10]")
    print("rusl : ", rusl, len(rusl))
    ret = serializers.serialize("python", rusl)
    return JsonResponse(json.dumps(ret, ensure_ascii=False), safe=False)


def getPrototype(request):
    '''
    获取原型
    :param request:
    :return:
    '''
    up_Attribute = request.GET.get("up_Attribute")
    relationId = request.GET.get("relation")
    down_Attribute = request.GET.get("down_Attribute")
    step = request.GET.get("step")
    hasPro = hasPrototypeObject(down_Attribute, relationId, up_Attribute, step)
    if (hasPro[0]):
        cdf = createDef(down_Attribute, relationId, step, up_Attribute)
        print("cdf:", cdf)
        if (not cdf):
            return HttpResponse("ok")
        else:
            return HttpResponse(cdf)
    else:
        return HttpResponse(hasPro[1].id + "," + hasPro[1].name)


def getPrototypeSearch(request):
    '''
    获取关系属性 以供选择对已知搜索
    :param request:
    :return:
    '''
    name = request.GET.get("name")
    attrs = Prototype.objects.filter(name__contains=name)
    js = {}
    jss = []
    for attr in attrs:
        js["name"] = attr.name
        js["id"] = attr.pk
        jss.append(js)
        js = {}
    return HttpResponse(jss)


def getRelation(request):
    '''
        获取关系属性 以供选择
        :param request:
        :return:
        '''
    name = request.GET.get("name")
    attrs = Relation.objects.filter(name__contains=name)[0:10]

    ret = serializers.serialize("python", attrs)

    return JsonResponse(json.dumps(ret, ensure_ascii=False), safe=False)


def getAttribute(request):
    '''
    获取方案属性 以供选择
    :param request:
    :return:
    '''
    name = request.GET.get("name")
    attrs = Attribute.objects.filter(name__contains=name)[0:10]

    ret = serializers.serialize("python", attrs)

    return JsonResponse(json.dumps(ret, ensure_ascii=False), safe=False)


# --Prototype--
def getAttribute_problem(request):
    '''
    问题属性模糊查询
    :param request:
    :return:
    '''
    name = request.GET.get("name")
    attrs = Attribute_problem.objects.filter(name__contains=name)[0:10]

    ret = serializers.serialize("python", attrs)

    return JsonResponse(json.dumps(ret, ensure_ascii=False), safe=False)


def analyseCreateAttribute_problem(request):
    '''
    自动分析 1.获取 createPlanStepProblem 生成的问题
    0.查询是否有问题属性 todo
    1.没有的定义出问题属性
    2.
    :param request:
    :return:
    '''
    pass


# 3.方案调用

def getObjInit(request):
    '''
    attributeId={"id":1}
    :param request:
    :return:
    '''
    name = request.GET.get("name")
    obj = ObjInit.objects.filter(name=name)
    attributeIds = obj[0].attributeId
    return JsonResponse(json.dumps(attributeIds, ensure_ascii=False), safe=False)


def checkSchemeFristStep(request):
    '''
    根据方案查询原型
    :param request:
    :return:
    '''


def checkSchemeFristStep(request):
    '''
    给出方案 第一步
    :param request:
    :return:
    '''
    down_Attribute_problem = request.GET.get("down_Attribute_problem")
    up_Attribute_problem = 0
    EnvirScheme = cS(down_Attribute_problem, up_Attribute_problem)
    return HttpResponse(EnvirScheme)


def cS(down_Attribute_problem, up_Attribute_problem):
    # 根据问题属性 查询方案--

    EnvirScheme = EnvironmentProblemPrototype.objects.filter(up_Attribute_problem=up_Attribute_problem,
                                                             down_Attribute_problem=down_Attribute_problem)
    return EnvirScheme


def checkScheme(request):
    '''
    给出方案 第二步以后
    :param request:
    :return:
    '''
    # 根据问题属性 查询方案--
    down_Attribute_problem = request.GET.get("down_Attribute_problem")
    up_Attribute_problem = request.GET.get("up_Attribute_problem")
    EnvirScheme = cS(down_Attribute_problem, up_Attribute_problem)
    return HttpResponse(EnvirScheme)


def createDef(name, down_Attribute, relationId, step, up_Attribute):
    '''

    :param name:
    :param down_Attribute:
    :param relationId:
    :param step:
    :param up_Attribute:
    :return:
    '''
    try:
        attribute1 = Attribute.objects.get(id=up_Attribute)
    except objClass.models.Attribute.DoesNotExist:
        return "上级属性不存在"
    up_AttributeName = attribute1.name
    # print("down_Attribute:",down_Attribute)
    try:
        attribute = Attribute.objects.get(id=down_Attribute)
    except objClass.models.Attribute.DoesNotExist:
        return "下级属性不存在"
    try:
        Prototype.objects.get(name=name)
        return "名称已存在"
    except:
        pass

    down_AttributeName = attribute.name
    # print("createDef 1 ", relationId)
    relationName = (Relation.objects.get(id=relationId)).name
    # print("createDef 2 ")

    # print("failNum:", failNum)
    Prototype.objects.create(name=name, up_Attribute=up_Attribute, up_AttributeName=up_AttributeName,
                             relation=relationId,
                             relationName=relationName, down_Attribute=down_Attribute,
                             down_AttributeName=down_AttributeName, step=step)


def hasPrototypeObject(down_Attribute, relationId, up_Attribute, step):
    '''
    是否是存在
    :param down_Attribute:
    :param relationId:
    :param up_Attribute:
    :param step:
    :return:  True 不存在 False 存在
    '''
    prototypeCheck = Prototype.objects.filter(up_Attribute=up_Attribute)
    if (prototypeCheck.count() == 0):
        print("--1--")
        return (True,)
    else:
        prototypeCheckSecond = prototypeCheck.filter(relation=relationId)
        print("--2--")
        if (prototypeCheckSecond.count() == 0):
            print("--3--")
            return (True,)
        else:
            print("--4--")
            prototypeCheckThirdly = prototypeCheckSecond.filter(down_Attribute=down_Attribute)
            if (prototypeCheckThirdly.count() == 0):
                print("--5没找到--")
                return (True,)
            else:
                prototypeCheckFourth = prototypeCheckThirdly.filter(step=step)
                print("--6--")
                if (prototypeCheckFourth.count() == 0):
                    print("--7--")
                    return (True,)
                else:
                    return (False, prototypeCheckFourth)


def createEnvironment(request):
    '''
    环境
    :return:
    '''
    # 原型
    up_Prototype = request.GET.get("up_Prototype")
    if (Prototype.objects.filter(id=up_Prototype).count() == 0):
        return HttpResponse("原型不存在")
    up_PrototypeName = request.GET.get("up_PrototypeName")
    # 上级问题
    up_Attribute_problem = request.GET.get("up_Attribute_problem")
    up_Attribute_problemName = request.GET.get("up_Attribute_problemName")

    # 下级问题
    down_Attribute_problem = request.GET.get("down_Attribute_problem")
    down_Attribute_problemName = request.GET.get("down_Attribute_problemName")

    # 通过
    cheked = request.GET.get("checked")

    # 方案id
    id = request.GET.get("schemeId")
    pspsCheck = PlanStepProblemScheme.objects.filter(id=id)
    print("pspsCheck:", pspsCheck)
    print("pspsCheck:", pspsCheck[0])
    print("pspsCheck:", pspsCheck[0].step)
    print("pspsCheck[0].schemeJson :", pspsCheck[0].schemeJson, type(pspsCheck[0].schemeJson))
    if (pspsCheck[0].schemeJson is None):
        if cheked == "0":
            # 未通过
            successNum = 1
        else:
            # 通过
            failNum = 1
        pNN = pspsCheck.update(schemeJson={"id": up_Prototype, "name": up_PrototypeName})
        print("pNN:", pNN)
        try:
            judge = judgeEnvironmentProblemPrototype(up_Attribute_problem, down_Attribute_problem, up_Prototype)

            if (judge[0]):
                print("---failNum111-----")
                if (successNum == 1):
                    EnvironmentProblemPrototype.objects.create(up_Prototype=up_Prototype,
                                                               up_PrototypeName=up_PrototypeName,
                                                               down_Attribute_problem=down_Attribute_problem,
                                                               down_Attribute_problemName=down_Attribute_problemName,
                                                               up_Attribute_problem=up_Attribute_problem,
                                                               up_Attribute_problemName=up_Attribute_problemName,
                                                               successNum=1, failNum=0)

                    return HttpResponse("ok1")
                else:
                    print("---failNum-----")
                    EnvironmentProblemPrototype.objects.create(up_Prototype=up_Prototype,
                                                               up_PrototypeName=up_PrototypeName,
                                                               down_Attribute_problem=down_Attribute_problem,
                                                               down_Attribute_problemName=down_Attribute_problemName,
                                                               up_Attribute_problem=up_Attribute_problem,
                                                               up_Attribute_problemName=up_Attribute_problemName,
                                                               successNum=0, failNum=1)

                    return HttpResponse("ok2")
            else:
                env = judge[1]
                if (successNum == 1):
                    suc = int(env[0].successNum) + 1
                    env.update(successNum=suc)
                else:
                    fail = int(env[0].failNum) + 1
                    env.update(failNum=fail)
                return HttpResponse("已更新")
        except:
            print("---except-----")
            print("fail successNum" + successNum + " failNum:" + failNum)
            return HttpResponse("fail successNum" + successNum + " failNum:" + failNum)
    else:
        return HttpResponse("方案已有属性")


def judgeEnvironmentProblemPrototype(up_Attribute_problem, down_Attribute_problem, up_Prototype):
    Env = EnvironmentProblemPrototype.objects.filter(up_Attribute_problem=up_Attribute_problem)
    if (Env.count() == 0):
        # 没查询到
        return (True,)
    else:
        Env1 = Env.filter(down_Attribute_problem=down_Attribute_problem)
        if (Env1.count() == 0):
            # 没查询到
            return (True,)
        else:
            # 没查询到
            print("***----****")
            Env2 = Env1.filter(up_Prototype=up_Prototype)
            if (Env2.count() == 0):
                # 没查询到
                return (True,)
            else:
                Env2[0].successNum
                return (False, Env2)
# def createProblem_Execute(request):
#     problem_collectId = request.GET.get("problem_collectId")
#     problem_collect = Problem_collect.objects.get(id=problem_collectId)
#
#     problemAttributeId = request.GET.get("problemAttributeId")
#     problemAttribute = Attribute_problem.objects.get(id=problemAttributeId)
#
#     # executeJson = request.GET.get("executeJson") #Prototype 的id
#     Problem_Execute.objects.create(problem_collectId=problem_collect, problemAttributeId=problemAttribute)


# def addExecuteJson(request):
#     '''
#     添加方案 {"id":1,"name":"方案名称","result":1,"losesText":"失败原因"}]
#     :param request:
#     :return:
#     '''
#     id = request.GET.get("id")
#     executeJsonStr = request.GET.get("addExecuteJson")
#     executeJson = json.load(executeJsonStr)
#     Problem_Execute.objects.filter(id=id).update(executeJson=executeJson)
#     return HttpResponse("ok")
# def create_Problem_collect(request):
#     '''对应计划问题'''
#     name = request.GET.get("name")
#     description = request.GET.get("description")
#     # 问题属性json
#     problemJsonStr = request.GET.get("problemJson")
#     problemJson = json.load(problemJsonStr)
#     problemJsonNum = len(problemJson)
#     planId = request.GET.get("planId")
#     # objectiveId = request.GET.get("objectiveId")
#
#     for pJson in problemJson:
#         # 查询属性是否存在
#         attProblem = Attribute_problem.objects.filter(id=pJson.get("id"))
#         if (attProblem.count() == 0):
#             problemJson.remove(pJson)
#         else:
#             pJson["name"] = attProblem[0]["name"]
#     problemJsonNumResult = len(problemJson)
#     if problemJsonNumResult == 0:
#         return HttpResponse("属性不存在 去添加问题属性页面 " + str(problemJsonNumResult) + "/" + str(problemJsonNum))
#
#     try:
#         plan = Plan.objects.get(id=planId)
#         objective = Objective.objects.get(id=plan.objectiveId)
#     except objClass.models.Attribute.DoesNotExist:
#         return HttpResponse("planId : " + planId + "不存在 或是 plan.objectiveId " + plan.objectiveId + "不存在")
#
#     Problem_collect.objects.create(name=name, description=description, problemJson=problemJson,
#                                    planId=plan, objectiveId=objective)
#     return HttpResponse("ok 进度: 已录入/需录入" + str(problemJsonNumResult) + "/" + str(problemJsonNum))


# def add_problem_collect(request):
#     '''
#     添加问题属性
#     :return:
#     '''
#     id = request.GET.get("id")
#     problemJsonStr = request.GET.get("problemJson")
#     problemJson = json.load(problemJsonStr)
#
#     try:
#         proColl = Problem_collect.objects.get(id=id)
#     except:
#         return HttpResponse("问题不存在")
#     prj = proColl.problemJson
#     prj.append(problemJson)
#     proColl.updata(problemJson=prj)
#
#     return HttpResponse("更新ok")

# def addEnvironment(request):
#     '''
#     环境打分
#     :param request:
#     :return:
#     '''
#     up_Prototype = request.GET.get("up_Prototype")
#     if (Prototype.objects.filter(id=up_Prototype).count() == 0):
#         return HttpResponse("原型不存在")
#
#     down_Prototype = request.GET.get("down_Prototype")
#     if (Prototype.objects.filter(id=down_Prototype).count() == 0):
#         return HttpResponse("原型不存在2")
#
#     successNum = request.GET.get("successNum")
#     failNum = request.GET.get("failNum")
#
#     # --------
#     hasResult = judgeEnvironment(down_Prototype, up_Prototype)
#     print("hasResult  : ", hasResult)
#     # print("hasResult-dir  : ", dir(hasResult[1][0]))
#     if (hasResult[0]):
#         # 不存在 True
#         return HttpResponse("原型不存在3")
#     else:
#         # 添加成功/失败 存在 False
#         print("successNum ： ", successNum)
#         sucR = Prototype.objects.filter(id=hasResult[1][0].id)[0]
#         try:
#             if (int(successNum) == 1):
#                 num = sucR.successNum
#                 Environment.objects.filter(id=hasResult[1][0].id).update(successNum=(int(num) + 1))
#             elif (int(failNum == 1)):
#                 num2 = sucR.failNum
#                 Environment.objects.filter(id=hasResult[1][0].id).update(successNum=(int(num2) + 1))
#             else:
#                 return HttpResponse("统计参数错误1 successNum " + successNum + " *  failNum:" + failNum + " *")
#         except:
#             return HttpResponse("统计参数错误2 successNum " + successNum + " *  failNum:" + failNum + " *")
#     return HttpResponse("ok")


# def createExecute_plan(request):
#     '''
#     执行计划
#     problemJson 来至于 problem_collect 问题收集
#     :return:
#     '''
#     problemJson = request.GET.get("problemJson")
#     planId=request.GET.get("planId")
#
#     plan=Plan.objects.get(id=planId)
#     step=plan.step
#     objectiveId = request.GET.get("objectiveId")
#     objective=Objective.objects.get(id=objectiveId)
#
#     Execute_plan.objects.create(problemJson=problemJson,step=step,planId=plan,objectiveId=objective)
#     return HttpResponse("ok")


# def createAnalysis_plan():
#     '''
#     分析存入方案
#     :return:
#     '''
#     pass
