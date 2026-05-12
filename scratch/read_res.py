content = open('res.json', 'rb').read()
try:
    print(content.decode('utf-16'))
except:
    try:
        print(content.decode('utf-8'))
    except:
        print(content)
