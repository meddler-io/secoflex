
import yaml
import enum
import logging


class OutputSchemaTypes(enum.Enum):
    ARRAY = "array"
    OBJECT = "object"
    FILE = "file"
    URL = "url"
    EMBEDDED_PACKAGE = "embedded_package"


class ToolType(enum.Enum):
    Dockerfile = "dockerfile"
    Zip = "zip"
    Tar = "tar"
    Image = "image"
    Git = "git"


class BaseToolContext():
    def __init__(self, tool_type: ToolType):
        self.tool_type = tool_type


class DockerfileToolContext(BaseToolContext):
    def __init__(self, dockerfile="Dockerfile"):
        super().__init__(ToolType.Dockerfile)


class TarToolContext(BaseToolContext):
    def __init__(self, bundle="package.tar.gz"):
        super().__init__(ToolType.Tar)


class ZipToolContext(BaseToolContext):
    def __init__(self, bundle="package.zip"):
        super().__init__(ToolType.Zip)


class ImageToolContext(BaseToolContext):
    def __init__(self, image, repository, username=None, password=None):
        super().__init__(ToolType.Image)


class ToolYaml():

    def __init__(self, file_path="sample.yaml") -> None:
        self.__file_path = file_path
        self.version = '1'
        logging.info("Startin Tool Parser")
        self.Parse()
        pass

    def Parse(self):
        try:
            with open('sample.yaml') as f:
                self.__data = yaml.load(f, Loader=yaml.FullLoader)
        except:
            logging.error("Unknown / Invalid File")
            raise Exception("No such file exists")

        logging.info("Found data:")
        logging.info(self.__data)

        self.parseTool()

    def parseTool(self):
        tools = self.__data["tools"]

        # Parse Type
        type = tools["type"].lower()
        if type == ToolType.Dockerfile:
            self.type = ToolType.Dockerfile
        elif type == ToolType.Zip:
            self.type = ToolType.Zip
        elif type == ToolType.Tar:
            self.type = ToolType.Tar
        elif type == ToolType.Image:
            self.type = ToolType.Image

        # Parse tool context
        if type == ToolType.Dockerfile:
            self.tool_context = DockerfileToolContext(tools["build"])
        elif type == ToolType.Zip:
            self.tool_context = ZipToolContext(tools["build"])

        elif type == ToolType.Tar:
            self.tool_context = TarToolContext(tools["build"])

        elif type == ToolType.Image:
            self.tool_context = ImageToolContext(tools["image"],
                                                 tools["credentials"]["reposuseritory"],
                                                 tools["credentials"]["user"],
                                                 tools["credentials"]["password"],
                                                 )
        # Parse result schema
        logging.info("Parsing Output Schema")
        output = tools["output"]
        schema = output["schema"]

        for key, value in zip(schema.keys(), schema.values()):

            identifier = value.get("id", key)
            datatype = value.get("datatype", "string")
            default = value.get("default", "")
            primary = value.get("primary", False)
            unique = value.get("unique", False)
            optional = value.get("optional", True)
            indexed = value.get("indexed", False)
            alias = value.get("alias", key)
            meta = value.get("meta", {})

            print(identifier)
            print(datatype)
            print(default)
            print(primary)
            print(unique)
            print(optional)
            print(indexed)
            print(alias)
            print(meta)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ToolYaml()
