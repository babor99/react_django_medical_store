import datetime
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from .serializers import *

# Create your views here.
class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True, context={"request":request})
        response_dict = {"error":False, "message":"All company list data", "data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message": "Company data saved successfully"}
        except:
            dict_response = {"error":True, "message": "Error during saving company data"}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company, context={"request":request})
 
        # fetching medicine_details with single midicine data
        serializer_data = serializer.data
        company_bank_details = CompanyBank.objects.filter(company_id= serializer_data["id"])
        company_bank_details_serializers = CompanyBankSerializer(company_bank_details, many=True)
        serializer_data["company_bank"] = company_bank_details_serializers.data
         
        return Response({"error":False, "message":"Single data fetch", "data": serializer_data})


    def update(self, request, pk=None):
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company, data=request.data, context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message":"Successfully updated company data"}
        except:
            dict_response = {"error":True, "message":"Error during updating company data"}

        return Response(dict_response)


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return Company.objects.filter(name=name)


class CompanyOnlyViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all()


class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CompanyBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message": "CompanyBank data saved successfully"}
        except:
            dict_response = {"error":True, "message": "Error during saving companybank data"}
        return Response(dict_response)
    
    def list(self, request):
        companybank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(companybank, many=True, context={"request":request})
        response_dict = {"error":False, "message":"All company bank list data", "data":serializer.data}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(companybank, context={"request":request})
        return Response({"error":False, "message":"Single data fetch", "data":serializer.data})

    def update(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        companybank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(companybank, data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"error":False, "message":"CompanyBank data has been updated"})


class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Saving MedicalDetail data in MedicineViewset
            medicine_id = serializer.data["id"]
            print("medicine_id",medicine_id)

            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                print("medical_detail",medicine_detail)
                medicine_detail["medicine_id"] = medicine_id
                medicine_details_list.append(medicine_detail)
                print("lists",medicine_details_list)

            serializer2 = MedicalDetailSerializer(data=medicine_details_list, many=True, context={"request":request})
            serializer2.is_valid()
            serializer2.save()

            dict_response = {"error":False, "message": "Medicine data saved successfully"}
        except Exception as e:
            print(e)
            dict_response = {"error":True, "message": "Error during saving Medicine data"}
        return Response(dict_response)
    
    def list(self, request):
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine, many=True, context={"request":request})

        # fetching medicine_details in medicine list
        medicine_data = serializer.data
        new_medicine_list = []
        for medicine in medicine_data:
            medicine_details = MedicalDetail.objects.filter(medicine_id= medicine["id"])
            medicine_details_serializers = MedicalDetailSerializerSimple(medicine_details, many=True)
            medicine["medicine_details"] = medicine_details_serializers.data
            new_medicine_list.append(medicine)

        response_dict = {"error":False, "message":"All Medicine list data", "data":new_medicine_list}
        return Response(response_dict)

    def retrieve(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, context={"request":request})

        # fetching medicine_details with single midicine data
        serializer_data = serializer.data
        medicine_details = MedicalDetail.objects.filter(medicine_id= serializer_data["id"])
        medicine_details_serializers = MedicalDetailSerializerSimple(medicine_details, many=True)
        serializer_data["medicine_details"] = medicine_details_serializers.data

        return Response({"error":False, "message":"Single data fetch", "data": serializer_data})

    def update(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        print(request.data)
        serializer = MedicineSerializer(medicine, data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        for salt_detail in request.data['medicine_details']:
            
            if salt_detail['id'] == 0:
                del salt_detail['id']
                salt_detail['medicine_id'] = serializer.data['id']
                serializer2 = MedicalDetailSerializer(data=salt_detail, context={"request":request})
                serializer2.is_valid()
                serializer2.save()
            else:
                queryset2 = MedicalDetail.objects.all()
                medicine_salt = get_object_or_404(queryset2, pk=salt_detail['id'])
                serializer3 = MedicalDetailSerializer(medicine_salt, data=salt_detail, context={"request":request})
                serializer3.is_valid()
                serializer3.save()

        return Response({"error":False, "message":"Medicine data has been updated"})


class MedicinebByNameViewSet(generics.ListAPIView):
    serializer_class = MedicineSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return Medicine.objects.filter(name__contains=name)


class CompanyAccountViewSet(viewsets.ViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        companyaccount = CompanyAccount.objects.all()
        serializer = CompanyAccountSerializer(companyaccount, many=True, context={"request":request})
        response_dict = {"error":False, "message":"All Company Account list data", "data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CompanyAccountSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message": "Company Account data saved successfully"}
        except:
            dict_response = {"error":True, "message": "Error during saving Company Account data"}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = CompanyAccount.objects.all()
        companyaccount = get_object_or_404(queryset, pk=pk)
        serializer = CompanyAccountSerializer(companyaccount, context={"request":request})
         
        return Response({"error":False, "message":"Single Company Account data fetch", "data": serializer_data})


    def update(self, request, pk=None):
        try:
            queryset = CompanyAccount.objects.all()
            companyaccount = get_object_or_404(queryset, pk=pk)
            serializer = CompanyAccountSerializer(companyaccount, data=request.data, context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message":"Successfully updated Company Account data"}
        except:
            dict_response = {"error":True, "message":"Error during updating Company Account data"}

        return Response(dict_response)


class EmployeeViewSet(viewsets.ViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True, context={"request":request})
        response_dict = {"error":False, "message":"All Employee list data", "data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data, context={"request": request})
            print(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message": "Employee data saved successfully"}
        except Exception as e:
            print(e)
            dict_response = {"error":True, "message": "Error during saving Employee data"}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = Employee.objects.all()
        employee = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSerializer(employee, context={"request":request})
         
        return Response({"error":False, "message":"Single Employee data fetch", "data": serializer.data})


    def update(self, request, pk=None):
        try:
            queryset = Employee.objects.all()
            employee = get_object_or_404(queryset, pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data, context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message":"Successfully updated Employee data"}
        except:
            dict_response = {"error":True, "message":"Error during updating Employee data"}

        return Response(dict_response)


class EmployeeBankViewSet(viewsets.ViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        employeebank = EmployeeBank.objects.all()
        serializer = EmployeeBankSerializer(employeebank, many=True, context={"request":request})
        response_dict = {"error":False, "message":"All Employee Bank list data", "data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = EmployeeBankSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message": "Employee Bank data saved successfully"}
        except Exception as e:
            dict_response = {"error":True, "message": "Error during saving Employee Bank data"}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = EmployeeBank.objects.all()
        employeebank = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeBankSerializer(employeebank, context={"request":request})
         
        return Response({"error":False, "message":"Single Employee Bank data fetch", "data": serializer_data})


    def update(self, request, pk=None):
        try:
            queryset = EmployeeBank.objects.all()
            employeebank = get_object_or_404(queryset, pk=pk)
            serializer = EmployeeBankSerializer(employeebank, data=request.data, context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message":"Successfully updated Employee Bank data"}
        except:
            dict_response = {"error":True, "message":"Error during updating Employee Bank data"}

        return Response(dict_response)


class EmployeeSalaryViewSet(viewsets.ViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        employeesalary = EmployeeSalary.objects.all()
        serializer = EmployeeSalarySerializer(employeesalary, many=True, context={"request":request})
        response_dict = {"error":False, "message":"All Employee Salary list data", "data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = EmployeeSalarySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message": "Employee Salary data saved successfully"}
        except Exception as e:
            dict_response = {"error":True, "message": "Error during saving Employee Salary data"}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = EmployeeSalary.objects.all()
        employeesalary = get_object_or_404(queryset, pk=pk)
        serializer = EmployeeSalarySerializer(employeesalary, context={"request":request})
         
        return Response({"error":False, "message":"Single Employee Salary data fetch", "data": serializer.data})


    def update(self, request, pk=None):
        try:
            queryset = EmployeeSalary.objects.all()
            employeesalary = get_object_or_404(queryset, pk=pk)
            serializer = EmployeeSalarySerializer(employeesalary, data=request.data, context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message":"Successfully updated Employee Salary data"}
        except:
            dict_response = {"error":True, "message":"Error during updating Employee Salary data"}

        return Response(dict_response)


class EmployeeBankByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeBankSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return EmployeeBank.objects.filter(employee_id=employee_id)


class EmployeeSalaryByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeSalarySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return EmployeeSalary.objects.filter(employee_id=employee_id)


class GenerateBillViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            serializer = CustomerSerializer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            customer_id = serializer.data["id"]

            bill_data = {}
            bill_data['customer_id'] = customer_id

            serializer2 = BillSerializer(data=bill_data, context={"request": request})
            serializer2.is_valid()
            serializer2.save()
            bill_id = serializer2.data["id"]

            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                medicine_detail1 = {} 
                medicine_detail1["bill_id"] = bill_id
                medicine_detail1["medicine_id"] = medicine_detail['id']
                medicine_detail1["qty"] = medicine_detail['qty']
                medicine_details_list.append(medicine_detail1)

                #update the in stock quantity
                medicine_to_deduct = Medicine.objects.get(id=medicine_detail['id'])
                medicine_to_deduct.in_stock_total = int(medicine_to_deduct.in_stock_total) - int(medicine_detail['qty'])
                medicine_to_deduct.save()

            serializer3 = BillDetailSerializer(data=medicine_details_list, many=True, context={"request":request})
            serializer3.is_valid()
            serializer3.save()

            dict_response = {"error":False, "message": "Bill Generated successfully"}
        except:
            dict_response = {"error":True, "message": "Error during generating Bill"}
        return Response(dict_response)


class CustomerRequestViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customer_request = CustomerRequest.objects.all()
        serializer = CustomerRequestSerializer(customer_request, many=True, context={"request":request})
        response_dict = {"error":False, "message":"All Customer Request list", "data":serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = CustomerRequestSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message": "Customer Request saved successfully"}
        except:
            dict_response = {"error":True, "message": "Error during saving Customer Request"}
        return Response(dict_response)


    def retrieve(self, request, pk=None):
        queryset = CustomerRequest.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = CustomerRequestSerializer(customer_request, context={"request":request})
         
        return Response({"error":False, "message":"Single data fetch", "data": serializer.data})


    def update(self, request, pk=None):
        try:
            queryset = CustomerRequest.objects.all()
            customer_request = get_object_or_404(queryset, pk=pk)
            serializer = CustomerRequestSerializer(customer_request, data=request.data, context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error":False, "message":"Successfully updated Customer Request data"}
        except:
            dict_response = {"error":True, "message":"Error during updating Customer Request data"}

        return Response(dict_response)


class HomePageViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customer_request = CustomerRequest.objects.all()
        cr_serializer = CustomerRequestSerializer(customer_request, many=True, context={"request":request})
        cr = len(cr_serializer.data)

        bill = Bill.objects.all()
        bill_serializer = BillSerializer(bill, many=True, context={"request":request})
        bills = len(bill_serializer.data)

        medicine = Medicine.objects.all()
        medicine_serializer = MedicineSerializer(medicine, many=True, context={"request":request})
        medicines = len(medicine_serializer.data)

        company = Company.objects.all()
        company_serializer = CompanySerializer(company, many=True, context={"request":request})
        companies = len(company_serializer.data)

        employee = Employee.objects.all()
        employee_serializer = EmployeeSerializer(employee, many=True, context={"request":request})
        employees = len(employee_serializer.data)
        
        completed_request = CustomerRequest.objects.filter(status=True)
        completed_request_serializer = CustomerRequestSerializer(completed_request, many=True, context={"request":request})
        completed_requests = len(completed_request_serializer.data)
        
        pending_request = CustomerRequest.objects.filter(status=False)
        pending_request_serializer = CustomerRequestSerializer(pending_request, many=True, context={"request":request})
        pending_requests = len(pending_request_serializer.data)

        #total profit calculation
        bill_details = BillDetail.objects.all()
        bill_details_serializer = BillDetailSerializer(bill_details, many=True, context={"request":request})
        bill_details_data = bill_details_serializer.data
        total_buy_cost = 0
        total_sell_amount = 0
        for bill_detail in bill_details_data:
            total_buy_cost += int(bill_detail['medicine']['buy_price']) * int(bill_detail['qty'])
            total_sell_amount += int(bill_detail['medicine']['sell_price']) * int(bill_detail['qty'])
        total_profit = total_sell_amount - total_buy_cost
        
        #total profit calculation for today
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        today_bill_details = BillDetail.objects.filter(added_on__date=today)
        today_bill_details_serializer = BillDetailSerializer(today_bill_details, many=True, context={"request":request})
        today_bill_details_data = today_bill_details_serializer.data
        today_buy_cost = 0
        today_sell_amount = 0
        for today_bill_detail in today_bill_details_data:
            today_buy_cost += int(today_bill_detail['medicine']['buy_price']) * int(today_bill_detail['qty'])
            today_sell_amount += int(today_bill_detail['medicine']['sell_price']) * int(today_bill_detail['qty'])
        today_profit = today_sell_amount - today_buy_cost

        #medicine expires in a week
        days_7 = datetime.datetime.today() + datetime.timedelta(days=7)
        a_week_later = days_7.strftime("%Y-%m-%d")
        medicine = Medicine.objects.filter(expire_date__range=[today, a_week_later])
        medicine_serializer = MedicineSerializer(medicine, many=True, context={"request":request})
        medicines_expires_in_week = len(medicine_serializer.data)

        #calculations for charts
        bill_dates = BillDetail.objects.order_by().values('added_on__date').distinct()
        profit_chart_list = []
        buy_chart_list = []
        sell_chart_list = []
        for bill_date in bill_dates:
            access_date = bill_date['added_on__date']
            bill_data = BillDetail.objects.filter(added_on__date=access_date)

            profit_amt_inner = 0
            buy_amt_inner = 0
            sell_amt_inner = 0
            for bill_single in bill_data:
                print(bill_single)
                buy_amt_inner += int(bill_single.medicine_id.buy_price) * int(bill_single.qty)
                sell_amt_inner += int(bill_single.medicine_id.sell_price) * int(bill_single.qty)
                profit_amt_inner = sell_amt_inner - buy_amt_inner
            profit_chart_list.append({'date':access_date, 'amount':profit_amt_inner})
            buy_chart_list.append({'date':access_date, 'amount':buy_amt_inner})
            sell_chart_list.append({'date':access_date, 'amount':sell_amt_inner})


        response_dict = {"error":False, "message":"Home Page data", "customer_requests":cr, "total_sales":bills,
        "total_medicines":medicines, "total_companies":companies, "total_employees":employees,
        "completed_requests":completed_requests, "pending_requests":pending_requests, 
        "total_profit":total_profit, "total_sales_amount":total_sell_amount, "today_sales_profit":today_profit,
        "today_sales_amount":today_sell_amount, "medicines_expires_in_week":medicines_expires_in_week,
        "profit_chart":profit_chart_list, "buy_chart":buy_chart_list, "sell_chart":sell_chart_list}
        return Response(response_dict)



company_list = CompanyViewSet.as_view({"get":"list"})
company_create = CompanyViewSet.as_view({"post":"create"})
company_update = CompanyViewSet.as_view({"put":"update"})

    