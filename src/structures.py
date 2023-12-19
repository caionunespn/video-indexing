class Video:
    def __init__(self, id, name, fps, dimensions, duration, language, keywords, thumbnail):
        self.id = id
        self.name = name
        self.fps = fps
        self.dimensions = dimensions
        self.duration = duration
        self.language = language
        self.keywords = keywords
        self.thumbnail = thumbnail

    def display_info(self):
        print()
        print(f"ID: {self.id}")
        print(f"Nome: {self.name}")
        print(f"FPS: {self.fps}")
        print(f"Dimensões: {self.dimensions[0]}x{self.dimensions[1]}")
        print(f"Duração: {self.duration} segundos")
        print(f"Idioma: {self.language}")
        print(f"Thumbnail: {self.thumbnail}")

    def search_by_keyword(self, search_term):
        terms = search_term.lower().split()
        result = False
        
        for word in terms:
            for keyword in self.keywords:
                if word in keyword:
                    result = True
                    break

        return result
