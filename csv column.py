def process(path):
    import csv
    data=[]
    with open(path, 'r') as csv1:
        for row in csv1.readlines():
            row=row.rstrip().split(',')
            data.append(row)
        for row in data:
            s=0
            for item in row:
                s=s+int(item)
                s=int(s)
            row.append(s)
        
    with open("ans.csv", 'w') as ans:
        writer=csv.writer(ans)
        writer.writerows(data)
