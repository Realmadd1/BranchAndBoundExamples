from p293_299.BranchAndBound import BrandAndBound
from p293_299.PPModel import PPModel


def main():
    ppModel = PPModel()
    planner = BrandAndBound(ppModel)
    planner.run()


if __name__ == '__main__':
    main()
    print()
