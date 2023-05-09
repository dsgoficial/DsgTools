from DsgTools.Modules.utils.message.htmlMessageDialog import HtmlMessageDialog
from DsgTools.Modules.utils.message.infoMessageBox import InfoMessageBox
from DsgTools.Modules.utils.message.errorMessageBox import ErrorMessageBox
from DsgTools.Modules.utils.message.questionMessageBox import QuestionMessageBox


class MessageFactory:
    def createMessage(self, messageType):
        messageTypes = {
            "HtmlMessageDialog": HtmlMessageDialog,
            "InfoMessageBox": InfoMessageBox,
            "ErrorMessageBox": ErrorMessageBox,
            "QuestionMessageBox": QuestionMessageBox,
        }
        return messageTypes[messageType]()
