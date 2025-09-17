import time
import os, random, pickle
import numpy as np 
import matplotlib.pyplot as plt
import torch 
import torch.nn.functional as F


def to_cuda(value,rank):
    if torch.cuda.is_available():
        return value.to(rank)
    elif torch.backends.mps.is_available():
        if value.dtype == torch.float64:
            return value.to(torch.device("mps"), dtype=torch.float32)
        else:
            return value.to(torch.device("mps"))
    else:
        if value.dtype == torch.float64:
            return value.cpu().to(torch.float32)
        else:
            return value.cpu()
def batch_to_cuda(batch, rank):
    for k in batch:
        if type( batch[k] ) is torch.Tensor:
            
            batch[k] = to_cuda(batch[k],rank)
        elif type( batch[k] ) is dict:
            for kk in batch[k]:
                batch[k][kk] = to_cuda(batch[k][kk],rank)

        
    return batch 

def detach_cuda(batch):
    for k in batch:
        if type( batch[k] ) is torch.Tensor:
            batch[k] = batch[k].detach()
    return batch 

def to_cpu(batch):
    for k in batch:
        if type( batch[k] ) is torch.Tensor:
            batch[k] = batch[k].cpu()
    return batch

def dict_to_cuda(dictData, rank):
    for k in dictData:
        if type(dictData[k]) is torch.Tensor:
            dictData[k] = dictData[k].cuda(rank)
    return dictData


def sample_to_batch(data):
    batch = {}
    for i in data:
        if type(data[i]) is torch.Tensor:
            batch[i] = torch.stack([data[i]], 0)
        else:
            batch[i] = [data[i]]
    return batch


#mode: 'constant', 'reflect', 'replicate' or 'circular'
def pad_temporal_data(data, length, mode='constant', padValue=0):
    #data: torch, shape Tx...
    if len(data.shape) > 1:
        data = data.transpose(0, -1)

    if data.shape[-1] < length:
        dL = length - data.shape[-1]
        data = F.pad(data, (0, dL), mode, padValue)

    if len(data.shape) > 1:
        data = data.transpose(-1, 0)
    return data[:length]


def rescale_temporal_data(data, length, mode='linear'):
    #data: torch, shape Tx...
    shape = data.shape
    if len(shape) > 1:
        data = data.transpose(0, -1)
    else:
        data = data.unsqueeze(0)

    if data.shape[-1] != length:
        #interpolate only support input of (B, C, .., T)
        data = F.interpolate(data.unsqueeze(0), length, mode=mode).squeeze(0)
    
    if len(shape) > 1:
        data = data.transpose(-1, 0)
    else:
        data = data.squeeze(0)
    return data


def get_temporal_numpy_data(file, length=None, rescale=True, scale=None):
    # Tx...
    if not os.path.isfile(file):
        return None

    data = np.load(file)
    data = torch.from_numpy(data)

    if length is None and scale is None:
        return data
    if length is None:
        length = int(data.shape[0] * scale)
    
    if rescale is True:
        return rescale_temporal_data(data, length)
    else:
        return pad_temporal_data(data, length)


def get_temporal_torch_data(file, length=None, rescale=True, scale=None):
	# Tx...
    if not os.path.isfile(file):
        return None

    data = torch.load(file, weights_only=False)

    if length is None and scale is None:
        return data
    if length is None:
        length = int(data.shape[0] * scale)
    
    if rescale is True:
        return rescale_temporal_data(data, length)
    else:
        return pad_temporal_data(data, length)


def get_random_crop_range(length, crop_range):
    if length <= crop_range[0]:
        return 0, length
    L = random.randint(crop_range[0], crop_range[1] if crop_range[1] is not None else length)
    L = length if L > length else L
    start = random.randint(0, length-L)
    end = start+L
    return start, end

def visualize_grid(images, row_names, col_names):
    '''
    此函数功能为将多张图片拼接成一张大图
    images: 二维数组，有横向与纵向
    row_names: 横向的文字标签
    col_names: 纵向的文字标签
    返回为matplotlib的figure对象
    '''
    assert len(images) == len(row_names)
    assert all(len(row) == len(col_names) for row in images)

    h, w, c = images[0][0].shape
    grid_rows = len(images)
    grid_cols = len(images[0])

    # 创建一张大图拼接所有图像
    grid_img = np.ones((h * grid_rows, w * grid_cols, 3), dtype=np.uint8) * 255

    for i in range(grid_rows):
        for j in range(grid_cols):
            y_start = i * h
            y_end = y_start + h
            x_start = j * w
            x_end = x_start + w
            grid_img[y_start:y_end, x_start:x_end] = images[i][j]

    # 使用 matplotlib 绘制图像和文字标签
    fig, ax = plt.subplots()
    ax.imshow(grid_img)
    ax.axis('off')

    for j, name in enumerate(col_names):
        x = j * w + w // 2
        ax.text(x, -10, name, ha='center', va='bottom', fontsize=12)

    for i, name in enumerate(row_names):
        y = i * h + h // 2
        ax.text(-10, y, name, ha='right', va='center', fontsize=12)

    plt.tight_layout()

    
    fig.canvas.draw()
    
    
    return fig