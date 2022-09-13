"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        
        "family": members
    }

    return jsonify(response_body), 200,


@app.route('/member/<int:member_id>', methods=['GET'])
def member_id(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)

    if member == None:
        return jsonify("no se encontró"), 400,

    return jsonify(member), 200,



@app.route('/member', methods=['POST'])
def post_member():
    print (request.json)
    newMember = jackson_family.add_member(request.json)
    # this is how you can use the Family datastructure by calling its methods
    if newMember == request.json:
        return jsonify('se agregó un nuevo miembro'), 200
    else:
        return jsonify('No hay nuevo miembro'), 400

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(id):

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.delete_member(id)
    if members == id:
        return jsonify('no existe'), 400
    else: 
        return jsonify(members), 200


    return jsonify("se eliminó con éxito"), 200,

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
