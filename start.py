import sys
import json

from src.decide import decide

def start():
    list_of_augmented = json.load(sys.stdin)
    json.dump(decide(list_of_augmented).toJson(), sys.stdout, indent=4)
    sys.stdout.write('\n')

if __name__ == "__main__":
    start();
