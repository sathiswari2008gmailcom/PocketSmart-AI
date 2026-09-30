from .catalog import catalog,search_url
def pick(kind,budget,limit=6):
    out=[]
    for title,cat,price,platform in sorted(catalog(kind),key=lambda x:x[2]):
        if price<=max(budget,1)*.8:
            out.append({"title":title,"category":cat,"estimated_price":float(price),"quantity":1,"platform":platform,"search_url":search_url(platform,title),"reason":"Budget-friendly fallback option from the local demo catalog.","notes":"Estimated price; verify current price on the platform."})
        if len(out)>=limit: break
    return out
def fallback_home(d):
    budget=float(d["budget"])
    remaining=budget
    items=[]
    for x in d["items"]:
        qty=int(x["quantity"])
        chosen=None
        for title,cat,price,platform in sorted(catalog("home"),key=lambda row:row[2]):
            if price*qty <= remaining:
                chosen=(title,cat,price,platform)
                break
        if chosen:
            title,cat,price,platform=chosen
            item_title=x["name"]+" - "+title
            reason="Fallback suggestion for "+x["name"]+"."
            items.append({"title":item_title,"category":cat,"estimated_price":round(price*qty,2),"quantity":qty,"platform":platform,"search_url":search_url(platform,title),"reason":reason,"notes":"Estimated price; verify current price on the platform."})
            remaining-=price*qty
    total=round(budget-remaining,2)
    summary=d["style"]+" setup for "+", ".join(d["rooms"])+"."
    return {"planner_type":"home","summary":summary,"budget":budget,"estimated_total":total,"remaining_budget":round(remaining,2),"allocation":{"furniture":round(budget*.45,2),"lighting":round(budget*.2,2),"decor":round(budget*.2,2),"storage":round(budget*.15,2)},"items":items,"source":"fallback","disclaimer":"Fallback estimates only. Verify live prices before purchase."}
def fallback_party(d):
    b=d["budget"]; g=d["guests"]; rows=[("Catering",b*.5,"Swiggy"),("Decoration",b*.2,"Amazon"),("Entertainment",b*.15,"Zomato"),("Accommodation/contingency",b*.15,"OYO")]; items=[]
    for cat,amount,platform in rows:
        items.append({"title":f'{d["event_type"]} {cat} plan',"category":cat.lower(),"estimated_price":round(amount/g,2) if cat=="Catering" else round(amount,2),"quantity":g if cat=="Catering" else 1,"platform":platform,"search_url":search_url(platform,cat),"reason":f"Allocated for {cat.lower()} based on the event budget.","notes":"Compare current local options on the platform."})
    total=round(sum(x["estimated_price"]*x["quantity"] for x in items),2)
    return {"planner_type":"party","summary":f'{d["event_type"]} plan for {g} guests.',"budget":b,"estimated_total":total,"remaining_budget":round(b-total,2),"allocation":{"catering":b*.5,"decoration":b*.2,"entertainment":b*.15,"contingency":b*.15},"items":items,"source":"fallback","disclaimer":"Venue and food prices vary by city, date and vendor."}
def fallback_jewelry(d):
    items=pick("jewelry",d["budget"],5); total=round(sum(x["estimated_price"]*x["quantity"] for x in items),2)
    return {"planner_type":"jewelry","summary":f'{d["style"]} jewelry ideas for {d["occasion"]}.',"budget":d["budget"],"estimated_total":total,"remaining_budget":round(d["budget"]-total,2),"allocation":{"earrings":d["budget"]*.35,"necklace":d["budget"]*.45,"bracelet":d["budget"]*.2},"items":items,"source":"fallback","disclaimer":"Image/style matching is an estimate. Verify product details and prices."}
