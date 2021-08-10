from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf.urls.static import static
from django.conf import settings

from medi_app import views

# Routes for api goes here..
router = routers.DefaultRouter()
router.register("company", views.CompanyViewSet, basename="company")
router.register("companybank", views.CompanyBankViewSet, basename="companybank")
router.register("companyaccount", views.CompanyAccountViewSet, basename="companyaccount")
router.register("medicine", views.MedicineViewSet, basename="medicine")
router.register("employee", views.EmployeeViewSet, basename="employee")
router.register("employeesalary", views.EmployeeSalaryViewSet, basename="employeesalary")
router.register("employeebank", views.EmployeeBankViewSet, basename="employeebank")
router.register("generate_bill_api", views.GenerateBillViewSet, basename="generate_bill_api")
router.register("customer_request", views.CustomerRequestViewSet, basename="customer_request")
router.register("homepage_data", views.HomePageViewSet, basename="homepage_data")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/gettoken/', TokenObtainPairView.as_view(), name='gettoken'),
    path('api/refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/companybyname/<str:name>/', views.CompanyNameViewSet.as_view(), name='companybyname'),
    path('api/companyonly/', views.CompanyOnlyViewSet.as_view(), name='companyonly'),
    path('api/medicinebyname/<str:name>/', views.MedicinebByNameViewSet.as_view(), name='medicinebyname'),
    path('api/employee_salaryby_id/<str:employee_id>/', views.EmployeeSalaryByEIDViewSet.as_view(), name='employee_salaryby_id'),
    path('api/employee_bankby_id/<str:employee_id>/', views.EmployeeBankByEIDViewSet.as_view(), name='employee_bankby_id'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


