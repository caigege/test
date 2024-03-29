"""sthing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from objClass import views as objClassView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createAttribute/', objClassView.createAttribute),
    path('createAttribute_problem/', objClassView.createAttribute_problem),
    path('createObjective/', objClassView.createObjective),
    path('createObjInit/', objClassView.createObjInit),
    path('createPlan/', objClassView.createPlan),
    path('createPrototype/', objClassView.createPrototype),
    path('prototype/addPrototype/', objClassView.addPrototype),
    path('createRelation/', objClassView.createRelation),
    path('getAttribute_problem/', objClassView.getAttribute_problem),
    path('createPlanStepProblem/', objClassView.createPlanStepProblem),
    path('addPlanStepProblem/', objClassView.addPlanStepProblem),
    path('page/', objClassView.page),
    path('planPage/', objClassView.planPage),
    path('planStepProblemPage/', objClassView.planStepProblemPage),
    path('planStepProblemSchemePage/', objClassView.planStepProblemSchemePage),
    path('createPlanStepProblemScheme/', objClassView.createPlanStepProblemScheme),
    path('planStepProblemSchemeJudge/', objClassView.planStepProblemSchemeJudge),
    path('analysisPage/', objClassView.analysisPage),
    path('analysisPageGetProblemAtt/', objClassView.analysisPageGetProblemAtt),
    path('analysisPageRemoveAtt/', objClassView.analysisPageRemoveAtt),
    path('getAttribute/', objClassView.getAttribute),
    path('getRelation/', objClassView.getRelation),
    path('getObjInit/', objClassView.getObjInit),
    path('addPlanStepProblemUp/', objClassView.addPlanStepProblemUp),
    path('addPlanStepProblemDown/', objClassView.addPlanStepProblemDown),
    path('getHadPrototype/', objClassView.getHadPrototype),
    path('createEnvironmentProblemPrototype2/', objClassView.createEnvironmentProblemPrototype2),
    path('createEnvironmentProblemPrototype/', objClassView.createEnvironmentProblemPrototype),
    path('createEnvironment/', objClassView.createEnvironment),
    path('setProblemAtt/', objClassView.setProblemAtt)

]
