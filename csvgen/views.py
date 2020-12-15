from django.shortcuts import render
import csv
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Schemas, CsvFile
from .fakegen import *
from datetime import datetime
from .forms import AddForm, FullAddForm, RowForm
from .tasks import csv_generator
from wsgiref.util import FileWrapper
import os
from FakeCSV.settings import BASE_DIR

def logout_view(request):
    """Log out and redirect to home(log in form)"""
    logout(request)
    return HttpResponsePermanentRedirect("/")


class HomeView(LoginRequiredMixin, ListView):
    """Home page with user schemas list"""
    model = Schemas

    def get_queryset(self):
        """admin can see all schemas, user only his own"""
        if self.request.user.is_staff:
            return Schemas.objects.all()
        else:
            return Schemas.objects.filter(user=self.request.user)


class NewView(LoginRequiredMixin, View):
    """New Schema page"""
    add_list = list()


    def post(self, request):
        """Rendering with new columns"""
        print(request.POST, "POST")
        form = AddForm(request.POST)
        if form.is_valid():
            add_data = request.POST
            self.add_list.append(form)
            print(self.add_list, "LIST")
            return render(request, "csvgen/schemas_form.html", {"form": AddForm,
                                                                'list': self.add_list,
                                                                'form2': FullAddForm})
        else:
            return HttpResponse("form not valid")


    def get(self, request):
        """render page with forms"""
        self.add_list.clear()
        data = {"form": AddForm, "form2": FullAddForm}
        return render(request, "csvgen/schemas_form.html", context=data)

    def delete(self, request):
        print("DELETE")


class AddSchemaFormView(LoginRequiredMixin, View):

    def post(self, request):
        """Creating new schema and redirect to homepage"""
        # print(request.POST, "POST ADD")
        data = dict(request.POST)
        fields = []

        ints = []
        texts = []

        index1 = 0
        index2 = 0
        # creating tuples (<index of integer type>, <it from\to values index>)
        # Example >> 'Type': ['date', 'date', 'integer', 'phone', 'integer'],
        # 'Order': ['0', '1', '2', '3', '4'], 'From': ['1', '1'], 'To': ['2', '3']}
        # will be [(2, 0), (5, 1)]
        for i in range(len(data["Type"])):
            if data["Type"][i] == "integer":
                ints.append((i, index1))
                index1 += 1
            if data["Type"][i] == "text":
                texts.append((i, index2))
                index2 += 1
        # creating model Schemas and add to DB
        for i in range(len(data["Column_name"])):
            if "integer" == data["Type"][i]:
                for tuples in ints:
                    print(tuples, "_", i)
                    if tuples[0] == i:
                        int_index = tuples[1]
                print(ints)
                tmp = (data["Column_name"][i], data["Type"][i], data.get("From")[int_index],
                       data.get("To")[int_index], None, data["Order"][i])
            elif "text" == data["Type"][i]:
                for tuples in texts:
                    if tuples[0] == i:
                        txt_index = tuples[1]
                tmp = (data["Column_name"][i], data["Type"][i], None,
                       None, data.get("Sentences")[txt_index], data["Order"][i])
            else:
                tmp = (data["Column_name"][i], data["Type"][i], None,
                       None, None, data["Order"][i])
            fields.append(tmp)
        schema = Schemas(title=request.POST["Name"],
                         Post_date=datetime.now().date(),
                         user=self.request.user,
                         fields=str(fields))
        schema.save()
        return HttpResponsePermanentRedirect("/")


class EditView(LoginRequiredMixin, View):


    def get(self, request, id, *args, **kwargs):
        csvs = CsvFile.objects.filter(schema_id=id)
        return render(request, "edit_schema.html", {'form': RowForm, "id": id, "csvs": csvs})



class CreateCsvView(LoginRequiredMixin, View):

    def post(self, request):
        rows = int(request.POST["row"])
        id = request.META.get("HTTP_REFERER")
        id = id.split("/")[-2]

        # starting celery task
        csv_generator.delay(rows, id)
        filename = str(id) + "_" + str(rows) + '.csv'
        to_save = CsvFile(filename=filename, create_date=datetime.now().date(), schema_id=id, is_ready=0)
        to_save.save()
        return HttpResponsePermanentRedirect("/edit/" + id + "/")


class CsvDownload(LoginRequiredMixin, View):

    def get(self, request, filename):
        file_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='text/csv')
                response['Content-Disposition'] = 'inline; filename=' + file_path
                return response


class DeleteSchema(LoginRequiredMixin, View):

    def get(self, request, id):
        Schemas.objects.get(pk=id).delete()
        return HttpResponsePermanentRedirect("/")


