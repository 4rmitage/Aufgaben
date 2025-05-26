zahl = int(input("Gib eine ganze Zahl ein: "))
 
 
halbiert = zahl // 2  
wieder_multipliziert = halbiert * 2
 
if wieder_multipliziert == zahl:
    print("Die Zahl ist gerade.")
else:
    print("Die Zahl ist ungerade.")