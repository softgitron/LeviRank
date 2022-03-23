import xml.etree.ElementTree as ET

import constants
from processing.topic import Topic


class Topics:
    topic_list: list[type[Topic] | None] = []

    def __init__(self, title_file_path: str = constants.TEST_TITLES_FILE_LOCATION):
        self.parse_topics_xml(title_file_path)

    def parse_topics_xml(self, title_file_path: str) -> None:
        tree = ET.parse(title_file_path)
        root_element = tree.getroot()

        # Iterate topics
        for topic_element in root_element.findall("topic"):
            topic = Topic()
            topic.number = int(topic_element.find("number").text)
            topic.title = topic_element.find("title").text
            self.topic_list.append(topic)


if __name__ == '__main__':
    topics = Topics()
    print(topics.topic_list)
