# eVoting System
> This is a project of Fault Tolerant Computing in spring 2022.  
> I wrote tests for this project as final project of the class Software Testing.

## Intro 
This project is an eVoting system based on gRPC. The system would be a distributed and fault tolerant system. The picture down below is a rough visualization of the system.  
![System overview](https://imgur.com/CggzJd3.png)

The goal of the project is to develop a remote electronic voting system. With the system, a registered user can hold a vote and collect ballots from registered users that might be located at different locations. At the end of a vote, the system will count the ballots and announce the results.

## RPC APIs
```java
class eVotingServicer {
    rpc PreAuth (VoterName) returns (Challenge);
    rpc Auth (AuthRequest) returns (AuthToken);
    rpc CreateElection (Election) returns (Status);
    rpc CastVote (Vote) returns (Status);
    rpc GetResult(ElectionName) returns (ElectionResult);
}
```

## Testing Targets
### `class Server()`: 19 methods
```java
class Server {
    add_token(self, index, name);
    isValid_token(self, index);
    get_name_by_token(self, index);
    add_challenge(self, index, challenge);
    get_challenge(self, index);
    add_register(self, index, group, public_key);
    del_register(self, index);
    get_register(self, index);
    get_register_publicKey(self, index);
    add_election(self, election);
    isExisted_election(self, index);
    get_election(self, index);
    add_vote(self, index, choice, voter);
    isRepeated_vote(self, index, voter);
    isValid_group(self, index, group);
    isDue_election(self, index);
    get_finalized_votes(self, index);
    RegisterVoter(self, voter);
    UnregisterVoter(self, votername);
}
```

### `class eVotingServicer()`: 5 user callable RPC calls
```java
class eVotingServicer {
    rpc PreAuth (VoterName) returns (Challenge);
    rpc Auth (AuthRequest) returns (AuthToken);
    rpc CreateElection (Election) returns (Status);
    rpc CastVote (Vote) returns (Status);
    rpc GetResult(ElectionName) returns (ElectionResult);
}
```

### `class DbAdapter()`: 12 methods 
```java
class DbAdapter {
    add_register(self, name, group, public_key)
    del_register(self, name)
    bytes_needed(self, n)
    get_register(self, name)
    add_challenge(self, name, challenge)
    get_challenge(self, name)
    add_token(self, token, expired, name)
    get_token(self, token)
    add_election(self, election_name, end_date, groups, choices)
    get_all_elections(self)
    get_election(self, election_name)
    add_vote(self, election_name, choice, voter)
}
```

## Testing Methods
Since the project is written in python,  I use **pytest** to do unit testing and end-to-end testing.

### Unit Test
> Line Coverage & Predicate Coverage  

* `class Server()`
* `class DbAdapter()`

### End-to-End Test
> Testing all user callable gRPC APIs, and try to test every possible responses(predefined) from the server.
* `PreAuth`
* `Auth`
  * success
  * invalid
* `CreateElection`
  * Status.code=0 : Election created successfully
  * Status.code=1 : Invalid authentication token
  * Status.code=2 : Missing groups or choices specification (at least one group and one choice should be listed for the election)
  * Status.code=3 : Unknown error
* `CastVote`
  * Status.code=0 : Successful vote
  * Status.code=1 : Invalid authentication token
  * Status.code=2 : Invalid election name
  * Status.code=3 : The voter’s group is not allowed in the election
  * Status.code=4 : A previous vote has been cast.
  * Status.code=5 : Unknown error.
* `GetResult`
  * ElectionReuslt.status = 0
  * ElectionResult.status = 1: Non-existent election
  * ElectionResult.status = 2: The election is still ongoing. Election result is not available yet.


## Test Codes  
* [Test for `class Server()`](https://github.com/PY-Chang/eVoting-System/blob/755e8ba8e2f9808209a2fb47bcc88998f2776991/evoting/server_test.py)
* [Test for `class DbAdapter()`](https://github.com/PY-Chang/eVoting-System/blob/755e8ba8e2f9808209a2fb47bcc88998f2776991/evoting/testDB.py)
* [End-to-End Tests](https://github.com/PY-Chang/eVoting-System/blob/755e8ba8e2f9808209a2fb47bcc88998f2776991/evoting/test_gRPC_API.py)


## Testing Results
### `class Server()`
* **23** tests in total
* Line coverage: **98%**
![server test](https://imgur.com/MgjFfUu.png)

### `class DbAdapter()`
* **21** tests in total
* Line coverage: **100%**
![DB test](https://imgur.com/08YueS2.png)

### End-to-End Testing
* **14** tests in total
* Testing every possible RPC call condition
![E2E test](https://imgur.com/u5KjzKg.png)

## Faults Found
> All the bugs are found during end-to-end testing and had already been patched (referring to GitHub commit history listed down below).  

### `class Server()`
* `isValid_token(self, index)`: [Link](https://github.com/PY-Chang/eVoting-System/commit/755e8ba8e2f9808209a2fb47bcc88998f2776991#r76136850)
* `isValid_group()`: [Link](https://github.com/PY-Chang/eVoting-System/commit/755e8ba8e2f9808209a2fb47bcc88998f2776991#r76136922)

### `class DbAdapter()`
* `add_election()`: [Link](https://github.com/PY-Chang/eVoting-System/commit/755e8ba8e2f9808209a2fb47bcc88998f2776991#r76136997)


## How to start the system
> Since our project is written in Python, there's no need to build the code.

0. `git clone https://github.com/PY-Chang/eVoting-System.git`
1. `git checkout Software-Testing`
2. `cd rqlite-v7.3.2-linux-amd64/`
3. `./rqlited -node-id 1 node.1`
4. `cd ../evoting`
5. `python3 server.py 50003 4001`
6. open another shell
7. `cd rqlite-v7.3.2-linux-amd64/`
8. `./rqlited -node-id 2 -http-addr localhost:4003 -raft-addr localhost:4004 -join http://localhost:4001 node.2`
9. `cd ../evoting`
10. `python3 server.py 50002 4003`
11. open another shell again
12. `cd evoting`
13. `python3 manager.py`

## How to run tests
> The system must be started before testing.
* Test for `class Server()`: `make server_test`
* Test for `class DbAdapter()`: `make detail_test`
* End-to-End Test: `make api_test`