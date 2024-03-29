import pytest
import subprocess
from pgbackup import pgdump

url = "postgres://demo:password@peddyua1c.mylabserver.com:5432/notes"

def test_dump_calls_pg_dump(mocker):
    """
    Utilize pg_dump with database URL
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(['pg_dump', url], stdout=subprocess.PIPE)



def test_dump_handles_oserror(mocker):
    """
    pgdump.dump returns a reasonable error if pg_dump isn't installed.
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)

def test_dump_file_name_without_timestamp():
    """
    pgdump.dump_file_name returns the name of the database
    """
    assert pgdump.dump_file_name(url)=='db_one.sql'

def test_dump_file_name_with_timestamp():
    """
    pgdump.dump_file_name returns the name of the datababse with timestamp
    """
    timestamp= "2017-12-03T13:40:02"
    assert pgdump.dump_file_name(url,timestamp) == f"db_one-2017-12-03T13:14:10.sql"

