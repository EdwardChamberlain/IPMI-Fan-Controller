import flask
from flaskr import app
from flaskr import forms
from flaskr import request

import logging

import config
import ipmitools


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    control_form = forms.Fanspeed_Form()

    if control_form.validate_on_submit():
        if None in [config.IPMI_HOST, config.IPMI_USER, config.IPMI_PASS]:
            logging.error(
                "UPDATE FAILED: A required enviroment variable has not been set."
            )
            flask.flash(
                "A required enviroment variable has not been set. Have you supplied your IPMI username, password, and host in the configure page?"
            )

        elif config.MANUAL_MODE is False:
            logging.error("UPDATE FAILED: Cannot control fan speed in auto mode.")
            flask.flash("Fan speed cannot be controlled. Enable manual control mode.")

        else:
            result = ipmitools.set_fan_speed(control_form.speed.data)
            flask.flash(result or f"Fans set to {control_form.speed.data}%")

    return flask.render_template(
        "index.html", MANUAL_MODE=config.MANUAL_MODE, form=control_form
    )


@app.route("/configure", methods=["GET", "POST"])
def configure():
    configure_form = forms.Configure_Form()

    if configure_form.validate_on_submit():
        config.IPMI_HOST = configure_form.host.data or config.IPMI_HOST
        config.IPMI_USER = configure_form.user.data or config.IPMI_USER
        config.IPMI_PASS = configure_form.passwd.data or config.IPMI_PASS
        flask.flash("Config Updated")

    return flask.render_template("configure.html", form=configure_form)


@app.route("/set_manual_mode")
def set_manual_mode():
    if None in [config.IPMI_HOST, config.IPMI_USER, config.IPMI_PASS]:
        logging.error(
            "MANUAL MODE NOT SET: A required enviroment variable has not been set."
        )
        flask.flash(
            "A required enviroment variable has not been set. Have you supplied your IPMI username, password, and host in the configure page?"
        )

    else:
        result = ipmitools.set_manual_mode()
        flask.flash(result or "Manual Mode Set. Please monitor temps.")

        if not result:
            config.MANUAL_MODE = True

    return flask.redirect(flask.url_for("configure"))


@app.route("/set_auto_mode")
def set_auto_mode():
    if None in [config.IPMI_HOST, config.IPMI_USER, config.IPMI_PASS]:
        logging.error(
            "AUTOMATIC MODE NOT SET: A required enviroment variable has not been set."
        )
        flask.flash(
            "A required enviroment variable has not been set. Have you supplied your IPMI username, password, and host in the configure page?"
        )

    else:
        result = ipmitools.set_auto_mode()
        flask.flash(result or "Auto Mode Set. Fan control disabled.")

        if not result:
            config.MANUAL_MODE = False

    return flask.redirect(flask.url_for("configure"))


@app.route("/set_fan_speeds")
def set_fan_speeds():
    percent = request.args.get("percent", default="99")
    if None in [config.IPMI_HOST, config.IPMI_USER, config.IPMI_PASS]:
        logging.error("UPDATE FAILED: A required enviroment variable has not been set.")
        flask.flash(
            "A required enviroment variable has not been set. Have you supplied your IPMI username, password, and host in the configure page?"
        )
    elif config.MANUAL_MODE is False:
        logging.error("UPDATE FAILED: Cannot control fan speed in auto mode.")
        flask.flash("Fan speed cannot be controlled. Enable manual control mode.")
    else:
        ipmitools.set_fan_speed(percent)
        flask.flash(f"Fans set to {percent}%")
    return flask.redirect(flask.url_for("index"))
