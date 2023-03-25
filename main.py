#!/usr/bin/python3

from rocket import *

def default_params() -> RocketParamsType:
    params = RocketParams(M_const = 9500, v_start = 1000)

    stage0 = RocketStage(G = 290000, uG = 320, M_fuel = 25000, M_const = 2500)
    stage1 = RocketStage(G = 800000, uG = 270, M_fuel = 100000, M_const = 5000)
    stage2 = RocketStage(G = 4000000, uG = 250, M_fuel = 170000, M_const = 7000)

    params.stages.append(stage0)
    params.stages.append(stage1)
    params.stages.append(stage2)
    return params


def main():

    r = Rocket(default_params())
    r.calc(0.1,10)


if __name__ == "__main__":
    main()



