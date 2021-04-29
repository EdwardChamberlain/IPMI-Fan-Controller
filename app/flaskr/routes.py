import flask
from flaskr import app
from flaskr import forms

import logging

import config
import ipmitools

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    control_form = forms.Fanspeed_Form() 
    
    if control_form.validate_on_submit():
        if None in [config.IPMI_HOST, config.IPMI_USER, config.IPMI_PASS]:
            logging.error("UPDATE FAILED: A required enviroment variable has not been set.")
            flask.flash("A required enviroment variable has not been set. Have you supplied your IPMI username, password, and host in the configure page?")

        elif config.MANUAL_MODE is False:
            logging.error("UPDATE FAILED: Cannot control fan speed in auto mode.")
            flask.flash("Fan speed cannot be controlled. Enable manual control mode.")

        else:
            result = ipmitools.set_fan_speed(control_form.speed.data)
            flask.flash(result or f"Fans set to {control_form.speed.data}%")

    return flask.render_template(
        'index.html',
        form=control_form
    )

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    IPMI_form = forms.Configure_Form()
    startup_form = forms.StartUp_Form()

    if IPMI_form.validate_on_submit():
        config.IPMI_HOST = IPMI_form.host.data or config.IPMI_HOST
        config.IPMI_USER = IPMI_form.user.data or config.IPMI_USER
        config.IPMI_PASS = IPMI_form.passwd.data or config.IPMI_PASS
        flask.flash("Config Updated")

    return flask.render_template(
        'configure.html',
        IPMI_form=IPMI_form,
        startup_form=startup_form,
    )

@app.route('/')
@app.route('/set_manual_mode')
def set_manual_mode():
    if None in [config.IPMI_HOST, config.IPMI_USER, config.IPMI_PASS]:
        logging.error("MANUAL MODE NOT SET: A required enviroment variable has not been set.")
        flask.flash("A required enviroment variable has not been set. Have you supplied your IPMI username, password, and host in the configure page?")

    else:
        result = ipmitools.set_manual_mode()
        flask.flash(result or "Manual Mode Set. Please monitor temps.")

        if not result:
            config.MANUAL_MODE = True

    return flask.redirect(flask.url_for('configure'))
