from core.models import Group,Host,CONFIG

def create(name,t):
    g=Group()
    g.name=name
    g.type=t
    g.save()
    return g.id

def list():
    re=Group.objects.all()
    return re

def search(q):
    re=Group.objects.filter(name__icontains=q).all()
    return re

def listByType(t):
    re=Group.objects.filter(type=t).all()
    return re

def show(groupid):
    group=Group.objects.filter(id=groupid)
    if group:
        return group.first()

def delete(groupid):
    group=Group.objects.filter(id=groupid)
    if group:
        #t=group.first().type
        #member=eval(t.capitalize()).objects.filter(group=group)
        #if member:
        #    for m in member:
        #        m.group.remove(group)
        group.delete()
        
def changeName(groupid,name):
    group=Group.objects.filter(id=groupid)
    if group:
        t=group.first()
        t.name=name
        t.save()
    
def addMember(groupid,members):
    groups=Group.objects.filter(id=groupid)
    if groups:
        group=groups.first()
        t=group.type
        for memberid in members:
            member=eval(t).objects.filter(id=memberid)
            if member:
                m=member.first()
                m.group.add(group)
                m.save()
                
def getMember(groupid):
    groups=Group.objects.filter(id=groupid)
    if groups:
        group=groups.first()
        t=group.type
        member=eval(t).objects.filter(group=group).all()
        return member
    
def delMember(groupid,members):
    groups=Group.objects.filter(id=groupid)
    if groups:
        group=groups.first()
        t=group.type
        for memberid in members:
            member=eval(t).objects.filter(id=memberid)
            if member:
                member.first().group.remove(group)
