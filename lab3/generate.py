#!/usr/bin/env python

x1 = 59.944741
x2 = 59.941290
y1 = 30.243517
y2 = 30.252689

file = open("out.txt", "w")

for i in range(20):
    for j in range(20):
        file.write(f"""
        {{
		"id": {i * 100 + j},
		"name": "РќР° РґРѕСЂРѕР¶РєСѓ! (AMOGUS #{i*20 + j + 1})",
		"description": "СѓР». РЁРµРІС‡РµРЅРєРѕ, 29",
		"picture": "/api/v1/containers/images/download/4abg11647626720916.jpg",
		"location": {{
			"lat": {x1 + (-x1+x2)/20*i},
			"lng": {y1 + (-y1+y2)/20*j}
		}},
		"ratesCount": 7,
		"type": null,
		"rate": 5,
		"visits": 0,
		"hasOwner": false,
		"hasOwnerActive": false,
		"status": "normal",
		"isFavorite": false,
		"reviews": [],
		"comments": []
        }},
        """)

file.close()