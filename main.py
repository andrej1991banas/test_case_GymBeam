from data_extractor import GolemioExtractorId
from extractor_ai import GolemioExtractor

# Use extractor libraries
if __name__ == "__main__":
    extractor = GolemioExtractor('config.json')
    extractor.run()


# Use extractor one Library with provided ID
if __name__ == "__main__":
    extractor = GolemioExtractorId('config_library_id.json')
    extractor.run()

