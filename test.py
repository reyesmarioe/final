d = {
        "02152022"  :   {
            "shoes" :   250,
            "food"  :   100,
            }
        }

print(d)

for k,v in d.items():
    print(k, v)
    for k,v in v.items():
        print(k, v)
