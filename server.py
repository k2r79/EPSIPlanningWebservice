from flask import Flask, jsonify
from flask.ext.pymongo import PyMongo
from flask.ext.cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

@app.route("/cours/")
def cours():
    cours = []
    for planning in mongo.db.planning.find():
        planning["_id"] = str(planning["_id"])
        planning["horaire_debut"] = planning["horaire_debut"].isoformat()
        planning["horaire_fin"] = planning["horaire_fin"].isoformat()

        cours.append(planning)

    return jsonify(data=cours), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))