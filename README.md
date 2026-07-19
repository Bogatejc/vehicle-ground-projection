# Vehicle Ground Projection and Heading Estimation

## Overview

This project estimates vehicle heading from GNSS measurements and projects the antenna position onto the moving plane, then visualizes the result as static plots and an animated GIF. The workflow is implemented in Python with separate modules for geometry, heading estimation, visualization, and animation.

## Input data

The input dataset should contain the following columns:

| Field       | Description         | Unit |
| ----------- | ------------------- | ---- |
| `time_s`    | Timestamp           | s    |
| `x_mm`      | GNSS X coordinate   | mm   |
| `y_mm`      | GNSS Y coordinate   | mm   |
| `roll_deg`  | Vehicle roll angle  | °    |
| `pitch_deg` | Vehicle pitch angle | °    |

The antenna height is fixed at 1500 mm, and the angle conventions are:

- Positive roll means the right side of the vehicle is lower.
- Positive pitch means the front of the vehicle is lower.

## How to run

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the workflow with the default input file:

```bash
python main.py
```

Optional arguments:

```bash
python main.py path/to/input.csv
python main.py --plots
python main.py --gif
python main.py --output my_results/solution.csv
python main.py path/to/input.csv --plots --gif --output my_results/solution.csv
```

By default, the processed CSV is written to `output/solution.csv`, and the GIF is written to `vehicle_motion.gif` when `--gif` is used.

## Solution summary

The workflow follows a compact geometry-based pipeline:

1. Data loading and preparation: the input CSV is read with pandas, and the attitude angles are converted from degrees to radians so they can be used directly in NumPy trigonometric calculations.
2. Heading estimation: because the vehicle is assumed to move smoothly forward, the heading at each point is estimated from the direction of the previous and next GNSS positions. This is computed with `atan2`, which produces the correct angle in all quadrants.
3. Ground projection: the antenna is mounted 1500 mm above the moving plane. Its projection onto that plane depends on both pitch and roll. The forward and lateral offsets are first computed in the vehicle frame and then rotated into the global XY frame using the estimated heading.
4. Result generation: the computed heading and projected coordinates are appended to the data frame as `heading_deg`, `ground_x_mm`, and `ground_y_mm`.
5. Visualization: the processed data can be exported as a CSV, displayed with static plots, or rendered as an animated GIF that shows the vehicle motion, heading, and attitude over time.

In short, the code transforms noisy GNSS motion into a physically meaningful estimate of the vehicle orientation and the trajectory of the antenna projection on the ground plane.

## Output

The generated solution file is written to the chosen output path, and the animation is saved as `vehicle_motion.gif` when requested.

![Vehicle Motion](vehicle_motion.gif)
