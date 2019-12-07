import tempfile
import pytest

from pgbackup import storage

@pytest.fixture
def infile():
    f=tempfile.TemporaryFile()
    f.write(b'Testing')
    f.seek(0)
    return f
def test_storing_file_locally(infile):
    """
    Writes content from one file-like to another
    """

    # docs.pthon.org/3/library/tempfile.html
    outfile=tempfile.NamedTemporaryFile(delete=False)#it won't delete file ones it's closed
    storage.local(infile,outfile)
    with open(outfile.name, 'rb') as f:
        assert f.read()==b'Testing'

def test_storing_file_on_s3(mocker, infile):
    """
    Writes content from one file-like to s3
    """
    #client comes from boto3
    client = mocker.Mock()
    storage.s3(client, infile, "bucket", "file-name")
    client.upload_fileobj.assert_called_with(infile,"bucket","file-name")
