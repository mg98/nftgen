# NFTgen

NFTgen is a tool to automatically generate the asset files for a deterministic NFT collection that is based on combination of layers of images.
It focuses on execution efficiency by taking advantage of multi-core processors of a system.
Ultimately, this allows users to generate 10,000s of assets within minutes, instead of hours or sometimes days, by 

**Current State:** Usable, but very basic. Under development. Contributions are welcome.

## Usage

The tool expects a directory path as an input. The directory should only contain folders. Each folder equates a layer in the final NFT image. The name is irrelevant, but the (alphabetical) order will translate to the order of layers (z-axis) in the NFT. Finally, those folders should contain alternate images (as PNG files) for that layer.

**Example:**
```
assets
├── background
│   ├── background_bronze.png
│   ├── background_gold.png
│   ├── background_platinum.png
│   └── background_silver.png
└── monkey
    ├── color_black-and-white.png
    ├── color_brown-and-white.png
    ├── color_grey-and-white.png
    └── color_white.png
```

### Run

Running the program will generate all possible combinations of the alternate images in each layer as PNG files in a folder `./results`.
It is required to provide the path to your prepared folder, containing the raw assets.
The program will use all CPU cores and a default of 2 threads per core. However, there is a parameter for you to tune the threads to potentially achieve even better performance.

**Example:**
```
python3 main.py /path/to/assets
```

**Reference:**
```
usage: main.py [-h] [--threads THREADS] assets_path

positional arguments:
  assets_path        Disk path to asset files.

optional arguments:
  -h, --help         show this help message and exit
  --threads THREADS  Amount of concurrent threads to run.
```

The project also ships with a [Dockerfile](./Dockerfile).