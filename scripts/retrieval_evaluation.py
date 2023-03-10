import sys
sys.path.append("../")
import torch.multiprocessing
torch.multiprocessing.set_sharing_strategy('file_system')
import argparse
import logging
from embedders.factory import EmbedderFactory
from evaluation.retrieval.retrieval import ImageRetrieval
import pandas as pd
from dotenv import load_dotenv
import os
from utils.results_handler import ResultsHandler
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def config():
    load_dotenv("../config.env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", default="plip", type=str)
    parser.add_argument("--caption_column", default="caption", type=str)
    parser.add_argument("--backbone", default='default', type=str)
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--seed", default=1, type=int)

    ## Probe hparams
    parser.add_argument("--alpha", default=0.01, type=float)
    return parser.parse_args()


if __name__ == "__main__":

    args = config()
    data_folder = os.environ["PC_EVALUATION_DATA_ROOT_FOLDER"]

    if args.model_name == "plip" and args.backbone == "default":
        args.backbone = os.environ["PC_DEFAULT_BACKBONE"]

    test_dataset_name = args.dataset + "_test.csv"

    test_dataset = pd.read_csv(os.path.join(data_folder, test_dataset_name))

    embedder = EmbedderFactory().factory(args.model_name, args.backbone)

    image_embeddings = embedder.image_embedder(test_dataset["image"].tolist(),
                                     additional_cache_name=test_dataset_name)

    # embeddings are generated using the selected caption, not the labels
    text_embeddings = embedder.text_embedder(test_dataset[args.caption_column].tolist(),
                                    additional_cache_name=test_dataset_name)

    prober = ImageRetrieval()

    results = prober.retrieval(image_embeddings, text_embeddings)

    additional_parameters = {'dataset': args.dataset, 'seed': args.seed,
                             'model': args.model_name, 'backbone': args.backbone}

    rs = ResultsHandler(args.dataset, "retrieval", additional_parameters)
    rs.add(results)

