class TopicService:

    def create_topic_lesson(self, topic, chunks, indices):

        relevant_chunks = []

        for index in indices:
            if index < len(chunks):
                relevant_chunks.append(chunks[index])

        lesson = " ".join(relevant_chunks)

        return lesson