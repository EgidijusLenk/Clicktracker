from enum import auto, unique
from sqlalchemy import Column, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String, DateTime, Boolean, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, relationship
Base = declarative_base()
engine = create_engine(
    "mysql+pymysql://admin:DcDTe63q%40@localhost/clicktracker", echo=True)
Session = sessionmaker(bind=engine, future=True)
session = Session()

#---Campaign Class---
class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    unique_camp_id = Column(String(32), unique=True, nullable=False)
    camp_name = Column(String(255), unique=False, nullable=False)
    camp_lander = Column(Integer, ForeignKey("landers.id")) #dont forget to set relationship and ForeignKey
    camp_offer = Column(Integer, ForeignKey("offers.id")) #dont forget to set relationship and ForeignKey
    camp_base_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    # Relationships
    landers = relationship("Lander")
    offers = relationship("Offer")
    def __repr__(self):
        return f"<Campaign - {self.unique_camp_id} and campaign name - {self.camp_name}"
#---Campaign Class end---
#---Click Class---
class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    unique_click_id = Column(String(32))
    click_camp = Column(Integer, ForeignKey("campaigns.id")) #dont forget to set relationship and ForeignKey
    click_lander = Column(Integer, ForeignKey("campaigns.camp_lander")) #dont forget to set relationship and ForeignKey
    click_offer = Column(Integer, ForeignKey("campaigns.camp_offer")) #dont forget to set relationship and ForeignKey
    # lander_click = Column(Integer)
    # offer_click = Column(Integer)
    lander_clicked_at = Column(DateTime, server_default=func.now())
    offer_clicked_at = Column(DateTime, server_default=func.now())
    click_converted = Column(Integer)
    click_converted_at = Column(DateTime, server_default=func.now())
    click_cost = Column(DECIMAL(10,10))
    click_param1 = Column(String(255))
    clicl_url_params = Column(String(600))
    # Relationships
    campaigns = relationship("Campaign", foreign_keys=[click_camp])
    def __repr__(self):
        return f"<Click unique id - {self.unique_click_id} and its campaign name - {self.click_camp} and camp unique id is {self.campaigns.unique_camp_id}"

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
    offer_traffic_source_id = Column(Integer, ForeignKey("traffic_sources.id")) #dont forget to set relationship and ForeignKey
    # Relationships
    traffic_sources = relationship("Traffic_source")
    def __repr__(self):
        return f"<Offer name - {self.offer_name} and its url - {self.offer_url}, and its traffic source name is {self.traffic_sources.source_name}"
#---Offer Class end---
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
    def __repr__(self):
        return f"<Traffic source name - {self.source_name}"
#---Traffic_source Class end---

Base.metadata.create_all(engine)