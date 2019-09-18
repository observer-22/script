import cv2
import os
from pathlib import Path
from concurrent.futures.thread import ThreadPoolExecutor


def get_path_list(f_type, file_path):
    file_list = [p for p in os.listdir(file_path) if p.endswith(f_type)]
    return file_list


def open_video(file_name, file_path):
    name = file_name.split('.')[0]
    saved_path = Path(name)
    is_exists = saved_path.exists()
    if not is_exists:
        new_path_save = str(Path.cwd().joinpath(str(saved_path)))
        os.makedirs(new_path_save)
        # 视频帧率12
        fps = 12
        # 保存图片的帧率间隔
        count = 2

        # 开始读视频
        video_capture = cv2.VideoCapture(f"{file_path}/{file_name}")

        i = 0
        j = 0

        while True:
            success, frame = video_capture.read()
            i += 1
            if i % count == 0:
                # 保存图片
                j += 1
                new_path = saved_path.joinpath(f"{name}_{str(j)}_{str(i)}.jpg")
                cv2.imwrite(str(new_path), frame)
                print(f"save --- {new_path}")
            if not success:
                print(f"end --- {name}")
                break


if __name__ == '__main__':
    #  视频文件存放路径
    file_path = r"E:\vedio"
    #  视频文件类型
    f_type = "mp4"
    #  同一时间最多处理视频文件数量
    max_workers = 5
    file_name_list = get_path_list(f_type, file_path)
    with ThreadPoolExecutor(max_workers=max_workers) as t:
        for path in file_name_list:
            obj = t.submit(open_video, path, file_path)

