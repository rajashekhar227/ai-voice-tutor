class LessonService:

    def create_lesson(self, chunks):

        lesson = " ".join(chunks)

        return lesson

    def create_topic_lesson(self, topic, chunks):

        content = " ".join(chunks)

        lesson = {
            "topic": topic,
            "content": content
        }

        return lesson