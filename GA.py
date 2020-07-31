from Population import Generation
from FileHandler import FileHandler


def main():
    # instantiate global items
    gFH = FileHandler()

    # load settings file
    settings_array = gFH.readFileToArray("setting")
    GENERATION_COUNT = int(settings_array[0])

    # Load Generations
    GENERATION_DICT = {

    }

    for gen in range(GENERATION_COUNT):
        GENERATION_DICT[("GEN" + str(gen))] = Generation(50)


if __name__ == "__main__":
    main()