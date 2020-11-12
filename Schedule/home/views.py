from home.GA import GA
from django.shortcuts import render
from django.http import HttpResponse
from home.item import Item
from home.GA import GA
import json



def index(request):
    print(request.POST)
    if request.method == 'POST':
        

        MeetingTime = ["7-9", "9-11", "13-15", "15-17"]

        date = request.POST.get("date", "T2,T3,T4").replace(" ", "").split(",")
        gen = int(request.POST.get("gen", "1000"))
        population=int(request.POST.get("population", "50"))
        subPerDay=int(request.POST.get("subPerDay", "5"))
        mutation=float(request.POST.get("mutation", "0.3"))
        classname = request.POST.get("classname", "")
        classname.replace('[', '').replace(']', '').replace('[','')
        classname = classname.split(",")

        teachername = request.POST.get("teachername", "")
        teachername = teachername.replace('[', '').replace(
            ']', '').replace('[', '').replace(" ", "")
        teachername = json.loads(teachername)
        for i in teachername:
            teachername[i] = teachername[i].split(",")

        sub = request.POST.get("sub", "")
        sub = sub.replace('[', '').replace(']', '').replace('[', '')
        sub = json.loads(sub)
        for i in sub:
            sub[i] = int(sub[i])

        #caculator
        
        test = GA(gen, classname, sub, MeetingTime, teachername,
                  date, subPerDay, mutation, population)
        print(gen, classname, sub, MeetingTime, teachername,
              date, subPerDay, mutation, population)
        res,score = test.schedule()
        print(res, score)
        stringdata=''
        for i in res:
            stringdata += ",".join(i)
            stringdata += "/"
        stringdata = stringdata[:-1]
        
        return HttpResponse(stringdata)
    return render(request, 'pages/a.html')
def contact(request):
    print(request.POST)
    return render(request, 'pages/contact.html')

