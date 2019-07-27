
from . import api
from .auth import auth
from flask import jsonify, request, g,url_for
from app.models import Cards
from app import db

import requests

# this is not here ?!  # get card by id
@api.route('/cards/<int:id>/', methods=['GET', 'POST'])
@auth.login_required
def get_card(id):
    card = Cards.query.get_or_404(id)
    return jsonify(card.to_dict())

# get collection of cards resource
@api.route('/cards/', methods=['GET', 'POST'])
@auth.login_required
def get_cards():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Cards.to_collection_dict(Cards.query, page, per_page, 'api.get_cards')
    return jsonify(data)

# dht11 from the card [id]
@api.route('/cards/<int:id>/dht11/', methods= ['GET', 'POST'])
@auth.login_required
def get_card_dht11(id):
    card = Cards.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = card.to_collection_dict(card.dht11_values, page, per_page, 'api.get_card_dht11', id=id)  # cards is relationship
    return jsonify(data)


@api.route('/cards/', methods=['POST'])
def new_card():
    card = Cards.from_json(request.to_json())
    card.owner = g.current_user
    db.session.add(card)
    db.session.commit()
    return jsonify(card.to_dict(), 201, {'Location': url_for('api.get_card', id=card.id)})



