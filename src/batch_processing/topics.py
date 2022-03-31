import xml.etree.ElementTree as ET

import constants
from batch_processing.topic import Topic


class Topics:
    topic_list: list[Topic] = []

    def __init__(self, title_file_path: str = constants.TEST_TITLES_FILE_LOCATION):
        self._parse_topics_xml(title_file_path)

    def _parse_topics_xml(self, title_file_path: str) -> None:
        tree = ET.parse(title_file_path)
        root_element = tree.getroot()

        # Iterate topics
        for topic_element in root_element.findall("topic"):
            topic = Topic()
            topic.number = int(topic_element.find("number").text)
            topic.title = topic_element.find("title").text
            # Touché 2021 topics do not have objects
            if topic_element.find("objects"):
                topic.objects = topic_element.find("objects").text
            topic.description = topic_element.find("description").text
            topic.narrative = topic_element.find("narrative").text
            self.topic_list.append(topic)

    def __iter__(self):
        return iter(self.topic_list)


if __name__ == '__main__':
    topics = Topics()
    print(topics.topic_list)
