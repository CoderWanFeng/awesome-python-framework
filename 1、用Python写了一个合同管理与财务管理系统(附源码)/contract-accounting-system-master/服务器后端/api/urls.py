from rest_framework.routers import DefaultRouter
from django.urls import path


from api.views import UserViewSet, TestViewSet, DepartmentViewSet, EntityViewSet, ProjectViewSet, \
    TrafficViewSet, AccountViewSet, Account_normalViewSet, Account_viewViewSet, Contract_planViewSet, \
    Contract_infoViewSet, attachmentViewSet, EntityAllViewSet, ProjectAllViewSet, UserAllViewSet, ZhuChe
from . import views

router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'usersall',UserAllViewSet)
# router.register(r'userstest',UsertestViewSet)
router.register(r'dept',DepartmentViewSet)
router.register(r'entity',EntityViewSet)
router.register(r'entityall',EntityAllViewSet)
router.register(r'projects',ProjectViewSet)
router.register(r'projectsall',ProjectAllViewSet)
router.register(r'test',TestViewSet)
router.register(r'traffictypes',TrafficViewSet)
router.register(r'Account_projects',AccountViewSet,basename = 'Account_projects')
router.register(r'Account_normals',Account_normalViewSet)
router.register(r'Account_views',Account_viewViewSet)
router.register(r'Contract_plans',Contract_planViewSet)
router.register(r'Contract_infos',Contract_infoViewSet)
router.register(r'attachments',attachmentViewSet)



urlpatterns = [
    # path('', views.index, name='index'),
    # path('testdb', views.testdb),
    path('dog', views.DogView.as_view()),
    path('getUserInfo', views.getUserInfo),
    path('login', views.Login.as_view()),
    path('getdata',views.TestData.as_view()),
    path('zhuche',ZhuChe.as_view()),
    # path('menus',views.GetMenus.as_view()),
]

urlpatterns += router.urls


