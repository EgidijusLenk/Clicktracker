import simplejson as json
from enum import auto, unique

from flask.app import Flask, jsonify
from sqlalchemy import Column, ForeignKey, create_engine, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String, DateTime, Boolean, DECIMAL, FLOAT, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://admin:DcDTe63q%40@localhost/clicktracker", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

#---Campaign Class---
class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    unique_camp_id = Column(String(32), unique=True, nullable=False)
    camp_name = Column(String(255), unique=False, nullable=False)
    traffic_source_id = Column(Integer, ForeignKey("traffic_sources.id"))
    camp_base_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    edited_at = Column(DateTime, onupdate=func.now())

    # Relationships
    traffic_source = relationship("Traffic_source")
    # offers = relationship("Offer")
    # affiliate_network = relationship("Affiliate_network")
    def __repr__(self):
        return f"<Campaign - {self.unique_camp_id} and campaign name - {self.camp_name}"
#---Campaign Class end---
#---Path Class---
class Path(Base):
    __tablename__ = "paths"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    path_name = Column(String(255), unique=False, nullable=False)
    path_camp = Column(String(32), ForeignKey("campaigns.unique_camp_id"))
    path_weight = Column(Integer)
    lander_1_id = Column(String(255), ForeignKey("landers.lander_url"))
    lander_2_id = Column(String(255), ForeignKey("landers.lander_url"))
    lander_3_id = Column(String(255), ForeignKey("landers.lander_url"))
    offer_1_id = Column(String(255), ForeignKey("offers.offer_url"))
    offer_2_id = Column(String(255), ForeignKey("offers.offer_url"))
    offer_3_id = Column(String(255), ForeignKey("offers.offer_url"))
    landers_weights = Column(String(255))
    offers_weights = Column(String(255))

    # Relationships
    campaigns = relationship("Campaign")
    lander1 = relationship("Lander", foreign_keys=[lander_1_id])
    lander2 = relationship("Lander", foreign_keys=[lander_2_id])
    lander3 = relationship("Lander", foreign_keys=[lander_3_id])
    offer1 = relationship("Offer", foreign_keys=[offer_1_id])
    offer2 = relationship("Offer", foreign_keys=[offer_2_id])
    offer3 = relationship("Offer", foreign_keys=[offer_3_id])
    # affiliate_network = relationship("Affiliate_network")
    def __repr__(self):
        return f"<Path name - {self.path_name}"
#---Path Class end---


#---Click Class---
class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    unique_click_id = Column(String(32))
    click_camp = Column(Integer, ForeignKey("campaigns.id"))
    click_camp_name = Column(String(255))
    click_lander = Column(String(255))
    click_offer = Column(String(255))
    lander_clicked = Column(Integer, default=0)
    lander_clicked_at = Column(DateTime, server_default=func.now())
    offer_clicked = Column(Integer, default=0)
    offer_clicked_at = Column(DateTime) # ar cia gerai?
    click_converted = Column(Integer)
    click_converted_at = Column(DateTime)
    click_cost = Column(DECIMAL(50,10))
    click_param1 = Column(String(255))
    clicl_url_params = Column(String(600))
    click_payout = Column(DECIMAL(50,3))
    url_custompar1 = Column(DECIMAL(50,3))
    url_custompar2 = Column(String(255))
    url_custompar3 = Column(String(255))
    url_custompar4 = Column(String(255))
    url_custompar5 = Column(String(255))
    url_custompar6 = Column(String(255))
    url_custompar7 = Column(String(255))
    url_custompar8 = Column(String(255))
    url_custompar9 = Column(String(255))
    # Relationships
    campaigns = relationship("Campaign", foreign_keys=[click_camp])
    def __repr__(self):
        return f"<Click unique id - {self.unique_click_id} and its campaign id is {self.click_camp} and camp unique id is {self.campaigns.unique_camp_id} and camp name is {self.campaigns.camp_name}"
    def to_dict(self):
        return {
            'unique_click_id': self.unique_click_id,
            'click_camp_name': self.click_camp_name,
            'click_lander': self.click_lander,
            'click_offer': self.click_offer,
            'lander_clicked': self.lander_clicked,
            'lander_clicked_at': self.offer_clicked,
            'offer_clicked': self.offer_clicked,
            'offer_clicked_at': self.offer_clicked
        }
#---Click Class end---
#---Lander Class---
class Lander(Base):
    __tablename__ = "landers"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    lander_name = Column(String(255))
    lander_url = Column(String(255))
    def __repr__(self):
        return f"<Lander name - {self.lander_name} and its url - {self.lander_url}"
#---Lander Class end---
#---Offer Class---
class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    offer_name = Column(String(255))
    offer_url = Column(String(255))
    click_param = Column(String(255))
    offer_aff_network_id = Column(Integer, ForeignKey("affiliate_network.id"))
    # Relationships
    affiliate_network = relationship("Affiliate_network")
    def __repr__(self):
        return f"<Offer name - {self.offer_name} and its url - {self.offer_url}, and its aff network name is {self.affiliate_network.network_name}"
#---Offer Class end---
#---Affiliate network Class---
class Affiliate_network(Base):
    __tablename__ = "affiliate_network"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    network_name = Column(String(255))
    click_param = Column(String(255))
    def __repr__(self):
        return f"<Affiliate network name - {self.network_name} and its click param: - {self.click_param}"
#---Affiliate network Classend---

#---Traffic_source Class---
class Traffic_source(Base):
    __tablename__ = "traffic_sources"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    source_name = Column(String(255))
    source_custom1 = Column(String(255))
    source_custom2 = Column(String(255))
    source_custom3 = Column(String(255))
    source_custom4 = Column(String(255))
    source_custom5 = Column(String(255))
    source_custom6 = Column(String(255))
    source_custom7 = Column(String(255))
    source_custom8 = Column(String(255))
    source_custom9 = Column(String(255))
    def __repr__(self):
        return f"<Traffic source name - {self.source_name}"
#---Traffic_source Class end---
# session.rollback()
# Base.metadata.create_all(engine)

def campaigns_query():
    result = session.execute(text(
        """
        SELECT campaigns.camp_name, 
concat(campaigns.camp_base_url, "/go/", unique_camp_id) as camp_link,
SUM(lander_clicked) as lander_clicks_total,
(select SUM(offer_clicked)) as offer_clicks_total,
(select SUM(url_custompar1)) as cost,
(select SUM(click_converted)) as click_converted_total,
cast(SUM(click_payout) as decimal(20,2)) as revenue,
(select SUM(offer_clicked) *100 / SUM(lander_clicked)) as ctr,
(select SUM(click_payout) - SUM(url_custompar1)) as profit,
(select SUM(url_custompar1) / SUM(lander_clicked)) as cpv,
(select SUM(click_converted) *100 / SUM(lander_clicked)) as cr,
(select (SUM(click_payout) - SUM(url_custompar1)) *100 / SUM(url_custompar1)) as roi,
SUM(click_payout) / SUM(lander_clicked) as epv,
(SUM(click_payout) - SUM(url_custompar1)) / SUM(lander_clicked) as ppc
From clicks
Inner join campaigns on clicks.click_camp = campaigns.id
-- where date(lander_clicked_at) = DATE(now())
group by
click_camp_name





        """
    ))
    # click_data=  [dict(r) for r in result]
    click_data = [to_dictx(r) for r in result]
    
    print(f"\n\n\n click_data is:\n\n\n {click_data}")
    # lst = ['camp_name', 'camp_link', 'lander_clicks_total', 'offer_clicks_total', 'cost', 'click_converted_total', 'revenue', 'ctr', 'profit', 'cr', 'roi', 'epv', 'ppc']

    return click_data
    # for r in result:
    #     z=0
    #     print(f"r is \n\n\n {list(r)}")
    #     for i in list(r):
            
    #         print(r[z])
    #         z+=1


def to_dictx(self):
        return {
            'camp_name': self.camp_name,
            'camp_link': self.camp_link,
            'lander_clicks_total': self.lander_clicks_total,
            'offer_clicks_total': self.offer_clicks_total,
            'cost': self.cost,
            'click_converted_total': self.click_converted_total,
            'revenue': self.revenue,
            'ctr': self.ctr,
            'profit': self.profit,
            'cr': self.cr,
            'roi': self.roi,
            'epv': self.epv,
            'ppc': self.ppc,
        }

# campaigns_query("as")

# click_data = [click.to_dict() for click in session.query(Click)]
#     # click_data = json.dumps(click_data, indent=4)
# print(f"\n\n\n users: {click_data}")

class construct_paths():
    def dumps():
        pass

    def loads():
        pass

formdata = {'camp_name': 'first camp1', 
    'traffic_source_id': 'traffic source1', 
    'camp_base_url': 'cam',
    'path1': 'path1', 
    'path1weight': '10',
    'lander1': 'landeris.lt', 
    'offer1': 'offeris.lt', 
    'path2': 'path2', 
    'path2weight': '10',
    'lander1': 'landeris.lt', 
    'offer1': 'offeris.lt', 
    'submit': True, 
    'csrf_token': 'IjIyZjlkYWM0NmRjMTc0Mjk0MzNjNzE4N2QzMzNjNmJjMmI4YTQ5MDUi.YYlCiQ.wJT9GCInfKKgk_bQVtvy6Tw_YUM'
    }