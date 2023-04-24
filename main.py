f=open('dfa.in','r') #deschidem fisierul
for i,line in enumerate(f): #citim din fisier linie cu linie,si actualizam DFA-ul de tip tuplu.
    if i==0:
        Q=line.split()
    if i==1:
        sigma=line.split()
    if i==2:
        start=line.strip()
    if i==3:
        final=line.split()
    delta={}
    j=0;
    if(i>=3):
        v=f.readlines()
        k=[]
        for j in range(0,len(v)):
            k=v[j].split()
            delta[(k[0],k[1])]=k[2]
#Eliminam starile innacesibile:
R={start}
newstate={start}
temp=set()
for i in newstate:
    for j in sigma:
        temp = temp.union([delta[(i, j)]])
    newstate = temp.difference(R)
    R = R.union(newstate)
while(newstate!=set()):
    temp=set()
    for i in newstate:
        for j in sigma:
            temp=temp.union([delta[(i,j)]])
    newstate=temp.difference(R)
    R=R.union(newstate)
Q=sorted(R)
del R
print('Q in urma eliminarii starilor inaccesibile si a sortarii:',Q)

NotFinal_States=set(Q).difference(final)

# creem o matrice pentru tabel
matrix=[]
for i in range(len(Q)):
    line=[]
    for j in range(len(Q)):
            line.append(None)
    matrix.append(line)

#parcurgem pasii crearii tabelului (in acest caz marcare perechi (final,non-final)
for q in Q:
    for p in Q:
        if((p in final and q not in final) or (p not in final and q in final)):
            aux1 = int(q[1:2])
            aux2 = int(p[1:2])
            matrix[aux1][aux2]='X'
        else:
            aux1 = int(q[1:2])
            aux2 = int(p[1:2])
            matrix[aux1][aux2]='O'

#urmatorul pas realizat cu ajutorul unui while (pasul 3)
fully_marked=1
while(fully_marked):
    fully_marked=0
    for q in Q:
        for p in Q:
            aux1 = int(q[1:2])
            aux2 = int(p[1:2])
            if(matrix[aux1][aux2]!='X'):
                for a in sigma:
                    if( (matrix[int((delta[(q,a)])[1:2])][int((delta[(p,a)])[1:2])]=='X')):
                        matrix[aux1][aux2]='X'
                        fully_marked=1;

#transformarea matricii patratice in forma unui tabel Myhill-Nerode
Table=[]
p=[]
for i in range(len(Q)):
    p=[]
    for j in range(len(Q)):
        elem=matrix[i]
        if(i>j):
            l=elem[j]
            p.append(l)
    Table.append(p)
print('Tabelul obtinut in urma finalizarii minimizarii folosing teorema Myhill-Nerode')
print('(privit de la stanga la dreapta,de sus in jos, ie primul element [q0,q0] este vid, urmatorul [q1]q[0] nu este marcat,[q2][q0] si [q2][q1] sunt marcate,etc')
print(Table)

#Parcurgerea tabelului si crearea noului DFA
Compact=[]
Compact_final=[]
new_final=list()
ok_fin=0
ok_sta=0
for i in range(len(Table)):
    for j in range(0,i):
        if Table[i][j]=='O':
            Compact.append(str('q'+str(i)+'q'+str(j))) # din pacate acest lucru a fortat notarea starilor cu starile de forma _q_(number)_
            if(start=='q'+str(i) or start=='q'+str(j)):
                new_start=str('q'+str(i)+'q'+str(j))
                ok_sta=1;
            if(ok_sta==0):
                new_start=start
            if('q'+str(i) in final or 'q'+str(j) in final):
                Compact_final.append(str('q'+str(i)+'q'+str(j)))
                new_final.append(str('q'+str(i)+'q'+str(j)))
                ok_fin=1;
            if(ok_fin==0):
                new_final=final;
#toti pasii urmatori sunt in continuarea comentarului de la linia 90
for q in Q:
    for i in range(len(Compact)):
        if q in Compact[i]:
            Q[int(q[1:2])]=Compact
newlist=[]
for i in Q:
    if i not in newlist:
        newlist.append(i)
temp=[]
for i in newlist:
    if type(i)==list:
        for j in i:
            temp.append(j)
    else:
        temp.append(i)
Q=temp

def find_index(list,elem):
    for i in range(len(list)):
        if elem==list[i]:
            return i
for q in final:
    temp=[]
    temp.append(q)
    if (q in str(Compact_final) and temp!=Compact_final):
        final[find_index(final,q)]=Compact_final
temp = []
for i in final:
    if type(i) == list:
        for j in i:
            temp.append(j)
    else:
        temp.append(i)
newlist=[]
for i in temp:
    if i not in newlist:
        newlist.append(i)

new_Q=Q #112-127
new_sigma=sigma
#new_start a fost creat odata cu parcurgerea tabelului, intrucat exista o unica stare initiala
new_final=newlist #129-148
new_delta={} #155-157
for i in range(len(new_Q)-1):
    for char in new_sigma:
        new_delta[(new_Q[i],char)]=new_Q[i+1]

#Afisarea noului automat:
print('Noile stari sunt:',new_Q)
print('Alfabetul(ramene la fel) este:',new_sigma)
print('Starea initiala este:',new_start)
print('Starile finale sunt:',new_final)
print('Functia de tranzitie este:')
for i in range(len(new_Q)-1):
    for char in new_sigma:
        print(new_Q[i],'--',char,'-->',new_delta[(new_Q[i],char)])