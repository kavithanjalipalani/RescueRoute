# backend/app/route_solver.py
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1,phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2-lat1); dl = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*(math.sin(dl/2)**2)
    return 2*R*math.asin(math.sqrt(a))

def find_nearest_ngos(lat, lng, ngos, topk=3):
    ngos_sorted = sorted(ngos, key=lambda x: haversine(lat,lng,x["lat"],x["lng"]))
    return ngos_sorted[:topk]

def simple_route_order(start, pickups):
    order = []
    cur = start
    rem = pickups.copy()
    while rem:
        rem.sort(key=lambda x: haversine(cur[0],cur[1], x["lat"],x["lng"]))
        n = rem.pop(0)
        order.append(n)
        cur = (n["lat"],n["lng"])
    return order
