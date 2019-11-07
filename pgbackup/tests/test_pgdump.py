import pytest
import subprocess
from pgbackup import pgdump

url = "postgres://demo:password@peddyua1c.mylabserver.com:5432/notes"

def test_dump_calls_pg_dump(mocker):
    """
    Utilize pg_dump with database URL
    """
    mocker.patch('subprocess.Popen')
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(['pg_dump', url], stdout=subprocess.PIPE)



def test_dump_handles_oserror(mocker):
    """
    pgdump.dump returns a reasonable error if pg_dump isn't installed.
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('no such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)
