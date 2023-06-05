import os
import cv2
import pandas as pd
from glob import glob
from pathlib import Path
from pykinect_recorder.main._pyk4a.pykinect import initialize_libraries
from pykinect_recorder.main._pyk4a.k4arecord import Playback
from pykinect_recorder.main._pyk4a.k4arecord._k4arecord import K4A_PLAYBACK_SEEK_BEGIN


def colorize(
    image,
    clipping_range,
    colormap,
):
    if clipping_range[0] or clipping_range[1]:
        img = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
    else:
        img = image.copy()
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    img = cv2.applyColorMap(img, colormap)
    return img


if __name__ == '__main__':
    print(Path.home())
    initialize_libraries()
    file_paths = glob(os.path.join(Path.home(), "Downloads", "*.mkv"))
    root_path = 'datas'
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    offsets = [56000000 for _ in range(len(file_paths))]  ## micro time

    for i, file_path in enumerate(file_paths):    
        playback = Playback(file_path)
        playback.seek_timestamp(offset=offsets[i], origin=K4A_PLAYBACK_SEEK_BEGIN)
        file_name = file_path.split('\\')[-1][:-4]
        cnt = 0
        frame = 100
        color_h, color_w = None, None
        depth_h, depth_w = None, None

        while cnt < frame:
            ret, current_frame = playback.update()
            if ret:
                current_rgb_frame = current_frame.get_color_image()
                current_ir_frame = current_frame.get_ir_image()
                if current_ir_frame[0]:
                    ir_frame = colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
                    depth_h, depth_w, _ = ir_frame.shape
                    cv2.imwrite(os.path.join(root_path, f"{file_name}_ir_{str(cnt).zfill(6)}.png"), ir_frame)

                if current_rgb_frame[0]:
                    rgb_frame = current_rgb_frame[1]
                    color_h, color_w, _ = rgb_frame.shape
                    cv2.imwrite(os.path.join(root_path, f"{file_name}_rgb_{str(cnt).zfill(6)}.jpg"), rgb_frame)
                cnt += 1
            else:
                break
        
        df = pd.read_csv("metadata.csv")
        length = df.shape[0]
        df.loc[length] = [file_name, offsets[i], frame, f"'({color_h}, {color_w})'", f"'({depth_h}, {depth_w})'"]
        df.to_csv("metadata.csv", index=False)
        print(file_name)