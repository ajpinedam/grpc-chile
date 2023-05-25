# client/client.py

from flask import Flask, render_template
import grpc
from character_pb2 import Allegiance, CharacterRequest
from character_pb2_grpc import GOTCharacterStub

app = Flask(__name__)

channel = grpc.insecure_channel("localhost:50052")
client = GOTCharacterStub(channel)

@app.route("/")
def render_homepage():
    request = CharacterRequest(house=Allegiance.STARK, max_results=3)
    response = client.GetCharacter(request)

    return render_template(
        "homepage.html",
        characters=response.characters,
    )