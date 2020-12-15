from csvgen.celery import app
from .models import Schemas, CsvFile
from .fakegen import *
import csv
from datetime import datetime
from django.http import HttpResponsePermanentRedirect
from django.http import JsonResponse

@app.task
def csv_generator(rows, id):
    schema = Schemas.objects.get(pk=id)
    # print(schema, "PRINT")
    fields = schema.fields.strip("[]").split("),")
    for i in range(len(fields)):
        fields[i] = fields[i].strip(" ()")
        fields[i] = fields[i].split(", ")
    fields.sort(key=lambda field: int(field[5].strip("'")))

    gens = {
        "integer": integer_gen,
        "date": date_gen,
        "phone": phone_gen,
        "email": email_gen,
        "name": name_gen,
        "address": address_gen,
        "domain": domain_gen,
        "job": job_gen,
        "company": company_gen,
        "text": text_gen
    }
    filename = str(id) + "_" + str(rows) + '.csv'
    with open(filename, 'w', newline='', encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow(["sep=,"])
        names = []
        for i in range(len(fields)):
            names.append(fields[i][0].strip("'"))
        # print(names)

        writer.writerow(names)
        types = []
        for i in range(len(fields)):
            if fields[i][1].strip("'") == "integer":
                types.append("/".join([fields[i][1].strip("'"), fields[i][2].strip("'"), fields[i][3].strip("'")]))
            elif fields[i][1].strip("'") == "text":
                types.append("/".join([fields[i][1].strip("'"), fields[i][4].strip("'")]))
            else:
                types.append(fields[i][1].strip("'"))
        # print(types)

        for i in range(rows):
            add = []
            for type in types:
                if "integer" in type:
                    int_split = type.split("/")
                    gen = gens[int_split[0]]
                    add.append(gen(int(int_split[1]), int(int_split[2])))
                elif "text" in type:
                    text_split = type.split("/")
                    gen = gens[text_split[0]]
                    add.append(gen(int(text_split[1])))
                else:
                    gen = gens[type]
                    add.append(gen())
            # print(add)
            writer.writerow(add)
        ready = CsvFile.objects.get(filename=filename)
        ready.is_ready = True
        ready.save()
        return True