import os
from PIL import Image
import itertools
import logging
import multiprocessing as mp
from functools import reduce
from threading import Thread
import argparse
from os import listdir
from os.path import isfile, join, isdir

parser = argparse.ArgumentParser()
parser.add_argument('assets_path', help='Disk path to asset files.')
parser.add_argument('--threads', help='Amount of concurrent threads to run.')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)

# TypeDef: Ordered list of layers to make an NFT asset (index 0 = background).
AssetRecipe = list[Image.Image]

CONCURRENT_THREADS = int(args.threads) if args.threads else 2

def get_assets():
	assets = []
	asset_dirs = [d for d in listdir(args.assets_path) if isdir(join(args.assets_path, d)) and d[0] != '.']
	for asset_dir in asset_dirs:
		asset_files = [join(asset_dir, f) for f in listdir(join(args.assets_path, asset_dir)) if isfile(join(args.assets_path, asset_dir, f))]
		assets.append(asset_files)
	return assets

def prepare_file(filename: str) -> Image.Image:
	return Image.open(join(args.assets_path, filename)).convert('RGBA')

def array_split(a: list, n: int) -> list:
    k, m = divmod(len(a), n)
    return list(a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def generate_assets(asset_recipes: list[AssetRecipe], counter: int):
	logging.debug(f'Starting at #{counter}.')
	for recipe in asset_recipes:
		for f in recipe[1:]:
			recipe[0].paste(f, (0,0), f)
		counter += 1
		recipe[0].save(f'./results/{counter}.png', format='png')
		logging.debug(f'Saved #{counter}.')

def run_process(asset_recipes: list[AssetRecipe], counter: int):
	chunks: list[list[AssetRecipe]] = array_split(asset_recipes, CONCURRENT_THREADS)

	get_counter_val = lambda i: reduce(lambda acc, chunk: acc + len(chunk), chunks[:i], counter)

	threads = [Thread(target=generate_assets, args=(chunk, get_counter_val(i))) for (i, chunk) in enumerate(chunks)]
	for t in threads: t.start()
	for t in threads: t.join()

if __name__ == '__main__':
	try:
		for f in listdir('./results'): os.remove(f'./results/{f}')
	except Exception as e:
		os.mkdir('./results')

	layers: list[list[Image.Image]] = list(map(lambda files: list(map(prepare_file, files)), get_assets()))
	
	try:
		all_asset_recipes: list[AssetRecipe] = list(itertools.product(*layers))

		logging.info(f'Total: {len(all_asset_recipes)}')

		counter = 0
		chunks: list[list[AssetRecipe]] = array_split(all_asset_recipes, mp.cpu_count())

		get_counter_val = lambda i: reduce(lambda acc, chunk: acc + len(chunk), chunks[:i], 0)

		processes = [mp.Process(target=run_process, args=(chunk, get_counter_val(i)), name=str(i)) for (i, chunk) in enumerate(chunks)]
		for p in processes: p.start()
		for p in processes: p.join()

		logging.info('Done.')
	finally:
		for images in layers:
			for img in images:
				img.close()
