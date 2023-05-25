# recommendations/recommendations.py
from concurrent import futures
import random
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from character_pb2 import (
    Allegiance,
    Character,
    CharacterResponse,
)

import character_pb2_grpc

HOUSES = {
    Allegiance.STARK: [
        Character(id=1,
                  title="Lord of Winterfell",
                  name="Ned Stark",
                  house=Allegiance.STARK,
                  age=55,
                  email="ned.stark@gmail.com",
                  religion="Old Gods of the Forest"),
        Character(id=2,
                  title="Princess",
                  name="Arya Stark",
                  house=Allegiance.STARK,
                  age=15,
                  email="arya.stark@gmail.com",
                  religion="Old Gods of the Forest"),
        Character(id=3,
                  title="King",
                  name="Robb Stark",
                  house=Allegiance.STARK,
                  age=31,
                  email="robb.stark@gmail.com",
                  religion="Old Gods of the Forest"),
    ],

    Allegiance.GREYJOY: [
        Character(id=4,
                  title="Prince",
                  name="Theon Greyjoy",
                  house=Allegiance.GREYJOY,
                  age=31,
                  email="theon.greyjoy@gmail.com",
                  religion="Drowned God"),
    ],    

    Allegiance.LANNISTER: [
        Character(id=10,
                  title="Queen",
                  name="Cersei Lannister",
                  house=Allegiance.LANNISTER,
                  age=37,
                  email="cersei.lannister@gmail.com",
                  religion="Faith of the Seven"),

        Character(id=5,
                  title="Ser",
                  name="Jaime Lannister",
                  house=Allegiance.LANNISTER,
                  age=44,
                  email="jaime.lannister@gmail.com",
                  religion="Faith of the Seven"),
        Character(id=6,
                  title="Lord",
                  name="Tyrion Lannister",
                  house=Allegiance.LANNISTER,
                  age=49,
                  email="tyrion.lannister@gmail.com",
                  religion="Faith of the Seven"),
    ],

    Allegiance.BARATHEON: [
        Character(id=7,
                  title="Ser",
                  name="Raymont Baratheon",
                  house=Allegiance.BARATHEON,
                  age=55,
                  email="raymont.baratheon@gmail.com",
                  religion="Faith of the Seven"),
        Character(id=8,
                  title="Ser",
                  name="Orys Baratheon",
                  house=Allegiance.BARATHEON,
                  age=55,
                  email="orys.baratheon@gmail.com",
                  religion="Faith of the Seven"),
    ],

    Allegiance.TARGARYEN: [
        Character(id=9,
                  title="Princess",
                  name="Daenerys Targaryen",
                  house=Allegiance.TARGARYEN,
                  age=24,
                  email="daenerys.targaryen@gmail.com",
                  religion="Faith of the Seven"),
    ],      
}

class GotCharactersService(character_pb2_grpc.GOTCharacterServicer):
    def GetCharacter(self, request, context):
        if request.house not in HOUSES:
            raise NotFound("Character not found")

        request_houses = HOUSES[request.house]
        num_results = min(request.max_results, len(request_houses))
        result = random.sample(request_houses, num_results)

        return CharacterResponse(characters=result)

def serve_rpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    character_pb2_grpc.add_GOTCharacterServicer_to_server(
        GotCharactersService(), server
    )

    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve_rpc()
