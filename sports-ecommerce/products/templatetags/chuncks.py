from django import template
register=template.Library()
@register.filter(name="chuncks")
def chuncks(list_data,chunck_size):
    chuncks=[]
    i=0
    for data in list_data:
        chuncks.append(data)
        i=i+1
        if i==chunck_size:
            yield chuncks
            i=0
            chuncks=[]
    if chuncks:    
        yield chuncks    