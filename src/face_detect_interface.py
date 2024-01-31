# -*- coding: utf-8 -*-
from __future__ import print_function
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from src.FaceBoxesPyTorch.data import cfg
from src.FaceBoxesPyTorch.layers.functions.prior_box import PriorBox
from src.FaceBoxesPyTorch.utils.nms_wrapper import nms
import cv2
from src.FaceBoxesPyTorch.models.faceboxes import FaceBoxes
from src.FaceBoxesPyTorch.utils.box_utils import decode
from src.FaceBoxesPyTorch.utils.timer import Timer


class FaceDetector(object):
    def __init__(self, weight_path):
        self._resize = 1  # 1 / 2.5 / 3
        self._confidence_threshold = 0.05
        self._top_k = 100
        self._nms_threshold = 0.3
        self._keep_top_k = 750

        torch.set_grad_enabled(False)
        net = FaceBoxes(phase='test', size=None, num_classes=2)  # initialize detector
        net = self._load_model(net, weight_path)
        net.eval()
        print('Finished loading model!')
        print(net)
        cudnn.benchmark = True
        self._device = torch.device("cpu")
        self._net = net.to(self._device)
        self._t = {'forward_pass': Timer(), 'misc': Timer()}

    def inference(self, frame, thresh=0.7):
        assert isinstance(frame, np.ndarray)
        img_raw = frame.copy()
        img = np.float32(img_raw)
        # img = cv2.resize(img, None, None, fx=self._resize, fy=self._resize, interpolation=cv2.INTER_LINEAR)
        im_height, im_width, _ = img.shape
        scale = torch.Tensor([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])
        img -= (104, 117, 123)
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).unsqueeze(0)
        img = img.to(self._device)
        scale = scale.to(self._device)

        self._t['forward_pass'].tic()
        loc, conf = self._net(img)  # forward pass
        self._t['forward_pass'].toc()
        self._t['misc'].tic()

        priorbox = PriorBox(cfg, image_size=(im_height, im_width))
        priors = priorbox.forward()
        priors = priors.to(self._device)
        prior_data = priors.data
        boxes = decode(loc.data.squeeze(0), prior_data, cfg['variance'])
        boxes = boxes * scale / self._resize
        boxes = boxes.cpu().numpy()
        scores = conf.squeeze(0).data.cpu().numpy()[:, 1]

        # ignore low scores
        inds = np.where(scores > self._confidence_threshold)[0]
        boxes = boxes[inds]
        scores = scores[inds]

        # keep top-K before NMS
        order = scores.argsort()[::-1][:self._top_k]
        boxes = boxes[order]
        scores = scores[order]

        # do NMS
        dets = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
        keep = nms(dets, self._nms_threshold, force_cpu=True)
        dets = dets[keep, :]

        # keep top-K faster NMS
        dets = dets[:self._keep_top_k, :]
        self._t['misc'].toc()
        res = []
        for b in dets:
            if b[4] < thresh:
                continue
            text = "{:.4f}".format(b[4])
            b = list(map(int, b))
            cv2.rectangle(img_raw, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
            cx = b[0]
            cy = b[1] + 12
            cv2.putText(img_raw, text, (cx, cy),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
            res.append(b[:4])
        return res, img_raw

    def _load_model(self, model, pretrained_path):
        print('Loading pretrained model from {}'.format(pretrained_path))
        pretrained_dict = torch.load(pretrained_path, map_location=lambda storage, loc: storage)
        if "state_dict" in pretrained_dict.keys():
            pretrained_dict = self._remove_prefix(pretrained_dict['state_dict'], 'module.')
        else:
            pretrained_dict = self._remove_prefix(pretrained_dict, 'module.')
        self._check_keys(model, pretrained_dict)
        model.load_state_dict(pretrained_dict, strict=False)
        return model

    def _remove_prefix(self, state_dict, prefix):
        ''' Old style model is stored with all names of parameters sharing common prefix 'module.' '''
        print('remove prefix \'{}\''.format(prefix))
        f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
        return {f(key): value for key, value in state_dict.items()}

    def _check_keys(self, model, pretrained_state_dict):
        ckpt_keys = set(pretrained_state_dict.keys())
        model_keys = set(model.state_dict().keys())
        used_pretrained_keys = model_keys & ckpt_keys
        unused_pretrained_keys = ckpt_keys - model_keys
        missing_keys = model_keys - ckpt_keys
        print('Missing keys:{}'.format(len(missing_keys)))
        print('Unused checkpoint keys:{}'.format(len(unused_pretrained_keys)))
        print('Used keys:{}'.format(len(used_pretrained_keys)))
        assert len(used_pretrained_keys) > 0, 'load NONE from pretrained checkpoint'
        return True


if __name__ == '__main__':
    face_man = FaceDetector("../weights/FaceBoxes.pth")
    img_path = "../test/5007442.jpg"
    img = cv2.imread(img_path)
    res = face_man.inference(img)
    print(res[0])
    cv2.imshow('res', res[1])
    cv2.waitKey(0)
    pass