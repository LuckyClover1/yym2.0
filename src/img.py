import cv2
import random
from src import global_
from src.tklog import Log


def sift_flann_func(template, matchPoint):
    img1 = cv2.imread(global_.local + template, 0)  # queryImage
    img2 = cv2.imread(global_.param.capture_img, 0)  # trainImage
    if matchPoint is None:
        matchPoint = 5
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # 指定算法
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # 指定递归次数

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    match_points = []
    for i, (m, n) in enumerate(matches):
        # 丢弃错误匹配，这里的0.7不知道是啥，反正效果挺好
        if m.distance < 0.97 * n.distance:
            # 匹配点位置
            x = kp2[m.trainIdx].pt[0]
            y = kp2[m.trainIdx].pt[1]
            # break;
            match_points.append((x, y))
    match_points.sort()
    width = img1.shape[1]
    height = img1.shape[0]
    x_0 = 0
    y_0 = 0
    p_count = 1
    for i, p in enumerate(match_points):
        if i == 0:
            x_0 = p[0]
            y_0 = p[1]
        elif abs(match_points[i - 1][0] - p[0]) < width \
                and abs(match_points[i - 1][1] - p[1]) < height:
            x_0 = x_0 + p[0]
            y_0 = y_0 + p[1]
            p_count = p_count + 1
    matchX = int(x_0 / p_count)
    matchY = int(y_0 / p_count)
    return (matchX, matchY)

#御魂匹配规则
def match_template(template):
    if template.find(",") > 0:
        tems = template.split(",")
        for tem in tems:
            img1 = cv2.imread(global_.resources + tem, 0)  # 模板

            img2 = cv2.imread(global_.param.capture_img, 0)  # 需要匹配的图片
            img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR);

            img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR);
            flann = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(flann)
            #Log.debug("------->匹配度：",str(max_val))
            if max_val >= 0.9:
                th, tw = img1.shape[:2]
                offset_x = int(random.randint(0, tw))
                offset_y = int(random.randint(0, th))
                return max_loc[0] + offset_x, max_loc[1] + offset_y

        return 0, 0
    else:
        img1 = cv2.imread(global_.resources + template, 0)  # 模板
        img2 = cv2.imread(global_.param.capture_img, 0)  # 需要匹配的图片
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR);
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR);
        flann = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(flann)
        #Log.debug("------->匹配度：",str(max_val))
        if max_val >= 0.9:
            th, tw = img1.shape[:2]
            if template.find("out") or template.find("attack") > 0: #解决退出图标太小,2倍缩小尺寸大小的坐标
                offset_x = int(random.randint(0, tw//2))
                offset_y = int(random.randint(0, th//2))
                return max_loc[0] + offset_x, max_loc[1] + offset_y
            else:
                offset_x = int(random.randint(0, tw))
                offset_y = int(random.randint(0,th ))
                return max_loc[0] + offset_x, max_loc[1] + offset_y

        return 0, 0

#探索匹配规则-离队状态
def match_template2(template):
    if template.find(",") > 0:
        tems = template.split(",")
        i = 0
        team = 0
        exploring = 0
        for tem in tems:
            img1 = cv2.imread(global_.resources + tem, 0)  # 模板
            img2 = cv2.imread(global_.param.capture_img, 0)  # 需要匹配的图片

            flann = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(flann)
            if i == 0:
                team = max_val
            else:
                exploring = max_val
            i = i + 1
        #print("组队-----------------")
        #print(team, exploring)
        if team < 0.85 and exploring >= 0.9: #没组队图标和在探索中，说明是离队状态
            return 1, 1
        else:
            return 0, 0

    else:
        img1 = cv2.imread(global_.resources + template, 0)  # 模板
        img2 = cv2.imread(global_.param.capture_img, 0)  # 需要匹配的图片

        flann = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(flann)

        #Log.debug("------->匹配度：",str(max_val))
        if max_val >= 0.9:
            th, tw = img1.shape[:2]
            offset_x = int(random.randint(0, tw))
            offset_y = int(random.randint(0, th))
            print( max_loc[0] + offset_x, max_loc[1] + offset_y)
            return max_loc[0] + offset_x, max_loc[1] + offset_y

        return 0, 0




