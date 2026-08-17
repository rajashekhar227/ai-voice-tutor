class LessonService:
    def create_lesson(self, chunks):
        lesson = " ".join(chunks)
        return lesson