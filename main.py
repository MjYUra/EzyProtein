import flask
from pair_search import pair_search,pairs_search,getModel,calculateg
from flask_cors import CORS
import json
f=open("./human_interactome.txt","r");
app = flask.Flask(__name__)
CORS(app)
@app.route("/")
def myIndex():
	return flask.render_template("index.html")

@app.route('/models/<path:filename>',methods=['GET','POST'])
def giveModel(filename):
    #path=flask.request.args.get('filename');
    return flask.send_from_directory(directory='models',filename=filename);


@app.route('/home', methods=['POST'])
def search():
	#s = flask.request.values["data"];
	s=flask.request.get_json();
	s=s["data"];
	if(s[2]["type"] == '0'):
	    a=pairs_search(s[0]["name"],float(s[1]["value"]),{"nodes":[],"edges":[]},1,{},set(),f);
	elif(s[2]["type"] == '1'):
	    a=getModel(s[0]["p1"],s[1]["p2"]);
	elif(s[2]["type"] == '2'):
		a=calculateg(s[0]["model"],s[1]["mut"]);
		
	
	#results=pair_search(s);
	#return flask.render_template("index.html", result=json.dumps(result))
	return json.dumps(a)

if __name__ == "__main__":
	with open("./human_interactome.txt","r") as f:
	    app.run(debug=True)
	
