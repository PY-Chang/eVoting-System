from concurrent import futures
from ctypes import resize
import logging
from random import choices
import signal
import sys
from typing import Optional

import grpc
import nacl
import eVoting_pb2
import eVoting_pb2_grpc

import secrets
from nacl.signing import SigningKey
from nacl.signing import VerifyKey
from nacl.encoding import Base64Encoder
from datetime import datetime, timedelta
from DbAdapter import DbAdapter

# Define
TOKEN_SIZE = 4
CHALLENGE_SIZE = 4

class Server: 

    ''' Internal State '''
    # index: register_name, value: {"group", "public_key"}
    registration_table = {}
    # index: register_name, value: challenge
    challenge_table = {} 
    # index: token, value: {"expired", "name"}
    token_table = {} 
    # index: election_name, value: {"end_date", "groups", "votes", "voters"}
    election_table = {}

    ''' TOKEN '''

    def __init__(self, db_ip, db_port):
        self.db_ip = db_ip
        self.db_port = db_port

    def add_token(self, index, name):
        expired = datetime.now()+timedelta(hours=1)
        db = DbAdapter(self.db_ip, self.db_port)
        db.add_token(index, expired, name)
        #self.token_table[index] = {"expired": expired, "name": name}

    def isValid_token(self, index):
        #if index not in self.token_table:
        #    return False
        #expired = self.token_table[index]["expired"]
        db = DbAdapter(self.db_ip, self.db_port)
        expired, name = db.get_token(index)
        ################## Fault Found!! by test_create_election_invalid_auth_token() ##################
        if name == None:
            return False
        else:
            return datetime.now()<expired

    def get_name_by_token(self, index):
        #return self.token_table[index]["name"]
        db = DbAdapter(self.db_ip, self.db_port)
        expired, name = db.get_token(index)
        return name

    ''' CHALLENGE '''

    def add_challenge(self, index, challenge):
        #self.challenge_table[index] = challenge
        db = DbAdapter(self.db_ip, self.db_port)
        db.add_challenge(index, challenge)

    def get_challenge(self, index):
        #return self.challenge_table[index]
        db = DbAdapter(self.db_ip, self.db_port)
        challenge = db.get_challenge(index)
        return challenge
    
    ''' REGISTRATION '''

    def add_register(self, index, group, public_key):
        db = DbAdapter(self.db_ip, self.db_port)
        status = db.add_register(index, group, public_key)
        return status
        #self.registration_table[index] = {"group": group, "public_key": public_key}

    def del_register(self, index):
        db = DbAdapter(self.db_ip, self.db_port)
        status = db.del_register(index)
        return status

    def get_register(self, index):
        db = DbAdapter(self.db_ip, self.db_port)
        group, public_key = db.get_register(index)
        table = {"group" : group, "public_key" : public_key}
        return table
        #return self.registration_table[index]

    def get_register_publicKey(self, index):
        db = DbAdapter(self.db_ip, self.db_port)
        group, public_key = db.get_register(index)
        return public_key
        #return self.registration_table[index]["public_key"]

    ''' ELECTION '''

    def add_election(self, election):
        db = DbAdapter(self.db_ip, self.db_port)
        index = election.name
        #votes = {}
        #for choice in election.choices:
        #    votes[choice] = 0
        due = election.end_date.ToDatetime()
        #self.election_table[index] = {"end_date": due, "groups": election.groups, "votes": votes, "voters": []}
        db.add_election(index, due, election.groups, election.choices)

    def isExisted_election(self, index):
        db = DbAdapter(self.db_ip, self.db_port)
        elections = db.get_all_elections()
        index = index.replace('?','')
        return index in elections
    
    def get_election(self, index):
        db = DbAdapter(self.db_ip, self.db_port)
        election = db.get_election(index)
        return election
        #return self.election_table[index]

    def add_vote(self, index, choice, voter):
        db = DbAdapter(self.db_ip, self.db_port)
        db.add_vote(index, choice, voter)
        #self.election_table[index]["votes"][choice] += 1
        #self.election_table[index]["voters"].append(voter)

    def isRepeated_vote(self, index, voter):
        election = self.get_election(index)
        # print("voters are " + election["voters"])
        # print(election)
        return voter in election["voters"]

    def isValid_group(self, index, group):
        election = self.get_election(index)
        #election = self.election_table[index]
        group_list = election["groups"].split(',')
        for iter in group_list:
            if iter == group:
                return True
        return False
        # return group in election["groups"]

    def isDue_election(self, index):
        election = self.get_election(index)
        #election = self.election_table[index]
        return datetime.now()>election["end_date"]

    def get_finalized_votes(self, index):
        election = self.get_election(index)
        #election = self.election_table[index]
        return election["votes"]

    ####################### Local Service API #######################
    def RegisterVoter(self, voter: eVoting_pb2.Voter) -> Optional[eVoting_pb2.Status]:
        try:
            index = voter.name
            public_key = VerifyKey(voter.public_key, encoder=Base64Encoder)
            status = self.add_register(index, voter.group, voter.public_key)
            return eVoting_pb2.Status(code=status)
            '''
            if index not in self.registration_table: 
                # Create a VerifyKey object from a hex serialized public key
                return eVoting_pb2.Status(code=0) # Status.code=0 : Successful registration
            else:
                return eVoting_pb2.Status(code=1) # Status.code=1 : Voter with the same name already exists
            '''

        except:
            return eVoting_pb2.Status(code=2) # Status.code=2 : Undefined error
        

    def UnregisterVoter(self, votername: eVoting_pb2.VoterName) -> Optional[eVoting_pb2.Status]:
        try:
            index = votername.name
            status = self.del_register(index)
            return eVoting_pb2.Status(code=status)
            '''
            if index in self.registration_table:  # Status.code=0 : Successful registration
                del self.registration_table[index]
                return eVoting_pb2.Status(code=0)
            else:
                return eVoting_pb2.Status(code=1) # Status.code=1 : No voter with the name exists on the server
            '''

        except:
            return eVoting_pb2.Status(code=2) # Status.code=2 : Undefined error