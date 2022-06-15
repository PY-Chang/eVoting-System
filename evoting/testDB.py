from DbAdapter import DbAdapter
import pyrqlite.dbapi2 as dbapi2
import pyrqlite.cursors as cursors
from datetime import datetime
import pytest
# from pytest_mock import mocker
from time import sleep

class TestDbAdapter:

    def test_add_register_none(self, mocker):
        db = DbAdapter("127.0.0.1", 4003)
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=123)
        status = db.add_register("test", 'b', b'123456')
        assert status == 1

    def test_add_register(self):
        db = DbAdapter("127.0.0.1", 4003)
        with open("key_base64.pub", "rb") as f:
            public_key_byte = f.read()
        status = db.add_register("new", 'n', public_key_byte)
        group, public_key = db.get_register("new")
        assert status == 1 #not first time run
        assert group == 'n'
    
    def test_del_register_none(self, mocker):
        db = DbAdapter("127.0.0.1", 4003)
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=None)
        status = db.del_register("test")
        assert status == 1

    def test_del_register(self, mocker):
        db = DbAdapter("127.0.0.1", 4003)
        db.add_register("temp", 't', b'123456')
        status = db.del_register("temp")
        status_get, key= db.get_register("temp")
        assert status == 0
        assert status_get == None

    def test_bytes_needed(self):
        ret = DbAdapter.bytes_needed(self, 0)
        assert ret == 1
        ret = DbAdapter.bytes_needed(self, 256)
        assert ret == 2

    def test_get_register_none(self, mocker):
        # db = DbAdapter("127.0.0.1", 4003)
        # mock_cursor = mocker.Mock()
        # mock_cursor.fetchone.return_value = None
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=None)
        group, public_key = DbAdapter.get_register(self, "Frog")
        # group, public_key = db.get_register("none")
        # print("public_key is:" + str(public_key))
        assert group == None

    def test_get_register(self):
        db = DbAdapter("127.0.0.1", 4001)
        group, public_key = db.get_register("Frog")
        # print(group)
        assert group == 'A'

    def test_get_register_mock_Verify_fetch(self, mocker):
        db = DbAdapter("127.0.0.1", 4001)
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=['mockGroup', 123456])
        mocker.patch("DbAdapter.VerifyKey", return_value='mockKey')

        group, public_key = db.get_register("mock")
        assert group == 'mockGroup'
        assert public_key == 'mockKey'

    def test_add_challenge(self):
        db = DbAdapter("127.0.0.1", 4001)
        db.add_challenge("new", b'789')
        challenge = db.get_challenge("new")
        assert challenge == b'\x00789'

    def test_get_challenge_none(self, mocker):
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=None)
        challenge = DbAdapter.get_challenge(DbAdapter, "Frog")
        assert challenge == None

    def test_add_token(self):
        db = DbAdapter("127.0.0.1", 4001)
        db.add_token(b"13579", datetime(1998, 10, 4, 10, 25 ,00), "new")
        expired_time, name = db.get_token(b"13579")
        assert expired_time == datetime(1998, 10, 4, 10, 25 ,00)
        assert name == "new"

    def test_get_token_none(self, mocker):
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=None)
        expired_time, name = DbAdapter.get_token(DbAdapter, b"13579")
        assert expired_time == None
        assert name == None

    def test_get_token_mock(self, mocker):
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=["07/10/1999, 10:25:00", "mockName"])
        expired_time, name = DbAdapter.get_token(DbAdapter, b"13579")
        assert expired_time == datetime(1999, 7, 10, 10, 25 ,00)
        assert name == "mockName"

    def test_add_election_choices_str(self):
        db = DbAdapter("127.0.0.1", 4001)
        election_name = "Presidential"
        end_date = datetime(2023, 7, 1, 10, 25 ,00)
        groups = ['all']
        choices = "Nick, Charlie"
        db.add_election(election_name, end_date, groups, choices)

        table = db.get_election(election_name)
        assert table['end_date'] == end_date

    def test_add_election_choices_list(self):
        db = DbAdapter("127.0.0.1", 4001)
        election_name = "Congress"
        end_date = datetime(2023, 7, 1, 10, 25 ,00)
        groups = ['117']
        choices = ["Kyle", "Vic"]
        db.add_election(election_name, end_date, groups, choices)

        table = db.get_election(election_name)
        # print(table)
        assert table['groups'] == groups[0]

    def test_get_all_elections_mock(self, mocker):
        mocker.patch("testDB.cursors.Cursor.fetchall", return_value=["Dont't", "say", "sorry"])
        elections = DbAdapter.get_all_elections(DbAdapter)
        assert elections == ['D', 's', 's']
    
    def test_get_election_mock(self, mocker):
        end_date = "07/01/2017, 10:25:00"
        groups = ['117']
        voters = ["Kyle", "Vic"]
        mocker.patch("testDB.cursors.Cursor.fetchone", return_value=[end_date, groups, voters])
        mocker.patch("testDB.cursors.Cursor.fetchall", return_value=["heart", "stopper"])
        mocker.patch("testDB.cursors.Cursor.execute")
        table = DbAdapter.get_election(DbAdapter, "mock")
        assert table['end_date'] == datetime(2017, 7, 1, 10, 25 ,00)
        assert table['votes'] == {'h' : 'e', 's': 't'}

    def test_add_vote(self):
        db = DbAdapter("127.0.0.1", 4001)
        election_name = "Presidential"
        choice = 'Nick'
        voter = 'new'
        db.add_vote(election_name, choice, voter)
        table = db.get_election(election_name)
        assert table['votes']['Nick'] == 1
    
    def test_add_vote_voters_none(self, capfd):
        db = DbAdapter("127.0.0.1", 4001)
        election_name = "do not exist"
        choice = 'Gale'
        voter = 'new'
        db.add_vote(election_name, choice, voter)
        out, err = capfd.readouterr()
        assert out == f'There no election name {election_name}\n'

    def test_add_vote_votes_none(self, capfd):
        db = DbAdapter("127.0.0.1", 4001)
        election_name = "Presidential"
        choice = 'Gale'
        voter = 'new'
        db.add_vote(election_name, choice, voter)
        out, err = capfd.readouterr()
        assert out == f'There no candidate name {choice}\n'
    
    def test_add_vote_new_voter(self, capfd):
        db = DbAdapter("127.0.0.1", 4001)
        election_name = "Presidential"
        choice = 'Nick'
        today = datetime.now()
        voter = str(today.strftime("%m/%d/%Y, %H:%M:%S"))
        table = db.get_election(election_name)

        db.add_vote(election_name, choice, voter)
        new_table = db.get_election(election_name)

        assert new_table['voters'] == table['voters']+ "," + voter



    

    # # @pytest.fixture()
    # def test2(self, mocker):
    #     mocker.patch("DbAdapter.DbAdapter.get_register", return_value=['B', '123'])
    #     group, public_key = DbAdapter.get_register("Frog")
    #     assert group == 'B'

    # def test_add_register(self):
    #     db = DbAdapter("127.0.0.1", 4001)
    #     status = db.add_register("none", 'a', b'324234')
    #     assert status == 1

    # def test_del_register(self):
    #     db = DbAdapter("127.0.0.1", 4001)
    #     status = db.del_register("Frog")
    #     # print(group)
    #     assert status == 0