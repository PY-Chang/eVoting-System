import base64
# from unittest import TestCase
import pytest
import grpc
from nacl.signing import SigningKey

import eVoting_pb2
import eVoting_pb2_grpc

from datetime import datetime, timedelta
from time import sleep
from DbAdapter import DbAdapter

class TestTemp:
    def est_create_election_invalid_auth_token(self): # code == 1
        with grpc.insecure_channel('localhost:50051') as channel:
            # create a stub for RPC call
            stub = eVoting_pb2_grpc.eVotingStub(channel)

            # election config
            election_name = "Presidential"
            groups = ["A"]
            choices = ["A", "B", "C"]
            due = datetime.now() + timedelta(seconds=1)  # due 1 seconds later

            # call CreateElection (declare variable in a different way due to timestamp library)
            election = eVoting_pb2.Election()
            election.name = election_name
            election.groups.extend(groups)
            election.choices.extend(choices)
            election.end_date.FromDatetime(due)
            election.token.value = bytes("Wrong token", encoding = "utf-8")
            createElectionResponse = stub.CreateElection(election)

            assert str(createElectionResponse.code) == '1' # Invalid authentication token

    def est_cast_vote_wrong_voter_group(self): # code == 3
        with grpc.insecure_channel('localhost:50051') as channel:
            # create a stub for RPC call
            stub = eVoting_pb2_grpc.eVotingStub(channel)

            # Read private key from file
            with open("private_key", "rb") as f:
                serialized_key = f.read()

            serialized_key = base64.b64decode(serialized_key)
            singning_key = SigningKey(serialized_key)

            preAuthResponse = stub.PreAuth(eVoting_pb2.VoterName(name="Frog"))

            challenge = preAuthResponse.value
            signed = singning_key.sign(challenge)
            signature = signed.signature

            authResponse = stub.Auth(eVoting_pb2.AuthRequest(
                name=eVoting_pb2.VoterName(name="Frog"), \
                response=eVoting_pb2.Response(value=bytes(signature)) \
                ))

            token = authResponse.value

            # election config
            election_name = "Presidential_wrong_group"
            groups = ["Not for A"]
            choices = ["A", "B", "C"]
            due = datetime.now() + timedelta(seconds=1)  # due 1 seconds later

            # call CreateElection (declare variable in a different way due to timestamp library)
            election = eVoting_pb2.Election()
            election.name = election_name
            election.groups.extend(groups)
            election.choices.extend(choices)
            election.end_date.FromDatetime(due)
            election.token.value = bytes(token)
            createElectionResponse = stub.CreateElection(election)

            # call CastVote
            castVoteResponse = stub.CastVote(eVoting_pb2.Vote(
                election_name=election_name,
                choice_name="A",
                token=eVoting_pb2.AuthToken(value=bytes(token))
            ))
            assert castVoteResponse.code == 3 # The voter’s group is not allowed in the election


    def est_cast_vote_already_voted(self): # code == 4
        with grpc.insecure_channel('localhost:50051') as channel:
            # create a stub for RPC call
            stub = eVoting_pb2_grpc.eVotingStub(channel)

            # Read private key from file
            with open("private_key", "rb") as f:
                serialized_key = f.read()

            serialized_key = base64.b64decode(serialized_key)
            singning_key = SigningKey(serialized_key)

            preAuthResponse = stub.PreAuth(eVoting_pb2.VoterName(name="Frog"))

            challenge = preAuthResponse.value
            signed = singning_key.sign(challenge)
            signature = signed.signature

            authResponse = stub.Auth(eVoting_pb2.AuthRequest(
                name=eVoting_pb2.VoterName(name="Frog"), \
                response=eVoting_pb2.Response(value=bytes(signature)) \
                ))

            token = authResponse.value

            # election config
            election_name = "Presidential"
            groups = ["A"]
            choices = ["A", "B", "C"]
            # choices = ["A, B, C"]
            due = datetime.now() + timedelta(seconds=5)  # due 1 seconds later

            # call CreateElection (declare variable in a different way due to timestamp library)
            election = eVoting_pb2.Election()
            election.name = election_name
            election.groups.extend(groups)
            election.choices.extend(choices)
            election.end_date.FromDatetime(due)
            election.token.value = bytes(token)
            createElectionResponse = stub.CreateElection(election)
            # print(str(createElectionResponse.code))
            # sleep(2)

            # call CastVote
            db = DbAdapter("127.0.0.1", 4001)
            Election = db.get_election(election_name)
            print(Election)
            castVoteResponse = stub.CastVote(eVoting_pb2.Vote(
                election_name=election_name,
                choice_name="A",
                token=eVoting_pb2.AuthToken(value=bytes(token))
            ))
            castVoteResponse = stub.CastVote(eVoting_pb2.Vote(
                election_name=election_name,
                choice_name="A",
                token=eVoting_pb2.AuthToken(value=bytes(token))
            ))
            assert castVoteResponse.code == 4 #  A previous vote has been cast.


    def est_cast_vote_success(self): # code == 0
        with grpc.insecure_channel('localhost:50051') as channel:
            # create a stub for RPC call
            stub = eVoting_pb2_grpc.eVotingStub(channel)

            # Read private key from file
            with open("private_key", "rb") as f:
                serialized_key = f.read()

            serialized_key = base64.b64decode(serialized_key)
            singning_key = SigningKey(serialized_key)

            preAuthResponse = stub.PreAuth(eVoting_pb2.VoterName(name="Frog"))

            challenge = preAuthResponse.value
            signed = singning_key.sign(challenge)
            signature = signed.signature

            authResponse = stub.Auth(eVoting_pb2.AuthRequest(
                name=eVoting_pb2.VoterName(name="Frog"), \
                response=eVoting_pb2.Response(value=bytes(signature)) \
                ))

            token = authResponse.value

            # election config
            election_name = "why"
            groups = ["A"]
            choices = ["A", "B", "C"]
            due = datetime.now() + timedelta(seconds=3)  # due 1 seconds later

            # call CreateElection (declare variable in a different way due to timestamp library)
            election = eVoting_pb2.Election()
            election.name = election_name
            election.groups.extend(groups)
            election.choices.extend(choices)
            election.end_date.FromDatetime(due)
            election.token.value = bytes(token)
            createElectionResponse = stub.CreateElection(election)


            db = DbAdapter("127.0.0.1", 4001)
            # db.add_election(election_name, due, groups, choices)
            Election = db.get_election(election_name)
            print(Election)

            # call CastVote
            castVoteResponse = stub.CastVote(eVoting_pb2.Vote(
                election_name=election_name,
                choice_name="A",
                token=eVoting_pb2.AuthToken(value=bytes(token))
            ))
            assert castVoteResponse.code == 0

    def test_redundent(sef):
        db = DbAdapter("127.0.0.1", 4003)
        with open("key_base64.pub", "rb") as f:
            public_key_byte = f.read()
        status = db.add_register("bob", 'n', public_key_byte)
        group, public_key = db.get_register("bob")

        db2 = DbAdapter("127.0.0.1", 4001)
        group2, public_key2 = db2.get_register("bob")
        db2.del_register("bob")
        group3, public_key = db.get_register("bob")
        assert group3 == None