from flask import Flask, jsonify
from flask.ext.pymongo import PyMongo
from flask.ext.cors import CORS
import os
import datetime

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


@app.route("/cours/")
def cours():
    cours = parse_cours(mongo.db.planning.find())

    return jsonify(data=cours), 200


@app.route("/cours/prochain")
def prochain_cours():
    cours = parse_cours(mongo.db.planning.find({"horaire_debut": {"$gte": datetime.datetime.utcnow()}}).sort("horaire_debut").limit(1))

    return jsonify(data=cours), 200


def parse_cours(donnees):
    cours = []
    for planning in donnees:
        planning["_id"] = str(planning["_id"])
        planning["horaire_debut"] = planning["horaire_debut"].isoformat()
        planning["horaire_fin"] = planning["horaire_fin"].isoformat()

        cours.append(planning)

    return cours


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("DEBUG", True))