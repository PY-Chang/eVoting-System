import pytest
import ServerClass as server
from DbAdapter import DbAdapter
from nacl.signing import VerifyKey
from nacl.encoding import Base64Encoder

import eVoting_pb2
import eVoting_pb2_grpc
from datetime import datetime, timedelta
from time import sleep

class TestServer:

    def test_add_token(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_token(b'54321', "apple")
        res = s.isValid_token(b'54321')
        assert res == True

    #def test_isValid_token(self)   ## same as test_add_token

    def test_isValid_token_not_exist(self):
        s = server.Server("127.0.0.1", 4001)
        res = s.isValid_token(b'489465146516')
        assert res == False

    def test_get_name_by_token(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_token(b'6325', "banana")
        name = s.get_name_by_token(b'6325')
        assert name == "banana"

    def test_add_challenge(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_challenge("coke", b'4657')
        challenge = s.get_challenge("coke")
        assert challenge == b'4657'
    
    def test_get_challenge(self):
        s = server.Server("127.0.0.1", 4001)
        challenge = s.get_challenge("nope")
        assert challenge == None

    def test_add_register(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_register("duke", "DD", b'15165156')
        status = s.add_register("duke", "DD", b'15165156')
        # print(status)
        assert status == 1
    
    def test_del_register(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_register("duke", "DD", b'15165156')
        status = s.del_register("duke")
        assert status == 0
    
    def test_get_register(self):
        s = server.Server("127.0.0.1", 4001)

        with open("key_base64.pub", "rb") as f:
            public_key_byte = f.read()
        
        public_key = VerifyKey(public_key_byte, encoder=Base64Encoder)

        s.add_register("thx", "tt", public_key_byte)
        res = s.get_register("thx")
        s.del_register("thx")
        assert res["group"] == "tt"
        assert res["public_key"] == public_key

    def test_get_register_publicKey(self):
        s = server.Server("127.0.0.1", 4001)
        with open("key_base64.pub", "rb") as f:
            public_key_byte = f.read()
        
        public_key = VerifyKey(public_key_byte, encoder=Base64Encoder)

        s.add_register("plz", "nn", public_key_byte)
        key = s.get_register_publicKey("plz")
        s.del_register("plz")
        assert key == public_key


    def test_add_election(self):
        s = server.Server("127.0.0.1", 4001)
        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        res = s.isExisted_election("unittest")
        assert res == True

    def test_isExisted_election(self):
        s = server.Server("127.0.0.1", 4001)
        res = s.isExisted_election("nope")
        assert res == False

    def test_get_election(self):
        s = server.Server("127.0.0.1", 4001)
        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        res = s.get_election("unittest")
        assert res['groups'] == election.groups[0]

    def test_add_vote(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_register("why", "pass", b'15165156')

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        s.add_vote("unittest", "true", "why")
        res = s.get_election("unittest")
        assert res['votes']["true"] == 1

    def test_isRepeated_vote(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_register("why", "pass", b'15165156')

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        s.add_vote("unittest", "true", "why")
        res = s.isRepeated_vote("unittest", "why")
        assert res == True

    def test_isRepeated_vote_not(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_register("why", "pass", b'15165156')

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        res = s.isRepeated_vote("unittest", "why")
        assert res == False

    def test_isValid_group(self):
        s = server.Server("127.0.0.1", 4001)

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        res = s.isValid_group("unittest", "pass")
        assert res == True

    def test_isValid_group_nope(self):
        s = server.Server("127.0.0.1", 4001)

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        res = s.isValid_group("unittest", "fail")
        assert res == False

    def test_isDue_election_not_due(self):
        s = server.Server("127.0.0.1", 4001)

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=3))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)

        res = s.isDue_election("unittest")
        assert res == False


    def test_isDue_election_due(self):
        s = server.Server("127.0.0.1", 4001)

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        sleep(1)

        res = s.isDue_election("unittest")
        assert res == True

    def test_get_finalized_votes(self):
        s = server.Server("127.0.0.1", 4001)
        s.add_register("why", "pass", b'15165156')

        election = eVoting_pb2.Election()
        election.name = "unittest"
        election.groups.extend(["pass"])
        election.choices.extend(["true", "false"])
        election.end_date.FromDatetime(datetime.now() + timedelta(seconds=1))
        election.token.value = bytes("Wrong token", encoding = "utf-8")

        s.add_election(election)
        s.add_vote("unittest", "true", "why")

        sleep(1)

        res = s.get_finalized_votes("unittest")
        assert res['true'] == 1
        assert res['false'] == 0


    def test_RegisterVoter_undefine_error(self):
        s = server.Server("127.0.0.1", 4001)
        res = s.RegisterVoter(eVoting_pb2.Voter(name="panic", group="A", public_key=b'let me sleep'))
        assert res.code == 2

    def test_RegisterVoter(self):
        s = server.Server("127.0.0.1", 4001)
        with open("key_base64.pub", "rb") as f:
            public_key_byte = f.read()
        
        public_key = VerifyKey(public_key_byte, encoder=Base64Encoder)

        res = s.RegisterVoter(eVoting_pb2.Voter(name="love", group="A", public_key=public_key_byte))
        s.UnregisterVoter(eVoting_pb2.Voter(name="love", group="A", public_key=public_key_byte))
        assert res.code == 0

    def test_UnregisterVoter_no_voter(self):
        s = server.Server("127.0.0.1", 4001)

        res = s.UnregisterVoter(eVoting_pb2.Voter(name="sam", group="A", public_key=b'153416546'))
        assert res.code == 1


    # def test_UnregisterVoter_undefine_error(self):
    #     s = server.Server("127.0.0.1", 4001)

    #     with open("key_base64.pub", "rb") as f:
    #         public_key_byte = f.read()
        
    #     public_key = VerifyKey(public_key_byte, encoder=Base64Encoder)

    #     s.RegisterVoter(eVoting_pb2.Voter(name="love", group="A", public_key=public_key_byte))

    #     res = s.UnregisterVoter(eVoting_pb2.Voter(name="love", group="A", public_key=b'153416546'))
    #     s.UnregisterVoter(eVoting_pb2.Voter(name="love", group="A", public_key=public_key_byte))
    #     assert res.code == 2


        









    def est(self):
        s = server.Server("127.0.0.1", 4001)
        s.isValid_token(132)