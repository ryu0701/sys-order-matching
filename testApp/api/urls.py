from django.urls import path
from testApp.api import views

urlpatterns = [
    path(r'v1/login', views.StfdbStaffViewSet.as_view() ,name='login'),
    path(r'v1/mstData/mstcity', views.MstCityViewSet.as_view() ,name='city'),
    path(r'v1/mstData/mstpref', views.MstPrefViewSet.as_view() ,name='prefecture'),
    path(r'v1/mstData/mstapproach', views.MstApproachStatusViewSet.as_view() ,name='approach_status'),
    path(r'v1/mstData/mstdisp', views.MstDispOrderViewSet.as_view() ,name='disp_order'),
    path(r'v1/mstData/mstcontactways', views.MstContactWaysViewSet.as_view() ,name='contact_ways'),
    path(r'v1/mstData/mstmedia', views.MstMediaViewSet.as_view() ,name='media'),
    path(r'v1/mstData/mstdisp', views.MstDispOrderViewSet.as_view() ,name='disp_order'),
    path(r'v1/mstData/mstcrstatus', views.MstCareerStatusViewSet.as_view() ,name='career_status'),
    path(r'v1/mstData/mstlastschool', views.MstLastSchoolViewSet.as_view() ,name='last_school'),
    path(r'v1/mstData/mstenglishlv', views.MstEnglishLevelViewSet.as_view() ,name='english_level'),
    path(r'v1/mstData/mstotherlang', views.MstOtherLangageViewSet.as_view() ,name='other_langage'),
    path(r'v1/mstData/mstenglishlv', views.MstEnglishLevelViewSet.as_view() ,name='english_level'),
    path(r'v1/mstData/mstSection', views.MstSectionAPIView.as_view() ,name='section'),
    path(r'v1/mstData/mstStaff', views.MstStaffAPIView.as_view() ,name='staff'),
    path(r'v1/mstData/mstCp2User', views.MstCp2UserAPIView.as_view() ,name='cp2user'),
    path(r'v1/mstData/mstIndustry', views.MstIndustryAPIView.as_view() ,name='mstIndustry'),
    path(r'v1/mstData/mstLicense', views.MstLicenseAPIView.as_view() ,name='mstLicense'),
    path(r'v1/mstData/mstOccupation', views.MstOccupationAPIView.as_view() ,name='mstOccupation'),


    path(r'v1/search', views.SearchAPIView.as_view() ,name='search'),
    path(r'v1/contactHistory', views.ContactHistoryAPIView.as_view() ,name='contactHistory'),
    path(r'v1/matchCareer', views.MatchCareerAPIView.as_view() ,name='matchCareer'),
    path(r'v1/customTel', views.CustomTelAPIView.as_view() ,name='customTel'),
    path(r'v1/keepClient', views.KeepClientAPIView.as_view() ,name='keepClient'),
    path(r'v1/getOrder', views.TrnOrderViewSet.as_view() ,name='order'),
    path(r'v1/searchHistory', views.TrnSearchLatestHistoryViewSet.as_view() ,name='searchHistory'),
    path(r'v1/searchParameter', views.TrnSearchParameterViewSet.as_view() ,name='searchParameter'),
    path(r'v1/getCareer', views.GetCareerAPIView.as_view() ,name='career'),
]