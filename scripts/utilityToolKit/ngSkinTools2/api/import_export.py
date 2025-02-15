from os import unlink

from ngSkinTools2.api import plugin

from . import transfer
from .influenceMapping import InfluenceMappingConfig


# noinspection PyClassHasNoInit
class FileFormat:
    JSON = "json"
    CompressedJSON = "compressed json"


# noinspection PyShadowingBuiltins
def import_json(
    target,
    file,
    vertex_transfer_mode=transfer.VertexTransferMode.closestPoint,
    influences_mapping_config=InfluenceMappingConfig.transfer_defaults(),
    format=FileFormat.JSON,
):
    """
    Transfer layers from file into provided target mesh. Existing layers, if any, will be preserved

    :param str target: destination mesh or skin cluster node name
    :param str file: file path to load json from
    :param vertex_transfer_mode: vertex mapping mode when matching imported file's vertices to the target mesh
    :param InfluenceMappingConfig influences_mapping_config:
    :param str format: expected file format, one of `FileFormat` values
    """

    importer = transfer.LayersTransfer()
    importer.vertex_transfer_mode = vertex_transfer_mode
    importer.influences_mapping.config = influences_mapping_config
    importer.load_source_from_file(file, format=format)
    importer.target = target
    importer.execute()


# noinspection PyShadowingBuiltins
def export_json(target, file, format=FileFormat.JSON):
    """
    Save skinning layers to file in json format, to be later used in `import_json`

    :param str target: source mesh or skin cluster node name
    :param str file: file path to save json to
    :param str format: exported file format, one of `FileFormat` values
    """

    with FileFormatWrapper(file, format=format, read_mode=False) as f:
        plugin.ngst2tools(
            tool="exportJsonFile",
            target=target,
            file=f.plain_file,
        )


def compress_gzip(source, dest):
    import gzip
    import shutil

    with open(source, 'rb') as f_in, gzip.open(dest, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def decompress_gzip(source, dest):
    import gzip
    import shutil

    with gzip.open(source, 'rb') as f_in, open(dest, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


class FileFormatWrapper:
    def __init__(self, target_file, format, read_mode=False):
        self.target_file = target_file
        self.format = format
        self.plain_file = target_file
        if self.using_temp_file():
            self.plain_file = target_file + "_temp"
        self.read_mode = read_mode

    def using_temp_file(self):
        return self.format != FileFormat.JSON

    def __compress__(self):
        if self.format == FileFormat.CompressedJSON:
            compress_gzip(self.plain_file, self.target_file)

    def __decompress__(self):
        if self.format == FileFormat.CompressedJSON:
            decompress_gzip(self.target_file, self.plain_file)

    def __enter__(self):
        if not self.using_temp_file():
            return self
        if self.read_mode:
            self.__decompress__()
        return self

    def __exit__(self, _, value, traceback):
        if not self.using_temp_file():
            return self

        try:
            if not self.read_mode:
                self.__compress__()
        finally:
            unlink(self.plain_file)
