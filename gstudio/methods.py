from gstudio.models import *
from objectapp.models import *
from django.template.defaultfilters import slugify
from datetime import datetime as date_time
import datetime as date_methds
import os
import shutil
import urllib
from demo.settings import PYSCRIPT_URL_GSTUDIO
from demo.settings import FILE_URL
#from demo.settings import MATHJAX_FILE_URL
from django.contrib.auth.models import User
#from django.contrib.sessions.models import Session
#from notification import notify
from notification import models as notification
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
#from django.contrib.comments.signals import comment_will_be_posted
from django.core.mail import send_mail
from django.contrib.sessions.models import Session
from djangoratings.models import *
lst1=[]
count=0
response_set=[]




def recur_responses(twist):
    global lst1
    lst1=[]
    return get_recur_responses_of_twist(twist)


def get_recur_responses_of_twist(twist):
    postnodes=twist.posterior_nodes.all()
    if postnodes:
        for each in postnodes:
            lst1.append(each)
            get_recur_responses_of_twist(each)
    return lst1
def get_rate_of_object_of_user(user,sysid):
#   us = User.objects.get(username="gnowgi")                                                                                                 
    print "insget",sysid,user
    voteofuser = Vote.objects.filter(user = user)
    rating_made = 0
    #voteofuser.count()                                                                                                                      
    for vote in voteofuser:
        objectofvote = vote.content_object
        if objectofvote.objecttypes.all():
            if objectofvote.objecttypes.all()[0].title=='Reply':
                objectofvoteid = objectofvote.getthread_of_response.id
                if sysid == objectofvoteid:
                    rating_made = rating_made + 1
    return rating_made
def posts_recd_for_subscr(subscrid,thdid):
    usr=User.objects.get(id=subscrid)
    c=0
    sys=System.objects.get(id=thdid)
#   get_twists_of_thread                                                                                                                     
    box=sys.system_set.all()[0]
    twists=box.gbobject_set.all()
    for each in twists:
        getresponses=recur_responses(each)
        for eachres in getresponses:
             if eachres.authors.all()[0]==usr:
               resp=recur_responses(eachres)
               c +=len(resp)
    return c
def get_all_logged_in_users():
    # Query all non-expired sessions                                                                                                        \
                                                                                                                                             
    sessions = Session.objects.filter(expire_date__gte=date_time.now())
    uid_list = []

    # Build a list of user ids from that query                                                                                              \
                                                                                                                                             
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list                                                                                            \
                                                                                                                                             
    return User.objects.filter(id__in=uid_list)

def get_authors_of_response(user,thread):
       count =0
       for each in thread.system_set.all()[0].gbobject_set.all():
           print "threads=",each
           response_set=recur_responses(each)
           print response_set
           for each1 in response_set:
               print each1.authors.all()[0],str(user)
               if str(each1.authors.all()[0])==str(user):
                   count=count+1
       return count

def get_no_of_twist_posted(user,thread):
       sys=System.objects.get(title=thread)
       count=0
       twistset=sys.system_set.all()[0].gbobject_set.all()
       for each1 in twistset:
                     if str(each1.authors.all()[0])==str(user):
                            count=count+1
       return count

def loom_status(pageid):
  retdict={}
  userdet=[]
  thdid=pageid
  #get subscribers                                                                                                                           
  sys=System.objects.get(id=pageid)
  box=sys.system_set.all()[0]
  logged_users=get_all_logged_in_users()
  #get online-offline                                                                                                                        
  print box.member_set.all(),"memset"
  for each in box.member_set.all():
      print each,"-eacch"
      eachuser=User.objects.get(username=each)
      print "eauseR",eachuser
      if eachuser in logged_users:
         userdet.append("green1")
      else:
         userdet.append("grey")
#     get no-of-posts(twist/responses)
#     resps=get_authors_of_response(each,sys)                                                                                              
#     thds=get_no_of_twist_posted(each,sys)                                                                                                
#     strng=str(thds)+"/"+str(resps)                                                                                                        #     userdet.append(strng)                                                                                                                
# #get Ratings user made                                                                                                                   
#     ratngs=get_rate_of_object_of_user(each,sys.id)                                                                                       
#     userdet.append(str(ratngs))                                                                                                          
# #responses his post received                                                                                                             
#     psts=posts_recd_for_subscr(each.id,thdid)                                                                                             #     userdet.append(str(psts))                                                                                                            
      retdict[each.username]=userdet
      userdet=[]
  return retdict



def check_page_exists(pgetocheck):
  fl=0
  getobjs=Gbobject.objects.filter(title=pgetocheck)
  if not getobjs:
      return fl
  else:
      for each in getobjs:
          sysid=System.objects.filter(id=each.id)
          if sysid:
            getob=System.objects.get(id=each.id)
            for eachtitle in getob.systemtypes.all():
                if eachtitle.title=='Wikipage':
                    print "wiki"
                    fl=1 
                    return fl
            fl=2
            return fl
          else:
            fl=2
            return fl
      return fl


def get_threadbox_of_twist(twistid):
 thid=""
 for each in System.objects.all():
        sys_set=each.system_set.all()
        if sys_set:
               sys_set=each.system_set.all()[0]
               for eachsys in sys_set.gbobject_set.all():
                      if eachsys.id==twistid:
                             return sys_set
 return thid

def delete(idnum):
 del_ob = Gbobject.objects.get(id=idnum)
 del_ob.delete()
 return True

def get_pdrawer():
    pagedrawer = []
    pageid=[]
    dict1={}
    #wikiset = Systemtype.objects.all()
    drawerset = Systemtype.objects.get(title="Wikipage")
    drawer= drawerset.member_systems.all()
    
    for each in drawer:
	pagedrawer.append(each.__str__())
	dict1[each.id]=each.__str__()
        
    	
    return dict1


def get_gbobjects(object_id):
    sys=System.objects.get(id=object_id)
    var=sys.in_gbobject_set_of.__dict__['through']
    varobset=[]
    title=[]
    for each in var.objects.all():
        
        if each.system_id == sys.id:
            s=Gbobject.objects.get(id=each.gbobject_id)
            s1=s.title
            varobset.append(s)
    return varobset


def make_rep_object(replytext,auth_id,usr):
 # create new twist response object
 new_ob = Gbobject()
 new_ob.title = "re-"
 new_ob.slug=slugify(new_ob.title)
 # save blank object to get auto generated id
 new_ob.save()
 # titleid contains own id + twist id
 titleid = "re-"+str(new_ob.id)
 contorg = unicode(replytext)
 fname=slugify(titleid)+"-"+usr 
 new_ob.content_org=contorg.encode('utf8')
 ext='.org'
 html='.html'
 # write to file
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(new_ob.content_org)
 myfile.close()

 # read again to remove carriage return character
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")

 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 # read 
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 # remove header content information
 data2 = data1[107:]
 
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]

 newdata=""
 for line in data3:
        newdata += line.lstrip()
 new_ob.content = newdata
 new_ob.title = "re-"
 new_ob.status = 2
 # changed to have format like re-102486-Title_of_twist
 new_ob.slug = slugify(fname)
 new_ob.title= str(replytext[0:50]) + fname
 new_ob.save()
 new_ob.slug = new_ob.slug + "-" + str(new_ob.id)
 new_ob.save()
 # cause new_ob to be  a member of Reply object type  
 new_ob.objecttypes.add(Objecttype.objects.get(title="Reply"))
 new_ob.authors.add(Author.objects.get(id=auth_id))
 new_ob.sites.add(Site.objects.get_current())
 return new_ob

def edit_section(sec_id,title,usr,isPreview):
 
 new_ob = Gbobject.objects.get(id=int(sec_id))
 contorg = unicode(title)
 new_ob.content_org=contorg.encode('utf8')
 ssid=new_ob.get_ssid.pop()
 fname=str(ssid)+"-"+usr
 boolean=False
 boolean=isPreview
 ext='.org'
 html='.html'
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(new_ob.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 #myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 #myfile.write("\n#+MATHJAX: align:"left" path:MATHJAX_FILE_URL mathml:t")
 
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 
 output = stdout.read()
 # if boolean:
     
 #     os.system("firefox /tmp/beta/%s"%(fname+html))
 #     data = open(os.path.join(FILE_URL,fname+html))
 #     data1 = data.readlines()
 #     data2 = data1[86:]
 #     dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 #     data3 = data2[:-6]
 #     newdata=""
 #     for line in data3:
 #         newdata += line.lstrip()
 #     print newdata

# else:
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[86:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
     newdata += line.lstrip()
     new_ob.content = newdata
     new_ob.save()
 return True


def make_topic_object(title,auth_id,content,usr):
 new_ob = Gbobject()
 new_ob.title = "Twist: " + title
 contorg = unicode(content)
 fname=slugify(title)+"-"+usr
 new_ob.content_org=contorg.encode('utf8') 
 ext='.org'
 html='.html'
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(new_ob.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 #myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[107:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 new_ob.content = newdata
 new_ob.status = 2
 new_ob.slug = slugify(title)
 
 new_ob.save()
 new_ob.slug = new_ob.slug + "-" + str(new_ob.id)
 new_ob.save()
 new_ob.objecttypes.add(Objecttype.objects.get(title="Topic"))
 new_ob.authors.add(Author.objects.get(id=auth_id))
 new_ob.sites.add(Site.objects.get_current())
 return new_ob

def make_sectionreply_object(content_org,title,auth_id,usr):
 new_ob = Gbobject()
 new_ob.title = title
 new_ob.status = 2
 new_ob.slug = slugify(title)
 contorg = unicode(content_org)
 fname=slugify(title)+"-"+usr

 new_ob.content_org=contorg.encode('utf8')
 ext='.org'
 html='.html'
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(new_ob.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 #myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[107:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 new_ob.content = newdata
 myfile = open('/tmp/file.org', 'w')
 # myfile.write(new_ob.content_org)
 # myfile.close()
 new_ob.save()
 new_ob.slug = new_ob.slug + "-" + str(new_ob.id)
 new_ob.save()
 new_ob.objecttypes.add(Objecttype.objects.get(title="Subsection"))
 new_ob.authors.add(Author.objects.get(id=auth_id))
 new_ob.sites.add(Site.objects.get_current())
 return new_ob


def make_section_object(title,auth_id,content_org,usr):
 new_ob = Gbobject()
 new_ob.title = title
 new_ob.status = 2
 new_ob.slug = slugify(title)
 fname=slugify(title)+"-"+usr
 #new_ob.content = content
 contorg = unicode(content_org)
 new_ob.content_org=contorg.encode('utf8')
 ext='.org'
 html='.html'
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(new_ob.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 #myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[107:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 new_ob.content = newdata
 new_ob.save()
 new_ob.slug = new_ob.slug + "-" + str(new_ob.id)
 new_ob.save()
 new_ob.objecttypes.add(Objecttype.objects.get(title="Section"))
 new_ob.authors.add(Author.objects.get(id=auth_id))
 new_ob.sites.add(Site.objects.get_current())
 return new_ob


def make_relation(rep,id_no,idusr,usr):
 r = make_rep_object(rep,idusr,usr)
 t = Gbobject.objects.get(id=id_no)
 t.posterior_nodes.add(r)
 r.prior_nodes.add(t)
 r.title="Re:"+str(r.id)+t.title
 r.slug=slugify(r.title)
 r.save()
 return True

def make_sectionrelation(rep,ptitle,id_no,idusr,usr):
 r = make_sectionreply_object(rep,ptitle,idusr,usr)
 t = Gbobject.objects.get(id=id_no)
 t.posterior_nodes.add(r)
 r.prior_nodes.add(t)
 return True


def rate_it(topic_id,request,rating):
 ob = Gbobject.objects.get(id=topic_id)
 ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
 return True

def rate_section(section_id,request,rating):
 ob = Gbobject.objects.get(id=section_id)
 ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
 return True



def create_meeting(title,idusr,content,usr):
 sys = System()
 sys.title = title
 sys.status = 2
 contorg = unicode(content)
 sys.content_org=contorg.encode('utf8')
 fname=slugify(title)+"-"+usr
 ext='.org'
 html='.html'
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(sys.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
# myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[107:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 sys.content = newdata
 sys.slug = slugify(title)
 sys.save()
 sys.slug = sys.slug + "-" + str(sys.id)
 sys.save()
 sys.systemtypes.add(Systemtype.objects.get(title="Meeting"))
 sys.authors.add(Author.objects.get(id=idusr))
 
# a = Attribute()
# a.title = "released button of " + title
# a.slug = slugify(a.title)
# a.content = a.slug
# a.status = 2
# a.subject = sys
# a.svalue = "False"
# a.attributetype_id = Attributetype.objects.get(title="release").id
# a.save()
 sys1 = System()
 sys1.title = "message box of " + title
 sys1.status = 2
 sys1.content = "contains messages of " + title
 sys1.slug = "message_box_of_" + slugify(title)
 sys1.save()
 sys1.slug = sys1.slug + "-" + str(sys1.id)
 sys1.save()
 sys1.systemtypes.add(Systemtype.objects.get(title="message_box"))
 sys.system_set.add(sys1)
 sys.member_set.add(Author.objects.get(id=idusr))
 sys.sites.add(Site.objects.get_current())
 sys1.sites.add(Site.objects.get_current())
 return sys.id 

def create_wikipage(title,idusr,content_org,usr,collection,list1,status):
 sys = System()
 sys.title = title
 if status:
     sys.status = 1
 else:
     sys.status = 2
 boolean=False
 boolean=collection

 list1=list1.split(",")
 contorg =content_org
 contorg=urllib.unquote_plus(contorg)
 sys.content_org=contorg.encode('utf8')+"\n\n"
 ext='.org'
 html='.html'
 fname=slugify(title)+"-"+usr
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(sys.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 #reptext=MATHJAX_FILE_URL
 #findtext="http://orgmode.org/mathjax/MathJax.js"
 #if findtext in newcontent:
  #      newcontent=newcontent.replace(findtext,reptext)
 
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 #myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[86:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 sys.content = newdata
 sys.slug = slugify(title)
 sys.save()
 i=0
 if boolean:
        while i<len(list1):
               s= str(list1[i])
               s=s.replace("'","")
               objs=Gbobject.objects.get(title=s)
               sys.gbobject_set.add(objs)
               i=i+1
               
 sys.systemtypes.add(Systemtype.objects.get(title="Wikipage"))
 if boolean:
        sys.systemtypes.add(Systemtype.objects.get(title="Collection"))
 sys.authors.add(Author.objects.get(id=idusr))
 
 #a = Attribute()
 #a.title = "released button of " + title
 #a.slug = slugify(a.title)
 #a.content = a.slug
 #a.status = 2
 #a.subject = sys
 #a.svalue = "False"
 #a.attributetype_id = Attributetype.objects.get(title="pagerelease").id
 #a.save()
 sys1 = System()
 sys1.title = "page box of " + title
 sys1.status = 2
 sys1.content = "contains pages of " + title
 sys1.slug = "page_box_of_" + slugify(title)
 sys1.save()
 sys1.systemtypes.add(Systemtype.objects.get(title="page_box"))
 sys.system_set.add(sys1)
 sys.member_set.add(Author.objects.get(id=idusr))
 sys.sites.add(Site.objects.get_current())
 sys1.sites.add(Site.objects.get_current())
 return sys.id



def make_att_true(meet_ob):
       for each in  meet_ob.subject_of.all():
              if(each.attributetype.title=='release'):
                     each.svalue = "true"
                     meet_ob.subject_of.add(each) 
                     break

def make_att_false(meet_ob):
 for each in  meet_ob.subject_of.all():
	if(each.attributetype.title=='release'):
 		each.svalue = ""
		meet_ob.subject_of.add(each)
		break

#def make_att1_true(page_ob):
 #      for each in  page_ob.subject_of.all():
  #            if(each.attributetype.title=='pagerelease'):
   #                  each.svalue = "true"
    #                 page_ob.subject_of.add(each) 
     #                break

#def make_att1_false(page_ob):
 #      for each in  page_ob.subject_of.all():
  #            if(each.attributetype.title=='pagerelease'):
   #                  each.svalue = ""
    #               page_ob.subject_of.add(each)
     #                break

def schedule_time(stTime, endTime, sys_id):
	 sys=System.objects.get(id=sys_id)
	 atty1=Attributetype.objects.get(title='timeofstart')
         atty2=Attributetype.objects.get(title='timeofend')
         ate= AttributeDateTimeField()
         ats= AttributeDateTimeField()
         ats.title='starttime of '+ sys.title;ats.slug=slugify(ats.title);
	 ats.subject=sys; ats.value=stTime; ats.attributetype=atty1;
         ate.title='endtime of '+ sys.title;ate.slug=slugify(ate.title);
         ate.subject=sys; ate.value=endTime; ate.attributetype=atty2;
	 ate.save()
	 ats.save()
	 #sys.save()
	 return  sys.id


def make_title(id_no):
 i = Gbobject.objects.get(id=id_no)
 return "Subsection of:"+i.title

def get_time(sys_id):
	later = False
	meetover = False
	sys=System.objects.filter(id=sys_id)
        if sys:
          sys=System.objects.get(id=sys_id)
        else:
          sys=Gbobject.objects.get(id=sys_id)
        now=date_time.now()
        starttime=""
        endtime=""
        for each in AttributeDateTimeField.objects.all():
                if(each.attributetype.title=='timeofstart' and each.subject.title==sys.title):
                        starttime=each.value
		        if (now - starttime)< date_methds.timedelta (minutes = 1):
		                later=True
        		else:
                		later = False

                if(each.attributetype.title=='timeofend' and each.subject.title==sys.title):
                        endtime=each.value
		        if(now-endtime)>date_methds.timedelta(minutes=1):
		                meetover=True
        		else:
                		meetover=False
        return (later, meetover, starttime, endtime)
def del_comment(comment_id):
 ob = Gbobject.objects.get(id=int(comment_id))
 for each in ob.posterior_nodes.all():
	del_comment(each.id)
 ob.delete()
 return True

def del_topic(topic_id):
 ob = Gbobject.objects.get(id=int(topic_id))
 for each in ob.posterior_nodes.all():
	del_comment(each.id)
 ob.delete()
 return True

def del_section(section_id):
 ob = Gbobject.objects.get(id=int(section_id))
 for each in ob.posterior_nodes.all():
	del_comment(each.id)
 ob.delete()
 return True

def edit_topic(topic_id,title,usr):
 ob=Gbobject.objects.get(id=int(topic_id))
 contorg = unicode(title)
 ob.content_org=contorg.encode('utf8')
 ssid=ob.get_ssid.pop()
 fname=str(ssid)+"-"+usr
 ext='.org'
 html='.html'
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(ob.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 #myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[107:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 ob.content = newdata
 ob.save()
 return True

def edit_thread(thread_id,title,usr):
 ob=System.objects.get(id=int(thread_id))
 contorg = unicode(title)
 ssid=ob.get_ssid.pop()
 fname=str(ssid)+"-"+usr
 ob.content_org=contorg.encode('utf8')
 ext='.org'
 html='.html'
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(ob.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)
 #myfile.readline()
 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[107:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 ob.content = newdata
 ob.save()

 return True

def edit_nodetype(iden,rep,usr):
 nid = NID.objects.get(id = iden)
 ssid=nid.get_ssid.pop()
 fname=str(ssid)+"-"+usr
 refobj = nid.ref
 refobj.content_org = rep
 #orgcontent = request.GET["content_org"]
 ext='.org'
 html='.html'
 #usr=str(request.user)
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(refobj.content_org)
 myfile.close()
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 rfile=myfile.readlines()
 scontent="".join(rfile)
 newcontent=scontent.replace("\r","")
 myfile = open(os.path.join(FILE_URL,fname+ext),'w')
 myfile.write(newcontent)

 myfile = open(os.path.join(FILE_URL,fname+ext),'a')
 myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
 myfile.write("\n#+TITLE: ")
 myfile = open(os.path.join(FILE_URL,fname+ext),'r')
 stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
 output = stdout.read()
 data = open(os.path.join(FILE_URL,fname+html))
 data1 = data.readlines()
 data2 = data1[107:]
 dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'
 data3 = data2[:-6]
 newdata=""
 for line in data3:
        newdata += line.lstrip()
 refobj.content= newdata
 refobj.save()
 return True

def check_release_or_not(meet_ob):
 fl = 0
 for each in meet_ob.subject_of.all():
 	if (each.attributetype.title=='release' and each.svalue=='true'):
          	fl=1
 return fl
def check_subscribe_or_not(meet_ob,user):
  fl=0
  if meet_ob.system_set.all():
    box=meet_ob.system_set.all()[0]
  else:
    box=""
    return fl
  ch=Author.objects.filter(id=user.id)
  if ch:
  	ch=Author.objects.get(id=user.id)
  else:
    	ch=""
  for each in box.member_set.all():
	if each == ch:
        	fl=1
  return fl

def check_usr_admin(userid):
  fl=0
  aut=Author.objects.filter(id=userid)
  if aut:
         aut=Author.objects.get(id=userid)
         if aut.is_superuser:
                fl=1
  return fl


def get_factory_loom_OTs():
 retlist=[]
 for each in Objecttype.objects.all():
	if each.parent:
		if ((each.parent.title=='Factory_Object') and (str(each.slug)[0:4]=='loom')):
			retlist.append(each.title)
 return retlist

def get_home_content():
  homeobj=Gbobject.objects.filter(title="home_specific_detail")
  if homeobj:
         homeobj=Gbobject.objects.get(title="home_specific_detail")
  return homeobj.content

def get_more_content():
  moreobj=Gbobject.objects.filter(title="more_specific_detail")
  if moreobj:
         moreobj=Gbobject.objects.get(title="more_specific_detail")
  return moreobj.content

def get_home_title():
  homeobj=Gbobject.objects.filter(title="home_title")
  content = ""
  if homeobj:
         homeobj=Gbobject.objects.get(title="home_title")
  	 content = homeobj.content
  return content

def sendMail_RegisterUser(senderuser,receiveruser,activity,conjuction,nid,url=None):

    nodeid =  NID.objects.get(id=nid)
    sys = nodeid.ref
    if url == None:
       url = sys.get_view_object_url
    site=Site.objects.get_current()
    render = render_to_string("/gstudio/notification/label.html",{'sender':senderuser,'activity':activity,'conjunction':conjuction,'object':sys.title,'url':url,'site':site}) 
    notification.create_notice_type(render, "Invitation Received", "you have received an invitation")
    notification.send(receiveruser, render,{"from_user": senderuser}, sender=senderuser)
    return

def sendMail_NonMember(senderuser,receiveremail,activity,conjuction,nid,url=None):
    nodeid =  NID.objects.get(id=nid)
    sys = nodeid.ref
    if url == None:
       url = sys.get_view_object_url
    site=Site.objects.get_current()
    render = render_to_string("/gstudio/notification/emailBody.html",{'sender':senderuser,'activity':activity,'conjunction':conjuction,'object':sys.title,'url':url,'site':site.domain}) 
    send_mail("Invitation", render, senderuser.email, [receiveremail,])
    return 
