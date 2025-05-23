import sys
import config

from utils import main_loop

def main():
    config.load_config(sys.argv[1])
    main_loop()

if __name__ == '__main__':
    main()