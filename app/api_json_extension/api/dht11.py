from . import api
from .auth import auth
from flask import jsonify, request
from app.models import Cards

# this is not here ?!
#@api.route('/dht11/<int:id>', methods=['GET', 'POST'])
#@auth.login_required
#def get_card(id):
 #   return jsonify(Cards.query.get_or_404(id).to_dict())