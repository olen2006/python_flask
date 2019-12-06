import tempfile
from pgbackup import storage
def test_storing_file_locally():
    """
    Writes content from one file-like to another
    """
    infile=tempfile.TemporaryFile()
    infile.write(b'Testing')
    infile.seek(0)
# docs.pthon.org/3/library/tempfile.html
    outfile=tempfile.NamedTemporaryFile(delete=False)#it won't delete file ones it's closed
    storage.local(infile,outfile)
    with open(outfile.name, 'rb') as f:
        assert f.read()==b'Testing'

