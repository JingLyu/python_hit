import os
os.chdir("/Users/jilv/scripts")
file='page_type_monetized_mapping.lkp'
page_type={}
with open(file) as f:
    
    lines = f.read().splitlines();
    for l in lines[1:]:
        row = l.split(",")
        page_type[row[0]]=1
print len(page_type)
f.close()

file_categ='categ_id_name_mapping.lkp'
d_categ_map={}
with open(file_categ) as f:
    lines = f.read().splitlines();
    for l in lines[1:]:
        row = l.split("\t")
        d_categ_map[row[0]] = row[1]
print d_categ_map
f.close()

os.chdir("/Users/jilv/scripts/ga_data")
file2='budget_traffic.csv'
file_o_name='budget_traffic_monetised.csv'
try:
    os.remove(file_o_name)
except OSError:
    pass
    

file_o=open(file_o_name,'wb')
with open(file2) as f:
    lines=f.read().splitlines();
    for l in lines:
        row=l.split(";")
        print row
        if row[3] in d_categ_map:
            lCateg=[d_categ_map[row[3]]]
        else:
            lCateg=['(None)']

        if row[5] in page_type:
            lM=['Monetised']
        else:
            lM=['Non-monetised']

        s=row[0:3]+ lCateg +[row[4]]+ lM+row[6:8]

        print s
        s_value=s[0]
        for x in s[1:]:
            s_value=s_value+','+ x
        print s_value
        s_value=s_value + '\n'
        file_o.write(s_value)
f.close()
file_o.close()
