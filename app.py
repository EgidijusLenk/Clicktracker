from models import Campaign, Click, Lander, Offer, Traffic_source, Affiliate_network
from flask import Flask, redirect, sessions, url_for, request, render_template, flash
from objects import create_new_click, click_to_offer, submit_campaign_data
from models import session, campaigns_query, Session
import simplejson as json
from forms import Create_campaign, Path, campaignas, Landerform, Offerform, TrafficSourceForm
app = Flask(__name__)







@app.route("/")
def nav():
    
    return render_template('nav.html', title='Welcome')


@app.route("/campaigns")
def campaigns():
    return render_template('campaigns.html', title='Campaigns')
#------




@app.route("/datatable")
def datatable():
    return render_template(
        'campaigns_table.html',
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja."
    )

@app.route("/go/<camp_id>")
def go(camp_id):
    z = request.query_string.decode('UTF-8')
    returned_object = create_new_click(camp_id,z)
    return f"""  <h1> and lander:   {returned_object[0]} and offer link: {returned_object[1]} <h1>
    <script type="text/javascript"> 
    localStorage.setItem("camp_lander", "{returned_object[0]}")
    localStorage.setItem("camp_offer", "{returned_object[1]}");
    localStorage.setItem("unique_click_id", "{returned_object[2]}");
    let x = localStorage.getItem("camp_lander");
    location.href = x
    </script>
    """
#---dummylander page---
@app.route("/dummylander")
def dummylander():
    return f"""this is dummy lander
        <form action="http://127.0.0.1:5000/redirecting">
        <input type="submit" value="BUY NOW" />
        </form>
        """
#---dummylander page end---

#-----redirect page -----
@app.route("/redirecting")
def redirect_to_offer():
    return render_template("/offerclicked.html")

    
#-----redirect page end-----

@app.route("/offerclicked", methods = ['POST'])
def redirect_to_offerx():
    unique_click_id = request.data.decode('UTF-8')
    click_to_offer(unique_click_id)
    print(f"\n\n\n\n\n  \n\n\n\n\n {unique_click_id}")
    return ('', 204) #204 means: return nothing
#---- dummy offer page-------
@app.route("/dummyoffer")
def dummyoffer():
    c = request.query_string.decode('UTF-8')
    return f"""Congrats! this is dummy offer page <br> param string is: <br> {c}"""
#---- dummy offer page end-------

#---- dummy camp base page-------
@app.route("/dummpybase")
def dummybase():
    return f"this is dummy base page"
#-------dummy camp base page end----------


@app.route("/newcampaign", methods=["GET", "POST"])
def newcampaign():
    landers = [{"value":g.id, "name": f"{g.lander_name} - {g.lander_url}"} for g in session.query(Lander).order_by('id').all()]
    offers = [{"value":g.id, "name": f"{g.offer_name} - {g.offer_url}"} for g in session.query(Offer).order_by('id').all()]
    traffic_sources = [{"value":g.id, "name": f"{g.source_name}"} for g in session.query(Traffic_source).order_by('id').all()]
    form = campaignas() 
    print(f"\n\n\n form.data: \n\n\n {form.data} \n\n errors: \n{form.errors}")
    if form.validate_on_submit(): 
        print(f"\n\n\n form validates: \n\n\n {form.data}\n")
    return render_template('newcampaign.html', form=form, landers=landers, offers=offers, traffic_sources=traffic_sources)


@app.route("/newlander", methods=["GET", "POST"])
def newlander():
    form = Landerform() 
    print(f"\n\n\n form.data: \n\n\n {form.data} \n\n errors: \n{form.errors}")
    if form.validate_on_submit(): 
        print(f"\n\n\n form validates: \n\n\n {form.data}\n")
    return render_template('newlander.html',form=form)


@app.route("/newoffer", methods=["GET", "POST"])
def newoffer():
    affiliate_network = [{"value":g.id, "name": f"{g.network_name}"} for g in session.query(Affiliate_network).order_by('id').all()]
    form = Offerform() 
    print(f"\n\n\n form.data: \n\n\n {form.data} \n\n errors: \n{form.errors}")
    if form.validate_on_submit(): 
        print(f"\n\n\n form validates: \n\n\n {form.data}\n")
    return render_template('newoffer.html',form=form, affiliate_network=affiliate_network)

@app.route("/newtrafficsource", methods=["GET", "POST"])
def newtrafficsource():
    form = TrafficSourceForm() 
    print(f"\n\n\n form.data: \n\n\n {form.data} \n\n errors: \n{form.errors}")
    if form.validate_on_submit(): 
        print(f"\n\n\n form validates: \n\n\n {form.data}\n")
    return render_template('newtrafficsource.html', form=form)


#---get landers list nebenaudojama---
@app.route('/api/landers')
def landerslist():
    return json.dumps([{"value":g.id, "name": f"{g.lander_name} - {g.lander_url}"} for g in session.query(Lander).order_by('id').all()])
#---get landers list end---

#---get offers list nebenaudojama---
@app.route('/api/offers')
def offerslist():
    return json.dumps([{"value":g.id, "name": f"{g.offer_name} - {g.offer_url}"} for g in session.query(Offer).order_by('id').all()])
#---get offers list end---





#---data endpoint---
@app.route("/api/campaigns")
def data():
    click_data = [click.to_dict() for click in session.query(Click)]
    print(f"\n\n\n data: \n\n\n {click_data}")
    return json.dumps(click_data)
#---data endpoint end---

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
    
