## 1. server.py
* isValid_token()
* line 56~590
* lack of error handling (expired might be none)

## 2. server.py
* isValid_group
* line 144~148
* since election["groups"] is a string, if the group name is the substring of the election["groups"] the it will return true

## 3. DbAdapter.py
* add_election
* line 171~175
* found by test_cast_vote_success
* because the type checking is not complete, choices pass by RPC call is google protobuf 