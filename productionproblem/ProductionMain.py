from productionproblem.BranchAndBound import BrandAndBound
from productionproblem.PPModel import PPModel


def main():
    ppModel = PPModel()
    planner = BrandAndBound(ppModel)
    planner.run()


if __name__ == '__main__':
    main()
