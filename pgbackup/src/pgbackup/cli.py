from argparse import Action,ArgumentParser

known_drivers=['local','s3']
class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error("Unknown driver. Available drivers are 'local' and 's3'")
        namespace.driver = driver.lower()
        namespace.destination = destination
        #validation of driver can be added

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('url', help="URL of the PostgreSQL database to backup")
    parser.add_argument('--driver','-d',
            help="how & where to store the backup",
            nargs=2,
            action=DriverAction,
            metavar=('driver','destination'),
            required=True)
    return parser

def main():
    #we need boto3 to create a client
    #we need pgdump and storage modules
    # create parser, parse the args and fetch the dump information
    import time
    import boto3
    from pgbackup import pgdump,storage

    args = create_parser().parse_args()
    #once we have the argsand regardless where we'll store it, we need information from postgresql server
    dump = pgdump.dump(args.url)#if url isn't given we'll have problems up above, if url is bed pgdump will rise an error //
    if args.driver == 's3':
        client = boto3.client('s3')
        #https://docs.python.org/3/library/time.html#time.strftime
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime())
        file_name=pgdump.dump_file_name(args.url, timestamp)
        print(f"Backing database up to {args.destination} in S3 as {file_name}")
        storage.s3(client, dump.stdout, args.destination,file_name)
    else:
        outfile = open(args.destination, 'wb')
        print(f"Backing database locally {args.destination}")
        storage.local(dump.stdout, outfile)
