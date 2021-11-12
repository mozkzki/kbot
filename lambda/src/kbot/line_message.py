from typing import List, Dict, Union
from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    URITemplateAction,
    PostbackTemplateAction,
)


class LineMessage:
    @staticmethod
    def make_text_message(text: str) -> TextSendMessage:
        message = text[:1900]
        if len(text) > 1900:
            message += "....."
        return TextSendMessage(text=message)

    @staticmethod
    def _make_template_actions(
        actions_data: List[Dict],
    ) -> List[Union[URITemplateAction, PostbackTemplateAction]]:
        template_actions = []
        for action in actions_data:
            label = action.get("label", "")
            data = action.get("data", "")
            display_text = action.get("display_text", "")
            url = action.get("url", "")
            if action.get("type", "url") == "url":
                template_action = URITemplateAction(label=label, uri=url)
            else:
                template_action = PostbackTemplateAction(
                    label=label, data=data, display_text=display_text
                )
            template_actions.append(template_action)
        return template_actions

    @staticmethod
    def make_button_message(message_data: Dict):
        actions = LineMessage._make_template_actions(message_data.get("actions", []))

        buttons_template = ButtonsTemplate(
            title=message_data.get("title", ""),
            text=message_data.get("text", ""),
            # thumbnail_image_url=message_data.get("image_url", ""),
            actions=actions,
            image_aspect_ratio="square",  # default = rectangle
            image_size="contain",  # default = cover
            image_background_color="#000000",  # default = #FFFFFF
        )
        return TemplateSendMessage(alt_text="button_message", template=buttons_template)

    @staticmethod
    def make_carousel_message(message_data_list: List[Dict]) -> TemplateSendMessage:
        columns = []
        for message_data in message_data_list:
            actions = LineMessage._make_template_actions(message_data.get("actions", []))

            column = CarouselColumn(
                title=message_data.get("title", "")[:40],
                text=message_data.get("text", "")[:60],
                thumbnail_image_url=message_data.get("image_url", ""),
                actions=actions,
            )
            columns.append(column)
            if len(columns) == 10:
                break

        return TemplateSendMessage(
            alt_text="carousel_message", template=CarouselTemplate(columns=columns)
        )
