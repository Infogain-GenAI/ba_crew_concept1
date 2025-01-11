from crewai_tools import PDFSearchTool

class pdf_source:
    def __init__(self, paramfilePath):
        self.paramfilePath = paramfilePath

obj = pdf_source(paramfilePath='value1')

tool = PDFSearchTool(pdf=obj.paramfilePath)