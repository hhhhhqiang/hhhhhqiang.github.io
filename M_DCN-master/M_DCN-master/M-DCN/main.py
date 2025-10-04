import argparse

import numpy as np
import torch

from load_data import Data
from train_eval import RunModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default="MDCN", help='MDCN')
    parser.add_argument('--dataset', type=str, default="FB15k",
                        help='FB15k, FB15k-237, WN18, WN18RR, YAGO3-10')
    parser.add_argument('--cuda', type=bool, default=False, help='use cuda or not')
    parser.add_argument('--get_best_results', type=bool, default=True, help='get best results or not')
    parser.add_argument('--get_complex_results', type=bool, default=False, help='get complex results or not')
    parser.add_argument('--num_to_eval', type=int, default=5, help='number to evaluate')

    # learning parameters
    parser.add_argument('--learning_rate', type=float, default=1e-2, help='learning rate')
    parser.add_argument('--batch_size', type=int, default=128, help='batch size')
    parser.add_argument('--num_iterations', type=int, default=1500, help='iterations number')
    parser.add_argument('--optimizer_method', type=str, default="Adam", help='optimizer method')
    parser.add_argument('--decay_rate', type=float, default=1.0, help='decay rate')
    parser.add_argument('--label_smoothing', type=float, default=0., help='label smoothing')

    # convolution parameters
    parser.add_argument('--ent_vec_dim', type=int, default=200, help='entity vector dimension')
    parser.add_argument('--rel_vec_dim', type=int, default=200, help='relation vector dimension')
    parser.add_argument('--input_dropout', type=float, default=0.1, help='input dropout')
    parser.add_argument('--feature_map_dropout', type=float, default=0.4, help='feature map dropout')
    parser.add_argument('--hidden_dropout', type=float, default=0.5, help='hidden dropout')
    parser.add_argument('--filt_h', type=int, default=3, help='filter height')
    parser.add_argument('--filt_w', type=int, default=3, help='filter width')
    parser.add_argument('--in_channels', type=int, default=1, help='in channels')
    parser.add_argument('--out_channels', type=int, default=32, help='out channels')

    args = parser.parse_args()
    dataset = args.dataset
    data_dir = "data/%s/" % dataset
    print(args)

    seed = 777
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

    data = Data(data_dir=data_dir, reverse=True)
    run = RunModel(data, modelname=args.model_name, optimizer_method=args.optimizer_method,
                   num_iterations=args.num_iterations, batch_size=args.batch_size, learning_rate=args.learning_rate,
                   decay_rate=args.decay_rate, ent_vec_dim=args.ent_vec_dim, rel_vec_dim=args.rel_vec_dim,
                   cuda=args.cuda, input_dropout=args.input_dropout, hidden_dropout=args.hidden_dropout,
                   feature_map_dropout=args.feature_map_dropout, in_channels=args.in_channels,
                   out_channels=args.out_channels, filt_h=args.filt_h, filt_w=args.filt_w,
                   label_smoothing=args.label_smoothing, num_to_eval=args.num_to_eval,
                   get_best_results=args.get_best_results, get_complex_results=args.get_complex_results)
    run.train_and_eval()


if __name__ == '__main__':
    main()
