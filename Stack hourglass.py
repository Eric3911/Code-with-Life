import math

import torch
import torch.nn as nn
import torch.nn.functional as F

norm_layer = (nn.BatchNorm1d, nn.BatchNorm2d, nn.GroupNorm, nn.InstanceNorm2d)
opt_layer = (nn.Conv2d, nn.Linear)


def dice_loss(preds, trues, weight=None, is_average=True, eps=1e-10):
    preds = preds.contiguous()
    trues = trues.contiguous()
    num = preds.size(0)
    preds = preds.view(num, -1)
    trues = trues.view(num, -1)
    if weight is not None:
        w = torch.autograd.Variable(weight).view(num, -1)
        preds = preds * w
        trues = trues * w
    intersection = (preds * trues).sum(1)
    scores = (2. * intersection + eps) / (preds.sum(1) + trues.sum(1) + eps)

    if is_average:
        score = scores.sum() / num
        return torch.clamp(score, 0., 1.)
    else:
        return scores


def conv3x3(in_planes, out_planes, strd=1, padding=1, bias=False):
    "3x3 convolution with padding"
    return nn.Conv2d(in_planes, out_planes, kernel_size=3,
                     stride=strd, padding=padding, bias=bias)


class ConvBlock(nn.Module):
    def __init__(self, in_planes, out_planes):
        super(ConvBlock, self).__init__()
        self.bn1 = nn.BatchNorm2d(in_planes)
        self.conv1 = conv3x3(in_planes, int(out_planes / 2))
        self.bn2 = nn.BatchNorm2d(int(out_planes / 2))
        self.conv2 = conv3x3(int(out_planes / 2), int(out_planes / 4))
        self.bn3 = nn.BatchNorm2d(int(out_planes / 4))
        self.conv3 = conv3x3(int(out_planes / 4), int(out_planes / 4))

        if in_planes != out_planes:
            self.downsample = nn.Sequential(
                nn.BatchNorm2d(in_planes),
                nn.ReLU(True),
                nn.Conv2d(in_planes, out_planes,
                          kernel_size=1, stride=1, bias=False),
            )
        else:
            self.downsample = None

    def forward(self, x):
        residual = x

        out1 = self.bn1(x)
        out1 = F.relu(out1, True)
        out1 = self.conv1(out1)

        out2 = self.bn2(out1)
        out2 = F.relu(out2, True)
        out2 = self.conv2(out2)

        out3 = self.bn3(out2)
        out3 = F.relu(out3, True)
        out3 = self.conv3(out3)

        out3 = torch.cat((out1, out2, out3), 1)

        if self.downsample is not None:
            residual = self.downsample(residual)

        out3 += residual

        return out3


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class PSPBlock(nn.Module):
    def __init__(self, features, sizes=(3, 5, 9), ):
        super().__init__()
        self.sizes, self.features = sizes, features
        self.conv = nn.Sequential(nn.Conv2d(len(sizes) * features, features, 1, 1, 0),
                                  nn.BatchNorm2d(features),
                                  nn.ReLU())

    def forward(self, x):
        f = x.size(1)
        fea = []
        for size in self.sizes:
            fea.append(F.avg_pool2d(x, size, 1, padding=size // 2))
        hhh = torch.cat(fea, dim=1)
        return self.conv(hhh)


class HourGlass(nn.Module):
    def __init__(self, num_modules, depth, num_features, sizes):
        super(HourGlass, self).__init__()
        self.sizes = sizes
        self.num_modules = num_modules
        self.depth = depth
        self.features = num_features

        self._generate_network(self.depth)
        self.ba = nn.Sequential(nn.BatchNorm2d(self.features), nn.ReLU())

    def _generate_network(self, level):
        self.add_module('b1_' + str(level), ConvBlock(self.features, self.features))

        self.add_module('b2_' + str(level), ConvBlock(self.features, self.features))

        if level > 1:
            self._generate_network(level - 1)
        else:
            self.add_module('b2_plus_' + str(level), ConvBlock(self.features, self.features))

        self.add_module('b3_' + str(level), ConvBlock(self.features, self.features))
        if isinstance(self.sizes, tuple):
            self.add_module('b_psp_' + str(level), PSPBlock(self.features, self.sizes))

    def _forward(self, level, inp):
        # Upper branch
        up1 = inp
        up1 = self._modules['b1_' + str(level)](up1)

        # Lower branch
        low1 = F.max_pool2d(inp, 2, stride=2)
        low1 = self._modules['b2_' + str(level)](low1)

        if level > 1:
            low2 = self._forward(level - 1, low1)
        else:
            low2 = low1
            low2 = self._modules['b2_plus_' + str(level)](low2)

        low3 = low2
        low3 = self._modules['b3_' + str(level)](low3)
        if isinstance(self.sizes, tuple):
            low3 = self._modules['b_psp_' + str(level)](low3)

        up2 = F.upsample_nearest(low3, scale_factor=2)

        return self.ba(up1 + up2)

    def forward(self, x):
        return self._forward(self.depth, x)


class FOX(nn.Module):
    def __init__(self, num_modules=1, base=64, depth=5, sizes=(3, 5), out_channels=2):
        super().__init__()
        self.num_modules = num_modules
        self.base = base

        # Base part
        # self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3)
        self.head = nn.Sequential(nn.BatchNorm2d(3),
                                  nn.Conv2d(3, base * 2, 3, 1, 1, bias=True),
                                  nn.Conv2d(base * 2, base * 4, 3, 1, 1, bias=False),
                                  nn.BatchNorm2d(base * 4),
                                  nn.ReLU())

        # Stacking part
        for hg_module in range(self.num_modules):
            self.add_module('m' + str(hg_module), HourGlass(1, depth, base * 4, sizes))
        self.conv_end = nn.Conv2d(base * 4, out_channels, 1, bias=True)

    def forward(self, x):
        x = self.head(x)
        previous = x
        for i in range(self.num_modules):
            previous = self._modules['m' + str(i)](previous)
        out = self.conv_end(previous)
        # out = F.log_softmax(out, dim=1)
        out = F.sigmoid(out)
        return out

    def init_param(self):
        for _layer in self.modules():
            if isinstance(_layer, opt_layer):
                nn.init.kaiming_normal_(_layer.weight, 2 ** 0.5)
            if isinstance(_layer, norm_layer):
                nn.init.constant_(_layer.weight, 1.0)
                nn.init.constant_(_layer.bias, 0.0)


class FOXStem(FOX):
    def __init__(self, num_modules=1, base=64, depth=5, sizes=(3, 5), out_channels=2):
        super().__init__(num_modules, base, depth, sizes, out_channels)
        self.head = nn.Sequential(nn.BatchNorm2d(3),
                                  nn.Conv2d(3, base, 3, 1, 1, bias=False),
                                  nn.BatchNorm2d(base),
                                  nn.ReLU(True),
                                  nn.Conv2d(base, base * 2, 3, 1, 1, bias=False),
                                  nn.BatchNorm2d(base * 2),
                                  nn.ReLU(True),
                                  nn.Conv2d(base * 2, base * 4, 3, 1, 1, bias=False),
                                  nn.BatchNorm2d(base * 4),
                                  nn.ReLU(True))


if __name__ == '__main__':
    model = FOXStem(1, 72, 5, (3, 5))
