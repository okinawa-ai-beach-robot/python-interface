from .. import logger
try:
    from jetson_utils import videoOutput
    from jetson_utils import cudaFromNumpy
except ModuleNotFoundError as ex:
    logger.warning(
        "Jetson utils not installed or not available! ImageViewerJetson not available!"
    )


class ImageViewerJetson:
    def __init__(self, title=None) -> None:
        self.display = videoOutput("display://0")
        print(
            "TODO I get a invalid OpenGL context, but when I type it in commands in the console direclty as a test it works!"
        )

    def show(self, img):
        print(img.dtype)

        cuda_mem = cudaFromNumpy(img)
        print(
            "img",
            cuda_mem.height,
            "img",
            cuda_mem.width,
            "img",
            cuda_mem.channels,
            "format",
            cuda_mem.format,
        )
        self.display.Render(cuda_mem)

    def close(self):
        self.display.Close()

    @staticmethod
    def close_all():
        pass
