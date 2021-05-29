from django.shortcuts import render,HttpResponse,redirect
from smartler import schedule
import urllib

def gethmformat(tm):
    h,m=tm.split(":")
    h, m = int(h), int(m)
    m = round(m / 0.6)
    return float(f"{h}.{m}")

def getnumformat(strlist):
    x=[float(x) for x in strlist]
    return x

def tolist(strlist):
    x=strlist.split("'")
    l=list()
    for i in range(1,len(x),2):
        l.append(x[i])
    return(l)
    
def formattime(strlist):
    x=strlist.strip("[]").replace("], [",";").split(";")
    y=[a.split(", ") for a in x]
    l=list()
    for x in y:
        temp=[float(x[0]),float(x[1])]
        l.append(temp)
    return l
def index(request):
    if request.method=="POST":
        print("posted values")
        start = request.POST.get("start")
        end = request.POST.get("end")
        name = request.POST.get("name")
        print(start,end,name)
        context={'start_task':start,'end_task':end,'name':name}
        return redirect('/task?'+urllib.parse.urlencode(context))
    else:
        return render(request,"index.html")
# Create your views here.
       


def task(request):
    if request.method=="POST":
        no_of_tasks=request.POST.get("no_of_tasks")
        start = request.POST.get("start_task")
        end = request.POST.get("end_task")
        tasks=list()
        rate=list()
        if no_of_tasks=="None" or no_of_tasks=="":
            return HttpResponse("alert('Come on now! Don't make fun of me, Tell me your Tasks!')")
        else:
            for x in range(int(no_of_tasks)):
                tasks.append(request.POST.get(f"task_{x}")[:-3])
                rate.append(request.POST.get(f"task_{x}")[-2])
        print("in task:POST")
        print(tasks,rate)
        
        context={'start_task':start,'end_task':end,'tasklist':tasks,'rate':rate}
        return redirect('/fixed?'+urllib.parse.urlencode(context))
        # return render(request,"fixed.html",{'start_task':start,'end_task':end,'tasklist':tasks,'rate':rate})
    elif request.method=="GET":
        print("in get task")
        start = request.GET.get("start_task")
        end = request.GET.get("end_task")
        name = request.GET.get("name")
        return render(request,"task.html",{'start_task':start,'end_task':end,'name':name})
    else:
        print("in else task")
        return HttpResponse(request,"<h2>Something went wrong!</h2>")
    
def fixed(request):
    if request.method=="POST":
        no_of_fix = request.POST.get("no_of_fix")
        start = request.POST.get("start_task")
        end = request.POST.get("end_task")
        fixname=list()
        fixtime=list()
        tasklist=request.POST.get("tasklist")
        rate=request.POST.get("rate")
        print(tasklist,rate)
        if no_of_fix=="":
            fixname=[]
            fixtime=[]
        else:
            for x in range(int(no_of_fix)):
                fixname.append(request.POST.get(f"fix_{x}")[:-13])
                v=request.POST.get(f"fix_{x}")[-13:]
                fixtime.append([gethmformat(v.split(",")[0][1:]),gethmformat(v.split(",")[1][:-1])])
        # return render(request,"schedular.html",{'tasklist':tasklist,'rate':rate})
        context={'tasklist':tasklist,'rate':rate,'fixname':fixname,'fixtime':fixtime,'start_task':start,'end_task':end}
        print(tasklist,rate,fixname,fixtime)
        return redirect('/schedular?'+ urllib.parse.urlencode(context))
    elif request.method=="GET":
        start=request.GET.get("start_task")
        end=request.GET.get("end_task")
        tasklist=request.GET.get("tasklist")
        rate=request.GET.get("rate")
        return render(request,'fixed.html',{'start_task':start,'end_task':end,'tasklist':tasklist,'rate':rate})
    else:
        return HttpResponse("<h2>Something went wrong</h2>")
    
def schedular(request):
    if request.method=="GET":
        tasks=request.GET.get("tasklist")
        rate=request.GET.get("rate")
        fixname=request.GET.get("fixname")
        fixtime=request.GET.get("fixtime")
        start = request.GET.get("start_task")
        end = request.GET.get("end_task")
        if len(tasks)==0:
            return HttpResponse("alert('You entered Wrong Info! Please go back and Recheck')")
        else:
            tasks=tolist(tasks)
            rate=[int(x) for x in tolist(rate)]
        if len(fixname)==0:
            fixname=[]
            fixtime=[]
        else:
            fixname=tolist(fixname)
            fixtime=formattime(fixtime)

        start=gethmformat(start)
        end=gethmformat(end)
        rate=getnumformat(rate)

        
        values=f"start: {start} and end: {end} \n task: {tasks}  and rate: {rate} \n fixname: {fixname} and fixtime: {fixtime}"
        display=schedule(tasks, rate, fixname, fixtime, start, end)
        return render(request,"schedular.html",{'schedule':display})
        
    else:
        return HttpResponse("<h2>Something went wrong!</h2>")
 
def oldtask(request):
    
    if request.method=="POST":
        # we ge time from here
        no_of_tasks=request.POST.get("no_of_tasks")
        no_of_fix = request.POST.get("no_of_fix")
        start = request.POST.get("start_task")
        end = request.POST.get("end_task")
        tasks=list()
        rate=list()
        fixname=list()
        fixtime=list()
        print("running")
        for x in range(int(no_of_tasks)):
            tasks.append(request.POST.get(f"task_{x}")[:-3])
            rate.append(request.POST.get(f"task_{x}")[-2])

        for x in range(int(no_of_fix)):
            fixname.append(request.POST.get(f"fix_{x}")[:-13])
            v=request.POST.get(f"fix_{x}")[-13:]
            fixtime.append([gethmformat(v.split(",")[0][1:]),gethmformat(v.split(",")[1][:-1])])
        
        # t=request.POST.get("task_0")
        # print(t)
                # calculating start and end in the format
        start=gethmformat(start)
        end=gethmformat(end)
        rate=getnumformat(rate)


                # gets formatted input
        print(f"start: {start} and end: {end}")
        print(f"task: {tasks} and rate: {rate}")
        print(f"fixname: {fixname} and fixtime: {fixtime}")

        display=schedule(tasks, rate, fixname, fixtime, start, end)
        return render(request, "index.html",{"result":display})
        # except:
        #     return render(request, "index.html",{'alert':'<script>alert("Whoops! Something went Wrong!");</script>'})

    elif request.method=="GET":
        start = request.GET.get("start")
        end = request.GET.get("end")
        name = request.GET.get("name")
        return render(request,"index.html",{'start_task':start,'end_task':end,'name':name})
    else:
        return render(request, "index.html")
