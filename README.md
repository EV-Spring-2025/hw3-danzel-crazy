[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/SdXSjEmH)
# EV-HW3: PhysGaussian

This homework is based on the recent CVPR 2024 paper [PhysGaussian](https://github.com/XPandora/PhysGaussian/tree/main), which introduces a novel framework that integrates physical constraints into 3D Gaussian representations for modeling generative dynamics.

You are **not required** to implement training from scratch. Instead, your task is to set up the environment as specified in the official repository and run the simulation scripts to observe and analyze the results.


## Getting the Code from the Official PhysGaussian GitHub Repository
Download the official codebase using the following command:
```
git clone https://github.com/XPandora/PhysGaussian.git
```


## Environment Setup
Navigate to the "PhysGaussian" directory and follow the instructions under the "Python Environment" section in the official README to set up the environment.


## Running the Simulation
Follow the "Quick Start" section and execute the simulation scripts as instructed. Make sure to verify your outputs and understand the role of physics constraints in the generated dynamics.


## Homework Instructions
Please complete Part 1–2 as described in the [Google Slides](https://docs.google.com/presentation/d/13JcQC12pI8Wb9ZuaVV400HVZr9eUeZvf7gB7Le8FRV4/edit?usp=sharing).

## How to implement
1. Change the config in ficus_config.json or ficus_config_jelly.json where the material is set to plasticine and jelly
2. For softening, change the value in mpm_solver_wrap.py 
3. run code to generate frame and video 
    ```
    CUDA_VISIBLE_DEVICES=1 python gs_simulation.py --model_path ./model/ficus_whitebg-trained/ --output_path output/plasticine/softening_1.0 --config ./config/ficus_config.json --render_img --compile_video --white_bg
    ```
4. use `cal_psnr.py` to calculate psnr and store in json file
## Discovery

### Base Setting of four parameters
- n_grid : 50
- substeps: 1e-4
- grid_v_damping_scale : 0.9999
- softening : 0.1

### Baseline video
- [Jelly baseline video](https://youtube.com/shorts/_UU24Kv53aQ)
- [plasticine baseline video](https://youtube.com/shorts/kXJdMmwUjfw?feature=share)

### Other video links
- [videos link](https://drive.google.com/drive/folders/1EEbIpLfggi9frNNdRKWPe5oHy-gc-8lg?usp=sharing)

### N_grid

| Material    | n_grid = 40 | n_grid = 50 (base) | n_grid = 60 |
|-------------|:-----------:|:------------------:|:-----------:|
| Plasticine  |   23.7062   |        Baseline     |   21.4192   |
---

- I do experiment on plasticine with n_grid = 40, 50(base), 60
- if n_grid set lower, the movement of the plant in the flowerpot becomes much less noticeable. For example, if you observe the leaf on the far right, there is almost no natural swaying when n_grid = 40. 
- Surprisingly, increasing the resolution does not necessarily lead to higher PSNR. The reason behind lower psnr may due to numerical instabilities or noise introduced at higher resolution. More sensitive dynamics causing slight deviations from ground truth reference, reducing the pixel-wise similarity (PSNR).

### substeps

| Material    | substeps = 1e-3 | substeps = 1e-4(base) | substeps = 1e-5 |
|-------------|:-----------:|:------------------:|:-----------:|
| Plasticine  |   76.2869   |    Baseline         |   76.2936   |
| Jelly       |   76.1947   |    Baseline         |   76.5433   |
---

- I do experiment on plasticine with substeps = 1e-3, 1e-4(base), 1e-5
- jelly with substeps = 1e-3, 1e-4(base), 1e-5
- I can barely see the diffrence on the value change of parameter 
- Changing the `substeps` parameter (i.e., time step size) shows **minimal impact on PSNR** for both Plasticine and Jelly. This suggests that the simulation is already temporally stable at the base value of `1e-4`.


### grid_v_damping_scale

| Material    | grid_v = 0.7 | grid_v = 0.9999 (base) | grid_v = 1.0  |
|-------------|:-----------:|:------------------:|:-----------:|
| Plasticine  |   21.8358   |    Baseline         |   18.7182   |
| Jelly       |   21.8366  |    Baseline         |   19.9982    |
---
- I do experiment on jelly with grid_v_damping_scale = 1.0, 0.9999, 0.7
- plasticine with grid_v_damping_scale = 1.0, 0.9999, 0.7
- Increasing grid_v_damping_scale too close to 1.0 leads to overdamping of grid velocities, which suppresses natural motion and results in lower PSNR. Conversely, reducing it to 0.7 allows more motion but may introduce slight instability or noise.

### softenings
| Material    | softening = 0.1(base) | softening = 0.5  | softening = 1.0  |
|-------------|:-----------:|:------------------:|:-----------:|
| Plasticine  |   19.9981   |    Baseline         |   20.1722   |
| Jelly       |   41.7469  |    Baseline         |   76.3451    |

- I do expriment on plasticine with softening = 0.1(baseline), 0.5, 1.0 and jelly with softening = 0.1(baseline), 0.5, 1.0
- Changing the softening parameter results in noticeable PSNR changes numerically, especially for Jelly, but visual differences are minimal. This suggests that softening affects the underlying numerical stability or contact smoothness, but does not significantly alter the visible motion in the simulation videos or maybe some setting is accidently cahnge yb me but I forget, I am not very confidence with the results though.


# Reference
```bibtex
@inproceedings{xie2024physgaussian,
    title     = {Physgaussian: Physics-integrated 3d gaussians for generative dynamics},
    author    = {Xie, Tianyi and Zong, Zeshun and Qiu, Yuxing and Li, Xuan and Feng, Yutao and Yang, Yin and Jiang, Chenfanfu},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    year      = {2024}
}
```
