# Example
```
from sixecho import Client
client = Client()
client.generate(str="ความสุขของผมคือการทำอะไรเสร็จตามเป้าหมาย  success is  happiness")
```
### **The sentense after process by word cut.**
```
client.array_words  
```
> result: ["ความ", "สุข", "ของ", "ผม", "คือ", "การ", "ทำ", "อะไร", "เสร็จ", "ตาม", "เป้าหมาย", "success", "is", "happiness"] 

### **Get 128 digest from minhash**
```
 client.digest()
```
> array([ 280072101,  120771717,  113505080,  311917730,   54061830,
        692412087,  649304561,   23680262,  694249824,  197969977,
        730608745,    3294324,  119644586,  104967492,  655069465,
        330578733,  167650525,   30155578,   94570067,  669191241,
        400818815,  707822458,   85461620,  299410067,  181811156,
        581906726,  306115892,  189564460,  639025353,   26255378,
        126074546,   53214985,  348378454,  497508499,  104284187,
         23435866,  108876607,  532962077,  493865851,  352687831,
        277870079,  739691578,  277002640,  242700697,  209081291,
        199246347,  704110980,   25410421,  440926714,  315754994,
          8674412,  470889755,   24030724,  374614089,    5048555,
        420416088,  264913768,  156187572,   14648640,  137841655,
        247921076,   35379752,  385401483,   48164330,  215199690,
          4491884,    5754411,   14017239,  422019175,  225669078,
        253756462,   20439884,  525322476,   11856924,  628562468,
        131301967,  157429308,   65264129,   95255415,   49861621,
        188771176,   79008575,  408659652,  371579957,  268051931,
         23974405,   44329717,  180740301,  223189329,   91436767,
        502285457,  331888618,   78426205,  446583374,  314333066,
        970062035,  183767130,  645427259,  426114499,  473613493,
        245407907,   36678152,  164107112,  767183044,   98423826,
         17005498,  124749844,  198212324,   96387823,   84699259,
        325820698,  296940523,  690824804,  140867532, 1170280539,
        474197952,   14187457,  260899183,   69353965,   58631678,
        102746586,  713347982,  227576955,  276376442,  217451670,
         65504487,  157439113,  298109273], dtype=uint64)

### **Load file to generate digest**
```
client.generate(fpath="file.txt")
```

### **Upload to server**
```bash
client = Client(api_key="Your Api key", host_url="Host digital content")
# Or Mutiple thread
client = Client(api_key="Your Api key", host_url="Host digital content",max_workers=2)

# Generate from text/string or content
client.generate(str="your content")

# Generate from a file
client.generate(fpath="your path file")

# Command upload to server follow by host_url
client.upload()
```

# Test 
## Configure
To configure the nosetests command, add a [nosetests] section to your setup.cfg file.

## Run all cases
```
python setup.py nosetests
```
## Run test single test case
```
python setup.py nosetests --tests sixecho/tests/test_client.py:TestSixecho.test_tokenize
```

# Upload testpypi 
```bash
python -m twine upload --repository testpypi dist/*
```

# Upload pypi
```bash
python -m twine upload dist/*
```

## Build new version
change version where setup(version="xxxx") from setup.py file. Use this command to build new version.
```bash
python setup.py sdist
```
