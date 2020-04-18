from django.urls import path

from index import views




from index.views import userinfo, bloginfo

urlpatterns = [
    #
    # path('register/',views.RegisterView.as_view()),
    # #
    # path('login/',views.LoginView.as_view()),
    # #
    # path('user/',views.UserView.as_view()),
    # path('user/userlog/',views.UserlogView.as_view()),
    # #path('order/',views.OrderView.as_view()),
    # path('write/',views.WriteView.as_view()),
    #
    #
    #
    # ###from index.views import userinfo
    # # name 参数和序列化器的 lookup_field 对应
    # path('userinfo/<id>/',userinfo,name='id'),
    # path('bloginfo/',bloginfo,name='title')

    path('',)

]