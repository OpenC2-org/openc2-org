import json, os
from openc2 import OpenC2Command
from bottle import Bottle, request, run, static_file

device = Bottle()


@device.route("/")
@device.route("/index.html")
def send_index():
    return send_static("index.html")


@device.route("/static/<filename:path>")
def send_static(filename):
    return static_file(filename, root=DOC_ROOT)


@device.post("/openc2/")
def command():
    body = request.body.read().decode(encoding="UTF-8")
    try:
        oc2 = OpenC2Command()
        cmd = oc2.from_json(body)
        cmdname = cmd["action"]
        cmdval = cmd
        resp = "Wheeee! +\nCommand = " + cmdname + " +\n  Target = " + cmdval["target"]["type"]
        for k,v in cmdval["target"]["specifiers"].items():
            resp += " +\n    " + k + ": " + str(v)
        resp += " + ..."
    except json.JSONDecodeError:
        resp = "JSON Decode Error: " + body
    return resp

if __name__ == "__main__":
    DOC_ROOT = os.path.join(os.getcwd(), "www")
    print("static content", DOC_ROOT)
    run(device, host="localhost", port=8080, debug=True)
