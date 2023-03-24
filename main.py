#!/usr/bin/python3

from rocket import *

def default_params() -> RocketParamsType:
    params = RocketParams(M_const = 1)

    stage0 = RocketStage(G = 1, uG = 2, M_fuel = 2, M_const = 1)

    params.stages.append(stage0)


def main():

    r = Rocket(default_params())
    r.curr_stage(0)


if __name__ == "__main__":
    main()



