def local(infile, outfile):
    outfile.write(infile.read())#open file, read from it and wrte it into another file
    outfile.close()
    infile.close()

def s3(client, infile, bucket, name):
    client.upload_fileobj(infile, bucket, name)


