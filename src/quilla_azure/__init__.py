from argparse import (
    ArgumentParser,
    Namespace
)
from pathlib import Path
from typing import Optional

from quilla.ctx import Context
from azure.storage.blob import ContainerClient


class QuillaAzure:
    container_client: Optional[str]
    run_id: Optional[str]

    def __init__(self):
        self.container_client = None
        self.run_id = None

    def quilla_addopts(self, parser: ArgumentParser):
        main_subparsers = parser.add_subparsers()
        parser = main_subparsers.add_parser(
            'az',
            help='A command to deal with images stored in azure blob storage'
        )
        az_subparsers = parser.add_subparsers()
        download_parser = az_subparsers.add_parser(
            'download',
            help='Downloads all images associated with a run ID'
        )

        download_parser.add_argument(
            'run_id',
            help='The run ID to search for'
        )
        download_parser.set_defaults(handler=lambda _: self.get_images())

    def quilla_configure(self, args: Namespace, ctx: Context):
        if args.connection_string is None:
            return
        self.container_client = ContainerClient.from_connection_string(
            args.connection_string,
            args.container_name,
        )

        self.run_id = ctx.run_id

    def get_images(self):
        if self.container_client is None:
            print('No connection string configured')
            return

        blobs = self.container_client.list_blobs()

        for blob in filter(lambda x: self.run_id in x.name, blobs):
            blob_path = Path(blob.name)
            blob_path.parent.mkdir(parents=True, exist_ok=True)
            blob_client = self.container_client.get_blob_client(blob)
            blob_data = blob_client.download_blob().readall()
            blob_path.touch()
            blob_path.write_bytes(blob_data)
