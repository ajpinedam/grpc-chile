import grpc
from character_pb2 import Allegiance, CharacterRequest
from character_pb2_grpc import GOTCharacterStub

channel = grpc.insecure_channel("localhost:50052")
client = GOTCharacterStub(channel)

request = CharacterRequest(house=Allegiance.LANNISTER, max_results=3)

client.GetCharacter(request)