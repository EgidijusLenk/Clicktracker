from types import new_class
from dependancies import id_generator
from sqlalchemy.sql.elements import Null
from models import Campaign, Click, Lander, Offer, Traffic_source, Affiliate_network, Path
from sqlalchemy.sql import func
from models import session
#------imports for quering, for testing purpose---- ar situ reikia?
from typing import Tuple
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
import simplejson as json

#------imports for quering, for testing purpose. End----

#----------
#---Create new campaign---
#cia dar reik perdaryt nuo vkr
def create_new_campaign(unique_camp_id, camp_name, traffic_source_id, camp_base_url):
    new_campaign = Campaign(
        unique_camp_id = unique_camp_id,
        camp_name = camp_name,
        traffic_source_id = traffic_source_id,
        camp_base_url = camp_base_url,
        )
    session.add(new_campaign)
    session.commit()
# #---Create new campaign end---
# create_new_campaign("pirmas camp", 1, "camp1.com")
#---Create new click---
def create_new_click(click_camp, params_query_string):
    
    # obj = session.query(Campaign).filter_by(unique_camp_id=click_camp).first()
    # print(f"\n\n\n\n\n\n\nobjektas x: {obj}")
    # print(f"\n\n\n\n\n\n\nobjektas x: {params_query_string}")
    # params_query_string = str(params_query_string)
    # d = dict(x.split("=") for x in params_query_string.split("&"))
    # d = list(d.values())
    # url_custompar = ["url_custompar1", "url_custompar2", "url_custompar3", "url_custompar4", "url_custompar5", "url_custompar6", "url_custompar7", "url_custompar8", "url_custompar9"]
    # dictz = dict(zip(url_custompar, d))
    # print(f" qqqqqqqqqqqqqqq {dictz}")
    # unique_click_id = id_generator()
    # click_offer = f"{obj.offers.offer_url}?{obj.offers.click_param}="
    # new_click = Click(
    #     unique_click_id = unique_click_id,
    #     click_camp = f"{obj.id}",
    #     click_camp_name = f"{obj.camp_name}",
    #     click_lander = f"{obj.landers.lander_url}",
    #     click_offer = click_offer,
    #     lander_clicked = +1,
    #     **dictz        
    # )

    # session.add(new_click)
    # session.commit()
    # return [obj.landers.lander_url, click_offer, unique_click_id]

#---nuo cia naujas  metodas---
        #---reikia paadaryti checka, kad tikrintu ar toks camp yra, ir at yra parametru string, nes ir be stringu turetu redirectinti
    #store url parameters in db:
    params_query_string = str(params_query_string)
    print(f" \n\n\n\n\n\nSTRINGis \n {params_query_string}")
    d = dict(x.split("=") for x in params_query_string.split("&"))
    d = list(d.values())
    url_custompar = ["url_custompar1", "url_custompar2", "url_custompar3", "url_custompar4", "url_custompar5", "url_custompar6", "url_custompar7", "url_custompar8", "url_custompar9"]
    dictz = dict(zip(url_custompar, d))
    unique_click_id = id_generator()
    # ---
    obj = session.query(Path).filter_by(path_camp=click_camp).all()
    paths_list= []
    for row in obj:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        paths_list.append(d)
    camp_paths = {
        'paths_weights': [],
        'paths_names':[],
        obj[0].path_name:{'landers_list': [obj[0].lander_1_id, obj[0].lander_2_id, obj[0].lander_3_id], 'offers_list': [f"{obj[0].offer_1_id}?{obj[0].offer1.click_param}=", f"{obj[0].offer_2_id}?{obj[0].offer2.click_param}=", f"{obj[0].offer_3_id}?{obj[0].offer3.click_param}="], 'landers_weights':list(map(int, obj[0].landers_weights.split(' '))), 'offers_weights': list(map(int, obj[0].offers_weights.split(' ')))},
        obj[1].path_name:{'landers_list': [obj[1].lander_1_id, obj[1].lander_2_id, obj[1].lander_3_id,], 'offers_list': [f"{obj[1].offer_1_id}?{obj[1].offer1.click_param}=", f"{obj[1].offer_2_id}?{obj[1].offer2.click_param}=", f"{obj[1].offer_3_id}?{obj[1].offer3.click_param}="], 'landers_weights':list(map(int, obj[1].landers_weights.split(' '))), 'offers_weights': list(map(int, obj[1].offers_weights.split(' ')))},
        }

    for path in paths_list:
        for key, pathval in path.items():
            # print(f"vals::: \n {path_name} and {pathval}")
            if key == "path_weight":
                camp_paths['paths_weights'].append(int(pathval))
            if key == 'path_name':
                camp_paths['paths_names'].append(pathval)

    # print(f"\n \n camp_paths: {camp_paths}") # paths weights

    chosen_path = random.choices(camp_paths['paths_names'], weights=camp_paths['paths_weights'])[0]

    landeris = random.choices(camp_paths[chosen_path]['landers_list'], weights=camp_paths[chosen_path]['landers_weights'])[0]
    offeris = random.choices(camp_paths[chosen_path]['offers_list'], weights=camp_paths[chosen_path]['offers_weights'])[0]
    # print(f"\n \n landeris: {landeris} \n offeris: {offeris}")
    # ---
    new_click = Click(
        unique_click_id = unique_click_id,
        click_camp = obj[0].campaigns.id,
        click_camp_name = obj[0].campaigns.unique_camp_id,
        click_lander = landeris,
        click_offer = offeris,
        lander_clicked = +1,
        **dictz        
    )

    session.add(new_click)
    session.commit()
    return [landeris, offeris, unique_click_id]



#---nuo cia naujas  metodas end---
#dummy string from url params:
# params_query_string = "b'cost={cost}&visitor_id=${SUBID}&zoneid={zoneid}&campaignid={campaignid}&bannerid={bannerid}&user_activity={user_activity}&zone_type={zone_type}'"
# create_new_click("5XV5I957JN7WJY3FBTXD5XLKB2A9YFCI", params_query_string)
#---Create new lander end---

#---click_to_offer--- sita padaryti!!!
def click_to_offer(unique_click_id):
    obj = session.query(Click).filter_by(unique_click_id=unique_click_id).first()
    print(f"here is obj \n\n\n\n{obj.__dict__}")
    setattr(obj, "offer_clicked", obj.offer_clicked+1)
    setattr(obj, "offer_clicked_at", func.now())
    session.commit()
# click_to_offer("CTB0G8VK1A4BRPBKPC6HG8H3HWTLEVBZ")
# result = [Click]\
#     .update()
#     .where([Click].c.name == 'Todd')
#     .values(email='newemail@example.com')
# create_new_lander("pirmas lander", "landerdomain.com")
#---click_to_offer end---
#---Click converted--- SITA REIKIA PADARYTI, KAI AFF NETWORKAS PINGINA ATGAL CONVERSIJA
def click_converted(unique_click_id, payout):
    pass
#---Click converted end---

#---Create new lander---
def create_new_lander(lander_name, lander_url):
    new_lander = Lander(
        lander_name = f"{lander_name}",
        lander_url = f"{lander_url}"
    )
    session.add(new_lander)  # Add the user
    session.commit()  # Commit the change

# create_new_lander("antras lander", "http://127.0.0.1:5000/dummylander3")
#---Create new lander end---



#---Create new path---
# create_new_path(unique_camp_id, unique_camp_id, formodata['path1weight'], formodata['path1lander1'], formodata['path1lander2'], formodata['path1lander3'], formodata['path1offer1'], formodata['path1offer2'], formodata['path1offer3'], path1_landers_weights, path1_offers_weights)
def create_new_path(path_name, path_camp, path_weight, lander_1_id, lander_2_id, lander_3_id, offer_1_id, offer_2_id, offer_3_id, landers_weights, offers_weights):
    create_new_path = Path(
        path_name = path_name,
        path_camp = path_camp,
        path_weight = path_weight,
        lander_1_id = lander_1_id,
        lander_2_id = lander_2_id,
        lander_3_id = lander_3_id,
        offer_1_id = offer_1_id,
        offer_2_id = offer_2_id,
        offer_3_id = offer_3_id,
        landers_weights = landers_weights,
        offers_weights = offers_weights,
    )
    session.add(create_new_path)  # Add the user
    session.commit()  # Commit the change

# create_new_path("pirmas path", "1M65XXD2I3ZWR240CKJPRL3GARR433W5", 10, "http://127.0.0.1:5000/dummylander", "http://127.0.0.1:5000/dummylander1", "http://127.0.0.1:5000/dummylander3", "http://127.0.0.1:5000/dummyoffer", "http://127.0.0.1:5000/dummyoffer", "http://127.0.0.1:5000/dummyoffer", "100 10 10", "100 10 10")
#---Create new path end---





#---Create new offer---
def create_new_offer(offer_name, offer_url, click_param, offer_aff_network_id):
    new_offer = Offer(
        offer_name = f"{offer_name}",
        offer_url = f"{offer_url}",
        click_param = f"{click_param}",
        offer_aff_network_id = f"{offer_aff_network_id}"
    )
    session.add(new_offer)  # Add the user
    session.commit()  # Commit the change

# create_new_offer("pirmas offers", "http://127.0.0.1:5000/dummyoffer", "sub1", 1)
#---Create new offer end---
#---Create new Affiliate network---
def create_new_aff_network(network_name, click_param):
    new_offer = Affiliate_network(
        network_name = f"{network_name}",
        click_param = f"{click_param}"
    )
    session.add(new_offer)  # Add the user
    session.commit()  # Commit the change

# create_new_aff_network("pirmas offers", "sub1")
#---Create new Affiliate network end---

#---Create new traffic source---
def create_new_traffic_source(source_name, source_custom1, source_custom2, source_custom3, source_custom4, source_custom5, source_custom6, source_custom7, source_custom8, source_custom9):
    new_traffic_source = Traffic_source(
        source_name = f"{source_name}",
        source_custom1 = f"{source_custom1}",
        source_custom2 = f"{source_custom2}",
        source_custom3 = f"{source_custom3}",
        source_custom4 = f"{source_custom4}",
        source_custom5 = f"{source_custom5}",
        source_custom6 = f"{source_custom6}",
        source_custom7 = f"{source_custom7}",
        source_custom8 = f"{source_custom8}",
        source_custom9 = f"{source_custom9}",
    )
    session.add(new_traffic_source)  # Add the user
    session.commit()  # Commit the change

# create_new_traffic_source("trecias traffic source", "cost={cost}", "visitor_id=${SUBID}", "zoneid={zoneid}", "campaignid={campaignid}", "bannerid={bannerid}", "user_activity={user_activity}", "zone_type={zone_type}", None, None)

#---Create new traffic source---



#--- testing purpose----
# kaip prisegti params str prie camp linko: sita koda prideti prie create campaign, kad returnintu i flaska
# obj = session.query(Campaign).filter_by(unique_camp_id="5XV5I957JN7WJY3FBTXD5XLKB2A9YFCI").first()

# camp_params_list = [obj.traffic_source.source_custom1, obj.traffic_source.source_custom2, obj.traffic_source.source_custom3, obj.traffic_source.source_custom4, obj.traffic_source.source_custom5, obj.traffic_source.source_custom6, obj.traffic_source.source_custom7, obj.traffic_source.source_custom8, obj.traffic_source.source_custom9]

# camp_params_string = str("?")
# for i in camp_params_list:
#     if i != 'None':
#         camp_params_string+=(f"{i}&")
# camp_params_string = camp_params_string.rstrip("&")
# print(f" strings 1 \n\n\n\n\n\n\nis {camp_params_string}")


# camp_params= str(f"")


# str = "b'cost={cost}&visitor_id=${SUBID}&zoneid={zoneid}&campaignid={campaignid}&bannerid={bannerid}&user_activity={user_activity}&zone_type={zone_type}'"
# str = str.lstrip("b'")
# str = str.rstrip("'")
# d = dict(x.split("=") for x in str.split("&"))
# d = list(d.values())
# url_custompar = ["url_custompar1", "url_custompar2", "url_custompar3", "url_custompar4", "url_custompar5", "url_custompar6", "url_custompar7", "url_custompar8", "url_custompar9"]
# dictz = dict(zip(url_custompar, d))
# print(f" qqqqqqqqqqqqqqq {dictz}")


# main()
#--- testing purpose end---6
# for val in obj.traffic_source:
#     print(val)
# obj = session.query(Offer).filter_by(id="1").first()
# print(f'objektas {obj}, \n source name is: {obj.traffic_sources.source_name}')
# unique_camp_id = "dummy"
# obj = session.query(Campaign).filter_by(unique_camp_id=unique_camp_id).first()
# print(f'objektas {obj}, \n lander url name is: {obj.landers.lander_url}')

# mainx()

# obj = session.query(Click)
# click_data = [click.to_dict() for click in session.query(Click)]
# print(f"\n\n\n users: {click_data}")
# testx(dict)
# def data_query
# click_data = [click.to_dict() for click in session.query(Click)]
#     print(f"\n\n\n users: {click_data}")

#     return {'data': click_data}
#--- test---
import random
landers_list = ['land1', 'land2', 'land3']
paths_weights = [10,50,50] #tarkim tures 3 paths, cia ju svoriai
landers_weights = [1, 1, 0]
offers_weights = [1, 1, 0]
zet = random.choices(landers_list, weights=landers_weights)
# print(f"randoms is this: \n\n {zet[0]}")

#--- test end---





def tipo_new_click(click_camp):

    camp_paths = json.loads(session.query(Campaign).filter_by(unique_camp_id=click_camp).first().paths)
    #issirenku patha
    chosen_path = random.choices(camp_paths['paths_names'], weights=camp_paths['paths_weights'])[0]
    #issirenku landeri
    landeris = random.choices(camp_paths[chosen_path]['landers_list'], weights=camp_paths[chosen_path]['landers_weights'])[0]
    #issirenku offeri
    offeris = random.choices(camp_paths[chosen_path]['offers_list'], weights=camp_paths[chosen_path]['offers_weights'])[0]

    lander = session.query(Lander).filter(Lander.id==landeris).first().lander_url
    offer = session.query(Offer).filter(Offer.id==offeris).first()
    click_offer = f"{offer.offer_url}?{offer.click_param}="
    print(f"\nrandoms path: {chosen_path}\nrandom lander: {landeris} \nrandom offer: {offeris}")
    print(f"\n landeris: {lander} and offeris: {click_offer}\n")
    
    lander_url = ''
    click_offer = ''
    print("\n\n\n\n\n\n\n\n vuolia? \n\n\n\n\n\n\n\n\n\n\n")
    return [lander_url, click_offer]
# tipo_new_click("9FC5ST4SHGNMK55JE9EJJZKOGS56MX89")
# camp_paths = {
#         'paths_weights': [10,100,1],
#         'paths_names':['pathid1', 'pathid2', 'pathid3'],
#         'pathid1':{'landers_list': [1,2,3], 'offers_list': [1,2,3], 'landers_weights':[50,50,0], 'offers_weights':[50,50,0]},
#         'pathid2' :{'landers_list': [1,2,3], 'offers_list': [1,2,3], 'landers_weights':[50,50,0], 'offers_weights':[50,50,0]},
#         'pathid3' :{'landers_list': [1,2,3], 'offers_list': [1,2,3], 'landers_weights':[50,50,0], 'offers_weights':[50,50,0]}}
# camp_paths = json.dumps(camp_paths)
# obj = json.loads(camp_paths)
# obj = session.query(Campaign).filter_by(unique_camp_id="Z3W7MRIWABNUA5ZB6NQ8Z0Z58NF588JS").first()
# print(f"\n\n\n\n\n\n rusis yra: {type(obj)}")

#--new camp object---
def tipo_new_camp(camp_name, traffic_source_id, camp_base_url, paths):
    new_campaign = Campaign(
        unique_camp_id = id_generator(),
        camp_name = camp_name,
        traffic_source_id = traffic_source_id,
        paths=paths,
        camp_base_url = camp_base_url
    )
    session.add(new_campaign)
    session.commit()

    print(f"this is print ")
#construct paths:

# pathid1 = {'landers_list': [1,2,3], 'offers_list': [1,2,3], 'landers_weights':[50,50,0], 'offers_weights':[50,50,0]}

# paths = {'paths_weights': [],
#         'paths_names':['pathid1'],}
# paths['paths_weights'] = []
# paths['paths_names'].append('pathid2')
# print(paths)
#tipo_new_camp()
#--new camp object end---

# click_camp = "1M65XXD2I3ZWR240CKJPRL3GARR433W5"
# obj = session.query(Path).filter_by(path_camp=click_camp).all()
# paths_list= []
# for row in obj:
#     d = {}
#     for column in row.__table__.columns:
#         d[column.name] = str(getattr(row, column.name))

#     paths_list.append(d)
# camp_paths = {
#     'paths_weights': [],
#     'paths_names':[],
#     obj[0].path_name:{'landers_list': [obj[0].lander_1_id, obj[0].lander_2_id, obj[0].lander_3_id], 'offers_list': [f"{obj[0].offer_1_id}?{obj[0].offer1.click_param}=", f"{obj[0].offer_2_id}?{obj[0].offer2.click_param}=", f"{obj[0].offer_3_id}?{obj[0].offer3.click_param}="], 'landers_weights':list(map(int, obj[0].landers_weights.split(' '))), 'offers_weights': list(map(int, obj[0].offers_weights.split(' ')))},
#     obj[1].path_name:{'landers_list': [obj[1].lander_1_id, obj[1].lander_2_id, obj[1].lander_3_id,], 'offers_list': [f"{obj[1].offer_1_id}?{obj[1].offer1.click_param}=", f"{obj[1].offer_2_id}?{obj[1].offer2.click_param}=", f"{obj[1].offer_3_id}?{obj[1].offer3.click_param}="], 'landers_weights':list(map(int, obj[1].landers_weights.split(' '))), 'offers_weights': list(map(int, obj[1].offers_weights.split(' ')))},
#     }

# for path in paths_list:
#     for key, pathval in path.items():
#         # print(f"vals::: \n {path_name} and {pathval}")
#         if key == "path_weight":
#             camp_paths['paths_weights'].append(int(pathval))
#         if key == 'path_name':
#             camp_paths['paths_names'].append(pathval)

# print(f"\n \n camp_paths: {camp_paths}") # paths weights

# chosen_path = random.choices(camp_paths['paths_names'], weights=camp_paths['paths_weights'])[0]

# landeris = random.choices(camp_paths[chosen_path]['landers_list'], weights=camp_paths[chosen_path]['landers_weights'])[0]
# offeris = random.choices(camp_paths[chosen_path]['offers_list'], weights=camp_paths[chosen_path]['offers_weights'])[0]
# print(f"\n \n landeris: {landeris} \n offeris: {offeris}")



# print(f"\npaths_weights:::  {v} \n obj.offer1.click_param:: {obj[0].offer1.click_param}")


# class linkselector():








# print(f"obj.path_1_id.lander1.lander_url is {obj.path_1_id.lander1.lander_url}\n\n obj.path1.lander1.lander_url is {obj.path1.lander1.lander_url}")
# dictx = {'key1' : obj.path_1_id, "key2" : obj.path_2_id }
# camp_paths = [obj.path_1_id, obj.path_2_id]
# path1_landers = [obj.path1.lander1.lander_url, obj.path1.lander2.lander_url, obj.path1.lander3.lander_url]
# path2_landers = [obj.path2.lander1.lander_url, obj.path2.lander2.lander_url, obj.path2.lander3.lander_url]
# paths_weights = [obj.path_1_weight, obj.path_2_weight]
# path1_lander_weights = [obj.path1.lander_1_weight, obj.path1.lander_3_weight, obj.path1.lander_3_weight]
# path2_lander_weights = [obj.path2.lander_1_weight, obj.path2.lander_3_weight, obj.path2.lander_3_weight]
# path1_offers = [f"{obj.path1.offer1.offer_url}?{obj.path1.offer1.click_param}=", f"{obj.path1.offer2.offer_url}?{obj.path1.offer2.click_param}=", f"{obj.path1.offer3.offer_url}?{obj.path1.offer3.click_param}="]
# path1_offer_weights = [obj.path1.offer_1_weight, obj.path1.offer_3_weight, obj.path1.offer_3_weight]
# path2_offer_weights = [obj.path2.offer_1_weight, obj.path2.offer_3_weight, obj.path2.offer_3_weight]
# # dictc = [key for key in dictx]
# chosen_path = random.choices([key for key in dictx], weights=paths_weights)
# print(f"keys: \n {chosen_path}")
# chosen_lander = random.choices([key for key in dictx], weights=paths_weights)

# for row in obj:
#     print(f"row is: {row}")
    #find out what path click has to follow:
# camp_paths_list = [obj.path_1_id, obj.path_2_id]
# paths_weights_list = [obj.path_1_weight, obj.path_2_weight]

# camp_path = random.choices(camp_paths_list, paths_weights_list)

# path_landers_list = ''
# landeris = obj.path1.lander1.lander_url


# d = {}
# for column in obj.__table__.columns:
#     d[column.name] = str(getattr(obj, column.name))

    
# print(f"\n\nthis is print {d}")

# formodata = {'camp_name': 'UK - pirmas campaign submitintas is formos', 
# 'traffic_source_id': 3, 
# 'camp_base_url': 'camp.com', 
# 'path1weight': 100, 
# 'path1lander1': 'http://127.0.0.1:5000/dummylander', 
# 'path1lander1weight': 50, 
# 'path1lander2': 'http://127.0.0.1:5000/dummylander1', 
# 'path1lander2weight': 40, 
# 'path1lander3': 'http://127.0.0.1:5000/dummylander', 
# 'path1lander3weight': 5, 
# 'path1offer1': 'http://127.0.0.1:5000/dummyoffer', 
# 'path1offer1weight': 50,
#  'path1offer2': 'http://127.0.0.1:5000/dummyoffer', 
#  'path1offer2weight': 50, 
#  'path1offer3': 'http://127.0.0.1:5000/dummyoffer',
#   'path1offer3weight': 50, 
#   'path2weight': 100, 
#   'path2lander1': 'http://127.0.0.1:5000/dummylander', 
#   'path2lander1weight': 50, 
#   'path2lander2': 'http://127.0.0.1:5000/dummylander', 
#   'path2lander2weight': 50, 
#   'path2lander3': 'http://127.0.0.1:5000/dummylander1', 
#   'path2lander3weight': 50, 
#   'path2offer1': 'http://127.0.0.1:5000/dummyoffer', 
#   'path2offer1weight': 15, 
#   'path2offer2': 'http://127.0.0.1:5000/dummyoffer', 
#   'path2offer2weight': 70, 
#   'path2offer3': 'http://127.0.0.1:5000/dummyoffer', 
#   'path2offer3weight': 100, 
#   'submit': True, 'csrf_token': 'IjA5NDliODAxZDFiNTVhYzM2ZTA2YzI3ZjlmNWQ1MDNjYzE5YWVkMWQi.YY6klA.QiDnDe1eYrg7cBRLlXpOI45iYmQ'}
def submit_campaign_data(formdata):
    unique_camp_id = id_generator(),
    path1_landers_weights = f'{formdata["path1lander1weight"]} {formdata["path1lander2weight"]} {formdata["path1lander3weight"]}'
    path1_offers_weights = f'{formdata["path1offer1weight"]} {formdata["path1offer2weight"]} {formdata["path1offer3weight"]}'
    path2_landers_weights = f'{formdata["path2lander1weight"]} {formdata["path2lander2weight"]} {formdata["path2lander3weight"]}'
    path2_offers_weights = f'{formdata["path2offer1weight"]} {formdata["path2offer2weight"]} {formdata["path2offer3weight"]}'
    create_new_campaign(unique_camp_id, formdata["camp_name"], formdata['traffic_source_id'], formdata['camp_base_url'])
    create_new_path(unique_camp_id, unique_camp_id, formdata['path1weight'], formdata['path1lander1'], formdata['path1lander2'], formdata['path1lander3'], formdata['path1offer1'], formdata['path1offer2'], formdata['path1offer3'], path1_landers_weights, path1_offers_weights)
    create_new_path(unique_camp_id, unique_camp_id, formdata['path2weight'], formdata['path2lander1'], formdata['path2lander2'], formdata['path2lander3'], formdata['path2offer1'], formdata['path2offer2'], formdata['path2offer3'], path2_landers_weights, path2_offers_weights)

# submit_campaign_data(formdata)