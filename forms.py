from flask_wtf import FlaskForm, RecaptchaField
from sqlalchemy.sql.elements import Null
from wtforms import StringField, TextField, SubmitField, IntegerField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email
import email_validator
import wtforms
from models import Campaign, Click, Lander, Offer, Traffic_source, Affiliate_network, session

class Create_campaign(FlaskForm):
    def lander_list():
        d = [(g.lander_url, g.lander_name) for g in session.query(Lander).order_by('lander_name').all()]
        z = [(0, "No lander chosen"), (0, "Direct to offer")]
        for i in d:
            z.append(i)
        return z
    def offer_list():
        d = [(g.offer_url, g.offer_name) for g in session.query(Offer).order_by('offer_name').all()]
        z = [(0, "No offer chosen")]
        for i in d:
            z.append(i)
        return z    
    """Contact form."""
    camp_name = StringField(
        'Campaign name',
        [DataRequired()]
    )
    traffic_source_id = SelectField(
        'Traffic source ID', validate_choice=False, 
        # choices=[(g.id, g.name) for g in Group.query.order_by('name')],
        choices=[(g.id, g.source_name) for g in session.query(Traffic_source).order_by('source_name').all()],
        coerce=int,
    )
    camp_base_url = TextField(
        'Campaign domain',
        [
            DataRequired(),
            Length(min=4,
            message=('Your message is too short.'))
        ]
    )
    
    path1weight = IntegerField(
        'path1weight'
    )
    path1lander1 = SelectField(
        'path1lander1', validate_choice=False,
        choices=lander_list()
    )
    path1lander1weight = IntegerField(
        'path1lander1weight'
    )

class Landerform(FlaskForm):
    lander_name = StringField()
    lander_url = StringField()
    submit = SubmitField('Submit')

class Offerform(FlaskForm):
    offer_name = StringField()
    offer_url = StringField()
    click_param = StringField()
    affiliate_network = SelectField()
    submit = SubmitField('Submit')

class Path(FlaskForm):   
    name = StringField()
    weight = IntegerField()
    lander = FieldList(SelectField(validate_choice=False), min_entries=1)
    lander_weight = FieldList(SelectField(validate_choice=False), min_entries=1)
    offer = FieldList(SelectField(validate_choice=False), min_entries=1)
    offer_weight = FieldList(SelectField(validate_choice=False), min_entries=1)
    class Meta:
        # This overrides the value from the base form.
        csrf = False
    
class campaignas(FlaskForm):
    name = StringField()
    traffic_source = SelectField()
    path = FieldList(FormField(Path), min_entries=1)
    submit = SubmitField('Submit')

class TrafficSourceForm(FlaskForm):
    name = StringField()
    cost_query = StringField()
    cost_token = StringField()
    custom_param1_query = StringField()
    custom_param1_token = StringField()
    custom_param2_query = StringField()
    custom_param2_token = StringField()
    custom_param3_query = StringField()
    custom_param3_token = StringField()
    custom_param4_query = StringField()
    custom_param4_token = StringField()
    custom_param5_query = StringField()
    custom_param5_token = StringField()
    custom_param6_query = StringField()
    custom_param6_token = StringField()
    custom_param7_query = StringField()
    custom_param7_token = StringField()
    custom_param8_query = StringField()
    custom_param8_token = StringField()
    custom_param9_query = StringField()
    custom_param9_token = StringField()

    submit = SubmitField('Submit')



